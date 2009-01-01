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
import gtk

def add_filters(filechooser):
    filter = gtk.FileFilter()
    filter.set_name("Shrinking Man files")
    filter.add_pattern("*.shriman")
    filechooser.add_filter(filter)
    
    filter = gtk.FileFilter()
    filter.set_name("All XML files")
    filter.add_mime_type("text/xml")
    filechooser.add_filter(filter)

    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    filechooser.add_filter(filter)

def create_filechooser_open():
    buttons     = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                   gtk.STOCK_OPEN,   gtk.RESPONSE_OK)
    filechooser = gtk.FileChooserDialog("Open...",
                                        None,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        buttons)
    add_filters(filechooser)
    return filechooser


def create_filechooser_save():
    buttons     = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                   gtk.STOCK_SAVE,   gtk.RESPONSE_OK)
    filechooser = gtk.FileChooserDialog("Save...",
                                        None,
                                        gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons)
    filechooser.set_do_overwrite_confirmation(True)
    add_filters(filechooser)
    return filechooser
