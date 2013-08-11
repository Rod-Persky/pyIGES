#!python3
# -*- coding: utf-8 -*-
"""
.. module:: IGES.IGESGeomLib
   :platform: Agnostic, Windows
   :synopsis: Main GUI program

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
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):  # Instead of using a if everywhere, make it a list
        return iter([self.x, self.y, self.z])


class IGESGeomPoint(IGESItemData):
    """
    :param node: Center point of the circle
    :type geometry: :py:class:`~pyiges.IGESGeomLib.IGESPoint` or [x, y, z]

    :param radius: Radius of the circle to be drawn either
    :type radius: :py:class:`~pyiges.IGESGeomLib.IGESPoint`, int or float

    Extension :py:class:`~pyiges.IGESGeomLib.IGESGeomArc` (Type 110, Form 0).
    Draw a simple circle constrained on the x plane."""
    def __init__(self, node):
        IGESItemData.__init__(self)
        self.EntityType.setPoint()
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1

        # Ensure that the data is indeed [x, y, z]
        for correct_length in range(len(list(node)), 3):
            node.append(0)

        self.AddParameters(node)
        self.AddParameters([0])

testpoint = IGESGeomPoint


class IGESExtrude(IGESItemData):  # 122
    def __init__(self, IGESObject, Length):
        IGESItemData.__init__(self)
        self.EntityType.setTabulatedCylinder()

        # Page 140 "Coordinates of the terminate point"!
        # Given we have the data at this point,
        #  we can just extract the startpoint

        object_type = type(IGESObject)

        if object_type == IGESGeomPolyline:
            startpoint = IGESObject.ParameterData[2:5]

        elif (object_type == IGESGeomCircle or
              object_type == IGESGeomArc):
            startpoint = IGESObject.ParameterData[3:5]
            startpoint.append(IGESObject.ParameterData[0])

        self.AddParameters([IGESObject.DirectoryDataPointer.data,
                            startpoint[0] + Length.x,
                            startpoint[1] + Length.y,
                            startpoint[2] + Length.z])

        #print(startpoint, '+', list(Length), '->', self.ParameterData[1:])


class IGESRevolve(IGESItemData):  # 120
    def __init__(self, profile, center_line, start_angle = 0, terminate_angle = pi * 2):
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
    """
    :param node: Center point of the circle
    :type geometry: :py:class:`~pyiges.IGESGeomLib.IGESPoint`

    :param radius: Radius of the circle to be drawn either
    :type radius: :py:class:`~pyiges.IGESGeomLib.IGESPoint`, int or float

    Extension :py:class:`~pyiges.IGESGeomLib.IGESGeomArc` (Type 110, Form 0).
    Draw a simple circle constrained on the x plane."""
    def __init__(self, node, radius):
        if type(node) is not IGESPoint:
            radius = IGESPoint(node.x + radius, node.y, node.z)

        IGESGeomArc.__init__(self, node.z, node, radius, radius)


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
    def __init__(self, *IGESPoints):
        IGESItemData.__init__(self)
        self.LineFontPattern.setSolid()

        self.EntityType.setClosedPlanarCurve()
        self.FormNumber = 12

        self.pointcount = 0
        self.AddParameters([2, self.pointcount])

        for Point in IGESPoints:
            self.AddPoint(Point)

    def AddPoint(self, Point):
        self.AddParameters(list(Point))

        self.pointcount = self.pointcount + 1
        self.ParameterData[1] = self.pointcount


class IGESGeomCompositeCurve(IGESItemData):  # 102
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


#===============================================================================
# class IGESCurveOnParametricSurface(IGESItemData):
#     """
#     142, Curve on a Parametric Surface Entity, Page 162"""
#     def __init__(self, *args):
#         IGESItemData.__init__(self)
#         self.EntityType.setCurveOnParaSurface()
#         self.FormNumber = 0
#
#         self.AddParameters(args)
#===============================================================================


class IGESCurveOnParametricSurface(IGESItemData):  # Page 193
    def __init__(self, IGESSurfaceS, IGESSurfaceB, IGESSurfaceC, pref):
        IGESItemData.__init__(self)
        self.EntityType.setCurveOnParaSurface()
        self.FormNumber = 0

        self.crtn = 1  # intersection of two surfaces
        self.AddParameters([self.crtn,
                            IGESSurfaceS.DirectoryDataPointer.data,
                            IGESSurfaceB.DirectoryDataPointer.data,
                            IGESSurfaceC.DirectoryDataPointer.data])
        self.AddParameters([pref])  # C is preferred

#class IGESTrimmedParaSurface(IGESItemData):
#    def __init__(self, *args):
#        """
#        144, Trimmed (Parametric) Surface Entity, Page 166
#        """
#        IGESItemData.__init__(self)
#        self.EntityType.setTrimmedParaSurface()
#       self.FormNumber = 0

#        self.AddParameters(args)


class IGESTrimmedParaSurface(IGESItemData):
    # 4.34 TRIMMED (PARAMETRIC) SURFACE ENTITY (TYPE 144)
    def __init__(self, trimmed_surface, outer_boundary_surface, *inner_boudary_surface):
        IGESItemData.__init__(self)
        self.EntityType.setTrimmedParaSurface()
        self.FormNumber = 0

        self.N1 = 1
        self.count_boundaries = 0  # N2

        try:
            outer_boundary_surface = outer_boundary_surface.DirectoryDataPointer.data
        except:
            pass

        self.AddParameters([trimmed_surface.DirectoryDataPointer.data,
                            self.N1,
                            self.count_boundaries,
                            outer_boundary_surface])

        for profile in inner_boudary_surface:
            self.add_bounding_profile(profile)

    def add_bounding_profile(self, inner_boudary_surface):
        if type(inner_boudary_surface) is not int:
            self.AddParameters([inner_boudary_surface.DirectoryDataPointer.data])
        else:
            self.AddParameters([inner_boudary_surface])

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

        for IGESObject in IGESObjects:
            self.AddObject(IGESObject)

    def AddObject(self, *IGESObjects):
        for IGESObject in IGESObjects:
            self.AddParameters([IGESObject.DirectoryDataPointer.data])
            self.entities_count = self.entities_count + 1
            self.ParameterData[2] = self.entities_count


class IGESTestSplineCurve(IGESItemData):
    def __init__(self):
        IGESItemData.__init__(self)
        self.EntityType.setLinearPath3D()
        self.FormNumber = 0

        self.AddParameters([3, 1, 3, 7, 0., 1., 2., 3., 4., 5., 6., 7., 5.817, 0.183686,
                            7.152560000000000E-007, 0.00391344, 7.42046, 0.116096,
                            - 1.430510000000000E-006, -0.0365138, 0.582714, 0.26764,
                            - 2.682210000000000E-007, -0.0384366, 6.0046, 0.195428, 0.011741,
                            - 0.0231148, 7.50004, 0.00655174, -0.109543, 0.0169944, 0.811917,
                            0.15233, -0.11531, -0.00673003, 6.18865, 0.149566, -0.0576034,
                            - 0.034095, 7.41404, -0.161551, -0.0585597, 0.0144959, 0.842207,
                            - 0.0984805, -0.1355, 0.000767251, 6.24652, -0.0679259, -0.159888,
                            0.0609804, 7.20843, -0.235182, -0.0150719, 0.0548643, 0.608993,
                            - 0.367179, -0.133198, 0.11326, 6.07969, -0.204761, 0.0230529,
                            - 0.00538516, 7.01304, -0.100733, 0.149521, -0.0375805, 0.221876,
                            - 0.293796, 0.206582, -0.0375974, 5.89259, -0.174811, 0.00689745,
                            0.041456, 7.02425, 0.0855677, 0.0367796, 0.0150364, 0.0970648,
                            0.00657602, 0.0937898, 0.0214335, 5.76614, -0.0366479, 0.131266,
                            - 0.0437549, 7.16163, 0.204236, 0.0818889, -0.0272963, 0.218864,
                            0.258456, 0.15809, -0.0526968, 5.817, 0.0946183,
                            1.430510000000000E-006, -0.26253, 7.42046, 0.286125, 0., -0.163778,
                            0.582714, 0.146546, -1.713630000000000E-007, -0.316181])


class IGESTestSplineSurf(IGESItemData):
    def __init__(self):
        IGESItemData.__init__(self)
        self.EntityType.setSplineSurface()

        self.FromNumber = 0

        #self.StatusNumber.EntityUseFlag.setDefinition()
        #self.StatusNumber.Hierachy.setGlobalDefer()

        #self.AddParameters([3])  # Cubic
        #self.AddParameters([1])  # Cartesian Product

        #self.number_of_u_segments = 0  # aka. M
        #self.number_of_v_segments = 0  # aka. N

        #self.AddParameters([self.number_of_u_segments,
        #                    self.number_of_v_segments])

        self.AddParameters([3, 1, 1, 3, 0., 1., 0., 1., 2., 3., 6.5, 0., 0., 0., -0.166666, 8.583070000000001E-006,
                            - 1.287460000000000E-005, 4.291530000000000E-006, -1.430510000000000E-006, -1.502040000000000E-005,
                            2.253060000000000E-005, -7.510190000000000E-006, -0.0833325, 6.437300000000000E-006, -9.655950000000000E-006,
                            3.218650000000000E-006, 7.5, -0.75, 0., 0., -0.0999956, 4.291530000000000E-006, -4.291530000000000E-006, 0.,
                            - 5.960460000000000E-006, -1.072880000000000E-006, -2.145770000000000E-006, 3.218650000000000E-006, 0.100002,
                            - 3.576280000000000E-007, 2.145770000000000E-006, -1.788140000000000E-006, 1., -1., -1.192090000000000E-007,
                            5.960460000000000E-008, 0., 0., 0., 0., 0., 5.364420000000000E-007, -7.152560000000000E-007,
                            1.788140000000000E-007, 0., -3.576280000000000E-007, 4.768370000000000E-007, -1.192090000000000E-007, 6.25,
                            0., 0., 0., -0.416667, -2.145770000000000E-006, 3.218650000000000E-006, -1.072880000000000E-006, -0.249998,
                            3.218650000000000E-006, -5.364420000000000E-006, 2.145770000000000E-006, 0.166666, -1.072880000000000E-006,
                            2.145770000000000E-006, -1.072880000000000E-006, 7.5, -0.749997, -4.291530000000000E-006,
                            1.430510000000000E-006, 0.199999, 1.072880000000000E-006, -2.145770000000000E-006, 1.072880000000000E-006,
                            0.300002, -5.364420000000000E-006, 1.072880000000000E-005, -6.794930000000000E-006, -0.25,
                            2.861020000000000E-006, -5.722050000000000E-006, 3.814700000000000E-006, 1., -1., -3.576280000000000E-007,
                            1.192090000000000E-007, 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 5.75, 0., 0., 0., -0.416666,
                            1.072880000000000E-006, -1.072880000000000E-006, 0., 0.249998, 2.145770000000000E-006,
                            - 2.145770000000000E-006, 0., -0.0833328, -3.218650000000000E-006, 3.218650000000000E-006, 0., 7.75, -0.749999,
                            - 1.430510000000000E-006, -4.768370000000000E-007, 0.0500009, -1.072880000000000E-006, 2.145770000000000E-006,
                            - 1.072880000000000E-006, -0.450001, 2.145770000000000E-006, -4.291530000000000E-006, 3.576280000000000E-006,
                            0.149999, -2.503400000000000E-006, 3.576280000000000E-006, -2.026560000000000E-006, 1., -1.,
                            - 3.576280000000000E-007, 1.192090000000000E-007, 0., 0., 0., 0., 0., -5.364420000000000E-007,
                            7.152560000000000E-007, -1.788140000000000E-007, 0., 3.576280000000000E-007, -4.768370000000000E-007,
                            1.192090000000000E-007, 5.5, 0., 0., 0., -0.166669, -4.291530000000000E-006, 4.291530000000000E-006, 0.,
                            0.500007, 1.287460000000000E-005, -1.287460000000000E-005, 0., -0.333338, -8.583070000000001E-006,
                            8.583070000000001E-006, 0., 7.5, -0.75, 0., 0., -0.400002, -4.291530000000000E-006, 4.291530000000000E-006,
                            0., 1.20001, 1.287460000000000E-005, -1.287460000000000E-005, 0., -0.800005, -8.583070000000001E-006,
                            8.583070000000001E-006, 0., 1., -1., -1.192090000000000E-007, 5.960460000000000E-008, 0., 0., 0., 0., 0., 0.,
                            0., 0., 0., 0., 0., 0., 6.5, 0., 0., 0., -0.166666, -4.291530000000000E-006, 1.287460000000000E-005,
                            - 8.583070000000001E-006, -1.430510000000000E-006, 7.510190000000000E-006, -2.253060000000000E-005,
                            1.502040000000000E-005, -0.0833325, -3.218650000000000E-006, 9.655950000000000E-006, -6.437300000000000E-006,
                            6.75, -0.75, 2.25, -1.5, -0.0999956, -4.291530000000000E-006, 1.287460000000000E-005, -8.583070000000001E-006,
                            - 5.960460000000000E-006, 4.291530000000000E-006, -1.287460000000000E-005, 8.583070000000001E-006, 0.100002,
                            - 1.430510000000000E-006, 4.291530000000000E-006, -2.861020000000000E-006, 0., -1., 3., -2., 0., 0., 0., 0.,
                            0., -3.576280000000000E-007, 1.072880000000000E-006, -7.152560000000000E-007, 0., 2.384190000000000E-007,
                            - 7.152560000000000E-007, 4.768370000000000E-007, 6.25, 0., 0., 0., -0.416667, 1.072880000000000E-006,
                            - 3.218650000000000E-006, 2.145770000000000E-006, -0.249998, -1.072880000000000E-006, 3.218650000000000E-006,
                            - 2.145770000000000E-006, 0.166666, 0., 0., 0., 6.75, -0.750001, 2.25, -1.5, 0.199999, 0., 0., 0., 0.3,
                            - 4.291530000000000E-006, 1.287460000000000E-005, -8.583070000000001E-006, -0.25, 2.861020000000000E-006,
                            - 8.583070000000001E-006, 5.722050000000000E-006, 0., -1., 3., -2., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                            0., 5.75, 0., 0., 0., -0.416666, -1.072880000000000E-006, 3.218650000000000E-006, -2.145770000000000E-006,
                            0.249998, -2.145770000000000E-006, 6.437300000000000E-006, -4.291530000000000E-006, -0.0833328,
                            3.218650000000000E-006, -9.655950000000000E-006, 6.437300000000000E-006, 7., -0.750003, 2.25001, -1.50001,
                            0.0500009, 0., 0., 0., -0.449999, 4.291530000000000E-006, -1.287460000000000E-005, 8.583070000000001E-006,
                            0.149998, -1.430510000000000E-006, 4.291530000000000E-006, -2.861020000000000E-006, 0., -1., 3., -2., 0., 0.,
                            0., 0., 0., 3.576280000000000E-007, -1.072880000000000E-006, 7.152560000000000E-007, 0.,
                            - 2.384190000000000E-007, 7.152560000000000E-007, -4.768370000000000E-007, 5.5, 0., 0., 0., -0.166669,
                            4.291530000000000E-006, -1.287460000000000E-005, 8.583070000000001E-006, 0.500007, -1.287460000000000E-005,
                            3.862380000000000E-005, -2.574920000000000E-005, -0.333338, 8.583070000000001E-006, -2.574920000000000E-005,
                            1.716610000000000E-005, 6.75, -0.75, 2.25, -1.5, -0.400002, 4.291530000000000E-006, -1.287460000000000E-005,
                            8.583070000000001E-006, 1.20001, -1.287460000000000E-005, 3.862380000000000E-005, -2.574920000000000E-005,
                            - 0.800005, 8.583070000000001E-006, -2.574920000000000E-005, 1.716610000000000E-005, 0., -1., 3., -2., 0., 0.,
                            0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])


#===============================================================================
#  TESTING
#===============================================================================

import unittest


class test_IGESGeomPoint(unittest.TestCase):
    def using_IGESPoint(self):
        point = IGESGeomPoint(IGESPoint(1, 2, 3))  # correct usage
        assert point.ParameterData == [1, 2, 3, 0], 'IGESGeomPoint convert from IGESPoint fail'

    def using_List(self):
        point = IGESGeomPoint([1, 2, 3])  # correct length but is a list
        assert point.ParameterData == [1, 2, 3, 0], 'IGESGeomPoint convert from [x, y, z] list fail'

    def using_XYList(self):
        point = IGESGeomPoint([1, 2])  # incorrect length
        assert point.ParameterData == [1, 2, 0, 0], 'IGESGeomPoint convert from [x, y] list fail'


class test_IGESGeomCircle(unittest.TestCase):
    def using_int_Radius(self):
        circle = IGESGeomCircle(IGESPoint(5, 5, 0), 5)

    def using_IGESPoint_radius(self):
        circle = IGESGeomCircle(IGESPoint(0, 0, 0), IGESPoint(5, 5, 0))
