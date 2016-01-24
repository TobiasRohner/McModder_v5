# -*- coding: utf-8 -*-
import os
import sys
import compileall





BASEPATH = os.path.dirname(sys.argv[0])



def loadClasses():
    
    initClass = open(BASEPATH+"/classes/objects/__init__.py", "w")
    
    libraryContent = os.listdir(BASEPATH+"/classes/objects")
    for c in libraryContent:
        name, ending = c.split(".")
        if name != "__init__" and ending == "py":
            initClass.write("from . import "+name+"\n")
            
    initClass.close()
    
    compileall.compile_file(BASEPATH+"/classes/objects/__init__.py")