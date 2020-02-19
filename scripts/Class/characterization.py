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

from person_cloud import PersonCloud
from person_local import PersonLocal
from person_cloud import Less_Blurred
from edit_files import Group
import cv2 as cv2
import sys
import os
import json


# import unicodedata

class Characterization:
    def __init__(self,source):
        self.ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
        n_imas, percent, n_train = self.get_parameters()
        self.n_images_to_take = n_imas
        self.percent_of_face = percent
        self.n_images_to_train = n_train
        self.source = source
        self.persons = self.setPersonSource()
        print(self.n_images_to_take, self.n_images_to_train, self.percent_of_face)  

    def setPersonSource(self):
        print("Use {} enviroment".format(self.source))
        if (self.source == 'local'):
            return PersonLocal()
        if (self.source == 'cloud' ):
            return PersonCloud()

    def get_parameters(self):
        with open(self.ROOT_PATH+"/Resources/interaction_parameters.json") as f:
            secretInfo = json.load(f)
            print("Interaction parameters: ", secretInfo)
            return secretInfo["n_images_to_take"], secretInfo["percent_of_face"], secretInfo["n_images_to_train"]

    def detect_person(self, frame):
        people = self.persons.detectPerson(frame)
        return people

    def indentify_person(self, frame):
        people = self.persons.identifyPerson(frame)
        return people

    def add_person(self, name, images):
        # blurred = Less_Blurred(len(images))
        # images = blurred.sort_less_blurred(images)
        person = self.persons.enrol(name, images)
        return person

    def get_persons(self):
        personsList = self.persons.persons_in_group()
        for p in personsList:
            print(p)
        return personsList

    def delete_person(self, name):
        self.persons.delete_person_by_name(name)
    
    def delete_all_person(self):
        pass
        #delete all person group

    def get_persons_attributes(self):
        G = Group()
        for p in G.persons:
            print(p)
        return G.persons
   


# c = Characterization("local")
# c.get_persons()
# c.indentify_person(True)