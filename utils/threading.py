# -*- coding: utf-8 -*-
from PyQt4 import QtCore




class Thread(QtCore.QThread):
    
    def __init__(self):
        """
        Thread(task, *args)
        """
        QtCore.QThread.__init__(self)
        
        def noTaskDef():
            print("Thread "+str(self.currentThreadId())+" has no function to run!")
        self.task = noTaskDef
        self.args = ()
        
        
    def __del__(self):
        
        self.wait()
        
        
    def setTask(self, task, *args):
        """
        Thread.setTask(function, *object)
        
        Args
        ----
        task (function):    Function to run when Thread.start() is called
        *args (object):     Arguments for the function
        """
        
        self.task = task
        self.args = args
        
        
    def run(self):
        """
        Run the predefined function in a second thread
        """
        
        self.task(*self.args)