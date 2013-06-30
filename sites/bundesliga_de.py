# -*- coding: utf-8 -*-
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'bundesliga_de'
SITE_NAME = 'Bundesliga.de'
SITE_ICON = 'bl.png'

URL_MAIN = 'http://www.bundesliga.de'
URL_TV = 'http://www.bundesliga.de/de/bundesliga-tv/navigation.php?area='
URL_GET_STREAM = 'http://btd-flv-lbwww-01.odmedia.net/bundesliga/'

def load():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Aktuell', 'aktuell')    
    __createMainMenuItem(oGui, 'Spieltag', 'spieltag')
    __createMainMenuItem(oGui, 'Stars', 'stars')
    __createMainMenuItem(oGui, 'Insider', 'insider')
    __createMainMenuItem(oGui, 'Historie', 'historie')
    __createMainMenuItem(oGui, 'Vereine', 'vereine')
    oGui.setEndOfDirectory()

def __createMainMenuItem(oGui, sTitle, sPlaylistId):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('listVideos')
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('playlistId', sPlaylistId)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
def listVideos():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('playlistId')):
        sPlaylistId = oInputParameterHandler.getValue('playlistId')

        if not oInputParameterHandler.exist('sUrl'):
            sUrl = URL_TV + str(sPlaylistId)
        else:
            sUrl = oInputParameterHandler.getValue('sUrl')
        

        if sPlaylistId == 'spieltag':
            oParser = cParser()
            if sUrl.find(URL_TV) != -1:
                sUrl = 'http://www.bundesliga.de/de/bundesliga-tv/index.php'
                oRequest = cRequestHandler(sUrl)
                sHtmlContent = oRequest.request()
                sPattern = '\'(/de/bundesliga-tv/navigation.php\?area=spieltag&saison=(\d+)[^\']+)\''
                aResult = oParser.parse(sHtmlContent, sPattern)
                sUrl = URL_MAIN + aResult[1][0][0]
                sSaison = aResult[1][0][1]
            else:
                sSaison = oParser.parse(sUrl, '&saison=(\d+)')[1][0]
            
            oRequest = cRequestHandler(sUrl)
            sHtmlContent = oRequest.request()
            
            sPattern = '<div class="matchDay matchDay[^<]*onclick="retrieveURL\(\'([^\']+)\'.*?>([^<]+)</div>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            if (aResult[0] == True):                
                #ausgew�hlte Saison
                for aEntry in aResult[1]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('listVideos')
                    oGuiElement.setTitle(aEntry[1])

                    sUrl = URL_MAIN + str(aEntry[0])
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sUrl)
                    oOutputParameterHandler.addParameter('playlistId', 'spieltagEinzeln')
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
                
                #�ltere Saison
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('listVideos')
                lastSaison = str(int(sSaison) - 1)
                oGuiElement.setTitle('*' + lastSaison + '*')

                sUrl = sUrl.replace(sSaison, lastSaison)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oOutputParameterHandler.addParameter('playlistId', 'spieltag')
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

            
        elif sPlaylistId == 'vereine':
            sPattern = '<div class="teamWappen" onclick="retrieveURL\(\'([^\']+)\'.*?<img src="([^"]+)" title="Videos des ([^"]+)" /></div>'
            oRequest = cRequestHandler(sUrl)
            sHtmlContent = oRequest.request()
           
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('listVideos')
                    oGuiElement.setTitle((aEntry[2]))
                    sThumbnail = URL_MAIN + str(aEntry[1])
                    oGuiElement.setThumbnail(sThumbnail)

                    sUrl = URL_MAIN + str(aEntry[0])
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sUrl)
                    oOutputParameterHandler.addParameter('playlistId', 'verein')
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
        else:
            sPattern = '<div class="zeile">.*?<img src="([^"]+)" id="bild" class="previewImg".*?<a href="javascript:showVideoSnippet\(\'([^\']+)\'\).*?title="([^"]+)".*?<div class="describe">(.*?)</div>'    
            oRequest = cRequestHandler(sUrl)
            sHtmlContent = oRequest.request()
            
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    sThumbnail = URL_MAIN + str(aEntry[0])
                    sUrl = URL_MAIN + str(aEntry[1])
                    sTitle = cUtil().unescape(str(aEntry[2]).decode('utf-8')).encode('utf-8') 
                    sDescription = cUtil().unescape(str(aEntry[3]).decode('utf-8')).encode('utf-8')
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('play')
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.setDescription(sDescription)
                    oGuiElement.setThumbnail(sThumbnail)
                    
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sUrl)
                    oOutputParameterHandler.addParameter('sTitle', sTitle)
                    
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
            oGui.setView('movies')
    oGui.setEndOfDirectory()

def play():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('sTitle')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        sTitle = oInputParameterHandler.getValue('sTitle')
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = 'ake_playlist.php%3Fflv%3D(.*?)%26'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sUrl = URL_GET_STREAM + str(aResult[1][0])
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setMediaUrl(sUrl)
            oGuiElement.setTitle(sTitle)

            oPlayer = cPlayer()
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
    return
            #oHoster = cHosterHandler().getHoster('bundesliga')
            #oHoster.setFileName(sTitle)
            #cHosterGui().showHosterMenuDirect(oGui, oHoster, sUrl)
