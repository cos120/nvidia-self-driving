#!/usr/bin/python3
"""
author: zj
file: screenshot.py
time: 17-6-20 
"""
from ctypes import cdll
from ctypes import c_uint8
import numpy as np
import time
import sys
import os
from numpy.ctypeslib import ndpointer
import scipy.misc
import matplotlib.pyplot as plt
print(__file__)
dir_path = os.path.dirname(os.path.realpath(__file__))
lib = cdll.LoadLibrary(dir_path+'/TorcsScreenShot.so')
lib.getScreenshot.restype = ndpointer(dtype=c_uint8, shape=(480,640,3))

class screenShotFromC(object):
    def __init__(self):
        self.torcsScreenShot = lib.getScreenshotTool()
        self.reserveScreenShotFlag()

    def reserveScreenShotFlag(self):
        lib.reserveScreenShotFlag(self.torcsScreenShot)

    def getImageAndLabel(self, angle):
        image = np.flipud(lib.getScreenshot(self.torcsScreenShot))
        image = scipy.misc.imresize(image,[240,320])
        return imageAndLabel(image,str(angle))

    def getImage(self):
        image = np.flipud(lib.getScreenshot(self.torcsScreenShot))
        image = scipy.misc.imresize(image, [ 240, 320 ])
        return image
    def stop(self):
        lib.stopTorcsImageTool()


class imageAndLabel():
    def __init__(self,image , label):
        self.image = image
        self.label = label

if __name__ == '__main__':
    pass
    # path = '/home/zj/PycharmProjects/py2/DeepNuc-master/demos/Torcs_oval_tracks_count_1/347_0.0.jpg'
    # image = scipy.misc.imread(path)
    # image1 = scipy.misc.imread(path)
    # aa = 70
    # image = image[ 90:156, 60:260 ]
    # fig, (ax, xx) = plt.subplots(2, 1, sharey=False)
    # # im = ax.imshow(r_input_img, cmap=plt.cm.Reds, interpolation='nearest')
    # im = ax.imshow(image)
    # # image1 = scipy.misc.imresize(image,(66,200))
    # im = xx.imshow(image1)
    # # plt.imshow(image)
    # plt.show()

    # start_time = time.time()
    # # s = screenshot()
    # # a = s.getTorcsScreenShot()
    # ims = []
    # s = screenShotFromC()
    # for i in range(100):
    #     # ims.append(s.getTorcsScreenShot())
    #     a = s.getImage()
    #
    # print(time.time() - start_time)
    #
    # # s.reserveScreenShotFlag()
    #
    # # b = np.frombuffer(a)
    # plt.imshow(a)
    # plt.show()

    # print(s.getImage())
    # im.show()