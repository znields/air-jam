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
sounds = {}

# iterate over each of the sounds
for file in listdir('./../sound/' + folder):

    # create the new sound and save it
    sounds[file.split('.')[0]] = pygame.mixer.Sound("./../sound/" + folder + '/' + file)

    # play the sound
    pygame.mixer.Sound.play(sounds[file.split('.')[0]])

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
debounce_left = 500
debounce_right = 500

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

            # get the body key points
            RWrists.append(np.array(data[rw_idx * 3: rw_idx * 3 + 2]))
            RShoulders.append(np.array(data[rs_idx * 3: rs_idx * 3 + 2]))
            LWrists.append(np.array(data[lw_idx * 3: lw_idx * 3 + 2]))
            LShoulders.append(np.array(data[ls_idx * 3: ls_idx * 3 + 2]))

            # TODO: remove
            print(RShoulders[-1])

            # iterate over each list of key points
            for l in [RWrists, RShoulders, LWrists, LShoulders]:

                # if there are more than five key points
                if len(l) > 5:
                    # remove the last one
                    l.pop(0)

            # calculate the right wrist velocity
            rw_velocity = RWrists[-1] - RWrists[0] / 0.5
            rw_speed = np.linalg.norm(rw_velocity)

            if rw_speed > 0.9 and debounce_right < 0:

                debounce_right = 500

                # if the right wrist is above the right shoulder
                if RWrists[-1][1] <= RShoulders[-1][1]:
                    print(RWrists[-1], RShoulders[-1])

                    # play the ride cymbal
                    sounds['ride-cymbal'].set_volume(rw_speed)
                    sounds['ride-cymbal'].play()
                    print('Ride Cymbal', rw_speed)

                else:

                    # if the right wrist is outside the right shoulder
                    if RWrists[-1][0] < RShoulders[-1][0]:

                        # play the floor tom
                        sounds['floor-tom'].set_volume(rw_speed)
                        sounds['floor-tom'].play()
                        print('Floor Tom', rw_speed)

                    else:
                        # play the floor tom
                        sounds['mid-tom'].set_volume(rw_speed)
                        sounds['mid-tom'].play()
                        print('Mid Tom', rw_speed)

            debounce_right -= 1
            lw_velocity = LWrists[-1] - LWrists[0]
            count += 1

    except FileNotFoundError:
        if count > 0:
            count -= 1

    except json.JSONDecodeError as e:
        pass

    except Exception as e:
        traceback.print_exc()
