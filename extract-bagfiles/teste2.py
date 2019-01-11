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
messages = bag.read_messages(topics=["/camera/image_raw/compressed/"])
num_images = bag.get_message_count(topic_filters=["/camera/image_raw/compressed/"])

for i in range(num_images):
    # READ NEXT MESSAGE IN BAG
    topic, msg, t  = messages.next()
    print(msg.header.stamp)
    #print(topic)
    #print(msg)
    # CONVERT MESSAGE TO A NUMPY ARRAY
    print("Received an image!")
    # Convert your ROS Image message to OpenCV2
    np_arr = np.fromstring(msg.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #cv2.imread()
    #cv2.imshow('cv_img', image_np)
    #cv2.imwrite('teste', image_np)
    #cv2.waitKey()
    im = Image.fromarray(image_np)
    im.save(str(msg.header.stamp) + ".jpeg")
    shutil.move(str(msg.header.stamp) + ".jpeg", "images")
    #cv2.imwrite('teste', image_np)
    #img = img.reshape(msg.height, msg.width)
    #time.sleep(1)
    # DO SOME PROCESSING ON THE IMAGE    
    # ... 