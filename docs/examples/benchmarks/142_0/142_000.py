#!python3.3
# -*- coding: utf-8 -*-
'''
.. module:: examples.benchmarks.142_000
   :platform: Agnostic, Windows
   :synopsis: Test for IGES type 142 form 0

.. Created on 01/08/2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES



.. figure:: ../144_0/144-000.png
   :scale: 70 %
   :height: 528 px
   :width: 1114 px
   :alt: 142 type
   :align: center

   142 type is a building block for the final 144 surface type, the 142
   step brings the geometry up to the second point - the trimmed surface.


.. literalinclude:: 142_000.py
    :pyobject: iges_142_000
    :linenos:
    :emphasize-lines: 43-47

The resulting IGES file should look like:

.. literalinclude:: 142-000.igs
    :language: py
    :linenos:
    :emphasize-lines: 12-13, 127

'''

import os
import sys
sys.path.append(os.path.abspath('../../../'))

import examples.benchmarks
#===============================================================================
#
#      114       1       0       1       0       0       0       000010001D      1
#      114       2       2      95       0                                D      2
#      100      96       0       1       0       0       0       001010501D      3
#      100       2       2       1       0                                D      4
#      112      97       0       1       0       0       0       000010001D      5
#      112       2       2      17       0                                D      6
#      142     114       0       1       0       0       0       000000001D      7
#      142       2       2       1       0                                D      8
#===============================================================================

# 114 = Parametric Spline Surface Entity        Page 98
# 100 = Circular Arc Entity                     Page 64
# 112 = Parametric Spline Curve Entity          Page 94
# 142 = Curve on a Parametric Surface Entity    Page 162


def iges_142_000():
    #import pyiges.IGESGeomLib as IGES
    from pyiges.IGESCore import IGEStorage
    #from pyiges.IGESGeomLib import IGESPoint
    filename = "142-000-benchmark.igs"

    system = IGEStorage()
    examples.benchmarks.standard_iges_setup(system, filename)

    # Exactly the same as 144 except for some values and the last surface generation step

    system.save(filename)

    if not os.environ.get('READTHEDOCS', None):
        print(system)
        #os.startfile("414-000-benchmark.igs")

if __name__ == "__main__":
    iges_142_000()
