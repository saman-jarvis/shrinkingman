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
from   config  import c as cfg
import gtk
import util

LOGO = "person.png"

class AboutDialog:
    def __init__(self):
        self.about = gtk.AboutDialog()
        self.about.set_version(cfg["APP_VERSION"])
        self.about.set_copyright(_("Copyright 2005 by Samuel Abels"))
        self.about.set_license(_("Licensed under the General Public License (GPL), Version 2.0"));
        self.about.set_website("http://debain.org/software/shrinkingman/")
        self.about.set_website_label(_("Homepage"))
        self.about.set_authors([_("Samuel Abels <spam debain org>")])
        logo = util.get_pixbuf(LOGO)
        self.about.set_logo(logo)

    def show(self):
        self.about.show()
