# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui

BASEPATH = os.path.dirname(sys.argv[0])

ITEMS = []




class ItemList(QtGui.QListWidget):
    
    def __init__(self, mainWindow, project):
        QtGui.QListWidget.__init__(self)
        
        self.mainWindow = mainWindow
        self.project = project
        
        
    def initMCItems(self):
        
        pass
    
    
    def loadCustomItems(self):
        
        pass
        
        
        
        
class Item(QtGui.QListWidgetItem):
    
    def __init__(self, name, package, texture):
        QtGui.QListWidgetItem.__init__(self)
        
        self.package = package
        self.texture = QtGui.QPixmap(texture)
        
        self.setText(name)
        self.setIcon(QtGui.QIcon(self.texture))
        
        
    def name(self):
        
        return self.text()
        
        
    def setName(self, name):
        
        self.setText(name)