import numpy as np
import rosbag
import time
import roslib
from sensor_msgs.msg import CompressedImage
from scipy.ndimage import filters
import cv2
import rospy
from PIL import Image
import shutil
import os
import threading
from align import align

caminhos = [os.path.join("../bag-files", nome) for nome in os.listdir("../bag-files")]
arquivos = [arq for arq in caminhos if os.path.isfile(arq)]

if not arquivos:
    print("There's no file in bag-files folder. Please, insert some file on this folder to build h5file.")
    exit()

for filename in arquivos:
    bag = rosbag.Bag(filename, "r")
    messages = bag.read_messages(topics=["/camera/image_raw/compressed/"])
    num_images = bag.get_message_count(topic_filters=["/camera/image_raw/compressed/"])
    dirTemp = "../bag-files/images"

    try:
        os.mkdir(dirTemp)
    except OSError:
        shutil.rmtree(dirTemp)
        os.mkdir(dirTemp)

    for i in range(num_images):
        topic, msg, t  = messages.next()
        #print(msg.header.stamp)
        #print("Received an image!")
        np_arr = np.fromstring(msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        im = Image.fromarray(image_np)
        im.save(str(msg.header.stamp) + ".jpeg")
        shutil.move(str(msg.header.stamp) + ".jpeg", "../bag-files/images")

        
    messages = bag.read_messages(topics=["/cmd_vel"])
    num_images = bag.get_message_count(topic_filters=["/cmd_vel"])
    dirTemp = "../bag-files/cmd_vel"

    try:
        os.mkdir(dirTemp)
    except OSError:
        os.rmdir(dirTemp)
        os.mkdir(dirTemp)

    for i in range(num_images):
        topic, msg, t  = messages.next()
        arq1 = open(str(t) +'.txt', 'w')
        texto = str(msg)
        arq1.write(texto)
        arq1.close()
        #print(t)
        shutil.move(str(t) + ".txt", "../bag-files/cmd_vel")

    messages = bag.read_messages(topics=["/pose"])
    num_images = bag.get_message_count(topic_filters=["/pose"])
    dirTemp = "../bag-files/pose"

    try:
        os.mkdir(dirTemp)
    except OSError:
        os.rmdir(dirTemp)
        os.mkdir(dirTemp)

    for i in range(num_images):
        topic, msg, t  = messages.next()
        arq1 = open(str(msg.header.stamp)+".txt", 'w')
        texto = str(msg.pose.pose)
        arq1.write(texto)
        arq1.close()
        #print(msg.header.stamp,t)
        shutil.move(str(msg.header.stamp)+".txt", "../bag-files/pose")

    messages = bag.read_messages(topics=["/joy"])
    num_images = bag.get_message_count(topic_filters=["/joy"])
    dirTemp = "../bag-files/joy"

    try:
        os.mkdir(dirTemp)
    except OSError:
        os.rmdir(dirTemp)
        os.mkdir(dirTemp)

    for i in range(num_images):
        topic, msg, t  = messages.next()
        arq1 = open(str(msg.header.stamp)+".txt", 'w')
        texto = str(msg.axes)
        arq1.write(texto)
        texto = str(msg.buttons)
        arq1.write(texto)
        arq1.close()
        #print(msg.header.stamp,t)
        shutil.move(str(msg.header.stamp)+".txt", "../bag-files/joy")

    mydata = align()
    mydata.alinha()