# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).replace("\\", "/").split("/")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import imp
from classes import _base
from widgets import menus
from utils import Decorators as dec
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
                          guiDef.Slot(self.gui, 125,35, True)]
                          
        self.dragItem = None
        
        self.tempRecipe = Recipe(self.mainWindow, self, "unknown")
        
        self.initUI()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(ADDONPATH+"/CraftingTable.ui", self)
        
        self.setAcceptDrops(True)
        
        self.itemList = menus.ItemList(self.mainWindow)
        self.tableLayout.insertWidget(0, self.itemList)
        
        self.gui.setMinimumSize(176, 166)
        self.gui.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.guiLayout.insertWidget(0, self.gui)
        
        self.connect(self.newRecipeButton, QtCore.SIGNAL("clicked()"), self.addRecipe)
        self.connect(self.removeRecipeButton, QtCore.SIGNAL("clicked()"), self.removeRecipe)
        self.connect(self.recipeList, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.selectRecipe)
        self.connect(self.recipeList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.renameRecipe)
        self.connect(self.shapedCheckbox, QtCore.SIGNAL("stateChanged(int)"), self.setShaped)
        
        
    def addRecipe(self):
        
        self.gui.slots[0].item = None
        self.gui.slots[1].item = None
        self.gui.slots[2].item = None
        self.gui.slots[3].item = None
        self.gui.slots[4].item = None
        self.gui.slots[5].item = None
        self.gui.slots[6].item = None
        self.gui.slots[7].item = None
        self.gui.slots[8].item = None
        self.gui.slots[9].item = None
        self.gui.slots[0].count = 0
        self.gui.slots[1].count = 0
        self.gui.slots[2].count = 0
        self.gui.slots[3].count = 0
        self.gui.slots[4].count = 0
        self.gui.slots[5].count = 0
        self.gui.slots[6].count = 0
        self.gui.slots[7].count = 0
        self.gui.slots[8].count = 0
        self.gui.slots[9].count = 0
        
        recipe = Recipe(self.mainWindow, self, "unknown")
        self.recipeList.addItem(recipe)
        self.recipeList.setCurrentItem(recipe)
        self.selectRecipe(recipe)
        
        self.gui.repaint()
        
        
    def removeRecipe(self):
        
        recipe = self.recipeList.currentItem()
        self.recipeList.takeItem(self.recipeList.row(recipe))
        
        self.gui.resetSlots()
        
        
    def selectRecipe(self, recipe):
        
        self.gui.slots[0].item = recipe.items[0].item
        self.gui.slots[1].item = recipe.items[1].item
        self.gui.slots[2].item = recipe.items[2].item
        self.gui.slots[3].item = recipe.items[3].item
        self.gui.slots[4].item = recipe.items[4].item
        self.gui.slots[5].item = recipe.items[5].item
        self.gui.slots[6].item = recipe.items[6].item
        self.gui.slots[7].item = recipe.items[7].item
        self.gui.slots[8].item = recipe.items[8].item
        self.gui.slots[9].item = recipe.items[9].item
        
        self.gui.slots[0].count = recipe.items[0].count
        self.gui.slots[1].count = recipe.items[1].count
        self.gui.slots[2].count = recipe.items[2].count
        self.gui.slots[3].count = recipe.items[3].count
        self.gui.slots[4].count = recipe.items[4].count
        self.gui.slots[5].count = recipe.items[5].count
        self.gui.slots[6].count = recipe.items[6].count
        self.gui.slots[7].count = recipe.items[7].count
        self.gui.slots[8].count = recipe.items[8].count
        self.gui.slots[9].count = recipe.items[9].count
        
        self.shapedCheckbox.setCheckState(QtCore.Qt.Checked if recipe.shaped else QtCore.Qt.Unchecked)
        
        self.gui.repaint()
        
        
    def updateRecipe(self, slots):
        
        recipe = self.recipeList.currentItem()
        if recipe == None:
            recipe = self.tempRecipe
        
        recipe.items[0].item = slots[0].item
        recipe.items[1].item = slots[1].item
        recipe.items[2].item = slots[2].item
        recipe.items[3].item = slots[3].item
        recipe.items[4].item = slots[4].item
        recipe.items[5].item = slots[5].item
        recipe.items[6].item = slots[6].item
        recipe.items[7].item = slots[7].item
        recipe.items[8].item = slots[8].item
        recipe.items[9].item = slots[9].item
        
        recipe.items[0].count = slots[0].count
        recipe.items[1].count = slots[1].count
        recipe.items[2].count = slots[2].count
        recipe.items[3].count = slots[3].count
        recipe.items[4].count = slots[4].count
        recipe.items[5].count = slots[5].count
        recipe.items[6].count = slots[6].count
        recipe.items[7].count = slots[7].count
        recipe.items[8].count = slots[8].count
        recipe.items[9].count = slots[9].count
        
        
    def renameRecipe(self, recipe):
        
        dialog = QtGui.QInputDialog()
        dialog.setTextValue(recipe.text())
        txt, ok = dialog.getText(self, "Change Name", "Name:")
        
        if ok:
            recipe.setText(str(txt))
            
            
    def setShaped(self, shaped):
        
        recipe = self.recipeList.currentItem()
        
        recipe.shaped = shaped == QtCore.Qt.Checked
        
        
    def save(self):
        
        data = {}
        
        data["identifier"] = self.identifier
        data["classtype"] = self.classtype
        data["name"] = str(self.name)
        data["recipes"] = []
        for r in range(self.recipeList.count()):
            recipe = self.recipeList.item(r)
            data["recipes"].append(recipe.save())
            
        return data
        
        
    def load(self, data):
        
        self.identifier = data["identifier"]
        self.classtype = data["classtype"]
        self.name = data["name"]
        for r in data["recipes"]:
            recipe = Recipe(self.mainWindow, self, r["name"])
            recipe.load(r)
            self.recipeList.addItem(recipe)
            
        
        
    def pull(self, cls):
        
        data = {}
        
        if cls.identifier == "BaseMod":
            
            recSrc = []
            for r in range(self.recipeList.count()):
                recipe = self.recipeList.item(r)
                recSrc.append(recipe.getSrc())
            data["commonInit"] = ["\n\n".join(recSrc)]
            data["imports"] = SrcCraftingTable.imports
            
        return data
            
            
    def generateSrc(self, src):
        
        for d in self.data.keys():
            src = src.replace("<"+d+">", "\n".join(self.data[d]))
            
        return src
        
        
    def completeModData(self):
        
        for k in self.data.keys():
            self.data[k] = []
        
        success = True
        
        for r in range(self.recipeList.count()):
            recipe = self.recipeList.item(r)
            success = success and recipe.completeModData()
        
        if success:
            self.mainWindow.console.write(self.name+": Successfully completed Mod Data")
        
        
        
        
class Recipe(QtGui.QListWidgetItem):
    
    
    def __init__(self, mainWindow, master, name):
        QtGui.QListWidgetItem.__init__(self)
        
        self.mainWindow = mainWindow
        self.master = master
        
        self.setText(name)
        
        self.items = [guiDef.ItemStack(self, None), guiDef.ItemStack(self, None), guiDef.ItemStack(self, None),
                      guiDef.ItemStack(self, None), guiDef.ItemStack(self, None), guiDef.ItemStack(self, None),
                      guiDef.ItemStack(self, None), guiDef.ItemStack(self, None), guiDef.ItemStack(self, None),
                      guiDef.ItemStack(self, None)]
                      
        self.shaped = True
        
        self.data = {"output":[],
                     "grid":[],
                     "items":[],
                     "inputs":[]}
                     
        self.ACRO = ["A", "B", "C", "D", "E", "F", "G", "H", "I", " "]
        
        
    def is1x1(self):
        
        count = 0
        for item in self.items:
            if item.item != None:
                count += 1
        return count == 1
                     
                     
    def is2x2(self):
        
        s1 = self.master.gui.slots[0].item == None
        s2 = self.master.gui.slots[1].item == None
        s3 = self.master.gui.slots[2].item == None
        s4 = self.master.gui.slots[3].item == None
        s5 = self.master.gui.slots[4].item == None
        s6 = self.master.gui.slots[5].item == None
        s7 = self.master.gui.slots[6].item == None
        s8 = self.master.gui.slots[7].item == None
        s9 = self.master.gui.slots[8].item == None
        
        return ((s3 and s6 and s7 and s8 and s9) or 
                (s1 and s4 and s7 and s8 and s9) or
                (s1 and s2 and s3 and s6 and s9) or
                (s1 and s2 and s3 and s4 and s7),
                ((s3 and s6 and s7 and s8 and s9),
                 (s1 and s4 and s7 and s8 and s9),
                 (s1 and s2 and s3 and s6 and s9),
                 (s1 and s2 and s3 and s4 and s7)))
                
                
    def is3x3(self):
        
        s1 = self.master.gui.slots[0].item != None
        s2 = self.master.gui.slots[1].item != None
        s3 = self.master.gui.slots[2].item != None
        s4 = self.master.gui.slots[3].item != None
        s5 = self.master.gui.slots[4].item != None
        s6 = self.master.gui.slots[5].item != None
        s7 = self.master.gui.slots[6].item != None
        s8 = self.master.gui.slots[7].item != None
        s9 = self.master.gui.slots[8].item != None
        
        return (((s1 or s2 or s3) and (s7 or s8 or s9)) or
                ((s1 or s4 or s7) and (s3 or s6 or s9)))
                
                
    def crop(self, acro):
        
        while  acro.count([]) == 0 and (acro[0][0]==" " and acro[1][0]==" " and acro[2][0]==" "):
            acro[0] = acro[0][1:]
            acro[1] = acro[1][1:]
            acro[2] = acro[2][1:]
        while acro.count([]) == 0 and (acro[0][-1]==" " and acro[1][-1]==" " and acro[2][-1]==" "):
            acro[0] = acro[0][:-1]
            acro[1] = acro[1][:-1]
            acro[2] = acro[2][:-1]
        while len(acro)!= 0 and acro[0].count(" ") == len(acro[0]):
            acro = acro[1:]
        while len(acro)!= 0 and acro[-1].count(" ") == len(acro[-1]):
            acro = acro[:-1]
            
        return acro
                
                
    def isShapeless(self):
        
        return self.is1x1()
                
                
    def getItemAcronym(self, usedItems, stack):
        
        if stack.item != None and stack.item in usedItems:
            return self.ACRO[usedItems.index(stack.item)]
        return " "
                
                
    def completeModData(self):
        
        for k in self.data.keys():
            self.data[k] = []
        
        success = True
        
        usedItems = []
        usedStacks = []
        for stack in self.items:
            if stack.item != None and not stack.item.identifier+";"+stack.item.text() in [item.identifier+";"+item.text() for item in usedItems]:
                usedItems.append(stack.item)
                
        usedStacks = []
        for stack in self.items[:-1]:
            if stack.item != None and not stack.item.identifier+";"+stack.item.text() in [s.item.identifier+";"+s.item.text() for s in usedStacks]:
                usedStacks.append(stack)
                
        if self.shaped:
            recipe = [[self.getItemAcronym(usedItems, self.items[0]), self.getItemAcronym(usedItems, self.items[1]), self.getItemAcronym(usedItems, self.items[2])],
                      [self.getItemAcronym(usedItems, self.items[3]), self.getItemAcronym(usedItems, self.items[4]), self.getItemAcronym(usedItems, self.items[5])],
                      [self.getItemAcronym(usedItems, self.items[6]), self.getItemAcronym(usedItems, self.items[7]), self.getItemAcronym(usedItems, self.items[8])]]
            recipe = ",\n".join(['"'+"".join(c)+'"' for c in self.crop(recipe)])
            self.data["grid"] += [recipe]
            #output
            self.data["output"] += [self.items[9].getItemStack()]
            #the items used with their acronym
            items = []
            for i in range(len(usedItems)):
                items.append("'"+self.ACRO[i]+"'")
                items.append(usedItems[i].instancename)
            self.data["items"] += [", ".join(items)]
            
        else:
            self.data["output"] += [self.items[9].getItemStack()]
            self.data["inputs"] += [", ".join([s.getItemStack() for s in usedStacks])]
        
        return success
        
        
    def generateSrc(self, src):
        
        for d in self.data.keys():
            src = src.replace("<"+d+">", "\n".join(self.data[d]))
            
        return src
        
        
    def getSrc(self):
        
        if self.shaped:
            src = SrcCraftingTable.recipeShaped
        else:
            src = SrcCraftingTable.recipeShapeless
        return self.generateSrc(src)
        
        
    def save(self):
        
        data = {}
        
        data["items"] = []
        for i in self.items:
            data["items"].append(i.save())
        data["name"] = str(self.text())
        data["shaped"] = self.shaped
        
        return data
        
        
    def load(self, data):
        
        self.setText(data["name"])
        self.shaped = data["shaped"]
        for i in range(len(data["items"])):
            self.items[i].load(data["items"][i])





def init(mainWindow):
    
    return
    
    
    
def onProjectCreated(mainWindow):
    
    mainWindow.project.addObject(CraftingTable(mainWindow, "CraftingTable"))