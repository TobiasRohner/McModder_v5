# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui




BASEPATH = os.path.dirname(sys.argv[0])

VANILLA_TABS = {"Building Blocks":"CreativeTabs.tabBlock",
                "Brewing":"CreativeTabs.tabBrewing",
                "Combat":"CreativeTabs.tabCombat",
                "Decorations":"CreativeTabs.tabDecorations",
                "Food":"CreativeTabs.tabFood",
                "Materials":"CreativeTabs.tabMaterials",
                "Misc":"CreativeTabs.tabMisc",
                "Redstone":"CreativeTabs.tabRedstone",
                "Tools":"CreativeTabs.tabTools",
                "Transport":"CreativeTabs.tabTransport"}
                
                
def mergeDicts(x, y):
    
    z = x.copy()
    z.update(y)
    
    return z





class CreativeDropdown(QtGui.QComboBox):
    
    def __init__(self, mainWindow):
        QtGui.QComboBox.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.tabs = {}
        
        self.updateTabs()
        
        
    def getCustomTabs(self):
        
        return {}
        
        
    def updateTabs(self):
        
        self.tabs = mergeDicts(VANILLA_TABS, self.getCustomTabs())
        for name in self.tabs.keys():
            if self.findText(name) == -1:
                self.addItem(name)
                
                
    def getTabClass(self, tabName):
        
        return self.tabs[tabName]