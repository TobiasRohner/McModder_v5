# -*- coding: utf-8 -*-
from PyQt4 import QtGui





class Console(QtGui.QDockWidget):
    
    def __init__(self, mainWindow):
        QtGui.QDockWidget.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.initUI()
        
        
    def initUI(self):
        
        self.textEdit = QtGui.QPlainTextEdit()
        self.textEdit.setReadOnly(True)
        
        self.setWidget(self.textEdit)
        
        self.setWindowTitle(self.mainWindow.translations.getTranslation("console"))
        
        
    def write(self, text):
        
        self.textEdit.appendPlainText(text)
        QtGui.qApp.processEvents()
        
        
    def clear(self):
        
        self.textEdit.clear()