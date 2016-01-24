# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore




class Editor(QtGui.QDockWidget):
    
    def __init__(self, mainWindow):
        QtGui.QDockWidget.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.initUI()
        
        
    def initUI(self):
        
        self.tabWidget = QtGui.QTabWidget()
        self.setWidget(self.tabWidget)
        
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        
        self.connect(self.tabWidget, QtCore.SIGNAL("tabCloseRequested(int)"), self.closeTab)
        
        self.setWindowTitle(self.mainWindow.translations.getTranslation("editor"))
        
        
    def openTab(self, obj):
        
        obj.renewWidgetEntrys()
        
        if self.tabWidget.indexOf(obj) != -1:
            self.tabWidget.setCurrentWidget(obj)
        
        else:
            self.tabWidget.addTab(obj, obj.name)
            
            
    def closeTab(self, i):
        
        self.tabWidget.removeTab(i)
        
        
    def renameTab(self, obj, name):
        
        tab = self.tabWidget.indexOf(obj)
        if tab != -1:
            self.tabWidget.setTabText(tab, name)