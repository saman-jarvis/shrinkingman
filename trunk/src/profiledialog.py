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
import gtk.glade
import util
from   config  import c as cfg
from   profile import Profile


class ProfileDialog:
    def __init__(self, profile):
        self.profile = profile
        self.xml     = util.get_glade_xml(cfg["APP_SYSNAME"] + ".glade",
                                          "profile")
        self.window  = self.xml.get_widget('profile')
        self.entry   = self.xml.get_widget('entry_name')
        self.height  = self.xml.get_widget('spinbutton_height')
        self.gender  = self.xml.get_widget('combobox_gender')
        self.update_form()
        self.xml.signal_autoconnect(self)
        #self.lock_signals = False

    def update_form(self):
        self.entry.set_text(self.profile.get_name())
        self.height.set_value(self.profile.get_height())
        self.gender.set_active(self.profile.get_gender())

    def on_button_close_pressed(self, widget):
        self.window.destroy()

    def on_entry_name_changed(self, widget):
        name = self.entry.get_text()
        if len(name) <= 0:
            return
        self.profile.set_name(name)

    def on_spinbutton_height_value_changed(self, widget):
        self.profile.set_height(self.height.get_value())

    def on_combobox_gender_changed(self, widget):
        self.profile.set_gender(self.gender.get_active())


if __name__ == '__main__':
    profile = Profile("test")
    dialog  = ProfileDialog(profile)
    gnome.init(cfg["APP_NAME"], cfg["APP_VERSION"])
    gtk.main()
