# -*- coding: utf-8 -*-
from pprint import pprint




class History():
    
    def __init__(self, maxDepth):
        
        self.maxDepth = maxDepth
        
        self.hist = []
        
        self.index = -1
        
        
    def addStep(self, cmdRedo, argsRedo, cmdUndo, argsUndo):
        
        if self.index < self.maxDepth:
            self.index += 1
        self.hist = self.hist[:self.index]
        self.hist.append([[cmdRedo, argsRedo], [cmdUndo, argsUndo]])
        print("Added new Step to History:")
        pprint([[cmdRedo, argsRedo], [cmdUndo, argsUndo]])
        
        
    def undo(self):
        
        if self.index > -1:
            self.hist[self.index][1][0](*self.hist[self.index][1][1])
            self.index -= 1
        
        
    def redo(self):
        
        if self.index < len(self.hist):
            self.hist[self.index][0][0](*self.hist[self.index][0][1])
            self.index += 1