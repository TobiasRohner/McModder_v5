# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).split("\\")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import imp
import pickle
from classes import _base

CraftingTable = imp.load_source("CraftingTable", ADDONPATH+"/CraftingTable.py")
        
        
        
        
class GUI():
    
    def __init__(mainWindow, name="", guiType="Custom"):
    
        if guiType == "CraftingTable":
            return CraftingTable.CraftingTable(mainWindow)
            
            
    def load(self, path):
        
        f = open(path, "r")
        
        data = pickle.load(f)
        if data["guiType"] == "CraftingTable":
            return CraftingTable.CraftingTable(mainWindow)
        
        f.close()

        
        
        
        
def init(mainWindow):
    
    return