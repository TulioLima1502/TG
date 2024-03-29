#!/usr/bin/env python
import os
import time
import shutil
from PIL import Image, ImageFilter
import numpy
import h5py
import cv2
import matplotlib.pyplot as plt
import imutils

#from resizeimage import resizeimage

class creatingh5():

    def listing(self):
        h5 = raw_input("Nome do pacote h5?")

        hdf5_path = h5 + ".h5"
        dt = h5py.special_dtype(vlen=str)
           
        images = [arq for arq in os.listdir("../bag-files/database_images")]
        cmd_vel = [arq for arq in os.listdir("../bag-files/database_cmdvel")]
        #position = [arq for arq in os.listdir("../bag-files/database_pose")]
        joystick = [arq for arq in os.listdir("../bag-files/database_joy")]

        im = cv2.imread( "../bag-files/database_images/" + images[0][0:-5] + ".jpeg" )
        #im = cv2.cvtColor(cv2.imread( "../bag-files/database_images/" + images[0][0:-5] + ".jpeg" ), cv2.COLOR_BGR2RGB)
        im = imutils.rotate(im, 180)
        #im = im.swapaxes(0,2).swapaxes(1,2)
        plt.imshow(im)
        plt.show()
        
        image_shape = ( len(images) , im.shape[2], 240 , 320)
        print(im.shape)

        f = h5py.File( hdf5_path , "w")

        f.create_dataset("X", image_shape, numpy.int8)
        #f.create_dataset("pose", (len(images),), dtype=dt)
        f.create_dataset("angle", (len(images),), dtype='float32')
        f.create_dataset("speed", (len(images),), dtype='float32')
        f.create_dataset("dataset_index", (len(images),), numpy.int32)
        
        print(f.keys())

        for i in range(len(images)):
            if i % 1000 == 0 and i > 1:
                print 'Train data: {}/{}'.format(i, len(images))
            addr = images[i]
            im = cv2.imread( "../bag-files/database_images/" + addr )
            print addr
            im = imutils.rotate(im, 180)
            print(im.shape)
            im = cv2.resize(im, (320, 240))
            #exit()
            
            cmdvel = open("../bag-files/database_cmdvel/" + addr[0:-5] + ".txt", 'r')
            comando = cmdvel.read()
            
            joystick = open("../bag-files/database_joy/" + addr[0:-5] + ".txt", 'r')
            controle = joystick.read()
            
            botao = controle.split()[6]
            botao = botao.replace('0.0)(',"")
            botao = botao.replace(',',"")
            if botao == '1':
                angulo = controle.split()[0]
                velocidade = controle.split()[1]
                angulo = angulo.replace('(',"")
                angulo = angulo.replace(',',"")
                velocidade = velocidade.replace(',',"")
                
                print('{}'.format(float(angulo)))
                print('{}'.format(float(velocidade)))
            else:
                angulo = 0.0
                velocidade = 0.0
                print('{}'.format(float(angulo)))
                print('{}'.format(float(velocidade)))
            #separar informacoes em conteudo de velocidade e de angulo
            
            #pose = open("../bag-files/database_pose/" + addr[0:-5] + ".txt", 'r')
            #posicao = pose.read()
            #plt.imshow(im)
            #plt.show()

            f["X"][i, ...] = im[None].swapaxes(1,3).swapaxes(2,3)
            #f["pose"][i, ...] = str(posicao)
            f["speed"][i, ...] = float(velocidade)
            new_angulo = float(angulo)*507.45
            print angulo
            print new_angulo
            #new_angulo = -5023 + (5023 + 5023)*((float(angulo) + 1)/(2))
            f["angle"][i, ...] = float(new_angulo)
            f["dataset_index"][i, ...] = i

            cmdvel.close()
            joystick.close()
            #pose.close()

        f.close()
        exit()

if __name__ == '__main__':
    mydata = creatingh5()
    mydata.listing()
