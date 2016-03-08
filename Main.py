# -*- coding: utf-8 -*-
import sys
import os
import shutil
import imp
import json
import widgets
from utils import translations, gradlew, Config, History
from classes import source
from PyQt4 import QtGui, QtCore, uic

import logging
logging.basicConfig()

try:
    import addons
except:
    pass

#Tricking py2exe Package Compilation
try:
    from OpenGL.platform import win32
except AttributeError:
    pass
try:
    from OpenGL import wrapper
except TypeError:
    pass
try:
    from OpenGL import converters
except TypeError:
    pass



BASEPATH = os.path.dirname(sys.argv[0])

CONFIGPATH = BASEPATH+"/config"

VERSION = "1.1.0-beta"   #Semantic versioning




def getPythonFiles(path):
    
    files = []
    if os.path.isdir(path):
        for c in os.listdir(path):
            if os.path.isdir(path+"/"+c):
                files += getPythonFiles(path+"/"+c)
            else:
                if c.split(".")[-1] == "py":
                    files.append(path+"/"+c)
    else:
        files.append(path)
    return files




class MainWindow(QtGui.QMainWindow):
    """
    Main Window operates as a common parent of all objects, over which they can communicate.
    """
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.addons = []
        
        #load the config
        self.config = Config(CONFIGPATH)
        if  not os.path.exists(CONFIGPATH):
            self.initializeConfig()
        self.config.loadData()
        
        self.history = History(100)
        
        self.translations = translations.Translations(self.config["language"])
        
        self.project = widgets.ProjectExplorer(self, "")
        self.projectPath = ""
        
        self.baseModClass = None
        self.guiClass = None
        
        self.initUI()
        self.initializeAddons()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(BASEPATH+"/ui/MainWindow.ui", self)
        
        self.editor = widgets.Editor(self)
        self.console = widgets.Console(self)
        
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.project)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.editor)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.console)
        
        self.newProjectMenubar = QtGui.QAction(QtGui.QIcon(BASEPATH+"/assets/icons/newProject.png"), self.translations.getTranslation("newProject"), self)
        self.openProjectMenubar = QtGui.QAction(self.translations.getTranslation("open"), self)
        self.openProjectMenubar.setShortcut("Ctrl+O")
        self.saveProjectMenubar = QtGui.QAction(self.translations.getTranslation("save"), self)
        self.saveProjectMenubar.setShortcut("Ctrl+S")
        self.exportProjectMenubar = QtGui.QAction(QtGui.QIcon(BASEPATH+"/assets/icons/export.png"), self.translations.getTranslation("exportProject"), self)
        self.exportProjectMenubar.setShortcut("Ctrl+E")
        self.exportJarMenubar = QtGui.QAction(self.translations.getTranslation("exportJar"), self)
        self.exportJarMenubar.setShortcut("Ctrl+Shift+E")
        self.runClientMenubar = QtGui.QAction(self.translations.getTranslation("runClient"), self)
        self.runClientMenubar.setShortcut("F5")
        self.undoMenubar = QtGui.QAction(self.translations.getTranslation("undo"), self)
        self.undoMenubar.setShortcut("Ctrl+Z")
        self.redoMenubar = QtGui.QAction(self.translations.getTranslation("redo"), self)
        self.redoMenubar.setShortcut("Ctrl+Y")
        self.addonsMenubar = QtGui.QAction(self.translations.getTranslation("addons"), self)
        self.delMenubar = QtGui.QAction(self.translations.getTranslation("delete"), self)
        self.delMenubar.setShortcut("Del")
        
        self.menubar = self.menuBar()
        
        self.fileMenubar = self.menubar.addMenu(self.translations.getTranslation("file"))
        self.editMenubar = self.menubar.addMenu(self.translations.getTranslation("edit"))
        self.newMenubar = self.menubar.addMenu(self.translations.getTranslation("new"))
        self.runMenubar = self.menubar.addMenu(self.translations.getTranslation("run"))
        self.optionMenubar = self.menubar.addMenu(self.translations.getTranslation("options"))
        
        self.projectToolbar = self.addToolBar("Project")
        self.runToolbar = self.addToolBar("Run")
        
        self.fileMenubar.addAction(self.newProjectMenubar)
        self.fileMenubar.addAction(self.openProjectMenubar)
        self.fileMenubar.addAction(self.saveProjectMenubar)
        self.fileMenubar.addAction(self.exportProjectMenubar)
        self.fileMenubar.addAction(self.exportJarMenubar)
        
        self.editMenubar.addAction(self.undoMenubar)
        self.editMenubar.addAction(self.redoMenubar)
        self.editMenubar.addAction(self.delMenubar)
        
        self.runMenubar.addAction(self.runClientMenubar)
        
        self.optionMenubar.addAction(self.addonsMenubar)
        
        self.projectToolbar.addAction(self.newProjectMenubar)
        self.projectToolbar.addAction(self.exportProjectMenubar)
        
        self.runToolbar.addAction(self.runClientMenubar)
        
        self.connect(self.newProjectMenubar, QtCore.SIGNAL('triggered()'), self.createNewProject)
        self.connect(self.openProjectMenubar, QtCore.SIGNAL('triggered()'), self.openProject)
        self.connect(self.saveProjectMenubar, QtCore.SIGNAL('triggered()'), self.save)
        self.connect(self.exportProjectMenubar, QtCore.SIGNAL('triggered()'), self.exportProject)
        self.connect(self.exportJarMenubar, QtCore.SIGNAL('triggered()'), self.exportJar)
        self.connect(self.undoMenubar, QtCore.SIGNAL('triggered()'), self.undo)
        self.connect(self.redoMenubar, QtCore.SIGNAL('triggered()'), self.redo)
        self.connect(self.runClientMenubar, QtCore.SIGNAL('triggered()'), self.runClient)
        self.connect(self.addonsMenubar, QtCore.SIGNAL('triggered()'), self.openAddonDialog)
        self.connect(self.delMenubar, QtCore.SIGNAL('triggered()'), self.delete)
        
        self.setCentralWidget(None)
        self.setDockNestingEnabled(True)
        
        
    def initializeConfig(self):
        """
        Write the most rudamentary config to disk.
        """
        
        self.config["language"] = "English"
        self.config["addons"] = [BASEPATH+"/addons/BaseMod/BaseMod.py",
                                 BASEPATH+"/addons/Block/Block.py",
                                 BASEPATH+"/addons/Item/Item.py",
                                 BASEPATH+"/addons/GUI/CraftingTable.py"]
        
        self.config.saveData()
        
        
    def initializeAddons(self):
        """
        Load all the addons from the paths found in the config.
        """
        
        self.addons = []
        
        for path in self.config["addons"]:
            for f in getPythonFiles(path):
                name = f.split("/")[-1].split(".")[0]
                mod = imp.load_source(name, f)
                if "init" in dir(mod):
                    self.addons.append((name, path, mod))
        
        for name, path, mod in self.addons:
            if "init" in dir(mod):
                mod.init(self)
                print("Initialized "+name)
                if name == "BaseMod":
                    self.baseModClass = mod
                elif name == "GUI":
                    self.guiClass = mod
                
                
    def openAddonDialog(self):
        
        widgets.Addons(self)
        
        
    def updateName(self, obj, name):
        """
        MainWindow.updateName(classes._base, str)
        
        Update the name of a Minecraft object.
        
        Args:
            obj (classes._base):    The object to rename
            name (str):             The new name of the object
        """
        
        self.editor.renameTab(obj, name)
        self.project.renameObject(obj, name)
        obj.name = name
        
        
    def addObject(self, obj):
        """
        MainWindow.addObject(classes._base)
        
        Add a new Minecraft object to the project.
        
        Args:
            obj (classes._base):    The object to add
        """
        
        self.project.addObject(obj)
        self.editor.openTab(obj)
        self.editor.tabWidget.setCurrentWidget(obj)
        
        
    def delete(self):
        """
        Delete the currently selected object, if the 'deleteable' flag is set to true.
        """
        
        selected = self.project.selectedObject()
        if selected.deleteable:
            self.project.removeObject(selected)
            self.editor.closeTab(self.editor.tabWidget.indexOf(selected))
        
        
    def runClient(self):
        """
        Run Minecraft with the current Mod loaded.
        """
        
        self.save()
        
        self.console.clear()
        
        self.exportProject()
        
        path = self.projectPath
        gradlew.runClient(path, self.console)
        
        
    def createNewProject(self):
        """
        Create a new project and set up the forge modding environment.
        """
        
        self.console.clear()
        
        projectpath = BASEPATH+"/Projects" if os.path.exists(BASEPATH+"/Projects") else "C:/"
        path = str(QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', projectpath, QtGui.QFileDialog.ShowDirsOnly))
        if path != "":
            name, ok = QtGui.QInputDialog.getText(self, self.translations.getTranslation("newProject"), self.translations.getTranslation("name"))
            name = str(name)
            if ok:
                self.projectPath = path+"/"+name
                self.project.name = name
                #build the file structure
                os.mkdir(self.projectPath)
                #file to mark the folder as a project
                f = open(self.projectPath+"/mcmodderproject", "w")
                f.write(VERSION)
                f.close()
                #install forge modloader
                gradlew.installForge(self.projectPath, self.console)
                
                #generate a BaseMod instance
                for n, p, addon in self.addons:
                    if "onProjectCreated" in dir(addon):
                        addon.onProjectCreated(self)
                
                self.save()
                
                
    def openProject(self):
        """
        Open a project from disk.
        """
        
        projectpath = BASEPATH+"/Projects" if os.path.exists(BASEPATH+"/Projects") else "C:/"
        path = str(QtGui.QFileDialog.getOpenFileName(self, self.translations.getTranslation("openProject"),
                                                           projectpath,
                                                           "JSON-Files"+" (*.json)"))
        if not path == "":
            self.projectPath = "/".join(path.replace("\\", "/").split("/")[:-1])
            self.project.load(path)
            
            
    def exportProject(self):
        """
        Export the current project's java source code.
        """
        
        self.save()
        
        #clear the current project
        path = self.projectPath+"/src/main"
        if os.path.exists(path):
            shutil.rmtree(path)
            
        os.makedirs(path+"/java")
        os.makedirs(path+"/resources")
        
        #export the newly compiled source code
        for t in self.project.objects.keys():
            for cls in self.project.objects[t]:
                cls.completeModData()
        
        for t in self.project.objects.keys():
            for cls in self.project.objects[t]:
                cls.export()
                
                
    def exportJar(self):
        """
        Export the current project as a .jar file.
        """
        
        path = str(QtGui.QFileDialog.getExistingDirectory(None, self.translations.getTranslation("destinationSelection"),
                                                          self.projectPath+"/java/build/libs",
                                                          QtGui.QFileDialog.ShowDirsOnly))
        if path != "":
            buildGradle = open(self.projectPath+"/java/build.gradle", "w")
            gradleSrc = source.SrcBuildGradle.main
            gradleSrc = gradleSrc.replace("<version>", self.project.objects["BaseMod"][0].version)
            gradleSrc = gradleSrc.replace("<mainPackage>", self.project.objects["BaseMod"][0].package())
            gradleSrc = gradleSrc.replace("<modname>", self.project.objects["BaseMod"][0].name)
            buildGradle.write(gradleSrc)
            buildGradle.close()
            
            self.exportProject()
            gradlew.exportMod(self.projectPath, self.console)
            if self.projectPath+"/java/build/libs/"+self.project.objects["BaseMod"][0].modid()+"-"+self.project.objects["BaseMod"][0].version+".jar" != path+"/"+self.project.objects["BaseMod"][0].modid()+"-"+self.project.objects["BaseMod"][0].version+".jar":
                shutil.copy2(self.projectPath+"/java/build/libs/"+self.project.objects["BaseMod"][0].modid()+"-"+self.project.objects["BaseMod"][0].version+".jar",
                             path+"/"+self.project.objects["BaseMod"][0].modid()+"-"+self.project.objects["BaseMod"][0].version+".jar")
                os.remove(self.projectPath+"/java/build/libs/"+self.project.objects["BaseMod"][0].modid()+"-"+self.project.objects["BaseMod"][0].version+".jar")
                
                
    def save(self):
        """
        Save the current project to disk after creating a backup of the current savefile.
        """
        
        if os.path.exists(self.projectPath+"/moddata.json"):
            shutil.copy2(self.projectPath+"/moddata.json", self.projectPath+"/moddata.backup")
        
        f = open(self.projectPath+"/moddata.json", "w")
        
        data = self.project.save()
        data["Version"] = VERSION
        json.dump(data, f, indent=4, separators=(',', ': '))
        
        f.close()
        
        self.console.write("Saved Mod to "+self.projectPath)
        
        self.project.unsavedChanges = False
                
                
    def undo(self):
        
        self.history.undo()
        
        
    def redo(self):
        
        self.history.redo()
        
        
        
        
        
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())