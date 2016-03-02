# -*- coding: utf-8 -*-
import abc
import os
import pickle
from widgets import menus
from PyQt4 import QtGui





class _base(QtGui.QWidget):
    """
    This class acts as a parent to all Mod objects.
    """
    
    def __init__(self, mainWindow, identifier, classtype):
        """
        _base(Main.MainWindow, str, str)
        
        Args:
            mainWindow (Main.MainWindow):       Pointer to the main window
            identifier (str):                   Identiifer (Tab) under which this object should be listen in the project explorer
            classtype (str):                    Name of the inheriting class
        """
        QtGui.QWidget.__init__(self)
        
        self.identifier = identifier
        self.classtype = classtype
        self.deleteable = True
        
        self.mainWindow = mainWindow
        
        self.name = "unknown"
        
        self.data = {}
        
        self.listWidgetItem = menus.ListWidgetItem(self.name, self.identifier, self.instancename(), self.package())
        
        
    def postInit(self, project):
        
        return
        
        
    @abc.abstractmethod
    def initUI(self):
        
        return
        
        
    def generateIcon(self):
        
        return
        
        
    def save(self):
        
        return


    def load(self, data):
        """
        _base.load(dict)
        
        Load the data from a Python dictionary
        
        Args:
            data (dict):    The saved data as a dictionary
        """
        
        for key in data.keys():
            value = data[key]
            if isinstance(value, u"".__class__) or isinstance(value, str):
                value = '"'+value+'"'
            exec("self."+key+"="+str(value))
            
        self.updateListWidgetItem()
        
        
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
        
        return self.mainWindow.project.name.replace(" ", "_")+"."+self.identifier
        
        
    @abc.abstractmethod
    def generateSrc(self):
        
        return
        
        
    @abc.abstractmethod
    def export(self):
        
        return
        
        
    def getListWidgetItem(self):
        
        return self.listWidgetItem
        
        
    def updateListWidgetItem(self):
        
        return