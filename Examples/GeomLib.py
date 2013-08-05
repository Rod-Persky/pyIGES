#!python3.3
# -*- coding: utf-8 -*-
"""
.. module:: Geometry.GeomLib
   :platform: Agnostic, Windows
   :synopsis: Main IGES Geometry Library

.. requires PyQt4, ctypes

.. Created on Wed Mar 20 21:11:53 2013
.. codeauthor::  Rod Persky <rodney.persky@gmail.com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://bitbucket.org/Rod-Persky/3d-turbomachinery-design-tool


.. todolist::
- See if we can output a plot into the documentation, this would be good
- See how the nurbs would actually be mapped to the circles etc, because
  we may have issues determining the knots between individual circles
- See how NURBS behaves as dt increases, and determine how weights would
  be allocated
- Integrate the object maker into a class definition, and auto assign an
  id to each circle, then we may be able to determine where the circle
  belongs within the system. Also the class represents an object, so then
  we can make some assumptions about how things work
- Actually the starting point can satisfy an infinite number of circles,
  we might instead define how the circle is a tangent to this point
  - Implemented angle to node from center
- Function currently draws a circle about the point specified, however we
  want it to be tangent to the current point, we will know exactly what
  to do when we get into the defining curves (bezier curve) that the
  circle is defined with respect to
- Check that no point is done twice
- It doesn't make sense to draw circles, because the hub and shroud
  has vertical sections, it would be more beneficial to figure out how
  to draw a nerbs line and go from there to generate the surface. I guess
  this could always be used to compare the nurbs surface to what it should
  be

"""

import numpy as np
from scipy.misc import comb


def mkCentLinePt(origin, theta, length) :
    """Make centered line points,
    A line that is centered on a node with a defined length and theta.

    Parameters
    -----------
    origin : array  Origin [x,y,z]
    theta  : float  Line heading in radians from the x-axis
    length : float  Length of the line to be drawn

    Returns
    -----------
    points : array Rectalinear CS [[x],[y]]

"""
    points = np.ones([2, 2], dtype='float64')
    xoffset = length * 0.5 * np.cos(theta)
    yoffset = length * 0.5 * np.sin(theta)

    points[0] = [origin[0] + xoffset, origin[0] - xoffset]
    points[1] = [origin[1] + yoffset, origin[1] - yoffset]

    return points


def mkCCTangent(circle1, circle2) :
    """Calculate Circle-Circle Tangent,
    With reference to method from wolfram mathworld [1]_

    Parameters
    -----------
    circle1 : array [x,y,z,r]
        The data that fully defines the circle, currently calculations
        are done on the x-y plane. z is ignored

    Returns
    --------
    tangent : array
        [[t1x,t2x,t3x,t4x], [t1y,t2y,t3y,t4y]]
        Allowing to directly draw the points, assumed to work from left to
        right so the data goes clockwise around the two circles
    points : array
        Automatically outputs when running this module by itself from python.
        Also shows up in the doctest below.

    Examples
    ---------

    >>> mkCCTangent([0,0,0,10],[10,10,0,10])
    (array([[ -7.07106781,   2.92893219,  17.07106781,   7.07106781],
           [  7.07106781,  17.07106781,   2.92893219,  -7.07106781]]), array([[  0.,   0.,  10.,   0.],
           [  0.,   0.,  10.,   0.]]))

    .. [1] Weisstein, Eric W. "Circle-Circle Tangents." From MathWorld--A
           Wolfram Web Resource.
           http://mathworld.wolfram.com/Circle-CircleTangents.html
    """

    x1, y1, r1 = circle1[0], circle1[1], circle1[3]
    x2, y2, r2 = circle2[0], circle2[1], circle2[3]

    if (x1, y1) == (x2, y2):
        raise RuntimeError("Circles with same centroid cannot have a tangent")

    hyp = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # hypotamoose length
    shorts = abs(r2 - r1)
    alpha = np.arccos(shorts / hyp)
    try:
        theta = np.arctan((y2 - y1) / (x2 - x1))
    except:
        theta = np.pi / 2  # cannot do x/0, but it happens because x2-x1 = 0

    tangent = []
    tangent.append([np.cos(theta + alpha) * r1 + x1, np.sin(theta + alpha) * r1 + y1])
    tangent.append([np.cos(theta + alpha) * r2 + x2, np.sin(theta + alpha) * r2 + y2])
    tangent.append([np.cos(theta - alpha) * r2 + x2, np.sin(theta - alpha) * r2 + y2])
    tangent.append([np.cos(theta - alpha) * r1 + x1, np.sin(theta - alpha) * r1 + y1])
    tangent = np.transpose(tangent)

    # if this is running just by itself, we're probably debugging...
    if __name__ == "__main__":
        points = []
        points.append([x1, y1])
        points.append([np.cos(theta + alpha) * shorts + x1, np.sin(theta + alpha) * shorts + y1])
        points.append([x2, y2])
        points.append([x1, y1])
        points = np.transpose(points)
        return tangent, points

    return tangent


# def mkCirclePts(origin, angle, radius, dt):
#     """Make circle points from a radius and starting vector
#     Also can essentially make any polygon inscribed into a circle
#
#     Parameters
#     -----------
#     origin : array Origin of the circle [x,y,z]
#     angle : int    Angle (degrees) from center of the circle to this node
#     radius : int   The radius of the circle
#     dt : int       The angle (degrees) between points
#
#     Returns
#     -----------
#     points : array Rectalinear CS [x,y,Z]
#
#     >>> print(mkCirclePts([123,456,789],0,10,120)[2]==[789, 797.66025404,789])
#     [ True False  True]
#
#     """
#
#     npoints = 360 // dt
#     output = pl.CylCS(0, origin)
#     output.AddPoint([[radius], [0], [angle]])
#     output.Duplicate(npoints, 0, 2 * np.pi)
#     return output.ConvToRectCS()

def three_point_circle(point, n=100):
    """Make a 3 point circle
    
    From origin, the function traces out n points in a clockwise
    direction.
    
    points = [[originx, point1x, point2x],[[originy, point1y, point2y]]
    """
    
    m = np.empty([2])
    a = np.empty([2])
    c = np.empty([2])
    
    for i in range(0,2):
        rise = point[1][i+1] - point[1][0]
        run = point[0][i+1] - point[0][0]
        c[i] = np.sqrt(np.power(rise, 2) + np.power(run, 2))
        a[i] = np.arctan(np.divide(rise,run))
        
        print("m ", i, " = ", rise, run)
        
    u = np.linspace(a[0], a[1], n)
   
    point_array = np.empty([2, n])
    
    point_array[0] = np.cos(u) * c[1] + point[0][0]
    point_array[1] = np.sin(u) * c[0] + point[1][0]

    print("u=", u)
    print("a=", a)
    
    return point_array

def bernstein_poly(n, i, u):
    return comb(n, i) * u ** (i) * (1 - u) ** (n - i)


def bezier_curve(P, nTimes=1000, dC=False):

    n = len(P[1])
    u = np.linspace(0.0, 1.0, nTimes)
    polynomial_array = np.empty([n, nTimes])

    for i in range(0, n):
        polynomial_array[i] = bernstein_poly(n - 1, i, u)

    return np.dot(P, polynomial_array)


if __name__ == '__main__':
    three_point_circle([[10, 10,  0],
                        [10,  0, 10]], 10)
