c = {}

# Application config.
c["APP_VERSION"]     = "0.2"
c["APP_NAME"]        = "Shrinking Man"
c["APP_SYSNAME"]     = "shrinkingman"
c["GETTEXT_PACKAGE"] = c["APP_SYSNAME"]

# File installation config - prefixes.
c["INSTALL_PREFIX"]     = "/usr/local/"
c["INSTALL_LIB_PFX"]    = c["INSTALL_PREFIX"] + "lib/"
c["INSTALL_SHARE_PFX"]  = c["INSTALL_PREFIX"] + "share/"
c["INSTALL_PIXMAP_PFX"] = c["INSTALL_PREFIX"] + "pixmaps/"
c["INSTALL_MIME_PFX"]   = "/usr/share/mime/"

# Concrete installation directories.
c["INSTALL_BIN"]        = c["INSTALL_PREFIX"]     + "bin/"
c["INSTALL_LIB"]        = c["INSTALL_LIB_PFX"]    + c["APP_SYSNAME"] + "/"
c["INSTALL_SHARE"]      = c["INSTALL_SHARE_PFX"]  + c["APP_SYSNAME"] + "/"
c["INSTALL_PIXMAP"]     = c["INSTALL_PIXMAP_PFX"] + c["APP_SYSNAME"] + "/"
c["INSTALL_ICON"]       = c["INSTALL_SHARE_PFX"]  + "icons/hicolor/"
c["INSTALL_LOCALE"]     = c["INSTALL_SHARE_PFX"]  + "locale/"
c["INSTALL_MIME_XML"]   = c["INSTALL_MIME_PFX"]   + "packages/"
c["INSTALL_MIME_KEYS"]  = "/usr/share/mime-info/"
c["INSTALL_MENU_XDG"]   = "/usr/share/applications/"

# Concrete files.
c["INSTALL_BIN_FILE"]  = c["INSTALL_BIN"] + c["APP_SYSNAME"]
