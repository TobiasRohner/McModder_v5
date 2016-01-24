# -*- coding: utf-8 -*-
import os
import sys
import urllib2
import zipfile
import subprocess
import shutil

from PyQt4 import QtGui


BASEPATH = os.path.dirname(sys.argv[0])
FORGE_URL = "http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.8-11.14.3.1502/forge-1.8-11.14.3.1502-src.zip"
BLOCK_SIZE = 8192

if BASEPATH[-5:] == "utils":
    BASEPATH = BASEPATH[:-6]





def installForge(installationPath, console):
    
    #download forge
    zipPath = _downloadForge(installationPath)
    
    #extract forge to the selected path
    forgeZip = zipfile.ZipFile(zipPath, "r")
    forgeZip.extractall(installationPath)
    forgeZip.close()
    #delete the forge zip file
    os.remove(zipPath)
    
    #setup the environment (Eclipse)
    _setupEnvironment(installationPath, console)
    
    #delete the example mod
    _deleteExampleCode(installationPath)
    
    


def runClient(projectPath, console):
    
    path = projectPath+"/java"
    
    os.chdir(path)
    process = subprocess.Popen('"'+path+'/gradlew" runClient', stdout=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        console.write(line.replace("\n", "").replace("\r", ""))
        QtGui.qApp.processEvents()
        
        


def exportMod(projectPath, console):
    
    path = projectPath+"/java"
    
    os.chdir(path)
    process = subprocess.Popen('"'+path+'/gradlew" build', stdout=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        console.write(line.replace("\n", "").replace("\r", ""))
        QtGui.qApp.processEvents()




def _downloadForge(path):
    
    zipPath = path+"/"+FORGE_URL.split("/")[-1]
    f = open(zipPath, "wb")
    
    u = urllib2.urlopen(FORGE_URL)
    meta = u.info()
    fileSize = int(meta.getheaders("Content-Length")[0])
    
    progressDialog = QtGui.QProgressDialog("Downloading Forge", "Cancel", 0, fileSize)
    
    #Download forge to BASEPATH/temp
    downloaded = 0
    while True:
        block = u.read(BLOCK_SIZE)
        if not block:
            break
        
        downloaded += len(block)
        f.write(block)
        
        progressDialog.setValue(downloaded)
        progressDialog.show()
        
    return zipPath
    
    
    
def _setupEnvironment(path, console):

    #setup the environment
    os.chdir(path)
    process = subprocess.Popen('"'+path+'/gradlew" setupDecompWorkspace eclipse', stdout=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        console.write(line.replace("\n", "").replace("\r", ""))
        QtGui.qApp.processEvents()
    
    
    
def _deleteExampleCode(path):
    
    shutil.rmtree(path+"/src/main/java/com")
    os.remove(path+"/src/main/resources/mcmod.info")






if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    installForge()
    
    sys.exit(app.exec_())