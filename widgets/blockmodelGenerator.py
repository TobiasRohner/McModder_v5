# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import math
from PyQt4 import QtGui, QtCore, QtOpenGL, uic
from OpenGL import GL, GLU



BASEPATH = os.path.dirname(sys.argv[0])




class BlockModelGenerator(QtGui.QDialog):
    
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        self.textures = []
        self.cuboids = [Cuboid("default", [0.0,0.0,0.0], [16.0,16.0,16.0])]
        
        self.initUI()
        
        self.show()
        
        
    def initUI(self):
        
        self.ui = uic.loadUi(BASEPATH+"/ui/BlockModelCreator.ui", self)
        
        self.GLWidget = ModelGLWidget(self)
        
        self.mainLayout.insertWidget(0, self.GLWidget, 1)
        
        
    def addCuboid(self, cub):
        
        self.cuboids.append(cub)
        
        
    def addTexture(self, mcPath):
        
        self.textures.append(mcPath)
        
        
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
        for cub in self.cuboids:
            model["elements"].append(cub.getDictRepr())
            
        model["textures"] = {}
        for i in range(len(self.textures)):
            model["textures"][str(i)] = self.textures[i]
            
        return self.dict2JSON(model)
        
        
        
        
class ModelGLWidget(QtOpenGL.QGLWidget):
    
    def __init__(self, modelGenerator):
        QtOpenGL.QGLWidget.__init__(self)
        
        self.modelGenerator = modelGenerator
        
        self.setMinimumSize(100, 100)
        
        
    def paintGL(self):
        
        GL.glBegin(GL.GL_QUADS)
        for cub in self.modelGenerator.cuboids:
            cub.draw(cub.translation, cub.rotation)
        GL.glEnd()


    def resizeGL(self, w, h):
        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(90.0, w/h, 0.1, 100.0)
        GL.glViewport(0, 0, w, h)


    def initializeGL(self):
        
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        
        
        
class Cuboid():
    
    def __init__(self, name, origin, dimensions, uvs=[[0, [0,0, 1,1]],
                                                    [0, [0,0, 1,1]],
                                                    [0, [0,0, 1,1]],
                                                    [0, [0,0, 1,1]],
                                                    [0, [0,0, 1,1]],
                                                    [0, [0,0, 1,1]]]):
        
        self.name = name
        self.origin = origin
        self.dimensions = dimensions
        self.uvs = uvs
        self.rotation = [0.0,0.0,0.0]
        self.translation = [0.0,0.0,0.0]
        
        
    def draw(self, trans, rot):
        
        GL.glVertex3f(self.corner1[0],
                      self.corner1[1],
                      self.corner1[2])
        GL.glVertex3f(self.corner2[0],
                      self.corner1[1],
                      self.corner1[2])
        GL.glVertex3f(self.corner2[0],
                      self.corner2[1],
                      self.corner1[2])
        GL.glVertex3f(self.corner1[0],
                      self.corner2[1],
                      self.corner1[2])
                    
                    
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