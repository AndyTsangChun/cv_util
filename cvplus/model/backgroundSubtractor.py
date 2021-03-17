#! /usr/bin/env python

import numpy as np
import os,sys,copy
import cv2

__author__ = "Andy Tsang"
__credits__ = ["Andy Tsang"]
__version__ = "0.0.1"
__maintainer__ = "Andy Tsang"
__email__ = "atc1992andy@gmail.com"

class BackgroundSubtractor:
	"""
	Module perform background subtraction to get contours
	"""
	def __init__(self, log=False, debug=False):
		self.__frameCount = 0
		self.bgModel = None
		self.contour_threshold = 3500

	def getForeground(self, frame, isResizeBG=False):
		"""
		Get foreground image by comparing background to current frame

		Args:
			frame (numpy.array): input image/frame
			isResizeBG (boolean): determine to resize bg model as frame size	
		Returns:
			* **foreground** (numpy.array)- output foreground image
		"""
		bg = copy.deepcopy(self.bgModel)
		if isResizeBG:
			bg = cv2.resize(self.bgModel,(frame.shape[1],frame.shape[0]))

		return cv2.absdiff(bg.astype(np.uint8),frame)

	def getMask(self, frame, isSingleChannel=False):
		"""
		Get binary mask

		
		Args:
			image(numpy.array): input image/frame
			isSingleChannel(boolean): return single channel image or not
		Returns:
			* **mask** (numpy.array) output foreground image, single channel
		"""
		foreGround = self.getForeground(self.__denoise(frame))
		# Convert to gray scale, reduce color from 3 to 1
		gray = cv2.cvtColor(foreGround,cv2.COLOR_BGR2GRAY)
		# Apply thresholding to obtain binary mask
		ret, mask = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
		if not isSingleChannel:
			mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)

		return mask

	def getContour(self, mask):
		"""
        Args:
        	mask (numpy.array): boolean mask obtain from getMask()
        Returns:
        	* **tmp_contour** contours raw contour
        	* **contourBoxes** Contour location in [cx,cy,width,height]
		"""
		thresh = cv2.dilate(mask, None, iterations=2)
		_, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

		tmp_contour = list()
		contourBoxes = list()
		for c in contours:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < self.contour_threshold:
				continue
	 
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(left, top, w, h) = cv2.boundingRect(c)
			contourBoxes.append([left+w/2,top+h/2,w,h])
			tmp_contour.append(c)

		return tmp_contour,contourBoxes

	def setContourSize(self, contour_threshold):
		self.contour_threshold = contour_threshold

	def setBGModel(self, bg):
		self.bgModel = self.__denoise(bg)

	def getFrameCount(self):
		return self.__frameCount

	def __denoise(self, frame):
		"""
		Remove noise from frame

		Args:
			frame (numpy.array): input image/frame
		Returns:
			frame (numpy.array): filtered image/frame
		"""
		frame = cv2.medianBlur(frame,5)
		frame = cv2.GaussianBlur(frame,(21,21),0)
		
		return frame
