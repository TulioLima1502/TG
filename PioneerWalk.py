import rospy
import roslib
import numpy as np
import cv2
import geometry_msgs.msg
import tf
from sensor_msgs.msg import CompressedImage
from time import sleep
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
import pygame
from pygame.locals import *
import imutils
import matplotlib.pyplot as plt
import sys
import argparse
from keras.models import model_from_json
import json
import math


pygame.init()
size = (320, 240)

pygame.display.set_caption("visualizador")
screen = pygame.display.set_mode(size)

camera_surface = pygame.surface.Surface((320,240),0,24).convert()

dimensions = [320, 240]
orientation = pygame.display.set_mode(dimensions)

orientation.fill((255, 255, 255))

circulo = [10, 10, 100, 100]

class pioneer():
    def __init__(self, debug=False ,ser= None):
        self.Image = None
        self.velocity_publisher = None
        self.image_subscriber = None
    
    def callback(self, ros_image):
        #self.Image = ros_image.data
        np_img = np.fromstring(ros_image.data, dtype=np.uint8)
        imagem = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        imagem_resized = cv2.resize(imutils.rotate(imagem, 180), (320, 240))
        self.Image = cv2.cvtColor(imagem_resized, cv2.COLOR_BGR2RGB)

    
    def move(self,path_modelo):
        print("Iniciando o Programa para mover o Pioneer")

        with open(path_modelo, 'r') as jfile:
            model = model_from_json(json.load(jfile))
    
        model.compile("sgd", "mse")
        weights_file = args.model.replace('json', 'keras')
        model.load_weights(weights_file)

        rospy.init_node('robot', anonymous=True)
        self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.image_subscriber = rospy.Subscriber('camera/image_raw/compressed', CompressedImage, callback = self.callback, queue_size=10)
        vel_msg = Twist()
        print(self.image_subscriber)
        #print(self.Image)
        
        sleep(2)

        vel_msg.linear.x = 1.0 # Setando a velocidade para um valor que nao provoca tantos erros na posicao
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0.0

        
        while not rospy.is_shutdown():
            t0 = rospy.Time.now().to_sec()
            image_now=self.Image
            
            predicted_steers = model.predict(image_now[None, :, :, :].transpose(0, 3, 1, 2))[0][0]
            predicted_steers = predicted_steers/507.45

            #pega o angulo pra cada imagem e insere em vel_msg.angular.z = 0.0

            pygame.surfarray.blit_array(camera_surface, image_now.swapaxes(0, 1))
            screen.blit(camera_surface, (0,0))

            pygame.draw.ellipse(orientation, (0, 0, 0), circulo, 2)
            
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
            
            vel_msg.angular.z = float(predicted_steers)

            print predicted_steers
            pygame.draw.line(orientation, (0, 255, 0), [60, 60], [x, y], 1)
            
            pygame.display.flip()
            self.velocity_publisher.publish(vel_msg)
            sleep(0.05)
        exit()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Path viewer')
    parser.add_argument('model', type=str, help='Path to model definition json. Model weights should be on the same path.')
    args = parser.parse_args()

    try:
        myRobot = pioneer()
        myRobot.move(args.model)
    except rospy.ROSInterruptException:
        pass