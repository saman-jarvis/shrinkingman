from os.path import join
c = {}

# Application config.
c["APP_VERSION"]     = "0.2.1"
c["APP_NAME"]        = "Shrinking Man"
c["APP_SYSNAME"]     = "shrinkingman"
c["GETTEXT_PACKAGE"] = c["APP_SYSNAME"]

# File installation config - prefixes.
c["INSTALL_PREFIX"]     = "/usr/local/"
c["INSTALL_LIB_PFX"]    = join(c["INSTALL_PREFIX"], "lib")
c["INSTALL_SHARE_PFX"]  = join(c["INSTALL_PREFIX"], "share")
c["INSTALL_PIXMAP_PFX"] = join(c["INSTALL_PREFIX"], "pixmaps")
c["INSTALL_MIME_PFX"]   = "/usr/share/mime/"

# Concrete installation directories.
c["INSTALL_BIN"]        = join(c["INSTALL_PREFIX"],     "bin",            '')
c["INSTALL_LIB"]        = join(c["INSTALL_LIB_PFX"],    c["APP_SYSNAME"], '')
print c["INSTALL_BIN"]
c["INSTALL_SHARE"]      = join(c["INSTALL_SHARE_PFX"],  c["APP_SYSNAME"], '')
c["INSTALL_PIXMAP"]     = join(c["INSTALL_PIXMAP_PFX"], c["APP_SYSNAME"], '')
c["INSTALL_ICON"]       = join(c["INSTALL_SHARE_PFX"],  "icons/hicolor",  '')
c["INSTALL_LOCALE"]     = join(c["INSTALL_SHARE_PFX"],  "locale",         '')
c["INSTALL_MIME_XML"]   = join(c["INSTALL_MIME_PFX"],   "packages",       '')
c["INSTALL_MIME_KEYS"]  = "/usr/share/mime-info/"
c["INSTALL_MENU_XDG"]   = "/usr/share/applications/"

# Concrete files.
c["INSTALL_BIN_FILE"]     = join(c["INSTALL_BIN"],   c["APP_SYSNAME"])
c["INSTALL_NUTRITION_DB"] = join(c["INSTALL_SHARE"], "nutrition.db")
