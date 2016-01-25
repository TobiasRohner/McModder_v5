# -*- coding: utf-8 -*-
import os
import sys
from classes import objects
from PyQt4 import QtGui, uic



BASEPATH = os.path.dirname(sys.argv[0])





class Project():
    
    def __init__(self, mainWindow, name):
        
        from classes import objects
        
        self.mainWindow = mainWindow
        
        self.name = name
        
        self.objects = {}
        
        
    def load(self):
        
        for ident in os.listdir(self.mainWindow.config["workspace"]+"/"+self.name+"/mod"):
            self.objects[ident] = []
            for c in os.listdir(self.mainWindow.config["workspace"]+"/"+self.name+"/mod/"+ident):
                name, t = c.split(".")
                if t == "mod":
                    if ident != "BaseMod":
                        exec("cls = objects."+ident+"."+ident+"(self.mainWindow, name)")
                    else:
                        cls = objects.BaseMod.BaseMod(self.mainWindow, self.name, name)
                    cls.project = self
                    cls.load(self.mainWindow.config["workspace"]+"/"+self.name+"/mod/"+ident+"/"+name+".mod")
                    self.objects[ident].append(cls)
    
    
    def addObject(self, obj):
        
        if not obj.identifier in self.objects.keys():
            self.objects[obj.identifier] = []
            
        self.objects[obj.identifier].append(obj)
        
        obj.project = self
        
        obj.save()
        
        
        
        
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