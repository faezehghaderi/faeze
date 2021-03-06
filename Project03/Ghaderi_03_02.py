# Ghaderi, Faezeh
# 1001-552-571
# 2018-10-07
# Assignment-03-02
import numpy as np
import math
# This module calculates the activation function
def calculate_activation_function(net_value,type='Sigmoid'):

	activation = []
	if type == 'Hardlim':
		net_value[net_value<0]=-1
		net_value[net_value>0]=+1
	if type == "Linear":
		net_value = net_value
	elif type == "Tangent":
		net_value = np.tanh(net_value)
	return net_value