#! /usr/bin/env python
import os,sys
import cv2, re
import numpy as np
try:
	from pyutil import PyLogger
except ImportError:
	from .. import PyLogger

__author__ = "Andy Tsang"
__credits__ = ["Andy Tsang"]
__version__ = "0.0.1"
__maintainer__ = "Andy Tsang"
__email__ = "atc1992andy@gmail.com"

SRC_TYPE_NAME = ["WebCam","Video","IPCam"]
OUTPUT_VIDEO_NAME = "source{}.avi"
SAVE_FORMAT = 'XVID'
DEFAULT_FPS = 20

class VideoController():
	def __init__(self, video_src, video_ratio=1, record_prefix="", record_name="", isRecord=False, log=False, debug=False):
		# init logger
		self.__logger = PyLogger(log=log,debug=debug)
		self.__vid_caps = list()
		self.__vid_writers = list()
		self.__record_path = os.path.join(record_prefix,record_name) if record_name != "" else os.path.join(record_prefix,OUTPUT_VIDEO_NAME)
		self.__video_ratio = video_ratio
		self.fps = DEFAULT_FPS
		# create a VideoCapture for each src
		for src in video_src:
			self.__initVideoSource(src)
		# init writer parameters
		self.__fourcc = cv2.VideoWriter_fourcc(*SAVE_FORMAT)
		if isRecord:
			self.__initVideoWriter()

	def __initVideoSource(self, src, camId=-1):
		"""
		Initialise video input source

		Args:
			src (object): video source used by Opencv, could be int or String
			camId (int): if any cameraId was given
		"""
		if src is None or src == "":
			return
		sourceType = -1
		# usb cam/web cam
		if type(src) is int:
			sourceType = 0
		# search for ipcams
		elif re.search( r'(http)|(rstp)|(https) & *', src, re.M|re.I):
			sourceType = 2
		# videos
		else:
			sourceType = 1
		cap = cv2.VideoCapture(src)
		if cap.isOpened():
			if camId == -1:
				camId = len(self.__vid_caps)
			if len(self.__vid_caps) > 0:
				cams = np.array(self.__vid_caps)[:,0]
				if camId in cams:
					camId = np.amax(cams) + 1
			fps = int(cap.get(cv2.CAP_PROP_FPS))
			self.__vid_caps.append([camId, sourceType, cap, src,fps])
			self.__logger.info("Video Input Connected to {}".format(src))
		else:
			self.__logger.error("No {} Source Found From {}".format(SRC_TYPE_NAME[sourceType], src))

	def __initVideoWriter(self):
		"""
		Initialise video writer
		"""
		for cap_info in self.__vid_caps:
			cap = cap_info[2] # get cv2.cap object
			fps = cap_info[4]
			if fps == 0 or self.fps < fps:
				fps = self.fps
			self.__vid_writers.append([cap_info[0],cv2.VideoWriter(self.__record_path.format(cap_info[0]),
																	self.__fourcc, 
																	fps, 
																	(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/self.__video_ratio),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/self.__video_ratio)))])

	def writeVideo(self, camId, frame):
		"""
		Write video to output

		Args:
			camId (int): if any cameraId was given
			frame (np.array): video frame to be written
		"""
		if len(self.__vid_writers) > 0:
			ids = np.array(self.__vid_writers)[:,0]
			if frame is not None:
				self.__vid_writers[np.where(ids == camId)[0][0]][1].write(frame)

	def getFrame(self, camId):
		"""
		Return frame from video source

		Args:
			camId (int): camera ID
		Returns:
			**frame** (np.array) - current frame
		"""
		# Capture frame-by-frame
		frame = None
		try:
			cap = self.__vid_caps[np.where(np.array(self.__vid_caps)[:,0]==camId)[0][0]][2]
			if cap is not None:
				ret, frame = cap.read()
				frame = cv2.resize(frame, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/self.__video_ratio),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/self.__video_ratio)))
			#frame = cv2.resize(frame, (420,240))
		except cv2.error:
			return None

		return frame

	def showFrame(self, frame, title="Video"):
		""" 
		Using OpenCV to display the current frame
		Title is important if need to display multi window

		Args:
			frame (np.array): frame given to be shown
			title (string): display window title, associate frame and display window
		"""
		# Display the resulting frame
		cv2.imshow(title,frame)
		# This line is important to keep the video showing
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cap.release()
			cv2.destroyAllWindows()

	def onClose(self):
		for cap in self.__vid_caps:
			cap[2].release()
		for writer in self.__vid_writers:
			writer[1].release()
		cv2.destroyAllWindows()

	def printVideoSrcInfo(self):
		# header
		self.__logger.info("{:5}|{:10}".format("CamID","Source"))
		# body
		for cap in self.__vid_caps:
			src = cap[3]
			if type(src) is int:
				src = SRC_TYPE_NAME[0]+ " {}".format(src)
			self.__logger.info("{:5}|{}".format(cap[0],src))

	def getVideoSrcInfo(self):
		"""
		Return Camera Information

		Returns:
			* **cam_info** (numpy.array) - camera information (camId, src)
		"""
		if len(self.__vid_caps) <= 0:
			return None
		return np.array(self.__vid_caps)[:,[0,3]]

	def drawInfo(self, frame, fps, color=(255,255,255), num_people=-1):
		"""
		Draw frame info

		Args:
			frame (numpy.array): input frame
			fps (int): Frame per second
			color (tuple): BGR color code
			num_people (int): number of people detected
		Returns:
			* **frame** (numpy.array) - modified frame
		"""
		frame_size = frame.shape
		cv2.putText(frame, "FPS:{}".format(fps), (20,frame_size[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
		if num_people >= 0:
			cv2.putText(frame, "Num.Person:{}".format(num_people), (frame_size[1]-150,frame_size[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

		return frame

	def setIsRecord(self, isRecord):
		"""
		Set is recorded video or not

		Args:
			isRecord (boolean): record video or not
		"""
		if isRecord and not self.isRecord:
			self.__initVideoWriter()
		self.isRecord = isRecord
