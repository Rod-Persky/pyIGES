#!python3.3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 18:33:27 2013
@author: Rod Persky
@license: Licensed under the Academic Free License ("AFL") v. 3.0
"""

import os
import sys
import numpy as np
from scipy.misc import comb

sys.path.append('../')
from IGES.IGESCore import IGEStorage
from IGES.IGESGeomLib import IGESPoint
import IGES.IGESGeomLib as IGES


def bernstein_poly(n, i, u):
    return comb(n, i) * u ** (i) * (1 - u) ** (n - i)


def bezier_curve(P, nTimes=1000, dC=False):
    n = len(P[1])
    u = np.linspace(0.0, 1.0, nTimes)
    polynomial_array = np.empty([n, nTimes])

    for i in range(0, n):
        polynomial_array[i] = bernstein_poly(n - 1, i, u)

    return np.dot(P, polynomial_array)


def testrun():
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
         [np.divide(1, 3), np.divide(np.pi, 6)],
         [np.divide(2, 3), 1],
         [1, 1],
         [1 + np.divide(1, 3), 1],
         [1 + np.divide(2, 3), np.divide(np.pi, 6)],
         [2, 0],
         [2 + np.divide(1, 3), 0 - np.divide(np.pi, 6)],
         [2 + np.divide(2, 3), 0 - 1],
         [3, 0 - 1],
         [3 + np.divide(1, 3), 0 - 1],
         [3 + np.divide(2, 3), 0 - np.divide(np.pi, 6)],
         [4, 0]]

    for i in range(0, 1):
        P.extend

    P = np.transpose(P)
    bezi = bezier_curve(P, nTimes=50)

    polyln = IGES.IGESGeomPolyline()

    for n in range(0, 70):
        for i in range(0, len(bezi[0])):
            polyln.AddPoint(IGESPoint(bezi[0][i], bezi[1][i]))
        bezi[0] = bezi[0] + 4

    system.Commit(polyln)
    system.save()
    os.startfile("IGESFile.igs")


if __name__ == '__main__':
    print("Imported modules successfully")
    import cProfile
    cProfile.run('testrun()')
