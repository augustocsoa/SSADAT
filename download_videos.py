# Common imports
import os
import sys
import glob
import yaml
import argparse
from configs.config import *
# Especific imports
import youtube_dl

#if __name__ == "__main__":
args = parse_args()

# If diretory no exist create
if not os.path.isdir(args.download_root):
  print("The download directory does not exist! creating..\n")
  os.makedirs(args.download_root)

url_list = []
for video in (l for l in open(args.videos_list) if not l.startswith('#')):
  #print(video.strip())
  url_list.append("https://www.youtube.com/watch?v="+video.strip())

#print("Download videos files..")
#url_list = open(args.videos_urls,'r').readlines()


ydl_opt = {'outtmpl': args.download_root + '/%(id)s.%(ext)s',
           'format': 'mp4'}

ydl = youtube_dl.YoutubeDL(ydl_opt)
ydl.download(url_list)
print("Download finished!\n")

video_files = sorted(glob.glob(args.download_root + '/*.mp4'))
print("Number of downloaded videos: \033[1;31m{}\033[0m".format(len(url_list)))
print("Number of videos in {}: \033[1;31m{}\033[0m".format(args.download_root, len(video_files)))


sys.exit(0)
