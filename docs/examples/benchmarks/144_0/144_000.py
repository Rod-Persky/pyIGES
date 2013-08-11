#!python3.3
# -*- coding: utf-8 -*-
'''
.. module:: examples.benchmarks.144_000
   :platform: Agnostic, Windows
   :synopsis: Test for IGES type 144 form 0

.. Created on 01/08/2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES

.. figure:: 144-000.png
   :scale: 70 %
   :height: 528 px
   :width: 1114 px
   :alt: 144 type
   :align: center

   144 Type construction, See table below

+------------------+--------------+-----------------+
| Stage 3,         | Stage 2,     | Stage 1,        |
| Generate Surface | |BENCH_142|_ | Create Elements |
+==================+==============+=================+
| |IGES_144|       | |IGES_142|   | |IGES_112|      |
+------------------+--------------+-----------------+
|                  |              | |IGES_100|      |
+------------------+--------------+-----------------+
|                  |              | |IGES_114|      |
+------------------+--------------+-----------------+

.. ToDo:: Figure out how this works.

.. literalinclude:: 144_000.py
    :pyobject: iges_144_000
    :linenos:
    :emphasize-lines: 24-26

The resulting IGES file should look like:

.. literalinclude:: 144-000.igs
    :language: py
    :linenos:
    :emphasize-lines: 14-15, 128

'''

import os
import sys
sys.path.append(os.path.abspath('../../../'))

import examples.benchmarks

# 114 = Parametric Spline Surface Entity        Page 98
# 100 = Circular Arc Entity                     Page 64
# 112 = Parametric Spline Curve Entity          Page 94
# 142 = Curve on a Parametric Surface Entity    Page 162
# 144 = Trimmed (Parametric) Surface Entity     Page 166

#===============================================================================
# Pref,
# 0 = Unspecified
# 1 = S o B is preferred
# 2 = C is preferred
# 3 = C and S o B are equally preferred
#===============================================================================

def iges_144_000():
    import pyiges.IGESGeomLib as IGES
    from pyiges.IGESGeomLib import IGESPoint
    from pyiges.IGESCore import IGEStorage

    system = IGEStorage()
    examples.benchmarks.standard_iges_setup(system, "144-000-benchmark.igs")

    para_spline_surface = IGES.IGESTestSplineSurf()
    system.Commit(para_spline_surface)

    circle = IGES.IGESGeomCircle(IGESPoint(6, 7.25, 0), IGESPoint(6.25, 7.25))
    system.Commit(circle)

    para_spline_curve = IGES.IGESTestSplineCurve()
    system.Commit(para_spline_curve)

    curve_on_parametric_surface = IGES.IGESCurveOnParametricSurface(para_spline_surface,
                                                                    circle,
                                                                    para_spline_curve,
                                                                    2)
    system.Commit(curve_on_parametric_surface)

    trimmed_parametric_surface = IGES.IGESTrimmedParaSurface(para_spline_surface,
                                                             curve_on_parametric_surface)
    system.Commit(trimmed_parametric_surface)

    system.save("144-000-benchmark.igs")

    if not os.environ.get('READTHEDOCS', None):
        print(system)
        os.startfile("144-000-benchmark.igs")

if __name__ == "__main__":
    iges_144_000()
