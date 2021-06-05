# Common imports
import os
import sys
import pickle
import yaml
import argparse

# Especific imports
import random
sys.path.append("../")
from configs.config import *
import cv2
import numpy as np
from sklearn.utils import shuffle
from keras.utils import to_categorical
from keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
import pprint

args = parse_args()

def openfile():
    try:
        file_in = args.pickle
    except IndexError as ie:
        print("Error: %s not found." % args.pickle)
        sys.exit(0)

    with open(file_in, "rb") as fi:
        mydict = pickle.load(fi)

    return mydict

short_clips = sorted(os.listdir(args.directory))
random.shuffle(short_clips)

train, val_test = np.split(short_clips, [int(len(short_clips)*args.train_perc)])
val,       test = np.split(val_test, [int(len(val_test)*args.val_perc)])

train_list = train.tolist()
val_list = val.tolist()
test_list = test.tolist()


print("\033[1;31m", end='')
print("Total number of short_clips found: {}".format(len(short_clips)))
print()
percent_train = ( (len(train_list)*100) / len(short_clips) )
print("Percentual train: {}%".format(round(percent_train,1 )))

percent_val = ( (len(val_list)*100) / len(short_clips) )
print("Percentual   val: {}%".format(round(percent_val,1 )))

percent_test = ( (len(test_list)*100) / len(short_clips) )
print("Percentual  test: {}%".format(round(percent_test,1 )))
print("\033[0m")


print("\033[1;37m"+"Running...."+"\033[0m")
if not os.path.isdir(args.npy_directory):
    os.mkdir(args.npy_directory)

cardict = openfile()

print("\033[1;36m"+"  Processing Train data ({} short_clips)..".format(len(train_list))+"\033[0m")
drive=[]
files=[]
carX = []
carY = []
cX=[]
carY_OH =[]
for drive in train_list:
    files = sorted(os.listdir(os.path.join(args.directory, drive)))
    cont = 0
    for arq in files:
        #print(args.directory + drive + "/" + arq)
        im_file = args.directory + drive + "/" + arq
        #print(im_file)
        #exit(0)
        img = cv2.imread(im_file)
        # print(sys.argv[1] + sys.argv[2][3:] + dir + "/" + arq)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227), interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = img_to_array(img)
        carX.append(img)
        carY.append(0 if cardict[drive]["target"][cont] == 0 else 1)
        # print(cardict[drive]["target"][cont])
        cont += 1

    files.clear()


print("  There are {} images e {} annotations in the dataset".format(len(carX), len(carY)) )
carY_OH = to_categorical(carY)

cX, carY_OH = shuffle(carX, carY_OH, random_state=0)

train_X = cX
train_Y = carY_OH

np.save(args.npy_directory + "Images_train.npy", train_X)
np.save(args.npy_directory + "Rotulos_train.npy", train_Y)

print("\033[1;37m  File saved!\033[0m\n")



print("\033[1;36m"+"  Processing Val data ({} short_clips)..".format(len(val_list))+"\033[0m")
drive=[]
files=[]
carX = []
carY = []
cX=[]
carY_OH =[]

for drive in val_list:
    files = sorted(os.listdir(os.path.join(args.directory, drive)))
    cont = 0
    for arq in files:
        #print(args.directory + drive + "/" + arq)
        im_file = args.directory + drive + "/" + arq
        #print(im_file)
        #exit(0)
        img = cv2.imread(im_file)
        # print(sys.argv[1] + sys.argv[2][3:] + dir + "/" + arq)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227), interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = img_to_array(img)
        carX.append(img)
        carY.append(0 if cardict[drive]["target"][cont] == 0 else 1)
        # print(cardict[drive]["target"][cont])
        cont += 1

    files.clear()


print("  There are {} images e {} annotations in the dataset".format(len(carX), len(carY)) )
carY_OH = to_categorical(carY)

cX, carY_OH = shuffle(carX, carY_OH, random_state=0)

val_X = cX
val_Y = carY_OH

np.save(args.npy_directory + "Images_val.npy", val_X)
np.save(args.npy_directory + "Rotulos_val.npy", val_Y)

print("\033[1;37m  File saved!\033[0m\n")


print("\033[1;36m"+"  Processing Test data ({} short_clips)..".format(len(test_list))+"\033[0m")
drive=[]
files=[]
carX = []
carY = []
cX=[]
carY_OH =[]

for drive in test_list:
    files = sorted(os.listdir(os.path.join(args.directory, drive)))
    cont = 0
    for arq in files:
        #print(args.directory + drive + "/" + arq)
        im_file = args.directory + drive + "/" + arq
        #print(im_file)
        #exit(0)
        img = cv2.imread(im_file)
        # print(sys.argv[1] + sys.argv[2][3:] + dir + "/" + arq)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227), interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = img_to_array(img)
        carX.append(img)
        carY.append(0 if cardict[drive]["target"][cont] == 0 else 1)
        # print(cardict[drive]["target"][cont])
        cont += 1

    files.clear()


print("  There are {} images e {} annotations in the dataset".format(len(carX), len(carY)) )
carY_OH = to_categorical(carY)

cX, carY_OH = shuffle(carX, carY_OH, random_state=0)

test_X = cX
test_Y = carY_OH

np.save(args.npy_directory + "Images_test.npy", test_X)
np.save(args.npy_directory + "Rotulos_test.npy", test_Y)

print("\033[1;37m  File saved!\033[0m\n")


sys.exit(0)
