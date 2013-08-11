#!python3.3
# -*- coding: utf-8 -*-
'''
.. module:: examples.benchmarks.144_000_example_1
   :platform: Agnostic, Windows
   :synopsis: Test for IGES type 144 form 0

.. Created on 01/08/2013
.. codeauthor::  Rod Persky <rodney.persky {removethis} AT gmail _DOT_ com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES

.. figure:: 144-000-example-1.png
   :scale: 70 %
   :height: 500 px
   :width: 766 px
   :alt: 142 type
   :align: center

   More straight forward example of |BENCH_142|_ for |BENCH_144|_.

+--------------+-----------------+
| Stage 2,     | Stage 1,        |
| |BENCH_142|  | Create Elements |
+==============+=================+
| |IGES_142|   | |IGES_100|      |
+--------------+-----------------+
|              | |IGES_108|      |
+--------------+-----------------+
|              | |IGES_122|      |
+--------------+-----------------+

The 144 combines geometry together. In the 144 benchmark the wave surface is combined with the
parametric spline curve and circle to generate a profile that is otherwise may be too difficult to
create. The use of this type of geometry would be an `intersect`, where there is two geometric
items that are basic that need to be combined in some way - e.g a tube through a plate, the
142 type could remove the plate surface where it physically joins to the tube. Indeed, this
example shows exactly that.

Some creativity is advised, it may not be straight forward to make a tube then try and remove
the profile from a plate - however it may be simple to make a circle on the plate and extrude
the surface from that.

The code to make a tube punch though a plate is:

.. literalinclude:: 144_000_example_1.py
    :pyobject: iges_144_000
    :linenos:
    :emphasize-lines: 34-37

'''

import os
import sys
sys.path.append(os.path.abspath('../../../'))

import examples.benchmarks


def iges_144_000():
    import pyiges.IGESGeomLib as IGES
    from pyiges.IGESCore import IGEStorage
    from pyiges.IGESGeomLib import IGESPoint

    filename = "144-000-example-1.igs"

    system = IGEStorage()
    examples.benchmarks.standard_iges_setup(system, filename)

    # Circular flat surface profile
    circular_flat_surface_profile = IGES.IGESGeomCircle(IGESPoint(0, 0, 0),
                                                        IGESPoint(10, 10, 0))
    system.Commit(circular_flat_surface_profile)

    # Make the surface from out outer profile, this is to be trimmed
    circular_flat_surface = IGES.IGESGeomPlane(circular_flat_surface_profile)
    system.Commit(circular_flat_surface)

    # We're going to put a bunch of holes into the surface
    hole = []          # Hole profiles
    hole_copse = []    # Curve on Parametric Surface entries (required!)

    for i in range(0, 6):
        hole.append(IGES.IGESGeomCircle(IGESPoint(-5 + i * 3, 0, 0),
                                             IGESPoint(-5 + i * 3, 1, 0)))
        system.Commit(hole[-1])

        # Make those tubes, given we are not using them as a reference,
        # Lets directly add them to the system.
        system.Commit(IGES.IGESExtrude(hole[-1], IGESPoint(0, 0, i + 1)))
        system.Commit(IGES.IGESExtrude(hole[-1], IGESPoint(0, 0, -i - 1)))

        hole_copse.append(IGES.IGESCurveOnParametricSurface(circular_flat_surface,
                                                                 hole[-1],
                                                                 hole[-1],
                                                                 1))
        system.Commit(hole_copse[-1])

    # Setup the surface we are to put holes into, we're using the whole surface,
    #   as indicated by the 0 in the outer profile parameter
    trimmed_surface = IGES.IGESTrimmedParaSurface(circular_flat_surface,
                                                          0)
    trimmed_surface.N1 = 0

    # Lets put those holes in!
    for _hole in hole_copse:
        trimmed_surface.add_bounding_profile(_hole)

    system.Commit(trimmed_surface)

    system.save(filename)

    if not os.environ.get('READTHEDOCS', None):
        print(system)
        os.startfile(filename)

if __name__ == "__main__":
    iges_144_000()
