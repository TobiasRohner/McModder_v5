# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image



BASEPATH = os.path.dirname(sys.argv[0])




def transparency(texturePath):
    """return the different alpha values used in the texture by
    loading the texture, iterating over the data, save the alpha value and deleting all duplicates"""
    col = list(Image.open(texturePath, "r").getdata())
    if len(col[0]) < 4:
        colors = [255]
    else:
        colors = list(set([a for r,g,b,a in list(Image.open(texturePath, "r").getdata())]))
    return colors
    
    
    
    
    
    
    
if __name__ == "__main__":
    
    print(transparency(r"E:\Programmieren\Python\McModder_v5\assets\textures\blocks/cactus_bottom.png"))