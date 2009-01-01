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
import config           as     cfg
from   food             import Food
from   day              import Day
from   aboutdialog      import AboutDialog
import filechooser
from   consumerdb       import ConsumerDB
from   consumerdb       import ConsumerDBGenerator
from   xml.sax          import make_parser
from   xml.sax.handler  import feature_namespaces


XML_GLADEFILE           = "shriman.glade"
XML_DATADIR             = os.environ.get("HOME", os.getcwd()) + "/"
XML_DATAFILE            = XML_DATADIR + ".defaultdb.shriman"
GC_KEY_LAST_OPENED_FILE = "/apps/" + cfg.APP_SYSNAME + "/last_opened_file"


class MainWindow:
    def __init__(self):
        self.days         = {}
        self.lock_signals = False
        
        self.datafile     = XML_DATAFILE
        self.gc           = gconf.client_get_default()
        gc_val            = self.gc.get(GC_KEY_LAST_OPENED_FILE)
        if gc_val:
            last_opened_file = gc_val.get_string()
            if (last_opened_file
                and os.path.isfile(last_opened_file)):
                self.datafile = last_opened_file

        self.xml          = util.get_glade_xml(XML_GLADEFILE)
        self.window       = self.xml.get_widget('mainwindow')
        self.treeview     = self.xml.get_widget('treeview_caleditor')
        self.calendar     = self.xml.get_widget('calendar')
        self.weight       = self.xml.get_widget('spinbutton_weight')
        self.food         = self.xml.get_widget('comboboxentry_food').get_child()
        self.quantity     = self.xml.get_widget('spinbutton_quantity')
        self.energy       = self.xml.get_widget('spinbutton_energy')
        self.hour         = self.xml.get_widget('spinbutton_hour')
        self.minute       = self.xml.get_widget('spinbutton_minute')
        self.buttonbox    = self.xml.get_widget('notebook_buttonbox')
        self.aboutdialog  = None
        
        t = time.localtime(time.time())
        self.hour.set_value(t[3])
        self.minute.set_value(t[4])
        
        self.model = gtk.ListStore(gobject.TYPE_PYOBJECT,
                                   gobject.TYPE_STRING,
                                   gobject.TYPE_STRING,
                                   gobject.TYPE_STRING,
                                   gobject.TYPE_STRING,
                                   gobject.TYPE_STRING)
        
        i = 0
        for name in (_("Food"), _("Calories"), _("Quantity"), _("Date")):
            i = i + 1
            renderer = gtk.CellRendererText()
            column   = gtk.TreeViewColumn(name, renderer, text = i)
            if i == 4:
                column.set_sort_column_id(5)
            else:
                column.set_sort_column_id(i)
            self.treeview.append_column(column)
        self.treeview.set_model(self.model)
        self.treeview.set_headers_clickable(True)
        self.treeview.set_rules_hint(True)
        self.model.set_sort_column_id(5, gtk.SORT_ASCENDING)
        self.selection = self.treeview.get_selection()
        self.selecthd  = self.selection.connect(
                               "changed", self.on_treeview_selection_changed)
        self.xml.signal_autoconnect(self)

        self.days_load()
        self.on_calendar_day_selected(self.calendar)
        
    def update_food_in_treeview(self, iter, food):
        self.model.set_value(iter, 0, food)
        self.model.set_value(iter, 1, food.name)
        self.model.set_value(iter, 2, food.energy)
        self.model.set_value(iter, 3, food.quantity)
        self.model.set_value(iter, 4, food.time.strftime("%x %X"))
        self.model.set_value(iter, 5, food.time.isoformat())
    
    def update_food_in_form(self, food_):
        self.lock_signals = True
        if food_:
            food = food_
            self.food.set_text(food.name)
        else:
            food = Food(_("Food"))
            self.food.set_text("")
        self.quantity.set_value(food.quantity)
        self.energy.set_value(food.energy)
        self.hour.set_value(food.time.hour)
        self.minute.set_value(food.time.minute)
        self.lock_signals = False
    
    def get_calendar_date(self):
        year, month, day = self.calendar.get_date()
        # This sucks: GtkCalendar returns a zero-based month.
        month = month + 1
        tmz   = tz.LocalTimezone()
        date  = datetime.datetime(year, month, day, 0, 0, 0, 0, tmz)
        return date
        
    def set_calendar_date(self, date):
        self.calendar.select_day(1)
        self.calendar.select_month(date.month - 1, date.year)
        self.calendar.select_day(date.day)
        
    def get_selected_day(self):
        date = self.get_calendar_date()
        if self.days.has_key(date.ctime()):
            day = self.days[date.ctime()]
        else:
            day = Day(date)
            self.days[date.ctime()] = day
        day.set_weight(self.weight.get_value())
        return day
        
    def get_food_from_form(self):
        foodname = self.food.get_text()
        if len(foodname) <= 0: return
        hour     = int(self.hour.get_value())
        minute   = int(self.minute.get_value())
        time     = datetime.time(hour, minute, 0, 0, tz.LocalTimezone())
        date     = self.get_calendar_date()
        date     = date.combine(date, time)
        quantity = round(self.quantity.get_value(), 2)
        food = Food(foodname)
        food.set_quantity(quantity)
        food.set_energy(self.energy.get_value())
        food.set_time(date)
        return food
        
    def update_title(self):
        file = os.path.basename(self.datafile)
        self.window.set_title("Shrinking Man - " + file)
        
    def days_clear(self):
        self.model.clear()
        self.days = {}
        self.update_title()
        
    def days_load(self):
        if not os.path.isfile(self.datafile): return
        parser = make_parser()
        db     = ConsumerDB()
        parser.setFeature(feature_namespaces, 0)
        parser.setContentHandler(db)
        parser.parse(self.datafile)
        self.days_clear()
        self.days = db.getDays()
        self.on_calendar_day_selected(self.calendar)
        self.gc.set_string(GC_KEY_LAST_OPENED_FILE, self.datafile)
        
    def days_save(self):
        gen = ConsumerDBGenerator()
        gen.generate(self.datafile, self.days)
        self.update_title()
        self.gc.set_string(GC_KEY_LAST_OPENED_FILE, self.datafile)

    def on_delete_event(*args):
        gtk.main_quit()
    
    def on_button_add_pressed(self, widget):
        self.selection.handler_block(self.selecthd)
        food = self.get_food_from_form()
        if not food: return
        day  = self.get_selected_day()
        day.add_food(food)
        iter = self.model.append()
        self.model.set_value(iter, 0, food)
        self.update_food_in_treeview(iter, food)
        self.update_food_in_form(None)
        self.selection.handler_unblock(self.selecthd)
        self.days_save()
    
    def on_button_delete_pressed(self, widget):
        model, iter = self.selection.get_selected()
        if not iter: return
        food = model.get_value(iter, 0)
        day  = self.get_selected_day()
        day.remove_food(food)
        self.model.remove(iter)
        self.days_save()
        self.update_food_in_form(None)
        self.buttonbox.set_current_page(0)

    def on_button_newform_pressed(self, widget):
        self.update_food_in_form(None)
        self.buttonbox.set_current_page(0)
        self.selection.unselect_all()

    def on_treeview_selection_changed(self, selection):
        model, iter = self.selection.get_selected()
        if not iter: return
        self.selection.handler_block(self.selecthd)
        self.buttonbox.set_current_page(1)
        food = model.get_value(iter, 0)
        self.update_food_in_form(food)
        self.selection.handler_unblock(self.selecthd)
    
    def on_spinbutton_weight_value_changed(self, widget):
        date = self.get_selected_day()
        #FIXME: We should implement a timer to do this.
        self.days_save() 

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
        if self.lock_signals: return
        model, iter = self.selection.get_selected()
        if not iter: return
        foodname = self.food.get_text()
        if len(foodname) <= 0: return
        
        day     = self.get_selected_day()
        oldfood = model.get_value(iter, 0)
        food    = self.get_food_from_form()
        day.add_food(food)
        day.remove_food(oldfood)
        self.update_food_in_treeview(iter, food)
        #FIXME: We should implement a timer to do this.
        self.days_save()
    
    def on_calendar_day_selected(self, widget):
        self.model.clear()
        self.buttonbox.set_current_page(0)
        self.weight.set_text("40")
        date = self.get_calendar_date()
        if not self.days.has_key(date.ctime()): return
        weight = self.days[date.ctime()].get_weight()
        self.weight.set_value(weight)

        for food in self.days[date.ctime()].get_foods():
            iter = self.model.append()
            self.update_food_in_treeview(iter, food)
    
    def on_menu_file_new_activate(self, widget):
        fc = filechooser.create_filechooser_save()
        path = os.path.dirname(self.datafile)
        if path != "":
            fc.set_current_folder(path)
        fc.set_current_name(_("unnamed.shriman"))
        response = fc.run()
        if response == gtk.RESPONSE_OK:
            self.datafile = fc.get_filename()
            self.days_clear()
        fc.destroy()

    def on_menu_file_open_activate(self, widget):
        fc = filechooser.create_filechooser_open()
        path = os.path.dirname(self.datafile)
        if path != "":
            fc.set_current_folder(path)
        response = fc.run()
        if response == gtk.RESPONSE_OK:
            self.datafile = fc.get_filename()
            self.days_load()
        fc.destroy()
    
    def on_menu_file_save_as_activate(self, widget):
        fc   = filechooser.create_filechooser_save()
        path = os.path.dirname(self.datafile)
        file = os.path.basename(self.datafile)
        if path != "":
            fc.set_current_folder(path)
        if file != "":
            fc.set_current_name(file)
        response = fc.run()
        if response == gtk.RESPONSE_OK:
            self.datafile = fc.get_filename()
            self.days_save()
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
        if not self.aboutdialog:
            self.aboutdialog = AboutDialog()
        self.aboutdialog.show()

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

