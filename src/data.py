from os import listdir
import json

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
            "RHeel"
        ]


def get_frames(video, key_points = KEY_POINTS):

    # initialize the result array
    result = {key_point: [] for key_point in key_points}

    data_dir = './data/'

    # iterate over each file in the folder
    for file in listdir(data_dir + video):

        # open the video data
        with open(data_dir + video + '/' + file) as f:
            # load the json in to a dictionary
            try:
                data = json.load(f)['people'][0]['pose_keypoints_2d']
            except IndexError:
                continue

            if len(data) == 3*len(KEY_POINTS):
                # iterate over the key_points
                for key_point in key_points:
                    # get the index of the key point
                    idx = KEY_POINTS.index(key_point)

                    # extract the coordinate
                    result[key_point].append((data[idx * 3], data[idx * 3 + 1]))

    return result
