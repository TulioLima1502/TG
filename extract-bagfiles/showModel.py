#!/usr/bin/env python
import argparse
import sys
import numpy as np
import h5py
import json
import os
import time
import cv2
import pylab
from keras.models import model_from_json
from keras.utils import plot_model
from vis.utils import utils
from keras import activations
import warnings
warnings.filterwarnings('ignore')
from vis.utils import utils
from matplotlib import pyplot as plt
from vis.visualization import visualize_saliency, overlay
import matplotlib.cm as cm
from vis.visualization import visualize_cam
from vis.visualization import visualize_activation
from keras import backend as K
import keras

from vis.losses import ActivationMaximization
from vis.regularizers import TotalVariation, LPNorm
from vis.optimizer import Optimizer

from PIL import Image

# ***** main loop *****
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Path viewer')
  parser.add_argument('model', type=str, help='Path to model definition json. Model weights should be on the same path.')
  args = parser.parse_args()

  with open(args.model, 'r') as jfile:
    model = model_from_json(json.load(jfile))

  model.compile("sgd", "mse")
  weights_file = args.model.replace('json', 'keras')
  model.load_weights(weights_file)

  plot_model(model, to_file='model.png')

  layers = []
  layer_dict = dict([(layer.name, layer) for layer in model.layers])
    
  keras_layer=layer_dict['dense_2'].output
  layer_idx = utils.find_layer_idx(model, 'lambda_1')

  model.layers[layer_idx].activation = activations.linear
  model = utils.apply_modifications(model)

  cam = h5py.File("retas_1.h5", "r")

  for layer in model.layers:
    layers.append(layer.name)

  for interator in layers:
    layer_idx = utils.find_layer_idx(model, interator)

    model.layers[layer_idx].activation = activations.linear
    model = utils.apply_modifications(model)

    img = visualize_activation(model, layer_idx, filter_indices=0)
    imagem = img.swapaxes(0,2).swapaxes(0,1)
    print(interator)
    plt.figure(interator)
    plt.imshow(imagem)
  plt.show()

  # for i in range(0, cam['X'].shape[0]):
  #   img = cam['X'][i]
  #   print img.shape
  #   # 20 is the imagenet index corresponding to `ouzel`
  #   grads = visualize_saliency(model, layer_idx, filter_indices=0, seed_input=img[None, :, :, :].transpose(0, 1, 2, 3), grad_modifier='negate')
      
  #   # visualize grads as heatmap
  #   plt.imshow(grads, cmap='jet')
  #   print grads.shape
  #   plt.show()
  exit()

  filter_indices = [1, 2, 3]
  losses = [
      (ActivationMaximization(keras_layer, filter_indices), 1),
      (LPNorm(model.input), 10),
      (TotalVariation(model.input), 10)
  ]

  optimizer = Optimizer(model.input, losses)
  opt_img, grads, _ = optimizer.minimize()

  print("Finalizou")
  exit()
  
  for layer in model.layers:
    layers.append(layer.name)

  for interator in layers:
    layer_idx = utils.find_layer_idx(model, interator)

    model.layers[layer_idx].activation = activations.linear
    model = utils.apply_modifications(model)

    img = visualize_activation(model, layer_idx, filter_indices=0)
    imagem = img.swapaxes(0,2).swapaxes(0,1)
    print(interator)
    plt.figure(interator)
    plt.imshow(imagem)
  plt.show()
  
  # layer_name = 'convolution2d_3'
  # filter_index = 0
  # input_img = utils.load_img('./3.jpeg')
  # input_img_data = np.random.random((1, 3, 320, 240)) * 20 + 128.
  # layer_output = layer_dict[layer_name].output
  # loss = K.mean(layer_output[:, :, :, filter_index])

  # grads = K.gradients(loss, input_img_data)[0]
  # grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)

  # iterate = K.function([input_img], [loss, grads])
  
  # print grads, loss, iterate

  img2 = utils.load_img('./3.jpeg')
  #input_img_data = np.random.random((1, 3, 240, 320)) * 20 + 128.

  #img1 = cv2.resize(utils.load_img('./1.jpeg'),(320, 240))
  #cv2.imwrite("3.jpeg", img1)
  #plt.rcParams['figure.figsize'] = (18, 6)

  bgr_img = utils.bgr2rgb(img2)
  #im = Image.fromarray(img2).convert('RGB')
  layer_idx=-1

  grads = visualize_cam(model, layer_idx, filter_indices=0, seed_input=img2)
  print(grads.shape)
  #plt.rcParams['figure.figsize'] = (18, 6)
  # Plot with 'jet' colormap to visualize as a heatmap.
  plt.imshow(grads)
  plt.show()

  exit()
  
  for modifier in ['guided', 'relu']:
    grads = visualize_saliency(model, layer_idx, filter_indices=0,
                               seed_input=img1)
    plt.figure()
    plt.title(modifier)
    plt.imshow(grads, cmap='jet')
  plt.show()
  time.sleep(10)

  print(layer_dict)
  layer_idx = utils.find_layer_idx(model, 'dense_2')
  #model.layers[layer_idx].activation = activations.linear
  #model = utils.apply_modifications(model)
  print(layer_idx)

  plt.rcParams['figure.figsize'] = (18, 6)

  img1 = cv2.resize(utils.load_img('./1.jpeg'),(320, 240))
  img2 = cv2.resize(utils.load_img('./2.jpeg'),(320, 240))

  f, ax = plt.subplots(1, 2)
  ax[0].imshow(img1)
  ax[1].imshow(img2)
  plt.show()
  
  f, ax = plt.subplots(1, 2)
  for i, img in enumerate([img1, img2]):    
    # 20 is the imagenet index corresponding to `ouzel`
    grads = visualize_saliency(model, layer_idx, filter_indices=0, seed_input=img)
   
    # visualize grads as heatmap
    ax[i].imshow(grads, cmap='jet')
  plt.show()
  print(img1)
  exit()

#   penultimate_layer = utils.find_layer_idx(model, 'dense_2')

#   for modifier in [None, 'guided', 'relu']:
#     plt.figure()
#     f, ax = plt.subplots(1, 2)
#     plt.suptitle("vanilla" if modifier is None else modifier)
#     for i, img in enumerate([img1, img2]):    
#         # 20 is the imagenet index corresponding to `ouzel`
#         grads = visualize_cam(model, layer_idx, filter_indices=20, 
#                               seed_input=img, penultimate_layer_idx=penultimate_layer,
#                               backprop_modifier=modifier)        
#         # Lets overlay the heatmap onto original image.    
#         jet_heatmap = np.uint8(cm.jet(grads)[..., :3] * 255)
#         ax[i].imshow(overlay(jet_heatmap, img))
#   plt.show()
#   exit()
#   layer_idx = utils.find_layer_idx(model, 'convolution2d_1')

#   f, ax = plt.subplots(1, 2)
#   for i, img in enumerate([img1, img2]):    
#       # 20 is the imagenet index corresponding to `ouzel`
#       grads = visualize_saliency(model, layer_idx, filter_indices=20, seed_input=img)
    
#       # visualize grads as heatmap
#       ax[i].imshow(grads, cmap='jet')
#   plt.show()
#   exit()
#   layer_name = 'predictions'
#   layer_dict = dict([(layer.name, layer) for layer in model.layers[1:]])
#   output_class = [20]

#   losses = [
#       (ActivationMaximization(layer_dict[layer_name], output_class), 2),
#       (LPNorm(model.input), 10),
#       (TotalVariation(model.input), 10)
#   ]
#   opt = Optimizer(model.input, losses)
#   opt.minimize(max_iter=500, verbose=True, image_modifiers=[Jitter()], callbacks=[GifGenerator('opt_progress')])