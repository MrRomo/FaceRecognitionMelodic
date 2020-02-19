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

import cv2
import os, sys
import queue as qe
from External_Layer.azure import Azure
from Utils.utils import Utils
from Utils.edit_files import Group
from Utils.edit_files import PersonFiles

class PersonCloud:

    def __init__(self,source):
        self.ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
        self.azureService = Azure()
        self.codeError = 0
        self.gotAttributes = False
        self.framesTrain = None
        self.bb_service = []
        # self.service = None
        self.name = "desconocido"
        self.lastInteractionTime = 0
        self.image = None
        self.G = Group()
        self.utils = Utils(source)

    def selector(self,req):
        if req.name:
            return self.memorize(req.name, req.n_images)
        else:
            return self.recognize()

    def check_img(self, frame):
        if type(frame) != bytes:
            retval, encoded_image = cv2.imencode('.png', frame)
            return encoded_image.tobytes()
        else:
            return frame

    def memorize(self, name, n_images):
        
        frames = [self.utils.take_picture_source() for i in range(n_images)]

        print('Numero de fotos tomadas:', len(frames))
        

        person_id, self.codeError = self.azureService.create_person(name)
        succes = False
        if person_id is not None:
            self.id_azure = person_id
            for frame in frames:
                imgBytes = self.check_img(frame)
                successEnrol, self.codeError = self.azureService.add_face(imgBytes, person_id)
                if successEnrol:  
                    succes = True
                    if self.azureService.attributes:
                        for key, value in self.azureService.attributes.items():
                            setattr(self, key, value)
                        self.image = frame
            if succes:
                self.azureService.train()
                person = self.azureService.attributes
                person["name"] = name
                person["personId"] = person_id
                print(person)
                self.G.add(person)
                return person
            else:
                print('No entrenado')
                return []
        
    def recognize(self):
        print(self.utils)
        frame = self.utils.take_picture_source()
        personsList = self.persons_in_group()
        self.reset_attributes()
        imgBytes = self.check_img(frame)
        people, error = self.azureService.identify(imgBytes)
        print(people)
        # print('IDENTIFY VERIFICATION: ', identify)
        if len(people):
            for person in personsList:
                if people['verify_recognition']:
                    if person['personId'] == people['id_azure']:
                        people['name'] = person['name']
                else:
                    people['name'] = 'Desconocido'
        return people

    def persons_in_group(self):
        personsList, self.codeError = self.azureService.get_all_names()
        return personsList

    def reset_attributes(self):
        attrNoEdit = ['azureService', 'debug', 'ROOT_PATH', 'db_handler', 'information']
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__") and attr not in attrNoEdit:
                if attr == 'name':
                    setattr(self, attr, "desconocido")
                else:
                    if type(getattr(self, attr)) == int:
                        setattr(self, attr, 0)
                    elif type(getattr(self, attr)) == str:
                        setattr(self, attr, "")
                    elif type(getattr(self, attr)) == bool:
                        setattr(self, attr, False)
                    elif type(getattr(self, attr)) == dict:
                        setattr(self, attr, {})
                    elif type(getattr(self, attr)) == tuple:
                        setattr(self, attr, ([], None))
                    else:
                        setattr(self, attr, None)
  