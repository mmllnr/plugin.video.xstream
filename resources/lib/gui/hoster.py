# -*- coding: utf-8 -*-
from resources.lib.handler.jdownloaderHandler import cJDownloaderHandler
from resources.lib.download import cDownload
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer
from resources.lib.handler.requestHandler import cRequestHandler
import urlresolver
import logger

class cHosterGui:

    SITE_NAME = 'cHosterGui'

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, bGetRedirectUrl = False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('showHosterMenu')
        oGuiElement.setTitle(oHoster.getDisplayName())

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    # step 2
    def showHosterMenu(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        #sFileName = oInputParameterHandler.getValue('sFileName')

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)
        
        self.showHosterMenuDirect(oGui, oHoster, sMediaUrl, bGetRedirectUrl)
        
        oGui.setEndOfDirectory()

    def showHosterMenuDirect(self, oGui, oHoster, sMediaUrl, bGetRedirectUrl=False, sFileName=''):
        # play
        self.__showPlayMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName)

        # playlist
        self.__showPlaylistMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName)

        # download
        self.__showDownloadMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName)        

        # JD
        self.__showJDMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName)	

        
    def __showPlayMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName=''):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')
        oGuiElement.setTitle('play')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', sFileName)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showDownloadMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName=''):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('download')
        oGuiElement.setTitle('download �ber XBMC')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', sFileName)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showJDMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName=''):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)        
        oGuiElement.setTitle('an JDownloader senden')
        oGuiElement.setFunction('sendToJDownloader')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showPlaylistMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName=''):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('addToPlaylist')
        oGuiElement.setTitle('add to playlist')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', sFileName)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def play(self):
        #oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):            
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call play: ' + sMediaUrl)

        sLink = urlresolver.resolve(sMediaUrl)
        
        if (sLink != False):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(sLink)
            oGuiElement.setTitle(sFileName)

            oPlayer = cPlayer()
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
        return

        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

        #oGui.setEndOfDirectory()

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call play: ' + sMediaUrl)

        sLink = urlresolver.resolve(sMediaUrl)

        if (sLink != False):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(sLink)
            oGuiElement.setTitle(sFileName)

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oGui.showInfo('Playlist', 'Stream wurde hinzugef�gt', 5);
            return
        oGui.showError('Playlist', 'Stream wurde nicht hinzugef�gt', 5);
        return False
        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

        #oGui.setEndOfDirectory()

    def download(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call download: ' + sMediaUrl)

        sLink = urlresolver.resolve(sMediaUrl)
        
        if (sLink != False):
            oDownload = cDownload()
            oDownload.download(sLink, 'Stream')
            return

        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

        oGui.setEndOfDirectory()

    def sendToJDownloader(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call send to JDownloader: ' + sMediaUrl)

        cJDownloaderHandler().sendToJDownloader(sMediaUrl)

        

    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
