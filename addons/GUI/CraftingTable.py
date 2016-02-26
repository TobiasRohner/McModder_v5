# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).replace("\\", "/").split("/")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import imp
from classes import _base
from widgets import menus
from PyQt4 import QtGui, QtCore, uic

guiDef = imp.load_source("guiDef", ADDONPATH+"/guiDef.py")
SrcCraftingTable = imp.load_source("SrcCraftingTable", ADDONPATH+"/SrcCraftingTable.py")





class CraftingTable(_base):
    
    def __init__(self, mainWindow, name):
        _base.__init__(self, mainWindow, "GUI", "CraftingTable")
        
        self.guiType = "CraftingTable"
        self.name = "CraftingTable"
        self.deleteable = False
        
        self.gui = guiDef.GUIWidget(self, BASEPATH+"/assets/textures/gui/container/crafting_table.png")
        self.gui.slots = [guiDef.Slot(self.gui, 30,17), guiDef.Slot(self.gui, 48,17), guiDef.Slot(self.gui, 66,17),
                          guiDef.Slot(self.gui, 30,35), guiDef.Slot(self.gui, 48,35), guiDef.Slot(self.gui, 66,35),
                          guiDef.Slot(self.gui, 30,53), guiDef.Slot(self.gui, 48,53), guiDef.Slot(self.gui, 66,53),
                          guiDef.Slot(self.gui, 125,35)]
                          
        self.dragItem = None
        
        self.initUI()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(ADDONPATH+"/CraftingTable.ui", self)
        
        self.setAcceptDrops(True)
        
        self.itemList = menus.ItemList(self.mainWindow)
        self.tableLayout.addWidget(self.itemList)
        
        self.gui.setMinimumSize(176, 166)
        self.gui.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.tableLayout.addWidget(self.gui)
        
        
    def save(self):
        
        data = {"identifier":self.identifier,
                "classtype":self.classtype,
                "name":self.name}
        return data
        
        
        
        
class Recipe(QtGui.QListWidgetItem):
    
    
    def __init__(self, mainWindow, master):
        QtGui.QListWidgetItem.__init__(self)
        
        self.mainWindow = mainWindow
        self.master = master






def init(mainWindow):
    
    return
    
    
    
def onProjectCreated(mainWindow):
    
    mainWindow.project.addObject(CraftingTable(mainWindow, "CraftingTable"))