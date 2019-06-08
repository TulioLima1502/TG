#!/usr/bin/env python
import argparse
import sys
import numpy as np
import h5py
import json
import os
import math
import matplotlib.pyplot as plt
import matplotlib
from keras.models import model_from_json
import random
import time
from dask_generator import concatenate


# ***** main loop *****
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Path viewer')
  parser.add_argument('model', type=str, help='Path to model definition json. Model weights should be on the same path.')
  parser.add_argument('--list', dest='DataValidation', action='store', help='Set a list of indices with divided dataset to validation')
  args = parser.parse_args()
  
  # Loading Model
  with open(args.model, 'r') as jfile:
    model = model_from_json(json.load(jfile))
  model.compile("sgd", "mse")
  weights_file = args.model.replace('json', 'keras')
  model.load_weights(weights_file)

  # Loading Data List to Validation
  DataIndex = []
  Data = []

  DataValidation = open(args.DataValidation, "r")
  Data = DataValidation.readlines()
  for a in Data:
    DataIndex.append(int(a))
  labels = DataIndex

  validation_path = [
    './extract-bagfiles/retas_1.h5',
    './extract-bagfiles/retas_2.h5',
    #'./extract-bagfiles/curvas_suaves_1.h5',
    #'./extract-bagfiles/curvas_suaves_2.h5',
    #'./extract-bagfiles/curvas_em_T_1.h5',
    #'./extract-bagfiles/curvas_em_T_1.h5',
  ]

  c5x, angle, speed, filters, hdf5_camera = concatenate(validation_path, time_len=1)
  graph_pred = np.array(0)
  erroNRMSE = np.array(0)
  graph_erro = np.array(0)

  max_and_min=np.array(0)

  labels_set = set(labels)

  for i in labels_set:
    max_and_min = np.append(max_and_min,np.copy(angle[i-1:i])[:, None][0][0])
  print("O valor maximo e minimo sao {0} e {1} respectivamente...".format(np.amax(max_and_min)/507.45,np.amin(max_and_min)/507.45))

  maximo = np.amax(max_and_min)/507.45
  minimo = np.amin(max_and_min)/507.45
  matriz_confusao=np.zeros((51,51))

  for i in sorted(labels_set):
    #print(i)
    for es, ee, x in c5x:
      if i >= es and i < ee:
        Imagem = x[i-es]
        angle
        break
    #print Imagem.shape
    #time.sleep(1)
    predicted_steers = model.predict(Imagem[None, :, :, :].transpose(0, 1, 2, 3))[0][0]
    angle_steers = np.copy(angle[i-1:i])[:, None][0][0]
    predicted_steers = predicted_steers/507.45
    angle_steers = angle_steers/507.45
    #print predicted_steers, angle_steers

    if predicted_steers > 1:
      predicted_steers=1
    elif predicted_steers < -1:
      predicted_steers=-1
    
    if angle_steers > 1:
      angle_steers=1
    elif angle_steers < -1:
      angle_steers=-1

    graph_pred = np.append(graph_pred,((angle_steers-predicted_steers)** 2))
    graph_erro = np.append(graph_erro,np.sqrt(np.average(graph_pred))/(maximo-minimo))

    print np.sqrt(np.average(graph_pred))/(maximo-minimo)

    erroNRMSE = np.append(erroNRMSE,(np.sqrt(((angle_steers-predicted_steers)** 2))/(maximo-minimo)))
    matriz_confusao[int(predicted_steers*25)+25][int(angle_steers*25)+25]=matriz_confusao[int(predicted_steers*25)+25][int(angle_steers*25)+25]+1

  #matriz_confusao[10][10]=0
  #saving_data = np.array([graph_x,graph_y,graph_predicted_y,erroNRMSE,graph_erro])
  #np.savetxt('data.csv', zip(graph_x,graph_y,graph_predicted_y,erroNRMSE,graph_erro), delimiter=',',fmt='%.18f')

  plt.figure("angulo,angulo_pred and NRMSE")
  plt.plot(graph_erro,'k-')
  plt.ylabel('Erro Normalizado (0 a 1)[0% - 100%]')
  plt.xlabel('Amostras')
  plt.show()

  print(np.amax(erroNRMSE))
  np.savetxt('data.mat', matriz_confusao)
  norm = matplotlib.colors.Normalize(vmin=0, vmax=200)
  plt.imshow(matriz_confusao, cmap='gray_r',norm=norm)
  plt.ylabel('Angulo Predito [-1 a 1]')
  plt.xlabel('Angulo Praticado [-1 a 1]')
  plt.colorbar()
  plt.show()