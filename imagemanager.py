#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 10:58:23 2018

@author: jorgejohnson

"""

import numpy
import struct
from PIL import Image, ImageTk, ImageEnhance
import tkinter as tk

class ImageTools:
    """this class support image operationss."""        
    def getImageHeader(self,path, filename):
        img = open(path+filename, 'rb')
        attr=[]
        n = 4
        c = img.read(1)
        while n > 0:
            data=''
            while ascii(c) != 0x20 and ascii(c) != 0x0A and ascii(c) != 0x0C:
                data=c + data  
                c = img.read(1)
            [data]+c  
            n-=1
        return attr
    
    def getImageArray(self,path, filename):
        """get an image and convert the image in a binary array."""        

        image = open(path+filename, 'rb')
        metadata = image.readline().split() 
        if len(metadata) == 4: #sometimes header attribute separator is 0x32
            rows = int(metadata[1])
            cols = int(metadata[2])
        else:
            #sometimes header attribute separator is 0x0A in some positions
            metadata = image.readline().split() 
            rows = int(metadata[0])
            cols = int(metadata[1])
            metadata = image.readline().split()

        imageArray = numpy.zeros(rows*cols,dtype=numpy.uint8)
        for i in range(rows*cols):
            pixel = image.read(1)
            pixel = struct.unpack('B', pixel)[0]
            imageArray[i] = pixel

        image.close()
        return imageArray
    
    def resize(self, path, filename, rows, cols):
        """change the size of an image to a new row,col desired size.
           The function gives you the new of the new image in file system.
        """       
        newFileName = str(rows)+'x'+str(cols)+'_'+filename
        img = Image.open(path+filename)
        new_img = img.resize((rows,cols))
        new_img.save(path+newFileName,'ppm')
        return newFileName


    def showImage(self, path, label):
        """show an image with a label
        """       
        win = tk.Tk()
        win.geometry("400x100")
        win.title("ClasID="+label)
        img = ImageTk.PhotoImage(file = path)
        panel = tk.Label(win, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")
        win.mainloop()
        return