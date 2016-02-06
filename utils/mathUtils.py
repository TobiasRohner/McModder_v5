# -*- coding: utf-8 -*-
import math




class Matrix():
    
    def __init__(self, mat):
        
        self.matrix = mat
        
        
    def __getitem__(self, key):
        
        return self.matrix[key]
        
        
    def __setitem__(self, key, value):
        
        self.matrix[key] = value
        
        
        
        
class Matrix3(Matrix):
    
    def __init__(self, mat=[[1.0,0.0,0.0],
                            [0.0,1.0,0.0],
                            [0.0,0.0,1.0]]):
        Matrix.__init__(self, mat)
        
        
    def __radd__(self, other):
        
        if isinstance(other, Matrix3):
            mat = Matrix3()
            mat[0][0] += other[0][0]
            mat[0][1] += other[0][1]
            mat[0][2] += other[0][2]
            mat[1][0] += other[1][0]
            mat[1][1] += other[1][1]
            mat[1][2] += other[1][2]
            mat[2][0] += other[2][0]
            mat[2][1] += other[2][1]
            mat[2][2] += other[2][2]
            return mat
        else:
            raise TypeError
            
            
    def __iadd__(self, other):
        
        self.matrix = (self+other).matrix
        
        
    def __rmul__(self, other):
        
        if isinstance(other, Matrix3):
            mat = Matrix3()
            mat[0][0] = self.matrix[0][0]*other[0][0] + self.matrix[1][0]*other[0][1] + self.matrix[2][0]*other[0][2]
            mat[0][1] = self.matrix[0][1]*other[0][0] + self.matrix[1][1]*other[0][1] + self.matrix[2][1]*other[0][2]
            mat[0][2] = self.matrix[0][2]*other[0][0] + self.matrix[1][2]*other[0][1] + self.matrix[2][2]*other[0][2]
            mat[1][0] = self.matrix[0][0]*other[1][0] + self.matrix[1][0]*other[1][1] + self.matrix[2][0]*other[1][2]
            mat[1][1] = self.matrix[0][1]*other[1][0] + self.matrix[1][1]*other[1][1] + self.matrix[2][1]*other[1][2]
            mat[1][2] = self.matrix[0][2]*other[1][0] + self.matrix[1][2]*other[1][1] + self.matrix[2][2]*other[1][2]
            mat[2][0] = self.matrix[0][0]*other[2][0] + self.matrix[1][0]*other[2][1] + self.matrix[2][0]*other[2][2]
            mat[2][1] = self.matrix[0][1]*other[2][0] + self.matrix[1][1]*other[2][1] + self.matrix[2][1]*other[2][2]
            mat[2][2] = self.matrix[0][2]*other[2][0] + self.matrix[1][2]*other[2][1] + self.matrix[2][2]*other[2][2]
            return mat
        elif isinstance(other, int) or isinstance(other, float):
            mat = Matrix3()
            mat[0][0] = other*self.matrix[0][0]
            mat[0][1] = other*self.matrix[0][1]
            mat[0][2] = other*self.matrix[0][2]
            mat[1][0] = other*self.matrix[1][0]
            mat[1][1] = other*self.matrix[1][1]
            mat[1][2] = other*self.matrix[1][2]
            mat[2][0] = other*self.matrix[2][0]
            mat[2][1] = other*self.matrix[2][1]
            mat[2][2] = other*self.matrix[2][2]
            return mat
        else:
            raise TypeError
            
            
    def __imul__(self, other):
        
        if isinstance(other, Vector3):
            raise TypeError
        else:
            self.matrix = (self*other).matrix
            
            
    def __rdiv__(self, other):
        
        if isinstance(other, int) or isinstance(other, float):
            mat = Matrix3()
            mat[0][0] = self.matrix[0][0]/other
            mat[0][1] = self.matrix[0][1]/other
            mat[0][2] = self.matrix[0][2]/other
            mat[1][0] = self.matrix[1][0]/other
            mat[1][1] = self.matrix[1][1]/other
            mat[1][2] = self.matrix[1][2]/other
            mat[2][0] = self.matrix[2][0]/other
            mat[2][1] = self.matrix[2][1]/other
            mat[2][2] = self.matrix[2][2]/other
            return mat
        else:
            raise TypeError
            
            
    def __idiv__(self, other):
        
        self.matrix = (self/other).matrix
        
        
    def __str__(self):
        
        strMat = [[str(e) for e in col] for col in self.matrix]
        length = 0
        for x in range(3):
            for y in range(3):
                if len(strMat[x][y]) > length:
                    length = len(strMat[x][y])
        strMat = [[e.center(length+2) for e in col] for col in strMat]
        final  = "/" +strMat[0][0]+strMat[1][0]+strMat[2][0]+"\\\n"
        final += "|" +strMat[0][1]+strMat[1][1]+strMat[2][1]+"|\n"
        final += "\\"+strMat[0][2]+strMat[1][2]+strMat[2][2]+"/"
        return final
        
        
    def transpose(self):
        
        mat = Matrix3()
        mat[0][0] = self.matrix[0][0]
        mat[0][1] = self.matrix[1][0]
        mat[0][2] = self.matrix[2][0]
        mat[1][0] = self.matrix[0][1]
        mat[1][1] = self.matrix[1][1]
        mat[1][2] = self.matrix[2][1]
        mat[2][0] = self.matrix[0][2]
        mat[2][1] = self.matrix[1][2]
        mat[2][2] = self.matrix[2][2]
        return mat
            
            
            
            
class Matrix4(Matrix):
    
    def __init__(self, mat=[[1.0,0.0,0.0,0.0],
                            [0.0,1.0,0.0,0.0],
                            [0.0,0.0,1.0,0.0],
                            [0.0,0.0,0.0,1.0]]):
        Matrix.__init__(self, mat)
        
        
    def __radd__(self, other):
        
        if isinstance(other, Matrix4):
            mat = Matrix4()
            mat[0][0] += other[0][0]
            mat[0][1] += other[0][1]
            mat[0][2] += other[0][2]
            mat[0][3] += other[0][3]
            mat[1][0] += other[1][0]
            mat[1][1] += other[1][1]
            mat[1][2] += other[1][2]
            mat[1][3] += other[1][3]
            mat[2][0] += other[2][0]
            mat[2][1] += other[2][1]
            mat[2][2] += other[2][2]
            mat[2][3] += other[2][3]
            mat[3][0] += other[3][0]
            mat[3][1] += other[3][1]
            mat[3][2] += other[3][2]
            mat[3][3] += other[3][3]
            return mat
        else:
            raise TypeError
            
            
    def __iadd__(self, other):
        
        self.matrix = (self+other).matrix
        
        
    def __rmul__(self, other):
        
        if isinstance(other, Matrix4):
            mat = Matrix4()
            mat[0][0] = self.matrix[0][0]*other[0][0] + self.matrix[1][0]*other[0][1] + self.matrix[2][0]*other[0][2] + self.matrix[3][0]*other[0][3]
            mat[0][1] = self.matrix[0][1]*other[0][0] + self.matrix[1][1]*other[0][1] + self.matrix[2][1]*other[0][2] + self.matrix[3][1]*other[0][3]
            mat[0][2] = self.matrix[0][2]*other[0][0] + self.matrix[1][2]*other[0][1] + self.matrix[2][2]*other[0][2] + self.matrix[3][2]*other[0][3]
            mat[0][3] = self.matrix[0][3]*other[0][0] + self.matrix[1][3]*other[0][1] + self.matrix[2][3]*other[0][2] + self.matrix[3][3]*other[0][3]
            mat[1][0] = self.matrix[0][0]*other[1][0] + self.matrix[1][0]*other[1][1] + self.matrix[2][0]*other[1][2] + self.matrix[3][0]*other[1][3]
            mat[1][1] = self.matrix[0][1]*other[1][0] + self.matrix[1][1]*other[1][1] + self.matrix[2][1]*other[1][2] + self.matrix[3][1]*other[1][3]
            mat[1][2] = self.matrix[0][2]*other[1][0] + self.matrix[1][2]*other[1][1] + self.matrix[2][2]*other[1][2] + self.matrix[3][2]*other[1][3]
            mat[1][3] = self.matrix[0][3]*other[1][0] + self.matrix[1][3]*other[1][1] + self.matrix[2][3]*other[1][2] + self.matrix[3][3]*other[1][3]
            mat[2][0] = self.matrix[0][0]*other[2][0] + self.matrix[1][0]*other[2][1] + self.matrix[2][0]*other[2][2] + self.matrix[3][0]*other[2][3]
            mat[2][1] = self.matrix[0][1]*other[2][0] + self.matrix[1][1]*other[2][1] + self.matrix[2][1]*other[2][2] + self.matrix[3][1]*other[2][3]
            mat[2][2] = self.matrix[0][2]*other[2][0] + self.matrix[1][2]*other[2][1] + self.matrix[2][2]*other[2][2] + self.matrix[3][2]*other[2][3]
            mat[2][3] = self.matrix[0][3]*other[2][0] + self.matrix[1][3]*other[2][1] + self.matrix[2][3]*other[2][2] + self.matrix[3][3]*other[2][3]
            mat[3][0] = self.matrix[0][0]*other[3][0] + self.matrix[1][0]*other[3][1] + self.matrix[2][0]*other[3][2] + self.matrix[3][0]*other[3][3]
            mat[3][1] = self.matrix[0][1]*other[3][0] + self.matrix[1][1]*other[3][1] + self.matrix[2][1]*other[3][2] + self.matrix[3][1]*other[3][3]
            mat[3][2] = self.matrix[0][2]*other[3][0] + self.matrix[1][2]*other[3][1] + self.matrix[2][2]*other[3][2] + self.matrix[3][2]*other[3][3]
            mat[3][3] = self.matrix[0][3]*other[3][0] + self.matrix[1][3]*other[3][1] + self.matrix[2][3]*other[3][2] + self.matrix[3][3]*other[3][3]
            return mat
        elif isinstance(other, int) or isinstance(other, float):
            mat = Matrix4()
            mat[0][0] = other*self.matrix[0][0]
            mat[0][1] = other*self.matrix[0][1]
            mat[0][2] = other*self.matrix[0][2]
            mat[0][3] = other*self.matrix[0][3]
            mat[1][0] = other*self.matrix[1][0]
            mat[1][1] = other*self.matrix[1][1]
            mat[1][2] = other*self.matrix[1][2]
            mat[1][3] = other*self.matrix[1][3]
            mat[2][0] = other*self.matrix[2][0]
            mat[2][1] = other*self.matrix[2][1]
            mat[2][2] = other*self.matrix[2][2]
            mat[2][3] = other*self.matrix[2][3]
            mat[3][0] = other*self.matrix[3][0]
            mat[3][1] = other*self.matrix[3][1]
            mat[3][2] = other*self.matrix[3][2]
            mat[3][3] = other*self.matrix[3][3]
            return mat
        else:
            raise TypeError
            
            
    def __imul__(self, other):
        
        if isinstance(other, Vector4):
            raise TypeError
        else:
            self.matrix = (self*other).matrix
            
            
    def __rdiv__(self, other):
        
        if isinstance(other, int) or isinstance(other, float):
            mat = Matrix4()
            mat[0][0] = self.matrix[0][0]/other
            mat[0][1] = self.matrix[0][1]/other
            mat[0][2] = self.matrix[0][2]/other
            mat[0][3] = self.matrix[0][3]/other
            mat[1][0] = self.matrix[1][0]/other
            mat[1][1] = self.matrix[1][1]/other
            mat[1][2] = self.matrix[1][2]/other
            mat[1][3] = self.matrix[1][3]/other
            mat[2][0] = self.matrix[2][0]/other
            mat[2][1] = self.matrix[2][1]/other
            mat[2][2] = self.matrix[2][2]/other
            mat[2][3] = self.matrix[2][3]/other
            mat[3][0] = self.matrix[3][0]/other
            mat[3][1] = self.matrix[3][1]/other
            mat[3][2] = self.matrix[3][2]/other
            mat[3][3] = self.matrix[3][3]/other
            return mat
        else:
            raise TypeError
            
            
    def __idiv__(self, other):
        
        self.matrix = (self/other).matrix
        
        
    def __str__(self):
        
        strMat = [[str(e) for e in col] for col in self.matrix]
        length = 0
        for x in range(4):
            for y in range(4):
                if len(strMat[x][y]) > length:
                    length = len(strMat[x][y])
        strMat = [[e.center(length+2) for e in col] for col in strMat]
        final  = "/" +strMat[0][0]+strMat[1][0]+strMat[2][0]+strMat[3][0]+"\\\n"
        final += "|" +strMat[0][1]+strMat[1][1]+strMat[2][1]+strMat[3][1]+"|\n"
        final += "|" +strMat[0][2]+strMat[1][2]+strMat[2][2]+strMat[3][2]+"|\n"
        final += "\\"+strMat[0][3]+strMat[1][3]+strMat[2][3]+strMat[3][3]+"/"
        return final
        
        
    def transpose(self):
        
        mat = Matrix4()
        mat[0][0] = self.matrix[0][0]
        mat[0][1] = self.matrix[1][0]
        mat[0][2] = self.matrix[2][0]
        mat[0][3] = self.matrix[3][0]
        mat[1][0] = self.matrix[0][1]
        mat[1][1] = self.matrix[1][1]
        mat[1][2] = self.matrix[2][1]
        mat[1][3] = self.matrix[3][1]
        mat[2][0] = self.matrix[0][2]
        mat[2][1] = self.matrix[1][2]
        mat[2][2] = self.matrix[2][2]
        mat[2][3] = self.matrix[3][2]
        mat[3][0] = self.matrix[0][3]
        mat[3][1] = self.matrix[1][3]
        mat[3][2] = self.matrix[2][3]
        mat[3][3] = self.matrix[3][3]
        return mat
        
        
        
        
class Matrix3Rotate(Matrix3):
    
    def __init__(self, rotx, roty, rotz):
        
        sx = math.sin(rotx)
        sy = math.sin(roty)
        sz = math.sin(rotz)
        cx = math.cos(rotx)
        cy = math.cos(roty)
        cz = math.cos(rotz)
        
        Matrix3.__init__(self, mat=[[         cy*cz,         -cy*sz,     sy],
                                    [cx*sz+sx*sy*cz, cx*cz-sx*sy*sz, -sx*cy],
                                    [sx*sz-cx*sy*cz, sx*cz+cx*sy*sz,  cx*cy]])
#        
#        Rx = Matrix3([[1.0, 0.0, 0.0],
#                      [0.0,  cx,  sx],
#                      [0.0, -sx,  cx]])
#        Ry = Matrix3([[ cy, 0.0, -sy],
#                      [0.0, 1.0, 0.0],
#                      [ sy, 0.0,  cy]])
#        Rz = Matrix3([[ cz,  sz, 0.0],
#                      [-sz,  cz, 0.0],
#                      [0.0, 0.0, 1.0]])
#        Rxyz = Rz*Ry*Rx
#        
#        self.matrix = Rxyz.matrix
        
        
        
        
class Matrix4Rotate(Matrix4):
    
    def __init__(self, rotx, roty, rotz):
        
        sx = math.sin(rotx)
        sy = math.sin(roty)
        sz = math.sin(rotz)
        cx = math.cos(rotx)
        cy = math.cos(roty)
        cz = math.cos(rotz)
        
        Matrix4.__init__(self, mat=[[         cy*cz,         -cy*sz,     sy, 0.0],
                                    [cx*sz+sx*sy*cz, cx*cz-sx*sy*sz, -sx*cy, 0.0],
                                    [sx*sz-cx*sy*cz, sx*cz+cx*sy*sz,  cx*cy, 0.0],
                                    [           0.0,            0.0,    0.0, 1.0]])
#        Matrix4.__init__(self)
#        
#        sx = math.sin(rotx)
#        sy = math.sin(roty)
#        sz = math.sin(rotz)
#        cx = math.cos(rotx)
#        cy = math.cos(roty)
#        cz = math.cos(rotz)
#        
#        Rx = Matrix4([[1.0, 0.0, 0.0, 0.0],
#                      [0.0,  cx,  sx, 0.0],
#                      [0.0, -sx,  cx, 0.0],
#                      [0.0, 0.0, 0.0, 1.0]])
#        Ry = Matrix4([[ cy, 0.0, -sy, 0.0],
#                      [0.0, 1.0, 0.0, 0.0],
#                      [ sy, 0.0,  cy, 0.0],
#                      [0.0, 0.0, 0.0, 1.0]])
#        Rz = Matrix4([[ cz,  sz, 0.0, 0.0],
#                      [-sz,  cz, 0.0, 0.0],
#                      [0.0, 0.0, 1.0, 0.0],
#                      [0.0, 0.0, 0.0, 1.0]])
#        Rxyz = Rx*Ry*Rz
#        
#        self.matrix = Rxyz.matrix
        
        
        
        
class Matrix3RotAround(Matrix3):
    
    def __init__(self, axis, angle):
        Matrix3.__init__(self)
        
        s = math.sin(angle)
        c = math.cos(angle)
        
        self.matrix[0][0] = axis[0]*axis[0]*(1.0-c) + c
        self.matrix[0][1] = axis[1]*axis[0]*(1.0-c) + axis[2]*s
        self.matrix[0][2] = axis[2]*axis[0]*(1.0-c) - axis[1]*s
        self.matrix[1][0] = axis[0]*axis[1]*(1.0-c) - axis[2]*s
        self.matrix[1][1] = axis[1]*axis[1]*(1.0-c) + c
        self.matrix[1][2] = axis[2]*axis[1]*(1.0-c) + axis[0]*s
        self.matrix[2][0] = axis[0]*axis[2]*(1.0-c) + axis[1]*s
        self.matrix[2][1] = axis[1]*axis[2]*(1.0-c) - axis[0]*s
        self.matrix[2][2] = axis[2]*axis[2]*(1.0-c) + c
        
        
        
        
class Matrix4RotAround(Matrix4):
    
    def __init__(self, axis, angle):
        Matrix4.__init__(self)
        
        s = math.sin(angle)
        c = math.cos(angle)
        
        self.matrix[0][0] = axis[0]*axis[0]*(1.0-c) + c
        self.matrix[0][1] = axis[1]*axis[0]*(1.0-c) + axis[2]*s
        self.matrix[0][2] = axis[2]*axis[0]*(1.0-c) - axis[1]*s
        self.matrix[0][3] = 0.0
        self.matrix[1][0] = axis[0]*axis[1]*(1.0-c) - axis[2]*s
        self.matrix[1][1] = axis[1]*axis[1]*(1.0-c) + c
        self.matrix[1][2] = axis[2]*axis[1]*(1.0-c) + axis[0]*s
        self.matrix[1][3] = 0.0
        self.matrix[2][0] = axis[0]*axis[2]*(1.0-c) + axis[1]*s
        self.matrix[2][1] = axis[1]*axis[2]*(1.0-c) - axis[0]*s
        self.matrix[2][2] = axis[2]*axis[2]*(1.0-c) + c
        self.matrix[2][3] = 0.0
        self.matrix[3][0] = 0.0
        self.matrix[3][1] = 0.0
        self.matrix[3][2] = 0.0
        self.matrix[3][3] = 1.0
        
        
        
        
class Matrix4Translate(Matrix4):
    
    def __init__(self, x, y, z):
        Matrix4.__init__(self, [[1.0, 0.0, 0.0, 0.0],
                                [0.0, 1.0, 0.0, 0.0],
                                [0.0, 0.0, 1.0, 0.0],
                                [  x,   y,   z, 1.0]])
                                
                                
                                
                                
class Matrix3Scale(Matrix3):
    
    def __init__(self, x, y, z):
        Matrix3.__init__(self, [[  x, 0.0, 0.0],
                                [0.0,   y, 0.0],
                                [0.0, 0.0,   z]])
                                
                                
                                
                                
class Matrix4Scale(Matrix4):
    
    def __init__(self, x, y, z, w=1.0):
        Matrix4.__init__(self, [[  x, 0.0, 0.0, 0.0],
                                [0.0,   y, 0.0, 0.0],
                                [0.0, 0.0,   z, 0.0],
                                [0.0, 0.0, 0.0,   w]])
                                
                                
                                
                                
class Matrix4Transform(Matrix4):
    
    def __init__(self, transx, transy, transz, rotx, roty, rotz):
        Matrix4.__init__(self)
        
        Rxyz = Matrix4Rotate(rotx, roty, rotz)
        Txyz = Matrix4Translate(transx, transy, transz)
        Trans = Txyz*Rxyz
        
        self.matrix = Trans.matrix
            
            
            
            
class Vector():
    
    def __init__(self, vec):
        
        self.vector = vec
        
        
    def __getitem__(self, key):
        
        return self.vector[key]
        
        
    def __setitem__(self, key, value):
        
        self.vector[key] = value
        
        
        
        
class Vector3(Vector):
    
    def __init__(self, x, y, z):
        Vector.__init__(self, [x, y, z])
        
        
    def __radd__(self, other):
        
        if isinstance(other, Vector3):
            vec = Vector3()
            vec[0] = self.vector[0]+other[0]
            vec[1] = self.vector[1]+other[1]
            vec[2] = self.vector[2]+other[2]
            return vec
        else:
            raise TypeError
            
            
    def __iadd__(self, other):
        
        self.vector = (self+other).vector
            
            
    def __rmul__(self, other):
        
        if isinstance(other, int) or isinstance(other, float):
            vec = Vector3()
            vec[0] = other*self.vector[0]
            vec[1] = other*self.vector[1]
            vec[2] = other*self.vector[2]
            return vec
        elif isinstance(other, Matrix3):
            vec = Vector3(0,0,0)
            vec[0] = self.vector[0]*other[0][0] + self.vector[1]*other[1][0] + self.vector[2]*other[2][0]
            vec[1] = self.vector[0]*other[0][1] + self.vector[1]*other[1][1] + self.vector[2]*other[2][1]
            vec[2] = self.vector[0]*other[0][2] + self.vector[1]*other[1][2] + self.vector[2]*other[2][2]
            return vec
        else:
            raise TypeError
            
            
    def __imul__(self, other):
        
        self.vector = (self*other).vector
            
            
    def __rdiv__(self, other):
        
        if isinstance(other, int) or isinstance(other, float):
            vec = Vector3()
            vec[0] = self.vector[0]/other
            vec[1] = self.vector[1]/other
            vec[2] = self.vector[2]/other
            return vec
        else:
            raise TypeError
            
            
    def __idiv__(self, other):
        
        self.vector = (self/other).vector
        
        
    def __str__(self):
        
        strVec = [str(e) for e in self.vector]
        length = 0
        for i in range(3):
            if self.vector[i] > length:
                length = self.vector[i]
        strVec = [e.center(length+2) for e in strVec]
        final  = "/" +strVec[0]+"\\\n"
        final += "|" +strVec[1] +"|\n"
        final += "\\"+strVec[2] +"/"
        return final
        
        
        
        
class Vector4(Vector):
    
    def __init__(self, x, y, z, w=1.0):
        Vector.__init__(self, [x, y, z, w])
        
        
    def __radd__(self, other):
        
        if isinstance(other, Vector3):
            vec = Vector4()
            vec[0] = self.vector[0]+other[0]
            vec[1] = self.vector[1]+other[1]
            vec[2] = self.vector[2]+other[2]
            vec[3] = self.vector[3]+other[3]
            return vec
        else:
            raise TypeError
            
            
    def __iadd__(self, other):
        
        self.vector = (self+other).vector
            
            
    def __rmul__(self, other):
        
        if isinstance(other, int) or isinstance(other, float):
            vec = Vector4()
            vec[0] = other*self.vector[0]
            vec[1] = other*self.vector[1]
            vec[2] = other*self.vector[2]
            vec[3] = other*self.vector[3]
            return vec
        elif isinstance(other, Matrix4):
            vec = Vector4(0,0,0,0)
            vec[0] = self.vector[0]*other[0][0] + self.vector[1]*other[1][0] + self.vector[2]*other[2][0] + self.vector[3]*other[3][0]
            vec[1] = self.vector[0]*other[0][1] + self.vector[1]*other[1][1] + self.vector[2]*other[2][1] + self.vector[3]*other[3][1]
            vec[2] = self.vector[0]*other[0][2] + self.vector[1]*other[1][2] + self.vector[2]*other[2][2] + self.vector[3]*other[3][2]
            vec[3] = self.vector[0]*other[0][3] + self.vector[1]*other[1][3] + self.vector[2]*other[2][3] + self.vector[3]*other[3][3]
            return vec
        else:
            raise TypeError
            
            
    def __imul__(self, other):
        
        self.vector = (self*other).vector
            
            
    def __rdiv__(self, other):
        
        if isinstance(other, int) or isinstance(other, float):
            vec = Vector4()
            vec[0] = self.vector[0]/other
            vec[1] = self.vector[1]/other
            vec[2] = self.vector[2]/other
            vec[3] = self.vector[3]/other
            return vec
        else:
            raise TypeError
            
            
    def __idiv__(self, other):
        
        self.vector = (self/other).vector
        
        
    def __str__(self):
        
        strVec = [str(e) for e in self.vector]
        length = 0
        for i in range(4):
            if len(strVec[i]) > length:
                length = len(strVec[i])
        strVec = [e.center(length+2) for e in strVec]
        final  = "/" +strVec[0]+"\\\n"
        final += "|" +strVec[1] +"|\n"
        final += "|" +strVec[2] +"|\n"
        final += "\\"+strVec[3] +"/"
        return final
        
        
        
        
def dot(vec1, vec2):
    
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3):
        return vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2]
    elif isinstance(vec1, Vector4) and isinstance(vec2, Vector4):
        return vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2] + vec1[3]*vec2[3]
    else:
        raise TypeError
        
        
        
        
def cross(vec1, vec2):
    
    if isinstance(vec1, Vector3) and isinstance(vec2, Vector3):
        return Vector3(vec1[1]*vec2[2] - vec1[2]*vec2[1],
                       vec1[2]*vec2[0] - vec1[0]*vec2[2],
                       vec1[0]*vec2[1] - vec1[1]*vec2[0])
    else:
        raise TypeError
            
            
            
            
if __name__ == "__main__":
    '''
    mat1 = Matrix4()
    mat2 = Matrix4()
    mat3 = mat1+mat2
    print(mat3)
    vec1 = Vector4(1,1,1,1)
    print(mat3*vec1)
    rot = Matrix4Rotate(math.pi, 0, 0)
    print(rot*vec1)
    '''
    print(Matrix4Rotate(0, 0, math.pi/2))