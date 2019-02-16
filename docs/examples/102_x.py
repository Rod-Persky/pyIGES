from pyiges.IGESCore import IGEStorage
from pyiges.IGESGeomLib import IGESPoint, IGESVector, IGESGeomPoint, IGESGeomLine, IGESGeomArc, IGESSplineCurve, IGESGeomCompositeCurve, IGESGeomTransform, IGESDrawingEntity, IGESViewEntity, IGESPropertyEntity
import pyiges.IGESGeomLib as IGES

filename = "f102x.igs"

system = IGEStorage()
system.GlobalSection.ParameterDelimiterCharacter = ","
system.GlobalSection.RecordDelimiter = ";"
system.GlobalSection.ProductIdentificationFromSender = "F102X"
system.GlobalSection.FileName = "102X.IGS"
system.GlobalSection.NativeSystemID = "102X.IGS"
system.GlobalSection.PreprocessorVersion = "pyIGES"
system.GlobalSection.IntegerBits = 16
system.GlobalSection.SPMagnitude = 6
system.GlobalSection.SPSignificance = 15
system.GlobalSection.DPMagnitude = 13
system.GlobalSection.DPSignificance = 15
system.GlobalSection.ProductIdentificationForReceiver = "F102X"
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

prop = IGESPropertyEntity([2,6.,8.], formNumber=16)
prop.StatusNumber.Subordinate.setLogicallyDependent()
system.Commit(prop)

view = IGESViewEntity([1,3.,0,0,0,0,0,0])
view.StatusNumber.EntityUseFlag.setOther()
view.StatusNumber.Subordinate.setLogicallyDependent()
system.Commit(view)

drawing = IGESDrawingEntity([1,3,0.,0.,0,0,1,1], formNumber=1)
drawing.StatusNumber.EntityUseFlag.setOther()
system.Commit(drawing)

trans = IGESGeomTransform([-1.,0.,0.,
                            3.5,0.,1.,
                            0.,15.,0.,
                            0.,-1.,0.], formNumber=1)
trans.StatusNumber.Hierachy.setGlobalDefer()
trans.LineWeightNum = 2
trans.Color.setCyan()
system.Commit(trans)

point = IGESGeomPoint(IGESPoint(3.5, 15.0, 0.0))
point.LineFontPattern.setNone()
point.LineWeightNum = 2
point.Color.setGreen()
point.StatusNumber.Hierachy.setGlobalDefer()
point.StatusNumber.EntityUseFlag.setGeometry()
point.StatusNumber.Subordinate.setPhysicallyDependent()
point.StatusNumber.Visablilty.setVisible()
system.Commit(point)

line = IGESGeomLine(IGESPoint(3.5, 15.0, 0.0), IGESPoint(3.5, 15.5, 0.0))
line.LineFontPattern.setSolid()
line.LineWeightNum = 2
line.Color.setBlue()
line.StatusNumber.Hierachy.setGlobalDefer()
line.StatusNumber.EntityUseFlag.setGeometry()
line.StatusNumber.Subordinate.setPhysicallyDependent()
line.StatusNumber.Visablilty.setVisible()
system.Commit(line)

arc = IGESGeomArc(0.0, IGESPoint(0.0, 0.0, 0.0),  IGESPoint(0.0, 0.5, 0.0), IGESPoint(-0.5, 0.0, 0.0))
arc.TransfrmMat = trans.DirectoryDataPointer.data
arc.LineFontPattern.setSolid()
arc.LineWeightNum = 2
arc.Color.setRed()
arc.StatusNumber.Hierachy.setGlobalDefer()
arc.StatusNumber.EntityUseFlag.setGeometry()
arc.StatusNumber.Subordinate.setPhysicallyDependent()
arc.StatusNumber.Visablilty.setVisible()
system.Commit(arc)

scurve = IGESSplineCurve(3, 1, 3)
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

compCurve = IGESGeomCompositeCurve(point, line, arc, scurve)
compCurve.LineWeightNum = 2
compCurve.Color.setMagenta()
compCurve.StatusNumber.Hierachy.setGlobalDefer()
system.Commit(compCurve)

system.save(filename = filename)
