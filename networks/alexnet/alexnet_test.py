# Common imports
import os
import sys
import glob
import yaml
import argparse

sys.path.append("../../")
from configs.config import *

# Especific imports
import numpy as np
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import pandas as pd
"""
    Input Parameters:
        directory = diretório onde foi salvo o modelo treinado
        data_dir = diretório do conjunto de dados
        classes =  número de classes

"""


args = parse_args()

print(type(args))
print(args)

model = keras.models.load_model(args.directory + "alexnet_train.h5")

test_X = np.load(args.data_dir + "Images_test.npy")
test_Y = np.load(args.data_dir + "Rotulos_test.npy")

test_eval = model.evaluate(test_X, test_Y, verbose=1)

print("\033[1;37;41m Results:\033[0m")
print("Test loss: {:.3f}".format(test_eval[0]))
print("Test accuracy: {:.3f}".format(test_eval[1]))


predicted_classes = model.predict(test_X)
predicted_classes = np.argmax(np.round(predicted_classes), axis=1)
predicted_classes = to_categorical(predicted_classes)

target_names = ["Class {}".format(i) for i in range(args.classes)]
target_names2 = ["Classe {}".format(i) for i in args.class_names.split(",")]

print("\033[1;37;41m Report:\033[0m")
print(classification_report(test_Y, predicted_classes, zero_division=0, target_names=target_names))

file_out1 = "../../lib/article/tabelas/alexnet_test_table.tex"
file_out2 = "../../lib/article/tabelas/alexnet_test_other.txt"
f1 = open(file_out1, 'w')
f2 = open(file_out2, 'w')

C = ''' modelo de parametros da função para imprimir no arquivo .tex
DataFrame.to_latex(buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, bold_rows=False, column_format=None, longtable=None, escape=None, encoding=None, decimal='.', multicolumn=None, multicolumn_format=None, multirow=None, caption=None, label=None)
'''

orig_stdout = sys.stdout
sys.stdout = f1
report = classification_report(
    test_Y,
    predicted_classes,
    zero_division=0,
    target_names=target_names2,
    output_dict=True,
)
df = pd.DataFrame(report).transpose()
print(
    df.to_latex(
        header=True,
        index=True,
        multirow=True,
        caption="Classification Report - AlexNet",
        label="table:Tab1",
    )
)
f1.close()

sys.stdout = orig_stdout

test_label = np.argmax(test_Y, axis=1)
predicted_classes = np.argmax(predicted_classes, axis=1)

cm = confusion_matrix(test_label, predicted_classes)

fp = cm.sum(axis=0) - np.diag(cm)
fn = cm.sum(axis=1) - np.diag(cm)
tp = np.diag(cm)
tn = cm.sum() - (fp + fn + tp)

sensitivity = tp / (tp + fn)
specificity = tn / (tn + fp)
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)

print("===  AlexNet out  ===")
print("Sensitivity: {:.3f}".format(sensitivity[0]))
print("Specificity: {:.3f}".format(specificity[0]))
print("Precision:   {:.3f}".format(precision[0]))
print("Accuracy:    {:.3f}".format(accuracy[0]))
print("Test loss:   {:.3f}".format(test_eval[0]))

sys.stdout = f2
print("===  AlexNet out  ===")
print("Sensitivity: {:.3f}".format(sensitivity[0]))
print("Specificity: {:.3f}".format(specificity[0]))
print("Precision:   {:.3f}".format(precision[0]))
print("Accuracy:    {:.3f}".format(accuracy[0]))
print("Test loss:   {:.3f}".format(test_eval[0]))
print("=====================")
f2.close()
sys.exit(0)
