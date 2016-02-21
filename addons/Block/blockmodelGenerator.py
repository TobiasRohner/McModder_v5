# -*- coding: utf-8 -*-
import os
import sys

ADDONPATH = "/".join(os.path.realpath(__file__).split("\\")[:-1])
BASEPATH = os.path.dirname(sys.argv[0])

import math
import copy
from utils import mathUtils as mu
from PyQt4 import QtGui, QtCore, QtOpenGL, uic
from PIL import Image
from OpenGL import GL, GLU
from OpenGL.GL import shaders




class BlockModelGenerator(QtGui.QMainWindow):
    
    def __init__(self, mainWindow, master):
        QtGui.QMainWindow.__init__(self)
        
        self.mainWindow = mainWindow
        self.master = master
        
        self.textures = []
        
        self.lastTexturePath = mainWindow.config["workspace"]
        
        self.initUI()
        
        self.show()
        
        self.loadData(self.master.modeldata[0])
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(ADDONPATH+"/BlockModelCreator.ui", self)
        
        self.GLWidget = ModelGLWidget(self)
        
        self.mainLayout.insertWidget(1, self.GLWidget, 1)
        
        self.uvEditorDown = UVEditor(self, BASEPATH+"/assets/textures/blocks/unknown.png")
        self.uvEditorUp = UVEditor(self, BASEPATH+"/assets/textures/blocks/unknown.png")
        self.uvEditorNorth = UVEditor(self, BASEPATH+"/assets/textures/blocks/unknown.png")
        self.uvEditorSouth = UVEditor(self, BASEPATH+"/assets/textures/blocks/unknown.png")
        self.uvEditorWest = UVEditor(self, BASEPATH+"/assets/textures/blocks/unknown.png")
        self.uvEditorEast = UVEditor(self, BASEPATH+"/assets/textures/blocks/unknown.png")
        
        self.textureDownLayout.layout().insertWidget(0, self.uvEditorDown, 1)
        self.textureUpLayout.layout().insertWidget(0, self.uvEditorUp, 1)
        self.textureNorthLayout.layout().insertWidget(0, self.uvEditorNorth, 1)
        self.textureSouthLayout.layout().insertWidget(0, self.uvEditorSouth, 1)
        self.textureWestLayout.layout().insertWidget(0, self.uvEditorWest, 1)
        self.textureEastLayout.layout().insertWidget(0, self.uvEditorEast, 1)
        
        self.scrollArea.setMinimumWidth(200)
        
        self.connect(self.dimensionsX, QtCore.SIGNAL("valueChanged(double)"), self.setDimensionX)
        self.connect(self.dimensionsY, QtCore.SIGNAL("valueChanged(double)"), self.setDimensionY)
        self.connect(self.dimensionsZ, QtCore.SIGNAL("valueChanged(double)"), self.setDimensionZ)
        self.connect(self.translationX, QtCore.SIGNAL("valueChanged(double)"), self.setTranslationX)
        self.connect(self.translationY, QtCore.SIGNAL("valueChanged(double)"), self.setTranslationY)
        self.connect(self.translationZ, QtCore.SIGNAL("valueChanged(double)"), self.setTranslationZ)
        self.connect(self.rotation, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.setRotation)
        self.connect(self.rotationAxisComboBox, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.setRotationAxis)
        self.connect(self.rotationCenterX, QtCore.SIGNAL("valueChanged(double)"), self.setRotationCenterX)
        self.connect(self.rotationCenterY, QtCore.SIGNAL("valueChanged(double)"), self.setRotationCenterY)
        self.connect(self.rotationCenterZ, QtCore.SIGNAL("valueChanged(double)"), self.setRotationCenterZ)
        self.connect(self.cuboidList, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.cuboidSelected)
        self.connect(self.cuboidList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.cuboidSelected)
        self.connect(self.addCuboidButton, QtCore.SIGNAL("clicked()"), self.addCuboid)
        self.connect(self.removeCuboidButton, QtCore.SIGNAL("clicked()"), self.removeCuboid)
        self.connect(self.cloneCuboidButton, QtCore.SIGNAL("clicked()"), self.cloneCuboid)
        self.connect(self.changeDownTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureDown)
        self.connect(self.changeUpTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureUp)
        self.connect(self.changeNorthTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureNorth)
        self.connect(self.changeSouthTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureSouth)
        self.connect(self.changeWestTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureWest)
        self.connect(self.changeEastTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureEast)
        self.connect(self.uvEditorDown, QtCore.SIGNAL("UPDATE_UVS"), self.updateUVsDown)
        self.connect(self.uvEditorUp, QtCore.SIGNAL("UPDATE_UVS"), self.updateUVsUp)
        self.connect(self.uvEditorNorth, QtCore.SIGNAL("UPDATE_UVS"), self.updateUVsNorth)
        self.connect(self.uvEditorSouth, QtCore.SIGNAL("UPDATE_UVS"), self.updateUVsSouth)
        self.connect(self.uvEditorWest, QtCore.SIGNAL("UPDATE_UVS"), self.updateUVsWest)
        self.connect(self.uvEditorEast, QtCore.SIGNAL("UPDATE_UVS"), self.updateUVsEast)
        self.connect(self.cuboidList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.changeCuboidName)
            
            
    def cuboidSelected(self, cuboid):
        
        self.dimensionsX.setValue(cuboid.dimensions[1])
        self.dimensionsY.setValue(cuboid.dimensions[2])
        self.dimensionsZ.setValue(cuboid.dimensions[0])
        self.translationX.setValue(cuboid.translation[1])
        self.translationY.setValue(cuboid.translation[2])
        self.translationZ.setValue(cuboid.translation[0])
        idx = 2
        if cuboid.rotation == -45:
            idx = 0
        elif cuboid.rotation == -22.5:
            idx = 1
        elif cuboid.rotation == 22.5:
            idx = 3
        elif cuboid.rotation == 45:
            idx = 4
        self.rotation.setCurrentIndex(idx)
        self.rotationAxisComboBox.setCurrentIndex(cuboid.rotationAxis)
        self.rotationCenterX.setValue(cuboid.rotationCenter[1])
        self.rotationCenterY.setValue(cuboid.rotationCenter[2])
        self.rotationCenterZ.setValue(cuboid.rotationCenter[0])
        self.uvEditorDown.loadTexture(cuboid.textures[0][0])
        self.uvEditorUp.loadTexture(cuboid.textures[1][0])
        self.uvEditorNorth.loadTexture(cuboid.textures[2][0])
        self.uvEditorSouth.loadTexture(cuboid.textures[3][0])
        self.uvEditorWest.loadTexture(cuboid.textures[4][0])
        self.uvEditorEast.loadTexture(cuboid.textures[5][0])
        self.uvEditorDown.updateUVs(copy.deepcopy(cuboid.uvs[0]))
        self.uvEditorUp.updateUVs(copy.deepcopy(cuboid.uvs[1]))
        self.uvEditorNorth.updateUVs(copy.deepcopy(cuboid.uvs[2]))
        self.uvEditorSouth.updateUVs(copy.deepcopy(cuboid.uvs[3]))
        self.uvEditorWest.updateUVs(copy.deepcopy(cuboid.uvs[4]))
        self.uvEditorEast.updateUVs(copy.deepcopy(cuboid.uvs[5]))
        cuboid.setTexture(0, cuboid.textures[0][0])
        cuboid.setTexture(1, cuboid.textures[1][0])
        cuboid.setTexture(2, cuboid.textures[2][0])
        cuboid.setTexture(3, cuboid.textures[3][0])
        cuboid.setTexture(4, cuboid.textures[4][0])
        cuboid.setTexture(5, cuboid.textures[5][0])
        self.GLWidget.updateGL()
        
        
    def updateUVsDown(self, uvs):
        
        self.selectedCuboid().uvs[0] = copy.deepcopy(uvs)
        self.GLWidget.updateGL()
        self.save()
        
        
    def updateUVsUp(self, uvs):
        
        self.selectedCuboid().uvs[1] = copy.deepcopy(uvs)
        self.GLWidget.updateGL()
        self.save()
        
        
    def updateUVsNorth(self, uvs):
        
        self.selectedCuboid().uvs[2] = copy.deepcopy(uvs)
        self.GLWidget.updateGL()
        self.save()
        
        
    def updateUVsSouth(self, uvs):
        
        self.selectedCuboid().uvs[3] = copy.deepcopy(uvs)
        self.GLWidget.updateGL()
        self.save()
        
        
    def updateUVsWest(self, uvs):
        
        self.selectedCuboid().uvs[4] = copy.deepcopy(uvs)
        self.GLWidget.updateGL()
        self.save()
        
        
    def updateUVsEast(self, uvs):
        
        self.selectedCuboid().uvs[5] = copy.deepcopy(uvs)
        self.GLWidget.updateGL()
        self.save()
        
        
    def setDimensionX(self, dim):
        
        self.selectedCuboid().dimensions[1] = dim
        self.selectedCuboid().updateScalingMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setDimensionY(self, dim):
        
        self.selectedCuboid().dimensions[2] = dim
        self.selectedCuboid().updateScalingMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setDimensionZ(self, dim):
        
        self.selectedCuboid().dimensions[0] = dim
        self.selectedCuboid().updateScalingMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setTranslationX(self, trans):
        
        self.selectedCuboid().translation[1] = trans
        self.selectedCuboid().updateTranslationMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setTranslationY(self, trans):
        
        self.selectedCuboid().translation[2] = trans
        self.selectedCuboid().updateTranslationMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setTranslationZ(self, trans):
        
        self.selectedCuboid().translation[0] = trans
        self.selectedCuboid().updateTranslationMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setRotationAxis(self, axis):
        
        self.selectedCuboid().rotationAxis = self.rotationAxisComboBox.findText(axis)
        self.selectedCuboid().updateRotationMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setRotation(self, rot):
        
        self.selectedCuboid().rotation = float(rot)
        self.selectedCuboid().updateRotationMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setRotationCenterX(self, pos):
        
        self.selectedCuboid().rotationCenter[1] = pos
        self.selectedCuboid().updateRotationMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setRotationCenterY(self, pos):
        
        self.selectedCuboid().rotationCenter[2] = pos
        self.selectedCuboid().updateRotationMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def setRotationCenterZ(self, pos):
        
        self.selectedCuboid().rotationCenter[0] = pos
        self.selectedCuboid().updateRotationMatrix()
        self.GLWidget.updateGL()
        self.save()
        
        
    def changeTextureDown(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.lastTexturePath,
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().setTexture(0, tex)
            self.uvEditorDown.loadTexture(tex)
            self.lastTexturePath = "/".join(tex.split("/")[:-1])
            self.GLWidget.updateGL()
            self.save()
            
            
    def changeTextureUp(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.lastTexturePath,
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().setTexture(1, tex)
            self.uvEditorUp.loadTexture(tex)
            self.lastTexturePath = "/".join(tex.split("/")[:-1])
            self.GLWidget.updateGL()
            self.save()
            
            
    def changeTextureNorth(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.lastTexturePath,
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().setTexture(2, tex)
            self.uvEditorNorth.loadTexture(tex)
            self.lastTexturePath = "/".join(tex.split("/")[:-1])
            self.GLWidget.updateGL()
            self.save()
            
            
    def changeTextureSouth(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.lastTexturePath,
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().setTexture(3, tex)
            self.uvEditorSouth.loadTexture(tex)
            self.lastTexturePath = "/".join(tex.split("/")[:-1])
            self.GLWidget.updateGL()
            self.save()
            
            
    def changeTextureWest(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.lastTexturePath,
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().setTexture(4, tex)
            self.uvEditorWest.loadTexture(tex)
            self.lastTexturePath = "/".join(tex.split("/")[:-1])
            self.GLWidget.updateGL()
            self.save()
            
            
    def changeTextureEast(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.lastTexturePath,
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().setTexture(5, tex)
            self.uvEditorEast.loadTexture(tex)
            self.lastTexturePath = "/".join(tex.split("/")[:-1])
            self.GLWidget.updateGL()
            self.save()
            
            
    def changeCuboidName(self, cuboid):
        
        dialog = QtGui.QInputDialog()
        dialog.setTextValue(cuboid.name)
        txt, ok = dialog.getText(self, "Change Name", "Name:")
        
        if ok:
            cuboid.setName(str(txt))
            self.save()
            
            
    def selectedCuboid(self):
        
        return self.cuboidList.currentItem()
        
        
    def addCuboid(self):
        
        cub = Cuboid("unnamed", [1.0, 1.0, 1.0], self)
        cub.loadShader("cuboid")
        self.cuboidList.addItem(cub)
        self.cuboidList.setCurrentItem(cub)
        self.cuboidSelected(cub)
        self.GLWidget.updateGL()
        self.save()
        
        
    def cloneCuboid(self):
        
        sel = self.selectedCuboid()
        cub = Cuboid(sel.name+"_copy", copy.deepcopy(sel.dimensions), self)
        cub.uvs = copy.deepcopy(sel.uvs)
        cub.translation = copy.deepcopy(sel.translation)
        cub.rotation = sel.rotation
        cub.rotationAxis = sel.rotationAxis
        cub.rotationCenter = copy.deepcopy(sel.rotationCenter)
        cub.updateRotationMatrix()
        cub.updateScalingMatrix()
        cub.updateTranslationMatrix()
        cub.loadShader("cuboid")
        cub.setTexture(0, sel.textures[0][0])
        cub.setTexture(1, sel.textures[1][0])
        cub.setTexture(2, sel.textures[2][0])
        cub.setTexture(3, sel.textures[3][0])
        cub.setTexture(4, sel.textures[4][0])
        cub.setTexture(5, sel.textures[5][0])
        self.cuboidList.addItem(cub)
        self.cuboidSelected(cub)
        self.GLWidget.updateGL()
        self.save()
        
        
    def removeCuboid(self):
        
        self.cuboidList.takeItem(self.cuboidList.currentRow())
        self.GLWidget.updateGL()
        self.save()
        
        
    def addTexture(self, path):
        
        if not path in self.textures:
            self.textures.append(path)
        return self.textures.index(path)
        
        
    def save(self):
        
        self.master.modeldata = [self.savedata(), self.getJSON(), self.textures]
        self.master.save()
        
        
    def cuboids(self):
        
        return [self.cuboidList.item(i) for i in range(self.cuboidList.count())]
        
        
    def dict2JSON(self, obj):
        
        if isinstance(obj, dict):
            s = []
            for key in obj.keys():
                s.append('\t"'+str(key)+'": '+self.dict2JSON(obj[key]).replace("\n", "\n\t"))
            
            return "{\n"+",\n".join(s)+"\n}"
            
        if isinstance(obj, list):
            if not sum([1 if isinstance(e, dict) or isinstance(e, list) else 0 for e in obj]):
                
                return str(obj).replace("'", '"')
                
            else:
                s = []
                for e in obj:
                    s.append("\t"+self.dict2JSON(e).replace("\n", "\n\t"))
                    
                return "[\n"+",\n".join(s)+"\n]"
            
        if isinstance(obj, str):
            return '"'+obj+'"'
            
        if isinstance(obj, bool):
            return "True" if obj else "False"
            
        if obj == None:
            return "Null"
            
        else:
            return str(obj)
        
        
    def getJSON(self):
        
        self.textures = []
        model = {}
        
        model["elements"] = []
        for cub in self.cuboids():
            model["elements"].append(cub.getDictRepr())
            
        model["textures"] = {}
        for i in range(len(self.textures)):
            model["textures"]["texture"+str(i)] = "<modid>:blocks/<unlocalizedName>_"+str(i)
            
        return self.dict2JSON(model)
        
        
    def savedata(self):
        
        return {"cuboids":[cub.savedata() for cub in self.cuboids()]}
        
        
    def loadData(self, data):
        
        for cubData in data["cuboids"]:
            cub = Cuboid(cubData["name"], cubData["dimensions"], self)
            cub.loadData(cubData)
            cub.loadShader("cuboid")
            self.cuboidList.addItem(cub)

        self.GLWidget.updateGL()
        
        
        
        
class ModelGLWidget(QtOpenGL.QGLWidget):
    
    xRotationChanged = QtCore.pyqtSignal(int)
    yRotationChanged = QtCore.pyqtSignal(int)
    zRotationChanged = QtCore.pyqtSignal(int)
    
    def __init__(self, modelGenerator):
        QtOpenGL.QGLWidget.__init__(self)
        
        self.modelGenerator = modelGenerator
        
        self.setMinimumSize(100, 100)
        
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.zoom = -50.0
        
        self.center = [8.0, 8.0, 8.0]

        self.lastPos = QtCore.QPoint()

        self.backgroundColor = QtGui.QColor.fromCmykF(0.0, 0.0, 0.0, 0.0)


    def setXRotation(self, angle):
        
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.updateGL()
            

    def setYRotation(self, angle):
        
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.updateGL()
            

    def setZRotation(self, angle):
        
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.updateGL()
            

    def initializeGL(self):
        
        self.qglClearColor(self.backgroundColor)
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        
        for cub in self.modelGenerator.cuboids():
            cub.loadShader("cuboid")
            

    def paintGL(self):
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, self.zoom)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glTranslated(-self.center[0], -self.center[1], -self.center[2])
        
        self.drawGrid()
        self.drawCoordinateSystem()
        for cub in self.modelGenerator.cuboids():
            cub.draw()


    def resizeGL(self, width, height):

        GL.glViewport(0, 0, width, height)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(90.0, float(self.width())/self.height(), 1.0, 100.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        
        
    def drawGrid(self):
        
        GL.glBegin(GL.GL_LINES)
        GL.glColor(0.75, 0.75, 0.75)
        for x in range(17):
            GL.glVertex3f(x,  0.0, 0.0)
            GL.glVertex3f(x, 16.0, 0.0)
        for y in range(17):
            GL.glVertex3f( 0.0, y, 0.0)
            GL.glVertex3f(16.0, y, 0.0)
        GL.glEnd()
        
        
    def drawCoordinateSystem(self):
        
        GL.glBegin(GL.GL_LINES)
        GL.glColor(0.0, 0.0, 1.0)
        GL.glVertex3f(-4.0, 0.0, 0.0)
        GL.glVertex3f(32.0, 0.0, 0.0)
        GL.glColor(1.0, 0.0, 0.0)
        GL.glVertex3f(0.0, -4.0, 0.0)
        GL.glVertex3f(0.0, 32.0, 0.0)
        GL.glColor(0.0, 1.0, 0.0)
        GL.glVertex3f(0.0, 0.0, -4.0)
        GL.glVertex3f(0.0, 0.0, 32.0)
        GL.glEnd()
        
        

    def mousePressEvent(self, event):
        
        self.lastPos = event.pos()
        

    def mouseMoveEvent(self, event):
        
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        
        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()
        
        
    def wheelEvent(self, event):
        
        self.zoom += float(event.delta())/240
        self.updateGL()


    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle
        
        
        
        
class UVEditor(QtGui.QWidget):
    
    def __init__(self, modelGenerator, texture):
        QtGui.QWidget.__init__(self)
        
        self.modelGenerator = modelGenerator
        
        self.texture = None
        self.uvs = [[0.0,0.0], [0.0,0.0]]
        
        self.selectedCorners = [False, False, False, False]
        self.moved = [[0.0, 0.0], [0.0, 0.0]]
        self.lastPos = QtCore.QPoint()
        
        self.loadTexture(texture)
        
        self.initUI()
        
        
    def initUI(self):
        
        self.setMinimumSize(100, 100)
        
        
    def loadTexture(self, path):
        
        self.texture = QtGui.QPixmap(path)
        self.repaint()
        
        
    def updateUVs(self, uvs):
        
        self.uvs = uvs
        self.repaint()
        
        
    def paintEvent(self, event):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawTexture(qp)
        self.drawUVs(qp)
        qp.end()
        
        
    def mousePressEvent(self, event):
        
        self.lastPos = event.pos()
        
        imgCoords = self.widget2ImageCoords([event.pos().x(), event.pos().y()])
        uvSize = [self.uvs[1][0]-self.uvs[0][0], self.uvs[1][1]-self.uvs[0][1]]
        
        if imgCoords[1] > self.uvs[0][1]-uvSize[1]/10 and imgCoords[1] < self.uvs[0][1]+uvSize[1]/10:
            self.selectedCorners[0] = True
        if imgCoords[0] > self.uvs[1][0]-uvSize[0]/10 and imgCoords[0] < self.uvs[1][0]+uvSize[0]/10:
            self.selectedCorners[1] = True
        if imgCoords[1] > self.uvs[1][1]-uvSize[1]/10 and imgCoords[1] < self.uvs[1][1]+uvSize[1]/10:
            self.selectedCorners[2] = True
        if imgCoords[0] > self.uvs[0][0]-uvSize[0]/10 and imgCoords[0] < self.uvs[0][0]+uvSize[0]/10:
            self.selectedCorners[3] = True
        if (imgCoords[0] > self.uvs[0][0]+uvSize[0]/10 and imgCoords[0] < self.uvs[1][0]-uvSize[0]/10
        and imgCoords[1] > self.uvs[0][1]+uvSize[1]/10 and imgCoords[1] < self.uvs[1][1]-uvSize[1]/10):
            self.selectedCorners[0] = True
            self.selectedCorners[1] = True
            self.selectedCorners[2] = True
            self.selectedCorners[3] = True
    
    
    def mouseReleaseEvent(self, event):
        
        self.uvs = [[self.crop(self.uvs[0][0]+self.moved[0][0], 0.0, 1.0), self.crop(self.uvs[0][1]+self.moved[0][1], 0.0, 1.0)],
                    [self.crop(self.uvs[1][0]+self.moved[1][0], 0.0, 1.0), self.crop(self.uvs[1][1]+self.moved[1][1], 0.0, 1.0)]]
        
        self.selectedCorners = [False, False, False, False]
        self.moved = [[0.0, 0.0], [0.0, 0.0]]
        
        
    def mouseMoveEvent(self, event):
        
        if event.buttons() & QtCore.Qt.LeftButton:
            
            textureWidth = self.texture.size().width()
            textureHeight = self.texture.size().height()
            aspect = float(textureWidth) / textureHeight
            
            if aspect < float(self.width()) / self.height():
                xSize = int(aspect * self.height())
                ySize = self.height()
            else:
                xSize = self.width()
                ySize = xSize/aspect
            dx = event.x() - self.lastPos.x()
            dy = event.y() - self.lastPos.y()
            for corner in range(4):
                if self.selectedCorners[corner]:
                    if corner == 0:
                        self.moved[0][1] = round(float(dy)/ySize*textureHeight)/textureHeight
                    if corner == 1:
                        self.moved[1][0] = round(float(dx)/xSize*textureWidth)/textureWidth
                    if corner == 2:
                        self.moved[1][1] = round(float(dy)/ySize*textureHeight)/textureHeight
                    if corner == 3:
                        self.moved[0][0] = round(float(dx)/xSize*textureWidth)/textureWidth
                    self.emit(QtCore.SIGNAL("UPDATE_UVS"),
                              [[self.crop(self.uvs[0][0]+self.moved[0][0], 0.0, 1.0), self.crop(self.uvs[0][1]+self.moved[0][1], 0.0, 1.0)],
                               [self.crop(self.uvs[1][0]+self.moved[1][0], 0.0, 1.0), self.crop(self.uvs[1][1]+self.moved[1][1], 0.0, 1.0)]])
            self.repaint()
            
            
    def crop(self, value, minV, maxV):
        
        return min(max(value, minV), maxV)
        
        
    def drawTexture(self, painter):
        
        left = self.image2WidgetCoords((0, 0))
        right = self.image2WidgetCoords((1, 1))
        painter.drawPixmap(left[0],
                           left[1],
                           right[0]-left[0],
                           right[1]-left[1],
                           self.texture)
        
        
    def drawUVs(self, painter):
        
        left = self.image2WidgetCoords((self.crop(self.uvs[0][0]+self.moved[0][0], 0.0, 1.0), self.crop(self.uvs[0][1]+self.moved[0][1], 0.0, 1.0)))
        right = self.image2WidgetCoords((self.crop(self.uvs[1][0]+self.moved[1][0], 0.0, 1.0), self.crop(self.uvs[1][1]+self.moved[1][1], 0.0, 1.0)))
            
        painter.fillRect(left[0],
                         left[1],
                         right[0]-left[0],
                         right[1]-left[1],
                         QtGui.QColor(255, 255, 255, 127))
        painter.brush().setColor(QtGui.QColor(255, 255, 255, 200))
        painter.drawRect(left[0],
                         left[1],
                         right[0]-left[0],
                         right[1]-left[1])
                         
                         
    def image2WidgetCoords(self, point):
        
        textureWidth = self.texture.size().width()
        textureHeight = self.texture.size().height()
        aspect = float(textureWidth) / textureHeight
        
        if aspect < float(self.width()) / self.height():
            xSize = int(aspect * self.height())
            ySize = self.height()
            xCorner = (self.width()-xSize)/2
            yCorner = 0
        else:
            xSize = self.width()
            ySize = xSize/aspect
            xCorner = 0
            yCorner = (self.height()-ySize)/2
            
        x, y = point
        scaledX = int(xSize*x)
        scaledY = int(ySize*y)
        translatedX = scaledX + xCorner
        translatedY = scaledY + yCorner
        
        return (translatedX, translatedY)
        
        
    def widget2ImageCoords(self, point):
        
        textureWidth = self.texture.size().width()
        textureHeight = self.texture.size().height()
        aspect = float(textureWidth) / textureHeight
        
        if aspect < float(self.width()) / self.height():
            xSize = int(aspect * self.height())
            ySize = self.height()
            xCorner = (self.width()-xSize)/2
            yCorner = 0
        else:
            xSize = self.width()
            ySize = xSize/aspect
            xCorner = 0
            yCorner = (self.height()-ySize)/2
            
        x, y = point
        translatedX = x - xCorner
        translatedY = y - yCorner
        scaledX = float(translatedX)/xSize
        scaledY = float(translatedY)/ySize
        
        return (scaledX, scaledY)

        
        
        
class Cuboid(QtGui.QListWidgetItem):
    
    def __init__(self, name, dimensions, modelGenerator, uvs=[[[0.0,0.0], [1.0,1.0]],
                                                              [[0.0,0.0], [1.0,1.0]],
                                                              [[0.0,0.0], [1.0,1.0]],
                                                              [[0.0,0.0], [1.0,1.0]],
                                                              [[0.0,0.0], [1.0,1.0]],
                                                              [[0.0,0.0], [1.0,1.0]]]):
        QtGui.QListWidgetItem.__init__(self, name)
        
        self.name = name
        self.textures = [[BASEPATH+"/assets/textures/blocks/unknown.png", 0, [0,0,""]],
                         [BASEPATH+"/assets/textures/blocks/unknown.png", 0, [0,0,""]],
                         [BASEPATH+"/assets/textures/blocks/unknown.png", 0, [0,0,""]],
                         [BASEPATH+"/assets/textures/blocks/unknown.png", 0, [0,0,""]],
                         [BASEPATH+"/assets/textures/blocks/unknown.png", 0, [0,0,""]],
                         [BASEPATH+"/assets/textures/blocks/unknown.png", 0, [0,0,""]]]
        self.texIdx = None
        self.dimensions = dimensions
        self.uvs = uvs
        self.rotation = 0.0
        self.rotationAxis = 0
        self.rotationCenter = [8.0,8.0,8.0]
        self.translation = [0.0,0.0,0.0]
        
        self.modelGenerator = modelGenerator
        
        self.shader = 0
        
#        verts = np.array([[0,0,0], [1,0,0], [1,1,0], [0,1,0], [0,0,1], [1,0,1], [1,1,1], [0,1,1]], dtype="f")
#        self.vertVBO = [vbo.VBO(v) for v in verts]
#        indices = np.array([3,2,1,0, 0,1,5,4, 0,4,7,3, 4,5,6,7, 3,7,6,2, 2,6,5,1], dtype=np.int32)
#        self.inxVBO = vbo.VBO(indices, target=GL.GL_ELEMENT_ARRAY_BUFFER)
        self.verts = [[[1,0,0], [0,0,0], [0,1,0], [1,1,0]],
                      [[0,0,1], [1,0,1], [1,1,1], [0,1,1]],
                      [[0,1,1], [0,1,0], [0,0,0], [0,0,1]],
                      [[1,0,1], [1,0,0], [1,1,0], [1,1,1]],
                      [[0,0,1], [0,0,0], [1,0,0], [1,0,1]],
                      [[1,1,1], [1,1,0], [0,1,0], [0,1,1]]]
        
        self.rotationMatrix = mu.Matrix4Rotate(0.0, 0.0, 0.0)
        self.translationMatrix = mu.Matrix4Translate(0.0, 0.0, 0.0)
        self.scalingMatrix = mu.Matrix4Scale(self.dimensions[0], self.dimensions[1], self.dimensions[2])
        
        self.transformationMatrix = self.translationMatrix * self.rotationMatrix * self.scalingMatrix
        
        self.gl2mcMat = mu.Matrix4([[0.0,0.0,1.0,0.0],
                                    [1.0,0.0,0.0,0.0],
                                    [0.0,1.0,0.0,0.0],
                                    [0.0,0.0,0.0,1.0]])
        
        self.initTextures()
        
        
    def setTranslate(self, x, y, z):
        
        self.translation[0] = x
        self.translation[1] = y
        self.translation[2] = z
        self.updateTranslationMatrix()
        
        
    def setRotation(self, x, y, z):
        
        self.rotation[0] = x
        self.rotation[1] = y
        self.rotation[2] = z
        self.updateRotationMatrix()
        
        
    def setDimensions(self, x, y, z):
        
        self.dimensions[0] = x
        self.dimensions[1] = y
        self.dimensions[2] = z
        self.updateScalingMatrix()
        
        
    def updateRotationMatrix(self):
        
        if self.rotationAxis == 0:
            self.rotationMatrix = mu.Matrix4Rotate(2*math.pi/360.0*self.rotation, 0.0, 0.0)
        if self.rotationAxis == 1:
            self.rotationMatrix = mu.Matrix4Rotate(0.0, 2*math.pi/360.0*self.rotation, 0.0)
        if self.rotationAxis == 2:
            self.rotationMatrix = mu.Matrix4Rotate(0.0, 0.0, 2*math.pi/360.0*self.rotation)
        
        
    def updateTranslationMatrix(self):
        
        self.translationMatrix = mu.Matrix4Translate(self.translation[0], self.translation[1], self.translation[2])
        
        
    def updateScalingMatrix(self):
        
        self.scalingMatrix = mu.Matrix4Scale(self.dimensions[0], self.dimensions[1], self.dimensions[2])
        
        
    def updateUVs(self, uvs):
        
        self.uvs = uvs
        
        
    def initTextures(self):
        
        self.texIdx = GL.glGenTextures(6)
        self.setTexture(0, self.textures[0][0])
        self.setTexture(1, self.textures[1][0])
        self.setTexture(2, self.textures[2][0])
        self.setTexture(3, self.textures[3][0])
        self.setTexture(4, self.textures[4][0])
        self.setTexture(5, self.textures[5][0])
        
        
    def setTexture(self, idx, path):
        
        self. textures[idx][0] = path
        
        im = Image.open(path)
        width, height, data = im.size[0], im.size[1], im.convert("RGBA").tostring("raw", "RGBA", 0, -1)
        self.textures[idx][2][0] = width
        self.textures[idx][2][1] = height
        self.textures[idx][2][2] = data
        GL.glActiveTexture(GL.GL_TEXTURE0+idx)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texIdx[idx])
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data);
        GL.glDisable(GL.GL_TEXTURE_2D)
        
        
    def loadShader(self, name):
        
        vsh = open(BASEPATH+"/assets/shader/"+name+".vsh")
        fsh = open(BASEPATH+"/assets/shader/"+name+".fsh")
        VERTEX_SHADER = shaders.compileShader(vsh.read(), GL.GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(fsh.read(), GL.GL_FRAGMENT_SHADER)
        vsh.close()
        fsh.close()
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        
        
    def draw(self):

        for polIdx, pol in zip(range(len(self.verts)), self.verts):
            
            GL.glActiveTexture(GL.GL_TEXTURE0+polIdx)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texIdx[polIdx])
            
            shaders.glUseProgram(self.shader)
            loc = GL.glGetUniformLocation(self.shader, "u_translate")
            GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.translationMatrix.matrix)
            loc = GL.glGetUniformLocation(self.shader, "u_rotate")
            GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.rotationMatrix.matrix)
            loc = GL.glGetUniformLocation(self.shader, "u_scale")
            GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.scalingMatrix.matrix)
            loc = GL.glGetUniformLocation(self.shader, "u_texture")
            GL.glUniform1i(loc, polIdx)
            loc = GL.glGetUniformLocation(self.shader, "u_rotationCenter")
            GL.glUniform4fv(loc, 1, self.rotationCenter)
            
            GL.glBegin(GL.GL_POLYGON)
            
            GL.glTexCoord2f(1.0-self.uvs[polIdx][0][0], 1.0-self.uvs[polIdx][0][1])
            GL.glVertex3f(pol[0][0], pol[0][1], pol[0][2])
            GL.glTexCoord2f(1.0-self.uvs[polIdx][0][0], 1.0-self.uvs[polIdx][1][1])
            GL.glVertex3f(pol[1][0], pol[1][1], pol[1][2])
            GL.glTexCoord2f(1.0-self.uvs[polIdx][1][0], 1.0-self.uvs[polIdx][1][1])
            GL.glVertex3f(pol[2][0], pol[2][1], pol[2][2])
            GL.glTexCoord2f(1.0-self.uvs[polIdx][1][0], 1.0-self.uvs[polIdx][0][1])
            GL.glVertex3f(pol[3][0], pol[3][1], pol[3][2])
            
            GL.glEnd()
            
            shaders.glUseProgram(0)
            
            
    def inMCCoordinates(self, pt):
        
        return (self.gl2mcMat*mu.Vector4(pt[0], pt[1], pt[2], 1.0)).vector[:3]
        
        
    def getUVs(self, texIdx):
        
        return [16*coord for coord in self.uvs[texIdx][0]+self.uvs[texIdx][1]]
        
        
    def setName(self, name):
        
        self.name = name
        self.setText(name)
                    
                    
    def getDictRepr(self):
        
        cub = {}
        
        cub["name"]  = self.name
        cub["from"]  = self.inMCCoordinates(self.translation)
        cub["to"]    = self.inMCCoordinates([trans+size for trans, size in zip(self.translation, self.dimensions)])
        cub["rotation"] = {"origin": self.inMCCoordinates(self.rotationCenter),
                           "axis": "z" if self.rotationAxis==0 else "x" if self.rotationAxis==1 else "y",
                           "angle": -self.rotation}
        cub["faces"] = {"down": {"texture":"texture"+str(self.modelGenerator.addTexture(self.textures[0][0])), "uv":self.getUVs(0)},
                        "up":   {"texture":"texture"+str(self.modelGenerator.addTexture(self.textures[1][0])), "uv":self.getUVs(1)},
                        "north":{"texture":"texture"+str(self.modelGenerator.addTexture(self.textures[2][0])), "uv":self.getUVs(2)},
                        "south":{"texture":"texture"+str(self.modelGenerator.addTexture(self.textures[3][0])), "uv":self.getUVs(3)},
                        "west": {"texture":"texture"+str(self.modelGenerator.addTexture(self.textures[4][0])), "uv":self.getUVs(4)},
                        "east": {"texture":"texture"+str(self.modelGenerator.addTexture(self.textures[5][0])), "uv":self.getUVs(5)}}
                        
        return cub
        
        
    def savedata(self):
        
        return {"name":self.name,
                "dimensions":self.dimensions,
                "translation":self.translation,
                "rotation":self.rotation,
                "rotationAxis":self.rotationAxis,
                "uvs":self.uvs,
                "textures":[tex[0] for tex in self.textures]}
                
                
    def loadData(self, data):
        
        self.dimensions = data["dimensions"]
        self.translation = data["translation"]
        self.rotation = data["rotation"]
        self.rotationAxis = data["rotationAxis"]
        self.uvs = data["uvs"]
        for idx in range(len(data["textures"])):
            self.setTexture(idx, data["textures"][idx])
        self.updateRotationMatrix()
        self.updateScalingMatrix()
        self.updateTranslationMatrix()
                        
                        
                        
                        
                        
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    gen = BlockModelGenerator()
    
    gen.addCuboid(Cuboid("block1", [0,0,0], [.5,.5,.5]))
    gen.addCuboid(Cuboid("block1", [.5,.5,.5], [1,1,1]))
    
    print(gen.getJSON())
    
    sys.exit(app.exec_())