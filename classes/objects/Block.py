# -*- coding: utf-8 -*-
import os
import sys
import pickle
import shutil
from PyQt4 import QtGui, QtCore, uic
from classes import _base, source
from widgets import menus
from utils import textureAttributes



BASEPATH = os.path.dirname(sys.argv[0])




class Block(_base):
    
    def __init__(self, mainWindow, name):
        _base.__init__(self, mainWindow, "Block")
        
        self.name = name
        self.multitextured = False
        self.texture = [BASEPATH+"/assets/textures/blocks/unknown.png"]*6
        self.transparency = "auto"
        self.material = "Material.rock"
        self.creativeTab = "Building Blocks"
        self.hardness = 2.0
        self.resistance = 10.0
        self.tool = "pickaxe"
        self.harvestLevel = 0
        self.rotateable = True
        
        self.data = {"package":[],
                     "imports":[],
                     "classname":[],
                     "unlocalizedName":[],
                     "material":[],
                     "creativeTab":[],
                     "hardness":[],
                     "resistance":[],
                     "tool":[],
                     "harvestLevel":[],
                     "modid":[],
                     "additionalAttributes":[],
                     "additionalDeclarations":[]}
        
        self.mainWindow.projectExplorer.updateWorkspace()
        
        self.initUI()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(BASEPATH+"/ui/Block.ui", self)
        
        self.creativeDropdown = menus.CreativeTabDropdown.CreativeDropdown(self.mainWindow)
        self.ui.propertiesForm.addRow(self.mainWindow.translations.getTranslation("creativeTab")+":", self.creativeDropdown)
        
        self.connect(self.nameInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setName)
        self.connect(self.textureModeInput, QtCore.SIGNAL("stateChanged(int)"), self.setTextureMode)
        self.connect(self.singleTextureInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setSingleTexture)
        self.connect(self.multiTextureDownInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureDown)
        self.connect(self.multiTextureUpInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureUp)
        self.connect(self.multiTextureNorthInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureNorth)
        self.connect(self.multiTextureSouthInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureSouth)
        self.connect(self.multiTextureWestInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureWest)
        self.connect(self.multiTextureEastInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setMultiTextureEast)
        self.connect(self.singleTextureButton, QtCore.SIGNAL("clicked()"), self.setSingleTextureButton)
        self.connect(self.multiTextureDownButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureDownButton)
        self.connect(self.multiTextureUpButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureUpButton)
        self.connect(self.multiTextureNorthButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureNorthButton)
        self.connect(self.multiTextureSouthButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureSouthButton)
        self.connect(self.multiTextureWestButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureWestButton)
        self.connect(self.multiTextureEastButton, QtCore.SIGNAL("clicked()"), self.setMultiTextureEastButton)
        self.connect(self.transparentButton, QtCore.SIGNAL("toggled(bool)"), self.setTransparent)
        self.connect(self.nonTransparentButton, QtCore.SIGNAL("toggled(bool)"), self.setNonTransparent)
        self.connect(self.autoDetectTransparencyButton, QtCore.SIGNAL("toggled(bool)"), self.setAutoDetectTransparent)
        self.connect(self.creativeDropdown, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.setCreativeTab)
        self.connect(self.rotateableInput, QtCore.SIGNAL("stateChanged(int)"), self.setRotateable)
        
        
    def setName(self, name):
        
        self.mainWindow.updateName(self, name)
        
        self.save()
        
        
    def setTextureMode(self, mode):
        
        self.multitextured = mode == QtCore.Qt.Checked
        
        self.textureStack.setCurrentIndex(1 if self.multitextured else 0)
        
        self.save()
        
        
    def setSingleTexture(self, texture):
        
        self.texture = [texture]*6
        
        self.multiTextureDownInput.setText(texture)
        self.multiTextureUpInput.setText(texture)
        self.multiTextureNorthInput.setText(texture)
        self.multiTextureSouthInput.setText(texture)
        self.multiTextureWestInput.setText(texture)
        self.multiTextureEastInput.setText(texture)
        
        self.save()
        
        
    def setMultiTextureDown(self, texture):
        
        self.texture[0] = texture
        
        self.singleTextureInput.setText(texture)
        
        self.save()
        
        
    def setMultiTextureUp(self, texture):
        
        self.texture[1] = texture
        
        self.save()
        
        
    def setMultiTextureNorth(self, texture):
        
        self.texture[2] = texture
        
        self.save()
        
        
    def setMultiTextureSouth(self, texture):
        
        self.texture[3] = texture
        
        self.save()
        
        
    def setMultiTextureWest(self, texture):
        
        self.texture[4] = texture
        
        self.save()
        
        
    def setMultiTextureEast(self, texture):
        
        self.texture[5] = texture
        
        self.save()
        
        
    def setSingleTextureButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture = [txt]*6
            self.singleTextureInput.setText(txt)
            self.multiTextureDownInput.setText(txt)
            self.multiTextureUpInput.setText(txt)
            self.multiTextureNorthInput.setText(txt)
            self.multiTextureSouthInput.setText(txt)
            self.multiTextureWestInput.setText(txt)
            self.multiTextureEastInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureDownButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[0] = txt
            self.multiTextureDownInput.setText(txt)
            self.singleTextureInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureUpButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[1] = txt
            self.multiTextureUpInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureNorthButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[2] = txt
            self.multiTextureNorthInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureSouthButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[3] = txt
            self.multiTextureSouthInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureWestButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[4] = txt
            self.multiTextureWestInput.setText(txt)
            
        self.save()
        
        
    def setMultiTextureEastButton(self):
        
        txt = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
                                                          
        if txt != "":
            self.texture[5] = txt
            self.multiTextureEastInput.setText(txt)
            
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
        
        
    def setCreativeTab(self, tab):
        
        self.creativeTab = tab
        
        self.save()
        
        
    def setRotateable(self, rotateable):
        
        self.rotateable = rotateable
        
        self.save()
        
        
    def getRenderLayer(self):
        
        if self.transparency == "nontransparent":
            return "SOLID"
            
        else:
            layer = "SOLID"
            for tex in self.texture:
                alpha = textureAttributes.transparency(tex)
                if 0 in alpha and 255 in alpha and len(alpha) == 2:
                    if layer != "TRANSLUCENT":
                        layer = "CUTOUT"
                if sum([0 if a==0 or a==255 else 1 for a in alpha]):
                    layer = "TRANSLUCENT"
                    
        return layer
            
        
        
    def save(self):
        
        if not os.path.exists(self.mainWindow.config["workspace"]+"/"+self.project.name+"/mod/"+self.identifier):
            os.makedirs(self.mainWindow.config["workspace"]+"/"+self.project.name+"/mod/"+self.identifier)
        
        f = open(self.mainWindow.config["workspace"]+"/"+self.project.name+"/mod/"+self.identifier+"/"+self.name+".mod", "w")
        
        data = {"name":self.name,
                "multitextured":self.multitextured,
                "texture":self.texture,
                "transparency":self.transparency,
                "creativeTab":self.creativeTab,
                "rotateable":self.rotateable}
        pickle.dump(data, f)
        
        f.close()
        
        
    def renewWidgetEntrys(self):
        
        self.nameInput.setText(self.name)
        self.singleTextureInput.setText(self.texture[0])
        self.multiTextureDownInput.setText(self.texture[0])
        self.multiTextureUpInput.setText(self.texture[1])
        self.multiTextureNorthInput.setText(self.texture[2])
        self.multiTextureSouthInput.setText(self.texture[3])
        self.multiTextureWestInput.setText(self.texture[4])
        self.multiTextureEastInput.setText(self.texture[5])
        self.transparentButton.setDown(self.transparency == "transparent")
        self.nonTransparentButton.setDown(self.transparency == "nontransparent")
        self.autoDetectTransparencyButton.setDown(self.transparency == "auto")
        self.textureModeInput.setCheckState(QtCore.Qt.Checked if self.multitextured else QtCore.Qt.Unchecked)
        self.textureStack.setCurrentIndex(1 if self.multitextured else 0)
        self.creativeDropdown.setCurrentIndex(self.creativeDropdown.findText(self.creativeTab))
        self.rotateableInput.setCheckState(QtCore.Qt.Checked if self.rotateable else QtCore.Qt.Unchecked)
        
        
    def addToModData(self, cls):
        
        data = {}
        
        if cls.identifier == "BaseMod":
            
            data["imports"] = ["import "+self.package()+"."+self.classname()+";",
                               "import net.minecraft.block.Block;"]
            
            data["declarations"] = ["    public static Block "+self.instancename()+";"]
            
            src = source.SrcBlock.commonInit
            src = src.replace("<instancename>", self.instancename())
            src = src.replace("<classname>", self.classname())
            data["commonInit"] = [src]
            
            src = source.SrcBlock.clientInit
            src = src.replace("<instancename>", self.instancename())
            src = src.replace("<modid>", cls.modid())
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
                
                toAdd = cls.addToModData(self)
                for entry in toAdd.keys():
                    if entry in self.data.keys():
                        self.data[entry] += toAdd[entry]
                    else:
                        self.mainWindow.console.write("WARNING: Object "+cls.identifier+"."+cls.name+" tried to add data to unknown Index "+entry)
                        success = False
                
                if cls.identifier == "BaseMod":
                    self.data["imports"] += ["import "+cls.package()+"."+cls.classname()+";"]
                    self.data["modid"] += [cls.modid()]
                        
        self.data["package"] += [self.package()]
        self.data["unlocalizedName"] += [self.unlocalizedName()]
        self.data["classname"] += [self.classname()]
        self.data["creativeTab"] += [self.creativeDropdown.getTabClass(self.creativeTab)]
        self.data["imports"] += [source.SrcBlock.imports]
        self.data["imports"] += ["import net.minecraft.creativetab.CreativeTabs;"]
        self.data["material"] += [self.material]
        self.data["hardness"] += [str(self.hardness)]
        self.data["resistance"] += [str(self.resistance)]
        self.data["tool"] += [self.tool]
        self.data["harvestLevel"] += [str(self.harvestLevel)]
        if self.transparency == "auto" and self.getRenderLayer() != "SOLID":
            self.data["additionalAttributes"] += [source.SrcBlock.renderLayerTransparent.replace("<layer>", self.getRenderLayer())]
            self.data["imports"] += ["import net.minecraftforge.fml.relauncher.Side;"]
            self.data["imports"] += ["import net.minecraftforge.fml.relauncher.SideOnly;"]
            self.data["imports"] += ["import net.minecraft.util.EnumWorldBlockLayer;"]
        if self.transparency == "transparent":
            self.data["additionalAttributes"] += [source.SrcBlock.renderLayerTransparent.replace("<layer>", self.getRenderLayer().replace("SOLID", "CUTOUT"))]
            self.data["imports"] += ["import net.minecraftforge.fml.relauncher.Side;"]
            self.data["imports"] += ["import net.minecraftforge.fml.relauncher.SideOnly;"]
            self.data["imports"] += ["import net.minecraft.util.EnumWorldBlockLayer;"]
        if self.multitextured and self.rotateable:
            self.data["additionalDeclarations"] += [source.SrcBlock.rotateableDeclarations]
            self.data["additionalAttributes"] += [source.SrcBlock.rotateableAdditionalAttributes]
            self.data["imports"] += ["import net.minecraft.block.properties.PropertyDirection;"]
            self.data["imports"] += ["import net.minecraft.util.EnumFacing;"]
            self.data["imports"] += ["import net.minecraft.block.state.IBlockState;"]
            self.data["imports"] += ["import net.minecraft.world.World;"]
            self.data["imports"] += ["import net.minecraft.util.BlockPos;"]
            self.data["imports"] += ["import net.minecraft.entity.EntityLivingBase;"]
            self.data["imports"] += ["import net.minecraft.block.state.BlockState;"]
            self.data["imports"] += ["import net.minecraft.block.properties.IProperty;"]
                        
        if success:
            self.mainWindow.console.write(self.name+": Successfully completed Mod Data")
            
            
    def generateSrc(self, src):
        
        for d in self.data.keys():
            src = src.replace("<"+d+">", "\n".join(self.data[d]))
            
        return src
        
        
    def export(self):
        """Export the main java file"""
        path = self.mainWindow.config["workspace"]+"/"+self.project.name+"/java/src/main/java/"+self.package().replace(".", "/")
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path+"/"+self.classname()+".java", "w")
        f.write(self.generateSrc(source.SrcBlock.main))
        f.close()
        
        """Export the blockstates"""
        path = self.mainWindow.config["workspace"]+"/"+self.project.name+"/java/src/main/resources/assets/"+self.data["modid"][0]+"/blockstates"
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path+"/"+self.classname()+".json", "w")
        if self.rotateable and self.multitextured:
            f.write(self.generateSrc(source.SrcBlock.blockstatesJsonRotateable))
        else:
            f.write(self.generateSrc(source.SrcBlock.blockstatesJson))
        f.close()
        
        """Export the blockmodel"""
        path = self.mainWindow.config["workspace"]+"/"+self.project.name+"/java/src/main/resources/assets/"+self.data["modid"][0]+"/models/block"
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path+"/"+self.classname()+".json", "w")
        if self.multitextured:
            f.write(self.generateSrc(source.SrcBlock.blockmodelJsonMultiTexture))
        else:
            f.write(self.generateSrc(source.SrcBlock.blockmodelJsonSingleTexture))
        f.close()
        
        """Export the itemmodel"""
        path = self.mainWindow.config["workspace"]+"/"+self.project.name+"/java/src/main/resources/assets/"+self.data["modid"][0]+"/models/item"
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path+"/"+self.classname()+".json", "w")
        f.write(self.generateSrc(source.SrcBlock.itemmodelJson))
        f.close()
        
        """Export the textures"""
        path = self.mainWindow.config["workspace"]+"/"+self.project.name+"/java/src/main/resources/assets/"+self.data["modid"][0]+"/textures/blocks"
        if not os.path.exists(path):
            os.makedirs(path)
        if self.multitextured:
            shutil.copy2(self.texture[0], path+"/"+self.unlocalizedName()+"_down.png")
            shutil.copy2(self.texture[1], path+"/"+self.unlocalizedName()+"_up.png")
            shutil.copy2(self.texture[2], path+"/"+self.unlocalizedName()+"_north.png")
            shutil.copy2(self.texture[3], path+"/"+self.unlocalizedName()+"_south.png")
            shutil.copy2(self.texture[4], path+"/"+self.unlocalizedName()+"_west.png")
            shutil.copy2(self.texture[5], path+"/"+self.unlocalizedName()+"_east.png")
        else:
            shutil.copy2(self.texture[0], path+"/"+self.unlocalizedName()+".png")
        
        self.mainWindow.console.write(self.name+": Successfully exported to "+path+"/"+self.package().replace(".", "/")+"/"+self.classname()+".java")
        
        
        
        
def createItem(mainWindow):
    
    name, ok = QtGui.QInputDialog.getText(mainWindow, mainWindow.translations.getTranslation("newBlock"), mainWindow.translations.getTranslation("name"))
    if ok:
        mainWindow.addObject(Block(mainWindow, name))


def init(mainWindow):
    
    newItemMenubar = QtGui.QAction(mainWindow.translations.getTranslation("block"), mainWindow)
    mainWindow.newMenubar.addAction(newItemMenubar)
    mainWindow.connect(newItemMenubar, QtCore.SIGNAL('triggered()'), lambda: createItem(mainWindow))