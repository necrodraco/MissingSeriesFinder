import xbmcaddon
import xbmcgui
#import os
import shlex, subprocess

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addondir    = xbmc.translatePath( addon.getAddonInfo('profile') )

xbmc.log("Program MissingSeriesFinder runs in Background");
#xbmc.log("dir is: " + addondir);
subprocess.call(["perl", "./MissingSeriesFinder.pl", "-path=" + addondir])
xbmc.log("Program MissingSeriesFinder finished");
