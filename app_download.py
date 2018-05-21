#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 06:34:26 2018

@author: jorgejohnson

This module manage the download of a remote file of images, and the extraction
of only images for classification.

Images are located in test and train directories usin parameter 
PERCENT_FOR_TESTING. This parameter can be found in file resources.py

"""

import click
from filemanager import FileManager
import resources as lr
import os

REMOTE_ORIGIN = lr.DATA_ORIGIN_PATH+lr.DATA_ORIGIN_FILENAME
IMAGE_FILE = lr.LOCAL_IMAGE_PATH + lr.DATA_ORIGIN_FILENAME

def downloadFile():
    """ get image file from INI web site"""
    click.clear()
    click.echo()
    click.echo(lr.APP_TITLE)

    doDownload = True
    fm = FileManager()
    if os.path.exists(IMAGE_FILE) and not lr.OVERWRITE_ON_DOWNLOAD:
           doDownload = False
           click.echo(":: VERY IMPORTANT:")
           click.echo(":: %s already exist." 
                      "\n:: Download not allowed because a file already exist!"
                      "\n   if you want to overwrite downloaded files, adjust "
                      "\n   option OVERWRITE_ON_DOWNLOAD in resources file!"
                      %IMAGE_FILE)

    if doDownload:
        print('\n== downloading DB: ',REMOTE_ORIGIN)
        fm.downloadSet(REMOTE_ORIGIN,lr.IMAGE_PATH)
    
    print('.... procceding with extraction... ')
    fm.extractFoldersFromZipFile(IMAGE_FILE,lr.LOCAL_IMAGE_PATH)    
    
    print('.... RANDOM SHUFFLING to train and test directories... ')
    ctrain, ctest = fm.splitDirectoryWithShuffle(
                        lr.LOCAL_IMAGE_FILE_PATH, 
                        lr.LOCAL_IMAGE_TRAIN_PATH, 
                        lr.LOCAL_IMAGE_TEST_PATH, lr.PERCENT_FOR_TESTING)
                
    click.echo(".... %d unzied, converted, and shuffed files for train." % ctrain)
    click.echo(".... %d unzied, converted, and shuffed files for test." % ctest)
    percenttest = lr.PERCENT_FOR_TESTING*100.0
    click.echo(".... a %%%3.2f of the files were reserved for testing purposes." %percenttest)
    click.echo(".... (PERCENT_FOR_TESTING can be changed in 'resources.py' file).")
    click.echo("-- Done --")