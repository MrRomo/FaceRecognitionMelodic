#!/usr/bin/env python3
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
import sys
from face_cloud.srv import FaceRecognizeCloud
from person_cloud import PersonCloud

if __name__ == '__main__':
    try:
        rospy.init_node('face_recognition_cloud')
        source = ''

        try:
            source = 'webcam' if sys.argv.index('webcam') else 'pepper'
        except:
            try:
                source ='file' if sys.argv.index('file') else 'pepper'
            except:
                source = 'pepper'        
        
        face = PersonCloud(source)
        print('Source from: ', source)
        rospy.Service('face_recognize_cloud',FaceRecognizeCloud, face.selector)
        print("Face Recognition Cloud - node started")
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
