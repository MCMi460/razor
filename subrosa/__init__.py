# MCMi460 on Github
# Track Handling, Sub-Rosa

# Version
version = 1.01

# Imports
import os, sys, random, traceback, threading, time, json, math, webbrowser, inspect
import youtube_dl
from sdl2 import sdlmixer as mix
#import pypresence
import PIL.Image
import requests
if os.name == 'nt':
    import pyreadline3
else:
    import readline

# Source files
from .files import *
fd = FileSystem()
from .audio import *
from .sources import *
from .console import *
