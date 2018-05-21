#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 07:09:48 2018

@author: jorgejohnson
"""
import click
import app_LR
import resources as lr

def train(model, directory):
    """  train a set of images for classification"""
    if model == lr.CMD_ARG_LR:
        app_LR.train(model, directory)
    elif model == lr.CMD_ARG_TF:
        click.echo(lr.NOT_IMPLEMENTED_YET)
    elif model == lr.CMD_ARG_LN:
        click.echo(lr.NOT_IMPLEMENTED_YET)