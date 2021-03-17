#! /usr/bin/env python

import os,sys
import numpy as np
import base64
import cv2
from scipy import misc
from PIL import Image

__author__ = "Andy Tsang"
__credits__ = ["Andy Tsang"]
__version__ = "0.0.2"
__maintainer__ = "Andy Tsang"
__email__ = "atc1992andy@gmail.com"

def normalize(image):
    """
    Basic normalization for image
    Args:
        image (np.array): original image range 0~255
    Returns:
        * **image** (np.array) - normalized image range 0.~1.
    """
    image = image / 255.
    
    return image

def getDownSampleImage(image, imageSize=320):
	"""
	Function take image and down sample to imageSize, while keeping the original ratio
	
	Args:
		image (numpy.array): image use for cropping (h,w,c)
		imageSize (int): target size
	Returns:
		* **resized_image** (numpy.array) - cropped image (h,w,c)
	"""

	image_ratio = float(image.shape[1])/image.shape[0]
	if image_ratio > 1:
		resized_image = cv2.resize(image, (imageSize, int(imageSize/image_ratio)))
	else:
		resized_image = cv2.resize(image, (int(imageSize*image_ratio), imageSize))

	return resized_image


def getCroppedImage(image, locations, imageSize=128, isWithPadding=False):
	"""
	Function take image and bounding boxes return cropped images
	
	Args:
		image (numpy.array): image use for cropping (h,w,c)
		locations (numpy.array): face location information
		imageSize (int): size of the cropped image
		isWithPadding (boolean): the cropped image whether with padding
	Returns:
		* **images** (numpy.array) - array of cropped images (n,h,w,c)
	"""
	new_images = []
	if image is None or locations is None or len(locations) <= 0:
		return
	for loc in locations:
		y = t = loc[0]
		r = loc[1]
		b = loc[2]
		x = l = loc[3]
		width = r-l
		height = b-t
		face_center = getCenterPoint(loc)
		face_center = (int(face_center[0]),int(face_center[1]))
		if isWithPadding:
			# length(top,left,bot,right)
			lengths = [face_center[1],face_center[0],image.shape[0]-face_center[1],image.shape[1]-face_center[0]]
			min_length = min(lengths)
			crop_img = misc.imresize(image[(face_center[1]-min_length):(face_center[1]+min_length), (face_center[0]-min_length):(face_center[0]+min_length)], (imageSize,imageSize))
		else:
			crop_img = misc.imresize(image[y:(y+height), x:(x+width)], (imageSize,imageSize))
		new_images.append(crop_img)
	new_images = np.array(new_images)

	return new_images

def npa2base64(npa):
	"""
	Convert image (numpy.array) to base64
	
	Args:
		npa (numpy.array): image in numpy.arry
	Returns:
		**b64** (string) - image in base64
	"""
	return (base64.b64encode(np.ascontiguousarray(npa))).decode("utf-8")

def base642npa(b64, shape):
	"""
	Convert image (string.base64) to numpy array
	
	Args:
		b64 (string): image in base64
		shape (tuple): shape of the image (h,w,c)
	Returns:
		* **npa** (numpy.array) - image in numpy array
	"""
	npa = np.reshape(np.frombuffer(base64.decodestring(b64), dtype=np.uint8),shape)

	return npa

def saveImgRGB(savePath, image):
	"""
	Save RGB image by cv2
	Args:
		image (numpy.array): image in RGB
	"""
	cv2.imwrite(savePath,cv2.cvtColor(image,cv2.COLOR_RGB2BGR))	


def PIL2CV(image):
	"""
	Convert PIL.image to OpenCV image

	Args:
		image (numpy.array): return image in numpy array
	"""	
	image = np.array(image)
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	return image

def CV2PIL(image):
	"""
	Convert OpenCV image to PIL.image
	
	Args:
		image (numpy.array): return image in PIL image
	"""
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image = Image.fromarray(image)

	return image						

def getCenterPoint(bbox):
	"""
	Function to get the center point of a given bbox (top,right,bot,left)
	
	Args:
		bbox (list): coordinate [top,right,bot,left]
	Returns:
		* **x** (int) - x of center
		* **y** (int) - y of center
	"""
	width = bbox[1]-bbox[3]
	height = bbox[2]-bbox[0]
	x = bbox[3] + width / 2
	y = bbox[0] + height / 2

	return x,y

def distanceOfpoints(dx,dy,isAbs=True):
	"""
	Function to get distance between points
	
	Args:
		dx (float): change of x-axis
		dy (float): change of y-axis
		isAbs (boolean): is getting absolute value
	Return:
		* **dist** (float) - distance between two points
	"""
	if isAbs:
		return math.hypot(dx, dy)
	else:
		DoSTH=True
