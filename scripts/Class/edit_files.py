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


from io import open
import pickle


class PersonFiles:

    # Constructor de clase
    def __init__(self, person):
        self.person = person
        print('The person {} has been saved in file personsGroupCloud.pckl'.format(self.person["name"]))

    def __str__(self):
        return '{} has {} hair, {}, is approximately {} years old and is {}'.format(self.person["name"], self.person["faceAttributes"]["hair"]["hairColor"], self.person["faceAttributes"]["age"],self.person["faceAttributes"]["gender"])

class Group:

    persons = []
    temp = []

    # Constructor de clase
    def __init__(self):
        self.load()

    def add(self,p):
        self.persons.append(p)
        self.save()

    def show(self):
        if len(self.persons) == 0:
            print("The group is empty in edit_files")
            return
        
        for p in self.persons:
            print(p)

    def load(self):
        file = open('personsGroupCloud.pckl', 'ab+')
        file.seek(0)
        try:
            self.persons = pickle.load(file)
        except:
            print("The File is Empty in edit_files")
        finally:
            file.close()
            print("{} persons loaded in edit_files".format(len(self.persons)))
    
    def delete(self,name):
        self.load()
        temp = []
        flag = False
        if len(self.persons) == 0:
            print("The group is empty in edit_files")
            return
        for person in self.persons:
            if person.name != name:
                temp.append(person)
            else:
                flag = True
                print("{} deleted in editfiles".format(name))
        if not flag:
            print("{} is not in group in editfiles".format(name))
        self.persons = temp
        self.save()
        
    def save(self):
        file = open('personsGroupCloud.pckl', 'wb')
        pickle.dump(self.persons, file)
        file.close()
