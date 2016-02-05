# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui, QtCore, uic




BASEPATH = os.path.dirname(sys.argv[0])




class Addons(QtGui.QDialog):
    
    def __init__(self, mainWindow):
        QtGui.QDialog.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.initUI()
        
        self.show()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(BASEPATH+"/ui/Addons.ui", self)
        
        for addon in self.loadedAddons():
            self.addonList.addItem(addon)
            
        self.connect(self.addAddonButton, QtCore.SIGNAL("clicked()"), self.addAddon)
        self.connect(self.removeAddonButton, QtCore.SIGNAL("clicked()"), self.removeAddon)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accepted)
        
        self.addonDescription.setReadOnly(True)
        
        
    def loadedAddons(self):
        
        return [_AddonListEntry(addon[0], addon[1]) for addon in self.mainWindow.addons]
        
        
    def addAddon(self):
        
        path = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("addonSelection"),
                                                          BASEPATH,
                                                          self.mainWindow.translations.getTranslation("pyFiles")+" (*.py)"))
        if path != "":
            name = path.split("/")[-1].split(".")[0]
            if len(self.addonList.findItems(name, QtCore.Qt.MatchCaseSensitive)) == 0:
                self.addonList.addItem(_AddonListEntry(name, path))
            
            
    def removeAddon(self):
        
        idx = self.addonList.currentRow()
        self.addonList.takeItem(idx)
        
        
    def accepted(self):
        
        addonPaths = [self.addonList.item(idx).path for idx in range(self.addonList.count())]
        self.mainWindow.config["addons"] = addonPaths
        self.mainWindow.config.saveData()
        
        QtGui.QMessageBox.about(self, self.mainWindow.translations.getTranslation("restartRequired"),
                                self.mainWindow.translations.getTranslation("restartToLoadAddons"))
        
        
        
        
class _AddonListEntry(QtGui.QListWidgetItem):
    
    def __init__(self, name, path):
        QtGui.QListWidgetItem.__init__(self, name)
        
        self.path = path