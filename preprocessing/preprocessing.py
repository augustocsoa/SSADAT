# Common imports
import os
import sys
import pickle
import yaml
import argparse

# Especific imports
sys.path.append("../")
from configs.config import *
import cv2
import numpy as np
from sklearn.utils import shuffle
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split

"""
    Input Parameters:
        directory = diretório onde se encontram os shor clips
        pickle = diretório onde se encontram as anotações
        npy_directory = diretório onde os arquivos npy serão salvos
        test_percenty = percentual de teste


"""

def equalize_hist(img):
  for c in range(0, 2):
    img[:,:,c] = cv2.equalizeHist(img[:,:,c])
  return img

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

cardict = openfile()

carX = []
carY = []

print("Running....")

for drive in sorted(os.listdir(args.directory)):

    files = sorted(os.listdir(os.path.join(args.directory, drive)))
    #print(files)
    #files.remove('.directory')
    #print(files)
    #exit(0)
    cont = 0
    for arq in files:
        #print(args.directory + drive + "/" + arq)
        im_file = args.directory + drive + "/" + arq
        #print(im_file)
        # exit(0)
        img = cv2.imread(im_file)
        # print(sys.argv[1] + sys.argv[2][3:] + dir + "/" + arq)
        img = equalize_hist(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227), interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
        img = img_to_array(img)
        carX.append(img)
        carY.append(0 if cardict[drive]["target"][cont] == 0 else 1)
        # print(cardict[drive]["target"][cont])
        cont += 1

    files.clear()

#exit(0)

print(
    "There are {} images e {} annotations in the dataset".format(len(carX), len(carY))
)

carY_OH = to_categorical(carY)

#for i in range(0, len(carY)):
#    print("Original label:", carY[i])
#    print("After conversion to one-hot:", carY_OH[i])

cX, carY_OH = shuffle(carX, carY_OH, random_state=0)
### test_eval
# cX = cX[0:50]
# cY = cY[0:50]
####


# split the raw data into 80% for training and 20% for test
train_X, test_X, train_Y, test_Y = train_test_split(
    cX, carY_OH, test_size=args.test_percenty, random_state=13
)

# train_X, test_X, train_Y, test_Y = train_test_split(
#    cX, cY, test_size=args.test_percenty, random_state=13
# )

print("-=-=-= First split stage =-=-=-")
print("train_X: ", len(train_X))
print("test_X: ", len(test_X))

percent_class_train = (len(train_X) * 100) / len(carX)
print("Percentual train: {:.2f}%".format(percent_class_train))
percent_class_test = (len(test_X) * 100) / len(carX)
print("Percentual  test: {:.2f}%".format(percent_class_test))

# split the training data into 80% for training and 20% for validation
train_X, val_X, train_Y, val_Y = train_test_split(
    train_X, train_Y, test_size=args.val_percenty, random_state=13
)

print("-=-=-= Second split stage =-=-=-")
print("train_X: ", len(train_X))
print("test_X: ", len(test_X))
print("val_X: ", len(val_X))

print("\033[1;31m")
percent_class_train = (len(train_X) * 100) / len(carX)
print("Percentual train: {}%".format(round(percent_class_train, 1)))
percent_class_val = (len(val_X) * 100) / len(carX)
print("Percentual   val: {}%".format(round(percent_class_val, 1)))
percent_class_test = (len(test_X) * 100) / len(carX)
print("Percentual  test: {}%".format(round(percent_class_test, 1)))
print("\033[0m")

#exit(0)

print("Writing to files..")

if not os.path.isdir(args.npy_directory):
    os.mkdir(args.npy_directory)

np.save(args.npy_directory + "Images_train.npy", train_X)
np.save(args.npy_directory + "Rotulos_train.npy", train_Y)

np.save(args.npy_directory + "Images_test.npy", test_X)
np.save(args.npy_directory + "Rotulos_test.npy", test_Y)

np.save(args.npy_directory + "Images_val.npy", val_X)
np.save(args.npy_directory + "Rotulos_val.npy", val_Y)

print("\033[1;37mDone!\033[0m")

sys.exit(0)
