#!/usr/bin/python -O
import os
import sys
import stat
import glob
import shutil
sys.path.append("src/")
import config as cfg


inst = {}
inst["pixmaps/*"]     = cfg.INSTALL_PIXMAP
inst["src/*.py"]      = cfg.INSTALL_LIB
inst["shriman.glade"] = cfg.INSTALL_SHARE

def install_file(name, dir):
    print "Copying file", name, "to", dir
    shutil.copy(file, dir)

for pattern in inst:
    if not os.path.isdir(inst[pattern]):
        print "Creating directory", inst[pattern]
        os.makedirs(inst[pattern])
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
