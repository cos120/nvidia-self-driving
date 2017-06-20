#!/usr/bin/python3
"""
author: zj
file: screenshot.py
time: 17-6-20 
"""
import pyscreenshot
import os
import subprocess as sp
import re
import time

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
    s = screenshot()
    a = s.getTorcsScreenShot()
    ims = []
    for i in range(10):
        ims.append(s.getTorcsScreenShot())
    print(time.time() - start_time)

    # im.show()