#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorlayer.layers.core import Layer
from tensorlayer.layers.core import TF_GRAPHKEYS_VARIABLES

from tensorlayer.decorators import deprecated_alias
from tensorlayer.decorators import force_return_self

__all__ = [
    # 'DeConv1d'  # TODO: Needs to be implemented
    'DeConv2d',
    'DeConv3d',
]


class DeConv2d(Layer):
    """Simplified version of :class:`DeConv2dLayer`.

    Parameters
    ----------
    prev_layer : :class:`Layer`
        Previous layer.
    n_filter : int
        The number of filters.
    filter_size : tuple of int
        The filter size (height, width).
    out_size : tuple of int
        Require if TF version < 1.3, (height, width) of output.
    strides : tuple of int
        The stride step (height, width).
    padding : str
        The padding algorithm type: "SAME" or "VALID".
    batch_size : int or None
        Require if TF < 1.3, int or None.
        If None, try to find the `batch_size` from the first dim of net.outputs (you should define the `batch_size` in the input placeholder).
    act : activation function
        The activation function of this layer.
    W_init : initializer
        The initializer for the weight matrix.
    b_init : initializer or None
        The initializer for the bias vector. If None, skip biases.
    W_init_args : dictionary
        The arguments for the weight matrix initializer (For TF < 1.3).
    b_init_args : dictionary
        The arguments for the bias vector initializer (For TF < 1.3).
    name : str
        A unique layer name.

    """

    @deprecated_alias(
        layer='prev_layer', n_out_channel='n_filter', end_support_version="2.0.0"
    )  # TODO: remove this line before releasing TL 2.0.0
    def __init__(
            self,
            prev_layer=None,
            n_filter=32,
            filter_size=(3, 3),
            strides=(2, 2),
            padding='valid',
            data_format='channels_last',
            W_init=tf.truncated_normal_initializer(stddev=0.02),
            b_init=tf.constant_initializer(value=0.0),
            W_init_args=None,  # TODO: Remove when TF <1.3 not supported
            b_init_args=None,  # TODO: Remove when TF <1.3 not supported
            act=None,
            name='deconv2d'
    ):

        if data_format not in ["channels_last", "channels_first"]:
            raise ValueError("`data_format` value is not valid, should be either: 'channels_last' or 'channels_first'")

        padding = padding.upper()
        if padding not in ["SAME", "VALID"]:
            raise ValueError("`padding` value is not valid, should be either: 'SAME' or 'VALID'")

        if len(strides) != 2:
            raise ValueError("len(strides) should be 2, DeConv2d and DeConv2dLayer are different.")

        self.prev_layer = prev_layer
        self.n_filter = n_filter
        self.filter_size = filter_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.W_init = W_init
        self.b_init = b_init
        self.act = act
        self.name = name

        super(DeConv2d, self).__init__(W_init_args=W_init_args, b_init_args=b_init_args)

    def __str__(self):
        additional_str = []

        try:
            additional_str.append("n_filter: %d" % self.n_filter)
        except AttributeError:
            pass

        try:
            additional_str.append("filter_size: %s" % str(self.filter_size))
        except AttributeError:
            pass

        try:
            additional_str.append("stride: %s" % str(self.strides))
        except AttributeError:
            pass

        try:
            additional_str.append("padding: %s" % self.padding)
        except AttributeError:
            pass

        try:
            additional_str.append("act: %s" % self.act.__name__ if self.act is not None else 'No Activation')
        except AttributeError:
            pass

        return self._str(additional_str)

    def compile(self, prev_layer, is_train=True):

        super(DeConv2d, self).compile(prev_layer)

        is_name_reuse = tf.get_variable_scope().reuse

        with tf.variable_scope(self.name) as vs:

            self.outputs = tf.layers.conv2d_transpose(
                inputs=self.inputs, filters=self.n_filter, kernel_size=self.filter_size, strides=self.strides,
                padding=self.padding, data_format=self.data_format, activation=None, kernel_initializer=self.W_init,
                bias_initializer=self.b_init, use_bias=(True if self.b_init else
                                                        False), reuse=is_name_reuse, trainable=is_train, name=None
            )

            self._apply_activation(self.outputs)

            self._local_weights = tf.get_collection(TF_GRAPHKEYS_VARIABLES, scope=vs.name)

        self._add_layers(self.outputs)
        self._add_params(self._local_weights)


class DeConv3d(Layer):
    """Simplified version of The :class:`DeConv3dLayer`, see `tf.contrib.layers.conv3d_transpose <https://www.tensorflow.org/api_docs/python/tf/contrib/layers/conv3d_transpose>`__.

    Parameters
    ----------
    prev_layer : :class:`Layer`
        Previous layer.
    n_filter : int
        The number of filters.
    filter_size : tuple of int
        The filter size (depth, height, width).
    stride : tuple of int
        The stride step (depth, height, width).
    padding : str
        The padding algorithm type: "SAME" or "VALID".
    act : activation function
        The activation function of this layer.
    W_init : initializer
        The initializer for the weight matrix.
    b_init : initializer or None
        The initializer for the bias vector. If None, skip bias.
    W_init_args : dictionary
        The arguments for the weight matrix initializer (For TF < 1.3).
    b_init_args : dictionary
        The arguments for the bias vector initializer (For TF < 1.3).
    name : str
        A unique layer name.

    """

    @deprecated_alias(
        layer='prev_layer', end_support_version="2.0.0"
    )  # TODO: remove this line before releasing TL 2.0.0
    def __init__(
            self,
            prev_layer=None,
            n_filter=32,
            filter_size=(3, 3, 3),
            strides=(2, 2, 2),
            padding='valid',
            data_format='channels_last',
            W_init=tf.truncated_normal_initializer(stddev=0.02),
            b_init=tf.constant_initializer(value=0.0),
            W_init_args=None,  # TODO: Remove when TF <1.3 not supported
            b_init_args=None,  # TODO: Remove when TF <1.3 not supported
            act=None,
            name='deconv3d'
    ):

        if data_format not in ["channels_last", "channels_first"]:
            raise ValueError("`data_format` value is not valid, should be either: 'channels_last' or 'channels_first'")

        padding = padding.upper()
        if padding not in ["SAME", "VALID"]:
            raise ValueError("`padding` value is not valid, should be either: 'SAME' or 'VALID'")

        self.prev_layer = prev_layer
        self.n_filter = n_filter
        self.filter_size = filter_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.W_init = W_init
        self.b_init = b_init
        self.act = act
        self.name = name

        super(DeConv3d, self).__init__(W_init_args=W_init_args, b_init_args=b_init_args)

    def __str__(self):
        additional_str = []

        try:
            additional_str.append("n_filter: %d" % self.n_filter)
        except AttributeError:
            pass

        try:
            additional_str.append("filter_size: %s" % str(self.filter_size))
        except AttributeError:
            pass

        try:
            additional_str.append("stride: %s" % str(self.strides))
        except AttributeError:
            pass

        try:
            additional_str.append("padding: %s" % self.padding)
        except AttributeError:
            pass

        try:
            additional_str.append("act: %s" % self.act.__name__ if self.act is not None else 'No Activation')
        except AttributeError:
            pass

        return self._str(additional_str)

    def compile(self, prev_layer, is_train=True):

        super(DeConv3d, self).compile(prev_layer)

        is_name_reuse = tf.get_variable_scope().reuse

        with tf.variable_scope(self.name) as vs:

            self.outputs = tf.layers.conv3d_transpose(
                inputs=self.inputs, filters=self.n_filter, kernel_size=self.filter_size, strides=self.strides,
                padding=self.padding, data_format=self.data_format, activation=None, kernel_initializer=self.W_init,
                bias_initializer=self.b_init, use_bias=(True if self.b_init else
                                                        False), reuse=is_name_reuse, trainable=is_train, name=None
            )

            self._apply_activation(self.outputs)

            self._local_weights = tf.get_collection(TF_GRAPHKEYS_VARIABLES, scope=vs.name)

        self._add_layers(self.outputs)
        self._add_params(self._local_weights)
