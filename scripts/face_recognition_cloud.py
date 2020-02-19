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
from face_cloud.srv  import FaceRecognizeCloud

if __name__ == '__main__':
    try:
        rospy.init_node('face_recognition_cloud')
        params = []

        try:
            params.append('webcam' if sys.argv.index('webcam') else 'pepper')
        except:
            try:
                params.append('file' if sys.argv.index('file') else 'pepper')
            except:
                params.append('pepper')
        
        
        face = FaceID(params[0])
        print(params)
        rospy.Service('robot_face_recognize',FaceRecognize, face.recognizeFace)
        print("robot face node started")
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
