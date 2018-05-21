#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:51:03 2018

@author: jorgejohnson
"""

import click
from logistictrainer import LogisticImageTrainer
import resources as lr
from filemanager import FileManager
from imagemanager import ImageTools
import os

def train(model, directory):
    """  train a set of images for classification"""
    click.clear()
    click.echo()
    click.echo(lr.APP_TITLE)

    if os.path.exists(directory):
        click.echo("== TRAINING...")
        logTrainer = LogisticImageTrainer()
        click.echo("== reading data from %s..." % directory)
        recs = logTrainer.loadTrainSet(directory)
        click.echo("== %i files loaded for training" % recs)
        if logTrainer.trainSetIsLoaded():
            acc = logTrainer.train()*100.0
            logTrainer.saveModel(lr.LOCAL_SAVED_MODEL_LR)
            click.echo('== Model Trained')
            click.echo("== Model saved to '%s'." % lr.LOCAL_SAVED_MODEL_LR)
            click.echo('== Model shows a %3.2f%% accuracy for trained data' % acc)
        else:
            print("== Training set not loaded")
    else:
        click.echo(':: Training image directory \'%s\' do not exist' % directory)
        click.echo(':: Please download a set of images, or copy a \n:: zip file with images directly on image directory')
        click.echo()

def test(model, directory):
    """  test a set of images for classification"""
    click.clear()
    click.echo()
    click.echo(lr.APP_TITLE)

    if os.path.exists(directory):
        logTrainer = LogisticImageTrainer()
        if os.path.exists(lr.LOCAL_SAVED_MODEL_LR):
            logTrainer.loadModel(lr.LOCAL_SAVED_MODEL_LR)
            click.echo("== TESTING...")
            print("== model", lr.LOCAL_SAVED_MODEL_LR, "loaded")
            click.echo("== reading data from %s..." % directory)
            recs = logTrainer.loadTestSet(directory)
            click.echo("== %i files loaded for testing" % recs)
            acc = logTrainer.test()*100.0
            click.echo('Model shows a %3.2f%% accuracy for tested data' % acc)
        else:
            print("The requied persisted model", lr.LOCAL_SAVED_MODEL_LR, "do not exist")
    else:
        click.echo(':: Testing image directory \'%s\' do not exist' % directory)
        click.echo()
        

def infer(model, directory):
    """  infer a set of images for classification"""
    click.clear()
    click.echo()
    click.echo(lr.APP_TITLE)

    fm = FileManager()
    directory = fm.adjustDirectoryPath(directory)
    logTrainer = LogisticImageTrainer()
    if os.path.exists(lr.LOCAL_SAVED_MODEL_LR):
        logTrainer.loadModel(lr.LOCAL_SAVED_MODEL_LR)
        print("== model", lr.LOCAL_SAVED_MODEL_LR, "loaded")
        it = ImageTools()
        imageList = fm.folderFileListOfImages(directory)
        if len(imageList) > 0:
            for filename in imageList:
                code,descr = logTrainer.infer(directory,filename)
                out = "== FILE {0:s} Class {1:s}->{2:s}".format(filename, code ,descr)
                click.echo(out)
            for filename in imageList:
                code,descr = logTrainer.infer(directory,filename)
                
                out = "== {0:s} -> {1:s}".format( code ,descr)
                it.showImage(directory+filename,out)
        else:
            click.echo(':: No files in \'%s\' directory' % directory)
    else:
        print("== model", lr.LOCAL_SAVED_MODEL_LR, "required for predictions do not exist!")
        

