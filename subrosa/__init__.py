# MCMi460 on Github
# Track Handling, Sub-Rosa

# Version
version = 0.3

# Imports
import os, sys, random, traceback, threading, time, json, math, webbrowser
import youtube_dl
#import pypresence
import PIL.Image
import requests
if os.name == 'nt':
    os.add_dll_directory(os.getcwd())
    import pyreadline3
else:
    import readline
import vlc

# Source files
from .files import *
fd = FileSystem()
from .sources import *
from .console import *
