# Common imports
import os
import sys
import glob
import yaml
import argparse
from configs.config import *
# Especific imports
import pickle as pkl
import shutil

#if __name__ == "__main__":
args = parse_args()

data = pkl.load(open(args.label_file,'rb'))

if not os.path.isdir(args.clips_dir):
  print("The clips dir directory does not exist! creating..\n")
  os.makedirs(args.clips_dir)

num_short_clips = 0
for key, value in data.items():
  video_name = key
  
  v_name, clip_index = video_name.split("_")
 
  video_dir = os.path.join(args.video_dir, value['video_name'])
  out_dir = os.path.join(args.clips_dir, video_name)




  if not os.path.isdir(out_dir):
    print("Extracting short clip {} from video: {}".format(clip_index, v_name ))

    os.mkdir(out_dir)
    start = value['clip_start']
    end = value['clip_end']
    for new_i, old_i in enumerate(range(int(start), int(end)+1)):
      img_name = str(old_i).zfill(5) + args.extension
      old_img_path = os.path.join(video_dir, img_name)    
      new_img_path = os.path.join(out_dir, str(new_i + 1).zfill(4) + '.jpg')

      shutil.copy(old_img_path, new_img_path)
  else:
    print( "Short clip {} from video: {} has been processed!".format(clip_index, v_name ))

  num_short_clips +=1

print()
print("Number of short clips: \033[1;31m{}\033[0m".format(num_short_clips))

sys.exit(0)
