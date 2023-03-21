# MCMi460 on Github
# Track Handling, Sub-Rosa

# Version
version = 1.0

# Imports
import os, sys, random, traceback, threading, time, json, math, webbrowser
import youtube_dl
#import pypresence
import PIL.Image
import requests
if os.name == 'nt':
    import pyreadline3
else:
    import readline

# Source files
from .files import *
# Post-files import
if os.name == 'nt':
    os.add_dll_directory(os.getcwd())
    #os.add_dll_directory(getPath('VLC'))
import vlc
# Continue
fd = FileSystem()
from .sources import *
from .console import *
