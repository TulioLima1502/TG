import h5py
import time
from PIL import Image
import matplotlib.pyplot as plt
from scipy.misc import imshow
import numpy
import PIL
import pygame
from pygame import surfarray
from vis.utils import utils
import cv2
from PIL import Image


camera = h5py.File("curvas_em_T_1.h5", "r")
a_group_key = list(camera.keys())[0]

print camera['X'].shape

pygame.init()
size = (320, 240)
pygame.display.set_caption("comma.ai data viewer")
screen = pygame.display.set_mode(size)

camera_surface = pygame.surface.Surface((320,240),0,24).convert()

for i in range(0, camera['X'].shape[0]):

    angle_steers = camera['angle'][i]
    speed_ms = camera['speed'][i]

    imagem = camera['X'][i]
    #imshow(imagem)
    print imagem.shape
    pygame.surfarray.blit_array(camera_surface, imagem.swapaxes(0,2))
    #camera_surface_2x = pygame.transform.scale2x(camera_surface)
    screen.blit(camera_surface, (0,0))
    pygame.display.flip()
    data = numpy.array(imagem.swapaxes(0,2).swapaxes(0,1))
    file = 'test.jpeg'
    data = utils.bgr2rgb(data)
    cv2.imwrite(file, data)
    #plt.imshow(data)
    cv2.imshow('cv_img', data)
    #cv2.imwrite('teste', image_np)
    cv2.waitKey(0)
    