#!python3.3
# -*- coding: utf-8 -*-
'''
.. module:: examples.benchmarks.144_000_example_2
   :platform: Agnostic, Windows
   :synopsis: Test for IGES type 144 form 0

.. Created on 01/08/2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES

.. figure:: 144-000-example-2.png
   :scale: 70 %
   :height: 507 px
   :width: 1191 px
   :alt: 142 type
   :align: center

   A more involved example of |BENCH_142|_ for |BENCH_144|_ on a 3D geometry.
   The geometry however isn't complex - just more involved.

+--------------+-----------------+
| Stage 2,     | Stage 1,        |
| |BENCH_142|  | Create Elements |
+==============+=================+
| |IGES_142|   | |IGES_106|      |
+--------------+-----------------+
|              | |IGES_110|      |
+--------------+-----------------+
|              | |IGES_120|      |
+--------------+-----------------+


This example draws a number of horizontally square slots
though a cone. In comparison to example 1, this is somewhat
more involved as tracing on a conical surface is tedious -it's not
particularly trivial though. The image on the left is an extension to
the task, having revolved the cutting profile - this illustrates
exactly why benchmarks need to be made (this is just too creative and
achieves nothing).

The code to make hole though a cone is:

.. literalinclude:: 144_000_example_2.py
    :pyobject: iges_144_000
    :linenos:
    :emphasize-lines: 27-29, 92-95, 99

'''

import os
import sys
import math

sys.path.append(os.path.abspath('../../../'))

import examples.benchmarks


def cyl_to_rect(cyl_system):
    #data is in format [[r], [theta], [z]]
    rect_system = [[], [], []]  # [[x], [y], [z]]

    for i in range(0, len(cyl_system[0])):
        rect_system[0].append(math.cos(math.radians(cyl_system[1][i])) * cyl_system[0][i])
        rect_system[1].append(math.sin(math.radians(cyl_system[1][i])) * cyl_system[0][i])
        rect_system[2].append(cyl_system[2][i])

    return rect_system


def iges_144_000():
    import pyiges.IGESGeomLib as IGES
    from pyiges.IGESCore import IGEStorage
    from pyiges.IGESGeomLib import IGESPoint

    filename = "144-000-example-2.igs"

    system = IGEStorage()
    examples.benchmarks.standard_iges_setup(system, filename)

    # Setup a cone like surface, the cone is boring but whatever!
    cone_surface_profile = IGES.IGESGeomPolyline(IGESPoint(-10, 0, 0),
                                                 IGESPoint(0, 0, 10))
    system.Commit(cone_surface_profile)

    # The centre of the revolve
    center_line = IGES.IGESGeomLine(IGESPoint(0, 0, 0),
                                    IGESPoint(0, 0, 10))
    system.Commit(center_line)

    # Make the surface from the profile, this is to be trimmed
    cone_surface = IGES.IGESRevolve(cone_surface_profile, center_line)
    system.Commit(cone_surface)

    #Setup the surface we are to put holes into, we're using the whole surface,
    #  as indicated by the 0 in the outer profile parameter
    trimmed_surface = IGES.IGESTrimmedParaSurface(cone_surface,
                                                  0)
    trimmed_surface.N1 = 0

    hole = []
    hole_copse = []

    # We're going to put a bunch of holes into the surface, because we don't
    # care about the index of the hole we can get away with specifying -8 to 8
    for holenum in range(-8, 8):
        hole.append(IGES.IGESGeomPolyline())
        hole_data = [[], [], []]

        # Top line following the cone profile
        for i in range(21 * holenum, 20 + 21 * holenum):
            hole_data[0].append(3)
            hole_data[1].append(i)
            hole_data[2].append(7)

        # Line down the cone profile
        hole_data[0].append(7)
        hole_data[1].append(hole_data[1][-1])
        hole_data[2].append(3)

        # Bottom line following the cone profile
        for i in range(20 + 21 * holenum, 21 * holenum, -1):
            hole_data[0].append(7)
            hole_data[1].append(i)
            hole_data[2].append(3)

        # Line back to start of the cone profile
        hole_data[0].append(hole_data[0][0])
        hole_data[1].append(hole_data[1][0])
        hole_data[2].append(hole_data[2][0])

        # Convert to rectangular coordinate system
        hole_rect_cs = cyl_to_rect(hole_data)

        # Push the points into the common format
        for i in range(0, len(hole_rect_cs[0])):
            hole[-1].AddPoint(IGESPoint(hole_rect_cs[0][i],
                                        hole_rect_cs[1][i],
                                        hole_rect_cs[2][i]))

        # Commit this hole
        system.Commit(hole[-1])

        # Lets make a really very crazy looking thing!
        # And revolve the cutting profile by a bit
        # Setup Revolve Line data
        random_line_data = cyl_to_rect([[-10, 10],
                                        [(20 * holenum) + 90, (20 * holenum) + 90],
                                        [10, 10]])

        # Make revolve line
        revolve_line = IGES.IGESGeomLine(IGESPoint(random_line_data[0][0], random_line_data[1][0], random_line_data[2][0]),
                                         IGESPoint(random_line_data[0][1], random_line_data[1][1], random_line_data[2][1]))

        # Commit revolve line
        system.Commit(revolve_line)

        # Make the revolve
        system.Commit(IGES.IGESRevolve(hole[-1], revolve_line, -1, 0))

        # Create the Curve on Parametric Surface
        hole_copse.append(IGES.IGESCurveOnParametricSurface(cone_surface,
                                                            hole[-1],
                                                            hole[-1],
                                                            2))
        system.Commit(hole_copse[-1])

        # Lets put that holes in!
        trimmed_surface.add_bounding_profile(hole_copse[-1])

    # commit that surface!
    system.Commit(trimmed_surface)

    system.save(filename)

    if not os.environ.get('READTHEDOCS', None):
        print(system)
        os.startfile(filename)

if __name__ == "__main__":
    iges_144_000()

