#!python3.3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:52:52 2013
@author: Rod Persky <rodney.persky@gmail.com
@license: Licensed under the Academic Free License ("AFL") v. 3.0
"""

from IGESCore import IGESPointer
import numpy as np
import pyximport; pyximport.install()
import IGESCompile

class IGESParameterEntry:
    def __init__(self):
        self.DirectoryDataPointer = IGESPointer()
        self.data = list()

    def AddParameters(self, data):
        self.data.extend(data)

    # TODO: Determine if 2.2.4.5.2 is required, currently just putting nulls
    def Parameters(self, IGESGlobal):
        cdata = self.data[:]
        cdata.insert(0, self.EntityType.value)
        cdata.extend([0, 0])
        out, self.ParameterLC = IGESCompile.IGESUnaligned(cdata, IGESGlobal, 'P', self.ParameterDataPointer.data * 2 - 1, 65)
        return out
