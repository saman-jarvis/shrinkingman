#!/usr/bin/python
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
import sys, os, gettext, locale
import gnome
import gtk.glade
from   config     import c as cfg
from   mainwindow import MainWindow

if __name__ == '__main__':
    # Locale and I18N stuff
    os.environ['LC_NUMERIC'] = 'C'
    locale.setlocale        (locale.LC_NUMERIC, 'C')
    gettext.bindtextdomain  (cfg["GETTEXT_PACKAGE"], cfg["INSTALL_LOCALE"])
    gettext.textdomain      (cfg["GETTEXT_PACKAGE"])
    gtk.glade.bindtextdomain(cfg["GETTEXT_PACKAGE"], cfg["INSTALL_LOCALE"])
    try:
        gtk.glade.textdomain(cfg["GETTEXT_PACKAGE"])
    except AttributeError:
        print "gtk.glade.textdomain not found; i18n will not work"

    gnome.init(cfg["APP_NAME"], cfg["APP_VERSION"])
    window = MainWindow()
    gtk.main()
