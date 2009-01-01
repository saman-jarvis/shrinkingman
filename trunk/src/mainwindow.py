##
# Author: Samuel Abels <spam debain org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
##
from   gettext import gettext as _
import gnome
import gconf
import gobject
import gtk.glade
import os
import time
import datetime
import util
import tz
from   config           import c as cfg
from   food             import Food
from   day              import Day
from   aboutdialog      import AboutDialog
import filechooser
from   consumerdb       import ConsumerDB
from   consumerdb       import ConsumerDBGenerator
from   xml.sax          import make_parser
from   xml.sax.handler  import feature_namespaces


XML_DATADIR             = os.environ.get("HOME", os.getcwd()) + "/"
XML_FILE_CONSUMERDB     = XML_DATADIR + ".defaultdb.shriman"
GC_KEY_LAST_OPENED_FILE = "/apps/" + cfg["APP_SYSNAME"] + "/last_opened_file"


class MainWindow:
    def __init__(self):
        self.days         = {}
        self.lock_signals = False
        
        # Determine the last opened file.
        self.xml_file_consumerdb = XML_FILE_CONSUMERDB
        self.gconf_client        = gconf.client_get_default()
        val = self.gconf_client.get(GC_KEY_LAST_OPENED_FILE)
        if val:
            last_opened_file = val.get_string()
            if (last_opened_file
                and os.path.isfile(last_opened_file)):
                self.xml_file_consumerdb = last_opened_file
        
        # Lookup all widgets.
        gladefile = cfg["APP_SYSNAME"] + ".glade"
        callback  = self.on_treeview_selection_changed
        self.xml                   = util.get_glade_xml(gladefile, "mainwindow")
        self.window                = self.xml.get_widget('mainwindow')
        self.treeview              = self.xml.get_widget('treeview_caleditor')
        self.treeview_selection    = self.treeview.get_selection()
        self.treeview_selection_hd = self.treeview_selection.connect("changed",
                                                                     callback)
        self.calendar              = self.xml.get_widget('calendar')
        self.spinbutton_weight     = self.xml.get_widget('spinbutton_weight')
        self.combobox_food         = self.xml.get_widget('comboboxentry_food')
        self.comboboxentry_food    = self.combobox_food.get_child()
        self.spinbutton_quantity   = self.xml.get_widget('spinbutton_quantity')
        self.spinbutton_energy     = self.xml.get_widget('spinbutton_energy')
        self.spinbutton_hour       = self.xml.get_widget('spinbutton_hour')
        self.spinbutton_minute     = self.xml.get_widget('spinbutton_minute')
        self.notebook_buttonbox    = self.xml.get_widget('notebook_buttonbox')
        self.label_energy_sum      = self.xml.get_widget('label_energy_sum')
        self.dialog_about          = None
        self.xml.signal_autoconnect(self)
        
        # Init widgets.
        t = time.localtime(time.time())
        self.spinbutton_hour.set_value(t[3])
        self.spinbutton_minute.set_value(t[4])
        
        # Init the listview.
        self.model = gtk.ListStore(gobject.TYPE_PYOBJECT,
                                   gobject.TYPE_STRING,
                                   gobject.TYPE_STRING,
                                   gobject.TYPE_STRING,
                                   gobject.TYPE_STRING,
                                   gobject.TYPE_STRING)
        
        renderer = gtk.CellRendererText()
        column   = gtk.TreeViewColumn(_("Food"), renderer, text = 1)
        column.set_sort_column_id(1)
        column.set_resizable(True)
        column.set_expand(True)
        self.treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column   = gtk.TreeViewColumn(_("Calories"), renderer, text = 2)
        column.set_sort_column_id(2)
        column.set_resizable(True)
        self.treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column   = gtk.TreeViewColumn(_("Quantity"), renderer, text = 3)
        column.set_sort_column_id(3)
        column.set_resizable(True)
        self.treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column   = gtk.TreeViewColumn(_("Time"), renderer, text = 4)
        column.set_sort_column_id(5)
        column.set_resizable(True)
        self.treeview.append_column(column)

        self.treeview.set_model(self.model)
        self.treeview.set_headers_clickable(True)
        self.treeview.set_rules_hint(True)
        self.model.set_sort_column_id(5, gtk.SORT_ASCENDING)
        
        # Finally, load the user data.
        self.load_days()
        self.on_calendar_day_selected(self.calendar)
        
    ################################################################
    # Data access methods.
    ################################################################
    # Clears the user's consumed food data.
    def clear_days(self):
        self.model.clear()
        self.days = {}
        self.update_title()
        
    # Loads the user data from the currently opened file.
    def load_days(self):
        if not os.path.isfile(self.xml_file_consumerdb):
            return
        parser = make_parser()
        db     = ConsumerDB()
        parser.setFeature(feature_namespaces, 0)
        parser.setContentHandler(db)
        parser.parse(self.xml_file_consumerdb)
        self.clear_days()
        self.days = db.getDays()
        self.gconf_client.set_string(GC_KEY_LAST_OPENED_FILE,
                                     self.xml_file_consumerdb)

        # Trigger a user interface update.
        self.on_calendar_day_selected(self.calendar)
        
    # Saves the user data to the currently opened file.
    def save_days(self):
        gen = ConsumerDBGenerator()
        gen.generate(self.xml_file_consumerdb, self.days)
        self.update_title()
        self.gconf_client.set_string(GC_KEY_LAST_OPENED_FILE,
                                     self.xml_file_consumerdb)
    
    ################################################################
    # UI interaction.
    ################################################################
    # Updates a single row in the listview.
    def update_food_in_treeview(self, iter, food):
        self.model.set_value(iter, 0, food)
        self.model.set_value(iter, 1, food.name)
        self.model.set_value(iter, 2, food.energy)
        self.model.set_value(iter, 3, food.quantity)
        self.model.set_value(iter, 4, food.time.strftime("%X"))
        self.model.set_value(iter, 5, food.time.isoformat())
    
    # Updates the number of calories consumed today.
    def update_energy_sum(self, day):
        sum = 0
        for food in day.get_foods():
            sum = sum + (food.energy * food.quantity)
        text = _("Calories consumed today: %i") % sum
        self.label_energy_sum.set_text(text)

    # Updates the given food in the form. If no food is given,
    # the form is reset to default values.
    def update_food_form(self, food):
        self.lock_signals = True
        if not food:
            food = Food(_("Food"))
            self.comboboxentry_food.set_text("")
        else:
            self.comboboxentry_food.set_text(food.name)
        self.spinbutton_quantity.set_value(food.quantity)
        self.spinbutton_energy.set_value(food.energy)
        self.spinbutton_hour.set_value(food.time.hour)
        self.spinbutton_minute.set_value(food.time.minute)
        self.lock_signals = False
    
    # Returns a food object that represents the current contents of the form.
    # Returns None if the form has no food name entered.
    def get_food_from_form(self):
        foodname = self.comboboxentry_food.get_text()
        if len(foodname) <= 0:
            return
        hour     = int(self.spinbutton_hour.get_value())
        minute   = int(self.spinbutton_minute.get_value())
        time     = datetime.time(hour, minute, 0, 0, tz.LocalTimezone())
        date     = self.get_calendar_date()
        date     = date.combine(date, time)
        quantity = round(self.spinbutton_quantity.get_value(), 2)
        food = Food(foodname)
        food.set_quantity(quantity)
        food.set_energy(self.spinbutton_energy.get_value())
        food.set_time(date)
        return food
        
    # Returns the currently selected date as a datetime object.
    def get_calendar_date(self):
        year, month, day = self.calendar.get_date()
        # This sucks: GtkCalendar returns a zero-based month.
        month = month + 1
        tmz   = tz.LocalTimezone()
        date  = datetime.datetime(year, month, day, 0, 0, 0, 0, tmz)
        return date
        
    # Selects the given date in the calendar.
    def set_calendar_date(self, date):
        self.calendar.select_day(1)
        self.calendar.select_month(date.month - 1, date.year)
        self.calendar.select_day(date.day)
        
    # Returns the currently selected day.
    def get_selected_day(self):
        # Return the day if it already exists.
        today_date = self.get_calendar_date()
        today      = self.days.setdefault(today_date.ctime(), Day(today_date))
        if today.get_weight() > 0:
            return today

        # If it was newly instantiated (get_weight == 0) above, inherit the
        # weight from the previous day.
        offset         = datetime.timedelta(1)
        yesterday_date = today_date - offset
        yesterday      = self.days.get(yesterday_date.ctime())
        if yesterday:
            today.set_weight(yesterday.get_weight())
            return today

        # If the previous day was not yet instantiated, get the default weight
        # from the form.
        weight = round(self.spinbutton_weight.get_value(), 2)
        today.set_weight(weight)
        return today
        
    # Updates the window title.
    def update_title(self):
        file = os.path.basename(self.xml_file_consumerdb)
        self.window.set_title(file)
        
    ################################################################
    # Callbacks.
    ################################################################
    def on_delete_event(*args):
        gtk.main_quit()
    
    def on_button_add_pressed(self, widget):
        food = self.get_food_from_form()
        if not food:
            return

        # Attach the food to the current day and update the GUI.
        self.treeview_selection.handler_block(self.treeview_selection_hd)
        day = self.get_selected_day()
        day.add_food(food)
        iter = self.model.append()
        self.update_food_in_treeview(iter, food)
        self.update_food_form(None)
        self.update_energy_sum(day)
        self.treeview_selection.handler_unblock(self.treeview_selection_hd)

        self.save_days()
    
    def on_button_delete_pressed(self, widget):
        model, iter = self.treeview_selection.get_selected()
        if not iter:
            return
        food = model.get_value(iter, 0)
        day  = self.get_selected_day()
        day.remove_food(food)
        self.update_energy_sum(day)
        self.model.remove(iter)
        self.save_days()
        self.update_food_form(None)
        self.notebook_buttonbox.set_current_page(0)

    def on_button_newform_pressed(self, widget):
        self.update_food_form(None)
        self.notebook_buttonbox.set_current_page(0)
        self.treeview_selection.unselect_all()

    def on_treeview_selection_changed(self, selection):
        model, iter = self.treeview_selection.get_selected()
        if not iter:
            return

        self.treeview_selection.handler_block(self.treeview_selection_hd)
        self.notebook_buttonbox.set_current_page(1)
        food = model.get_value(iter, 0)
        self.update_food_form(food)
        self.treeview_selection.handler_unblock(self.treeview_selection_hd)
    
    def on_spinbutton_weight_value_changed(self, widget):
        date = self.get_selected_day()
        #FIXME: We should implement a timer to do this.
        self.save_days() 

    def on_comboboxentry_food_changed(self, widget):
        self.on_entry_changed(widget)

    def on_spinbutton_energy_value_changed(self, widget):
        self.on_entry_changed(widget)

    def on_spinbutton_quantity_value_changed(self, widget):
        self.on_entry_changed(widget)

    def on_spinbutton_hour_value_changed(self, widget):
        self.on_entry_changed(widget)

    def on_spinbutton_minute_value_changed(self, widget):
        self.on_entry_changed(widget)

    def on_entry_changed(self, widget):
        if self.lock_signals:
            return

        # A name is required and a row must be selected.
        foodname    = self.comboboxentry_food.get_text()
        model, iter = self.treeview_selection.get_selected()
        if len(foodname) <= 0 or not iter:
            return
        
        # Re-save the data.
        self.lock_signals = True
        day     = self.get_selected_day()
        oldfood = model.get_value(iter, 0)
        food    = self.get_food_from_form()
        day.add_food(food)
        day.remove_food(oldfood)
        self.update_food_in_treeview(iter, food)
        self.update_energy_sum(day)
        #FIXME: We should implement a timer to do this.
        self.save_days()
        self.lock_signals = False
    
    def on_calendar_day_selected(self, widget):
        self.model.clear()
        self.notebook_buttonbox.set_current_page(0)
        today = self.get_selected_day()
        self.spinbutton_weight.set_value(today.get_weight())
        if not today:
            return
        
        for food in today.get_foods():
            iter = self.model.append()
            self.update_food_in_treeview(iter, food)
        self.update_energy_sum(today)
    
    ################################################################
    # Menu callbacks.
    ################################################################
    def on_menu_file_new_activate(self, widget):
        fc   = filechooser.create_filechooser_save()
        path = os.path.dirname(self.xml_file_consumerdb)
        if path != "":
            fc.set_current_folder(path)
        fc.set_current_name(_("unnamed.shriman"))
        response = fc.run()
        if response == gtk.RESPONSE_OK:
            self.xml_file_consumerdb = fc.get_filename()
            self.clear_days()
        fc.destroy()

    def on_menu_file_open_activate(self, widget):
        fc   = filechooser.create_filechooser_open()
        path = os.path.dirname(self.xml_file_consumerdb)
        if path != "":
            fc.set_current_folder(path)
        response = fc.run()
        if response == gtk.RESPONSE_OK:
            self.xml_file_consumerdb = fc.get_filename()
            self.load_days()
        fc.destroy()
    
    def on_menu_file_save_as_activate(self, widget):
        fc   = filechooser.create_filechooser_save()
        path = os.path.dirname(self.xml_file_consumerdb)
        file = os.path.basename(self.xml_file_consumerdb)
        if path != "":
            fc.set_current_folder(path)
        if file != "":
            fc.set_current_name(file)
        response = fc.run()
        if response == gtk.RESPONSE_OK:
            self.xml_file_consumerdb = fc.get_filename()
            self.save_days()
        fc.destroy()
        
    def on_menu_file_quit_activate(self, widget):
        gtk.main_quit()

    def on_menu_edit_cut_activate(self, widget):
        widget = self.window.get_focus()
        if not hasattr(widget, "cut_clipboard"):
            return
        widget.cut_clipboard()

    def on_menu_edit_copy_activate(self, widget):
        widget = self.window.get_focus()
        if not hasattr(widget, "copy_clipboard"):
            return
        widget.copy_clipboard()

    def on_menu_edit_paste_activate(self, widget):
        widget = self.window.get_focus()
        if not hasattr(widget, "paste_clipboard"):
            return
        widget.paste_clipboard()

    def on_menu_edit_delete_activate(self, widget):
        widget = self.window.get_focus()
        if not hasattr(widget, "delete_selection"):
            return
        widget.delete_selection()

    def on_menu_view_previous_day_activate(self, widget):
        date   = self.get_calendar_date()
        offset = datetime.timedelta(1)
        date   = date - offset
        self.set_calendar_date(date)
        
    def on_menu_view_next_day_activate(self, widget):
        date   = self.get_calendar_date()
        offset = datetime.timedelta(1)
        date   = date + offset
        self.set_calendar_date(date)

    def on_menu_view_today_activate(self, widget):
        date = datetime.datetime.now()
        self.set_calendar_date(date)

    def on_menu_help_about_activate(self, widget):
        if not self.dialog_about:
            self.dialog_about = AboutDialog()
        self.dialog_about.show()

    ################################################################
    # Toolbutton callbacks.
    ################################################################
    def on_toolbutton_new_clicked(self, widget):
        self.on_menu_file_new_activate(widget)

    def on_toolbutton_open_clicked(self, widget):
        self.on_menu_file_open_activate(widget)

    def on_toolbutton_previous_day_clicked(self, widget):
        self.on_menu_view_previous_day_activate(widget)

    def on_toolbutton_next_day_clicked(self, widget):
        self.on_menu_view_next_day_activate(widget)

    def on_toolbutton_today_clicked(self, widget):
        self.on_menu_view_today_activate(widget)
