# -*- coding: utf-8 -*-
import os
import sys
import pickle
import shutil
from PyQt4 import QtGui, QtCore, uic
from classes import _base, source
from widgets import menus, BlockModelGenerator
from utils import textureAttributes



BASEPATH = os.path.dirname(sys.argv[0])




class Block(_base):
    
    def __init__(self, mainWindow, name):
        _base.__init__(self, mainWindow, "Block")
        
        self.name = name
        self.texture = [BASEPATH+"/assets/textures/blocks/unknown.png"]*6
        self.transparency = "auto"
        self.material = "Material.rock"
        self.creativeTab = "Building Blocks"
        self.hardness = 2.0
        self.resistance = 10.0
        self.tool = "pickaxe"
        self.harvestLevel = 0
        self.rotateable = True
        
        self.modeldata = [{'cuboids':
                            [{'textures':
                                [BASEPATH+'/assets/textures/blocks/unknown.png',
                                 BASEPATH+'/assets/textures/blocks/unknown.png',
                                 BASEPATH+'/assets/textures/blocks/unknown.png',
                                 BASEPATH+'/assets/textures/blocks/unknown.png',
                                 BASEPATH+'/assets/textures/blocks/unknown.png',
                                 BASEPATH+'/assets/textures/blocks/unknown.png'],
                            'name': 'unnamed',
                            'uvs':
                                [[[0.0, 0.0], [1.0, 1.0]],
                                 [[0.0, 0.0], [1.0, 1.0]],
                                 [[0.0, 0.0], [1.0, 1.0]],
                                 [[0.0, 0.0], [1.0, 1.0]],
                                 [[0.0, 0.0], [1.0, 1.0]],
                                 [[0.0, 0.0], [1.0, 1.0]]],
                            'translation': [0.0, 0.0, 0.0],
                            'rotation': [0.0, 0.0, 0.0],
                            'dimensions': [16.0, 16.0, 16.0]}]},
                        ""]
        
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
        self.connect(self.transparentButton, QtCore.SIGNAL("toggled(bool)"), self.setTransparent)
        self.connect(self.nonTransparentButton, QtCore.SIGNAL("toggled(bool)"), self.setNonTransparent)
        self.connect(self.autoDetectTransparencyButton, QtCore.SIGNAL("toggled(bool)"), self.setAutoDetectTransparent)
        self.connect(self.creativeDropdown, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.setCreativeTab)
        self.connect(self.rotateableInput, QtCore.SIGNAL("stateChanged(int)"), self.setRotateable)
        self.connect(self.editBlockButton, QtCore.SIGNAL("clicked()"), self.editBlock)
        
        
    def setName(self, name):
        
        self.mainWindow.updateName(self, name)
        
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
        
        
    def editBlock(self):
        
        self.modeldata = BlockModelGenerator.getModel(self.mainWindow, self.modeldata[0])
        self.save()
        
        
    def getRenderLayer(self):
        
        if self.transparency == "nontransparent":
            return "SOLID"
            
        else:
            layer = "SOLID"
            for cub in self.modeldata[0]["cuboids"]:
                for tex in cub["textures"]:
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
                "transparency":self.transparency,
                "creativeTab":self.creativeTab,
                "rotateable":self.rotateable,
                "modeldata":self.modeldata}
        pickle.dump(data, f)
        
        f.close()
        
        
    def renewWidgetEntrys(self):
        
        self.nameInput.setText(self.name)
        self.transparentButton.setDown(self.transparency == "transparent")
        self.nonTransparentButton.setDown(self.transparency == "nontransparent")
        self.autoDetectTransparencyButton.setDown(self.transparency == "auto")
        self.creativeDropdown.setCurrentIndex(self.creativeDropdown.findText(self.creativeTab))
        self.rotateableInput.setCheckState(QtCore.Qt.Checked if self.rotateable else QtCore.Qt.Unchecked)
        
        
    def pull(self, cls):
        
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
                
                toAdd = cls.pull(self)
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
        if self.rotateable:
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
        if self.rotateable:
            f.write(self.generateSrc(source.SrcBlock.blockstatesJsonRotateable))
        else:
            f.write(self.generateSrc(source.SrcBlock.blockstatesJson))
        f.close()
        
        """Export the blockmodel"""
        path = self.mainWindow.config["workspace"]+"/"+self.project.name+"/java/src/main/resources/assets/"+self.data["modid"][0]+"/models/block"
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path+"/"+self.classname()+".json", "w")
        f.write(self.generateSrc(self.modeldata[1]))
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
        for idx in range(len(self.modeldata[2])):
            shutil.copy2(self.modeldata[2][idx], path+"/"+self.unlocalizedName()+"_"+str(idx)+".png")
        
        self.mainWindow.console.write(self.name+": Successfully exported to "+path+"/"+self.package().replace(".", "/")+"/"+self.classname()+".java")
        
        
        
        
def createBlock(mainWindow):
    
    name, ok = QtGui.QInputDialog.getText(mainWindow, mainWindow.translations.getTranslation("newBlock"), mainWindow.translations.getTranslation("name"))
    if ok:
        mainWindow.addObject(Block(mainWindow, name))


def init(mainWindow):
    
    newItemMenubar = QtGui.QAction(mainWindow.translations.getTranslation("block"), mainWindow)
    mainWindow.newMenubar.addAction(newItemMenubar)
    mainWindow.connect(newItemMenubar, QtCore.SIGNAL('triggered()'), lambda: createBlock(mainWindow))