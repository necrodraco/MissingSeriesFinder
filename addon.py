import xbmcaddon
import xbmcgui
#import os
import shlex, subprocess

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

Popen(["./MissingSeriesFinder.pl", "–path"])
xbmc.log("Program start in Background");
