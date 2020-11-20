# Common imports
import os
import sys
import glob
import yaml
import argparse
from configs.config import *
# Especific imports
import subprocess


class FFMPEGFrames2videos:
  def __init__(self, in_root, out_root, ext_in, ext_out, fps ):
    self.in_root = in_root
    self.out_root = out_root
    self.ext_in = ext_in
    self.ext_out = ext_out
    self.fps = fps
    self.processed = 0

  def makevideo(self, input_folder):
    clip = input_folder
    input_folder = self.in_root+'/'+clip
    outputfile = self.out_root+'/'+clip+self.ext_out
    #print(input_folder)
    #print(outputfile)
    if os.path.exists(outputfile):
      print("    Short clip {} has been processed!".format(clip))

    else:
      #print("  Creating video from short clip {}".format(clip))

      #query = "ls -la " + input_folder
      query = "ffmpeg -framerate "+str(self.fps)+" -i "+input_folder+"/%04d"+self.ext_in+" -s:v 1280x720 -c:v mpeg4 -crf 28 -pix_fmt yuv420p "+outputfile
      #print(query)
      response = subprocess.Popen(query, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
      stdout, stderr = response.communicate()
      exit_code = response.wait()
      if exit_code == 1:
        print("\033[31m",stderr,"\033[0m")
      else:
        self.processed += 1

  #def getprocessed():
  #  return self.processed

args = parse_args()

if not os.path.isdir(args.short_clips_dir):
  print("The short_clips directory does not exist! Aborting..\n")
  sys.exit(1)


if not os.path.isdir(args.rec_videos_dir):
  print("The rec_videos directory does not exist! creating..\n")
  os.makedirs(args.rec_videos_dir)


all_short_clips = sorted(glob.glob(os.path.join(args.short_clips_dir, '*')))

assert len(all_short_clips) > 0

print("Total number of short_clips found: \033[1;31m{}\033[0m".format(len(all_short_clips)))

in_root = args.short_clips_dir
out_root = args.rec_videos_dir
ext_in = args.ext_in
ext_out = args.ext_out
fps = args.fps

folder_obj = FFMPEGFrames2videos(in_root, out_root, ext_in, ext_out, fps)

for clip in all_short_clips:
  path, folder = os.path.split(clip)
  #print(path)
  #print(folder)
  print("\033[1;36m"+"  Processing Short Clip {}..".format(folder)+"\033[0m")

  folder_obj.makevideo(folder)
  #break
  #exit(0)


print("\nNumber of videos created: \033[1;31m{}\033[0m".format(folder_obj.processed))
video_files = sorted(glob.glob(args.rec_videos_dir + '/*.mp4'))
print("Number of videos in {}: \033[1;31m{}\033[0m".format(args.rec_videos_dir, len(video_files)))

sys.exit(0)
