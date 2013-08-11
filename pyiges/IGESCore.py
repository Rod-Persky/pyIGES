#!python3
# -*- coding: utf-8 -*-
"""
.. module:: IGES.IGESCore
   :platform: Agnostic, Windows
   :synopsis: Main GUI program


.. Created on Sat Mar 30 15:00:26 2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES

"""


from pyiges.IGESOptions import (IGESModelUnits,
                                IGESEntityTypeNumber,
                                IGESStatusNumber,
                                IGESColorNumber,
                                IGESLineFontPattern,
                                IGESPointer,
                                IGESDateTime)

import pyiges.IGESCompile as IGESCompile


class IGESectionFunctions:
    def __init__(self):
        self._data = list()
        self._linecount = 1

    def getNewPointer(self):
        return IGESPointer(self._linecount)

    def __str__(self):
        return IGESCompile.format_line(self._data, self.LetterCode)

    def AddLines(self, lines):
        self._linecount = self._linecount + len(lines)
        self._data.extend(lines)


class IGESParameterEntry:
    def __init__(self):
        pass


class IGESItemData:
    """IGES Item Data

    When adding to IGES File,
    1) Get DirectoryDataPointer
    2) Compile ParameterData (which relies on the DirectoryDataPointer)
    3) Update ParameterLineCount
    4) get ParameterDataPointer
    5) compile directory data (which relies on ParameterLineCount and ParameterDataPointer)
    """
    def __init__(self):
        #Pointers and data that needs updating
        self.DirectoryDataPointer = IGESPointer()       # Pointer,           First line of Directory Data
        self.ParameterDataPointer = IGESPointer()       # Pointer,           First line of Parameter Data
        self.ParameterLineCount = int(0)                # Integer,           2.2.4.4.14 Relies on knowing how many parameter lines are in object definition

        #IGES parameter data information
        self.ParameterData = list()

        # IGES directory data information See 2.2.4.4
        self.EntityType = IGESEntityTypeNumber()        # Integer,           Table 3 Page 38
        self.Structure = int(0)                         # Integer/Pointer,   2.2.4.4.3 Not using macro instance
        self.LineFontPattern = IGESLineFontPattern()    # Integer/Pointer,   2.2.4.4.4 table
        self.Level = int(0)                             # Integer/Pointer,   2.2.4.4.5 ???
        self.View = int(0)                              # Null/Pointer,      2.2.4.4.6 Visable in all views
        self.TransfrmMat = int(0)                       # Null/Pointer,      2.2.4.4.7 0=no transform -> see #4.21
        self.LabelDispAssoc = int(0)                    # Null/Pointer,      2.2.4.4.8 default
        self.StatusNumber = IGESStatusNumber()          # Integer,           2.2.4.4.9
        self.LineWeightNum = int(0)                     # Integer,           2.2.4.4.12 use default of reciever
        self.Color = IGESColorNumber()                  # Integer/Pointer,   2.2.4.4.13
        self.FormNumber = int(0)                        # Integer,           2.2.4.4.15 default
        self.EntityLabel = ""                           # String,            2.2.4.4.18 Object Name
        self.EntitySubScript = ""

        self.add_extended_data = False                   # Some items seem to needs this whilst other do not

        #Compiled items
        self.CompiledDirectory = list()
        self.CompiledParameter = list()

    def AddParameters(self, data):
        try:
            self.ParameterData.extend(list(data))
        except Exception as inst:
            raise TypeError(inst)

    def CompileDirectory(self):
        items = [str(self.EntityType),                   # Item 1
                 self.ParameterDataPointer,              # Item 2
                 self.Structure,                         # Item 3
                 str(self.LineFontPattern),              # Item 4
                 self.Level,                             # Item 5
                 self.View,                              # Item 6
                 self.TransfrmMat,                       # Item 7
                 self.LabelDispAssoc,                    # Item 8
                 str(self.StatusNumber),                 # Item 9
                 self.LineWeightNum,                     # Item 12
                 self.Color.getValue(),                  # Item 13
                 self.ParameterLineCount,                # Item 14
                 self.FormNumber,                        # Item 15
                 "", "",                                 # Item 16, 17 Reserved
                 self.EntityLabel[:8],                   # Item 18
                 self.EntitySubScript]                   # Item 19

        Line1Template = "{p[0]:>8}{p[1]:>8}{p[2]:>8}{p[3]:>8}{p[4]:>8}{p[5]:>8}{p[6]:>8}{p[7]:>8}{p[8]:>8}"
        Line2Template = "{p[0]:>8}{p[9]:>8}{p[10]:>8}{p[11]:>8}{p[12]:>8}{p[13]:>8}{p[14]:>8}{p[15]:>8}{p[16]:>8}"

        self.CompiledDirectory = [Line1Template.format(p = items)]
        self.CompiledDirectory.append(Line2Template.format(p = items))

        return self.CompiledDirectory

    def CompileParameters(self, IGESGlobal):
        #IGESGlobal is required because we need IGESGlobal.ParameterDelimiterCharacter
        cdata = [self.EntityType.value]
        cdata.extend(self.ParameterData[:])

        if self.add_extended_data:
            cdata.extend([0, 0])

        self.CompiledParameter, self.ParameterLineCount = IGESCompile.IGESUnaligned(cdata, IGESGlobal, 'P', self.DirectoryDataPointer.data)
        return self.CompiledParameter


class IGEStart(IGESectionFunctions):
    Template = "{0}{1:72}S{2:7}"
    LetterCode = "S"

    def __init__(self):
        IGESectionFunctions.__init__(self)
        self.Prolog = [
        "|--------------3D PARAMETRIC TURBINE GEN TOOL--------------------------",
        "|................ Written By, Rodney Persky............................",
        "|............WARNING, CONFIG FILE FAILED TO LOAD.......................",
        "|............BEWARE: UNITS WILL NOT BE CORRECT AT ALL.................."]

    def __str__(self):
        out = ""
        for line in range(0, len(self.Prolog)):
            out = self.Template.format(out, self.Prolog[line][0][:72], line + 1)
        self._linecount = line + 1
        return out


class IGESGlobal(IGESDateTime, IGESModelUnits, IGESectionFunctions):
    LetterCode = "G"
    LineLength = 65

    def __init__(self):                                     # 2.2.4.3
        IGESectionFunctions.__init__(self)
        self.ParameterDelimiterCharacter = ","              # 1, String
        self.RecordDelimiter = ";"                          # 2, String
        self.ProductIdentificationFromSender = "IGESFile"   # 3, String
        self.FileName = "IGESFileAGenD"                     # 4, String
        self.NativeSystemID = "<unspecified>"               # 5, String
        self.PreprocessorVersion = "<unspecified>"          # 6, String
        self.IntegerBits = int(8)                           # 7, Integer
        self.SPMagnitude = int(19)                          # 8, Integer
        self.SPSignificance = int(3)                        # 9, Integer
        self.DPMagnitude = int(38)                          # 10, Integer
        self.DPSignificance = int(6)                        # 11, Integer
        self.ProductIdentificationForReceiver = "IGESFile"  # 12, String
        self.ModelSpaceScale = float(1)                     # 13, Real
        self.Units = IGESModelUnits()                       # 14 = Integer, 15 = Flag
        self.MaxNumberLineWeightGrads = int(1)              # 16, Integer
        self.WidthMaxLineWeightUnits = float(16)            # 17, Real
        self.DateTimeFileGeneration = str(IGESDateTime())   # 18, String
        self.MaxUserResolution = float(0.0001)              # 19, Real
        self.MaxCoordValue = float(1000)                    # 20, Real
        self.NameOfAuthor = "IGESAuthor"                    # 21, String
        self.AuthorOrg = ""                                 # 22, String
        self.VersionFlag = int(11)                          # 23, Integer
        self.DraftStandardFlag = int(0)                     # 24, Integer
        self.DateTimeCreated = str(IGESDateTime())          # 25, String
        self.AppProtocol = "0"                              # 26, String

    def GetItems(self):
        return [self.ParameterDelimiterCharacter, self.RecordDelimiter,
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
        self.AddLines(IGESCompile.IGESUnaligned(self.GetItems(), self, self.LetterCode, 0)[0])
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
    def IGESTerminate(self):  # output must be wrapped exactly like every other section
        return "S{:7}G{:7}D{:7}P{:7}{:>41}{:7}".format(
                                            len(self.StartSection._data) + 1,
                                            len(self.GlobalSection._data),
                                            self.DirectorySection._linecount - 1,
                                            self.ParameterSection._linecount - 1,
                                            "T", 1)


class IGEStorage(IGESTerminate):
    """IGES Storage"""
    def __init__(self):  # Wrap core functions
        self.StartSection = IGEStart()
        self.DirectorySection = IGESDirectory()
        self.ParameterSection = IGESParameter()
        self.GlobalSection = IGESGlobal()

    def Commit(self, IGESObject):

        IGESObject.DirectoryDataPointer = self.DirectorySection.getNewPointer()
        IGESObject.CompileParameters(self.GlobalSection)
        IGESObject.ParameterDataPointer = self.ParameterSection.getNewPointer()
        IGESObject.CompileDirectory()

        self.ParameterSection.AddLines(IGESObject.CompiledParameter)
        self.DirectorySection.AddLines(IGESObject.CompiledDirectory)

    def save(self, filename = 'IGESFile.igs'):
        try:
            myFile = open(filename, 'w')
            myFile.write(str(self))
            myFile.close()
            print("\n\nSuccessfuly wrote:", filename)
        except:
            print("File write error")

    def __str__(self):
        out = str(self.StartSection)
        out = "".join([out, str(self.GlobalSection), ""])
        out = "".join([out, str(self.DirectorySection), ""])
        out = "".join([out, str(self.ParameterSection), "\n"])
        out = "".join([out, self.IGESTerminate()])
        return out

if __name__ == "__main__":
    import pyiges.data.examples.IGESTest as IGESTest
    IGESTest.testrun()
