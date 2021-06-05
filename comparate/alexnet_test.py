# Common imports
import os
import sys
import glob
import yaml
import cv2
import argparse
import pickle

sys.path.append("./")
from configs.config import *

# Especific imports
import numpy as np
from sklearn.utils import shuffle
from tensorflow import keras
from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.utils import to_categorical


args = parse_args()

print(type(args))
print(args)

model_final = keras.models.load_model(args.directory_models + "alexnet_train.h5")

cont = 0
if not os.path.isdir("comparate/saidas_rede/"):
    print("The rec_videos directory does not exist! creating..\n")
    os.makedirs("comparate/saidas_rede/")


for drive in sorted(os.listdir(args.directory_images)):
    files = sorted(os.listdir(os.path.join(args.directory_images, drive)))
    print(drive)
    carX = []
    for arq in files:
        im_file = args.directory_images + drive + "/" + arq
        img = cv2.imread(im_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227), interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = img_to_array(img)
        carX.append(img)

    carX = np.array(carX)

    predicted_classes = model_final.predict(carX)
    predicted_classes = np.argmax(np.round(predicted_classes), axis=1)
    predicted = predicted_classes
    np.save("comparate/saidas_rede/short_" + str(cont) + ".npy", predicted)
    cont += 1
    files.clear()

sys.exit(0)
