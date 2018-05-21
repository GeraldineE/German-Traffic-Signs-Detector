#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 11:01:24 2018

@author: jorgejohnson


"""

from filemanager import FileManager
from imagemanager import ImageTools
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import resources as lr
import os

class LogisticImageTrainer:
    """this class support file system operations."""        

    def __init__(self):
        self.__datTrain = []
        self.__datTest = []
        self.__lblTrain = []
        self.__lblTest = []
        self.__tempoDataSet = None
        self.__tempoLabelSet =None
    
        self.__model = None
        
        self.__CLassDic = FileManager().loadClassIdDictionary()

    def __factorModel(self):
        """factor a multinomial Logistic Regression Image Trainer
        """
        self.__model = LogisticRegression(
                 multi_class='multinomial',solver='lbfgs'
                )
        
    def trainSetIsLoaded(self): 
        """get if there is a set of images loaded
        """
        return len(self.__datTrain) > 0

    def modelTrained(self): 
        """get if the model is trained
        """
        return not self.__model is None

    def __deleteSets(self):
        """delete old data.
        """
        if not self.__tempoDataSet is None: 
            del self.__tempoDataSet
        if not self.__tempoLabelSet is None: 
            del self.__tempoLabelSet

    def __scoreTrainSet(self):
        """get the score for a trained data set
        """
        return self.__model.score(
                self.__datTrain,self.__lblTrain
                )

    def __fitTrainSet(self):
        """fit a trained data set
        """
        return self.__model.fit(
                self.__datTrain,self.__lblTrain
                )

    def __scoreTestSet(self):
        """get the score for a test data set
        """
        return self.__model.score(
                self.__datTest,self.__lblTest
                )

    def trainSetSize(self): 
        """get the number of images in a train dataset
        """
        return len(self.__datTrain)
    
    def testSetSize(self): 
        """get the number of images in a test dataset
        """
        return len(self.__datTest)
 
    def saveModel(self, filename):
        """persist a trained model to the file system to posterior usage
        """
        joblib.dump(self.__model, filename)
    
    def __loadSet(self,path):
        """Given a directory with images, load all images as set.
           Set can be use later as a train or test set
        """
        self.__deleteSets()
        self.__tempoDataSet = []
        self.__tempoLabelSet = []
        fm = FileManager()
        path = fm.adjustDirectoryPath(path)
        imageList = fm.folderFileListOfImages(path)
        it = ImageTools()
        for filename in imageList:
            imgArray = it.getImageArray(path, filename)
            parts = filename.split('_')
            IdClass = int(parts[0])
            self.__tempoDataSet.append(imgArray)
            self.__tempoLabelSet.append(IdClass)

    def loadTrainSet(self,path): 
        """ Given a directory containing images, this method load a new set
            of images to be trained and return the length of the train set
        """
        self.__loadSet(path)
        self.__datTrain = self.__tempoDataSet
        self.__lblTrain = self.__tempoLabelSet
        return len(self.__datTrain)

    def loadTestSet(self,path): 
        """ Given a directory containing images, this method load a new set
            of images to be tested and return the length of the test set.
            A persisted model should be loaded using the loadModel method 
            in order to work
        """
        self.__loadSet(path)
        self.__datTest = self.__tempoDataSet
        self.__lblTest = self.__tempoLabelSet
        return len(self.__datTest)

    def train(self):
        """This funtion assume a preloaded train set; 
           You can use the loadTrainSet() method to do this.
        """
        self.__factorModel()
        self.__model.fit(self.__datTrain,self.__lblTrain)
        return self.__scoreTrainSet()

    def test(self):
        """This funtion assume a trained model in order to be able to testing
        """         
        return self.__scoreTestSet()

    def infer(self, path, filename):
        """Allows to infer on an image, based on a saved model
        """                
        fm = FileManager()
        path = fm.adjustDirectoryPath(path)

        it = ImageTools()
        newfile=it.resize(path,filename,
                          lr.IMAGE_RESIZE_ROWS,lr.IMAGE_RESIZE_COLS)
        imgArray = []
        imgArray.append(it.getImageArray(path, newfile))
        os.remove(path+newfile)
        prediction = str(self.__model.predict(imgArray)[0])
        description = self.__CLassDic[prediction]
        return prediction,description
    
    def loadModel(self, persistedModelFileName):
        """This funtion load a persisted model, to test, or make inference
        """         
        self.__model  = joblib.load(persistedModelFileName)
