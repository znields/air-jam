from shutil import rmtree
import json
import numpy as np
import traceback
from os import listdir
import pygame
import sys

folder = '8-bit'
sounds = {}
pygame.mixer.init()
# iterate over each of the sounds
for file in listdir('./../sound/' + folder):
    # create the new sound and save it
    sounds[file.split('.')[0]] = pygame.mixer.Sound("./../sound/" + folder + '/' + file)
# create the key points
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

group2parts = {"face": ["Nose"],
                "hips": ["RHip", "LHip", "MidHip"],
                "knees": ["LKnee", "RKnee"],
                "elbows": ["LElbow", "RElbow"],
                "hands": ["LWrist", "RWrist"],
                "shoulders": ["LShoulder", "RShoulder"]}

group2threshold = {"face": 0.015,
                    "hips": 0.02,
                    "knees": 0.02,
                    "elbows": 0.03,
                    "hands": 0.04,
                    "shoulders": 0.015}

debounce = {"face": 1000,
            "hips": 1000,
            "knees": 1000,
            "elbows": 1000,
            "hands": 1000,
            "shoulders": 1000}

# try to erase the previous data
try: rmtree('./../data/live')
except Exception as e: print(e)



# initialize count and debounce
count = 0

# create a list for right wrist points
x_coords = []
y_coords = []

# continuously search for new json files
while True:
    try:
        # try to open the next json file as f
        with open('./../data/live/' + str(count).zfill(12) + '_' + 'keypoints.json') as f:
            # read the poeple from the json object
            people = json.load(f)['people']

            # get the pose key points
            data = people[0]['pose_keypoints_2d'] if people else [0 for _ in range(75)]

            x_coords.append(np.array(data[0::3]))
            y_coords.append(np.array(data[1::3]))

            for k in debounce.keys():
                debounce[k] -= 1
            count += 1

            num_out = 0
            for i in range(len(x_coords[-1])):
                if x_coords[-1] == [0,0,0]:
                    num_out += 1

            # if the length of wrists is more than 5
            if len(x_coords) <= 5 or len(y_coords) <= 5:
                continue

            x_coords.pop(0)
            y_coords.pop(0)

            x_diff = np.subtract(x_coords[0], x_coords[-1])
            y_diff = np.subtract(y_coords[0], y_coords[-1])

            for i in range(len(x_diff)):
                x_diff[i] = abs(x_diff[i])
                y_diff[i] = abs(y_diff[i])

            for group in group2parts.keys():
                diff, xdiff, ydiff = 0, 0, 0
                for part in group2parts[group]:
                    index = KEY_POINTS.index(part)
                    xdiff += x_diff[index]
                    ydiff += y_diff[index]
                diff = xdiff**2 + ydiff**2
                if debounce[group] < 500 and diff > group2threshold[group]:
                    debounce[group] = 3000
                    s = sounds[group]
                    s.play()

    except FileNotFoundError:
        if count > 0:
            count -= 1

    except json.JSONDecodeError as e:
        pass

    except Exception as e:
        traceback.print_exc()
