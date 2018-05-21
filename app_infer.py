#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 07:05:06 2018

@author: jorgejohnson
"""
import click
import app_LR
import resources as lr

def infer(model, directory):
    if model == lr.CMD_ARG_LR:
        app_LR.infer(model, directory)
    elif model == lr.CMD_ARG_TF:
        click.echo(lr.NOT_IMPLEMENTED_YET)
    elif model == lr.CMD_ARG_LN:
        click.echo(lr.NOT_IMPLEMENTED_YET)