# -*- coding: utf-8 -*-
import os
import sys
import pickle

try:
  file_in = sys.argv[1]
except IndexError as ie:
  print("Usage: 'python %s <pickle_file.pkl>'" % sys.argv[0])
  sys.exit(0)

with open(file_in, 'rb') as fi:
  mydict = pickle.load(fi)



print(mydict)
print("=====================")
print("Tipo: ", type(mydict))
print("Tamanho: ", len(mydict))

exit(0)
