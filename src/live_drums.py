from shutil import rmtree
import json
import numpy as np
import traceback
import pygame
from os import listdir
from pythonosc import osc_message_builder, udp_client


PORT_NUMBER = 3333
IP_NUM = '192.168.43.144'
client = udp_client.SimpleUDPClient(IP_NUM, PORT_NUMBER)

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
debounce_left = 800
debounce_right = 800

# create a list for right wrist points
RWrists = []
RShoulders = []

LWrists = []
LShoulders = []

rw_idx = KEY_POINTS.index('RWrist')
rs_idx = KEY_POINTS.index('RShoulder')
lw_idx = KEY_POINTS.index('LWrist')
ls_idx = KEY_POINTS.index('LShoulder')
hip_idx = KEY_POINTS.index('MidHip')

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

            MidHip = set(data[hip_idx * 3: hip_idx * 3 + 2])

            # iterate over each list of key points
            for l in [RWrists, RShoulders, LWrists, LShoulders]:

                # if there are more than five key points
                if len(l) > 200:
                    # remove the last one
                    l.pop(0)

            # calculate the right wrist velocity
            rw_velocity = RWrists[-1] - RWrists[0]
            rw_speed = np.linalg.norm(rw_velocity)

            if rw_speed > 0.1 and rw_velocity[1] > 0 > debounce_right and 0 not in MidHip:

                debounce_right = 800

                # if the right wrist is outside the right shoulder
                if RWrists[-1][0] + 0.05 < RShoulders[-1][0]:

                    client.send_message('/hit', 1)
                    # play the floor tom
                    # sounds['floor-tom'].set_volume(rw_speed)
                    sounds['floor-tom'].play()
                    print('Floor Tom', rw_speed)

                else:

                    client.send_message('/hit', 2)

                    # play the floor tom
                    # sounds['mid-tom'].set_volume(rw_speed)
                    sounds['mid-tom'].play()
                    print('Mid Tom', rw_speed)

            debounce_right -= 1

            #########################################

            # calculate the left wrist velocity
            lw_velocity = LWrists[-1] - LWrists[0]
            lw_speed = np.linalg.norm(lw_velocity)

            if lw_speed > 0.1 and lw_velocity[1] > 0 > debounce_left and 0 not in MidHip:

                debounce_left = 800

                # if the right wrist is outside the right shoulder
                if LWrists[-1][0] - 0.05 < LShoulders[-1][0]:

                    client.send_message('/hit', 3)

                    # play the snare drum
                    # sounds['snare-drum'].set_volume(rw_speed)
                    sounds['snare-drum'].play()
                    print('Snare Drum', rw_speed)

                else:

                    client.send_message('/hit', 4)

                    # play the floor tom
                    # sounds['ride-cymbal'].set_volume(rw_speed)
                    sounds['ride-cymbal'].play()
                    print('Ride Cymbal', rw_speed)

            debounce_left -= 1

            count += 1

    except FileNotFoundError:
        if count > 0:
            count -= 1

    except json.JSONDecodeError as e:
        pass

    except Exception as e:
        traceback.print_exc()
