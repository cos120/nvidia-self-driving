"""
author: zj
file: visual_back_prop.py
time: 17-7-20
"""
import numpy as np
from keras.models import load_model
import tensorflow as tf
import scipy.misc
import os

flags = tf.app.flags
FLAGS = tf.app.flags.FLAGS
flags.DEFINE_string('model_dir', '/home/zj/PycharmProjects/py3/nvidia-self-driving/model-029.h5', """ Directory of model """)
flags.DEFINE_string('result_dir', '/home/zj/Desktop/e/', """ Directory of result """)

flags.DEFINE_string('image_dir', '/home/zj/Desktop/a/',
                    """Directory of image """)
class VisualBackprop():
    def __init__(self, model_path,image_set_path,result_path):
        """

        :param model: keras model
        :param image_set_path: path for visualize image set
        :param result_path: path for result
        """
        self.model = load_model(model_path)
        self.keras_layers = [
            layer for layer in self.model.layers if 'conv' in layer.name][::-1]
        self.conv_layers = [layer.output for layer in self.keras_layers]
        self.paras = [layer.get_weights() for layer in self.keras_layers]
        self.weights = []
        self.bias = []
        self.assign_ops = []
        self.result = []
        self.image_set_path = image_set_path
        self.result_path = result_path

        #get model weights and bias, assign them to tensors for calculation
        for w, b in self.paras:
            self.weights.append(w)
            self.bias.append(b)
        self.weight_net_var = [var for var in tf.global_variables(
        ) if 'kernel' in var.name and 'conv' in var.name][::-1]
        self.bias_net_var = [var for var in tf.global_variables(
        ) if 'bias' in var.name and 'conv' in var.name][::-1]

        for i, var in enumerate(self.weight_net_var):
            self.assign_ops.append(
                tf.assign(
                    var,
                    tf.assign(var, self.weights[i])
                )
            )

        for i, var in enumerate(self.bias_net_var):
            self.assign_ops.append(
                tf.assign(
                    var,
                    tf.assign(var, self.bias[i])
                )
            )
        self.sess = tf.Session()
        self.sess.run(self.assign_ops)
        self.set_visualize_tensor()
    def set_visualize_tensor(self):

        visual_back_prop = None
        for i, layer in enumerate(self.conv_layers):
            average = tf.expand_dims(tf.reduce_mean(layer, [3]), 3)
            if visual_back_prop is not None:

                visual_back_prop = visual_back_prop * average
                visual_back_prop = self.deconv(
                    visual_back_prop, self.keras_layers[i])
            else:

                visual_back_prop = self.deconv(average, self.keras_layers[i])
            self.result.append(tf.squeeze(visual_back_prop))


    def deconv(self, feature_map, k_layer):
        kernel = np.ones(
            (k_layer.kernel_size[0],
             k_layer.kernel_size[1],
             1,
             1),
            dtype=np.float32)
        strides = (1, k_layer.strides[0], k_layer.strides[1], 1)
        output_shape = (1, k_layer.input_shape[1], k_layer.input_shape[2], 1)
        y = tf.nn.conv2d_transpose(
            feature_map,
            kernel,
            strides=strides,
            padding='VALID',
            output_shape=output_shape)
        return y

    def calculate(self):
        """
        you should preprocess your image to fit model input
        :return:
        """
        for i, file in enumerate( sorted( os.listdir( self.image_set_path ) ) ):
            image = scipy.misc.imread( self.image_set_path + file )[ 90:156, 60:260 ]
            result = self.sess.run(self.result,feed_dict={self.model.input:np.array([image])})
            scipy.misc.imsave( self.result_path + str( i ).zfill( 3 ) + '.png', result[-1] )


def main(_):
    model_path = FLAGS.model_dir
    result_dir = FLAGS.result_dir
    image_dir = FLAGS.image_dir

    vis = VisualBackprop( model_path, image_dir, result_dir )

    vis.calculate()
if __name__ == '__main__':

    tf.app.run()
