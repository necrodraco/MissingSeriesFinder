import xbmcaddon
import xbmcgui
import os

addon       = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
addondir    = xbmc.translatePath( addon.getAddonInfo('path') )
addonsettings    = xbmc.translatePath( addon.getAddonInfo('profile') )

line1 = "Program MissingSeriesFinder addondir: " + addondir
line2 = "Program MissingSeriesFinder addonsettings: " + addonsettings

xbmc.log(line1)
xbmc.log(line2)

command = "perl " + addondir + "/MissingSeriesFinder.pl -home=" + addondir + " -path=" + addonsettings
xbmc.log("command: " + command)
os.system(command)

xbmcgui.Dialog().ok(addonname, command);