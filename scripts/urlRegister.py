reg = """Windows Registry Editor Version 5.00

[-HKEY_CLASSES_ROOT\razor]

[HKEY_CLASSES_ROOT\razor]
@=""
"URL Protocol"=""

[HKEY_CLASSES_ROOT\razor\shell]
@=""

[HKEY_CLASSES_ROOT\razor\shell\open]

[HKEY_CLASSES_ROOT\razor\shell\open\command]
@="PLACEHOLDER %1"
"""
import os

def write(exe, loc):
    with open(loc, 'w+') as file:
        file.write(reg.replace('PLACEHOLDER', exe))
