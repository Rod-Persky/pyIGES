#!python3.3
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
from pyiges.IGESGeomLib import IGESPoint
import pyiges.IGESGeomLib as IGES
from examples.GeomLib import bezier_curve


def testrun(filename = "IGESFile.igs"):
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

    line = IGES.IGESGeomLine(IGESPoint(-2, -5, 0), IGESPoint(22, -5, 0))
    system.Commit(line)

    #system.Commit(IGES.IGESRevolve(polyln, line))

    #system.Commit(IGES.IGESExtrude(polyln.DirectoryDataPointer.data, IGESPoint(0,0,10)))
    print(system)

    system.save(filename)

    if not environ.get('READTHEDOCS', None) == 'True':
        startfile(filename)


if __name__ == '__main__':
    print("Imported modules successfully")
    import cProfile
    cProfile.run('testrun()')
