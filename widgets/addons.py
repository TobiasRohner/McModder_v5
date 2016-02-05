# -*- coding: utf-8 -*-
import os
import sys
import imp
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
        self.connect(self.addonList, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.addonSelected)
        
        self.addonDescription.setReadOnly(True)
        
        
    def descriptionText(self, name, path, description):

        return "Name: "+name+"\nPath: "+path+"\n\n"+description
        
        
    def loadedAddons(self):
        
        addons = []
        for addon in self.mainWindow.addons:
            name = addon[0]
            path = addon[1]
            description = ""
            if "description" in dir(addon[2]):
                description = addon[2].description
            addons.append(_AddonListEntry(name, path, description))
        return addons
        
        
    def addAddon(self):
        
        path = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("addonSelection"),
                                                          BASEPATH,
                                                          self.mainWindow.translations.getTranslation("pyFiles")+" (*.py)"))
        if path != "":
            name = path.split("/")[-1].split(".")[0]
            module = imp.load_source(name, path)
            if len(self.addonList.findItems(name, QtCore.Qt.MatchCaseSensitive)) == 0:
                self.addonList.addItem(_AddonListEntry(name, path, module.description if "description" in dir(module) else ""))
            
            
    def removeAddon(self):
        
        idx = self.addonList.currentRow()
        self.addonList.takeItem(idx)
        
        
    def addonSelected(self, addon):
        
        self.addonDescription.setPlainText(self.descriptionText(addon.name, addon.path, addon.description))
        
        
    def accepted(self):
        
        addonPaths = [self.addonList.item(idx).path for idx in range(self.addonList.count())]
        self.mainWindow.config["addons"] = addonPaths
        self.mainWindow.config.saveData()
        
        QtGui.QMessageBox.about(self, self.mainWindow.translations.getTranslation("restartRequired"),
                                self.mainWindow.translations.getTranslation("restartToLoadAddons"))
        
        
        
        
class _AddonListEntry(QtGui.QListWidgetItem):
    
    def __init__(self, name, path, description):
        QtGui.QListWidgetItem.__init__(self, name)
        
        self.name = name
        self.path = path
        self.description = description