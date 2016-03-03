# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).replace("\\", "/").split("/")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import imp
from PyQt4 import QtGui, QtCore




class GUIWidget(QtGui.QWidget):
    """
    Class for the graphical representation of a Minecraft GUI
    """
    
    def __init__(self, master, texturepath):
        """
        GUIWidget(classes._base, str)
        
        Args:
            master (classes._base):     Class, which contains an instance of GUIWidget
            texturepath (str):          Path to the GUI texture
        """
        QtGui.QWidget.__init__(self)
        
        self.master = master
        
        self.texture = QtGui.QPixmap(texturepath)
        
        self.pos = QtCore.QPoint()
        
        self.slots = []
        
        self.dragItem = None
        
        self.lastClick = [False, QtCore.QPoint(), -1]
        
        self.setAcceptDrops(True)
                      
                      
    def imageCornersInWidgetCoordinates(self):
        """
        GUIWidget.imageCornersInWidgetCoordinates() -> list[list[int], list[int]]
        
        Return the position of the top left corner of the GUI texture and its width and height in the QtGui.QWidget's coordinate system.
        
        Returns:
            list[list[int], list[int]]:     [[Corner X, Corner Y], [Width, Height]]
        """
        
        width = self.texture.width()
        height = self.texture.height()
        aspect = float(width)/height
        
        if float(self.width())/self.height() > aspect:
            h = self.height()
            w = int(aspect*h)
            xc = int(float(self.width()-w)/2)
            yc = 0
        else:
            w = self.width()
            h = int(float(w)/aspect)
            xc = 0
            yc = int(float(self.height()-h)/2)
            
        return [[xc,yc], [w,h]]
        
        
    def image2widgetCoords(self, x, y):
        """
        GUIWidget.image2widgetCoords(int, int) -> (int, int)
        
        Convert image to QtGui.QWidget coordinates (Coordinates in Pixels)
        
        Args:
            x (int):        X Coordinate of a pixel in the image
            y (int):        Y Coordinate of a pixel in the image
            
        Returns:
            (int, int):     Coordinates of the given pixel in QtGui.QWidget coordinates
        """
        
        c, s = self.imageCornersInWidgetCoordinates()
        
        xpos = c[0] + x*s[0]/self.texture.width()
        ypos = c[1] + y*s[1]/self.texture.height()
        
        return xpos, ypos
        
        
    def widget2imageCoords(self, x, y):
        """
        GUIWidget.widget2imageCoords(int, int) -> (int, int)
        
        Convert QtGui.QWidget to image coordinates (Coordinates in Pixels)
        
        Args:
            x (int):        X Coordinate of a pixel in the QtGui.QWidget
            y (int):        Y Coordinate of a pixel in the QtGui.QWidget
            
        Returns:
            (int, int):     Coordinates of the given pixel in image coordinates
        """
        
        c, s = self.imageCornersInWidgetCoordinates()
        
        xpos = (x-c[0])*self.texture.width()/s[0]
        ypos = (y-c[1])*self.texture.width()/s[1]
        
        return xpos, ypos
        
        
    def paintEvent(self, event):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawTexture(qp)
        self.drawSlots(qp)
        self.drawOverlayIcon(qp)
        qp.end()
        
        
    def drawTexture(self, painter):
        
        c, s = self.imageCornersInWidgetCoordinates()
        painter.drawPixmap(c[0], c[1], s[0], s[1], self.texture)
        
        
    def inSlot(self, x, y):
        """
        GUIWidget.inSlot(int, int) -> int
        
        Return the index of the Slot the coordinate is in.
        If it's not over any Slot, return -1.
        
        Args:
            x (int):    QtGui.QWidget x coordinate in pixels
            y (int):    QtGui.QWidget y coordinate in pixels
            
        Returns:
            int:        Index of the Slot lying under the given pixel
        """
        
        imgCoords = self.widget2imageCoords(x, y)
        for i in range(len(self.slots)):
            if self.slots[i].x>=imgCoords[0]-16 and self.slots[i].y>=imgCoords[1]-16 and self.slots[i].x<=imgCoords[0] and self.slots[i].y<=imgCoords[1]:
                return i
        return -1
        
        
    def drawOverlayIcon(self, painter):
        """
        GUIWidget.drawOverlayIcon(QtGui.QPainter)
        
        Draw a transparent in a Slot, over which a drag object hovers.
        
        Args:
            painter (QtGui.QPainter):   The QtGui.QPainter instance
        """
        
        if self.dragItem != None:
            slotIdx = self.inSlot(self.pos.x(), self.pos.y())
            if slotIdx != -1:
                slot = self.slots[slotIdx]
                painter.setOpacity(0.5)
                c, s = self.imageCornersInWidgetCoordinates()
                x, y = self.image2widgetCoords(slot.x, slot.y)
                painter.drawPixmap(x, y, 16*s[0]/self.texture.width(), 16*s[1]/self.texture.height(), self.dragItem.texture)
                painter.setOpacity(1)
                
                
    def drawSlots(self, painter):
        
        for slot in self.slots:
            slot.draw(painter)
            
            
    def itemFromInformation(self, identifier, name):
        """
        GUIWidget.itemFromInformation(str, str) -> ListWidgetItem
        
        Return a pointer to the ListWidgetItem instance of an ItemList corresponding to the given information.
        
        Args:
            identifier (str):   Identifier of the item (Vanilla, Item, Block)
            name (str):         Name of the item
            
        Returns:
            ListWidgetItem:     Pointer to the ListWidgetItem instance corresponding to the given information
        """
        
        return self.master.itemList.getItem(name, identifier)
        
        
    def mousePressEvent(self, event):
        
        slotIdx = self.inSlot(event.pos().x(), event.pos().y())
        
        self.lastClick[0] = True
        self.lastClick[1] = event.pos()
        self.lastClick[2] = slotIdx
        
        
    def mouseReleaseEvent(self, event):
        
        self.lastClick[0] = False
                
                
    def mouseMoveEvent(self, event):
        
        if self.lastClick[0]:
            if (self.lastClick[1].x()-event.pos().x())**2+(self.lastClick[1].y()-event.pos().y())**2 > 5:
                if self.lastClick[2] != -1:
                    
                    selectedSlot = self.slots[self.lastClick[2]]
                    selectedItem = selectedSlot.item
                    
                    if selectedItem != None:
                        
                        drag = QtGui.QDrag(self)
                        
                        mimeData = QtCore.QMimeData()
                        mimeData.setText(selectedItem.text()+";"+selectedItem.identifier+";"+str(selectedSlot.count))
                        
                        pixmap = selectedItem.texture.scaled(50, 50)
                        painter = QtGui.QPainter(pixmap)
                        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
                        painter.fillRect(pixmap.rect(), QtGui.QColor(0,0,0,127))
                        painter.end()
                        
                        drag.setMimeData(mimeData)
                        drag.setPixmap(pixmap)
                        
                        self.slots[self.lastClick[2]].item = None
                        self.slots[self.lastClick[2]].count = 0
                        
                        drag.exec_(QtCore.Qt.MoveAction)
            
            
    def mouseDoubleClickEvent(self, event):
        
        slotIdx = self.inSlot(event.pos().x(), event.pos().y())
        
        if slotIdx != -1:
            count, ok = QtGui.QInputDialog.getInt(self, "Count", "Number:", value=self.slots[slotIdx].count, min=1, max=64)
            if ok:
                if self.slots[slotIdx].stackable:
                    self.slots[slotIdx].count = count
        
        
    def dragEnterEvent(self, event):
        
        event.accept()
        data = event.mimeData().text()
        name, identifier, count = data.split(";")
        self.dragItem = self.itemFromInformation(identifier, name)
        self.master.updateRecipe(self.slots)
        
        
    def dragLeaveEvent(self, event):
        
        self.dragItem = None
        
        
    def dragMoveEvent(self, event):
        
        self.pos = event.pos()
        self.repaint()
        
        
    def dropEvent(self, event):
        
        data = event.mimeData().text()
        name, identifier, count = data.split(";")
        
        slotIdx = self.inSlot(self.pos.x(), self.pos.y())
        if slotIdx != -1:
            self.slots[slotIdx].setItem(self.itemFromInformation(identifier, name), int(count))
            self.master.updateRecipe(self.slots)
        
        self.dragItem = None
        
        self.repaint()
        
        
    def resetSlots(self):
        
        for slot in self.slots:
            slot.item = None
            slot.count = 0
        self.repaint()
        
        
        
        
        
class Slot():
    """
    Container to store an ItemStack
    """
    
    def __init__(self, master, x, y, stackable=False):
        """
        Slot(GUIWidget, int, int, bool)
        
        Args:
            master (GUIWidget):     GUIWidget instance, to which this Slot belongs to
            x (int):                X position of the Slot in image pixels
            y (int):                Y position of the Slot in image pixels
            stackable (bool):       If items could be stacked inside this Slot (default=False)
        """
        
        self.master = master
        
        self.x = x
        self.y = y
        
        self.stackable = stackable
        
        self.item = None
        
        self.count = 0
        
        self.font = QtGui.QPixmap(BASEPATH+"/assets/textures/font/ascii.png")
        self.numberSize = (5,7)
        self.numbers = [(0 ,24),
                        (8 ,24),
                        (16,24),
                        (24,24),
                        (32,24),
                        (40,24),
                        (48,24),
                        (56,24),
                        (64,24),
                        (72,24)]
        
        
    def setItem(self, item, count=1):
        """
        Slot.setItem(ListWidgetItem, int)
        
        Add the specified number of items to the Slot.
        
        Args:
            item (ListWidgetItem):  Item to be added
            count (int):            Number of items to be added (default=1)
        """
        
        if self.stackable:
            if item == self.item:
                self.count += count
            else:
                self.item = item
                self.count = count
        else:
            self.item = item
            self.count = 1
        
        
    def draw(self, painter):
        
        self.drawIcon(painter)
        self.drawCount(painter)
    
    
    def drawIcon(self, painter):
        
        if self.item != None:
            c, s = self.master.imageCornersInWidgetCoordinates()
            x, y = self.master.image2widgetCoords(self.x, self.y)
            painter.drawPixmap(x, y, 16*s[0]/self.master.texture.width(), 16*s[1]/self.master.texture.height(), self.item.texture)
            
            
    def drawCount(self, painter):
        
        if self.count > 1:
            c, s = self.master.imageCornersInWidgetCoordinates()
            numbers = list(str(self.count))
            numbers.reverse()
            numbers = map(lambda n: int(n), numbers)
            xpos = self.numberSize[0]
            for n in numbers:
                x, y = self.master.image2widgetCoords(self.x+16-xpos, self.y+16-self.numberSize[1])
                painter.drawPixmap(x, y, self.numberSize[0]*s[0]/self.master.texture.width(), self.numberSize[1]*s[1]/self.master.texture.height(),
                                   self.font,
                                   self.numbers[n][0], self.numbers[n][1], self.numberSize[0], self.numberSize[1])
                xpos += self.numberSize[0]
                
                
    def getItemStack(self):
        """
        Slot.getItemStack() -> str
        
        Return the Java code for the Minecraft item stack inside this Slot.
        
        Returns:
            str:    Java source code of the Minecraft item stack inside this Slot
        """
        
        return "new ItemStack("+self.item.instancename+", "+str(self.count)+")"
        
        
        
        
        
class ItemStack():
    """
    Container for a specific number of items
    """
    
    def __init__(self, master, item, count=1):
        """
        ItemStack(object, ListWidgetItem, int)
        
        Args:
            master (object):        The object the ItemStack instance belongs to (mostly Recipes)
            item (ListWidgetItem):  Item stored in this ItemStack
            count (int):            Number of items stored
        """
        
        self.item = item
        self.count = count
        
        self.master = master
        
        
    def save(self):
        
        data = {}
        
        data["count"] = self.count
        data["item"] = None
        if self.item != None:
            data["item"] = self.item.save()
        
        return data
        
        
    def load(self, data):
        
        self.count = data["count"]
        if data["item"] != None:
            self.item = self.master.master.itemList.getItem(data["item"]["name"], data["item"]["identifier"])
            
            
    def getItemStack(self):
        
        return "new ItemStack("+self.item.instancename+", "+str(self.count)+")"