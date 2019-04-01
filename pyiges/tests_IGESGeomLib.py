#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: IGES.IGESGeomLib
   :platform: Agnostic, Windows
   :synopsis: Main GUI program

.. requires math (unittest)

.. Created on Sun Mar 31 16:57:00 2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES
"""

# External Libraries / Modules
import unittest

# Internal Modules
from pyiges.IGESGeomLib import IGESPoint, IGESGeomPoint, IGESGeomCircle
import pyiges


class Test_IGESGeomPoint(unittest.TestCase):
    def test_using_IGESPoint(self):
        point = IGESGeomPoint(IGESPoint(1, 2, 3))  # correct usage
        self.assertEqual(point.ParameterData, [1, 2, 3, 0], msg='IGESGeomPoint convert from IGESPoint fail')

    def test_using_List(self):
        point = IGESGeomPoint([1, 2, 3])  # correct length but is a list
        self.assertEqual(point.ParameterData, [1, 2, 3, 0], msg='IGESGeomPoint convert from [x, y, z] list fail')

    def test_using_XYList(self):
        point = IGESGeomPoint([1, 2])  # incorrect length
        self.assertEqual(point.ParameterData, [1, 2, 0, 0], msg='IGESGeomPoint convert from [x, y] list fail')


class Test_IGESGeomCircle(unittest.TestCase):
    def test_using_int_Radius(self):
        circle = IGESGeomCircle(IGESPoint(5, 5, 0), 5)
        self.assertEqual(circle.ParameterData, [0, 5, 5, 10, 5, 10, 5], msg='IGESGeomCircle convert from [IGESPoint, radius] list fail')

    def test_using_IGESPoint_radius(self):
        circle = IGESGeomCircle(IGESPoint(0, 0, 0), IGESPoint(5, 5, 0))
        self.assertEqual(circle.ParameterData, [0, 0, 0, 5, 5, 5, 5], msg='IGESGeomCircle convert from [IGESPoint, IGESPoint] list fail')

if __name__ == '__main__':
    unittest.main()
