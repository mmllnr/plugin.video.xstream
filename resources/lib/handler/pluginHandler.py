from resources.lib.config import cConfig
import sys
import os
import xbmcaddon
import logger

class cPluginHandler:

    def getPluginHandle(self):
        try:
            return int( sys.argv[ 1 ] )
        except:
            return 0

    def getPluginPath(self):
        try:
            return sys.argv[0]
        except:
            return ''

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        items = os.listdir(sFolder)
        for sItemName in items:
            sFilePath = os.path.join(sFolder, sItemName)
            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')

            if (os.path.isdir(sFilePath) == False):
                if (str(sFilePath.lower()).endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def __importPlugin(self, sName):
        try:
            plugin = __import__(sName, globals(), locals())
            sSiteName = plugin.SITE_NAME
            sPluginSettingsName = 'plugin_' + sName                        
        except Exception, e:
            logger.error("Can't import plugin: %s :%s" % (sName, e))
            return False, None, None, None
        try:
            sSiteIcon = plugin.SITE_ICON
            return True, sSiteName, sPluginSettingsName, sSiteIcon
        except:
            return True, sSiteName, sPluginSettingsName, ''

    def getRootFolder(self):
        sRootFolder = xbmcaddon.Addon(id='plugin.video.xstream').getAddonInfo('path')
        logger.info('root folder: ' + sRootFolder)
        return sRootFolder

    def getAvailablePlugins(self):
        oConfig = cConfig()

        sFolder =  self.getRootFolder()
        sIconFolder = os.path.join(sFolder, 'resources','art','sites')
        sFolder = os.path.join(sFolder, 'sites')

        # xbox hack
        sFolder = sFolder.replace('\\', '/')
        logger.info('sites folder: ' + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            logger.info('load plugin: '+ str(sFileName))

            # wir versuchen das plugin zu importieren
            aPlugin = self.__importPlugin(sFileName)
            if aPlugin[0]:
                sSiteName = aPlugin[1]
                sPluginSettingsName = aPlugin[2]
                if aPlugin[3] != '':
                    sSiteIcon = os.path.join(sIconFolder, aPlugin[3])
                else:
                    sSiteIcon = ''

                # existieren zu diesem plugin die an/aus settings
                bPlugin = oConfig.getSetting(sPluginSettingsName)
                if (bPlugin != ''):
                    # settings gefunden
                    if (bPlugin == 'true'):
                        aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteIcon))
                else:
                   # settings nicht gefunden, also schalten wir es trotzdem sichtbar
                   aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteIcon))

        return aPlugins

    def __createAvailablePluginsItem(self, sPluginName, sPluginIdentifier, sPluginIcon):
        aPluginEntry = []
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginIcon)
        return aPluginEntry