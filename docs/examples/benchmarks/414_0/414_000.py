#!python3.3
# -*- coding: utf-8 -*-
#!python3.3
# -*- coding: utf-8 -*-
'''
.. module:: examples.benchmarks.414_000
   :platform: Agnostic, Windows
   :synopsis: Test for IGES type 414 form 0

.. Created on 01/08/2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES


414 is a key 3D modelling tool, it creates a circular pattern. However, in
all tested programs 414 is no longer supported - although only a small number
of packages were tested, there may be some out there that do support this
feature.

An example of the 414 pattern is shown below, however this is simplistic -
it should be possible to do circular patterns around any axis and for
an arbitrarily complex group.


.. figure:: 414-000.png
   :scale: 70 %
   :height: 347 px
   :width: 300 px
   :alt: 414 type illustrated by the circular pattern of people
   :align: center

   414 type shown by the circular pattern of people

In the example code below it's seen that the setup is standard up to the
grouping of objects on line 36 /41 the 414 circular array is then setup
on lines 43 to 47. Note that the documentation for the class can be found
at :py:class:`pyiges.IGESGeomLib.IGESCircularArray`

.. literalinclude:: 414_000.py
    :pyobject: iges_414_000
    :linenos:
    :emphasize-lines: 43-47

The resulting IGES file should look like

.. literalinclude:: 414-000.igs
    :language: py
    :linenos:
    :emphasize-lines: 20-21, 29

'''

import os
import sys
sys.path.append(os.path.abspath('../../../'))

import examples.benchmarks


def iges_414_000():
    import pyiges.IGESGeomLib as IGES
    from pyiges.IGESCore import IGEStorage
    from pyiges.IGESGeomLib import IGESPoint

    system = IGEStorage()
    examples.benchmarks.standard_iges_setup(system, "414-000-benchmark.igs")

    line_1 = IGES.IGESGeomLine(IGESPoint(-0.13, 0, 0),
                               IGESPoint(0, 0.25, 0))

    line_2 = IGES.IGESGeomLine(IGESPoint(0, 0.25, 0),
                               IGESPoint(0.13, 0, 0))

    line_3 = IGES.IGESGeomLine(IGESPoint(0, 0.25, 0),
                               IGESPoint(0, 0.44, 0))

    line_4 = IGES.IGESGeomLine(IGESPoint(0, 0.38, 0),
                               IGESPoint(0.09, 0.28, 0))

    line_5 = IGES.IGESGeomLine(IGESPoint(0, 0.38, 0),
                               IGESPoint(-0.09, 0.28, 0))

    circle_1 = IGES.IGESGeomArc(0,
                                IGESPoint(0, 0.5),
                                IGESPoint(0.06, 0.5),
                                IGESPoint(0.06, 0.5))

    system.Commit(line_1)
    system.Commit(line_2)
    system.Commit(line_3)
    system.Commit(line_4)
    system.Commit(line_5)
    system.Commit(circle_1)

    person_group = IGES.IGESGroup("PERSON", line_1,
                                  line_2, line_3,
                                  line_4, line_5,
                                  circle_1)

    system.Commit(person_group)

    person_array = IGES.IGESCircularArray(person_group,
                                          3,
                                          IGESPoint(5.5, 1.5, 0),
                                          0.5,
                                          0.52, 2.09)

    system.Commit(person_array)

    system.save("414-000-benchmark.igs")

    if not os.environ.get('READTHEDOCS', None):
        print(system)
        os.startfile("414-000-benchmark.igs")

if __name__ == "__main__":
    iges_414_000()
