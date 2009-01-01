#!/usr/bin/python -O
import os
import sys
import stat
import glob
import shutil
sys.path.append("src/")
import config as cfg


desktopfile = cfg.APP_NAME + ".desktop"

inst = {}
inst["pixmaps/person.png"] = cfg.INSTALL_PIXMAP
inst["pixmaps/icon32.png"] = cfg.INSTALL_ICON + "32x32/apps/shrinkingman.png"
inst["pixmaps/icon48.png"] = cfg.INSTALL_ICON + "48x48/apps/shrinkingman.png"
inst["shriman.glade"]      = cfg.INSTALL_SHARE
inst[desktopfile]          = cfg.INSTALL_MENU_XDG
inst["src/*.py"]           = cfg.INSTALL_LIB

def install_file(name, dir):
    print "Copying file", name, "to", dir
    shutil.copy(file, dir)


def gen_desktop_file(name):
    infile  = file(name + ".in")
    content = infile.read(20000)
    content = content.replace("%APP_NAME%",    cfg.APP_NAME)
    content = content.replace("%APP_SYSNAME%", cfg.APP_SYSNAME)
    content = content.replace("%INSTALL_BIN%", cfg.INSTALL_BIN)
    outfile = file(name, "w")
    outfile.write(content)


##########################################
# Start
##########################################
gen_desktop_file(cfg.APP_NAME + ".desktop")

for pattern in inst:
    dirname = os.path.dirname(inst[pattern])
    if not os.path.isdir(dirname):
        print "Creating directory", dirname
        os.makedirs(dirname)
    files = glob.glob(pattern)
    for file in files:
      if not file.endswith("CVS"):
        install_file(file, inst[pattern])


binfile = cfg.INSTALL_LIB + cfg.APP_SHORT_SYSNAME + ".py"

print "Changing permissions."
# That's permission 755
os.chmod(binfile, stat.S_IRWXU
                | stat.S_IRGRP | stat.S_IXGRP
                | stat.S_IROTH | stat.S_IXOTH)

print "Creating application symlink."
os.remove(cfg.INSTALL_BIN + cfg.APP_SYSNAME)
os.symlink(binfile, cfg.INSTALL_BIN + cfg.APP_SYSNAME)

print "Compiling the application..."
sys.path.append(cfg.INSTALL_LIB)
import shriman     # Causes compilation of the program

print "Installation successfully completed!"
print "To start", cfg.APP_NAME + ", type", cfg.APP_SYSNAME
