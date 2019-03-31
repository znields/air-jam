from shutil import rmtree
import json
import numpy as np
import traceback
from os import listdir

folder = 'guitar'

# initialize pygame
pygame.mixer.init()# the sounds
sounds = []

# iterate over each of the sounds
for file in listdir('./../sound/' + folder):

    # create the new sound and save its
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
            "LAnkle"
        ]

# try to erase the previous data

try: rmtree('./../data/live')
except Exception as e: print(e)


# initialize count and debounce
count = 0
debounce = 10

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

            # increment count and decrement debounce
            debounce -= 1
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

            x_avg = np.sort(x_diff)[(len(x_diff) + num_out)//2]
            y_avg = np.sort(y_diff)[(len(y_diff) + num_out)//2]

            speed = x_avg**2 + y_avg**2
            if (debounce < 0 and speed > 0.02):
                debounce = 20
                print(speed)


    except FileNotFoundError:
        if count > 0:
            count -= 1

    except json.JSONDecodeError as e:
        pass

    except Exception as e:
        traceback.print_exc()
