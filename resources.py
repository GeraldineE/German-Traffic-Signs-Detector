#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 11:07:23 2018

@author: jorgejohnson
"""

DATA_ORIGIN_PATH        = 'http://benchmark.ini.rub.de/Dataset_GTSDB/'
DATA_ORIGIN_FILENAME    = 'FullIJCNN2013.zip'
DATA_PATH               = 'FullIJCNN2013/'
LOCAL_IMAGE_PATH        = 'images/'
LOCAL_IMAGE_FILE_PATH   = 'images/FullIJCNN2013/'
LOCAL_IMAGE_TRAIN_PATH  = 'images/train/'
LOCAL_IMAGE_TEST_PATH   = 'images/test/'
LOCAL_SAVED_MODEL_LR    = 'models/model-LR/saved/LRmodel.pkl'
DOWNLOAD_COMPLETE       = '== Download complete!'
ERROR                   = 'AN ERROR OCURRED! '
NOT_IMPLEMENTED_YET     = 'this feature is not implemented on this version'
CMD_ARG_LR              = 'lr'
CMD_ARG_TF              = 'tf'
CMD_ARG_LN              = 'ln'
OVERWRITE_ON_DOWNLOAD   = False
IMAGE_RESIZE_ROWS       = 32
IMAGE_RESIZE_COLS       = 32
PERCENT_FOR_TESTING     = 0.2
APP_TITLE               = "MiniTools for Machine Learning (MTML) -- jorge johnson-- version 0.1"