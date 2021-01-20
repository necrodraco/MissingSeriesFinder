import xbmcaddon
import xbmcgui

import tvdb_api

import json
import time
import os
import datetime
import re

addon               = xbmcaddon.Addon()
addonname           = addon.getAddonInfo('name')
icon                = addon.getAddonInfo('icon')
messagetime         = 1000 #in miliseconds

waitTime            = addon.getSettingNumber('waitTime')
if waitTime < 2.0: 
    waitTime = 2.0
logPath             = addon.getSetting('Path_to_Log')
logOption           = addon.getSettingBool('LogOption')
onlyReleased        = addon.getSettingBool('onlyReleased')
tvdbapikey          = addon.getSetting('tvdbapikey')

messageIdZero       = addon.getLocalizedString(32101)
messageErrorUnknown = addon.getLocalizedString(32102)
messageFoundShow    = addon.getLocalizedString(32103)
messageIdNotSet     = addon.getLocalizedString(32104)
messageDiscTitle    = addon.getLocalizedString(32105)
messageDiscMessage  = addon.getLocalizedString(32106)
messageWriteIntoLog = addon.getLocalizedString(32107)
messageInFolder     = addon.getLocalizedString(32108)
messageFinished     = addon.getLocalizedString(32109)
messageStartSearch  = addon.getLocalizedString(32110)
messageMissingShows = addon.getLocalizedString(32111)
messageNotFoundShows= addon.getLocalizedString(32112)
messageErrorJson    = addon.getLocalizedString(32113)
messageFinished     = addon.getLocalizedString(32114)

t                  = tvdb_api.Tvdb(apikey=tvdbapikey)
today              = datetime.datetime.now()

notfoundshows={}
othererror={}

def logging(mtype, message): 
    #xbmcgui.Dialog().ok(addonname, message)
    xbmc.log('%s=%s' % (mtype, message),level=xbmc.LOGNOTICE)

def loggingJson(mtype, messageJson):
    xbmc.log('%s=' % mtype,level=xbmc.LOGNOTICE)
    xbmc.log(json.dumps(messageJson, indent=4, sort_keys=True),level=xbmc.LOGNOTICE)

def message(message):
    message=message.replace(",","")
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,message, messagetime, icon))

def jsoncall(rpccmd):
    rpccmd = json.dumps(rpccmd)
    result = xbmc.executeJSONRPC(rpccmd)
    return json.loads(result)

def getShowsKodi(start, end):
    cmd={
        'jsonrpc': '2.0', 
        'method': 'VideoLibrary.GetTVShows', 
        'params': { 
            'properties': [
              "season", 
              "uniqueid", 
              "file"
            ], 
            'limits': {
                'start': start, 
                'end': end
            }
        }, 
        'id': 'libTvShows'
    }
    result=jsoncall(cmd)
    return result['result']

def getEpisodesKodi(tvshowid, season):
    cmd={
        'jsonrpc': '2.0', 
        'method': 'VideoLibrary.GetEpisodes', 
        'params': { 
            'tvshowid': tvshowid, 
            'season': season, 
            'properties': ["episode"],
        }, 
        'id': 'libTvShows'
    }
    result=jsoncall(cmd)
    return result['result']

def getShowTvdb(tvShow, showname, showfolder):
    s={}
    try:
        s=t[tvShow]
    except tvdb_api.tvdb_error:
        if tvShow not in othererror: 
            othererror[tvShow]={}
        if tvShow == 0:
            othererror[showname]['reason']=messageIdZero
            othererror[showname]['name']=showname
            othererror[showname]['folder']=showfolder
        else: 
            othererror[showname]['reason']=messageErrorUnknowns
            othererror[tvShow]['name']=showname
            othererror[tvShow]['folder']=showfolder
    #after a call, wait 2+ sec to ensure tvdb never blocks the apikey
    time.sleep(waitTime)
    return s

def prepareDict(tlist, tvdbid, show):
    if tvdbid not in tlist:
        tlist[tvdbid]={}
        tlist[tvdbid]['name']=show['label']
        tlist[tvdbid]['folder']=show['file']
        tlist[tvdbid]['episodes']={}

def getCleanShows(): 
    shows={}
    showsRaw=getShowsKodi(0,0)
    end=showsRaw['limits']['total']
    start=0
    while end > start:
        tend=start+10
        if tend > end: 
            tend=end
        showsRaw=getShowsKodi(start,tend)
        start=tend
        for show in showsRaw['tvshows']: 
            message(messageFoundShow % show['label'].replace(',',''))
            tvshowid=int(show['tvshowid'])
            tvdbid=0
            if 'tvdb' in show['uniqueid'] : 
                tvdbid=int(show['uniqueid']['tvdb'])
            else: 
                if 'uniqueid' in show:
                    if not show['uniqueid']['unknown']:
                        othererror[show['label']]={}
                        othererror[show['label']]['reason']=messageIdNotSet
                        othererror[show['label']]['name']=show['label']
                        othererror[show['label']]['folder']=show['file']
                        continue;
                    tvdbid=int(show['uniqueid']['unknown'])
            seasons=int(show['season'])
            if seasons > 0 :
                for season in range(seasons+1): 
                    tvshowsRaw=getEpisodesKodi(tvshowid, season)
                    if 'episodes' in tvshowsRaw: 
                        tvshowsRaw=tvshowsRaw['episodes']
                        #loggingJson("quickraw", tshowsRaw)
                        for episodeRaw in tvshowsRaw: 
                            episode=episodeRaw['episode']
                            prepareDict(shows, tvdbid, show)
                            if season not in shows[tvdbid]['episodes']: 
                                shows[tvdbid]['episodes'][season]={}
                            shows[tvdbid]['episodes'][season][episode]=1;
            else: #Seasons == 0
                prepareDict(notfoundshows, tvdbid, show)
                notfoundshows[tvdbid]['episodes'][0]={}
                notfoundshows[tvdbid]['episodes'][0][0]=1
    return shows

def writefile(path, subpath, folder, filename):
    destination= "%s%s/%s/%s.disc" % (path, subpath,folder,filename)
    diskfile = open(destination, 'w')
    diskfile.write("<discstub>\n")
    diskfile.write("    <title>%s</title>\n" % messageDiscTitle)
    diskfile.write("    <message>%s</message>\n" % messageDiscMessage)
    diskfile.write("</discstub>")
    diskfile.close()  

def writeEpisodeToList(slist, stype, showfolder, show, season, episode, writeTitle): 
    if writeTitle == 1: 
        slist.write(show + "\n")
        slist.write(messageInFolder % showfolder)
        message(messageWriteIntoLog % show)
        if bool(logOption): 
            folder="%s%s/%s" % (logPath, stype, show)
            if not(os.path.exists(folder)):
                os.makedirs(folder)
    
    missingEpisode = "S%02dE%02d" % (season, episode)
    slist.write(missingEpisode + "\n")
    if bool(logOption): 
        writefile(logPath, stype, show, missingEpisode) 
    return 0

def searchAndWriteMissingShows(shows, stype, stext):
    if not bool(shows): #No Shows found
        return 
    if not(os.path.exists(logPath)) : 
        os.makedirs(logPath)
    logfile = open(logPath + stype + '.log', 'w')
    logfile.write(stext)
    
    for tvdbid in shows.keys():
        showname=shows[tvdbid]['name']
        showfolder=shows[tvdbid]['folder']
        showTvDb=getShowTvdb(tvdbid, showname, showfolder)
        x=1
        for seasonTvDb in showTvDb: 
            for episodeTvDb in showTvDb[seasonTvDb]: 
                if episodeTvDb == 0 and seasonTvDb == 0: 
                    continue #Some Series have S00E00 Files, which would not scrobbable
                
                if bool(onlyReleased): #Skip episodes not released yet
                    firstAired=showTvDb[seasonTvDb][episodeTvDb]['firstAired']
                    if firstAired and re.match(r'^\d{4}-\d{2}-\d{2}$', firstAired): #If firstaired is not set, ignore
                        datesplit=firstAired.split("-")
                        firstAired=datetime.datetime(int(datesplit[0]), int(datesplit[1]), int(datesplit[2]))
                        if today < firstAired: 
                            continue
                
                #Skip all Episodes that are in the Library
                if seasonTvDb in shows[tvdbid]['episodes'] and episodeTvDb in shows[tvdbid]['episodes'][seasonTvDb]:
                    continue

                #Write Episode in the List
                x=writeEpisodeToList(logfile, stype, showfolder, showname, seasonTvDb, episodeTvDb, x)
    logfile.write(messageFinished)
    logfile.close()

def main():
    message(messageStartSearch)
    shows=getCleanShows()
    searchAndWriteMissingShows(shows, "MissingShows", messageMissingShows);
    searchAndWriteMissingShows(notfoundshows, "NotFoundShows", messageNotFoundShows);
    if bool(othererror):
        logfile=open(logPath + 'other.log', 'w')
        logfile.write(messageErrorJson)
        logfile.write(json.dumps(othererror, indent=4, sort_keys=True));
        logfile.close()
    xbmcgui.Dialog().ok(addonname, messageFinished)

main()