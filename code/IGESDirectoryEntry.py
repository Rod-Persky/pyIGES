#!python3.3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 14:46:07 2013
@author: Rod Persky <rodney.persky@gmail.com
@license: Licensed under the Academic Free License ("AFL") v. 3.0
"""

from IGESCore import IGESPointer
from IGESOptions import IGESEntityTypeNumber, IGESStatusNumber, IGESColorNumber, IGESLineFontPattern


class IGESDirectoryEntry:
    def __init__(self):
        # See 2.2.4.4
        self.EntityType = IGESEntityTypeNumber()  # Integer,           Table 3 Page 38
        self.ParameterDataPointer = IGESPointer()  # Pointer,           First line of Parameter Data
        self.Structure = int(0)  # Integer/Pointer,   2.2.4.4.3 Not using macro instance
        self.LineFontPattern = IGESLineFontPattern()  # Integer/Pointer,   2.2.4.4.4 table
        self.Level = int(0)  # Integer/Pointer,   2.2.4.4.5 ???
        self.View = int(0)  # Null/Pointer,      2.2.4.4.6 Visable in all views
        self.TransfrmMat = int(0)  # Null/Pointer,      2.2.4.4.7 0=no transform -> see #4.21
        self.LabelDispAssoc = int(0)  # Null/Pointer,      2.2.4.4.8 default
        self.StatusNumber = IGESStatusNumber()  # Integer,           2.2.4.4.9
        self.LineWeightNum = int(0)  # Integer,           2.2.4.4.12 use default of reciever
        self.Color = IGESColorNumber()  # Integer/Pointer,   2.2.4.4.13
        self.ParameterLC = int(0)  # Integer,           2.2.4.4.14 Relies on knowing how many parameter lines are in object definition
        self.FormNumber = int(0)  # Integer,           2.2.4.4.15 default
        self.EntityLabel = ""  # String,            2.2.4.4.18 Object Name
        self.EntitySubScript = ""  #

    def GetItems(self):
        return [str(self.EntityType),  # Item 1
                self.ParameterDataPointer,  # Item 2
                self.Structure,  # Item 3
                str(self.LineFontPattern),  # Item 4
                self.Level,  # Item 5
                self.View,  # Item 6
                self.TransfrmMat,  # Item 7
                self.LabelDispAssoc,  # Item 8
                str(self.StatusNumber),  # Item 9
                self.LineWeightNum,  # Item 12
                self.Color.getValue(),  # Item 13
                self.ParameterLC,  # Item 14
                self.FormNumber,  # Item 15
                "", "",  # Item 16, 17 Reserved
                self.EntityLabel[:8],  # Item 18
                self.EntitySubScript]  # Item 19

    def Directory(self):

        L1Temp = '{p[0]:>8}{p[1]:>8}{p[2]:>8}{p[3]:>8}{p[4]:>8}{p[5]:>8}{p[6]:>8}{p[7]:>8}{p[8]:>8}'
        L2Temp = '{p[0]:>8}{p[9]:>8}{p[10]:>8}{p[11]:>8}{p[12]:>8}{p[13]:>8}{p[14]:>8}{p[15]:>8}{p[16]:>8}'

        L1Temp = L1Temp.format(p=self.GetItems())
        L2Temp = L2Temp.format(p=self.GetItems())

        # L1Temp = "{0}D{1:>7}".format(L1Temp, self.DirectoryDataPointer)
        # L2Temp = "{0}D{1:>7}".format(L2Temp, self.DirectoryDataPointer+1)

        return "{}\n{}".format(L1Temp, L2Temp)


