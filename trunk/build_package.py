#!/usr/bin/env python
import usda2sql
import os
import sys
import glob
import shutil
sys.path.append("src/")
from   config import c as cfg

files = ["AUTHORS", "ChangeLog", "COPYING", "INSTALL", "README"]
files = files + glob.glob("pixmaps/*.png")
files = files + glob.glob("pixmaps/*.svg")
files = files + glob.glob("src/*py")
files = files + glob.glob("*.py")
files.append("shrinkingman.desktop.in")
files.append("shrinkingman.glade")
files.append("shrinkingman.xml.in")
files.append("usda.db")
files.append("usda.sql")

# Create temporary directory.
if os.path.isdir(cfg["APP_SYSNAME"]):
    shutil.rmtree(cfg["APP_SYSNAME"])
os.makedirs(cfg["APP_SYSNAME"])

# Copy the files into that dir.
for file in files:
    print file
    dir = cfg["APP_SYSNAME"] + "/" + os.path.dirname(file)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    shutil.copy(file, dir)

# Make a tarball.
tarball = cfg["APP_SYSNAME"] + "-" + cfg["APP_VERSION"] + "-1.tar.gz"
os.system("tar czf " + tarball + " " + cfg["APP_SYSNAME"])

# Remove the temporary directory.
shutil.rmtree(cfg["APP_SYSNAME"])
