import h5py
import time
from PIL import Image
import matplotlib.pyplot as plt
from scipy.misc import imshow
import numpy as np
import PIL
import pygame
from pygame import surfarray
from vis.utils import utils
import cv2
from PIL import Image

camera = h5py.File("curvas_pose1.h5", "r")
a_group_key = list(camera.keys())

print(camera['X'].shape, a_group_key)

pygame.init()
size = (320, 240)
pygame.display.set_caption("comma.ai data viewer")
screen = pygame.display.set_mode(size)

camera_surface = pygame.surface.Surface((320, 240), 0, 24).convert()
graph_x = np.array(0)
graph_y = np.array(0)

#for i in range(350, 720):
for i in range(720, 925):
    
    # angle_steers = camera['angle'][i]
    # speed_ms = camera['speed'][i]
    pose = camera['pose'][i]
    imagem = camera['X'][i]

    pose_x = pose.split()[2]
    pose_y = pose.split()[4]
    print pose_x,pose_y
    print i
    
    graph_x = np.append(graph_x,float(pose_x))
    graph_y = np.append(graph_y,float(pose_y))

    plt.figure("Posicao do robo")
    plt.plot(graph_x[1:i],graph_y[1:i],'b-')
    plt.ylabel('Posicao em Y')
    plt.xlabel('Posicao em X')
    #plt.axis((-4, 0, 5, 30))
    plt.axis((-1, 5, -1, 6))
    plt.pause(0.000001)
    plt.clf()

    pygame.surfarray.blit_array(camera_surface, imagem.swapaxes(0,2))
    screen.blit(camera_surface, (0,0))
    pygame.display.flip()
    #time.sleep(1)
plt.figure("Rede realizando curva")
plt.plot(graph_x[1:i],graph_y[1:i],'b-')
plt.ylabel('Posicao em Y')
plt.xlabel('Posicao em X')
#plt.axis((-4, 0, 5, 30))
plt.axis((-1, 5, -1, 6))
plt.show()
