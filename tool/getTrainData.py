"""
author: zj
file: getTrainData.py
time: 17-6-26
"""
import os
import signal
import sys
import time

import pygame
import tensorflow as tf

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from tool import snakeoil3_gym, driveTool

flags = tf.app.flags
FLAGS = tf.app.flags.FLAGS

flags.DEFINE_integer('target_speed', '120', """target speed""")
flags.DEFINE_string(
    'traindata_save_dir',
    'Torcs_oval',
    """Relative directory under workdir/demos which to generate train data""")
flags.DEFINE_integer(
    'torcs_loop',
    '2',
    """play torcs for different tracks, once you select, you have to finish""")

# drive tool variable declare


def main(_):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    torcs_loop = FLAGS.torcs_loop

    print("root_dir:  {}".format(root_dir))
    traindata_save_dir = FLAGS.traindata_save_dir
    path = root_dir + '/' + traindata_save_dir + \
        '_tracks_count_' + str(torcs_loop)
    print(path)
    print("save in {}, target_speed {}".format(path, FLAGS.target_speed))
    if (os.path.exists(path)):
        print('directory existed, run again')
        sys.exit()
    else:
        os.mkdir(path)

    os.chdir(path)
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    pygame.display.init()
    # variable
    C = snakeoil3_gym.Client(p=3001)  # 3001
    driver = driveTool.driveClient(FLAGS.target_speed, C, joystick)
    save = driveTool.myThread(joystick, path)

    # save image
    save.start()

    for i in range(torcs_loop):
        while C.get_servers_input() != -1:
            driver.drive()
            C.respond_to_server()
        print("you have finish {} loop".format(i + 1))
        if i != torcs_loop - 1:

            C.setup_connection()
            driver.resetDrive()
    C.shutdown()

    # with open(path + '/' + 'data.txt', 'w') as f:
    #     for l in tool.labels:
    #         f.write(str(l) + '\n')

    save.stop(True)
    time.sleep(1)
    try:
        sys.exit()  # this always raises SystemExit
    except SystemExit:
        print("sys.exit() worked as expected")
        os.kill(os.getpid(), signal.SIGTERM)
    except BaseException:
        print("Something went horribly wrong")  #


if __name__ == '__main__':
    tf.app.run()
