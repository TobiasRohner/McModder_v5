# -*- coding: utf-8 -*-
from PyQt4 import QtGui





class Console(QtGui.QDockWidget):
    
    def __init__(self, mainWindow):
        """
        Console(Main.MainWindow)
        
        Args:
            mainWindow (Main.MainWindow):   Pointer to the main window
        """
        QtGui.QDockWidget.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.initUI()
        
        
    def initUI(self):
        
        self.textEdit = QtGui.QPlainTextEdit()
        self.textEdit.setReadOnly(True)
        
        self.setWidget(self.textEdit)
        
        self.setWindowTitle(self.mainWindow.translations.getTranslation("console"))
        
        
    def write(self, text):
        """
        Console.write(str)
        
        Output some text to the console.
        
        Args:
            text (str):     Text to be written in the console
        """
        
        self.textEdit.appendPlainText(text)
        QtGui.qApp.processEvents()
        
        
    def clear(self):
        """
        Clear the console.
        """
        
        self.textEdit.clear()