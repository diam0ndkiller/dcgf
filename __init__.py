#!/bin/python3

from . import cmd

try:
	import pip
	import pygame
	import datetime
	import colorama
	import numpy
except:
	cmd.install_python_module("pip")
	cmd.install_python_module("pygame")
	cmd.install_python_module("datetime")
	cmd.install_python_module("colorama")
	cmd.install_python_module("numpy")

from .surface import *
from .files import *
from .logger import *
