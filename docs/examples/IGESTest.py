#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: examples.IGESTest
   :platform: Agnostic
   :synopsis: Test IGES system

.. requires numpy, os (startfile)

.. Created on Tue Apr  2 18:33:27 2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES
"""

# External Libraries / Modules
from os import (startfile, environ)

try:
    import numpy
except:
    if environ.get('READTHEDOCS', None) == 'True':
        import mock
        numpy = mock.Mock(return_value = None)


# Internal Modules
from pyiges.IGESCore import IGEStorage
from pyiges.IGESGeomLib import IGESPoint, IGESVector
import pyiges.IGESGeomLib as IGES
from GeomLib import bezier_curve


def testrun():
    # testrun_torus()
    testrun_extrude_arc()
    testrun_arc_circle()
    testrun_polyline()
    testrun_rotate_polyline()
    testrun_extrude_polyline()
    # testrun_random_surface()
    testrun_spline_curve()


def testrun_torus(filename="IGESFile_torus.igs"):
    """Dont know if this works, neither FreeCAD not IGES Viewer will display anyting for a torus element"""
    system = IGEStorage()
    system.StartSection.Prolog = " "
    system.GlobalSection.IntegerBits = int(32)
    system.GlobalSection.SPMagnitude = int(38)
    system.GlobalSection.SPSignificance = int(6)
    system.GlobalSection.DPMagnitude = int(38)
    system.GlobalSection.DPSignificance = int(15)
    system.GlobalSection.MaxNumberLineWeightGrads = int(8)
    system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
    system.GlobalSection.MaxCoordValue = float(71)

    torus = IGES.IGESGeomTorus(50, 10, IGESPoint(0,0,0), IGESVector(0,0,1))
    system.Commit(torus)
    system.save(filename)


def testrun_extrude_arc(filename="IGESFile_extrude_arc.igs"):
    """draw arc and extrude it to a target points"""
    system = IGEStorage()
    system.StartSection.Prolog = " "
    system.GlobalSection.IntegerBits = int(32)
    system.GlobalSection.SPMagnitude = int(38)
    system.GlobalSection.SPSignificance = int(6)
    system.GlobalSection.DPMagnitude = int(38)
    system.GlobalSection.DPSignificance = int(15)
    system.GlobalSection.MaxNumberLineWeightGrads = int(8)
    system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
    system.GlobalSection.MaxCoordValue = float(71)

    arc = IGES.IGESGeomArc(0, IGESPoint(20, 11, 0), IGESPoint(20.25, 11, 0), IGESPoint(19.75, 11, 0))
    system.Commit(arc)

    ext = IGES.IGESExtrude(arc, IGESPoint(20.4857, 11.2357, -0.9428))
    system.Commit(ext)

    system.save(filename)


def testrun_arc_circle(filename="IGESFile_arc_circle.igs"):
    """draw an arc and a circle, both in a plane paralell to the X-Y-plane"""
    system = IGEStorage()
    system.StartSection.Prolog = " "
    system.GlobalSection.IntegerBits = int(32)
    system.GlobalSection.SPMagnitude = int(38)
    system.GlobalSection.SPSignificance = int(6)
    system.GlobalSection.DPMagnitude = int(38)
    system.GlobalSection.DPSignificance = int(15)
    system.GlobalSection.MaxNumberLineWeightGrads = int(8)
    system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
    system.GlobalSection.MaxCoordValue = float(71)

    arc = IGES.IGESGeomArc(-3, IGESPoint(2, 5, 0), IGESPoint(-3, 0, 0), IGESPoint(2, 10, 0))
    system.Commit(arc)

    circ = IGES.IGESGeomCircle(IGESPoint(5, 5, 5), 5)
    system.Commit(circ)

    system.save(filename)


def testrun_polyline(filename="IGESFile_polyline.igs"):
    """draw a poly line"""
    system = IGEStorage()
    system.StartSection.Prolog = " "
    system.GlobalSection.IntegerBits = int(32)
    system.GlobalSection.SPMagnitude = int(38)
    system.GlobalSection.SPSignificance = int(6)
    system.GlobalSection.DPMagnitude = int(38)
    system.GlobalSection.DPSignificance = int(15)
    system.GlobalSection.MaxNumberLineWeightGrads = int(8)
    system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
    system.GlobalSection.MaxCoordValue = float(71)

    # add poly line from numpy array
    P = [[0, 0],
         [numpy.divide(1, 3), numpy.divide(numpy.pi, 6)],
         [numpy.divide(2, 3), 1],
         [1, 1],
         [1 + numpy.divide(1, 3), 1],
         [1 + numpy.divide(2, 3), numpy.divide(numpy.pi, 6)],
         [2, 0],
         [2 + numpy.divide(1, 3), 0 - numpy.divide(numpy.pi, 6)],
         [2 + numpy.divide(2, 3), 0 - 1],
         [3, 0 - 1],
         [3 + numpy.divide(1, 3), 0 - 1],
         [3 + numpy.divide(2, 3), 0 - numpy.divide(numpy.pi, 6)],
         [4, 0]]
    for i in range(0, 1):
        P.extend
    P = numpy.transpose(P)
    bezi = bezier_curve(P, nTimes = 50)
    polyln = IGES.IGESGeomPolyline()
    for n in range(0, 5):
        for i in range(0, len(bezi[0])):
            polyln.AddPoint(IGESPoint(bezi[0][i], bezi[1][i], 10))
        bezi[0] = bezi[0] + 4
    system.Commit(polyln)

    system.save(filename)


def testrun_rotate_polyline(filename="IGESFile_rotate_polyline.igs"):
    """draw a poly line and rotate it around a line to for a cylindrical object"""
    system = IGEStorage()
    system.StartSection.Prolog = " "
    system.GlobalSection.IntegerBits = int(32)
    system.GlobalSection.SPMagnitude = int(38)
    system.GlobalSection.SPSignificance = int(6)
    system.GlobalSection.DPMagnitude = int(38)
    system.GlobalSection.DPSignificance = int(15)
    system.GlobalSection.MaxNumberLineWeightGrads = int(8)
    system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
    system.GlobalSection.MaxCoordValue = float(71)

    # add poly line from numpy array
    P = [[0, 0],
         [numpy.divide(1, 3), numpy.divide(numpy.pi, 6)],
         [numpy.divide(2, 3), 1],
         [1, 1],
         [1 + numpy.divide(1, 3), 1],
         [1 + numpy.divide(2, 3), numpy.divide(numpy.pi, 6)],
         [2, 0],
         [2 + numpy.divide(1, 3), 0 - numpy.divide(numpy.pi, 6)],
         [2 + numpy.divide(2, 3), 0 - 1],
         [3, 0 - 1],
         [3 + numpy.divide(1, 3), 0 - 1],
         [3 + numpy.divide(2, 3), 0 - numpy.divide(numpy.pi, 6)],
         [4, 0]]
    for i in range(0, 1):
        P.extend
    P = numpy.transpose(P)
    bezi = bezier_curve(P, nTimes = 50)
    polyln = IGES.IGESGeomPolyline()
    for n in range(0, 5):
        for i in range(0, len(bezi[0])):
            polyln.AddPoint(IGESPoint(bezi[0][i], bezi[1][i], 10))
        bezi[0] = bezi[0] + 4
    system.Commit(polyln)

    # add straight line
    line = IGES.IGESGeomLine(IGESPoint(-2, -5, 0), IGESPoint(22, -5, 0))
    system.Commit(line)

    # revolve polyline around line
    system.Commit(IGES.IGESRevolve(polyln, line))

    system.save(filename)


def testrun_extrude_polyline(filename="IGESFile_extrude_polyline.igs"):
    """draw a poly line and extrude it to a target points"""
    system = IGEStorage()
    system.StartSection.Prolog = " "
    system.GlobalSection.IntegerBits = int(32)
    system.GlobalSection.SPMagnitude = int(38)
    system.GlobalSection.SPSignificance = int(6)
    system.GlobalSection.DPMagnitude = int(38)
    system.GlobalSection.DPSignificance = int(15)
    system.GlobalSection.MaxNumberLineWeightGrads = int(8)
    system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
    system.GlobalSection.MaxCoordValue = float(71)

    # add poly line from numpy array
    P = [[0, 0],
         [numpy.divide(1, 3), numpy.divide(numpy.pi, 6)],
         [numpy.divide(2, 3), 1],
         [1, 1],
         [1 + numpy.divide(1, 3), 1],
         [1 + numpy.divide(2, 3), numpy.divide(numpy.pi, 6)],
         [2, 0],
         [2 + numpy.divide(1, 3), 0 - numpy.divide(numpy.pi, 6)],
         [2 + numpy.divide(2, 3), 0 - 1],
         [3, 0 - 1],
         [3 + numpy.divide(1, 3), 0 - 1],
         [3 + numpy.divide(2, 3), 0 - numpy.divide(numpy.pi, 6)],
         [4, 0]]
    for i in range(0, 1):
        P.extend
    P = numpy.transpose(P)
    bezi = bezier_curve(P, nTimes = 50)
    polyln = IGES.IGESGeomPolyline()
    for n in range(0, 5):
        for i in range(0, len(bezi[0])):
            polyln.AddPoint(IGESPoint(bezi[0][i], bezi[1][i], 10))
        bezi[0] = bezi[0] + 4
    system.Commit(polyln)

    # extrude polyline to endpoint
    system.Commit(IGES.IGESExtrude(polyln, IGESPoint(0, 0, 15)))

    system.save(filename)


def testrun_random_surface(filename="IGESFile_random_surface.igs"):
    """draw a randomiced surface consisting of b spline surface segments"""
    system = IGEStorage()
    system.StartSection.Prolog = " "
    system.GlobalSection.IntegerBits = int(32)
    system.GlobalSection.SPMagnitude = int(38)
    system.GlobalSection.SPSignificance = int(6)
    system.GlobalSection.DPMagnitude = int(38)
    system.GlobalSection.DPSignificance = int(15)
    system.GlobalSection.MaxNumberLineWeightGrads = int(8)
    system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
    system.GlobalSection.MaxCoordValue = float(71)

    scale = 2.5
    # data = numpy.zeros(shape=(3,5), dtype=int)
    data = numpy.random.rand(100, 100)
    # print("random data generated:", data.shape)

    for line_nr in range(0, data.shape[0]-1):
        # print("line number:", line_nr)
        for row_nr in range(0, data.shape[1]-1):
            x1 = line_nr * scale
            x2 = (line_nr + 1) * scale
            y1 = row_nr * scale
            y2 = (row_nr + 1) * scale
            p1 = IGESPoint(x1, y1, float(data[line_nr][row_nr]))
            p2 = IGESPoint(x2, y1, float(data[line_nr+1][row_nr]))
            p3 = IGESPoint(x1, y2, float(data[line_nr][row_nr+1]))
            p4 = IGESPoint(x2, y2, float(data[line_nr+1][row_nr+1]))
            square = IGES.IGESRationalBSplineSurface(p1, p2, p3, p4)
            system.Commit(square)

    # print("save file:", line_nr)
    system.save(filename)


def testrun_spline_curve(filename="IGESFile_spline_curve.igs"):
    """draw a spline curve"""
    system = IGEStorage()
    system.StartSection.Prolog = " "
    system.GlobalSection.IntegerBits = int(32)
    system.GlobalSection.SPMagnitude = int(38)
    system.GlobalSection.SPSignificance = int(6)
    system.GlobalSection.DPMagnitude = int(38)
    system.GlobalSection.DPSignificance = int(15)
    system.GlobalSection.MaxNumberLineWeightGrads = int(8)
    system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
    system.GlobalSection.MaxCoordValue = float(71)

    spline_curve = IGES.IGESSplineCurve(stype=3, h=1, ndim=3)
    spline_curve.addSegment(0., [5.817, 0.183686, 7.152560000000000E-007, 0.00391344,
                                 7.42046, 0.116096, -1.430510000000000E-006, -0.0365138,
                                 0.582714, 0.26764, -2.682210000000000E-007, -0.0384366])
    spline_curve.addSegment(1., [6.0046, 0.195428, 0.011741, -0.0231148,
                                 7.50004, 0.00655174, -0.109543, 0.0169944,
                                 0.811917, 0.15233, -0.11531, -0.00673003])
    spline_curve.addSegment(2., [6.18865, 0.149566, -0.0576034, -0.034095,
                                 7.41404, -0.161551, -0.0585597, 0.0144959,
                                 0.842207, - 0.0984805, -0.1355, 0.000767251])
    spline_curve.addSegment(3., [6.24652, -0.0679259, -0.159888, 0.0609804,
                                 7.20843, -0.235182, -0.0150719, 0.0548643,
                                 0.608993, - 0.367179, -0.133198, 0.11326])
    spline_curve.addSegment(4., [6.07969, -0.204761, 0.0230529, -0.00538516,
                                 7.01304, -0.100733, 0.149521, -0.0375805,
                                 0.221876, - 0.293796, 0.206582, -0.0375974])
    spline_curve.addSegment(5., [5.89259, -0.174811, 0.00689745, 0.041456,
                                 7.02425, 0.0855677, 0.0367796, 0.0150364,
                                 0.0970648, 0.00657602, 0.0937898, 0.0214335])
    spline_curve.addSegment(6., [5.76614, -0.0366479, 0.131266, -0.0437549,
                                 7.16163, 0.204236, 0.0818889, -0.0272963,
                                 0.218864, 0.258456, 0.15809, -0.0526968])
    spline_curve.addSegment(7., [5.817, 0.0946183, 1.430510000000000E-006, -0.26253,
                                 7.42046, 0.286125, 0., -0.163778,
                                 0.582714, 0.146546, -1.713630000000000E-007, -0.316181])

    system.Commit(spline_curve)

    system.save(filename)

if __name__ == '__main__':
    print("Imported modules successfully")
    import cProfile
    cProfile.run('testrun()')
