from shutil import rmtree
import json
import numpy as np
import traceback
import pygame
from os import listdir

folder = 'drums'

# initialize pygame
pygame.mixer.init()

# initialize the sounds
sounds = []

# iterate over each of the sounds
for file in listdir('./../sound/' + folder):

    # create the new sound and save it
    sounds.append(pygame.mixer.Sound("./../sound/" + folder + '/' + file))

    # play the sound
    pygame.mixer.Sound.play(sounds[-1])

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

# try to erase the previous data
try: rmtree('./../data/live')
except Exception as e: pass

# initialize count and debounce
count = 0
debounce = 500

# create a list for right wrist points
RWrists = []
RShoulders = []

LWrists = []
LShoulders = []

rw_idx = KEY_POINTS.index('RWrist')
rs_idx = KEY_POINTS.index('RShoulder')
lw_idx = KEY_POINTS.index('LWrist')
ls_idx = KEY_POINTS.index('LShoulder')

# continuously search for new json files
while True:
    try:
        # try to open the next json file as f
        with open('./../data/live/' + str(count).zfill(12) + '_' + 'keypoints.json') as f:

            # read the poeple from the json object
            people = json.load(f)['people']

            # get the pose key points
            data = people[0]['pose_keypoints_2d'] if people else [0 for _ in range(78)]

            RWrists.append(np.array(data[rw_idx * 3: rw_idx * 3 + 1]))
            RShoulders.append(np.array(data[rw_idx * 3: rw_idx * 3 + 1]))


        count += 1

    except FileNotFoundError:
        if count > 0:
            count -= 1

    except json.JSONDecodeError as e:
        pass

    except Exception as e:
        traceback.print_exc()
