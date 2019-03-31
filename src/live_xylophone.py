from shutil import rmtree
import json
import numpy as np
import traceback
import pygame
from os import listdir
from time import sleep

folder = 'xylophone'

# initialize pygame
pygame.mixer.init()

# initialize the sounds
sounds = []

# iterate over each of the sounds
for file in listdir('./../sound/' + folder):

    # create the new sound and save it
    sounds.append(pygame.mixer.Sound(r"./../sound/" + folder + '/' + file))

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
debounce_left = 1000
debounce_right = 1000

# create a list for right wrist points
RWrists = []
RShoulders = []

LWrists = []
LShoulders = []

rw_idx = KEY_POINTS.index('RWrist')
lw_idx = KEY_POINTS.index('LWrist')
mhip_idx = KEY_POINTS.index('MidHip')

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
            LWrists.append(np.array(data[lw_idx * 3: lw_idx * 3 + 2]))
            MidHip = np.array(data[mhip_idx * 3: mhip_idx * 3 + 2])

            # iterate over each list of key points
            for l in [RWrists, RShoulders, LWrists, LShoulders]:

                # if there are more than five key points
                if len(l) > 200:
                    # remove the last one
                    l.pop(0)

            # calculate the right wrist velocity
            rw_velocity = RWrists[-1] - RWrists[0]
            rw_speed = np.linalg.norm(rw_velocity)

            if rw_speed > 0.1 and rw_velocity[1] > 0.05 and 0 > debounce_right and 0 not in MidHip:

                debounce_right = 1000

                i_prev = 0.0

                for sound, i, note in zip(sounds, np.linspace(0.05, 1.0, len(sounds)), listdir('./../sound/' + folder)):

                    # if the hand distance is in the right range
                    if i_prev < RWrists[-1][0] < i:
                        # set the sound volume based on strum speed
                        # sound.set_volume(np.linalg.norm(RWristVelocity))

                        # play the sound
                        sound.play()

                        # print the strum
                        print('Tap:', note.split('.')[0], np.linalg.norm(rw_velocity))

                    i_prev = i

            debounce_right -= 1

            #########################################

            # calculate the left wrist velocity
            lw_velocity = LWrists[-1] - LWrists[0]
            lw_speed = np.linalg.norm(lw_velocity)

            if lw_speed > 0.1 and lw_velocity[1] > 0.03 and 0 > debounce_left and 0 not in MidHip:

                debounce_left = 1000

                i_prev = 0.0

                for sound, i, note in zip(sounds, np.linspace(0.03, 1.0, len(sounds)), listdir('./../sound/' + folder)):

                    # if the hand distance is in the right range
                    if i_prev < LWrists[-1][0] < i:
                        # set the sound volume based on strum speed
                        # sound.set_volume(np.linalg.norm(RWristVelocity))

                        # play the sound
                        sound.play()

                        # print the strum
                        print('Tap:', note.split('.')[0], np.linalg.norm(rw_velocity))

                    i_prev = i

            debounce_left -= 1

            count += 1

    except FileNotFoundError:
        if count > 0:
            count -= 1

    except json.JSONDecodeError as e:
        pass

    except Exception as e:
        traceback.print_exc()
