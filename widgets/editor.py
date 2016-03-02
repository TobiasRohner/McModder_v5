# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore




class Editor(QtGui.QDockWidget):
    """
    Editor, in which each instance of classes._base gets its own tab to display its GUI.
    """
    
    def __init__(self, mainWindow):
        """
        Editor(Main.MainWindow)
        
        Args:
            mainWindow (Main.MainWindow):       Pointer to the main window
        """
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
        """
        Editor.openTab(classes._base)
        
        Open the instance of classes._base in a new tab in the Editor.
        
        Args:
            obj (classes._base):    Object to be opened in the Editor
        """
        
        obj.renewWidgetEntrys()
        
        if self.tabWidget.indexOf(obj) != -1:
            self.tabWidget.setCurrentWidget(obj)
        
        else:
            self.tabWidget.addTab(obj, obj.name)
            
            
    def closeTab(self, i):
        """
        Editor.closeTab(int)
        
        Close the tab at the specific index.
        
        Args:
            i (int):    Index of the tab to close
        """
        
        self.tabWidget.removeTab(i)
        
        
    def renameTab(self, obj, name):
        """
        Editor.renameTab(classes._base, str)
        
        Rename the tab of a specific object.
        Only gets called by Main.MainWindow.updateName(classes._base, str)
        
        Args:
            obj (classes._base):    Object whose tab should be renamed
            name (str):             New name of the tab
        """
        
        tab = self.tabWidget.indexOf(obj)
        if tab != -1:
            self.tabWidget.setTabText(tab, name)