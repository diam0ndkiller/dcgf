from . import cmd

try:
    import pip
    import pygame
    import datetime
    import colorama
    import numpy
except:
    print("Auto import: ")
    cmd.import_python_module("pip")
    cmd.import_python_module("pygame")
    cmd.import_python_module("datetime")
    cmd.import_python_module("colorama")
    cmd.import_python_module("numpy")

from .surface import *
from .files import *
from .logger import *
