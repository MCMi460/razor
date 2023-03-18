# MCMi460 on Github
# Track Handling, Sub-Rosa

# Version
version = 0.3

# Imports
import os, sys, random, traceback, threading, time, json, copy
import youtube_dl
import vlc
import pypresence
if os.name == 'nt':
    import pyreadline3
else:
    import readline

# Source files
from .files import *
fd = FileSystem()
from .sources import *
from .console import *
