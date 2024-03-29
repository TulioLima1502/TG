#!/usr/bin/env python
import argparse
import sys
import numpy as np
import h5py
import pygame
from pygame.locals import *
import json
import os
import math
import matplotlib.pyplot as plt
import matplotlib
from keras.models import model_from_json
import random
import time

pygame.init()
size = (320, 240)

pygame.display.set_caption("comma.ai data viewer")
screen = pygame.display.set_mode(size)

camera_surface = pygame.surface.Surface((320,240),0,24).convert()

dimensions = [320, 240]
orientation = pygame.display.set_mode(dimensions)

orientation.fill((255, 255, 255))

circulo = [10, 10, 100, 100]

# ***** get perspective transform for images *****
from skimage import transform as tf

rsrc = \
 [[43.45456230828867, 118.00743250075844],
  [104.5055617352614, 69.46865203761757],
  [114.86050156739812, 60.83953551083698],
  [129.74572757609468, 50.48459567870026],
  [132.98164627363735, 46.38576532847949],
  [301.0336906326895, 98.16046448916306],
  [238.25686790036065, 62.56535881619311],
  [227.2547443287154, 56.30924933427718],
  [209.13359962247614, 46.817221154818526],
  [203.9561297064078, 43.5813024572758]]
rdst = \
 [[10.822125594094452, 1.42189132706374],
  [21.177065426231174, 1.5297552836484982],
  [25.275895776451954, 1.42189132706374],
  [36.062291434927694, 1.6376192402332563],
  [40.376849698318004, 1.42189132706374],
  [11.900765159942026, -2.1376192402332563],
  [22.25570499207874, -2.1376192402332563],
  [26.785991168638553, -2.029755283648498],
  [37.033067044190524, -2.029755283648498],
  [41.67121717733509, -2.029755283648498]]

tform3_img = tf.ProjectiveTransform()
tform3_img.estimate(np.array(rdst), np.array(rsrc))

def perspective_tform(x, y):
  p1, p2 = tform3_img((x,y))[0]
  return p2, p1

# ***** functions to draw lines *****
def draw_pt(img, x, y, color, sz=1):
  row, col = perspective_tform(x, y)
  if row >= 0 and row < img.shape[0] and\
     col >= 0 and col < img.shape[1]:
    img[int(row)-int(sz):int(row)+int(sz), int(col)-int(sz):int(col)+int(sz)] = color

def draw_path(img, path_x, path_y, color):
  for x, y in zip(path_x, path_y):
    draw_pt(img, x, y, color)

# ***** functions to draw predicted path *****

def calc_curvature(v_ego, angle_steers, angle_offset=0):
  deg_to_rad = np.pi/180.
  slip_fator = 0.0014 # slip factor obtained from real data
  steer_ratio = 15.3  # from http://www.edmunds.com/acura/ilx/2016/road-test-specs/
  wheel_base = 2.67   # from http://www.edmunds.com/acura/ilx/2016/sedan/features-specs/

  angle_steers_rad = (angle_steers - angle_offset) * deg_to_rad
  curvature = angle_steers_rad/(steer_ratio * wheel_base * (1. + slip_fator * v_ego**2))
  return -angle_steers

def calc_lookahead_offset(v_ego, angle_steers, d_lookahead, angle_offset=0):
  #*** this function returns the lateral offset given the steering angle, speed and the lookahead distance
  curvature = calc_curvature(v_ego, angle_steers, angle_offset)

  # clip is to avoid arcsin NaNs due to too sharp turns
  y_actual = d_lookahead * np.tan(np.arcsin(np.clip(d_lookahead * curvature, -0.999, 0.999))/2.)
  return y_actual, curvature

def draw_path_on(img, speed_ms, angle_steers, color=(0,0,255)):
  path_x = np.arange(0., 100.1, 0.5)
  path_y, _ = calc_lookahead_offset(speed_ms, angle_steers, path_x)
  draw_path(img, path_x, path_y, color)

# ***** main loop *****
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Path viewer')
  parser.add_argument('model', type=str, help='Path to model definition json. Model weights should be on the same path.')
  parser.add_argument('--dataset', type=str, default="terceiro-curvas.h5", help='Dataset/video clip name')
  args = parser.parse_args()

  with open(args.model, 'r') as jfile:
    model = model_from_json(json.load(jfile))

  model.compile("sgd", "mse")
  weights_file = args.model.replace('json', 'keras')
  model.load_weights(weights_file)

  # default dataset is the validation data on the highway
  dataset = args.dataset
  skip = 300

  #log = h5py.File("log/2016-06-08--11-46-01.h5", "r")
  cam = h5py.File("validacao_retas_2andar_noite.h5", "r")

  print cam.keys()
  graph_x = np.array(0)
  graph_y = np.array(0)
  graph_predicted_y = np.array(0)
  graph_pred = np.array(0)
  erroNRMSE = np.array(0)
  graph_erro = np.array(0)

  max_and_min=np.array(0)
  
  position_x = []
  position_y = []
  angulos = [0]
  #plt.figure("angulo")
  #plt.plot(graph_x,graph_y)
  #plt.ylabel('Estercamento (-1 a 1)')
  #plt.xlabel('Amostras')
  #plt.show()
  #plt.pause(0.00001)
  #plt.clf()
  #exit()
  angulo_aux = 0
  for i in range(0, cam['X'].shape[0]):
    max_and_min = np.append(max_and_min,cam['angle'][i])

  print("O valor maximo e minimo sao {0} e {1} respectivamente...".format(np.amax(max_and_min)/507.45,np.amin(max_and_min)/507.45))

  maximo = np.amax(max_and_min)/507.45
  minimo = np.amin(max_and_min)/507.45

  matriz_confusao=np.zeros((21,21))

  # skip to highway
  for i in range(0, cam['X'].shape[0]):
  #randoms = []
  #randoms = range(0, cam['X'].shape[0])
  #random.shuffle(randoms)
  #print randoms
  #for i in randoms:

    #if i%100 == 0:
    #  print "%.2f seconds elapsed" % (i/100.0)
    img = cam['X'][i]
    #print img[None, :, :, :].transpose(0, 3, 1, 2)
    predicted_steers = model.predict(img[None, :, :, :].transpose(0, 1, 2, 3))[0][0]
    predicted_steers = predicted_steers/507.45
    if predicted_steers > 1:
      predicted_steers=1
    elif predicted_steers < -1:
      predicted_steers=-1
    #predicted_steers = -1 + (1 + 1)*((predicted_steers + 5023)/(5023+5023))
    #print predicted_steers

    angle_steers = cam['angle'][i]
    angle_steers = angle_steers/507.45
    if angle_steers > 1:
      angle_steers=1
    elif angle_steers < -1:
      angle_steers=-1
    #angle_steers = -1 + (1 + 1)*((angle_steers + 5023)/(5023+5023))
    speed_ms = cam['speed'][i]
    #print img.shape , cam['dataset_index'][i]
    pygame.surfarray.blit_array(camera_surface, img.swapaxes(0, 2))
    screen.blit(camera_surface, (0,0))

    pygame.draw.ellipse(orientation, (0, 0, 0), circulo, 2)
    x = angle_steers
    if x > 1.0:
      x=1
    elif x < -1.0:
      x=-1
    y = math.sqrt(1 - (x*x))
    if x!=0:
      angulo = math.degrees(math.atan(abs(y/x)))
    else:
      angulo = 90
    if x<=0:
      angulo = 180 - angulo
    x = 60 - 50 * math.cos(math.radians(angulo))
    y = 60 - 50 * math.sin(math.radians(angulo))
    
    graph_x = np.append(graph_x,i)
    graph_y = np.append(graph_y,angle_steers)
     
    pygame.draw.line(orientation, (255, 0, 0), [60, 60], [x, y], 1)

    x = predicted_steers
    if x > 1.0:
      x=1
    elif x < -1.0:
      x=-1
    y = math.sqrt(1 - (x*x))
    if x!=0:
      angulo = math.degrees(math.atan(abs(y/x)))
    else:
      angulo = 90
    if x<=0:
      angulo = 180 - angulo
    x = 60 - 50 * math.cos(math.radians(angulo))
    y = 60 - 50 * math.sin(math.radians(angulo))
    
    graph_pred = np.append(graph_pred,((angle_steers-predicted_steers)** 2))
    graph_predicted_y = np.append(graph_predicted_y,predicted_steers)

    #print angle_steers,predicted_steers
    
    pygame.draw.line(orientation, (0, 255, 0), [60, 60], [x, y], 1)
    pygame.display.flip()
    graph_erro = np.append(graph_erro,np.sqrt(np.average(graph_pred))/(maximo-minimo))
    print np.sqrt(np.average(graph_pred))/(maximo-minimo)
    erroNRMSE = np.append(erroNRMSE,(np.sqrt(((angle_steers-predicted_steers)** 2))/(maximo-minimo)))
    matriz_confusao[int(predicted_steers*10)+10][int(angle_steers*10)+10]=matriz_confusao[int(predicted_steers*10)+10][int(angle_steers*10)+10]+1

    # plt.figure("angulo,angulo_pred and NRMSE")
    # if np.size(graph_x) <= 200:
    #   plt.plot(graph_x,graph_y,'r-',graph_x,graph_predicted_y,'b-',graph_x,erroNRMSE,'g-',graph_x,graph_erro,'y*')
    # else:
    #   plt.plot(graph_x[i-200:i],graph_y[i-200:i],'r-',graph_x[i-200:i],graph_predicted_y[i-200:i],'b-',graph_x[i-200:i],erroNRMSE[i-200:i],'g-',graph_x[i-200:i],graph_erro[i-200:i],'y*')
    # plt.ylabel('Estercamento (-1 a 1)')
    # plt.xlabel('Amostras')
    # plt.pause(0.000001)
    # plt.clf()
  
  matriz_confusao[10][10]=0
  #saving_data = np.array([graph_x,graph_y,graph_predicted_y,erroNRMSE,graph_erro])
  #np.savetxt('data.csv', zip(graph_x,graph_y,graph_predicted_y,erroNRMSE,graph_erro), delimiter=',',fmt='%.18f')

  plt.figure("angulo,angulo_pred and NRMSE")
  plt.plot(graph_x,graph_y,'r-',graph_x,graph_predicted_y,'k-')
  #plt.plot(graph_x,graph_y,'r-',graph_x,graph_predicted_y,'b-',graph_x,erroNRMSE,'g-',graph_x,graph_erro,'k-')
  plt.ylabel('Estercamento (-1 a 1)')
  plt.xlabel('Amostras')
  #plt.ylim(-1,1)
  plt.xlim(0,cam['X'].shape[0])
  plt.legend(['Realizado', 'Sugerido'])
  plt.show()

  print(np.amax(erroNRMSE))
  plt.imshow(matriz_confusao, cmap='gray_r')
  plt.colorbar()
  plt.show()