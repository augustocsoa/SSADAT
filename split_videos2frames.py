# Common imports
import os
import sys
import glob
import yaml
import argparse
from configs.config import *
# Especific imports
import subprocess

class FFMPEGFrames:
    def __init__(self, output, ext):
        self.output = output
        self.ext = ext
    def extract_frames(self, input, fps):
        output = input.split('/')[-1].split('.')[0]
        
        output_dir = os.path.join(self.output, output)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print("Splitting video: {}".format(input))

        else:
            print(input + " has been processed!")
            return 

        query = "ffmpeg -i " + input + " -vf fps=" + str(fps) + " -qscale:v 0 " + output_dir + "/%05d." + self.ext
        response = subprocess.Popen(query, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = response.communicate()
        exit_code = response.wait()
        if exit_code == 1:
          print("\033[31m",stderr,"\033[0m")

args = parse_args()

# If diretory no exist create
if not os.path.isdir(args.image_dir):
  print("The image directory does not exist! creating..\n")
  os.makedirs(args.image_dir)

print("Splitting videos to frames..\n")

input_video_dir = args.video_dir
fps = args.fps
out_root = args.image_dir
ext = args.extension

f = FFMPEGFrames(out_root, ext)

all_video_names = []
for video in (l for l in open(args.videos_list) if not l.startswith('#')):
  #print(video.strip())
  all_video_names.append(input_video_dir+"/"+video.strip()+".mp4")

#all_video_names = sorted(glob.glob(os.path.join(input_video_dir, '*')))

assert len(all_video_names) > 0

for video_name in all_video_names:
    f.extract_frames(video_name, fps)

print("\nNumber of splited videos: \033[1;31m{}\033[0m".format(len(all_video_names)))

sys.exit(0)
