'''
.. module:: examples.iges414000
   :platform: Agnostic, Windows
   :synopsis: Test for IGES type 414 form 0
   
   
Created on 01/08/2013

@author: Rodney Persky

414 doesn't work (as in, this code generates the correct file, just it
doesn't actually render the extra persons)
'''

from pyiges.IGESCore import IGEStorage
import pyiges.IGESGeomLib as IGES
from pyiges.IGESGeomLib import IGESPoint
import os

def person_414():   
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
    
    line_1 = IGES.IGESGeomLine(IGESPoint(-0.13, 0,0),
                               IGESPoint(0, 0.25, 0))
    line_1.add_extended_data = False
    
    line_2 = IGES.IGESGeomLine(IGESPoint(0,0.25,0),
                               IGESPoint(0.13, 0, 0))
    line_2.add_extended_data = False
    
    line_3 = IGES.IGESGeomLine(IGESPoint(0, 0.25,0),
                               IGESPoint(0, 0.44, 0))
    line_3.add_extended_data = False
    
    line_4 = IGES.IGESGeomLine(IGESPoint(0, 0.38, 0),
                               IGESPoint(0.9, 0.28, 0))
    line_4.add_extended_data = False
    
    line_5 = IGES.IGESGeomLine(IGESPoint(0, 0.38, 0),
                               IGESPoint(-0.09, 0.28, 0))
    line_5.add_extended_data = False
    
    circle_1 = IGES.IGESGeomArc(0,
                                IGESPoint(0, 0.5),
                                IGESPoint(0.06, 0.05),
                                IGESPoint(0.06, 0.5))
    
    circle_1.add_extended_data = False

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
    
    system.save("414-000.igs")
    os.startfile("414-000.igs")
    
    
    print(system)
    
if __name__ == "__main__":
    person_414()