# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui, uic



BASEPATH = os.path.dirname(sys.argv[0])





class Project():
    
    def __init__(self, mainWindow, name):
        
        self.mainWindow = mainWindow
        
        self.name = name
        
        self.objects = {}
        
        
    def load(self, data):
        
        for ident in os.listdir(self.mainWindow.config["workspace"]+"/"+self.name+"/mod"):
            self.objects[ident] = []
            for c in os.listdir(self.mainWindow.config["workspace"]+"/"+self.name+"/mod/"+ident):
                name, t = c.split(".")
                if t == "mod":
                    if ident != "BaseMod":
                        exec("cls = self.getModule('"+ident+"')."+ident+"(self.mainWindow, name)")
                    else:
                        cls = self.mainWindow.baseModClass.BaseMod(self.mainWindow, self.name, name)
                    cls.project = self
                    cls.load(self.mainWindow.config["workspace"]+"/"+self.name+"/mod/"+ident+"/"+name+".mod")
                    self.objects[ident].append(cls)
                    
                    
    def getModule(self, name):
        
        for mod in self.mainWindow.addons:
            if mod[0] == name:
                return mod[2]
    
    
    def addObject(self, obj):
        
        if not obj.identifier in self.objects.keys():
            self.objects[obj.identifier] = []
            
        self.objects[obj.identifier].append(obj)
        
        obj.project = self
        
        
    def save(self):
        
        data = {}
        for key in self.objects.keys():
            for obj in self.objects[key]:
                data[obj.name] = obj.save()
        return data
        
        
        
        
class Constructor(QtGui.QDialog):
    
    def __init__(self, mainWindow, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.initUI(mainWindow)
        
        
    def initUI(self, mainWindow):
        self.ui = uic.loadUi(BASEPATH+"/ui/Project_Constructor.ui", self)
        
        self.name.setText(mainWindow.translations.getTranslation("name"))
    
    
    def params(self):
        """returns a tuple of all parameters that were given"""
        name = str(self.nameInput.text())
        
        return (name,)
    
    
    @staticmethod
    def getParams(mainWindow, parent=None):
        """returns a tuple of all parameters. the first element in the tuple is a boolean if the dialog was accepted"""
        dialog = Constructor(mainWindow, parent)
        if not dialog.exec_() == QtGui.QDialog.Accepted:
            return None
            
        return dialog.params()