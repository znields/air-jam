import subprocess
from os import listdir

# iterate over each file in the unprocessed video folder


for file in set(listdir('./../videos/unprocessed')) - set(listdir('./../data')):

    # get the name and extension of the file
    name, ext = file.split('.')

    # process the video
    subprocess.call([r"./bin/OpenPoseDemo.exe",
                     "--video", "./../videos/unprocessed/" + file,
                     "--write_video", "./../videos/processed/" + name + '.avi',
                     "--write_json", "./../data/" + file,
                     '--keypoint_scale', '3'])
