# -*- coding: utf-8 -*-
import abc
import os
import pickle
from PyQt4 import QtGui





class _base(QtGui.QWidget):
    
    def __init__(self, mainWindow, identifier, classtype):
        QtGui.QWidget.__init__(self)
        
        self.identifier = identifier
        self.classtype = classtype
        
        self.mainWindow = mainWindow
        self.project = mainWindow.currentProject()
        
        self.name = "unknown"
        
        self.data = {}
        
        
    @abc.abstractmethod
    def initUI(self):
        
        return
        
        
    def generateIcon(self):
        
        return
        
        
    def save(self):
        
        return


    def load(self, path):
        
        f = open(path, "r")
        
        data = pickle.load(f)
        for key in data.keys():
            value = data[key]
            if isinstance(value, u"".__class__) or isinstance(value, str):
                value = '"'+value+'"'
            exec("self."+key+"="+str(value))
        
        f.close()
        
        
    @abc.abstractmethod
    def renewWidgetEntrys(self):
        
        return
        
    
    @abc.abstractmethod
    def pull(self, cls):
        
        return {}
        
        
    @abc.abstractmethod
    def completeModData(self):
        
        return
        
        
    def instancename(self):
        
        return self.name.replace(" ", "_")+"_Instance"
        
        
    def classname(self):
        
        return self.name.replace(" ", "_")
        
        
    def unlocalizedName(self):
        
        return self.classname()
        
        
    def package(self):
        
        return self.project.name.replace(" ", "_")+"."+self.identifier
        
        
    @abc.abstractmethod
    def generateSrc(self):
        
        return
        
        
    @abc.abstractmethod
    def export(self):
        
        return