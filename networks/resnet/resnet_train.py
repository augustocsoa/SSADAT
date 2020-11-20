# Common imports
import os
import sys
import glob
import yaml
import argparse

# Especific imports
sys.path.append("../../")
from configs.config import *
import numpy as np
from tensorflow import keras
import json
import pickle

"""
    Input Parameters:
        batch_size = tamanho do conjunto de dados de treinamento
        epochs = número de epocas de treinamento
        data_dir = diretório do conjunto de dados
        directory = diretório onde salvará o modelo treinado

"""

args = parse_args()

model = keras.models.load_model(args.directory + "resnet_sem_treino.h5")

train_X = np.load(args.data_dir + "Images_train.npy")
train_Y = np.load(args.data_dir + "Rotulos_train.npy")
val_X = np.load(args.data_dir + "Images_val.npy")
val_Y = np.load(args.data_dir + "Rotulos_val.npy")

print("\033[1;31m")
print("Training:   ", train_X.shape, train_Y.shape)
print("Validation: ", val_X.shape, val_Y.shape)
print("\033[0m")

model_train = model.fit(
    train_X,
    train_Y,
    batch_size=args.batch_size,
    epochs=args.epochs,
    verbose=1,
    validation_data=(val_X, val_Y),
)

if not os.path.isdir(args.directory):
    os.mkdir(args.directory)

model.save(args.directory + "resnet_train.h5")
print("Model file saved.")

file_out = "train-history.pkl"
fo = open(file_out, 'wb')
pickle.dump(model_train.history, fo, 3)
fo.close()

#with open('train-history.json', 'w') as fjs:
#    json.dump(model_train.history, fjs,  separators=(', ', ': '), indent=2)

print("History file saved.")

sys.exit(0)
