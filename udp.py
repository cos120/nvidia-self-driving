"""
author: zj
file: udp.py
time: 17-6-19 
"""
import socket
import threading
import rx
import pygame
import snakeoil3_gym
import scipy
import scipy.misc
import math
import time
import screenshot
import _thread
rate = 180 / scipy.pi

labels = []
class myThread (threading.Thread):
    def __init__(self,pad):
        threading.Thread.__init__(self)
        self.isStart = True
        self.screen = screenshot.screenshot()
        self.pad = pad
    def stop(self,stop):
        self.isStart = stop
    def run(self):
        # if(self.isStart):
        #     saveimage(self.image,self.imageIndex)
        # scipy.misc.imsave('/home/zj/Desktop/data/' + str(image.label) + '.png', image.image)
        while(self.isStart):
            labels.append(self.pad.get_axis(3)*100)
            rx.Observable.from_( [self.screen.getTorcsScreenShot()])\
            .subscribe(lambda image: scipy.misc.imsave('/home/zj/Desktop/data/' + str(image.label) + '.png', image.image))
            # images.append(screenshot.getTorcsScreenShot())

def clip(v,lo,hi):
    if v<lo: return lo
    elif v>hi: return hi
    else: return v

def drive(c,pad):
    S = c.S.d
    R = c.R.d
    target_speed = 120
    pygame.event.pump()
        # axis 0 left = -1 right = 1
        # axis 1 up = -1 down = 1
    axis_0 , axis_1 = joystick.get_axis(3),joystick.get_axis(1)
    # print(axis_0)
    if(S['speedX'] > target_speed):
        R['accel'] -= .1
    else:
        R['accel'] += .1
    # print(S['angle'] * rate)
    # print(axis_0*100)
    if(math.fabs(axis_0) >0.8):
        R['steer'] = S['angle'] /scipy.pi - 0.3*axis_0
    else:
        R['steer'] = S['angle'] /scipy.pi - 0.1*axis_0

    # clock.tick(500)
    R['steer'] = clip(R['steer'], -1, 1)

    if S['speedX'] > 50:
        R['gear'] = 2
    if S['speedX'] > 80:
        R['gear'] = 3

def saveimage(image,index):
    image = screenshot.getTorcsScreenShot()
    scipy.misc.imsave('/home/zj/Desktop/data/' + str(index) + '.png', image)
if __name__ == '__main__':

    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    clock = pygame.time.Clock()

    print(joystick.get_id())
    pygame.display.init()
    C = snakeoil3_gym.Client(p=3001)  # 3001
    imageIndex = 0
    start = time.time()
    save = myThread(joystick)
    save.start()
    for step in range(C.maxSteps,0,-1):
        C.get_servers_input()
        drive(C,joystick)
        # print(C.S.d['angle'])
        # save.setImage(screenshot.getTorcsScreenShot(),imageIndex)
        C.respond_to_server()

        imageIndex +=1
    C.shutdown()
    save.stop(False)
    print(time.time() - start)
    with open('/home/zj/Desktop/data/data.txt','w') as f:
        for l in labels:
            f.write(str(l)+'\n')
    # for image in enumerate(images):
    #     scipy.misc.imsave('/home/zj/Desktop/data/' + str(i) + '.png', image)
