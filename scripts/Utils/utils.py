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
import cv2
from cv_bridge import CvBridge
import os
import sys
import rospy

# from robot_toolkit_msgs.msg import camera_parameters_msg, depth_to_laser_msg, vision_tools_msg
# from robot_toolkit_msgs.srv import vision_tools_srv



class Utils:

    def __init__(self, source, percent_of_face=0):
        self.source = source
        self.percent_of_face = percent_of_face
        self.bridge = CvBridge()

    def setProps(self, people, frame_size):
        props = []
        prop = 0
        for face_detected in people:
            pi = (face_detected['faceRectangle']['left'],face_detected['faceRectangle']['top'])
            pf = (face_detected['faceRectangle']['left']+face_detected['faceRectangle']['width'],face_detected['faceRectangle']['top']+face_detected['faceRectangle']['height'])
            prop = (face_detected['faceRectangle']['width']
                    * face_detected['faceRectangle']['height'])
            # guarda el calculo de las proporciones en cada ciclo
            props.append({"pi": pi, "pf": pf, "prop": round(prop*100/float(frame_size), 4)})
        return props

    def take_picture_source(self, framePub=None):
        print("take picture from source: *{}*".format(self.source))        
        if self.source == 'webcam':
            cap = cv2.VideoCapture(0)
            error, frame = cap.read()
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            cap.release()
        elif self.source == 'file':
            ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
            frame = cv2.imread(ROOT_PATH+"/Resources/gente1.jpg")
        else:
            frame = framePub
        return frame

    def add_features_to_image(self, frame, batch):
        frame_size = frame.shape[0]*frame.shape[1]
        isInFront = False
        print ("ADD Freatures***")
        c = 0
        props = []
        cords = []
        for i in range(len(batch)):
            c+=1
            people = batch[i]
            if people:
                font = cv2.FONT_HERSHEY_SIMPLEX
                #top, rigth, bottom and left
                w,t,l,h = people['faceRectangle'].values()
                pi = (l,t)
                pf = (l+w,t+h)
                cords.append((pi,pf))
                # props = self.setProps(people, frame_size)
                # pi = (face_detected['faceRectangle']['left'],face_detected['faceRectangle']['top'])
                # pf = (face_detected['faceRectangle']['left']+face_detected['faceRectangle']['width'],face_detected['faceRectangle']['top']+face_detected['faceRectangle']['height'])
                cv2.rectangle(frame,pi,pf, (255, 255, 0), 3)
                prop = round((w+h)*100/float(frame_size), 4)
                props.append(prop)
                cv2.putText(frame, str(prop)+'%' + ' - ' + str(c), pi, font, 1, (255, 150, 0), 2, cv2.LINE_AA)
                if 'name' in people:
                    cv2.rectangle(frame, (pi[0], pf[1]+50), (pf), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, str(people['name']), (pi[0]+10,pf[1]+30), font, 1, (255, 150, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(frame, "Unknow", (pi[0]+10,pf[1]+30), font, 1, (255, 150, 0), 2, cv2.LINE_AA)
                    
                # for prop in props:

        if len(props):
            if max(props) >= self.percent_of_face:
                index = props.index(max(props))
                isInFront = True
                # Remarca la cara mayor
                cv2.rectangle(frame, cords[index][0],cords[index][1], (0, 0, 255), 5)
        response = {"frame": self.bridge.cv2_to_imgmsg(frame, "bgr8"), "isInFront": isInFront}
        return response
    
def sortDictionary(val):
    return val['faceRectangle']['width']


def setDictionary(locations):
    people = list()
    areas = list()
    for face_location in locations:
        width = face_location[1]-face_location[3]
        height = face_location[2]-face_location[0]
        dictionary_of_features = {'faceId': None, 'faceRectangle': {'width': int(width), 'top': int(
            face_location[0]), 'height': int(height), 'left': int(face_location[3])}, 'faceAttributes': None}
        people.append(dictionary_of_features)
        areas.append(width*height)
    return people, areas

                      
class Less_Blurred:
    def __init__(self, nImages):
        self.nImages = nImages
        self.fm = qe.PriorityQueue(100)
        self.frames = []
    def sort_less_blurred(self, images):
        self.fm = qe.PriorityQueue(100)
        self.frames = []
        if type(images) == dict:
            for imgID in images:
                self.fm.put((1/cv2.Laplacian(images[imgID], cv2.CV_64F).var(),imgID))
            for i in range(self.nImages):
                dat = self.fm.get()
                nIma = dat[1]
                self.frames.append(images[nIma])
        else:
            print('review images type')

