#!/bin/bash
CWD=$(pwd)
FILE=A3D_labels.pkl

if [ -f "$FILE" ]; then
    PH=$CWD
else
    PH=$CWD/datasets
fi

python3 $PH/unpack_pickle_comparate.py $PH/A3D_labels.pkl
sed -i 's/_0000/_0/g' A3D_labels.txt
sed -i "s/'idx': '000/'idx': '/g" A3D_labels.txt
python3 $PH/pack_pickle.py $PH/A3D_labels.txt
mv A3D_labels_my.pkl labels_comparate.pkl
