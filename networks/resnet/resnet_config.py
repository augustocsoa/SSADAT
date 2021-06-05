# Common imports
import os
import sys
import glob
import yaml
import argparse

sys.path.append("../../")
from configs.config import *

# Especific imports
from tensorflow import keras
import numpy as np
from tensorflow.keras.optimizers import SGD

"""
    Input Parameters:
        input_shape = tupla com as dimensões de entrada (x,y,z)
        classes = número de instâncias de classificação
        directory = diretório onde será salvo o modelo da rede neural

"""

# if __name__ == "__main__":
args = parse_args()

## Parametrização da Rede

# Entrada da Rede
# print(tuple(map(int, args.input_shape[1:-1].split(","))))
input = keras.layers.Input(shape=tuple(map(int, args.input_shape[1:-1].split(","))))
# input = keras.layers.Input(shape=(None, None, 3))


# Bloco Identidade


def identity_block(input, kernel_size, filters, stage, block):

    # Variables
    filters1, filters2, filters3 = filters
    conv_name_base = "res" + str(stage) + block + "_branch"
    bn_name_base = "bn" + str(stage) + block + "_branch"
    # Create layers
    output = keras.layers.Conv2D(
        filters1, (1, 1), kernel_initializer="he_normal", name=conv_name_base + "2a"
    )(input)
    output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + "2a")(output)
    output = keras.layers.Activation("relu")(output)
    output = keras.layers.Conv2D(
        filters2,
        kernel_size,
        padding="same",
        kernel_initializer="he_normal",
        name=conv_name_base + "2b",
    )(output)
    output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + "2b")(output)
    output = keras.layers.Activation("relu")(output)
    output = keras.layers.Conv2D(
        filters3, (1, 1), kernel_initializer="he_normal", name=conv_name_base + "2c"
    )(output)
    output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + "2c")(output)
    output = keras.layers.add([output, input])
    output = keras.layers.Activation("relu")(output)
    # Return a block
    return output


# Bloco de Convolução
def conv_block(input, kernel_size, filters, stage, block, strides=(2, 2)):
    # Variables
    filters1, filters2, filters3 = filters
    conv_name_base = "res" + str(stage) + block + "_branch"
    bn_name_base = "bn" + str(stage) + block + "_branch"
    # Create block layers
    output = keras.layers.Conv2D(
        filters1,
        (1, 1),
        strides=strides,
        kernel_initializer="he_normal",
        name=conv_name_base + "2a",
    )(input)
    output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + "2a")(output)
    output = keras.layers.Activation("relu")(output)
    output = keras.layers.Conv2D(
        filters2,
        kernel_size,
        padding="same",
        kernel_initializer="he_normal",
        name=conv_name_base + "2b",
    )(output)
    output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + "2b")(output)
    output = keras.layers.Activation("relu")(output)
    output = keras.layers.Conv2D(
        filters3, (1, 1), kernel_initializer="he_normal", name=conv_name_base + "2c"
    )(output)
    output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + "2c")(output)
    shortcut = keras.layers.Conv2D(
        filters3,
        (1, 1),
        strides=strides,
        kernel_initializer="he_normal",
        name=conv_name_base + "1",
    )(input)
    shortcut = keras.layers.BatchNormalization(axis=3, name=bn_name_base + "1")(
        shortcut
    )
    output = keras.layers.add([output, shortcut])
    # output = keras.layers.add([output, input])
    output = keras.layers.Activation("relu")(output)
    # Return a block
    return output


# Camadas Intermediárias
output = keras.layers.ZeroPadding2D(padding=3, name="padding_conv1")(input)
output = keras.layers.Conv2D(
    64,
    (7, 7),
    strides=(2, 2),
    padding="valid",
    kernel_initializer="he_normal",
    use_bias=False,
    name="conv1",
)(output)
output = keras.layers.BatchNormalization(axis=3, epsilon=1e-5, name="bn_conv1")(output)
output = keras.layers.Activation("relu", name="conv1_relu")(output)
output = keras.layers.ZeroPadding2D(padding=(1, 1), name="pool1_pad")(output)
output = keras.layers.MaxPooling2D((3, 3), strides=(2, 2), name="pool1")(output)
output = conv_block(output, 3, [64, 64, 256], stage=2, block="a", strides=(1, 1))
output = identity_block(output, 3, [64, 64, 256], stage=2, block="b")
output = identity_block(output, 3, [64, 64, 256], stage=2, block="c")

output = conv_block(output, 3, [128, 128, 512], stage=3, block="a")
output = identity_block(output, 3, [128, 128, 512], stage=3, block="b")
output = identity_block(output, 3, [128, 128, 512], stage=3, block="c")
output = identity_block(output, 3, [128, 128, 512], stage=3, block="d")

output = conv_block(output, 3, [256, 256, 1024], stage=4, block="a")
output = identity_block(output, 3, [256, 256, 1024], stage=4, block="b")
output = identity_block(output, 3, [256, 256, 1024], stage=4, block="c")
output = identity_block(output, 3, [256, 256, 1024], stage=4, block="d")
output = identity_block(output, 3, [256, 256, 1024], stage=4, block="e")
output = identity_block(output, 3, [256, 256, 1024], stage=4, block="f")

output = conv_block(output, 3, [512, 512, 2048], stage=5, block="a")
output = identity_block(output, 3, [512, 512, 2048], stage=5, block="b")
output = identity_block(output, 3, [512, 512, 2048], stage=5, block="c")

output = keras.layers.GlobalAveragePooling2D(name="pool5")(output)
output = keras.layers.Dense(args.classes, activation="softmax", name="fc1000")(output)

# Criação do Modelo
model = keras.models.Model(inputs=input, outputs=output, name="resnet50")

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

model.save(args.directory + "resnet_sem_treino.h5")

sys.exit(0)
