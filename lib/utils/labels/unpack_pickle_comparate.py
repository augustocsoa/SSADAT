# -*- coding: utf-8 -*-
import os
import sys
import pickle

try:
  file_in = sys.argv[1]
except IndexError as ie:
  print("Usage: 'python %s <pickle_file.pkl>'" % sys.argv[0])
  sys.exit(0)

file_out = file_in[:-4]+".txt"
file_out2 = file_in[:-4]+"-todos.txt"

with open(file_in, 'rb') as fi:
  mydict = pickle.load(fi)

#with open(file_out, 'w') as fo:
#  print(mydict, file=fo)

'''
video_list = ['LNT8NB2Dv-E', 'MpQRD8W9AI8', 'Pkbqo1FfhXA', 'R88JhqThHrg', 'RRdjvUcHo84',
              'SafZaefNbPY', 'TaKq4zsain0', 'U45XrAuG8ig', 'U733SSe0rYQ', 'Va7Nhr2U2RU',
              'WQIFMny6bBg', 'WT9VsYRM2lA', 'Wz6MqbWY3J8', 'lUqh2cWtw74', 'mMmP417u9BA',
              'x9KLVJK1bYY', 'xBw2JlZI3Us', 'xJ6j1oGguNo', 'xppvOHVVSWk']

'''

# Para usar uma lista comentada:
video_list = []
for video in (l for l in open('../../../comparate/video_list.txt') if not l.startswith('#')):
  #print(video.strip())
  video_list.append(video.strip())

#fo = open(file_out, 'w', encoding='utf8')

fo = open(file_out, 'w')
fo.write("{")
num = 0
contador = 0
for key in mydict.keys():
  if key.startswith(tuple(video_list)):
    #print("Pegando slice num: %d de video: %s "%(num,key))
    #print("Extraindo features de short clip: %s do arquivo .pkl"%key)
    fo.write("'")
    fo.write(key)
    fo.write("': ")
    fo.write(str(mydict[key]))
    fo.write(", ")
    contador += 1
    #print(key, new_dict[key])
  num += 1
fo.close()
# so para tirar a virgula...
with open(file_out, 'rb+') as filehandle:
  filehandle.seek(-2, os.SEEK_END)
  filehandle.truncate()
  filehandle.write(b'}')

print()
print("Numero total de short clips do arquivo pickle: %d"%num)
print("Numero total de short clips da lista dos videos escolhidos: %d"%contador)

# caso queira ver todos os short clips descomentar o bloco abaixo
'''
fo2 = open(file_out2, 'w')
fo2.write("{")
num = 1
for key in mydict.keys():
  #print("Pegando slice num: %d de video: %s "%(num,key))
  fo2.write("'")
  fo2.write(key)
  fo2.write("': ")
  fo2.write(str(mydict[key]))
  fo2.write(",\n ")
  num += 1
    #print(key, new_dict[key])
fo2.close()
# so para tirar a virgula...
with open(file_out2, 'rb+') as filehandle:
  filehandle.seek(-2, os.SEEK_END)
  filehandle.truncate()
  filehandle.write(b'}')
'''


sys.exit(0)
