"""
author: zj
file: udp.py
time: 17-6-19 
"""
import threading
import rx
import pygame
from rx.concurrency import ThreadPoolScheduler
import pygame
import snakeoil3_gym
import scipy
import scipy.misc
import math
import time
import screenshot
import tensorflow as tf
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))

labels = []

flags = tf.app.flags
FLAGS = tf.app.flags.FLAGS


flags.DEFINE_string('save_dir','data',"""Directory under which to place image and label""")
flags.DEFINE_integer('target_speed','120',"""target speed""")

root_dir = os.path.dirname(__file__)
save_dir = FLAGS.save_dir
global target_speed

class ob(rx.Observer):
    def __init__(self):
        self.count = 0

    def on_next(self, value):
        scipy.misc.imsave(str(value.label) + '.jpg', value.image)

    def on_completed(self):
        self.count+=1

    def on_error(self, error):
        pass

class myThread (threading.Thread):
    def __init__(self,pad,dir):
        """
        for save
        :param pad: game pad object
        """
        threading.Thread.__init__(self)
        self.isStart = True
        self.screen = screenshot.screenShotFromC()
        self.pad = pad
        self.count=0
        self.dir = dir
        self.ob = ob()

    def stop(self,stop):
        self.isStart = not stop
        while True:
            print("{}  {}".format(self.ob.count, self.count))
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
            rx.Observable.from_( [self.screen.getImage()])\
            .subscribe(self.ob)
            self.count += 1
            labels.append(str(self.count) + '.jpg ' + str(self.pad.get_axis(3) * 100))
            # rx.Observable.from_( [1])\
            # .subscribe(lambda image: print(image))
            # print(1)

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
        self.logSpeed()
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
            R['accel'] -= .1
        else:
            R['accel'] += .1


        if(math.fabs(axis_0) >0.8):# steer
            R['steer'] = S['angle'] /scipy.pi - 0.3*axis_0
        else:
            R['steer'] = S['angle'] /scipy.pi - 0.1*axis_0
        R['steer'] = self.clip(R['steer'], -1, 1)

        R['gear'] = 1
        if S['speedX'] > 50:
            R['gear'] = 2
        if S['speedX'] > 80:
            R['gear'] = 3
        if S['speedX'] > 110:
            R['clutch'] = 1
            R['gear'] = 4
            R['clutch'] = 0
        if S['speedX'] > 150:
            R['clutch'] = 1
            R['gear'] = 5
            R['clutch'] = 0
        if S['speedX'] > 200:
            R['clutch'] = 1
            R['gear'] = 6
            R['clutch'] = 0.0

def main(_):
    """
    main function
    :param _: null
    :return: null
    """
    #init
    path = root_dir + '/' + save_dir
    print("save in {}, target_speed {}".format(path,FLAGS.target_speed))
    if (os.path.exists(path)):
        print('directory existed, run again')
        sys.exit()
    else:
        os.mkdir(root_dir + '/' + save_dir)

    os.chdir(path)
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    pygame.display.init()

    #variable
    C = snakeoil3_gym.Client(p=3001)  # 3001
    driver = driveClient(FLAGS.target_speed,C,joystick)
    start = time.time()
    save = myThread(joystick,path)

    #save image
    save.start()

    #control fragment
    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        driver.drive()
        C.respond_to_server()
    C.shutdown()

    print(time.time() - start)
    with open(path + '/' + 'data.txt', 'w') as f:
        for l in labels:
            f.write(str(l) + '\n')

    save.stop(True)
    # save.is

    sys.exit()
if __name__ == '__main__':
    tf.app.run()


