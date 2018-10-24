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

def location2bbox(location):
	"""
	From location [top,right,bot,left] to bbox [x,y,width,height]
	
	Args:
		location (list): coordinate [top,right,bot,left]
	Returns:
		**bbox** (list) - bounding box [x,y,width,height]
	"""
	bbox = [location[3],location[0],location[1]-location[3],location[2]-location[0]]

	return bbox

def bbox2location(bbox):
	"""
	From bbox [x,y,width,height] to location [top,right,bot,left]
	
	Args:
		bbox (list): bounding box [x,y,width,height]
	Returns:
		**location** (list) - coordinate [top,right,bot,left]
	"""
	location = [bbox[1],bbox[0]+bbox[2],bbox[1]+bbox[3],bbox[0]]

	return location

def bbox_iou(box1, box2):
    """
    Calculating the IoU of two ht_vision.boundingBox
    Args:
        box1 (ht_vision.BoundingBox): Box 1
        box2 (ht_vision.BoundingBox): Box 2
    Returns:
        * **iou** (float) - Intersect over Union
    """
    x1_min  = box1.cx - box1.w/2
    x1_max  = box1.cx + box1.w/2
    y1_min  = box1.cy - box1.h/2
    y1_max  = box1.cy + box1.h/2
    
    x2_min  = box2.cx - box2.w/2
    x2_max  = box2.cx + box2.w/2
    y2_min  = box2.cy - box2.h/2
    y2_max  = box2.cy + box2.h/2
    
    intersect_w = interval_overlap([x1_min, x1_max], [x2_min, x2_max])
    intersect_h = interval_overlap([y1_min, y1_max], [y2_min, y2_max])
    
    intersect = intersect_w * intersect_h
    
    union = box1.w * box1.h + box2.w * box2.h - intersect
    
    if union <= 0:
        return 0
        
    return float(intersect) / union
    
def interval_overlap(interval_a, interval_b):
    """
    Return the minium coordinate from 2 given interval

    Args:
        interval_a (list): Interval a
        interval_b (list): Interval b
    Returns:
        * **min** (float) - minium coordinate
    """
    x1, x2 = interval_a
    x3, x4 = interval_b

    if x3 < x1:
        if x4 < x1:
            return 0
        else:
            return min(x2,x4) - x1
    else:
        if x2 < x3:
            return 0
        else:
            return min(x2,x4) - x3  