# -*- coding: utf-8 -*-
import os
import sys
import json
from PyQt4 import QtGui, QtCore

BASEPATH = os.path.dirname(sys.argv[0])

ITEMS = []




class ItemList(QtGui.QListWidget):
    """
    List of all Items in the Game. This includes Vanilla and Modded Items.
    """
    
    def __init__(self, mainWindow):
        """
        ItemList(Main.MainWindow)
        
        Args:
            mainWindow (Main.MainWindow):   Pointer to the main window
        """
        QtGui.QListWidget.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.standardItems = []
        
        self.initMCItems()
        for item in self.standardItems:
            self.addItem(item)
        self.reloadItems()
        
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDropIndicatorShown(True)
        
        self.connect(self.mainWindow, QtCore.SIGNAL("UPDATE_ITEMLIST"), self.reloadItems)
        
        
    def initMCItems(self):
        """
        Load all Vanilla Minecraft Items from the icons.json file and add them to the List.
        """
        
        f = open(BASEPATH+"/assets/icons.json")
        data = json.load(f)
        f.close()
        for name in data.keys():
            texPath = BASEPATH+"/assets/textures/icons/"+data[name]["texture"]
            if data[name]["type"] == "Item":
                self.standardItems.append(ListWidgetItem(name, "Vanilla", "Items."+data[name]["name"], "net.minecraft.init.Items", texPath))
            elif data[name]["type"] == "Block":
                self.standardItems.append(ListWidgetItem(name, "Vanilla", "Blocks."+data[name]["name"], "net.minecraft.init.Blocks", texPath))
    
    
    def reloadItems(self):
        """
        Reload all Modded Items.
        """
        
        if "Item" in self.mainWindow.project.objects.keys():
            for item in self.mainWindow.project.objects["Item"]:
                i = self.findItems(item.name, QtCore.Qt.MatchExactly)
                if len(i) == 0:
                    self.addItem(item.getListWidgetItem())
            itemnames = [it.name for it in self.mainWindow.project.objects["Item"]]+[self.item(it).text() for it in range(self.count())]
            for i in range(self.count()):
                if not self.item(i).text() in itemnames:
                    self.removeItemWidget(self.item(i))
        self.sortItems()
        
        
    def startDrag(self, supportedActions):
        
        selectedItem = self.selectedItems()[0]
        
        drag = QtGui.QDrag(self)
        
        mimeData = QtCore.QMimeData()
        mimeData.setText(selectedItem.text()+";"+selectedItem.identifier+";1")
        
        pixmap = selectedItem.texture.scaled(50, 50)
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QtGui.QColor(0,0,0,127))
        painter.end()
        
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        
        drag.exec_(QtCore.Qt.MoveAction)
        
        
    def getItem(self, name, identifier):
        """
        ItemList.getItem(str, str) -> ListWidgetItem
        
        Get a pointer to the ListWidgetItem representing the specified Item.
        
        Args:
            name (str):         Name of the Item
            identifier (str):   The Identifier String (Vanilla, Item or Block)
            
        Returns:
            ListWidgetItem:     Pointer to the ListWidgetItem of the specified Item
        """
        
        for item in self.findItems(name, QtCore.Qt.MatchExactly):
            if item.identifier == identifier:
                return item
        
        
        
        
class ListWidgetItem(QtGui.QListWidgetItem):
    """
    QtGui.QListWidgetItem representation of an Item or Block in the Game.
    """
    
    def __init__(self, name, identifier, instancename, package, texturepath=BASEPATH+"/assets/textures/icons/unknown.png"):
        """
        ListWidgetItem(str, str, str, str, str)
        
        Args:
            name (str):             The Items name
            identifier (str):       Identifier of the Item (Vanilla, Item, Block)
            instancename (str):     Name of the Instance inside the Java source
            package (str):          Java package
            texturepath (str):      Path to the Items texture (default=BASEPATH+"/assets/textures/icons/unknown.png")
        """
        QtGui.QListWidgetItem.__init__(self)
        
        if not os.path.exists(texturepath):
            texturepath = BASEPATH+"/assets/textures/icons/unknown.png"
        
        self.setText(name)
        self.identifier = identifier
        self.instancename = instancename
        self.package = package
        self.texture = QtGui.QPixmap(texturepath)
        self.iconObj = QtGui.QIcon(self.texture)
        self.setIcon(self.iconObj)
        
        
    def updateIcon(self, path):
        """
        ListWidgetItem.updateIcon(str)
        
        Args:
            path (str):     Path to the new texture
        """
        
        self.texture = QtGui.QPixmap(path)
        self.iconObj = QtGui.QIcon(self.texture)
        self.setIcon(self.iconObj)
        
        
    def save(self):
        
        return {"identifier":self.identifier, "name":self.text()}