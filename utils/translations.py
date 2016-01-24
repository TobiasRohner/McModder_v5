# -*- coding: utf-8 -*-
import os
import sys


BASEPATH = os.path.dirname(sys.argv[0])





class Translations():
    
    def __init__(self, lang):
        
        self.lang = lang
        self.translations = {}
        
        self.loadLanguage()
        
        
    def loadLanguage(self):
        
        f = open(BASEPATH+"/lang/"+self.lang+".lang")
        
        lines = f.readlines()
        for line in lines:
            key, value = line.split("=")
            self.translations[key] = value.replace("\n", "")
            
        f.close()
        
        f = open(BASEPATH+"/lang/English.lang")
        
        lines = f.readlines()
        for line in lines:
            key, value = line.split("=")
            if not key in self.translations.keys():
                self.translations[key] = value.replace("\n", "")
            
        f.close()
        
        
    def getTranslation(self, key):
        
        return self.translations[key]