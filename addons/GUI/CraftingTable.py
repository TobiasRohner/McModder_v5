# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).replace("\\", "/").split("/")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import imp
from classes import _base
from widgets import menus
from PyQt4 import QtGui, QtCore, uic

SrcCraftingTable = imp.load_source("SrcCraftingTable", ADDONPATH+"/SrcCraftingTable.py")





class CraftingTable(_base):
    
    def __init__(self, mainWindow, name):
        _base.__init__(self, mainWindow, "GUI", "CraftingTable")
        
        self.guiType = "CraftingTable"
        self.name = "CraftingTable"
        self.isdeleteable = False
        
        self.initUI()
        
        
#    def postInit(self, project):
#        
#        self.itemList.project = project
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(ADDONPATH+"/CraftingTable.ui", self)
        
#        self.itemList = menus.ItemList(self.mainWindow)
#        self.tableLayout.addWidget(self.itemList)
        
        self.guiWidget = GUIGraphic(self)
        self.guiWidget.setMinimumSize(176, 166)
        self.guiWidget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.tableLayout.addWidget(self.guiWidget)
        
        
    def save(self):
        
        data = {"identifier":self.identifier,
                "classtype":self.classtype,
                "name":self.name}
        return data
    
    
    
    
class GUIGraphic(QtGui.QWidget):
    
    def __init__(self, master):
        QtGui.QWidget.__init__(self)
        
        self.master = master
        
        self.texture = QtGui.QPixmap(BASEPATH+"/assets/textures/gui/container/crafting_table.png")
        
        
    def paintEvent(self, event):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawTexture(qp)
        qp.end()
        
        
    def drawTexture(self, painter):
        
        width = self.texture.width()
        height = self.texture.height()
        aspect = float(width)/height
        
        if float(self.width())/self.height() > aspect:
            h = self.height()
            w = int(aspect*h)
            xc = int(float(self.width()-w)/2)
            yc = 0
        else:
            w = self.width()
            h = int(float(w)/aspect)
            xc = 0
            yc = int(float(self.height()-h)/2)
        painter.drawPixmap(xc, yc, w, h, self.texture)
        
        
        
        
class Recipe(QtGui.QListWidgetItem):
    
    
    def __init__(self, mainWindow, master):
        QtGui.QListWidgetItem.__init__(self)
        
        self.mainWindow = mainWindow
        self.master = master






def init(mainWindow):
    
    return
    
    
    
def onProjectCreated(mainWindow):
    
    mainWindow.project.addObject(CraftingTable(mainWindow, "CraftingTable"))