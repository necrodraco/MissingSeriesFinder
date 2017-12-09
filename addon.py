import xbmcaddon
import xbmcgui
import os

addon       = xbmcaddon.Addon('script.missing.seriesfinder')
addondir    = xbmc.translatePath( addon.getAddonInfo('path') )
addonsettings    = xbmc.translatePath( addon.getAddonInfo('profile') )

xbmc.log("Program MissingSeriesFinder addondir: " + addondir)
xbmc.log("Program MissingSeriesFinder addonsettings: " + addonsettings)

command = "perl " + addondir + "/MissingSeriesFinder.pl -home=" + addondir + " -path=" + addonsettings
xbmc.log("command: " + command)
os.system(command)
