# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).split("\\")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import imp
from classes import _base
from PyQt4 import QtGui, QtCore

SrcCraftingTableRecipe = imp.load_source("SrcCraftingTableRecipe", ADDONPATH+"/SrcCraftingTableRecipe.py")





class CraftingTableRecipe(_base):
    
    def __init__(self, mainWindow, name):
        _base.__init__(self, mainWindow, "CraftingTableRecipe")
        
        self.name = name
        
        
    def initUI(self):
        
        pass






def init(mainWindow):
    
    return