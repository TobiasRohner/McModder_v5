# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).replace("\\", "/").split("/")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import imp
from PyQt4 import QtGui, QtCore




class GUIWidget(QtGui.QWidget):
    
    def __init__(self, master, texturepath):
        QtGui.QWidget.__init__(self)
        
        self.master = master
        
        self.texture = QtGui.QPixmap(texturepath)
        
        self.pos = QtCore.QPoint()
        
        self.slots = []
        
        self.dragItem = None
        
        self.setAcceptDrops(True)
                      
                      
    def imageCornersInWidgetCoordinates(self):
        
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
        
        c, s = self.imageCornersInWidgetCoordinates()
        
        xpos = c[0] + x*s[0]/self.texture.width()
        ypos = c[1] + y*s[1]/self.texture.height()
        
        return xpos, ypos
        
        
    def widget2imageCoords(self, x, y):
        
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
        
        imgCoords = self.widget2imageCoords(x, y)
        for i in range(len(self.slots)):
            if self.slots[i].x>=imgCoords[0]-16 and self.slots[i].y>=imgCoords[1]-16 and self.slots[i].x<=imgCoords[0] and self.slots[i].y<=imgCoords[1]:
                return i
        return -1
        
        
    def drawOverlayIcon(self, painter):
        
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
        
        return self.master.itemList.findItems(name, QtCore.Qt.MatchExactly)[0]
        
        
    def dragEnterEvent(self, event):
        
        event.accept()
        data = event.mimeData().text()
        name, identifier = data.split(";")
        self.dragItem = self.itemFromInformation(identifier, name)
        
        
    def dragLeaveEvent(self, event):
        
        self.dragItem = None
        
        
    def dragMoveEvent(self, event):
        
        self.pos = event.pos()
        self.repaint()
        
        
    def dropEvent(self, event):
        
        data = event.mimeData().text()
        name, identifier = data.split(";")
        
        slotIdx = self.inSlot(self.pos.x(), self.pos.y())
        if slotIdx != -1:
            self.slots[slotIdx].item = self.itemFromInformation(identifier, name)
        
        self.dragItem = None
        
        self.repaint()
        
        
        
        
        
class Slot():
    
    def __init__(self, master, x, y):
        
        self.master = master
        
        self.x = x
        self.y = y
        
        self.item = None
        
        
    def draw(self, painter):
        
        self.drawIcon(painter)
    
    
    def drawIcon(self, painter):
        
        if self.item != None:
            c, s = self.master.imageCornersInWidgetCoordinates()
            x, y = self.master.image2widgetCoords(self.x, self.y)
            painter.drawPixmap(x, y, 16*s[0]/self.master.texture.width(), 16*s[1]/self.master.texture.height(), self.item.texture)