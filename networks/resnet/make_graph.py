# Common imports
import os
import sys
import json
import numpy as np
import math
#import pprint
import matplotlib as mpl
# Use the pgf backend (must be done before import pyplot interface)
mpl.use('pgf')
import matplotlib.pyplot as plt
import pickle

#r"""
#print(plt.rcParams.keys())
#exit(0)

plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": True,
    "font.size": 8,
    "figure.titlesize": 10,
    "figure.titleweight": 'bold',
    "pgf.preamble": "\n".join([
      r"\usepackage[utf8x]{inputenc}",
      r"\usepackage[T1]{fontenc}",
    ]),
})

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12


plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

""" #"""

#plt.style.use('default')
#plt.style.use('classic')
#plt.style.use('ggplot')
#plt.style.use('seaborn')
#plt.style.use('Solarize_Light2')
#plt.style.use('bmh')
#plt.style.use('tex')

file_in = "train-history.pkl"
with open(file_in, 'rb') as fi:
  history = pickle.load(fi)

#with open('train-history.json', 'r') as histfile:
#    history = json.loads(histfile.read())

#pprint.pprint(history)

label_0 = list(history.keys())[0]
values_0 = list(history.values())[0]

label_1 = list(history.keys())[1]
values_1 = list(history.values())[1]

label_2 = list(history.keys())[2]
values_2 = list(history.values())[2]

label_3 = list(history.keys())[3]
values_3 = list(history.values())[3]

epochs = list(range(1, len(values_0)+1))

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(6,7), gridspec_kw={'hspace': 0.4, 'wspace': 0.3})
fig.suptitle('Curvas de aprendizado ')

ax1.set_title('Comparação da acurácia, Treino e Validação')
ax1.set_facecolor('#eafff5')
ax1.plot(epochs, values_1, color='r', linewidth=1.0, label="Treino")
ax1.plot(epochs, values_3, color='b', linewidth=1.0, label="Validação")
ax1.set_xlabel('épocas')
ax1.set_ylabel('acurácia')
ax1.fill_between(epochs, values_1, values_3, color="darkviolet", alpha=0.2)
xticks = np.arange(min(epochs), max(epochs)+1, 3.0)
xticks = np.append(xticks, [max(epochs)], axis=None)
ax1.set_xticks(xticks)
#ax1.set_yticks()
#ax1.set_xlim()
#ax1.set_ylim([0.2, 1])
#ax1.set_yscale('linear')
ax1.grid(color='k', alpha=0.5, linestyle='dotted', linewidth=0.6)
ax1.legend(loc="lower right")
#ax1.legend(loc="lower right", shadow=True, title="Legenda", fancybox=True, framealpha=0.5)


ax2.set_title('Comparação da perca, Treino e  Validação')
ax2.set_facecolor('#eafff5')
ax2.plot(epochs, values_0, color='r', linewidth=1.0, label="Treino")
ax2.plot(epochs, values_2, color='b', linewidth=1.0, label="Validação")
ax2.set_xlabel('épocas')
ax2.set_ylabel('perca')
ax2.fill_between(epochs, values_0, values_2, color="darkviolet", alpha=0.2)
xticks = np.arange(min(epochs), max(epochs)+1, 3.0)
xticks = np.append(xticks, [max(epochs)], axis=None)
ax2.set_xticks(xticks)
#ax2.set_yticks()
#ax2.set_xlim()
ax2.set_ylim([0, 1])
#ax2.set_yscale('logit')
ax2.grid(color='k', alpha=0.5, linestyle='dotted', linewidth=0.6)
ax2.legend(loc="upper right")
#ax2.legend(loc="lower right", shadow=True, title="Legenda", fancybox=True, framealpha=0.5)


plt.savefig('resnet_train.png', format='png', dpi=150)

plt.savefig(
  "../../lib/article/figuras/resnet_train.pgf", format="pgf", bbox_inches="tight"
)

#plt.show()

sys.exit(0)
