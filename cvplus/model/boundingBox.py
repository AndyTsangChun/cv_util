#! /usr/bin/env python
import cv2
import numpy as np
try:
	from pyutil import PyLogger
except ImportError:
	from .. import PyLogger
from .. import getTextBoxRatio

__author__ = "Andy Tsang"
__credits__ = ["Andy Tsang"]
__version__ = "0.0.1"
__maintainer__ = "Andy Tsang"
__email__ = "atc1992andy@gmail.com"

class BoundingBox:
	"""
	Object Classes for Bounding Box, DEFAULT takes NON-CORNER parameters
	All coordinate DEFAULT represent in integer as required by some libraries(Python3+)

	THIS OBJECT HAS 2 MODE, INT for exact coordinate and FLOAT for relative position
	"""
	__slots__=["__logger",'cx','cy','width','height','ymin','xmin','ymax','xmax','conf','classes','label','cname','pose','truncated','difficult','score']
	def __init__(self, cx=0, cy=0, width=0, height=0, ymin=0, xmin=0, ymax=0, xmax=0, conf=None, classes=None, label=None, cname=None, pose=None, truncated=0, difficult=0, isCorners=False, isCoordinates=True, log=False, debug=False):
		"""
		Args:
			cx (int/float): X-coordinate of bounding box center
			cy (int/float): Y-coordinate of bounding box center
			width (int/float): Width of bounding box
			height (int/float): Height of bounding box
			ymin (int/float): Y coordinate of Top-Left corner
			xmin (int/float): X coordinate of Top-Left corner
			ymax (int/float): Y coordinate of Bottom-Right corner
			xmax (int/float): X coordinate of Bottom-Right corner
			conf (float): Confidene of prediction
			classes (np.arry): One-Hot Encoded
			label (int): class label
			cname (string): Class name
			pose (int): object pose
			truncated (int): truncated from COCO
			difficult (int): difficult level
			isCorners (boolean): BoundingBox is init with size parameters or corner coordinates
			isCoordinate (boolean) : Determine whether this bounding box information int (exact coordinate) or is float (relative to image size)
			log (boolean): show log or not
			debug (boolean): show debug info or not
		"""
		# init logger
		self.__logger = PyLogger(log=log,debug=debug)

		if isCoordinates:
			# exact coordinate
			if isCorners:
				assert (not(ymin == xmin == ymax == xmax == 0)), self.__logger.error("Invalid bounding box corner coordinates is given.")
				self.ymin = int(ymin)
				self.xmin = int(xmin)
				self.ymax = int(ymax)
				self.xmax = int(xmax)
				self.cx, self.cy, self.width, self.height = self.__corners2sizes(int(ymin), int(xmin), int(ymax), int(xmax), isCoordinates)
			else:
				assert (not(cx == cy == width == height == 0)), self.__logger.error("Invalid bounding box size parameters is given.")
				self.cx = int(cx)
				self.cy = int(cy)
				self.width = int(width)
				self.height = int(height)
				self.ymin, self.xmin, self.ymax, self.xmax = self.__sizes2corners(int(cx), int(cy), int(width), int(height), isCoordinates)
		else:
			# relative position
			if isCorners:
				assert (not(ymin == xmin == ymax == xmax == 0)), self.__logger.error("Invalid bounding box corner coordinates is given.")
				self.ymin = ymin
				self.xmin = xmin
				self.ymax = ymax
				self.xmax = xmax
				self.cx, self.cy, self.width, self.height = self.__corners2sizes(ymin, xmin, ymax, xmax, isCoordinates)
			else:
				assert (not(cx == cy == width == height == 0)), self.__logger.error("Invalid bounding box size parameters is given.")				
				self.cx = cx
				self.cy = cy
				self.width = width
				self.height = height
				self.ymin, self.xmin, self.ymax, self.xmax = self.__sizes2corners(cx, cy, width, height, isCoordinates)

		self.conf = conf
		self.classes = classes
		self.cname = cname
		self.pose = pose
		self.truncated = truncated
		self.difficult = difficult

		self.label = -1 if label is None else label
		self.score = -1

		if self.classes is not None and len(self.classes) > 1:
			self.getLabel()
			self.getScore()

	def __sizes2corners(self, cx, cy, width, height, isCoordinates=True):
		"""
		Args:
			cx (int): X-coordinate of bounding box center
			cy (int): Y-coordinate of bounding box center
			width (int): Width of bounding box
			height (int): Height of bounding box
		Returns:
			ymin (int)- Y coordinate of Top-Left corner
			xmin (int)- X coordinate of Top-Left corner
			ymax (int)- Y coordinate of Bottom-Right corner
			xmax (int)- X coordinate of Bottom-Right corner
		"""
		ymin = cy - height/2.
		xmin = cx - width/2.
		ymax = cy + height/2.
		xmax = cx + width/2.

		if isCoordinates:
			return int(ymin), int(xmin), int(ymax), int(xmax)
		else:
			return ymin, xmin, ymax, xmax

	def __corners2sizes(self, ymin, xmin, ymax, xmax, isCoordinates=True):
		"""
		Args:
			ymin (int): Y coordinate of Top-Left corner
			xmin (int): X coordinate of Top-Left corner
			ymax (int): Y coordinate of Bottom-Right corner
			xmax (int): X coordinate of Bottom-Right corner
		Returns:
			cx (int)- X-coordinate of bounding box center
			cy (int)- Y-coordinate of bounding box center
			width (int)- Width of bounding box
			height (int)- Height of bounding box
		"""
		width = xmax - xmin
		height = ymax - ymin
		cx = xmin + width/2.
		cy = ymin + height/2.

		if isCoordinates:
			return int(cx), int(cy), int(width), int(height)
		else:
			return cx, cy, width, height

	def crop(self, image):
		"""
		Crop and return the boundingbox image

		Args:
			image (np.array): image to crop
		Returns:
			**crop_image** (np.array) - cropped image
		"""
		return image.copy()[self.ymin:self.ymax,self.xmin:self.xmax]


	def draw(self, image, color=(0,255,0), thickness=2, drawText=False):
		"""
		Draw the bounding box on the image

		Args:
			image (np.array): image to draw on
			color (tuple): color in RGB
			thickness (int): thickness of the border of the bounding box
		Returns:
			* **image** (np.array) - modifited image
		"""
		if drawText:
			image = self.drawText(image=image, color=color)
		cv2.rectangle(image, (self.xmin,self.ymin), (self.xmax,self.ymax), color, thickness)

		return image

	def drawText(self, image, text=None, color=(0,255,0), size=-1, thickness=1, font=cv2.FONT_HERSHEY_DUPLEX, offset=(0,-5)):
		"""
		Draw text

		Args:
			image (np.array): image to draw on
			text (string): text to be drawn
			color (tuple): color in RGB
			size (int): font size
			thickness (int): thickness of text
			font (int): cv2 font type
			offset (tuple): x,y offset of the text
		Returns:
			* **image** (np.array) - modifited image
		"""
		box_w = self.xmax-self.xmin
		text = "{} {:.2f}".format(self.cname, self.conf) if text is None else text
		if size == -1:
			size, nh = getTextBoxRatio(text, box_w, font=font, thickness=thickness)
		cv2.putText(image, text, (self.xmin+offset[0],self.ymin+offset[1]), font, size, color, thickness)

		return image

	def getLabel(self):
		if self.classes is not None or self.label == -1:
			self.label = np.argmax(self.classes)
		
		return self.label
	
	def getScore(self):
		if self.classes is not None or self.score == -1:
			self.score = self.classes[self.getLabel()]
			
		return self.score

	def __str__(self):
		return "Label:{}, BBox:({},{}),({},{})".format(self.label, self.xmin, self.ymin, self.xmax, self.ymax)
