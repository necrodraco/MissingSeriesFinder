import xbmcaddon
import xbmcgui
#import os
import shlex, subprocess

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

xbmc.log("Program MissingSeriesFinder runs in Background");
Popen(["./MissingSeriesFinder.pl", "–path"])
xbmc.log("Program MissingSeriesFinder finished");
