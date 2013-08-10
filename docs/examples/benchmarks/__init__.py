#!python3.3
# -*- coding: utf-8 -*-
"""
.. module:: examples.benchmarks
   :platform: Agnostic, Windows
   :synopsis: Full suite of benchmarks
   
   
Created on 10/08/2013

"""


def standard_iges_setup(system, filename):
    system.StartSection.Prolog = " "
    
    system.GlobalSection.IntegerBits = int(32)
    system.GlobalSection.SPMagnitude = int(38)
    system.GlobalSection.SPSignificance = int(6)
    system.GlobalSection.DPMagnitude = int(38)
    system.GlobalSection.DPSignificance = int(15)
    
    system.GlobalSection.MaxNumberLineWeightGrads = int(8)
    system.GlobalSection.WidthMaxLineWeightUnits = float(0.016)
    system.GlobalSection.MaxCoordValue = float(71)

    index_dot = filename.index('.')
    system.GlobalSection.ProductIdentificationFromSender = filename[:index_dot]
    system.GlobalSection.FileName = filename
    
    system.GlobalSection.ProductIdentificationForReceiver = \
      system.GlobalSection.ProductIdentificationFromSender
      
    system.GlobalSection.AuthorOrg = "Queensland Uni. of Tech."
    system.GlobalSection.NameOfAuthor = "Rodney Persky"
    