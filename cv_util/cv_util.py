#! /usr/bin/env python

import io,os,sys,cv2,math
import numpy as np

__author__ = "Andy Tsang"
__credits__ = ["Andy Tsang"]
__version__ = "0.0.0"
__maintainer__ = "Andy Tsang"
__email__ = "atc1992andy@gmail.com"

"""
Util function to extend basic opencv function
"""

def getTextBoxRatio(text, box_width, font=cv2.FONT_HERSHEY_DUPLEX, thickness=1):
	"""
	Return text box ratio 
	
	Args:
		text (str): string of text wish to print
		box_width (int): Width of the background box
		font (int): cv2 font type
		thickness (int): string thickness
	Returns:
		* **text_ratio** (float) - text ratio for opencv
		* **nh** (int) - new height
	"""
	normal_length = cv2.getTextSize(text, font, 1, thickness)
	tw = normal_length[0][0]
	nh = normal_length[0][1]
	text_ratio = 1
	if tw > box_width:
		text_ratio = (box_width/float(tw))
		nh = cv2.getTextSize(text, font, text_ratio, thickness)[0][1]

	return text_ratio, nh

def drawDashedLine(image, color, start_pos, end_pos, width=1, dash_length=8):
	"""
	Draw dashed line
	
	Args:
		image (np.array): image to draw on
		color (tuple): color code (R,G,B)
		start_pos (tuple): start coordinate
		end_pos (tuple): end coordinate
		width (int): line width
		dash_length (int): space between dash
	"""
	x1, y1 = start_pos
	x2, y2 = end_pos
	dl = dash_length

	if (x1 == x2):
		ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
		xcoords = [x1] * len(ycoords)
	elif (y1 == y2):
		xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
		ycoords = [y1] * len(xcoords)
	else:
		a = abs(x2 - x1)
		b = abs(y2 - y1)
		c = round(math.sqrt(a**2 + b**2))
		dx = dl * a / c
		dy = dl * b / c

		xcoords = [int(x) for x in np.arange(x1, x2, dx if x1 < x2 else -dx)]
		ycoords = [int(y) for y in np.arange(y1, y2, dy if y1 < y2 else 1)]

	next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
	last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
	for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
		start = (round(x1), round(y1))
		end = (round(x2), round(y2))
		cv2.line(image, start, end, color, width)