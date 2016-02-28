# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).replace("\\", "/").split("/")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import pickle
import shutil
import imp
from widgets import menus
from classes import _base
from PyQt4 import QtGui, QtCore, uic

SrcItem = imp.load_source("SrcItem", ADDONPATH+"/SrcItem.py")





class Item(_base):
    
    def __init__(self, mainWindow, name):
        _base.__init__(self, mainWindow, "Item", "Item")
        
        self.name = name
        self.texture = BASEPATH+"/assets/textures/items/unknown.png"
        self.creativeTab = "Misc"
        
        self.listWidgetItem.setText(self.name)
        self.listWidgetItem.instancename = self.instancename()
        
        self.data = {"package":[],
                     "imports":[],
                     "classname":[],
                     "name":[],
                     "unlocalizedName":[],
                     "basemod":[],
                     "modid":[],
                     "creativeTab":[],
                     "texture":[]}
        
        self.initUI()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(ADDONPATH+"/Item.ui", self)
        
        self.creativeDropdown = menus.CreativeTabDropdown.CreativeDropdown(self.mainWindow)
        self.ui.propertiesForm.addRow(self.mainWindow.translations.getTranslation("creativeTab")+":", self.creativeDropdown)
        
        self.connect(self.nameInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setName)
        self.connect(self.textureInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setTexture)
        self.connect(self.textureButton, QtCore.SIGNAL("clicked()"), self.setTextureButton)
        self.connect(self.creativeDropdown, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.setCreativeTab)
        
        
    def setName(self, name):
        
        self.mainWindow.updateName(self, name)
        self.listWidgetItem.setText(name)
        self.listWidgetItem.instancename = self.instancename()
        
        
    def setTexture(self, texture):
        
        self.texture = texture
        self.listWidgetItem.updateIcon(texture)
        
        
    def setTextureButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.projectPath,
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if txt != "":
            self.texture = txt
            self.textureInput.setText(self.texture)
            self.listWidgetItem.updateIcon(self.texture)
        
        
    def setCreativeTab(self, tab):
        
        self.creativeTab = tab
        
        
    def renewWidgetEntrys(self):
        
        self.nameInput.setText(self.name)
        self.textureInput.setText(self.texture)
        self.creativeDropdown.setCurrentIndex(self.creativeDropdown.findText(self.creativeTab))
        
        
    def updateListWidgetItem(self):
        
        self.listWidgetItem.setText(self.name)
        self.listWidgetItem.updateIcon(self.texture)
        
        
    def save(self):
        
        data = {"identifier":self.identifier,
                "classtype":self.classtype,
                "name":self.name,
                "texture":self.texture,
                "creativeTab":self.creativeTab}
        return data
        
        
    def pull(self, cls):
        
        data = {}
        
        if cls.identifier == "BaseMod":
            
            data["imports"] = ["import "+self.package()+"."+self.classname()+";",
                               "import net.minecraft.item.Item;"]
            
            data["declarations"] = ["    public static Item "+self.instancename()+";"]
            
            src = SrcItem.commonInit
            src = src.replace("<instancename>", self.instancename())
            src = src.replace("<classname>", self.classname())
            data["commonInit"] = [src]
            
            src = SrcItem.clientInit
            src = src.replace("<instancename>", self.instancename())
            src = src.replace("<modid>", self.project.objects["BaseMod"][0].modid())
            src = src.replace("<unlocalizedName>", self.unlocalizedName())
            data["clientInit"] = [src]
            
        return data
        
        
    def completeModData(self):
        """ask every class in the project, if it has to add something to the mod data of the base mod"""
        for k in self.data.keys():
            self.data[k] = []
        
        success = True
        for t in self.project.objects.keys():
            for cls in self.project.objects[t]:
                
                toAdd = cls.pull(self)
                for entry in toAdd.keys():
                    if entry in self.data.keys():
                        self.data[entry] += toAdd[entry]
                    else:
                        self.mainWindow.console.write("WARNING: Object "+cls.identifier+"."+cls.name+" tried to add data to unknown Index "+entry)
                        success = False
                
                if cls.identifier == "BaseMod":
                    self.data["basemod"] += [cls.classname()]
                    self.data["modid"] += [cls.modid()]
                    self.data["imports"] += ["import "+cls.package()+"."+cls.classname()+";"]
                        
        self.data["package"] += [self.package()]
        self.data["imports"] += ["import net.minecraft.creativetab.CreativeTabs;"]
        self.data["name"] += [self.name]
        self.data["unlocalizedName"] += [self.unlocalizedName()]
        self.data["classname"] += [self.classname()]
        self.data["creativeTab"] += [self.creativeDropdown.getTabClass(self.creativeTab)]
        self.data["texture"] += [self.texture.split("/")[-1].split(".")[0]]
        self.data["imports"] += [SrcItem.imports]
                        
        if success:
            self.mainWindow.console.write(self.name+": Successfully completed Mod Data")
            
            
    def generateSrc(self):
        
        src = SrcItem.main
        
        for d in self.data.keys():
            src = src.replace("<"+d+">", "\n".join(self.data[d]))
            
        return src
        
        
    def generateJsonSrc(self):
        
        src = SrcItem.json
        
        for d in self.data.keys():
            src = src.replace("<"+d+">", "\n".join(self.data[d]))
            
        return src
        
        
    def export(self):
        
        path = self.mainWindow.projectPath+"/src/main/java/"+self.package().replace(".", "/")
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path+"/"+"/"+self.classname()+".java", "w")
        f.write(self.generateSrc())
        f.close()
        
        path = self.mainWindow.projectPath+"/src/main/resources/assets/"+self.data["modid"][0]+"/models/item"
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path+"/"+self.unlocalizedName()+".json", "w")
        f.write(self.generateJsonSrc())
        f.close()
        
        path = self.mainWindow.projectPath+"/src/main/resources/assets/"+self.data["modid"][0]+"/textures/items"
        if not os.path.exists(path):
            os.makedirs(path)
        shutil.copy2(self.texture, path+"/"+self.unlocalizedName()+".png")
        
        path = self.mainWindow.projectPath+"/src/main/java"
        self.mainWindow.console.write(self.name+": Successfully exported to "+path+"/"+self.package().replace(".", "/")+"/"+self.classname()+".java")
        
        
        
        
        
def createItem(mainWindow):
    
    name, ok = QtGui.QInputDialog.getText(mainWindow, mainWindow.translations.getTranslation("newItem"), mainWindow.translations.getTranslation("name"))
    if ok:
        mainWindow.addObject(Item(mainWindow, name))
        mainWindow.emit(QtCore.SIGNAL("UPDATE_ITEMLIST"))


def init(mainWindow):
    
    newItemMenubar = QtGui.QAction(mainWindow.translations.getTranslation("item"), mainWindow)
    mainWindow.newMenubar.addAction(newItemMenubar)
    mainWindow.connect(newItemMenubar, QtCore.SIGNAL('triggered()'), lambda: createItem(mainWindow))