# -*- coding: utf-8 -*-
import os
import sys
import pickle
from PyQt4 import QtGui, QtCore



BASEPATH = os.path.dirname(sys.argv[0])





class ProjectExplorer(QtGui.QDockWidget):
    
    def __init__(self, mainWindow):
        QtGui.QDockWidget.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.projects = []
        
        self.initUI()
        
        
    def initUI(self):
        
        self.treeWidget = QtGui.QTreeWidget()
        self.setWidget(self.treeWidget)
        
        self.connect(self.treeWidget, QtCore.SIGNAL('itemDoubleClicked (QTreeWidgetItem*,int)'), self.selectItem)
        
        self.setWindowTitle(self.mainWindow.translations.getTranslation("projectExplorer"))
        
        
    def updateWorkspace(self):
        
        #list all projects out of the folders
        for proj in self.mainWindow.projects:
            exists = False
            p = None
            for project in self.projects:
                if project.name == proj.name:
                    exists = True
                    p = project
                    break
            if exists:
                p.updateProject()
            else:
                p = Project(self.mainWindow, proj.name)
                self.projects.append(p)
                p.updateProject()
                    
        #self.treeWidget.clear()
        self.treeWidget.addTopLevelItems(self.projects)
        
        
    def selectedProject(self):
        
        items = self.treeWidget.selectedItems()
        if len(items) > 0:
            item = items[0]
            while not isinstance(item, Project):
                item = item.parent()
        
            return item.text(0)
            
        return None
        
        
    def selectItem(self, item):
        
        #low level item
        cls = None
        if item.parent() and item.parent().parent() and not item.parent().parent().parent():
            name = item.text(0)
            identifier = item.parent().text(0)
            classes = self.mainWindow.currentProject().objects[identifier]
            for c in classes:
                if c.name == name:
                    cls = c
                    
            self.mainWindow.editor.openTab(cls)
        
        
    def renameObject(self, obj, name):
        
        items = [i for i in self.treeWidget.findItems(obj.name, QtCore.Qt.MatchRecursive) if i.parent() and i.parent().parent() and not i.parent().parent().parent()]
        for i in items:
            if i.parent().text(0) == obj.identifier:
                i.setText(0, name)
                
                
                
                
                
class Project(QtGui.QTreeWidgetItem):
    
    def __init__(self, mainWindow, name):
        QtGui.QTreeWidgetItem.__init__(self)
        
        self.mainWindow = mainWindow
        self.name = name
        
        self.icon = QtGui.QIcon(BASEPATH+"/assets/icons/mod.png")
        
        self.setText(0, self.name)
        self.setIcon(0, self.icon)
        
        
    def updateProject(self):
        
        data = self.mainWindow.getProject(self.name).save()
        for name in data.keys():
            ident = data[name]["identifier"]
            exists = False
            for c in range(self.childCount()):
                if self.child(c).text(0) == ident:
                    exists = True
                    subItem = self.child(c)
            if not exists:
                subItem = QtGui.QTreeWidgetItem()
                subItem.setText(0, ident)
                self.addChild(subItem)
                
            exists = False
            for c in range(subItem.childCount()):
                if subItem.child(c).text(0) == name:
                    exists = True
                    subsubItem = subItem.child(c)
            if not exists:
                subsubItem = QtGui.QTreeWidgetItem()
                subsubItem.setText(0, name)
                subItem.addChild(subsubItem)