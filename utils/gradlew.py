# -*- coding: utf-8 -*-
import os
import sys
import urllib2
import zipfile
import subprocess
import shutil

from widgets import console as c

from PyQt4 import QtGui


BASEPATH = os.path.dirname(sys.argv[0])
FORGE_URL = "http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.8-11.14.3.1502/forge-1.8-11.14.3.1502-src.zip"
BLOCK_SIZE = 8192

if BASEPATH[-5:] == "utils":
    BASEPATH = BASEPATH[:-6]





def installForge(installationPath, console):
    """
    installForge(str, widgets.console.Console)
    
    Install Forge to the specified path.
    Stream the console output to the specified console.
    
    Args
    ----
    installationPath (str):             Path to the installation folder of Forge
    console (widgets.console.Console):  Console to stream the output to
    """
    
    #download forge
    zipPath = str(_downloadForge(installationPath))
    
    #extract forge to the selected path
    forgeZip = zipfile.ZipFile(zipPath, "r")
    forgeZip.extractall(str(installationPath))
    forgeZip.close()
    #delete the forge zip file
    os.remove(zipPath)
    
    #setup the environment (Eclipse)
    _setupEnvironment(str(installationPath), console)
    
    #delete the example mod
    _deleteExampleCode(str(installationPath))
    
    


def runClient(projectPath, console):
    """
    runClient(str, widgets.console.Console)
    
    Run the Minecraft Client with the Forge Mod installed.
    
    Args
    ----
    projectPath (str):                  Path to the root folder of Forge
    console (widgets.console.Console):  Console to stream the output to
    """

    os.chdir(projectPath)
    process = subprocess.Popen('"'+projectPath+'/gradlew" runClient', stdout=subprocess.PIPE, shell=True)
    c.streamToConsole(console, process)
        
        


def exportMod(projectPath, console):
    """
    exportMod(str, widgets.console.Console)
    
    Export the Mod as a .jar.
    
    Args
    ----
    projectPath (str):                  Path to the root folder of Forge
    console (widgets.console.Console):  Console to stream the output to
    """
    
    path = projectPath+"/java"
    
    os.chdir(path)
    process = subprocess.Popen('"'+path+'/gradlew" build', stdout=subprocess.PIPE, shell=True)
    c.streamToConsole(console, process)




def _downloadForge(path):
    """
    _downloadForge(str)
    
    Download Forge from FORGE_URL
    """
    
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
    """
    _setupEnvironment(str, widgets.console.Console)
    """

    #setup the environment
    os.chdir(path)
    process = subprocess.Popen('"'+path+'/gradlew" setupDecompWorkspace eclipse', stdout=subprocess.PIPE, shell=True)
    c.streamToConsole(console, process)
    
    
    
def _deleteExampleCode(path):
    """
    _deleteExampleCode(str)
    """
    
    shutil.rmtree(path+"/src/main/java/com")
    os.remove(path+"/src/main/resources/mcmod.info")






if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    installForge()
    
    sys.exit(app.exec_())