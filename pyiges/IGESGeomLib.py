#!python3.3
# -*- coding: utf-8 -*-
"""
.. module:: IGES.IGESGeomLib
   :platform: Agnostic, Windows
   :synopsis: Main GUI program

.. requires numpy

.. Created on Sun Mar 31 16:57:00 2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES
"""

# External Libraries / Modules
from math import pi

# Internal Modules
from pyiges.IGESCore import IGESItemData


class IGESPoint:  # BASIC ITEM, NOT A GEOM ITEM
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z


class IGESGeomPoint(IGESItemData):
    def __init__(self, node):
        IGESItemData.__init__(self)
        self.EntityType.setPoint()
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.AddParameters([node.x, node.y, node.z, 0])

class IGESExtrude(IGESItemData):  #122
    def __init__(self, IGESObject, Length):
        IGESItemData.__init__(self)
        self.EntityType.setTabulatedCylinder()
        
        if type(IGESObject) == int:
            raise DeprecationWarning("IGESExtrude now uses the IGESObject directly!")
        
        # Page 140 "Coordinates of the terminate point"!
        # Given we have the data at this point,
        #  we can just extract the startpoint
        startpoint = IGESObject.ParameterData[2:5]
        


        self.AddParameters([IGESObject.DirectoryDataPointer.data,
                            startpoint[0] + Length.x,
                            startpoint[1] + Length.y,
                            startpoint[2] + Length.z])


class IGESRevolve(IGESItemData):  # 120
    def __init__(self, profile, center_line, start_angle=0, terminate_angle=pi*2):
        IGESItemData.__init__(self)
        self.EntityType.setRevolvedSurface()

        self.AddParameters([center_line.DirectoryDataPointer.data,
                            profile.DirectoryDataPointer.data,
                            start_angle,
                            terminate_angle])


class IGESGeomLine(IGESItemData):  # 116
    def __init__(self, startpoint, endpoint):
        IGESItemData.__init__(self)
        self.EntityType.setLine()

        self.AddParameters([startpoint.x, startpoint.y, startpoint.z,
                            endpoint.x, endpoint.y, endpoint.z])


#===============================================================================
# class IGESCentLinePt(IGESGeomLine):
#     def __init__(self, node, theta, length):
# 
#         xoffset = length * 0.5 * np.cos(theta)
#         yoffset = length * 0.5 * np.sin(theta)
# 
#         startpoint = IGESPoint(node.x + xoffset, node.y + yoffset)
#         endpoint = IGESPoint(node.x - xoffset, node.y - yoffset)
# 
#         startpoint.x = np.around(startpoint.x, 7)
#         startpoint.y = np.around(startpoint.y, 7)
#         endpoint.x = np.around(endpoint.x, 7)
#         endpoint.y = np.around(endpoint.y, 7)
# 
#         IGESGeomLine.__init__(self, startpoint, endpoint)
#===============================================================================


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
       Page 86
       123"""
    def __init__(self, *args):
        IGESItemData.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        self.EntityType.setCopiousData()
        self.FormNumber = 63

        self.pointcount = 0
        self.AddParameters([2, self.pointcount])
        
        for IGESPoint in args:
            self.AddPoint(IGESPoint)

    def AddPoint(self, point):
        self.AddParameters([point.x, point.y, point.z])
        self.pointcount = self.pointcount + 1
        self.ParameterData[1] = self.pointcount


class IGESGeomCompositeCurve(IGESItemData):  #102
    def __init__(self, *args):
        IGESItemData.__init__(self)
        self.EntityType.setCompositeCurve()
        self.FormNumber = 0
        
        self.object_count = 0
        self.AddParameters(self.object_count)
        
        for IGESObject in args:
            self.AddObject(IGESObject)
    
    def AddObject(self, IGESObject):
        self.object_count = self.object_count + 1
        self.AddParameters(IGESObject.DirectoryDataPointer.data)
        self.ParameterData[1] = self.object_count
        

#===============================================================================
# class IGESGeomPlaneaaaa(IGESItemData):
#     def __init__(self):
#         IGESItemData.__init__(self)
#         self.EntityType.setClosedPlanarCurve()
#         self.FormNumber = 63
#         
#         self.AddParameters([2])  # Page 115, x, y, z
#         
#         self.pointcount = 0
#         self.AddParameters([self.pointcount])
#         
#         self.AddParameters([0])
#         
#     def AddPoint(self, *args):
#         """Add surface bounding point
#         *args is IGESPoint"""
#         
#         for IGESPoint in args:
#             self.AddParameters([IGESPoint.x, IGESPoint.y, IGESPoint.z])
#             self.pointcount = self.pointcount + 1
#             self.ParameterData[1] = self.pointcount
#===============================================================================


class IGESGeomPlane(IGESItemData):
    def __init__(self, bounding_profile):
        IGESItemData.__init__(self)
        self.EntityType.setPlane()
        self.FormNumber = 1
        
        self.coefficients = [0, 0, 1, 0]
        self.AddParameters(self.coefficients)
        self.AddParameters([bounding_profile.DirectoryDataPointer.data])
        self.AddParameters([0, 0])
        
    def setRemove(self):
        self.FormNumber = -1
    

class IGESGeomIntersectionSurfaces(IGESItemData):  # Page 193
    def __init__(self, IGESSurfaceS, IGESSurfaceB, IGESSurfaceC):
        IGESItemData.__init__(self)
        self.EntityType.setCurveOnParaSurface()
        self.FormNumber = 0
        
        self.crtn = 2  # intersection of two surfaces
        self.AddParameters([self.crtn,
                            IGESSurfaceS.DirectoryDataPointer.data,
                            IGESSurfaceB.DirectoryDataPointer.data,
                            IGESSurfaceC.DirectoryDataPointer.data])
        self.AddParameters([2])  # C is preferred
        
        

class IGESGeomTrimSurface(IGESItemData):
    def __init__(self, first_surface, *IGESClosedProfile):
        IGESItemData.__init__(self)
        self.EntityType.setBoundedSurface()
        self.FormNumber = 0
        
        self.type = 1
        self.sptr = first_surface.DirectoryDataPointer.data
        self.count_boundaries = 0
        
        self.AddParameters([self.type, self.sptr, self.count_boundaries])
        
        for profile in IGESClosedProfile:
            self.add_bounding_profile(profile)
            
    def add_bounding_profile(self, IGESClosedProfile):
        self.AddParameters([IGESClosedProfile.DirectoryDataPointer.data])
        self.count_boundaries = self.count_boundaries + 1
        self.ParameterData[2] = self.count_boundaries


class IGESGeomTransform(IGESItemData):
    """ Transform / Move Geometry"""
     
    def __init__(self, transform_matrix):
        IGESItemData.__init__(self)
        self.EntityType.setTransformMatrix()
        self.FormNumber = 0
        
        if len(transform_matrix) == 9:
            self.AddParameters(transform_matrix)
        else:
            raise TypeError("A transform matrix is 9 numbers")
        
        
class IGESCircularArray(IGESItemData): # 414
    """
    :param geometry: Geometry that is to be put into a circular array
    :type geometry: :py:class:`~pyiges.IGESGeomLib.IGESGroup` or IGES Object
    
    :param int number: Number of occurance there should be of the geometry,
                   starting from 1.
                   
    :param center: The node that rotation is done about
    :type center: :py:class:`~pyiges.IGESGeomLib.IGESPoint`
    
    :param radius: Radius of the circle the objects are inscribed about
    :type radius: int or float
    
    :param start_angle: Int/Float andle in _radians_ of the starting point
    :type start_angle: int or float
    
    :param delta_angle: Int/Float angle across which the objects are distributed
    :type delta_angle: int or float
    
    IGES Circular Array (Type 414, Form 0). Duplicate a form or group in a circle.
    See :py:mod:`examples.benchmarks.414_0.414_000` for how this function works."""
    def __init__(self, geometry, number, center,
                 radius, start_angle, delta_angle):
        IGESItemData.__init__(self)
        self.EntityType.setCircularArray()
        self.FormNumber = 0
        
        self.add_extended_data = False
        
        self.AddParameters([geometry.DirectoryDataPointer.data])
        self.AddParameters([number])
        self.AddParameters([center.x, center.y, center.z])
        self.AddParameters([radius])
        self.AddParameters([start_angle, delta_angle])
        self.AddParameters([0])
        
        
class IGESGroup(IGESItemData):
    def __init__(self, name, *IGESObjects):
        IGESItemData.__init__(self)
        self.EntityType.setSubfigureInstance()
        
        self.FormNumber = 0
        self.StatusNumber.EntityUseFlag.setDefinition()
        self.StatusNumber.Hierachy.setGlobalDefer()
        
        self.AddParameters([0])
        self.AddParameters([name])
        self.entities_count = 0
        self.AddParameters(self.entities_count)

        self.add_extended_data = False
        
        for IGESObject in IGESObjects:
            self.AddObject(IGESObject)
            
    def AddObject(self, *IGESObjects):
        for IGESObject in IGESObjects:
            self.AddParameters([IGESObject.DirectoryDataPointer.data])
            self.entities_count = self.entities_count + 1
            self.ParameterData[2] = self.entities_count
