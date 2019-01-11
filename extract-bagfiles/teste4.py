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

bag = rosbag.Bag("_2018-08-29-20-32-42.bag", "r")
messages = bag.read_messages(topics=["/pose"])
num_images = bag.get_message_count(topic_filters=["/pose"])

for i in range(num_images):
    # READ NEXT MESSAGE IN BAG
    topic, msg, t  = messages.next()
    #print(msg)
    #print(msg.angular)
    #print(msg.pose.pose)
    #print(topic)
    #print(t)
    # CONVERT MESSAGE TO A NUMPY ARRAY
    #print("Received an cmd_vel!")
    
    arq1 = open(str(msg.header.stamp)+".txt", 'w')
    texto = str(msg.pose.pose)
    arq1.write(texto)
    arq1.close()
    #arq2 = open(str(t) +'-angular.txt', 'w')
    #texto = str(msg.angular)
    #arq2.write(texto)
    #arq2.close()
    print(msg.header.stamp,t)
    
    # Convert your ROS Image message to OpenCV2
    #np_arr = np.fromstring(msg.data, np.uint8)
    #image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #cv2.imread()
    #cv2.imshow('cv_img', image_np)
    #cv2.imwrite('teste', image_np)
    #cv2.waitKey()
    #im = Image.fromarray(image_np)
    #im.save(str(msg.header.stamp) + ".jpeg")
    
    shutil.move(str(msg.header.stamp)+".txt", "pose")
    #shutil.move(str(t) + "-angular.txt", "cmd_vel")
    
    #cv2.imwrite('teste', image_np)
    #img = img.reshape(msg.height, msg.width)
    
    #time.sleep(0.1)
    
    # DO SOME PROCESSING ON THE IMAGE    
    # ... 