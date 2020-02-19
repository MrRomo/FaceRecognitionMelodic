#!/usr/bin/env python
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
import json
from face.srv import FaceDetector
from face.srv import FaceMemorize
from face.srv import FaceRecognize
from rospy_message_converter import message_converter
from std_msgs.msg import String
import ast
import pandas as pd
import time
col = ['None', 'Detector', 'Recognize', 'Memorize']
df = pd.DataFrame(columns=col)
c = 0

class TestFaceID():

    def detect_face(self, cvWind):
        try:
            detect_face_request = rospy.ServiceProxy('robot_face_detector', FaceDetector)
            is_face_in_Front = detect_face_request(cvWind)
            # obtiene un bool del servicio que dice si hay cara o no

            if is_face_in_Front.response:
                print("\nSi Hay cara\n")
            else:
                print("\nNo hay cara\n")
        except rospy.ServiceException:
            print ("Error!! Make sure robot_face node is running ")
        
    def recognize_face(self, cvWind):
        try:
            recognize_face_request = rospy.ServiceProxy(
                'robot_face_recognize', FaceRecognize)
            response = recognize_face_request(cvWind)
            # Convierte la respuesta en un diccionerio util

            attributes = message_converter.convert_ros_message_to_dictionary(
                response)
            attributes = eval(attributes['features'])
            print attributes
            if (attributes is not None) and ('name' in attributes):
                print('Person {} detected'.format(str(attributes['name'])))
            else:
                print('Cara desconocida')

        except rospy.ServiceException:
            print ("Error!! Make sure robot_face node is running ")

    def memorize_face(self, name, cvWind, n_images):
        try:
            memorize_face_request = rospy.ServiceProxy('robot_face_memorize', FaceMemorize)
            response = memorize_face_request(name, cvWind, n_images)
            # Convierte la respuesta en un diccionerio util
            person = message_converter.convert_ros_message_to_dictionary(response)
            person = eval(person['person'])
            if person is not None:
                print("Person name: {}".format(str(person["name"])))
            else:
                print "Not person detected"

        except rospy.ServiceException:
            print ("Error!! Make sure robot_face node is running ")


if __name__ == '__main__':
    try:
        rospy.init_node('test_face_node', anonymous=True)
        rospy.loginfo("Nodo Test Face Iniciado")
        test = TestFaceID()
        while 1:
            try:
                option = int(raw_input('** Welcome to Robot Face Test Node ** \n What do you want to test\n 1. Face detector service \n 2. Face recognition service\n 3. Face memorize service \n 4. Salir\n'))
                if(option == 4):
                    print('Saliendo')
                    break
                choise = raw_input('you want the captures to be displayed? (S/n) ')
                start = time.time()
                    
                if(choise == ('s' or 'yes' or 'si' or 'S')):
                    cvWindow = True
                else:
                    cvWindow = False
                if(option == 1):
                    print('-Detector service:')
                    test.detect_face(cvWindow)
                elif(option == 2):
                    print('-Recognize service:')
                    test.recognize_face(cvWindow)
                elif(option == 3):
                    print('-Memorize service:')
                    name = 'Ricardo' + str(c)
                    n_images = int(raw_input('Ingrese el numero de imagenes que desea entrenar:  ')) 
                    # name = raw_input('Ingrese el nombre de la persona que desea registrar:  ')
                    test.memorize_face(name, cvWindow, n_images)
                else:
                    print('Value error, please enter a valid option')

                stop = time.time()
                times = stop-start
                if(option<=len(col)):
                    df = df.append({col[option]:times}, ignore_index =True)
                    print ("Detector: {} - Recognize: {} Memorize: {}".format(df['Detector'].mean(),df['Recognize'].mean(),df['Memorize'].mean()))
                    print df
                    c+=1
            except ValueError, e:
                print("Value error, please enter a number : %s" % e)



    except rospy.ROSInterruptException:
        pass
