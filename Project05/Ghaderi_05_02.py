# Ghaderi, Faezeh
# 1001-552-571
# 2018-11-25
# Assignment-05-02
import numpy as np
import tensorflow as tf

# This module calculates the activation function
def calculate_activation_function(net_value,type='Relu'):

	#activation = []
	if type == 'Relu':
		net_value=tf.nn.relu(net_value)
		

	elif type == "Sigmoid":
		net_value = tf.nn.sigmoid(net_value)
	return net_value