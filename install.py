#!/usr/bin/python -O
import os
import sys
import stat
import glob
import shutil
sys.path.append("src/")
from   config import c as cfg
inst = {}


##########################################
# Helper functions
##########################################
def install_file(name, dir):
    print "Copying file", name, "to", dir, "..."
    shutil.copy(file, dir)


def remove_dir(name):
    if os.path.isdir(name):
        print "Removing", name, "..."
        files = glob.glob(name + "*.py*")
        files = files + glob.glob(name + "*.glade")
        files = files + glob.glob(name + "*.png")
        for file in files:
            os.remove(file)
        os.rmdir(name)


def gen_file(name):
    print "Generating", name, "..."
    infile  = file(name + ".in")
    content = infile.read(20000)
    for key in cfg:
        content = content.replace("%" + key + "%", cfg[key])
    outfile = file(name, "w")
    outfile.write(content)


##########################################
# Config
##########################################
# Desktop file name and installation location.
desktopfile       = cfg["APP_SYSNAME"] + ".desktop"
inst[desktopfile] = cfg["INSTALL_MENU_XDG"]
gen_file(desktopfile)

# Icon file names and installation locations.
iconname                   = cfg["APP_SYSNAME"] + ".png"
inst["pixmaps/icon32.png"] = cfg["INSTALL_ICON"] + "32x32/apps/" + iconname
inst["pixmaps/icon48.png"] = cfg["INSTALL_ICON"] + "48x48/apps/" + iconname

# Mime type definition file.
mime_xml_file       = cfg["APP_SYSNAME"] + ".xml"
inst[mime_xml_file] = cfg["INSTALL_MIME_XML"]
gen_file(mime_xml_file)

# Mime .keys file name and installation location.
#mime_key_file       = cfg["APP_SYSNAME"] + ".keys"
#inst[mime_key_file] = cfg["INSTALL_MIME_KEYS"]
#cfg["MIME_ICON"]    = inst["pixmaps/icon48.png"] # Hack for mime.keys file
#gen_file(mime_key_file)

# Mime .mime file name and installation location.
#mime_mime_file       = cfg["APP_SYSNAME"] + ".mime"
#inst[mime_mime_file] = cfg["INSTALL_MIME_KEYS"]
#gen_file(mime_mime_file)

# Pixmap file installation locations.
inst["pixmaps/person.png"] = cfg["INSTALL_PIXMAP"]

# Date file installation locations.
gladefile       = cfg["APP_SYSNAME"] + ".glade"
inst[gladefile] = cfg["INSTALL_SHARE"]

# Library files.
inst["src/*.py"] = cfg["INSTALL_LIB"]


##########################################
# Cleanup older installations.
##########################################
print "Cleaning up older installations..."
remove_dir(cfg["INSTALL_LIB_PFX"]   + "shriman/")
remove_dir(cfg["INSTALL_SHARE_PFX"] + "shriman/")
if os.path.isfile(cfg["INSTALL_BIN_FILE"]):
    os.remove(cfg["INSTALL_BIN_FILE"])


##########################################
# Start.
##########################################
print "Installing new version..."
for pattern in inst:
    dirname = os.path.dirname(inst[pattern])
    if not os.path.isdir(dirname):
        print "Creating directory", dirname, "..."
        os.makedirs(dirname)
    files = glob.glob(pattern)
    for file in files:
      if not file.endswith("CVS"):
        install_file(file, inst[pattern])


print "Changing permission of the root script to 755..."
binfile = cfg["INSTALL_LIB"] + cfg["APP_SYSNAME"] + ".py"
os.chmod(binfile, stat.S_IRWXU
                | stat.S_IRGRP | stat.S_IXGRP
                | stat.S_IROTH | stat.S_IXOTH)

print "Creating application symlink..."
os.symlink(binfile, cfg["INSTALL_BIN_FILE"])

print "Running MIME database update..."
os.system("update-mime-database " + cfg["INSTALL_MIME_PFX"])

print "Compiling the application..."
os.chdir(cfg["INSTALL_LIB"])
sys.path.append(cfg["INSTALL_LIB"])
import shrinkingman     # Causes compilation of the program

print "Installation successfully completed!"
print "To start", cfg["APP_NAME"] + ", type", cfg["APP_SYSNAME"]
