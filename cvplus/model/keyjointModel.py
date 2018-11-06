from enum import Enum

__author__ = "Andy Tsang"
__credits__ = ["Andy Tsang"]
__version__ = "0.0.1"
__maintainer__ = "Andy Tsang"
__email__ = "atc1992andy@gmail.com"

"""
CVPlus human model
Using 15 Joint Point
"""
class CVPlusPart(Enum):
	Nose = 0
	Neck = 1
	RShoulder = 2
	RElbow = 3
	RWrist = 4
	LShoulder = 5
	LElbow = 6
	LWrist = 7
	RHip = 8
	RKnee = 9 
	RAnkle = 10
	LHip = 11
	LKnee = 12
	LAnkle = 13
	CHip = 14
# paf pairs
CVPLUS_Pairs = [(0, 1), (1, 5), (1, 2), (1, 14),
         (2, 3), (2, 8), (3, 4), (5, 6),
         (5, 11), (6, 7), (8, 14), (8, 9),
         (9, 10), (11, 14), (11, 12), (12, 13)]
CVPLUS_PairsName = ["Neck","LShoulder","RShoulder","Back",
                "RArm","RWaist","RForearm","LArm",
                "LWaist","LForearm","RHip","RThigh",
                "RCalf","LHip","LThigh","LCalf"]
# joint angle pairs
CVPLUS_AnglePairs = [(4,3,2), (3,2,8), (2,1,0), (0,1,5),
              (11,5,6), (5,6,7), (9,8,14), (8,14,1),
              (1,14,11), (14,11,12), (10,9,8), (11,12,13)]
CVPLUS_AngleName = ["RElbow","RArmpit","RNeck","LNeck",
                "LArmpit","LElbow","RCrotch","RWaist",
                "LWaist","LCrotch","RKnee","LKnee"]
# determine view padding edge for opencv, frontal 
CVPLUS_AngleViewEdge = [0,1,0,0,
                        1,0,1,0,
                        0,1,1,1]
# degree of freedom
"""
DOF Baseline
shoulder: bend from 0-90°; straighten 90-0 °; move away from the body 0-90° ; move towards the body 90-0° ; rotate away form the center of the body 0-90° ; rotate toward the center of the body 90-0°
elbow: bend from 0-90°; straighten 90-0 °; move away from the body 0-90° ; move towards the body 90-0° ; rotate away form the center of the body 0-90° ; rotate toward the center of the body 90-0°
wrist: bend from 0-90°; straighten 0-70 °; move away from the body 0-25° ; move towards the body 0-65°
metacarpophalangeal fingers: bend down 0-90°; straighten 0-30°
interphalangeal – proximal: bend 0-120°; straighten 120-0°
interphalangeal – distal: bend 0-80°; straighten 80-0°
metacarpophalangeal-thumb: bend 0-70°; straighten 60-0°; abduct 0-50°; adduct 40-0°
interphalangeal – thumb: bend 0-90°; straighten 90-0°
hip: bend from 0-125°; straighten 115-0°; move away from the body 0-45° ; move towards the body 45-0° ; rotate away form the center of the body 0-45° ; rotate toward the center of the body 45-0° ; abduction 0-25°; adduction 20-0°
knee: bend from 0-130°; straighten 120-0°
ankle: bend downward 0-50°; move upward 0-20°
foot: turn inward 0-35°; turn outward 0-25°
metatarsophalangeal toes: bend down 0-35°; bend up 0-80°
interphalangeal: bend down 0-50°; bend up 50-80°
"""
CVPLUS_AngleDOF = [180,180,135,135,
                180,180,270,135,
                135,270,180,180]

"""
Human model based on MSCoco pose challenge dataset
Using 19 joint point
"""
class CocoPart(Enum):
    Nose = 0
    Neck = 1
    RShoulder = 2
    RElbow = 3
    RWrist = 4
    LShoulder = 5
    LElbow = 6
    LWrist = 7
    RHip = 8
    RKnee = 9
    RAnkle = 10
    LHip = 11
    LKnee = 12
    LAnkle = 13
    REye = 14
    LEye = 15
    REar = 16
    LEar = 17
    Background = 18
    #
COCO_Pairs = [(1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10), (1, 11), (11, 12), (12, 13), (1, 0), (0, 14), (14, 16), (0, 15), (15, 17), (2, 16), (5, 17)]
COCO_PairsRender = COCO_Pairs[:-2]

"""
Human model based on MPII dataset
Using 14 joint point
"""
class MPIIPart(Enum):
    RAnkle = 0
    RKnee = 1
    RHip = 2
    LHip = 3
    LKnee = 4
    LAnkle = 5
    RWrist = 6
    RElbow = 7
    RShoulder = 8
    LShoulder = 9
    LElbow = 10
    LWrist = 11
    Neck = 12
    Head = 13
    #

    @staticmethod
    def from_coco(human):
        # t = {
        #     MPIIPart.RAnkle: CocoPart.RAnkle,
        #     MPIIPart.RKnee: CocoPart.RKnee,
        #     MPIIPart.RHip: CocoPart.RHip,
        #     MPIIPart.LHip: CocoPart.LHip,
        #     MPIIPart.LKnee: CocoPart.LKnee,
        #     MPIIPart.LAnkle: CocoPart.LAnkle,
        #     MPIIPart.RWrist: CocoPart.RWrist,
        #     MPIIPart.RElbow: CocoPart.RElbow,
        #     MPIIPart.RShoulder: CocoPart.RShoulder,
        #     MPIIPart.LShoulder: CocoPart.LShoulder,
        #     MPIIPart.LElbow: CocoPart.LElbow,
        #     MPIIPart.LWrist: CocoPart.LWrist,
        #     MPIIPart.Neck: CocoPart.Neck,
        #     MPIIPart.Nose: CocoPart.Nose,
        # }

        t = [
            (MPIIPart.Head, CocoPart.Nose),
            (MPIIPart.Neck, CocoPart.Neck),
            (MPIIPart.RShoulder, CocoPart.RShoulder),
            (MPIIPart.RElbow, CocoPart.RElbow),
            (MPIIPart.RWrist, CocoPart.RWrist),
            (MPIIPart.LShoulder, CocoPart.LShoulder),
            (MPIIPart.LElbow, CocoPart.LElbow),
            (MPIIPart.LWrist, CocoPart.LWrist),
            (MPIIPart.RHip, CocoPart.RHip),
            (MPIIPart.RKnee, CocoPart.RKnee),
            (MPIIPart.RAnkle, CocoPart.RAnkle),
            (MPIIPart.LHip, CocoPart.LHip),
            (MPIIPart.LKnee, CocoPart.LKnee),
            (MPIIPart.LAnkle, CocoPart.LAnkle),
        ]

        pose_2d_mpii = []
        visibilty = []
        for mpi, coco in t:
            if coco.value not in human.body_parts.keys():
                pose_2d_mpii.append((0, 0))
                visibilty.append(False)
                continue
            pose_2d_mpii.append((human.body_parts[coco.value].x, human.body_parts[coco.value].y))
            visibilty.append(True)
        return pose_2d_mpii, visibilty

