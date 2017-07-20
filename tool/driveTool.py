"""
author: zj
file: driveTool.py
time: 17-6-26 
"""
import math
import threading

import pygame
import rx
import scipy
import scipy.misc
from rx.concurrency import ThreadPoolScheduler

from tool import screenshot

pool_scheduler = ThreadPoolScheduler(1)

labels = []

class ob(rx.Observer):
    def __init__(self):
        self.count = 0

    def on_next(self, value):
        # print ("save")
        scipy.misc.imsave(str(self.count).zfill(5)+'_'+value.label + '.jpg', value.image)

    def on_completed(self):
        self.count+=1
        # print("saved {}".format(self.count))

    def on_error(self, error):
        print('error')
        pass

class myThread (threading.Thread):
    def __init__(self,pad,dir):
        """
        for save
        :param pad: game pad object
        """
        super(myThread, self).__init__()
        self.isStart = True
        self.screen = screenshot.screenShotFromC()
        self.pad = pad
        self.count=0
        self.dir = dir
        self.ob = ob()
        self.setDaemon(True)
    def stop(self,stop):
        self.isStart = not stop
        while True:
            print("saved count: {}, target count: {}".format(self.ob.count, self.count))
            if (self.ob.count == self.count):
                self.screen.stop()
                break


    def run(self):
        """
        for save image and label
        format : \d+.jpg label
        :return:
        """
        while(self.isStart):
            # print (222)
            rx.Observable.from_([ self.screen.getImageAndLabel(self.pad.get_axis(3)) ])\
            .subscribe(self.ob)
            self.count += 1
            # labels.append(str(self.count) + '.jpg ' + str(self.pad.get_axis(3)))
            # rx.Observable.from_( [1])\
            # .subscribe(lambda image: print(image))
            # print(1)
        # print (1111111111111)

class driveClient():
    def __init__(self,target_speed,c,pad):
        """
        :param target_speed: speed
        :param c: client control car in torcs
        :param pad: game pad object
        """
        self.target_speed = target_speed
        self.c = c
        self.pad = pad
        # self.logSpeed()

    def clip(self, v, lo, hi):
        """
        :param v: input value
        :param lo: down boundary
        :param hi: up boundary
        :return: value in (lo,hi)
        """
        if v < lo:
            return lo
        elif v > hi:
            return hi
        else:
            return v
    def logSpeed(self):
        threading.Timer(1.0, self.logSpeed).start()
        print("speed is {}".format(self.target_speed))


    def drive(self):
        """
        for drive
        :return: null
        """
        S = self.c.S.d #server
        R = self.c.R.d #client
        pygame.event.pump()
        # axis 0 left = -1 right = 1
        # axis 1 up = -1 down = 1
        axis_0 , axis_1 = self.pad.get_axis(3),self.pad.get_axis(1)
        if(axis_1 > 0):#brake
            R['brake'] = axis_1 / 3
            self.target_speed -= math.ceil(axis_1) / 10
        elif(axis_1 < 0):
            self.target_speed -= math.floor(axis_1) / 10
        else:
            R['brake'] = 0

        if(S['speedX'] > self.target_speed): #forward speed
            R['accel'] = 0
            # print("over")
        else:
            R['accel'] += 0.01
            # print("low")


        if S['speedX'] > 50:
            R['gear'] = 2
        if S['speedX'] > 80:
            R['gear'] = 3
        if S['speedX'] > 110:
            # R['clutch'] = 1
            R['gear'] = 4
            # R['clutch'] = 0
        if S['speedX'] > 150:
            # R['clutch'] = 1
            R['gear'] = 5
            # R['clutch'] = 0
        if S['speedX'] > 200:
            # R['clutch'] = 1
            R['gear'] = 6
            R['clutch'] = 0.0
        if(math.fabs(axis_0) >0.8):# steer
            R['steer'] = S['angle'] /scipy.pi - 0.2*axis_0
        else:
            R['steer'] = S['angle'] /scipy.pi - 0.1*axis_0
        # print (axis_0)
        R['steer'] = self.clip(R['steer'], -1, 1)

        # R['gear'] = 1

    def dataDrive(self,angle):
        S = self.c.S.d  # server
        R = self.c.R.d  # client

        if (S['speedX'] > self.target_speed):  # forward speed
            R['accel'] -= 0.005
            # print("over")
        else:
            R['accel'] += 0.005
            # print("low")

            R[ 'gear' ] = 1
        if S['speedX'] > 50:
            R['gear'] = 2
        if S['speedX'] > 80:
            R['gear'] = 3
        if S['speedX'] > 110:
            # R['clutch'] = 1
            R['gear'] = 4
            # R['clutch'] = 0
        if S['speedX'] > 150:
            # R['clutch'] = 1
            R['gear'] = 5
            # R['clutch'] = 0
        if S['speedX'] > 200:
            # R['clutch'] = 1
            R['gear'] = 6
            R['clutch'] = 0.0

        if (math.fabs(angle) > 0.8):  # steer
            R[ 'steer' ] = S[ 'angle' ] / scipy.pi - 0.2 * angle
        else:
            R[ 'steer' ] = S[ 'angle' ] / scipy.pi - 0.1 * angle
        R[ 'steer' ] = self.clip(R[ 'steer' ], -1, 1)


        # R['steer'] = self.clip(R['steer'], -1, 1)
    def resetDrive(self):
        S = self.c.S.d  # server
        R = self.c.R.d  # client

        R[ 'accel' ] = 0
        R[ 'steer' ] = S[ 'angle' ] / scipy.pi