#!python3.3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 18:07:29 2013
@author: Rod Persky <rodney.persky@gmail.com
@license: Licensed under the Academic Free License ("AFL") v. 3.0
"""

class IGESModelUnits:
    # This is used in two contexts, 2.2.4.3.14 and 2.2.4.3.15
    def __init__(self):       self.setMillimeters()  # Default
    def setInches(self):      self.UnitsFlag, self.UnitsName = 1, "IN"
    def setMillimeters(self): self.UnitsFlag, self.UnitsName = 2, "MM"
    def setMils(self):        self.UnitsFlag, self.UnitsName = 8, "MIL"
    def setMicrons(self):     self.UnitsFlag, self.UnitsName = 9, "UM"
    def setCentimeters(self): self.UnitsFlag, self.UnitsName = 10, "CM"

class IGESParameter:
    def __init__(self): self.value = 0
    def __str__(self): return str(self.value)
    def getValue(self): return self.value


class IGESEntityTypeNumber(IGESParameter):
    def setCircularArc(self):          self.value = 100
    def setCompositeCurve(self):       self.value = 102
    def setConicArc(self):             self.value = 104
    def setCopiousData(self):          self.value = 106
    def setLinearPath2D(self):         self.value = 111
    def setLinearPath3D(self):         self.value = 112
    def setClosedPlanarCurve(self):    self.value = 163
    def setPlane(self):                self.value = 108
    def setLine(self):                 self.value = 110
    def setSplineCurve(self):          self.value = 112
    def setSplineSurface(self):        self.value = 114
    def setPoint(self):                self.value = 116
    def setRuledSurface(self):         self.value = 118
    def setRevolvedSurface(self):      self.value = 120
    def setTabCylinder(self):          self.value = 122
    def setTransformMatrix(self):      self.value = 124
    def setFlash(self):                self.value = 125
    def setRBSplineCurve(self):        self.value = 126
    def setRBSplineSurface(self):      self.value = 128
    def setOffsetCurve(self):          self.value = 130
    def setOffsetSurface(self):        self.value = 140
    def setBoundary(self):             self.value = 141
    def setCurveOnParaSurface(self):   self.value = 142
    def setBoundedSurface(self):       self.value = 143
    def setTrimmedParaSurface(self):   self.value = 144
    def setSphere(self):               self.value = 158
    def setTorus(self):                self.value = 160
    def setPlaneSurface(self):         self.value = 190
    def setRightCircCylSurf(self):     self.value = 192
    def setRightCircConSurf(self):     self.value = 194
    def setSphericalSurf(self):        self.value = 196
    def setToroidSurf(self):           self.value = 198


class IGESLineFontPattern(IGESParameter):
    def setNone(self):      self.value = 0
    def setSolid(self):     self.value = 1
    def setDashed(self):    self.value = 2
    def setPhantom(self):   self.value = 3
    def setCenterline(self): self.value = 4
    def setDotted(self):    self.value = 5


class IGESColorNumber(IGESParameter):
    def setNone(self):      self.value = 0
    def setBlack(self):     self.value = 1
    def setRed(self):       self.value = 2
    def setGreen(self):     self.value = 3
    def setBlue(self):      self.value = 4
    def setYellow(self):    self.value = 5
    def setMagenta(self):   self.value = 6
    def setCyan(self):      self.value = 7
    def setWhite(self):     self.value = 8


class IGESBlankStatus(IGESParameter):
    def setVisible(self):   self.value = 0
    def setBlanked(self):   self.value = 1


class IGESubordinate(IGESParameter):
    def setIndependent(self): self.value = 0
    def setPhysicallyDependent(self): self.value = 1
    def setLogicallyDependent(self): self.value = 2
    def setPysANDLogDependent(self): self.value = 3


class IGESEntityUseFlag(IGESParameter):
    def setGeometry(self): self.value = 0
    def setAnnotation(self): self.value = 1
    def setDefinition(self): self.value = 2
    def setOther(self): self.value = 3
    def setLogicORPositional(self): self.value = 4
    def set2DParametric(self): self.value = 5
    def setConstructionGeometry(self): self.value = 6


class IGESHierachy(IGESParameter):
    def setGlobalTopDown(self): self.value = 0
    def setGlobalDifer(self): self.value = 1
    def setUseHieracyProperty(self): self.value = 2


class IGESStatusNumber:
    def __init__(self):
        self.Visablilty = IGESBlankStatus()
        self.Subordinate = IGESubordinate()
        self.EntityUseFlag = IGESEntityUseFlag()
        self.Hierachy = IGESHierachy()

    def __str__(self):
        return "{:0>2}{:0>2}{:0>2}{:0>2}".format(self.Visablilty, self.Subordinate, self.EntityUseFlag, self.Hierachy)
