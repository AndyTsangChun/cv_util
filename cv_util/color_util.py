#! /usr/bin/env python
import numpy as np
from random import shuffle

__author__ = "Andy Tsang"
__credits__ = ["Andy Tsang"]
__version__ = "0.0.0"
__maintainer__ = "Andy Tsang"
__email__ = "atc1992andy@gmail.com"

GOLDEN_RATIO = 0.618033988749895

def genColors(num, isShuffle=False):
	"""
	Generate a list of color in RGB
	
	Args:
		num (int): number of color to generate
		isShuffle (boolean): random shuffle the color or follow hsv sequence
	Return:
		**colors** (boolean) - list of color code, in RGB
	"""
	colors = []
	for i in range(num):
		h = 1. / num * i
		h += GOLDEN_RATIO
		h %= 1
		r, g, b = hsv2rgb(h, 0.9, 0.9)
		colors.append(rgb2hex(r, g, b))

	if isShuffle:
		shuffle(colors)

	return colors

def hsv2rgb(h, s, v):
	"""
	Convert color space from HSV to RGB
	
	Args:
		h (float): Hue
		s (float): Saturation
		v (float): Value
	Return:
		* **r** (int) - Red
		* **g** (int) - Green
		* **b** (int) - Blue
	"""
	h_i = int(h*6)
	f = h*6 - h_i
	p = v * (1 - s)
	q = v * (1 - f*s)
	t = v * (1 - (1 - f) * s)
	if h_i == 0:
		r, g, b = v, t, p
	if h_i == 1:
		r, g, b = q, v, p
	if h_i == 2:
		r, g, b = p, v, t
	if h_i == 3:
		r, g, b = p, q, v
	if h_i == 4:
		r, g, b = t, p, v
	if h_i == 5:
		r, g, b = v, p, q

	return int(r*256), int(g*256), int(b*256)

def rgb2hex(r, g, b):
	"""
	Convert RGB to color hex
	
	Args:
		r (int): Red
		g (int): Green
		b (int): Blue
	Returns:
		**hex** (string) - Hex color code
	"""
	return '#%02x%02x%02x' % (r, g, b)