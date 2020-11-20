# -*- coding: utf-8 -*-
import os
import sys
import json
import pickle

try:
  file_in = sys.argv[1]

except IndexError as ie:
  print("Usage: 'python %s <pickle_file.pkl>'" % sys.argv[0])
  sys.exit(0)

file_out = file_in[:-4]+"_my2.pkl"

fi = open(file_in, 'rb')
mydict = pickle.load(fi)
fi.close()

dict2 = {}
for p in mydict.keys():
    if mydict[p]['video_name']=='26CH4m5Huck':
        dict2[p]=mydict[p]
    if mydict[p]['video_name']=='B1MpK2hye3o':
        dict2[p]=mydict[p]
    if mydict[p]['video_name']=='eW9vWga9F5M':
        dict2[p]=mydict[p]
    if mydict[p]['video_name']=='fTmYppzzloc':
        dict2[p]=mydict[p]
    if mydict[p]['video_name']=='GkDXwJXjQx0':
        dict2[p]=mydict[p]
    if mydict[p]['video_name']=='LNT8NB2Dv-E':
        dict2[p]=mydict[p]
    if mydict[p]['video_name']=='R88JhqThHrg':
        dict2[p]=mydict[p]
    if mydict[p]['video_name']=='SafZaefNbPY':
        dict2[p]=mydict[p]
    if mydict[p]['video_name']=='U45XrAuG8ig':
        dict2[p]=mydict[p]
    if mydict[p]['video_name']=='U733SSe0rYQ':
        dict2[p]=mydict[p]

fo = open(file_out, 'wb')
pickle.dump(dict2, fo, 3)
fo.close()

exit(0)
