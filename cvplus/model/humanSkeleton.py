import math
import numpy as np
from . import keyjointModel
from .keyjointModel import CocoPart, MPIIPart, CVPlusPart

DEFAULT_JOINT_COLOR = (250,250,250)
DEFAULT_PAIR_COLOR = (0,255,0)

class HumanSkeleton2D:
	"""
	Human SkeletonModel designed for 2Dimension space
	"""
	__slots__ = ['humanId','body_parts', 'pairs', 'pairs_dist', 'angles', 'score', 'partType', 'isFrontal']
	def __init__(self, humanId, pairs, partType="CVPlus"):
		self.humanId = humanId
		self.partType = partType
		self.score = 0.0
		self.pairs = list()
		self.pairs_dist = list()
		self.body_parts = dict()

	def __str__(self):
		return ' '.join([str(x) for x in self.body_parts.values()])

	def __repr__(self):
		return self.__str__()

	def addBodyParts(self, jointId, x, y, score, z=0):
		self.body_parts[jointId] = KeyJoint(jointId, x, y, z, score)

	def initModelDetails(self,image_size=(1,1)):
		self.isFrontal = self.__checkPoseFacade()
		# cal MHip, since its not estimated by the dataset
		if partType="CVPlus" and 8 in self.body_parts and 11 in self.body_parts:
			jointId = 14
			rhip = self.body_parts[8]
			lhip = self.body_parts[11]
			human_id = int(rhip.uidx.split('-')[0])
			# cal hip center
			chip_x = (lhip.x + rhip.x)/2
			chip_y = (lhip.y + rhip.y)/2
			chip_z = 0
			chip_score = (rhip.score + lhip.score) /2
			self.body_parts[14] = KeyJoint(
						'%d-%d' % (human_id, jointId), jointId,
						chip_x,
						chip_y,
						chip_z,
						chip_score
					)

		# pairs_dist
		self.pairs_dist = dict()
		if self.partType == "MSCOCO":
			num_of_pairs = keyjointModel.COCO_Pairs
		elif self.partType == "CVPlus":
			num_of_pairs = keyjointModel.CVPlus_Pairs
		elif self.partType == "MPII":
			raise NotImplementedError
		for i, pairs in enumerate(num_of_pairs):
			try:
				joint1 = self.body_parts[pairs[0]]
				joint2 = self.body_parts[pairs[1]]
				w,h = image_size
				self.pairs_dist[i] = HumanSkeleton2D._get_length((joint1.x*w,joint1.y*h),(joint2.x*w,joint2.y*h))
			except KeyError:
				# body part not exsist
				self.pairs_dist[i] = -1

		# cal angles
		if self.partType == "CVPlus":
			self.angles = dict()
			for i, angle_pair in enumerate(keyjointModel.CVPlus_AnglePairs):
				try:
					joint1 = self.body_parts[angle_pair[0]]
					joint2 = self.body_parts[angle_pair[1]]
					joint3 = self.body_parts[angle_pair[2]]
					# This part should integrate with self.pairs_dist
					self.angles[i] = HumanSkeleton2D._get_angle((joint1.x,joint1.y), (joint2.x,joint2.y), (joint3.x,joint3.y))
				except KeyError:
					# body part not exsist
					self.angles[i] = -1

	def part_count(self):
		return len(self.body_parts.keys())

	def get_max_score(self):
		return max([x.score for _, x in self.body_parts.items()])

	@staticmethod
	def _get_angle(pt1, pt2, pt3, ptAngle=2):
		"""
		pt is in format (x,y)
		pt1 is point on left/top
		pt2 is point on mid
		pt3 is point on right/bot
		"""
		c = HumanSkeleton2D._get_length(pt1,pt2) # pt1_2_len
		a = HumanSkeleton2D._get_length(pt2,pt3) # pt2_3_len
		b = HumanSkeleton2D._get_length(pt3,pt1) # pt3_1_len
		if ptAngle == 1:
			cos = np.clip((b**2+c**2-a**2)/(2*b*c),-1,1)
		if ptAngle == 2:
			cos = np.clip((c**2+a**2-b**2)/(2*c*a),-1,1)
		if ptAngle == 3:
			cos = np.clip((a**2+b**2-c**2)/(2*a*b),-1,1)
		delta = math.degrees(math.acos(cos))

		return delta

	@staticmethod
	def _get_length(pt1, pt2):
		"""
		pt is in format (x,y)
		"""
		return np.sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2)

	def __checkPoseFacade(self):
		"""
		Check the facade of the person
		True is equals to Frontal
		False is equals to Backward
		None is equals to Unknown due to missing body_part
		"""
		# this function should be replace my an output from the NN predicting which face is that person facing
		if 2 in self.body_parts and 5 in self.body_parts and 8 in self.body_parts and 11 in self.body_parts:
			if self.body_parts[5].x < self.body_parts[2].x and self.body_parts[11].x < self.body_parts[8].x:
				return False
			else:
				return True
		return None

	def drawSkeleton(self, image, isKeepBG=True):
		skeleton_frame = image.copy()
		if not isKeepBG:
			skeleton_frame[skeleton_frame > 0] = 0
		overlay = skeleton_frame.copy()
		image_h, image_w = image.shape[:2]
		centers = dict()

		# check partType
		if partType == "MSCOCO":
			skeleton_pairs = keyjointModel.COCO_Pairs
		elif partType =="CVPlus":
			skeleton_pairs = keyjointModel.CVPlus_Pairs
			skeleton_angle_pairs = keyjointModel.CVPLUS_AnglePairs
			skeleton_angle_ve = keyjointModel.CVPLUS_AngleViewEdge
			skeleton_angle_dof = keyjointModel.CVPLUS_AngleDOF
		else:
			# partType not support
			raise NotImplementedError

		# draw key joint
		for i in human.body_parts.keys():
			body_part = human.body_parts[i]
			center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
			centers[i] = center
			cv2.circle(skeleton_frame, center, 3, DEFAULT_JOINT_COLOR, thickness=2, lineType=8, shift=0)
		# draw angle
		if partType == "CVPlus":
			for i, (anglePair, viewEdge, dof) in enumerate(zip(skeleton_angle_pairs, skeleton_angle_ve, skeleton_angle_dof)):
				try:
					angle = human.angles[i]
					if angle > dof:
						angle = dof
					self.__draw_angle(overlay, human.body_parts[anglePair[0]], human.body_parts[anglePair[1]], human.body_parts[anglePair[2]], angle, viewEdge)
				except KeyError:
					# body part not exsist
					pass

		# add angle overlay
		alpha = 0.5
		beta = 1-alpha
		cv2.addWeighted(overlay, alpha, skeleton_frame, beta, 0, skeleton_frame)
		
		# draw line
		for pair_order, pair in enumerate(skeleton_pairs):
			if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
				continue
			cv2.line(skeleton_frame, centers[pair[0]], centers[pair[1]], DEFAULT_PAIR_COLOR, 2)

		return skeleton_frame

	def __draw_angle(self, image, pt1, pt2, pt3, angle, viewEdge, color=(0,255,0)):
		image_h, image_w = image.shape[:2]
		# for opencv we need an extra point with same x-axis but different y-axis to pt2
		padding_pt = (pt2.x, pt2.y - 0.0000000001)
		# if angle was not calculated, set to 0 degree
		if angle == -1:
			angle = 0
		try:
			# determine to calculate opencv visualize padding angle based on which edge
			# padding calculate starting from straight up with -90 passed to opencv since
			# that function was doesn't start 0 from straight up
			if viewEdge == 0:
				padding_angle = int(self.__get_angle((pt2.x,pt2.y),(pt1.x,pt1.y),padding_pt))
				if pt1.x < pt2.x:
					pt2_angle = pt2_angle - padding_angle
					padding_angle = -padding_angle
			else:
				padding_angle = int(self.__get_angle((pt2.x,pt2.y),(pt3.x,pt3.y),padding_pt))
				if pt3.x < pt2.x:
					pt2_angle = pt2_angle - padding_angle
					padding_angle = -padding_angle
				else:
					pt2_angle = pt2_angle + padding_angle
		except ValueError:
			padding_angle = 0

		# if given coordiate are in ratio, we convery the back to exact coordinate
		center = (int(pt2.x * image_w + 0.5), int(pt2.y * image_h + 0.5))
		# draw ellipse
		cv2.ellipse(image, center, (20,20), -90, padding_angle, angle, color, -1, 8)

class KeyJoint:
	"""
	Key Joint Object, just rename this part from body part for easier understanding as other paper
	"""
	__slots__ = ('jointId', 'x', 'y', 'z', 'score')

	def __init__(self, jointId, x, y, z, score):
		"""
		Args:
			jointId(int): joint index(eg. 0 for nose), for exact index please refer to keyjoint model
			x: x-coordinate of keyjoint
			y: y-coordinate of keyjoint
			z: z-coordinate of keyjoint
			score : confidence score
		"""
		self.jointId = jointId
		self.x, self.y, self.z = x, y, z
		self.score = score

	def get_part_name(self, partType):
		if partType == "MSCOCO":
			return CocoPart(self.jointId)
		elif partType == "MPII":
			return MPIIPart(self.jointId)
		elif partType == "CVPlus":
			return CVPlusPart(self.jointId)

	def __str__(self):
		return 'KeyJoint:%d-(%.2f, %.2f, %.2f) score=%.2f' % (self.jointId, self.x, self.y, self.z, self.score)

	def __repr__(self):
		return self.__str__()
