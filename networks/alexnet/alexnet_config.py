# Common imports
import os
import sys
import glob
import yaml
import argparse

sys.path.append("../../")
from configs.config import *

# Especific imports
#import keras
from tensorflow import keras
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Activation,
    Dropout,
    Flatten,
    Conv2D,
    MaxPooling2D,
)
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import SGD
"""
    Input Parameters:
        input_shape = tupla com as dimensões de entrada (x,y,z)
        classes = número de instâncias de classificação
        activation_func = função de ativação
        activation_func_dense = função de ativação da camada densa
        filters_l1 = quantidade de filtros da camada 1
        filters_l2 = quantidade de filtros da camada 2
        filters_l3 = quantidade de filtros da camada 3
        filters_l4 = quantidade de filtros da camada 4
        filters_l5 = quantidade de filtros da camada 5
        kernel_size = tupla com dimensões do kernel (x,y)
        val_regularization = valor de regularização
        padding_conv = tipo de padding das camadas de convolução
        padding_max_pool = tipo de padding das camadas de max polling
        strides_conv = tupla com dimensões do kernel (x,y)
        strides_max_pool = tupla com dimensões do kernel (x,y)
        dropout_n1 = primeiro valor de dropout n1
        dropout_n2 = primeiro valor de dropout n2
        num_neural = número de neurônios da camada Dense
        directory = diretório onde será salvo o modelo da rede neural
"""

# if __name__ == "__main__":
args = parse_args()

## Parametrização da Rede
np.random.seed(1)

# Instantiate an empty model
model = Sequential(name="alexnet")

model.add(
    Conv2D(
        filters=args.filters_l1,
        input_shape=tuple(map(int, args.input_shape[1:-1].split(","))),
        activation=args.activation_func,
        kernel_size=tuple(map(int, args.kernel_size[1:-1].split(","))),
        strides=tuple(map(int, args.strides_conv[1:-1].split(","))),
        padding=args.padding_conv,
        kernel_regularizer=l2(args.val_regularization),
        bias_regularizer=l2(args.val_regularization),
    )
)
# model.add(

# 2nd Convolutional Layer
model.add(
    Conv2D(
        filters=args.filters_l2,
        kernel_size=tuple(map(int, args.kernel_size[1:-1].split(","))),
        activation=args.activation_func,
        strides=tuple(map(int, args.strides_conv[1:-1].split(","))),
        padding=args.padding_conv,
        kernel_regularizer=l2(args.val_regularization),
        bias_regularizer=l2(args.val_regularization),
    )
)
# Max Pooling
model.add(
    MaxPooling2D(
        pool_size=tuple(map(int, args.strides_max_pool[1:-1].split(","))),
        strides=tuple(map(int, args.strides_max_pool[1:-1].split(","))),
        padding=args.padding_max_pool,
    )
)

model.add(Dropout(args.dropout_n1))

# 3rd Convolutional Layer
model.add(
    Conv2D(
        filters=args.filters_l3,
        kernel_size=tuple(map(int, args.kernel_size[1:-1].split(","))),
        activation=args.activation_func,
        strides=tuple(map(int, args.strides_conv[1:-1].split(","))),
        padding=args.padding_conv,
        kernel_regularizer=l2(args.val_regularization),
        bias_regularizer=l2(args.val_regularization),
    )
)
# Max Pooling
model.add(
    MaxPooling2D(
        pool_size=tuple(map(int, args.strides_max_pool[1:-1].split(","))),
        strides=tuple(map(int, args.strides_max_pool[1:-1].split(","))),
        padding=args.padding_max_pool,
    )
)

# 4th Convolutional Layer
model.add(
    Conv2D(
        filters=args.filters_l4,
        kernel_size=tuple(map(int, args.kernel_size[1:-1].split(","))),
        activation=args.activation_func,
        strides=tuple(map(int, args.strides_conv[1:-1].split(","))),
        padding=args.padding_conv,
        kernel_regularizer=l2(args.val_regularization),
        bias_regularizer=l2(args.val_regularization),
    )
)
# Max Pooling
model.add(
    MaxPooling2D(
        pool_size=tuple(map(int, args.strides_max_pool[1:-1].split(","))),
        strides=tuple(map(int, args.strides_max_pool[1:-1].split(","))),
        padding=args.padding_max_pool,
    )
)

# 5th Convolutional Layer
model.add(
    Conv2D(
        filters=args.filters_l5,
        kernel_size=tuple(map(int, args.kernel_size[1:-1].split(","))),
        activation=args.activation_func,
        strides=tuple(map(int, args.strides_conv[1:-1].split(","))),
        padding=args.padding_conv,
        kernel_regularizer=l2(args.val_regularization),
        bias_regularizer=l2(args.val_regularization),
    )
)

# Passing it to a Fully Connected layer
model.add(Flatten())

model.add(Dropout(args.dropout_n2))

# Fully Connected Layers
model.add(Dense(args.num_neural, activation=args.activation_func))

# Output Layer
model.add(Dense(args.classes, activation=args.activation_func_dense))

print("\033[1;31m")
model.summary()
print("\033[0m")

## Network Compile model
# option 1
model.compile(
  optimizer = keras.optimizers.Adam(),
  loss = keras.losses.categorical_crossentropy,
  metrics = ["accuracy"]
)

# option 2
#model.compile(
#  optimizer = 'adam',
#  loss = 'binary_crossentropy',
#  metrics = ['accuracy']
#)

# option 3
#opt = SGD(lr=0.01, momentum=0.9)
#opt = SGD()
#model.compile(
#  optimizer = 'sgd',
#  loss = 'binary_crossentropy',
#  metrics = ['accuracy']
#)

if not os.path.isdir(args.directory):
  os.makedirs(args.directory)

model.save(args.directory + "alexnet_sem_treino.h5")

sys.exit(0)
