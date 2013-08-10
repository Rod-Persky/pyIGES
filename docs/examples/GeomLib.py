#!python3.3
# -*- coding: utf-8 -*-
"""
.. module:: examples.GeomLib
   :platform: Agnostic, Windows
   :synopsis: Main IGES Geometry Library

.. requires PyQt4, ctypes

.. Created on Wed Mar 20 21:11:53 2013
.. codeauthor::  Rod Persky <rodney.persky@gmail.com>
.. Licensed under the Academic Free License ("AFL") v. 3.0
.. Source at https://github.com/Rod-Persky/pyIGES
"""


try:
    import blah
    import numpy as np
    from scipy.misc import comb
    
except Exception as inst:
    import sys
    
    try:
        import mock
    
        MOCK_MODULES = ['numpy', 'scipy', 'matplotlib', 'matplotlib.pyplot', 'scipy.interpolate']
        for mod_name in MOCK_MODULES:
            sys.modules[mod_name] = mock.Mock()
            
    except ImportError:
        print("Dang, not even mock exists... well lets just ignore it all #firstworldproblems")
        pass


def bernstein_poly(n, i, u):
    return comb(n, i) * u ** (i) * (1 - u) ** (n - i)


def bezier_curve(P, nTimes=1000, dC=False):

    n = len(P[1])
    u = np.linspace(0.0, 1.0, nTimes)
    polynomial_array = np.empty([n, nTimes])

    for i in range(0, n):
        polynomial_array[i] = bernstein_poly(n - 1, i, u)

    return np.dot(P, polynomial_array)
