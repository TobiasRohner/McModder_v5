# -*- coding: utf-8 -*-
import os
import sys
import pickle
from PyQt4 import QtGui, QtCore, uic
from classes import _base, source



BASEPATH = os.path.dirname(sys.argv[0])




class Block(_base):
    
    def __init__(self, mainWindow, name):
        _base.__init__(self, mainWindow, "Block")
        
        self.name = name
        self.textureMode = False
        self.texture = [BASEPATH+"/assets/textures/blocks/unknown.png"]*6
        self.transparency = "auto"
        self.material = "Material.rock"
        self.creativeTab = "CreativeTabs.tabBlock"
        self.hardness = 2.0
        self.resistance = 10.0
        self.tool = "pickaxe"
        self.harvestLevel = 0
        
        self.data = {"package":[],
                     "imports":[],
                     "classname":[],
                     "unlocalizedName":[],
                     "material":[],
                     "creativeTab":[],
                     "hardness":[],
                     "resistance":[],
                     "tool":[],
                     "harvestLevel":[]}
        
        self.mainWindow.projectExplorer.updateWorkspace()
        
        self.initUI()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(BASEPATH+"/ui/Block.ui", self)
        
        self.connect(self.textureModeInput, QtCore.SIGNAL("stateChanged(int)"), self.setTextureMode)
        self.connect(self.singleTextureInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setSingleTexture)
        self.connect(self.multiTextureTopInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureTop)
        self.connect(self.multiTextureBottomInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureBottom)
        self.connect(self.multiTextureFrontInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureFront)
        self.connect(self.multiTextureBackInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureBack)
        self.connect(self.multiTextureLeftInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureLeft)
        self.connect(self.multiTextureRightInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureRight)
        self.connect(self.singleTextureButton, QtCore.SIGNAL("clicked()"), self.setSingleTextureButton)
        self.connect(self.multiTextureTopButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureTopButton)
        self.connect(self.multiTextureBottomButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureBottomButton)
        self.connect(self.multiTextureFrontButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureFrontButton)
        self.connect(self.multiTextureBackButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureBackButton)
        self.connect(self.multiTextureLeftButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureLeftButton)
        self.connect(self.multiTextureRightButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureRightButton)
        self.connect(self.transparentButton, QtCore.SIGNAL("clicked(bool"), self.setTransparent)
        self.connect(self.nonTransparentButton, QtCore.SIGNAL("clicked(bool"), self.setNonTransparent)
        self.connect(self.autoDetectTransparencyButton, QtCore.SIGNAL("clicked(bool"), self.setAutoDetectTransparent)
        
        
    def setName(self, name):
        
        self.mainWindow.updateName(self, name)
        
        self.save()
        
        
    def setTextureMode(self, mode):
        
        self.textureMode = mode == QtCore.Qt.Checked
        
        self.textureStack.setCurrentIndex(1 if self.textureMode else 0)
        
        self.save()
        
        
    def setSingleTexture(self, texture):
        
        self.texture = [texture]*6
        
        self.multiTextureTopInput.setText(texture)
        self.multiTextureBottomInput.setText(texture)
        self.multiTextureFrontInput.setText(texture)
        self.multiTextureBackInput.setText(texture)
        self.multiTextureLeftInput.setText(texture)
        self.multiTextureRightInput.setText(texture)
        
        self.save()
        
        
    def setMultiTextureTop(self, texture):
        
        self.texture[0] = texture
        
        self.singleTextureInput.setText(texture)
        
        self.save()
        
        
    def setMultiTextureBottom(self, texture):
        
        self.texture[1] = texture
        
        self.save()
        
        
    def setMultiTextureFront(self, texture):
        
        self.texture[2] = texture
        
        self.save()
        
        
    def setMultiTextureBack(self, texture):
        
        self.texture[3] = texture
        
        self.save()
        
        
    def setMultiTextureLeft(self, texture):
        
        self.texture[4] = texture
        
        self.save()
        
        
    def setMultiTextureRight(self, texture):
        
        self.texture[5] = texture
        
        self.save()
        
        
    def setSingleTextureButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture = [txt]*6
            self.singleTextureInput.setText(txt)
            self.multiTextureTopInput.setText(txt)
            self.multiTextureBottomInput.setText(txt)
            self.multiTextureFrontInput.setText(txt)
            self.multiTextureBackInput.setText(txt)
            self.multiTextureLeftInput.setText(txt)
            self.multiTextureRightInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureTopButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[0] = txt
            self.multiTextureTopInput.setText(txt)
            self.singleTextureInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureBottomButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[1] = txt
            self.multiTextureBottomInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureFrontButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[2] = txt
            self.multiTextureFrontInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureBackButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[3] = txt
            self.multiTextureBackInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureLeftButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[4] = txt
            self.multiTextureLeftInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureRightButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[5] = txt
            self.multiTextureRightInput.setText(txt)
            
        self.save()
        
        
    def setTransparent(self, checked):
        
        if checked:
            self.transparency = "transparent"
            
        self.save()
        
        
    def setNonTransparent(self, checked):
        
        if checked:
            self.transparency = "nontransparent"
            
        self.save()
        
        
    def setAutoDetectTransparent(self, checked):
        
        if checked:
            self.transparency = "auto"
            
        self.save()
            
        
        
    def save(self):
        
        if not os.path.exists(self.mainWindow.config["workspace"]+"/"+self.project.name+"/mod/"+self.identifier):
            os.makedirs(self.mainWindow.config["workspace"]+"/"+self.project.name+"/mod/"+self.identifier)
        
        f = open(self.mainWindow.config["workspace"]+"/"+self.project.name+"/mod/"+self.identifier+"/"+self.name+".mod", "w")
        
        data = {"name":self.name,
                "textureMode":self.textureMode,
                "texture":self.texture,
                "transparency":self.transparency}
        pickle.dump(data, f)
        
        f.close()
        
        
    def renewWidgetEntrys(self):
        
        self.nameInput.setText(self.name)
        self.singleTextureInput.setText(self.texture[0])
        self.multiTextureTopInput.setText(self.texture[0])
        self.multiTextureBottomInput.setText(self.texture[1])
        self.multiTextureFrontInput.setText(self.texture[2])
        self.multiTextureBackInput.setText(self.texture[3])
        self.multiTextureLeftInput.setText(self.texture[4])
        self.multiTextureRightInput.setText(self.texture[5])
        self.transparentButton.setDown(self.transparency == "transparent")
        self.nonTransparentButton.setDown(self.transparency == "nontransparent")
        self.autoDetectTransparencyButton.setDown(self.transparency == "auto")
        self.textureModeInput.setCheckState(QtCore.Qt.Checked if self.textureMode else QtCore.Qt.Unchecked)
        self.textureStack.setCurrentIndex(1 if self.textureMode else 0)
        
        
    def addToModData(self, cls):
        
        data = {}
        
        if cls.identifier == "BaseMod":
            
            data["imports"] = ["import "+self.package()+";",
                               "import net.minecraft.block.Block;"]
            
            data["declarations"] = ["    public static Block "+self.instancename()+";"]
            
            src = source.SrcBlock.commonInit
            src = src.replace("<instancename>", self.instancename())
            src = src.replace("<classname>", self.classname())
            data["commonInit"] = [src]
            
        return data
        
        
    def completeModData(self):
        """ask every class in the project, if it has to add something to the mod data of the base mod"""
        for k in self.data.keys():
            self.data[k] = []
        
        success = True
        for t in self.project.objects.keys():
            for cls in self.project.objects[t]:
                
                toAdd = cls.addToModData(self)
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
        self.data["name"] += [self.name]
        self.data["unlocalizedName"] += [self.unlocalizedName()]
        self.data["classname"] += [self.classname()]
        self.data["creativeTab"] += [self.creativeTab]
        self.data["imports"] += [source.SrcItem.imports]
        self.data["imports"] += ["import net.minecraft.creativetab.CreativeTabs;"]
                        
        if success:
            self.mainWindow.console.write(self.name+": Successfully completed Mod Data")
        
        
        
        
def createItem(mainWindow):
    
    name, ok = QtGui.QInputDialog.getText(mainWindow, mainWindow.translations.getTranslation("newBlock"), mainWindow.translations.getTranslation("name"))
    if ok:
        mainWindow.addObject(Block(mainWindow, name))


def init(mainWindow):
    
    newItemMenubar = QtGui.QAction(mainWindow.translations.getTranslation("block"), mainWindow)
    mainWindow.newMenubar.addAction(newItemMenubar)
    mainWindow.connect(newItemMenubar, QtCore.SIGNAL('triggered()'), lambda: createItem(mainWindow))