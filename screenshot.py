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


class screenshot():
    def __init__(self):
        self.imageIndex = 0;
        self.bbox = self.getTorcsBbox()

    def getTorcsBbox(self):
        x = sp.check_output('xwininfo -name /usr/local/lib/torcs/torcs-bin', shell=True)
        x = x.decode('utf-8')
        # print(x)
        x = x[64:]
        print(x)
        x = re.findall('[\d]+', x)
        print(x)
        Xposition = int(x[0])
        Yposition = int(x[1])
        Xsize = int(x[4])
        Ysize = int(x[5])
        print(1)
        return (Xposition,Yposition,Xposition+Xsize,Yposition+Ysize)


    def getTorcsScreenShot(self):
        # print(2)
        self.imageIndex+=1
        # return [pyscreenshot.grab(bbox=self.bbox,backend='scrot'),self.imageIndex]
        return imageAndLabel(pyscreenshot.grab(bbox=self.bbox,backend='scrot'),self.imageIndex)
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