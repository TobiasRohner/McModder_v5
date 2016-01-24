# -*- coding: utf-8 -*-
import os
import sys
import pickle
from PyQt4 import QtGui, QtCore, uic

from classes import source




BASEPATH = os.path.dirname(sys.argv[0])





class BaseMod(QtGui.QWidget):
    
    def __init__(self, mainWindow, project, name):
        QtGui.QWidget.__init__(self)
        
        self.identifier = "BaseMod"
        
        self.mainWindow = mainWindow
        self.project = project
        
        self.name = name
        self.version = "1.0"
        
        self.data = {"package":[],
                     "imports":[],
                     "classname":[],
                     "name":[],
                     "modid":[],
                     "version":[],
                     "proxies":[],
                     "declarations":[],
                     "preInit":[],
                     "commonInit":[],
                     "clientInit":[],
                     "postInit":[]}
        
        self.initUI()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(BASEPATH+"/ui/BaseMod.ui", self)

        self.connect(self.versionInput, QtCore.SIGNAL("textEdited(const QString&)"), self.setVersion)
        
        
    def setVersion(self, ver):
        
        self.mainWindow.history.addStep(self.setVersion, [self.version], self.setName, [ver])
        
        self.version = ver
        self.save()
        
        
    def renewWidgetEntrys(self):
        
        self.versionInput.setText(self.version)
        
        
    def save(self):
        
        if not os.path.exists(self.mainWindow.config["workspace"]+"/"+self.name+"/mod/"+self.identifier):
            os.makedirs(self.mainWindow.config["workspace"]+"/"+self.name+"/mod/"+self.identifier)
        
        f = open(self.mainWindow.config["workspace"]+"/"+self.name+"/mod/"+self.identifier+"/"+self.name+".mod", "w")
        
        data = {"name":self.name,
                "version":self.version}
        pickle.dump(data, f)
        
        f.close()
        
        
    def load(self, path):
        
        f = open(path, "r")
        
        data = pickle.load(f)
        for key in data.keys():
            value = data[key]
            if isinstance(value, u"".__class__) or isinstance(value, str):
                value = '"'+value+'"'
            exec("self."+key+"="+str(value))
        
        f.close()
        
        
    def classname(self):
        
        return self.name.replace(" ", "_")
        
        
    def modid(self):
        
        return self.classname().lower()
        
        
    def package(self):
        
        return self.project.name.replace(" ", "_")
        
        
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
                        
        self.data["package"] += [self.package()]
        self.data["classname"] += [self.classname()]
        self.data["name"] += [self.project.name]
        self.data["modid"] += [self.modid()]
        self.data["version"] += [self.version]
        self.data["proxies"] += [source.SrcBaseMod.proxies]
        self.data["imports"] += [source.SrcBaseMod.imports]
                        
        if success:
            self.mainWindow.console.write("BaseMod: Successfully completed Mod Data")
            
            
    def addToModData(self, cls):
        #TODO
        return {}
        
        
    def generateSrc(self):
        
        src = source.SrcBaseMod.main
        
        for d in self.data.keys():
            src = src.replace("<"+d+">", "\n".join(self.data[d]))
            
        return src
        
        
    def export(self):
        
        path = self.mainWindow.config["workspace"]+"/"+self.project.name+"/java/src/main/java/"+self.project.name.replace(" ", "")
        
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path+"/"+self.classname()+".java", "w")
        
        f.write(self.generateSrc())
        
        f.close()
        
        self.mainWindow.console.write("BaseMod: Successfully exported to "+path+"/"+self.name+".java")
        
        
        
        
class Constructor(QtGui.QDialog):
    
    def __init__(self, mainWindow, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.initUI(mainWindow)
        
        
    def initUI(self, mainWindow):
        self.ui = uic.loadUi(BASEPATH+"/ui/BaseMod_Constructor.ui", self)
        
        self.name.setText(mainWindow.translations.getTranslation("name"))
        self.modid.setText(mainWindow.translations.getTranslation("modid"))
        self.version.setText(mainWindow.translations.getTranslation("version"))
    
    
    def params(self):
        """returns a tuple of all parameters that were given"""
        name = str(self.nameInput.text())
        modid = str(self.modidInput.text())
        version = str(self.versionInput.text())
        
        return (name, modid, version)
    
    
    @staticmethod
    def getParams(mainWindow, parent=None):
        """returns a tuple of all parameters. the first element in the tuple is a boolean if the dialog was accepted"""
        dialog = Constructor(mainWindow, parent)
        if not dialog.exec_() == QtGui.QDialog.Accepted:
            return None
            
        return dialog.params()
        
        


def init(mainWindow):
    
    return