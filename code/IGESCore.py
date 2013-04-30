# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:00:26 2013
@author: Rod Persky
Licensed under the Academic Free License ("AFL") v. 3.0
"""

import time as Time
import pyximport; pyximport.install()
import IGESCompile
from IGESOptions import IGESModelUnits

class IGESPointer:
    def __init__(self):  self.data = 0
    def __str__(self): return str(self.data)
    def __add__(self, other): return self.data+1 #Only use when printing

class IGESDateTime:
    def __init__(self): self.time = Time.strftime('%Y%m%d.%H%M%S')     # 2.2.4.3.18
    def __str__(self): return self.time

class IGESectionFunctions:
    def __init__(self):
        self._data = list()
        self._linecount = 1

    def __str__(self):
        return IGESCompile.Join(self._data, self.LetterCode)

    #ToDo: Consider not splitting the lines back into an array and use
    #       the linecount returned from the IGESCompile.IGESUnaligned
    def AddLines(self,lines):
        lines = lines.split("\n")
        self._data.extend(lines)
        #self._linecount = len(self._data)+1
        #self._linecount += len(lines)

    def ToIGES(self):
        raise DeprecationWarning("ToIGES now depreciated")


class IGEStart(IGESectionFunctions):
    Template = "{0}{1:72}S{2:7}"
    LetterCode = "S"
    def __init__(self):
        IGESectionFunctions.__init__(self)
        self.Prolog = [
        "|--------------3D PARAMETRIC TURBINE GEN TOOL--------------------------",
        "|................ Writen By, Rodney Persky.............................",
        "|............WARNING, CONFIG FILE FAILED TO LOAD.......................",
        "|............BEWARE: UNITS WILL NOT BE CORRECT AT ALL.................."]
  

    def __str__(self):
        out = ""
        for line in range(0, len(self.Prolog)):
            out = self.Template.format(out,self.Prolog[line][0][:72],line+1)
        self._linecount = line+1
        return out


class IGESGlobal(IGESDateTime, IGESModelUnits, IGESectionFunctions):
    LetterCode = "G"
    def __init__(self):         #2.2.4.3
        IGESectionFunctions.__init__(self)
        self.ParameterDelimiterCharacter = ","              # 1, String
        self.RecordDelimiter = ";"                          # 2, String
        self.ProductIdentificationFromSender = "IGESFile"   # 3, String
        self.FileName = "IGESFileAGenD"                     # 4, String
        self.NativeSystemID = "<unspecified>"               # 5, String
        self.PreprocessorVersion="<unspecified>"            # 6, String
        self.IntegerBits = int(8)                           # 7, Integer
        self.SPMagnitude = int(19)                          # 8, Integer
        self.SPSignificance = int(3)                        # 9, Integer
        self.DPMagnitude = int(38)                          #10, Integer
        self.DPSignificance = int(6)                        #11, Integer
        self.ProductIdentificationForReceiver = "IGESFile"  #12, String
        self.ModelSpaceScale = float(1)                     #13, Real
        self.Units = IGESModelUnits()                       #14 = Integer, 15 = Flag
        self.MaxNumberLineWeightGrads = int(1)              #16, Integer
        self.WidthMaxLineWeightUnits = float(16)            #17, Real
        self.DateTimeFileGeneration = str(IGESDateTime())   #18, String
        self.MaxUserResolution = float(0.0001)              #19, Real
        self.MaxCoordValue = float(1000)                    #20, Real
        self.NameOfAuthor = "IGESAuthor"                    #21, String
        self.AuthorOrg = "QUT"                              #22, String
        self.VersionFlag = int(11)                          #23, Integer
        self.DraftStandardFlag = int(0)                     #24, Integer
        self.DateTimeCreated = str(IGESDateTime())          #25, String
        self.AppProtocol = "0"                              #26, String

    def GetItems(self):
        return [self.ParameterDelimiterCharacter,     self.RecordDelimiter,
         self.ProductIdentificationFromSender, self.FileName, self.NativeSystemID,
         self.PreprocessorVersion, self.IntegerBits,
         self.SPMagnitude, self.SPSignificance, self.DPMagnitude, self.DPSignificance,
         self.ProductIdentificationForReceiver, self.ModelSpaceScale, self.Units.UnitsFlag,
         self.Units.UnitsName, self.MaxNumberLineWeightGrads, self.WidthMaxLineWeightUnits,
         self.DateTimeFileGeneration, self.MaxUserResolution, self.MaxCoordValue,
         self.NameOfAuthor, self.AuthorOrg, self.VersionFlag, self.DraftStandardFlag,
         self.DateTimeCreated, self.AppProtocol]
         
    def __str__(self):
        self._data = []
        self.AddLines(IGESCompile.IGESUnaligned(self.GetItems(), self, self.LetterCode, 0,72)[0])
        return IGESectionFunctions.__str__(self)


class IGESDirectory(IGESectionFunctions):
    LetterCode = "D"
    def __init__(self):
        IGESectionFunctions.__init__(self)


class IGESParameter(IGESectionFunctions):
    LetterCode = "P"
    def __init__(self):
        IGESectionFunctions.__init__(self)


class IGESTerminate:
    def IGESTerminate(self): #output must be wrapped exactly like every other section
        return "S{:7}G{:7}D{:7}P{:7}{:>41}{:7}".format(
                                            len(self.StartSection._data)+1,
                                            len(self.GlobalSection._data),
                                            len(self.DirectorySection._data),
                                            len(self.ParameterSection._data),
                                            "T", 1)

class IGEStorage(IGESTerminate):
    """IGES Storage"""

    def __init__(self): #Wrap core functions
        self.StartSection = IGEStart()
        self.GlobalSection = IGESGlobal()
        self.DirectorySection = IGESDirectory()
        self.ParameterSection = IGESParameter()

    def Commit(self, object):
        #Step 1, Update/get pointer from storage
        #Step 2, Commit rendered object to storage
        object.ParameterDataPointer.data = len(self.ParameterSection._data)+1
        object.DirectoryDataPointer.data = len(self.DirectorySection._data)+1
        self.ParameterSection.AddLines(object.Parameters(self.GlobalSection))
        self.DirectorySection.AddLines(object.Directory())
        
    def save(self, filename='IGESFile.igs'):
        try:
            myFile = open(filename, 'w')
            myFile.write(str(self))
            myFile.close()
            print("\n\nSuccessfuly wrote:",filename)
        except:
            print("File write error")

    def __str__(self):
        out = str(self.StartSection)
        out = "".join((out,str(self.GlobalSection)))
        out = "".join((out,str(self.DirectorySection)))
        out = "".join((out,str(self.ParameterSection),"\n"))
        out = "".join((out,self.IGESTerminate()))
        return out



