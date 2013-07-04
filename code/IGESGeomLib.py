#!python3.3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:57:00 2013
@author: Rod Persky
@license: Licensed under the Academic Free License ("AFL") v. 3.0
"""

from IGES.IGESCore import IGESItemData
import numpy as np


class IGESPoint:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z


class IGESGeomLine(IGESItemData):  # 116
    def __init__(self, startpoint, endpoint):
        IGESItemData.__init__(self)

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


class IGESGeomArc(IGESItemData):  # Wrapper of iges geometry
    def __init__(self, z, node, startpoint, endpoint):
        IGESItemData.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setCircularArc()

        self.AddParameters([z, node.x, node.y, startpoint.x, startpoint.y, endpoint.x, endpoint.y])


class IGESGeomCircle(IGESItemData):
    def __init__(self, node, radius):
        point = IGESPoint(node.x + radius, node.y, node.z)
        IGESGeomArc.__init__(self, node.z, node, point, point)


class IGESGeomTorus(IGESItemData):
    def __init__(self, r1, r2, node, vector):
        IGESItemData.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setTorus()

        self.AddParameters([r1, r2, node.x, node.y, node.z, vector.x, vector.y, vector.z])


class IGESGeomSphere(IGESItemData):
    def __init__(self, radius, node):
        IGESItemData.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setSphere()

        self.AddParameters([radius, node.x, node.y, node.z])


class IGESGeomPolyline(IGESItemData):
    """IGES Simple Closed Planar Curve Entity (Type 106, Form 63)
       Page 86"""
    def __init__(self):
        IGESItemData.__init__(self)
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
        self.ParameterData[1] = self.pointcount


class IGESGeomPoint(IGESItemData):
    def __init__(self, node):
        IGESItemData.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setPoint()

        self.AddParameters([node.x, node.y, node.z, 0])
