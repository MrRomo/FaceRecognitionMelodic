# -*- coding: utf-8 -*-
#!/usr/bin/env python
# license removed for brevity
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
from characterization import Characterization
from sensor_msgs.msg import Image
import cv2
import time
from datetime import datetime
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from utils import Utils
try:
    from robot_toolkit_msgs.srv import vision_tools_srv
    from robot_toolkit_msgs.msg import camera_parameters_msg, depth_to_laser_msg, vision_tools_msg
except ImportError, e:
    print("Error on %s" % e)
cv_bridge = CvBridge()


class FaceID():
    def __init__(self, camera, person):
        self.imagePub = rospy.Publisher('/faceImage', Image, queue_size=10)
        self.person = Characterization(person)
        self.source = camera
        self.frame = None
        self.resolution = [120, 240, 480, 960, 1920, 0, 0, 0, 60, 30]
        self.res = 4
        self.request = False
        self.utils = Utils(self.source, self.person.percent_of_face)
        if (camera == 'pepper'):
            rospy.wait_for_service('/robot_toolkit/vision_tools_srv')
            self.camera = rospy.ServiceProxy(
                '/robot_toolkit/vision_tools_srv', vision_tools_srv)
            rospy.Subscriber(
                "/robot_toolkit_node/camera/front/image_raw", Image, self.frontCameraCallback)

    def detectFace(self, req):
        print "Detect request"
        #self.initCamera()
	while (not(self.request)and(self.source == 'pepper')):
	    rospy.sleep(.3)
	    print "waiting for valid frame {}".format(type(self.frame))
        frame = self.utils.take_picture_source(self.frame)
        self.frame = None
	self.request = False
        people = self.person.detect_person(frame)
        res = self.utils.add_features_to_image(frame, people)
        if req.cvWindow:
            self.imagePub.publish(res["frame"])
        
        return res["isInFront"]

    def recognizeFace(self, req):
        print "Recognize request"
        #self.initCamera()
	while (not(self.request)and(self.source == 'pepper')):
	    rospy.sleep(.3)
	    print "waiting for valid frame {}".format(type(self.frame))
        frame = self.utils.take_picture_source(self.frame)
        self.frame = None
	self.request = False
        people = self.person.indentify_person(frame)
        if req.cvWindow and people:
            res = self.utils.add_features_to_image(frame, [people])
            self.imagePub.publish(res["frame"])
        
        return str(people)

    def memorizeFace(self, req):
        print "Memorize request"
        #self.initCamera()
        while (not(self.request)and(self.source == 'pepper')):
           rospy.sleep(.3)
           print "waiting for valid frame {}".format(type(self.frame))
        images = []
        for i in range(req.n_images):
            frame = self.utils.take_picture_source(self.frame)
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            print frame.shape
            images.append(frame)
            if(self.source == 'pepper'):
                self.frame = None
                while self.frame is None:
                    pass

        print("n_images toke {}".format(len(images)))

        person = self.person.add_person(req.name, images)  # Add person
        if req.cvWindow and person:
            res = self.utils.add_features_to_image(frame, [person])
            self.imagePub.publish(res["frame"])
        print("Person faceid", person)
        
        return str(person)

    def frontCameraCallback(self, frontData):

        image = None
        imageFrontCamera = None
        print("received imageCallback")
        if (frontData.encoding == 'compressed bgr8'):
            frame = np.frombuffer(frontData.data, dtype='uint8')
            image = cv2.imdecode(frame, 1)
        else:
            image = cv_bridge.imgmsg_to_cv2(frontData, "bgr8")

        if (image is not None):
            timestamp = datetime.now()
            print("photo {} {}".format(image.shape, timestamp))
            if image.shape[0] == self.resolution[self.res]:
                imageFrontCamera = image
                self.request = True
            else:
		self.request = False
               

        self.frame = imageFrontCamera


    def initCamera(self):
        # 
        if ((self.frame is None)and(self.source == 'pepper')):
            print "change camera"
            msg = vision_tools_msg()
            msg.camera_name = "front_camera"
            msg.command = "custom"
            msg.frame_rate = 1
            msg.resolution = self.res
            msg.color_space = 11
            service = self.camera(msg)
            msg.command = "set_parameters"
            msg.camera_parameters.brightness = 5
            msg.camera_parameters.contrast = 32
            msg.camera_parameters.saturation = 64
            msg.camera_parameters.hue = 0
            msg.camera_parameters.horizontal_flip = 0
            msg.camera_parameters.vertical_flip = 0
            msg.camera_parameters.auto_exposition = 1
            msg.camera_parameters.auto_white_balance = 1
            msg.camera_parameters.auto_gain = 1
            msg.camera_parameters.reset_camera_registers = 0
            msg.camera_parameters.auto_focus = 1
            msg.camera_parameters.compress = True
            msg.camera_parameters.compression_factor = 30
            service = self.camera(msg)
            print service
            print msg
            while (not(self.request)):
                time.sleep(1)
                print "waiting for valid frame {}".format(type(self.frame))
            
    
    def shutdownCamera(self):
        print "shutdown camera"
        msg = vision_tools_msg()
        msg.camera_name = "front_camera"
        msg.command = "disable"
        
