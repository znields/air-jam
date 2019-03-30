from os import listdir
from shutil import rmtree
import json
from math import acos
import numpy as np

KEY_POINTS = [
            "Nose",
            "Neck",
            "RShoulder",
            "RElbow",
            "RWrist",
            "LShoulder",
            "LElbow",
            "LWrist",
            "MidHip",
            "RHip",
            "RKnee",
            "RAnkle",
            "LHip",
            "LKnee",
            "LAnkle",
            "REye",
            "LEye",
            "REar",
            "LEar",
            "LBigToe",
            "LSmallToe",
            "LHeel",
            "RBigToe",
            "RSmallToe",
            "RHeel",
            "Background"
        ]

rmtree('./../data/live')
count = 0

MidHips = []
LWrists = []
RWrists = []

while True:
    try:
        with open('./../data/live/' + str(count).zfill(12) + '_' + 'keypoints.json') as f:

            people = json.load(f)['people']
            data = people[0]['pose_keypoints_2d'] if people else [0 for _ in range(25)]

            MidHips.append(np.array(data[KEY_POINTS.index('MidHip') * 3: KEY_POINTS.index('MidHip') * 3 + 2]))
            LWrists.append(np.array(data[KEY_POINTS.index('LWrist') * 3: KEY_POINTS.index('LWrist') * 3 + 2]))
            RWrists.append(np.array(data[KEY_POINTS.index('RWrist') * 3: KEY_POINTS.index('RWrist') * 3 + 2]))

            for i in [MidHips, LWrists, RWrists]:
                if len(i) > 5:
                    i.pop(0)

            RWristVelocity = np.array([0.0, 0.0]) if len(RWrists) < 5 else RWrists[-1] - RWrists[0]

            print(RWristVelocity)

            count += 1

    except FileNotFoundError:

        if count > 0:
            count -= 1

    except Exception as e:
        print(e)
