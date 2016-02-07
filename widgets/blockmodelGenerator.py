# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import math
from utils import mathUtils as mu
from PyQt4 import QtGui, QtCore, QtOpenGL, uic
from OpenGL import GL, GLU
from OpenGL.GL import shaders
from OpenGL.arrays import vbo



BASEPATH = os.path.dirname(sys.argv[0])




class BlockModelGenerator(QtGui.QDialog):
    
    def __init__(self, mainWindow):
        QtGui.QDialog.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.initUI()
        
        self.show()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(BASEPATH+"/ui/BlockModelCreator.ui", self)
        
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
        self.connect(self.rotationX, QtCore.SIGNAL("valueChanged(double)"), self.setRotationX)
        self.connect(self.rotationY, QtCore.SIGNAL("valueChanged(double)"), self.setRotationY)
        self.connect(self.rotationZ, QtCore.SIGNAL("valueChanged(double)"), self.setRotationZ)
        self.connect(self.cuboidList, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.cuboidSelected)
        self.connect(self.addCuboidButton, QtCore.SIGNAL("clicked()"), self.addCuboid)
        self.connect(self.removeCuboidButton, QtCore.SIGNAL("clicked()"), self.removeCuboid)
        self.connect(self.changeDownTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureDown)
        self.connect(self.changeUpTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureUp)
        self.connect(self.changeNorthTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureNorth)
        self.connect(self.changeSouthTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureSouth)
        self.connect(self.changeWestTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureWest)
        self.connect(self.changeEastTextureButton, QtCore.SIGNAL("clicked()"), self.changeTextureEast)
            
            
    def cuboidSelected(self, cuboid):
        
        self.dimensionsX.setValue(cuboid.dimensions[0])
        self.dimensionsY.setValue(cuboid.dimensions[1])
        self.dimensionsZ.setValue(cuboid.dimensions[2])
        self.translationX.setValue(cuboid.translation[0])
        self.translationY.setValue(cuboid.translation[1])
        self.translationZ.setValue(cuboid.translation[2])
        self.rotationX.setValue(cuboid.rotation[0])
        self.rotationY.setValue(cuboid.rotation[1])
        self.rotationZ.setValue(cuboid.rotation[2])
        self.uvEditorDown.loadTexture(cuboid.textures[0])
        self.uvEditorUp.loadTexture(cuboid.textures[1])
        self.uvEditorNorth.loadTexture(cuboid.textures[2])
        self.uvEditorSouth.loadTexture(cuboid.textures[3])
        self.uvEditorWest.loadTexture(cuboid.textures[4])
        self.uvEditorEast.loadTexture(cuboid.textures[5])
        
        
    def setDimensionX(self, dim):
        
        self.selectedCuboid().dimensions[0] = dim
        self.selectedCuboid().updateScalingMatrix()
        self.GLWidget.updateGL()
        
        
    def setDimensionY(self, dim):
        
        self.selectedCuboid().dimensions[1] = dim
        self.selectedCuboid().updateScalingMatrix()
        self.GLWidget.updateGL()
        
        
    def setDimensionZ(self, dim):
        
        self.selectedCuboid().dimensions[2] = dim
        self.selectedCuboid().updateScalingMatrix()
        self.GLWidget.updateGL()
        
        
    def setTranslationX(self, trans):
        
        self.selectedCuboid().translation[0] = trans
        self.selectedCuboid().updateTranslationMatrix()
        self.GLWidget.updateGL()
        
        
    def setTranslationY(self, trans):
        
        self.selectedCuboid().translation[1] = trans
        self.selectedCuboid().updateTranslationMatrix()
        self.GLWidget.updateGL()
        
        
    def setTranslationZ(self, trans):
        
        self.selectedCuboid().translation[2] = trans
        self.selectedCuboid().updateTranslationMatrix()
        self.GLWidget.updateGL()
        
        
    def setRotationX(self, rot):
        
        self.selectedCuboid().rotation[0] = rot/180.0*math.pi
        self.selectedCuboid().updateRotationMatrix()
        self.GLWidget.updateGL()
        
        
    def setRotationY(self, rot):
        
        self.selectedCuboid().rotation[1] = rot/180.0*math.pi
        self.selectedCuboid().updateRotationMatrix()
        self.GLWidget.updateGL()
        
        
    def setRotationZ(self, rot):
        
        self.selectedCuboid().rotation[2] = rot/180.0*math.pi
        self.selectedCuboid().updateRotationMatrix()
        self.GLWidget.updateGL()
        
        
    def changeTextureDown(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().textures[0] = tex
            self.uvEditorDown.loadTexture(tex)
            
            
    def changeTextureUp(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().textures[1] = tex
            self.uvEditorUp.loadTexture(tex)
            
            
    def changeTextureNorth(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().textures[2] = tex
            self.uvEditorNorth.loadTexture(tex)
            
            
    def changeTextureSouth(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().textures[3] = tex
            self.uvEditorSouth.loadTexture(tex)
            
            
    def changeTextureWest(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().textures[4] = tex
            self.uvEditorWest.loadTexture(tex)
            
            
    def changeTextureEast(self):
        
        tex = str(QtGui.QFileDialog.getOpenFileName(self, self.mainWindow.translations.getTranslation("textureSelection"),
                                                          self.mainWindow.config["workspace"],
                                                          self.mainWindow.translations.getTranslation("pngFiles")+" (*.png)"))
        if tex != "":
            self.selectedCuboid().textures[5] = tex
            self.uvEditorEast.loadTexture(tex)
            
            
    def selectedCuboid(self):
        
        return self.cuboidList.currentItem()
        
        
    def addCuboid(self):
        
        cub = Cuboid("unnamed", [1.0, 1.0, 1.0])
        cub.loadShader("cuboid")
        self.cuboidList.addItem(cub)
        self.GLWidget.updateGL()
        
        
    def removeCuboid(self):
        
        self.cuboidList.takeItem(self.cuboidList.currentRow())
        self.GLWidget.updateGL()
        
        
    def addTexture(self, mcPath):
        
        self.textures.append(mcPath)
        
        
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
        
        model = {}
        
        model["elements"] = []
        for cub in self.cuboids():
            model["elements"].append(cub.getDictRepr())
            
        model["textures"] = {}
        for i in range(len(self.textures)):
            model["textures"][str(i)] = self.textures[i]
            
        return self.dict2JSON(model)
        
        
        
        
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
        self.uvs = [[0,0], [0,0]]
        
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
        
        
    def drawTexture(self, painter):
        
        textureWidth = self.texture.size().width()
        textureHeight = self.texture.size().height()
        left = self.image2WidgetCoords((0, 0))
        right = self.image2WidgetCoords((textureWidth, textureHeight))
        painter.drawPixmap(left[0],
                           left[1],
                           right[0]-left[0],
                           right[1]-left[1],
                           self.texture)
        
        
    def drawUVs(self, painter):
        
        left = self.image2WidgetCoords((self.uvs[0][0], self.uvs[0][1]))
        right = self.image2WidgetCoords((self.uvs[1][0], self.uvs[1][1]))
            
        painter.fillRect(left[0],
                         left[1],
                         right[0]-left[0],
                         right[1]-left[1],
                         QtGui.QColor(255, 255, 255, 127))
                         
                         
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
        scaledX = int(xSize*float(x)/textureWidth)
        scaledY = int(ySize*float(y)/textureHeight)
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
        scaledX = int(textureWidth*float(translatedX)/xSize)
        scaledY = int(textureHeight*float(translatedY)/ySize)
        
        return (scaledX, scaledY)

        
        
        
class Cuboid(QtGui.QListWidgetItem):
    
    def __init__(self, name, dimensions, uvs=[[0, [0,0, 1,1]],
                                              [0, [0,0, 1,1]],
                                              [0, [0,0, 1,1]],
                                              [0, [0,0, 1,1]],
                                              [0, [0,0, 1,1]],
                                              [0, [0,0, 1,1]]]):
        QtGui.QListWidgetItem.__init__(self, name)
        
        self.name = name
        self.textures = [BASEPATH+"/assets/textures/blocks/unknown.png"]*6
        self.dimensions = dimensions
        self.uvs = uvs
        self.rotation = [0.0,0.0,0.0]
        self.translation = [0.0,0.0,0.0]
        
        self.shader = 0
        
        verts = np.array([[0,0,0], [1,0,0], [1,1,0], [0,1,0], [0,0,1], [1,0,1], [1,1,1], [0,1,1]], dtype="f")
        self.vertVBO = vbo.VBO(verts)
        indices = np.array([3,2,1,0, 0,1,5,4, 0,4,7,3, 4,5,6,7, 3,7,6,2, 2,6,5,1], dtype=np.int32)
        self.inxVBO = vbo.VBO(indices, target=GL.GL_ELEMENT_ARRAY_BUFFER)
        
        self.rotationMatrix = mu.Matrix4Rotate(0.0, 0.0, 0.0)
        self.translationMatrix = mu.Matrix4Translate(0.0, 0.0, 0.0)
        self.scalingMatrix = mu.Matrix4Scale(self.dimensions[0], self.dimensions[1], self.dimensions[2])
        
        self.transformationMatrix = self.translationMatrix * self.rotationMatrix * self.scalingMatrix
        
        
    def setRranslate(self, x, y, z):
        
        self.translation[0] = x
        self.translation[1] = y
        self.translation[2] = z
        
        
    def setRotation(self, x, y, z):
        
        self.rotation[0] = x
        self.rotation[1] = y
        self.rotation[2] = z
        self.rotationMatrix = mu.Matrix4Rotate(x, y, z)
        
        
    def updateRotationMatrix(self):
        
        self.rotationMatrix = mu.Matrix4Rotate(self.rotation[0], self.rotation[1], self.rotation[2])
        
        
    def updateTranslationMatrix(self):
        
        self.translationMatrix = mu.Matrix4Translate(self.translation[0], self.translation[1], self.translation[2])
        
        
    def updateScalingMatrix(self):
        
        self.scalingMatrix = mu.Matrix4Scale(self.dimensions[0], self.dimensions[1], self.dimensions[2])
        
        
    def loadShader(self, name):
        
        vsh = open(BASEPATH+"/assets/shader/"+name+".vsh")
        fsh = open(BASEPATH+"/assets/shader/"+name+".fsh")
        VERTEX_SHADER = shaders.compileShader(vsh.read(), GL.GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(fsh.read(), GL.GL_FRAGMENT_SHADER)
        vsh.close()
        fsh.close()
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        
        
    def draw(self):
        
        shaders.glUseProgram(self.shader)
        loc = GL.glGetUniformLocation(self.shader, "u_translate")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.translationMatrix.matrix)
        loc = GL.glGetUniformLocation(self.shader, "u_rotate")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.rotationMatrix.matrix)
        loc = GL.glGetUniformLocation(self.shader, "u_scale")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.scalingMatrix.matrix)
        try:
            self.inxVBO.bind()
            self.vertVBO.bind()
            try:
                GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
                GL.glVertexPointerf(self.vertVBO)
                #GL.glDrawArrays(GL.GL_QUADS, 0, 9)
                GL.glDrawElementsui(GL.GL_QUADS, self.inxVBO)
            finally:
                self.vertVBO.unbind()
                self.inxVBO.unbind()
                GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        finally:
            shaders.glUseProgram(0)
                    
                    
    def getDictRepr(self):
        
        cub = {}
        
        cub["name"]  = self.name
        cub["from"]  = self.corner1
        cub["to"]    = self.corner2
        cub["faces"] = {"north":{"texture":"#"+str(self.uvs[0][0]), "uv":self.uvs[0][1]},
                        "east": {"texture":"#"+str(self.uvs[1][0]), "uv":self.uvs[1][1]},
                        "south":{"texture":"#"+str(self.uvs[2][0]), "uv":self.uvs[2][1]},
                        "west": {"texture":"#"+str(self.uvs[3][0]), "uv":self.uvs[3][1]},
                        "up":   {"texture":"#"+str(self.uvs[4][0]), "uv":self.uvs[4][1]},
                        "down": {"texture":"#"+str(self.uvs[5][0]), "uv":self.uvs[5][1]}}
                        
        return cub
                        
                        
                        
                        
                        
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    gen = BlockModelGenerator()
    
    gen.addCuboid(Cuboid("block1", [0,0,0], [.5,.5,.5]))
    gen.addCuboid(Cuboid("block1", [.5,.5,.5], [1,1,1]))
    
    print(gen.getJSON())
    
    sys.exit(app.exec_())