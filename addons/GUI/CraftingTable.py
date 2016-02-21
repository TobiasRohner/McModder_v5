# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).split("\\")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import imp
import pickle
from classes import _base
from PyQt4 import QtGui, QtCore, uic

SrcCraftingTable = imp.load_source("SrcCraftingTable", ADDONPATH+"/SrcCraftingTable.py")





class CraftingTable(_base):
    
    def __init__(self, mainWindow):
        _base.__init__(self, mainWindow, "GUI")
        
        self.guiType = "CraftingTable"
        self.name = "Crafting Table"
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(ADDONPATH+"/CraftingTable.ui", self)
        
        self.guiWidget = GUIGraphic(self)
        self.mainLayout.insertWidget(0, self.guiWidget)
        
        
    def save(self):
        
        if not os.path.exists(self.mainWindow.config["workspace"]+"/"+self.project.name+"/mod/"+self.identifier):
            os.makedirs(self.mainWindow.config["workspace"]+"/"+self.project.name+"/mod/"+self.identifier)
        
        f = open(self.mainWindow.config["workspace"]+"/"+self.project.name+"/mod/"+self.identifier+"/"+self.name+".mod", "w")
        
        data = {"name":self.name,
                "guiType":self.guiType}
        pickle.dump(data, f)
        
        f.close()
    
    
    
    
class GUIGraphic(QtGui.QWidget):
    
    def __init__(self, master):
        QtGui.QWidget.__init__(self)
        
        self.master = master






def init(mainWindow):
    
    return