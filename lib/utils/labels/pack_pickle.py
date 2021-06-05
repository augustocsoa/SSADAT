# -*- coding: utf-8 -*-
import os
import sys
import pickle
from numpy import array

try:
  file_in = sys.argv[1]
except IndexError as ie:
  print("Usage: 'python %s <text_file.txt>'" % sys.argv[0])
  sys.exit(0)

file_out = file_in[:-4]+"_my.pkl"

dict1 = eval(open(file_in).read())

fo = open(file_out, 'wb')
pickle.dump(dict1, fo, 3)
fo.close()

exit(0)
