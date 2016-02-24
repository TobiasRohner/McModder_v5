# -*- coding: utf-8 -*-
import os
import sys
import json
from PyQt4 import QtGui

BASEPATH = os.path.dirname(sys.argv[0])

ITEMS = []




class ItemList(QtGui.QListWidget):
    
    def __init__(self, mainWindow, project=None):
        QtGui.QListWidget.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.standardItems = []
        self.project = project
        
        self.initMCItems()
        
        
    def initMCItems(self):
        
        f = open(BASEPATH+"/assets/icons.json")
        data = json.load(f)
        f.close()
        for name in data.keys():
            texPath = BASEPATH+"/assets/textures/icons/"+data[name]["texture"]
            if data[name]["type"] == "Item":
                self.standardItems.append(Item(None, name, "Items."+data[name]["name"], texPath))
            elif data[name]["type"] == "Block":
                self.standardItems.append(Item(None, name, "Blocks."+data[name]["name"], texPath))
    
    
    def customItems(self):
        
        items = []
        for item in self.project.objects["Item"]:
            items.append(Item(item))
        return items
    
    
    def reloadItems(self):
        
        self.clear()
        for item in self.standardItems:
            self.addItem(item)
        for item in self.customItems(self.project):
            self.addItem(item)
        self.sortItems()
        
        
    def showEvent(self, event):
        
        self.reloadItems()
        
        
        
        
class Item(QtGui.QListWidgetItem):
    
    def __init__(self, item):
        QtGui.QListWidgetItem.__init__(self)
        
        self.item = item
        self.package = item.package()
        self.texture = QtGui.QPixmap(item.texture)
        
        self.setText(item.name)
        self.setIcon(QtGui.QIcon(self.texture))
        
        
    def getName(self):
        
        return self.item.name
            
            
    def getPackage(self):
        
        return self.item.package()