from shutil import rmtree
import json
import numpy as np
import traceback
import pydub
from pydub.playback import play
from os import listdir
import pygame

folder = 'guitar'

# initialize the sounds
sounds = []

pygame.mixer.init()

# iterate over each of the sounds
for file in listdir('./../sound/' + folder):

    # create the new sound and save it
    sound = pygame.mixer.Sound('./../sound/' + folder + '/' + file)

    # save the sound
    sounds.append(sound)

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

# continuously search for new json files
while True:
    try:
        # try to open the next json file as f
        with open('./../data/live/' + str(count).zfill(12) + '_' + 'keypoints.json') as f:

            # read the poeple from the json object
            people = json.load(f)['people']

            # get the pose key points
            data = people[0]['pose_keypoints_2d'] if people else [0 for _ in range(75)]

            # get the indices for left hip and wrist and right wrist
            lh_idx, lw_idx, rw_idx = KEY_POINTS.index('LHip'), KEY_POINTS.index('LWrist'), KEY_POINTS.index('RWrist')

            # get the current left hip and left wrist points
            LHip = np.array(data[lh_idx * 3: lh_idx * 3 + 2])
            LWrist = np.array(data[lw_idx * 3: lw_idx * 3 + 2])

            # get the current right wrist
            RWrists.append(np.array(data[rw_idx * 3: rw_idx * 3 + 2]))

            # if the length of wrists is more than 5
            if len(RWrists) > 5:

                # remove the first element
                RWrists.pop(0)

            # calculate the wrist velocity for the last half second
            RWristVelocity = np.array([0.0, 0.0]) if len(RWrists) < 5 else (RWrists[-1] - RWrists[0]) / 0.4

            # calculate the left wrist difference from the hip
            handDistance = np.linalg.norm(LHip - LWrist) / 1

            # if the right wrist's downward velocity is more than 0.2
            if RWristVelocity[1] > 0.2 and debounce < 0 and handDistance > 0.05:

                i_prev = 0.05

                # iterate over the sounds
                for sound, i, note in zip(sounds, np.linspace(0.2, 0.8, len(sounds)), listdir('./../sound/' + folder)):

                    # if the hand distance is in the right range
                    if i_prev < handDistance < i:

                        # set the sound volume based on strum speed
                        sound.set_volume(np.linalg.norm(RWristVelocity))

                        # play the sound
                        sound.play()

                        # print the strum
                        print('Strum:', note.split('.')[0], np.linalg.norm(RWristVelocity))

                    i_prev = i

                # reset the debounce
                debounce = 500

            # increment count and decrement debounce
            debounce -= 1
            count += 1

    except FileNotFoundError:
        if count > 0:
            count -= 1

    except json.JSONDecodeError as e:
        pass

    except Exception as e:
        traceback.print_exc()
