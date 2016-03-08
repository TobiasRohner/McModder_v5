# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from utils import threading





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
        
        
        
        
        
def streamToConsole(console, process):
    """
    streamToConsole(Console, stdout.Popen)
    
    Stream the text output of the specified process to a Console object.
    
    Args
    ----
    console (Console):          The console for the process's output to be streamed to
    process (stdout.Popen):     Process, which output should be streamed to the console
    """
    
    t = threading.Thread()
    
    def task():
        for line in iter(process.stdout.readline, ''):
            t.emit(QtCore.SIGNAL("WRITE_TO_CONSOLE"), line.replace("\n", "").replace("\r", ""))
#            console.write(line.replace("\n", "").replace("\r", ""))
    
    console.connect(t, QtCore.SIGNAL("WRITE_TO_CONSOLE"), console.write)
    t.setTask(task)
    t.start()