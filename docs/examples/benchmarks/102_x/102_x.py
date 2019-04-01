from pyiges.IGESCore import IGEStorage
import pyiges.IGESGeomLib as IGES

filename = "102_x.igs"

"""
1H,,1H;,5HF102X,9HF102X.IGS,13H{unspecified},13H{unspecified},16,6,15,  G      1
13,15,5HF102X,3.,1,4HINCH,8,0.016,15H20060617.212531,0.0001,15.5,       G      2
22H Dennette@WiZ-WORX.com,15H www.IGES5x.org,11,3,13H920717.080000,     G      3
22HMIL-PRF-28000B Class 2;                                              G      4
     406       1                                                00020000D      1
     406       2               1      16                                D      2
     410       2                                                00020300D      3
     410       2               1                                        D      4
     404       3                                                00000300D      5
     404       2               1                                        D      6
     124       4       0       0       0       0       0       000000001D      7
     124       2       2       1       0                                D      8
     116       5       0       0       0       0       0       000010001D      9
     116       2       3       1       0                                D     10
     110       6       0       1       0       0       0       000010001D     11
     110       2       4       1       0                                D     12
     100       7       0       1       0       0       7       000010001D     13
     100       2       2       1       0                                D     14
     112       8       0       1       0       0       0       000010001D     15
     112       2       7       5       0                                D     16
     102      13       0       0       0       0       0       000000001D     17
     102       2       6       1       0                                D     18
406,2,6.,8.;                                                           1P      1
410,1,3.,0,0,0,0,0,0;                                                  3P      2
404,1,3,0.,0.,0,0,1,1;                                                 5P      3
124,-1.,0.,0.,3.5,0.,1.,0.,15.,0.,0.,-1.,0.;                           7P      4
116,3.5,15.,0.,;                                                       9P      5
110,3.5,15.,0.,3.5,15.5,0.;                                           11P      6
100,0.,0.,0.,0.,0.5,-0.5,0.;                                          13P      7
112,3,1,3,2,0.,1.,2.,4.,0.5625,0.,-0.0625,15.,-0.312501,              15P      8
1.430510000000000E-006,0.0624995,0.,0.,0.,0.,4.5,0.375,-0.1875,       15P      9
0.0625,14.75,-0.125,0.1875,-0.0625005,0.,0.,0.,0.,4.75,0.1875,        15P     10
0.,0.375,14.75,0.062499,-2.861020000000000E-006,-0.375003,0.,0.,      15P     11
0.,0.;                                                                15P     12
102,4,9,11,13,15;                                                     17P     13
"""

system = IGEStorage()
system.GlobalSection.ParameterDelimiterCharacter = ","
system.GlobalSection.RecordDelimiter = ";"
system.GlobalSection.ProductIdentificationFromSender = filename.split(".")[0]
system.GlobalSection.FileName = filename
system.GlobalSection.NativeSystemID = filename
system.GlobalSection.PreprocessorVersion = "pyIGES"
system.GlobalSection.IntegerBits = 16
system.GlobalSection.SPMagnitude = 6
system.GlobalSection.SPSignificance = 15
system.GlobalSection.DPMagnitude = 13
system.GlobalSection.DPSignificance = 15
system.GlobalSection.ProductIdentificationForReceiver = filename.split(".")[0]
system.GlobalSection.ModelSpaceScale = 3.0
system.GlobalSection.Units.setInches()
system.GlobalSection.MaxNumberLineWeightGrads = 8
system.GlobalSection.WidthMaxLineWeightUnits = 0.016
system.GlobalSection.MaxUserResolution = 0.0001
system.GlobalSection.MaxCoordValue = 15.5
system.GlobalSection.NameOfAuthor = "github.com"
system.GlobalSection.AuthorOrg = "pyIGES"
system.GlobalSection.VersionFlag = 11
system.GlobalSection.DraftStandardFlag = 3
system.GlobalSection.AppProtocol = "pyIGES"

prop = IGES.IGESPropertyEntity([2,6.,8.], formNumber=16)
prop.StatusNumber.Subordinate.setLogicallyDependent()
system.Commit(prop)

view = IGES.IGESViewEntity([1,3.,0,0,0,0,0,0])
view.StatusNumber.EntityUseFlag.setOther()
view.StatusNumber.Subordinate.setLogicallyDependent()
system.Commit(view)

drawing = IGES.IGESDrawingEntity([1,3,0.,0.,0,0,1,1], formNumber=1)
drawing.StatusNumber.EntityUseFlag.setOther()
system.Commit(drawing)

trans = IGES.IGESGeomTransform([-1.,0.,0.,
                            3.5,0.,1.,
                            0.,15.,0.,
                            0.,-1.,0.], formNumber=1)
trans.StatusNumber.Hierachy.setGlobalDefer()
trans.LineWeightNum = 2
trans.Color.setCyan()
system.Commit(trans)

point = IGES.IGESGeomPoint(IGES.IGESPoint(3.5, 15.0, 0.0))
point.LineFontPattern.setNone()
point.LineWeightNum = 2
point.Color.setGreen()
point.StatusNumber.Hierachy.setGlobalDefer()
point.StatusNumber.EntityUseFlag.setGeometry()
point.StatusNumber.Subordinate.setPhysicallyDependent()
point.StatusNumber.Visablilty.setVisible()
system.Commit(point)

line = IGES.IGESGeomLine(IGES.IGESPoint(3.5, 15.0, 0.0), IGES.IGESPoint(3.5, 15.5, 0.0))
line.LineFontPattern.setSolid()
line.LineWeightNum = 2
line.Color.setBlue()
line.StatusNumber.Hierachy.setGlobalDefer()
line.StatusNumber.EntityUseFlag.setGeometry()
line.StatusNumber.Subordinate.setPhysicallyDependent()
line.StatusNumber.Visablilty.setVisible()
system.Commit(line)

arc = IGES.IGESGeomArc(0.0, IGES.IGESPoint(0.0, 0.0, 0.0),  IGES.IGESPoint(0.0, 0.5, 0.0), IGES.IGESPoint(-0.5, 0.0, 0.0))
arc.TransfrmMat = trans.DirectoryDataPointer.data
arc.LineFontPattern.setSolid()
arc.LineWeightNum = 2
arc.Color.setRed()
arc.StatusNumber.Hierachy.setGlobalDefer()
arc.StatusNumber.EntityUseFlag.setGeometry()
arc.StatusNumber.Subordinate.setPhysicallyDependent()
arc.StatusNumber.Visablilty.setVisible()
system.Commit(arc)

scurve = IGES.IGESSplineCurve(3, 1, 3)
scurve.addSegment(0.0, [4.,0.5625,0.,-0.0625,15.,-0.312501,1.430510000000000E-006,0.0624995,0.,0.,0.,0.])
scurve.addSegment(1.0, [4.5,0.375,-0.1875,0.0625,14.75,-0.125,0.1875,-0.0625005,0., 0., 0., 0.])
scurve.addSegment(2.0, [4.75, 0.1875, 0., 0.375, 14.75, 0.062499, -2.861020000000000E-006, -0.375003, 0., 0., 0., 0.])
scurve.LineFontPattern.setSolid()
scurve.LineWeightNum = 2
scurve.Color.setCyan()
scurve.StatusNumber.Hierachy.setGlobalDefer()
scurve.StatusNumber.EntityUseFlag.setGeometry()
scurve.StatusNumber.Subordinate.setPhysicallyDependent()
scurve.StatusNumber.Visablilty.setVisible()
system.Commit(scurve)

compCurve = IGES.IGESGeomCompositeCurve(point, line, arc, scurve)
compCurve.LineWeightNum = 2
compCurve.Color.setMagenta()
compCurve.StatusNumber.Hierachy.setGlobalDefer()
system.Commit(compCurve)

system.save(filename = filename)
