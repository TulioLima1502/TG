import h5py
import time
from PIL import Image
import matplotlib.pyplot as plt
from scipy.misc import imshow
import numpy
import PIL
import pygame
from pygame import surfarray
import cv2

camera = h5py.File("segundo.h5", "r")
a_group_key = list(camera.keys())[0]

print camera['X'].shape

pygame.init()
size = (640, 480)
pygame.display.set_caption("comma.ai data viewer")
screen = pygame.display.set_mode(size)

camera_surface = pygame.surface.Surface((640,480),0,24).convert()

for i in range(0, camera['X'].shape[0]):

    angle_steers = camera['angle'][i]
    speed_ms = camera['speed'][i]

    imagem = camera['X'][i]
    #imshow(imagem)

    pygame.surfarray.blit_array(camera_surface, imagem.swapaxes(0,1))
    #camera_surface_2x = pygame.transform.scale2x(camera_surface)
    screen.blit(camera_surface, (0,0))
    pygame.display.flip()
    #time.sleep(1)
