# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import sys
import os
import time
import shutil

import Main



VERSION = Main.VERSION
BASEPATH = os.path.dirname(sys.argv[0])



def findData(path):
    data = {"\\".join(str(path).split("\\")[6:]):[]}
    
    for e in os.listdir(path):
        if os.path.isfile(path+"\\"+e):
            data["\\".join(str(path).split("\\")[6:])].append(path+"\\"+e)
        else:
            data.update(findData(path+"\\"+e))
            
    return data
    
    
def transformData(data):
    dataList = []
    
    for d in data:
        dataList.append(tuple([d, data[d]]))
        
    return dataList



starttime = time.time()


sys.argv.append("py2exe")


imageformatFiles = transformData(findData(r"C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats"))
uiFiles = transformData(findData(BASEPATH+r"\ui"))
assetFiles = transformData(findData(BASEPATH+r"\assets"))
addonFiles = transformData(findData(BASEPATH+r"\addons"))
docFiles = transformData(findData(BASEPATH+r"\doc\html"))


setup(windows=[{"script":"Main.py"}],

      options={"py2exe":{"includes":["sip",
                                     "PyQt4.QtGui",
                                     "PyQt4.QtCore",
                                     "PyQt4.uic",
                                     "sys",
                                     "os",
                                     "zipfile",
                                     "subprocess",
                                     "PIL",
                                     "pickle",
                                     "json",
                                     "imp",
                                     "shutil",
                                     "PyQt4.QtOpenGL",
                                     "math",
                                     "copy",
                                     "logging"],
                         "packages":["classes",
                                     "utils",
                                     "widgets",
                                     "OpenGL.GL",
                                     "OpenGL.GL.shaders",
                                     "OpenGL.GLU",
                                     "OpenGL_accelerate"],
                         "excludes":[],
                         "dll_excludes": ["MSVCP90.dll",
                                          "MSWSOCK.dll",
                                          "mswsock.dll",
                                          "powrprof.dll"],
                         "bundle_files":1,
                         "compressed":False,
                         "optimize":2,
                         "dist_dir":"builds/"+VERSION}},
                         
      zipfile=None,
               
      data_files=imageformatFiles)

shutil.copytree(BASEPATH+r"\ui", "builds/"+VERSION+"/ui")
shutil.copytree(BASEPATH+r"\assets", "builds/"+VERSION+"/assets")
shutil.copytree(BASEPATH+r"\addons", "builds/"+VERSION+"/addons")
shutil.copytree(BASEPATH+r"\doc\html", "builds/"+VERSION+"/doc")

os.makedirs("builds/"+VERSION+"/Projects")
      
      
shutil.rmtree(BASEPATH+"/build")
      
endtime = time.time()

print("\n\n*** Done in %s seconds ***"%str(endtime-starttime))