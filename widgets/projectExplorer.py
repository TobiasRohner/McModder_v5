# -*- coding: utf-8 -*-
import os
import sys
import json
from PyQt4 import QtGui, QtCore



BASEPATH = os.path.dirname(sys.argv[0])





class ProjectExplorer(QtGui.QDockWidget):
    """
    Project Explorer to list all the objects in the current project.
    Doubles as container for those objects.
    """
    
    def __init__(self, mainWindow, name):
        """
        ProjectExplorer(Main.MainWindow, str)
        
        Args:
            mainWindow (Main.MainWindow):   Pointer to the main window
            name (str):                     Name of the project
        """
        QtGui.QDockWidget.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.name = name
        
        self.unsavedChanges = False
        
        self.objects = {}
        
        self.initUI()
        
        
    def initUI(self):
        
        self.treeWidget = QtGui.QTreeWidget()
        self.setWidget(self.treeWidget)
        
        self.connect(self.treeWidget, QtCore.SIGNAL('itemDoubleClicked (QTreeWidgetItem*,int)'), self.selectItem)
        
        self.setWindowTitle(self.mainWindow.translations.getTranslation("projectExplorer"))
        
        
    def load(self, path):
        """
        ProjectExplorer.load(str)
        
        Load a project from disk.
        
        Args:
            path (str):     Filepath to the moddata.json file
        """
        
        f = open(path)
        data = json.load(f)
        f.close()
        
        self.name = path.replace("\\", "/").split("/")[-2]
        
        for key in data.keys():
            objData = data[key]
            cls = None
            exec("cls = self.getModule('"+objData["classtype"]+"')."+objData["classtype"]+"(self.mainWindow, objData['name'])")
            cls.load(objData)
            self.addObject(cls)
            
            
    def getModule(self, name):
        """
        ProjectExplorer.getModule(str) -> module
        
        Return the Module with the given name.
        Used to access addons.
        
        Args:
            name (str):     Name of the module to return
        
        Returns:
            module:         Python Module object of the addon
        """
        
        for mod in self.mainWindow.addons:
            if mod[0] == name:
                return mod[2]
                
                
    def addObject(self, obj):
        """
        ProjectExplorer.addObject(classes._base)
        
        Add an instance of classes._base to the project.
        
        Args:
            obj (classes._base):    The object to be added
        """
        
        if not obj.identifier in self.objects.keys():
            self.objects[obj.identifier] = []
            
        self.objects[obj.identifier].append(obj)
        
        obj.project = self
        
        ident = self.treeWidget.findItems(obj.identifier, QtCore.Qt.MatchExactly)
        if len(ident) == 0:
            identItem = QtGui.QTreeWidgetItem()
            identItem.setText(0, obj.identifier)
            self.treeWidget.addTopLevelItem(identItem)
        else:
            identItem = ident[0]
        subItem = QtGui.QTreeWidgetItem()
        subItem.setText(0, obj.name)
        identItem.addChild(subItem)
        
        self.treeWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        
        
    def removeObject(self, obj):
        """
        ProjectExplorer.removeObject(classes._base)
        
        Remove/Delete the given object.
        
        Args:
            obj (classes._base):    Object to be removed
        """
        
        identItem = self.treeWidget.findItems(obj.identifier, QtCore.Qt.MatchExactly)[0]
        for i in range(identItem.childCount()):
            if identItem.child(i).text(0) == obj.name:
                identItem.removeChild(identItem.child(i))
                break
        self.treeWidget.sortItems(0, QtCore.Qt.AscendingOrder)
        
        self.objects[obj.identifier].remove(obj)
        if len(self.objects[obj.identifier]) == 0:
            self.objects.pop(obj.identifier, None)
            self.treeWidget.removeItemWidget(self.treeWidget.findItems(obj.identifier, QtCore.Qt.MatchExactly))
        
        
    def selectedObject(self):
        """
        ProjectExplorer.selectedObject() -> classes._base
        
        Get the currently selected object.
        
        Returns:
            classes._base:  Currently selected object
        """
        
        items = self.treeWidget.selectedItems()
        if len(items) > 0:
            item = items[0]
            if item.parent() and not item.parent().parent():
                ident = item.parent().text(0)
                for obj in self.objects[ident]:
                    if obj.name == item.text(0):
                        return obj
        return None
        
        
    def selectItem(self, item):
        
        #low level item
        cls = None
        if item.parent() and not item.parent().parent():
            name = item.text(0)
            identifier = str(item.parent().text(0))
            for c in self.objects[identifier]:
                if c.name == name:
                    cls = c
                    
            self.mainWindow.editor.openTab(cls)
        
        
    def renameObject(self, obj, name):
        """
        ProjectExplorer.renameObject(classes._base, str)
        
        Rename the list entry of a specific object.
        Only gets called by Main.MainWindow.updateName(classes._base, str)
        
        Args:
            obj (classes._base):    Object whose list entry should be renamed
            name (str):             New name of the list entry
        """
        
        items = [i for i in self.treeWidget.findItems(obj.name, QtCore.Qt.MatchRecursive) if i.parent() and not i.parent().parent()]
        for i in items:
            if i.parent().text(0) == obj.identifier:
                i.setText(0, name)
                
                
    def save(self):
        """
        ProjectExplorer.save() -> dict
        
        Return the project data to be saved to disk.
        
        Returns:
            dict:   Data to store
        """
        
        data = {}
        for key in self.objects.keys():
            for obj in self.objects[key]:
                data[obj.name] = obj.save()
        return data