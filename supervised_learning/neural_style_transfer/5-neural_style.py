#!/usr/bin/env python3
"""Module that defines the NST class"""
import numpy as np
import tensorflow as tf


class NST:
    """Class that performs tasks for neural style transfer"""
    style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1',
                    'block4_conv1', 'block5_conv1']
    content_layer = 'block5_conv2'

    def __init__(self, style_image, content_image, alpha=1e4, beta=1):
        """Class constructor for the NST class"""
        if not isinstance(style_image, np.ndarray) or style_image.ndim != 3:
            raise TypeError(
                "style_image must be a numpy.ndarray with shape (h, w, 3)")
        if not isinstance(content_image, np.ndarray) or content_image.ndim != 3:
            raise TypeError(
                "content_image must be a numpy.ndarray with shape (h, w, 3)")
        if not isinstance(alpha, (int, float)) or alpha < 0:
            raise TypeError("alpha must be a non-negative number")
        if not isinstance(beta, (int, float)) or beta < 0:
            raise TypeError("beta must be a non-negative number")

        tf.enable_eager_execution()

        self.style_image = self.scale_image(style_image)
        self.content_image = self.scale_image(content_image)
        self.alpha = alpha
        self.beta = beta
        self.load_model()
        self.generate_features()

    @staticmethod
    def scale_image(image):
        """Rescales an image such that its pixels values are between 0 and 1
        and its largest side is 512 pixels"""
        if not isinstance(image, np.ndarray) or image.ndim != 3:
            raise TypeError(
                "image must be a numpy.ndarray with shape (h, w, 3)")

        max_dim = max(image.shape[:-1])
        scale = 512 / max_dim
        new_shape = tuple([int(dim * scale) for dim in image.shape[:-1]] + [3])
        image = tf.image.resize_bicubic(np.expand_dims(image, 0), new_shape[:2])
        image = tf.clip_by_value(image / 255, 0, 1)
        return image

    def load_model(self):
        """Creates the model used to calculate cost"""
        vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
        vgg.trainable = False
        outputs = [vgg.get_layer(layer).output for layer in self.style_layers]
        outputs.append(vgg.get_layer(self.content_layer).output)
        self.model = tf.keras.Model(vgg.input, outputs)

    @staticmethod
    def gram_matrix(input_layer):
        """Calculates the gram matrix of a layer"""
        result = tf.linalg.einsum('bijc,bijd->bcd', input_layer, input_layer)
        input_shape = tf.shape(input_layer)
        num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
        return result / (num_locations)

    def generate_features(self):
        """Extracts the features used to calculate neural style cost"""
        vgg19 = tf.keras.applications.vgg19
        preprocessed_style = vgg19.preprocess_input(self.style_image * 255)
        preprocessed_content = vgg19.preprocess_input(self.content_image * 255)
        style_features = self.model(preprocessed_style)
        content_features = self.model(preprocessed_content)
        self.gram_style_features = [self.gram_matrix(style_feature)
                                    for style_feature in style_features[:-1]]
        self.content_feature = content_features[-1]

    def layer_style_cost(self, style_output, gram_target):
        """Calculates the style cost for a single layer"""
        if not isinstance(style_output, (tf.Tensor, tf.Variable)) or \
           style_output.ndim != 4:
            raise TypeError("style_output must be a tensor of rank 4")
        if not isinstance(gram_target, (tf.Tensor, tf.Variable)) or \
           gram_target.ndim != 3:
            raise TypeError("gram_target must be a tensor of rank 3")

        gram_style = self.gram_matrix(style_output)
        return tf.reduce_mean(tf.square(gram_style - gram_target))

    def style_cost(self, style_outputs):
        """Calculates the style cost for generated image

        parameters:
            style_outputs: list containing style outputs for the generated image

        returns: the style cost
        """
        if not isinstance(style_outputs, list):
            raise TypeError(
                "style_outputs must be a list with a length of {}".format(
                    len(self.style_layers)))

        if len(style_outputs) != len(self.style_layers):
            raise TypeError(
                "style_outputs must be a list with a length of {}".format(
                    len(self.style_layers)))

        style_costs = []
        weight = 1.0 / float(len(self.style_layers))

        for style_output, gram_target in zip(style_outputs,
                                             self.gram_style_features):
            layer_style_cost = self.layer_style_cost(style_output, gram_target)
            weighted_layer_style_cost = layer_style_cost * weight
            style_costs.append(weighted_layer_style_cost)

        return tf.add_n(style_costs)
