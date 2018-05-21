#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 10:58:23 2018

@author: jorgejohnson

"""

import urllib.request
from pathlib import Path
from imagemanager import ImageTools
from random import shuffle
import resources as lres
import os

EXTLENGHT = 4
EXT_IMAGE = ".ppm"
class FileManager:
    """this class support file system operations."""        

    def subfolderList(self, folderPath):
        """get a list of subfolders inside a folder."""        
        p = Path(folderPath)
        return [f.name for f in p.iterdir() if f.is_dir()]

    def folderFileListOfImages(self, folderPath):
        """get a list of ppm image files in a folder."""        
        p = Path(folderPath)
        return [f.name for f in p.iterdir() if (f.is_file() and f.name[-EXTLENGHT:] == EXT_IMAGE)]
        
    def __downloadwebFile(self,url, dest):
        """download a web file to a destination directory."""        
        file_name = url.split('/')[-1]
        u = urllib.request.urlopen(url)
        f = open(dest+file_name, 'wb')
        meta = u.info()
        file_size = int(meta["Content-Length"])
        print ("Downloading: %s %s bytes" % (file_name, file_size))
    
        file_size_dl = 0
        block_sz = int(file_size*0.005)
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
    
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%] - " % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print (status)
    
        f.close()
    
    def downloadSet(self,url,dest):
        """public method to download a web file to a destination directory."""        
        self.__downloadwebFile(url,dest)

    def extractFoldersFromZipFile(self,localZipFile, targetDir):
        """extract from zipfile only the folders with image files."""        
        import zipfile
        with zipfile.ZipFile(localZipFile,'r') as zfileMgr:
            for f in zfileMgr.namelist():
                if f[-1] == "/" or f.count("/") > 1 or f.count('.txt') > 0:
                   zfileMgr.extract(f,targetDir)

    def adjustDirectoryPath(self, path):
        """Add a slash as the final character of a plath.
        """
        if not path.endswith('/'):
           path+='/'
        return path
    
    def splitDirectoryWithShuffle(self,sourcepath, trainpath, testpath, testpercent):        
        sourcepath = self.adjustDirectoryPath(sourcepath)
        trainpath = self.adjustDirectoryPath(trainpath)
        testpath = self.adjustDirectoryPath(testpath)
        if not os.path.exists(trainpath):
            os.makedirs(trainpath)
        if not os.path.exists(testpath):
            os.makedirs(testpath)
        fm = FileManager()
        it = ImageTools()
        folderList = fm.subfolderList(sourcepath)
        ctrain=0
        ctest=0
        for classID in folderList:
            imageList = fm.folderFileListOfImages(sourcepath+classID+'/')
            shuffle(imageList)
            ntrain = round(len(imageList) * (1-testpercent))
            ntest = len(imageList) - ntrain
            for f in imageList:
                newfilename=it.resize(
                                sourcepath+classID+'/',f, 
                                lres.IMAGE_RESIZE_ROWS,lres.IMAGE_RESIZE_COLS)
                if ntrain > 0:
                    ctrain+=1
                    ntrain -= 1
                    os.rename(sourcepath+classID+'/'+newfilename, trainpath+classID+'_'+newfilename)
                elif ntest > 0:
                    ctest+=1
                    os.rename(sourcepath+classID+'/'+newfilename, testpath+classID+'_'+newfilename)
                    ntest -= 1
        return ctrain,ctest
    
    import ast

    def loadClassIdDictionary(self):
        Dic = {}
        with open('ClassId.txt', 'r') as f:
            codeList = f.read().split('\n')
            for item in codeList :
                parts = item.split('=')
                Dic[parts[0].strip()] = parts[1].strip()
        return Dic
