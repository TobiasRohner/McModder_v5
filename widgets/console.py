# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from utils import threading
from utils import Decorators as dec





class Console(QtGui.QDockWidget):
    
    def __init__(self, mainWindow):
        """
        Console(Main.MainWindow)
        
        Args
        ----
        mainWindow (Main.MainWindow):   Pointer to the main window
        """
        QtGui.QDockWidget.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.initUI()
        
        
    def initUI(self):
        
        self.textEdit = QtGui.QPlainTextEdit()
        self.textEdit.setReadOnly(True)
        
        self.textEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        
        self.setWidget(self.textEdit)
        
        self.setWindowTitle(self.mainWindow.translations.getTranslation("console"))
        
        
    @dec.accepts((str, unicode))
    def write(self, text):
        """
        Console.write(str)
        
        Output some text to the console.
        
        Args
        ----
        text (str):     Text to be written in the console
        """
        
        print(text)
        self.textEdit.appendPlainText(text)
        
        
    def clear(self):
        """
        Clear the console.
        """
        
        self.textEdit.clear()
        
        
    @dec.accepts(file)
    def streamToConsole(self, stdout):
        """
        Console.streamToConsole(file)
        
        Stream the text output of the specified process to this Console object.
        
        Args
        ----
        process (file):     Process, which output should be streamed to the console
        """
        
        t = threading.Thread()
        
        def task():
            for line in iter(stdout.readline, ''):
                t.emit(QtCore.SIGNAL("WRITE_TO_CONSOLE"), line.replace("\n", "").replace("\r", ""))
    #            console.write(line.replace("\n", "").replace("\r", ""))
        
        self.connect(t, QtCore.SIGNAL("WRITE_TO_CONSOLE"), self.write)
        t.setTask(task)
        t.start()