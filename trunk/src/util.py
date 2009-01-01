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
import os
import sys
import string
import gtk
import gtk.glade
from   config import c as cfg


def get_pixbuf(basename):
    file = cfg["INSTALL_PIXMAP"] + basename
    if not os.path.isfile(file):
        file = os.path.dirname(sys.argv[0]) + "/../pixmaps/" + basename
    pixbuf = None
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(file)
    except:
        print "Error:", file, "not found."
    return pixbuf

def get_glade_xml(basename):
    file = cfg["INSTALL_SHARE"] + basename
    if not os.path.isfile(file):
        file = os.path.dirname(sys.argv[0]) + "/../" + basename
    xml = None
    try:
        xml = gtk.glade.XML(file)
    except:
        print "Error:", file, "not found."
    return xml
