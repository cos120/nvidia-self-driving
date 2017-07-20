"""
author: zj
file: keras_nvidia.py
time: 17-7-19
"""
import numpy as np 
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.layers import Lambda, Conv2D, Dropout, Dense, Flatten
import scipy.misc
import tensorflow as tf
import os
flags = tf.app.flags
FLAGS = tf.app.flags.FLAGS
flags.DEFINE_integer('num_epochs', 30, """ Number of training epochs """)
flags.DEFINE_integer('batch_size', 32, """ Number of batch size """)

flags.DEFINE_string('image_dir', '/home/zj/PycharmProjects/py3/nvidia-self-driving/tool/Torcs_oval_tracks_count_5/',
                    """Directory of image """)
class nvidia_self_driving():
    def __init__(self,batch_size,epochs,image_path):
        self.batch_size = batch_size
        self.epochs = epochs
        self.image_path = image_path
        self.model = self.build_model()
        self.size = len( os.listdir(self.image_path ) )

    def build_model(self):

        model = Sequential()
        model.add(Lambda(lambda x: x/127.5-1.0, input_shape=(66, 200, 3)))
        model.add(Conv2D(24, 5, 5, activation='elu', subsample=(2, 2)))
        model.add(Conv2D(36, 5, 5, activation='elu', subsample=(2, 2)))
        model.add(Conv2D(48, 5, 5, activation='elu', subsample=(2, 2)))
        model.add(Conv2D(64, 3, 3, activation='elu'))
        model.add(Conv2D(64, 3, 3, activation='elu'))
        model.add(Dropout(0.75))
        model.add(Flatten())
        model.add(Dense(100, activation='elu'))
        model.add(Dense(50, activation='elu'))
        model.add(Dense(10, activation='elu'))
        model.add(Dense(1))
        model.summary()

        return model


    def train(self):
        checkpoint = ModelCheckpoint('model-{epoch:03d}.h5',
                                     monitor='val_loss',
                                     verbose=0,
                                     save_best_only=False,
                                     mode='auto')
        self.model.compile(loss='mean_squared_error', optimizer=Adam(1e-4))
        self.model.fit_generator(self.batch_generator(),
                            steps_per_epoch=self.size // self.batch_size,
                            epochs = self.epochs,
                            max_q_size=self.batch_size * 20,
                            callbacks=[checkpoint],
                            verbose=1)

    def read_image(self,images_path):
        return np.array([scipy.misc.imread(image)[ 90:156, 60:260 ] for image in images_path])



    def batch_generator(self):
        """

        :param batch_size:
        :return: image generator
        """

        images = []
        labels = []
        for file in sorted(os.listdir(self.image_path)):
           images.append(self.image_path + file)
           labels.append(float(file.split('_')[1][:-4]))

        temp = list(zip(images,labels))

        np.random.shuffle(temp)


        images, labels = zip(*temp)
        labels = [float(i) for i in labels]
        while True:
            for index in range(self.size // self.batch_size):
                yield self.read_image(images[index * self.batch_size : (index+1) * self.batch_size]), np.array(labels[index * self.batch_size : (index+1) * self.batch_size])
            temp = list(zip(images,labels))

            np.random.shuffle(temp)


            images, labels = zip(*temp)
    
def main(_):
    epochs = FLAGS.num_epochs
    batch_size = FLAGS.batch_size
    path = FLAGS.image_dir
    self_driving = nvidia_self_driving( batch_size,epochs,path )

    self_driving.train()
if __name__ == '__main__':
    tf.app.run()

    
    