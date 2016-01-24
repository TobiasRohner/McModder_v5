# -*- coding: utf-8 -*-
import sys
import os
import inspect
import shutil
import widgets
from utils import translations, gradlew, Config, loadClassLibrary, History
from classes import source
from PyQt4 import QtGui, QtCore, uic



BASEPATH = os.path.dirname(sys.argv[0])

CONFIGPATH = BASEPATH+"/config"

VERSION = "0.0.1"




class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        #load the config
        self.config = Config(CONFIGPATH)
        if  not os.path.exists(CONFIGPATH):
            self.initializeConfig()
        self.config.loadData()
        
        self.history = History(100)
        
        self.translations = translations.Translations(self.config["language"])
        
        self.projects = []
        
        self.initUI()
        self.initializeProjects()
        
        self.projectExplorer.updateWorkspace()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(BASEPATH+"/ui/MainWindow.ui", self)
        
        self.projectExplorer = widgets.ProjectExplorer(self)
        self.editor = widgets.Editor(self)
        self.console = widgets.Console(self)
        
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.projectExplorer)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.editor)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.console)
        
        self.newProjectMenubar = QtGui.QAction(QtGui.QIcon(BASEPATH+"/assets/icons/newProject.png"), self.translations.getTranslation("newProject"), self)
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
        
        self.menubar = self.menuBar()
        
        self.fileMenubar = self.menubar.addMenu(self.translations.getTranslation("file"))
        self.editMenubar = self.menubar.addMenu(self.translations.getTranslation("edit"))
        self.newMenubar = self.menubar.addMenu(self.translations.getTranslation("new"))
        self.runMenubar = self.menubar.addMenu(self.translations.getTranslation("run"))
        self.optionMenubar = self.menubar.addMenu(self.translations.getTranslation("options"))
        
        self.projectToolbar = self.addToolBar("Project")
        self.runToolbar = self.addToolBar("Run")
        
        self.fileMenubar.addAction(self.newProjectMenubar)
        self.fileMenubar.addAction(self.exportProjectMenubar)
        self.fileMenubar.addAction(self.exportJarMenubar)
        
        self.editMenubar.addAction(self.undoMenubar)
        self.editMenubar.addAction(self.redoMenubar)
        
        self.runMenubar.addAction(self.runClientMenubar)
        
        self.projectToolbar.addAction(self.newProjectMenubar)
        self.projectToolbar.addAction(self.exportProjectMenubar)
        
        self.runToolbar.addAction(self.runClientMenubar)
        
        self.initializeMinecraftObjects()
        
        self.connect(self.newProjectMenubar, QtCore.SIGNAL('triggered()'), self.createNewProject)
        self.connect(self.exportProjectMenubar, QtCore.SIGNAL('triggered()'), self.exportProject)
        self.connect(self.exportJarMenubar, QtCore.SIGNAL('triggered()'), self.exportJar)
        self.connect(self.undoMenubar, QtCore.SIGNAL('triggered()'), self.undo)
        self.connect(self.redoMenubar, QtCore.SIGNAL('triggered()'), self.redo)
        self.connect(self.runClientMenubar, QtCore.SIGNAL('triggered()'), self.runClient)
        
        self.setCentralWidget(None)
        self.setDockNestingEnabled(True)
        
        
    def initializeConfig(self):
        
        self.config["workspace"] = QtGui.QFileDialog.getExistingDirectory(None, 'Select a workspace:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        self.config["language"] = "English"
        
        self.config.saveData()
        
        
    def initializeMinecraftObjects(self):
        
        classes = [(cls, name) for name, cls in objects.__dict__.items() if inspect.ismodule(cls)]
        for cls, name in classes:
            if "init" in dir(cls):
                cls.init(self)
                print("Initialized "+name)
            
            
    def initializeProjects(self):
        
        proj = [f for f in os.listdir(self.config["workspace"]) if os.path.exists(self.config["workspace"]+"/"+f+"/mcmodderproject")]
        for p in proj:
            self.projects.append(Project.Project(self, p))
            self.projects[-1].load()
            
        self.projectExplorer.updateWorkspace()
        
        
    def updateName(self, obj, name):
        
        os.rename(self.config["workspace"]+"/"+obj.project.name+"/mod/"+obj.identifier+"/"+obj.name+".mod",
                  self.config["workspace"]+"/"+obj.project.name+"/mod/"+obj.identifier+"/"+name+".mod")
        self.editor.renameTab(obj, name)
        self.projectExplorer.renameObject(obj, name)
        obj.name = name
        
        
    def currentProject(self):
        
        nme = self.projectExplorer.selectedProject()
        for proj in self.projects:
            if proj.name == nme:
                return proj
        return None
        
        
    def addObject(self, obj):
        
        proj = self.currentProject()
        if proj:
            proj.addObject(obj)
            
        self.projectExplorer.updateWorkspace()
        self.editor.openTab(obj)
        self.editor.tabWidget.setCurrentWidget(obj)
        
        
    def runClient(self):
        
        self.exportProject()
        
        path = self.config["workspace"]+"/"+self.currentProject().name
        gradlew.runClient(path, self.console)
        
        
    def createNewProject(self):
            
        arg = Project.Constructor(self).getParams(self)
        if arg:
            #build the file structure
            os.mkdir(self.config["workspace"]+"/"+arg[0])
            os.mkdir(self.config["workspace"]+"/"+arg[0]+"/mod")
            os.mkdir(self.config["workspace"]+"/"+arg[0]+"/java")
            #file to mark the folder as a project
            f = open(self.config["workspace"]+"/"+arg[0]+"/mcmodderproject", "w")
            f.write(VERSION)
            f.close()
            #install forge modloader
            gradlew.installForge(self.config["workspace"]+"/"+arg[0]+"/java", self.console)
            
            #generate a BaseMod instance
            self.projects.append(Project.Project(self, arg[0]))
            self.projects[-1].addObject(objects.BaseMod.BaseMod(self, self.projects[-1], arg[0]))
            
            self.projectExplorer.updateWorkspace()
            
            
    def exportProject(self):
        
        proj = self.currentProject()
        
        #clear the current project
        path = self.config["workspace"]+"/"+proj.name+"/java/src/main"
        shutil.rmtree(path)
        
        #export the newly compiled source code
        for t in proj.objects.keys():
            for cls in proj.objects[t]:
                cls.completeModData()
        
        for t in proj.objects.keys():
            for cls in proj.objects[t]:
                cls.export()
                
                
    def exportJar(self):
        
        path = QtGui.QFileDialog.getExistingDirectory(None, self.translations.getTranslation("destinationSelection"),
                                                      self.config["workspace"]+"/"+self.currentProject().name+"/java/build/libs",
                                                      QtGui.QFileDialog.ShowDirsOnly)
        if path != "":
            buildGradle = open(self.config["workspace"]+"/"+self.currentProject().name+"/java/build.gradle", "w")
            gradleSrc = source.SrcBuildGradle.main
            gradleSrc = gradleSrc.replace("<version>", self.currentProject().objects["BaseMod"][0].version)
            gradleSrc = gradleSrc.replace("<mainPackage>", self.currentProject().objects["BaseMod"][0].package())
            gradleSrc = gradleSrc.replace("<modname>", self.currentProject().objects["BaseMod"][0].name)
            buildGradle.write(gradleSrc)
            buildGradle.close()
            
            self.exportProject()
            gradlew.exportMod(self.config["workspace"]+"/"+self.currentProject().name, self.console)
            if self.config["workspace"]+"/"+self.currentProject().name+"/java/build/libs/"+self.currentProject().objects["BaseMod"][0].modid()+"-"+self.currentProject().objects["BaseMod"][0].version+".jar" != path+"/"+self.currentProject().objects["BaseMod"][0].modid()+"-"+self.currentProject().objects["BaseMod"][0].version+".jar":
                shutil.copy2(self.config["workspace"]+"/"+self.currentProject().name+"/java/build/libs/"+self.currentProject().objects["BaseMod"][0].modid()+"-"+self.currentProject().objects["BaseMod"][0].version+".jar",
                             path+"/"+self.currentProject().objects["BaseMod"][0].modid()+"-"+self.currentProject().objects["BaseMod"][0].version+".jar")
                os.remove(self.config["workspace"]+"/"+self.currentProject().name+"/java/build/libs/"+self.currentProject().objects["BaseMod"][0].modid()+"-"+self.currentProject().objects["BaseMod"][0].version+".jar")
                
                
    def undo(self):
        
        self.history.undo()
        
        
    def redo(self):
        
        self.history.redo()
        
        
        
        
        
if __name__ == "__main__":
    
    loadClassLibrary.loadClasses()
    
    from classes import objects
    from classes import Project
    
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())