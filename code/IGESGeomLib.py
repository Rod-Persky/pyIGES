# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:57:00 2013
@author: Rod Persky
Licensed under the Academic Free License ("AFL") v. 3.0
"""

from IGESDirectoryEntry import IGESDirectoryEntry
from IGESParameterEntry import IGESParameterEntry
import numpy as np

#116
class IGESPoint:
    def __init__(self,x,y,z=0):
        self.x = x
        self.y = y
        self.z = z
#    def __str__(self):
#        return "X={:}, Y={:}, Z={:}".format(self.x, self.y, self.z)

class IGESGeomLine(IGESDirectoryEntry, IGESParameterEntry): #Wrapper of iges geometry
    def __init__(self, startpoint, endpoint):
        IGESDirectoryEntry.__init__(self)
        IGESParameterEntry.__init__(self)
        
        self.LineFontPattern.setDashed()
        self.Color.setBlue()
        self.StatusNumber.Hierachy.setGlobalDifer()
        self.LineWeightNum = 1
        self.ParameterLC = 1
        
        self.EntityType.setLine()
        
        self.AddParameters([startpoint.x, startpoint.y, startpoint.z,
                            endpoint.x, endpoint.y, endpoint.z])
                            
class IGESCentLinePt(IGESGeomLine):
    def __init__(self,node,theta,length):

        xoffset = length * 0.5 * np.cos(theta)
        yoffset = length * 0.5 * np.sin(theta)

        startpoint = IGESPoint(node.x+xoffset, node.y+yoffset)
        endpoint   = IGESPoint(node.x-xoffset, node.y-yoffset)
        
        startpoint.x = np.around(startpoint.x,7)
        startpoint.y = np.around(startpoint.y,7)
        endpoint.x = np.around(endpoint.x,7)
        endpoint.y = np.around(endpoint.y,7)        
               
        
        IGESGeomLine.__init__(self, startpoint, endpoint)
    
class IGESMultilineTest(IGESDirectoryEntry, IGESParameterEntry):
        def __init__(self):
            IGESDirectoryEntry.__init__(self)
            IGESParameterEntry.__init__(self)
            self.LineFontPattern.setSolid()
            self.LineWeightNum = 1
            self.ParameterLC = 1
            
            self.EntityType.setCircularArc()
            self.AddParameters([np.pi,np.pi,np.pi,np.pi,np.pi,np.pi,np.pi,
                                np.pi,np.pi,np.pi,np.pi,np.pi,np.pi,np.pi,
                                np.pi,np.pi,np.pi,np.pi,np.pi,np.pi,np.pi])

class IGESGeomArc(IGESDirectoryEntry, IGESParameterEntry): #Wrapper of iges geometry
    def __init__(self,z, node, startpoint, endpoint):
        IGESDirectoryEntry.__init__(self)
        IGESParameterEntry.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1
        
        self.EntityType.setCircularArc()
        
        self.AddParameters([z, node.x, node.y, startpoint.x, startpoint.y, endpoint.x, endpoint.y])
        
    

class IGESGeomCircle(IGESGeomArc): #Wrapper of iges geometry
    def __init__(self,node,radius):
        z = node.z
        point = node
        point.x = point.x + radius
        
        IGESGeomArc.__init__(self, z, node, point, point)

class IGESGeomPoint(IGESDirectoryEntry, IGESParameterEntry):
    def __init__(self, node):
        IGESDirectoryEntry.__init__(self)
        IGESParameterEntry.__init__(self)
        self.LineFontPattern.setSolid()
        self.LineWeightNum = 1
        self.ParameterLC = 1
        
        self.EntityType.setPoint()
        
        self.AddParameters([node.x, node.y, node.z, 0])
    
