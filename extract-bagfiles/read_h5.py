import h5py
import time
from PIL import Image
import matplotlib.pyplot as plt


camera = h5py.File("camera/2016-06-08--11-46-01.h5", "r")
log = h5py.File("log/2016-06-08--11-46-01.h5", "r")

a_group_key = list(camera.keys())[0]
b_group_key = list(log.keys())[0]

print camera['X'].shape

plt.ion()
for i in range(0, log['times'].shape[0]):

    angle_steers = log['steering_angle'][i]
    speed_ms = log['speed'][i]

    #print(i,log['cam1_ptr'][i],angle_steers,speed_ms)

    imagem = camera['X'][log['cam1_ptr'][i]].swapaxes(0,2).swapaxes(0,1)

    #imgr = Image.fromarray(imagem[0],mode=None)
    #imgg = Image.fromarray(imagem[1],mode=None)
    #imgb = Image.fromarray(imagem[2],mode=None)

    #merged=Image.merge("RGB",(imgr,imgg,imgb))
    imgplot = plt.imshow(imagem)
    plt.show()
    #plt.draw()
    plt.pause(0.00001)
    plt.clf()

