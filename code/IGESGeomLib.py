#!python3.3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:57:00 2013
@author: Rod Persky <rodney.persky@gmail.com
@license: Licensed under the Academic Free License ("AFL") v. 3.0
"""

from IGESDirectoryEntry import IGESDirectoryEntry
from IGESParameterEntry import IGESParameterEntry
import numpy as np

# 116
class IGESPoint:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
#    def __str__(self):
#        return "X={:}, Y={:}, Z={:}".format(self.x, self.y, self.z)

class IGESGeomLine(IGESDirectoryEntry, IGESParameterEntry):  # Wrapper of iges geometry
    def __init__(self, startpoint, endpoint):
        IGESDirectoryEntry.__init__(self)
        IGESParameterEntry.__init__(self)

        self.LineFontPattern.setDashed()
        self.Color.setBlue()
        self.StatusNumber.Hierachy.setGlobalDifer()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setLine()

        self.AddParameters([startpoint.x, startpoint.y, startpoint.z,
                            endpoint.x, endpoint.y, endpoint.z])

class IGESCentLinePt(IGESGeomLine):
    def __init__(self, node, theta, length):

        xoffset = length * 0.5 * np.cos(theta)
        yoffset = length * 0.5 * np.sin(theta)

        startpoint = IGESPoint(node.x + xoffset, node.y + yoffset)
        endpoint = IGESPoint(node.x - xoffset, node.y - yoffset)

        startpoint.x = np.around(startpoint.x, 7)
        startpoint.y = np.around(startpoint.y, 7)
        endpoint.x = np.around(endpoint.x, 7)
        endpoint.y = np.around(endpoint.y, 7)


        IGESGeomLine.__init__(self, startpoint, endpoint)

class IGESMultilineTest(IGESDirectoryEntry, IGESParameterEntry):
        def __init__(self, otherpointer):
            IGESDirectoryEntry.__init__(self)
            IGESParameterEntry.__init__(self)
            self.LineFontPattern.setSolid()
            self.LineWeightNum = 1
            self.ParameterLC = 1

            self.EntityType.setCircularArc()

            if otherpointer.data == 0:
                raise ValueError("Commit sibling before creating parent")

            self.AddParameters([otherpointer.data, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi,
                                np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi,
                                np.pi, np.pi, np.pi, np.pi, np.pi, np.pi, np.pi])

class IGESGeomArc(IGESDirectoryEntry, IGESParameterEntry):  # Wrapper of iges geometry
    def __init__(self, z, node, startpoint, endpoint):
        IGESDirectoryEntry.__init__(self)
        IGESParameterEntry.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setCircularArc()

        self.AddParameters([z, node.x, node.y, startpoint.x, startpoint.y, endpoint.x, endpoint.y])


class IGESGeomCircle(IGESDirectoryEntry, IGESParameterEntry):
    def __init__(self, node, radius):
        point = IGESPoint(node.x + radius, node.y, node.z)
        IGESGeomArc.__init__(self, node.z, node, point, point)

class IGESGeomTorus(IGESDirectoryEntry, IGESParameterEntry):
    def __init__(self, r1, r2, node, vector):
        IGESDirectoryEntry.__init__(self)
        IGESParameterEntry.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setTorus()

        self.AddParameters([r1, r2, node.x, node.y, node.z, vector.x, vector.y, vector.z])

class IGESGeomSphere(IGESDirectoryEntry, IGESParameterEntry):
    def __init__(self, radius, node):
        IGESDirectoryEntry.__init__(self)
        IGESParameterEntry.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setSphere()

        self.AddParameters([radius, node.x, node.y, node.z])

class IGESGeomPolyline(IGESDirectoryEntry, IGESParameterEntry):
    """IGES Simple Closed Planar Curve Entity (Type 106, Form 63)
       Page 86"""
    def __init__(self):
        IGESDirectoryEntry.__init__(self)
        IGESParameterEntry.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setCopiousData()
        self.FormNumber = 63

        self.pointcount = 0
        self.AddParameters([2, self.pointcount])

    def AddPoint(self, point):
        self.AddParameters([point.x, point.y, point.z])
        self.pointcount = self.pointcount + 1
        self.data[1] = self.pointcount

class IGESGeomPoint(IGESDirectoryEntry, IGESParameterEntry):
    def __init__(self, node):
        IGESDirectoryEntry.__init__(self)
        IGESParameterEntry.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setPoint()

        self.AddParameters([node.x, node.y, node.z, 0])

