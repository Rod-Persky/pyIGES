from pyiges.IGESCore import IGEStorage
import pyiges.IGESGeomLib as IGES

filename = "122_0.igs"

"""
1H,,1H;,7H122-000,11H122-000.IGS,9H{unknown},9H{unknown},16,6,15,13,15, G      1
7H122-000,1.,1,4HINCH,8,0.016,15H20020525.195625,0.0001,20.4857,        G      2
21Hdennette@wiz-worx.com,23HLegacy PDD AP Committee,10,3,               G      3
13H920717.080000;                                                       G      4
     100       1       0       1       0       0       0       000010001D      1
     100       0       5       1       0                                D      2
     122       2       0       1       0       0       0       000000001D      3
     122       0       5       1       0                                D      4
100,0.,20.,11.,20.25,11.,19.75,11.;                                    1P      1
122,1,20.4857,11.2357,-0.9428;                                         3P      2
S      1G      4D      4P      2                                        T      1
"""

system = IGEStorage()
system.GlobalSection.ParameterDelimiterCharacter = ","
system.GlobalSection.RecordDelimiter = ";"
system.GlobalSection.ProductIdentificationFromSender = "122-000"
system.GlobalSection.FileName = "122-000.IGS"
system.GlobalSection.NativeSystemID = "122-000.IGS"
system.GlobalSection.PreprocessorVersion = "pyIGES"
system.GlobalSection.IntegerBits = 16
system.GlobalSection.SPMagnitude = 6
system.GlobalSection.SPSignificance = 15
system.GlobalSection.DPMagnitude = 13
system.GlobalSection.DPSignificance = 15
system.GlobalSection.ProductIdentificationForReceiver = "122-000"
system.GlobalSection.ModelSpaceScale = 1.0
system.GlobalSection.Units.setInches()
system.GlobalSection.MaxNumberLineWeightGrads = 8
system.GlobalSection.WidthMaxLineWeightUnits = 0.016
system.GlobalSection.MaxUserResolution = 0.0001
system.GlobalSection.MaxCoordValue = 20.4857
system.GlobalSection.NameOfAuthor = "github.com"
system.GlobalSection.AuthorOrg = "pyIGES"
system.GlobalSection.VersionFlag = 11
system.GlobalSection.DraftStandardFlag = 3
system.GlobalSection.AppProtocol = "pyIGES"

arc = IGES.IGESGeomArc(0, IGES.IGESPoint(20, 11),  IGES.IGESPoint(20.25, 11), IGES.IGESPoint(19.75, 11))
arc.Color.setYellow()
arc.StatusNumber.Hierachy.setGlobalDefer()
arc.StatusNumber.EntityUseFlag.setGeometry()
arc.StatusNumber.Subordinate.setPhysicallyDependent()
arc.StatusNumber.Visablilty.setVisible()
system.Commit(arc)

extr = IGES.IGESExtrude(arc, IGES.IGESPoint(20.4857, 11.2357, -0.9428))
arc.Color.setYellow()
system.Commit(extr)

system.save(filename = filename)
