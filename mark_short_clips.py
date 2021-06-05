# Common imports
import os
import sys
import glob
import yaml
import argparse
from configs.config import *
# Especific imports
import pickle
import cv2

args = parse_args()

def pickle2dict(file):
  file_in = file
  try:
    with open(file_in, "rb") as fi:
      mydict = pickle.load(fi)
    
  except FileNotFoundError as fnf:
    print("\033[41mError:\033[0m {} \033[31mnot found.\033[0m".format(args.labels))
    sys.exit(1)
  except PermissionError:
    print("\033[41mError:\033[0m {} \033[31mYou don't have permission to open this file.\033[0m".format(args.labels))
    sys.exit(1)

  return mydict

labels = pickle2dict(args.labels)

if not os.path.isdir(args.short_clips_dir):
  print("The short_clips directory does not exist! Aborting..\n")
  sys.exit(1)

all_short_clips = sorted(glob.glob(os.path.join(args.short_clips_dir, '*')))

assert len(all_short_clips) > 0

print("Total number of short_clips found: \033[1;31m{}\033[0m".format(len(all_short_clips)))

num_short_clips = 0
for clip in all_short_clips:
  path, folder = os.path.split(clip)
  #print(path)
  #print(folder)
  print("\033[1;36m"+"  Processing Short Clip {}..".format(folder)+"\033[0m")

  all_frames = sorted(glob.glob(os.path.join(path, folder, '*')))
  #print(all_frames[0])

  mark = labels[folder]["target"]

  for frame in range(len(all_frames)):
    if mark[frame] == 1:
      image = cv2.imread(all_frames[frame])
      #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      text = 'Accident Detected!!'
      font = cv2.FONT_HERSHEY_SIMPLEX 
      org = (320, 340) 
      fontScale = 2.5
      color = (20, 20, 235) 
      thickness = 4
      # Using cv2.putText() method 
      image = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False)
      cv2.imwrite(all_frames[frame],image)
      #cv2.imshow("Previsao", image)
      #cv2.waitKey(0)
      #cv2.destroyAllWindows()
  num_short_clips +=1
  #break

print("Number of short clips marked: \033[1;31m{}\033[0m".format(num_short_clips))


sys.exit(0)
