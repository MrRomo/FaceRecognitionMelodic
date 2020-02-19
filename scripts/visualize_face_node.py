#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# //======================================================================//
# //  This software is free: you can redistribute it and/or modify        //
# //  it under the terms of the GNU General Public License Version 3,     //
# //  as published by the Free Software Foundation.                       //
# //  This software is distributed in the hope that it will be useful,    //
# //  but WITHOUT ANY WARRANTY; without even the implied warranty of      //
# //  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE..  See the      //
# //  GNU General Public License for more details.                        //
# //  You should have received a copy of the GNU General Public License   //
# //  Version 3 in the file COPYING that came with this distribution.     //
# //  If not, see <http://www.gnu.org/licenses/>                          //
# //======================================================================//
# //                                                                      //
# //      Copyright (c) 2019 SinfonIA Pepper RoboCup Team                 //
# //      Sinfonia - Colombia                                             //
# //      https://sinfoniateam.github.io/sinfonia/index.html              //
# //                                                                      //
# //======================================================================//


import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import threading
import cv2
#from person import Person

class CV_Image():
    def __init__(self):
        self.bridge = CvBridge()
        #self.persons = Person()
        self.imageFlag = False
        self.cv_image = None
        self.imageSub = rospy.Subscriber('/faceImage', Image, self.imageCallback)
        
    def imageCallback(self, msg):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
            self.imageFlag = True
        except CvBridgeError as e:
            print(e)
    def visualize(self):
        rate = rospy.Rate(1) # 10hz
        while not rospy.is_shutdown():
            if self.imageFlag:
                plt.figure(1)
                image.imageFlag = False;
                plt.imshow(image.cv_image, cmap = 'gray', interpolation = 'bicubic')
                plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
                plt.draw()

            rate.sleep()  
    
if __name__ == '__main__':
    try:
        rospy.init_node('visualize_face_node', anonymous=True)
        rospy.loginfo("Nodo visualize_face_image Iniciado")
        image = CV_Image();
        hilo2 = threading.Thread(target = image.visualize)
        hilo2.daemon = True
        hilo2.start()
        plt.figure(1)
        plt.show()      
    except rospy.ROSInterruptException:
        pass