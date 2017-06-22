#!/usr/bin/python3
"""
author: zj
file: screenshot.py
time: 17-6-20 
"""
import pyscreenshot
from ctypes import cdll
from ctypes import c_uint8
import subprocess as sp
import re
import numpy as np
import time
from numpy.ctypeslib import ndpointer
import scipy.misc
import matplotlib.pyplot as plt
lib = cdll.LoadLibrary('screenShotTool/TorcsScreenShot.so')
lib.getScreenshot.restype = ndpointer(dtype=c_uint8, shape=(480,640,3))

class screenShotFromC(object):
    def __init__(self):
        self.torcsScreenShot = lib.getScreenshotTool()
        self.reserveScreenShotFlag()
        self.imageIndex = 0

    def reserveScreenShotFlag(self):
        lib.reserveScreenShotFlag(self.torcsScreenShot)

    def getImage(self):
        self.imageIndex += 1
        return imageAndLabel(np.flipud(lib.getScreenshot(self.torcsScreenShot)),self.imageIndex)

    def stop(self):
        lib.stopTorcsImageTool()


class imageAndLabel():
    def __init__(self,image , label):
        self.image = image
        self.label = label

if __name__ == '__main__':
    start_time = time.time()
    # s = screenshot()
    # a = s.getTorcsScreenShot()
    ims = []
    s = screenShotFromC()
    for i in range(100):
        # ims.append(s.getTorcsScreenShot())
        a = s.getImage()

    print(time.time() - start_time)

    # s.reserveScreenShotFlag()

    # b = np.frombuffer(a)
    plt.imshow(a)
    plt.show()

    # print(s.getImage())
    # im.show()