#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 18:03:41 2018

@author: jorgejohnson


This is the main program controlled using click library
possible commands are:
    download
    infer for infering on a set of images
    train for training a set of images
    test  for testing a set of images
"""
import click
import app_infer
import app_train
import app_test
import app_download

@click.group()
def groupDownload():
    pass

@groupDownload.command()
def download():
    """ get image file from INI web site"""
    app_download.downloadFile()

@click.group()
def groupTrainTestInfer():
    pass

@groupTrainTestInfer.command()
@click.option('--model', '-m',type=click.Choice(['lr', 'tf' , 'ln']))
@click.option('--directory','-d')
def infer(model, directory):
    """ infer files based on a method"""
    app_infer.infer(model,directory)


@groupTrainTestInfer.command()
@click.option('--model', '-m',type=click.Choice(['lr', 'tf' , 'ln']))
@click.option('--directory','-d')
def train(model, directory):
    """ train a model based on a method"""
    app_train.train(model,directory)


@groupTrainTestInfer.command()
@click.option('--model', '-m',type=click.Choice(['lr', 'tf' , 'ln']))
@click.option('--directory','-d')
def test(model, directory):
    """  test a set of images for classification"""
    app_test.test(model,directory)
        
cli = click.CommandCollection(sources=[groupDownload, groupTrainTestInfer])
if __name__ == '__main__':
    cli()
