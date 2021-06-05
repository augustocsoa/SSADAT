# Passos para executar os códigos

## Passo 1 (Preparação):
Editar o arquivo datasets/A3D/video_list.txt
e descomentar os videos que vão compor a a base
total dos datasets

```bash
cd lib/utils/labels
./generates_new_pickle_file.sh
cp labels.pkl ../../../annotations/A3D/
cd ../../../
```

```bash
python3 download_videos.py --load_config configs/download.yaml
python3 split_videos2frames.py --load_config configs/videos2frames.yaml
python3 extract_short_clips.py --load_config configs/short_clips.yaml
```

## Passo 2 (Pre Processamento):
```bash
cd preprocessing
python3 preprocessing.py --load_config ../configs/preprocessing.yaml
cd ..
```

## Passo 3 (Rodar rede neural AlexNet)
```bash
cd networks/alexnet/
python3 alexnet_config.py --load_config ../../configs/alexnet_config.yaml

python3 alexnet_train.py --load_config ../../configs/alexnet_train.yaml
python3 make_graph.py

python3 alexnet_test.py --load_config ../../configs/alexnet_test.yaml
cd ../..
```
## Passo 4 (Rodar rede neural ResNet)
```bash
cd networks/resnet/
python3 resnet_config.py --load_config ../../configs/resnet_config.yaml

python3 resnet_train.py --load_config ../../configs/resnet_train.yaml
python3 make_graph.py

python3 resnet_test.py --load_config ../../configs/resnet_test.yaml
cd ../..
```
## Passo 5 (Reconstruir os videos marcados _True labels_)
```bash
python3 mark_short_clips.py --load_config configs/mark_short_clips.yaml

python3 make_videos.py --load_config configs/make_videos.yaml
```

## Passo 5 (Reconstruir os videos usando rede treinada)
```bash
cd comparate/

python3 comparate_alexnet.py

python3 comparate_resnet.py

```
