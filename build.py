from distutils.core import setup
import py2exe
import sys
import cv2
import numpy
import pyautogui
import mediapipe
sys.setrecursionlimit(5000)

sys.argv.append('py2exe')
includes = ['cv2', 'numpy', 'mediapipe', 'pyautogui',"start","matplotlib"]
excludes = ['_gtkagg', '_tkagg', 'curses', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs' ]

packages = []
dll_excludes = []

setup(
     options = {"py2exe": {
                          "packages": ['entities','core'],
                          "includes":includes,
                          "excludes":excludes,
                          'bundle_files': 3
                         }
              },
    console=['main.py']
)