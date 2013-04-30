# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:58:02 2013
@author: Rod Persky
Licensed under the Academic Free License ("AFL") v. 3.0
"""

import numpy as np
#cython: boundscheck=False
#cython: wraparound=False


class Lines:
    def __init__(self, int nlines, int linelength, str section, int pointer):
        self.lines = np.empty(nlines, dtype=np.dtype("object"))
        self.nline, self.linelength, self.section, self.pointer  = 0, linelength, section, pointer

    def Store(self, str thisline, int retry = 0):
        try:
            if self.section == "P":
                thisline = "{:<{linelength}}{pointer:>7}".format(thisline, linelength=self.linelength, pointer=self.pointer)
            self.lines[self.nline] = thisline
            self.nline = self.nline + 1
        except IndexError:
            try:
                self.lines.resize((self.nline+5,1))
            except ValueError:
                raise ValueError("Estimated storage size too small, resize failed")

            print "Length guess incorrect, adding length"
            self.Store(thisline,retry+1)

    def ReadStore(self):
        return self.lines[:self.nline].tolist()

    def String(self):
        cdef int i

        out = self.lines[0]
        for i from 1 <= i < self.nline:
            out = "{}\n{}".format(out, self.lines[i])

        return out

cpdef str Join(list data, str section):
    cdef str out = ""

    for i from 0 <= i < len(data):
        out = "{}{}{:<72}{}{:7}".format(out,"\n",data[i],section,i+1)

    return out

cpdef IGESUnaligned(list data, object IGESGlobal, str section, int DirectoryPointer, int linelength):
    #Step 1, Convert data
    #Step 2, Check line length is less then 72
        #Step 2a, Add parameter to line
        #Step 2b, Add line to LineStore
    #Step 4, return LineStore sting

    cdef str Line, Param = ""
    cdef int i, n = 0

    LineStore = Lines(5, linelength, section, DirectoryPointer)

    if len(data) == 0:
        raise ValueError("Parameter data is 0 length")


    for i from 0 <= i < len(data):
        if type(data[i]) == str:
            Param = "{}H{}".format(len(data[i]),data[i])
        elif type(data[i]) == int:
            Param = "{}".format(data[i])
        elif type(data[i]) == float:
            Param = "{}".format(np.around(data[i],5))
        else:
            raise NotImplementedError("Unable to convert type ",type(data[i]))


        if i == 0:
            Line = Param
        else:
            if len(Line)+len(Param)+1 < linelength:
                Line = "{0}{delim}{1}".format(Line, Param, delim=IGESGlobal.ParameterDelimiterCharacter)
            elif len(Param) < linelength-5:
                Line = "{0}{delim}".format(Line, delim=IGESGlobal.ParameterDelimiterCharacter)

                LineStore.Store(Line)
                Line = Param
            else:
                raise NotImplementedError("Character by character wrapping not implimented, you must shorten",Param)

    Line = "{0}{recend}".format(Line, recend=IGESGlobal.RecordDelimiter)
    LineStore.Store(Line)

    return LineStore.String(), LineStore.nline
