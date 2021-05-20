import os
import xml.etree.ElementTree as et
from enum import Enum 
from xml.dom import minidom
from glob import glob
from pathlib import Path
import argparse

from src.ReportBuilder import ReportBuilder

class DivReferenceType(Enum):
    RelToOne = 0
    RelToTwo = 1

class SegRelTo(Enum):
    FromStart = 0,
    FromEnd = 1
class TrackSegmentType(Enum):
    AA = 0,
    AB = 1,
    BA = 2,
    BB = 3

class Segment:
    def __init__(self, SegName, Position = "0.0", RelativeTo="FromStart", SegmentType = "8F1I01.AA66.xxxx-1"):
        self.SegName = SegName
        self.Position = float(Position)
        self.SegmentType = TrackSegmentType.BB #Doing this as a placeholder
        if(RelativeTo == "FromStart"):
            self.RelativeTo = SegRelTo.FromStart
        else:
            self.RelativeTo = SegRelTo.FromEnd
        if self.SegName.find("::") > -1:
            self.SegName = self.SegName.lstrip('::')
        if self.SegName == "":
            print("Bad segname")
        self.setSegmentType(SegmentType)

    def __str__(self):
        return "{segName}:{type} {relTo} at {pos}".format(
            segName = self.SegName,
            type = self.SegmentType,
            relTo = self.RelativeTo,
            pos = str(self.Position)
        )

    def setSegmentType(self,SegmentType):
        if SegmentType.find("AA66") > -1:
            self.SegmentType = TrackSegmentType.AA
            if self.RelativeTo == SegRelTo.FromEnd:
                self.PosFromStart = str(0.66 - float(self.Position))
            else:
                self.PosFromStart = str(self.Position)
        elif SegmentType.find("AB2B") > -1:
            self.SegmentType = TrackSegmentType.AB
            if self.RelativeTo == SegRelTo.FromEnd:
                self.PosFromStart = str(0.450642056 - float(self.Position))
            else:
                self.PosFromStart = self.Position
        elif SegmentType.find("BA2B") > -1:
            self.SegmentType = TrackSegmentType.BA
            if self.RelativeTo == SegRelTo.FromEnd:
                self.PosFromStart = str(0.450642056 - float(self.Position))
            else:
                self.PosFromStart = str(self.Position)
    
    def segLength(self) -> float:
        if self.SegmentType == TrackSegmentType.AA:
            return 0.66
        elif self.SegmentType == TrackSegmentType.AB or self.SegmentType == TrackSegmentType.BA:
            return 0.450642056
                    
class Diverter:
    def __init__(self,DivType, SpurTrackSegment, BaseTrackSegment, DivTestPosition = 0.045):
        self.DivType = DivType
        self.SpurTrackSegment = SpurTrackSegment
        self.BaseTrackSegment = BaseTrackSegment
        self.DivTestPosition = DivTestPosition
        self._chooseRefSegment()

    def __str__(self):
        return "{segSpur} connected to {segBase} type {divType}".format(
            segSpur = self.SpurTrackSegment,
            segBase = self.BaseTrackSegment,
            divType = self.DivType
        )
    
    def __getRefSegment(self) -> Segment:
        if self.RefSegment == "spur":
            return self.SpurTrackSegment
        else:
            return self.BaseTrackSegment

    def BuildSector(self,XmlElement):
        newSector = et.SubElement(XmlElement, "Element")
        newSector.attrib["ID"] = self.SectorName
        newSector.attrib["Type"] = "sector"
        selector = et.SubElement(newSector, "Selector")
        selector.attrib["ID"] = "Type"
        selector.attrib["Value"] = "Composed"
        group = et.SubElement(selector, "Group")
        group.attrib["ID"] = "StartSegment"
        prop = et.SubElement(group, "Property")
        prop.attrib["ID"] = "SegmentRef"
        prop.attrib["Value"] = "::{segName}".format(segName = self.__getRefSegment().SegName)
        if self.__getRefSegment().RelativeTo == SegRelTo.FromEnd or \
                self.__getRefSegment().SegmentType == TrackSegmentType.BA:
            prop = et.SubElement(group, "Property")
            prop.attrib["ID"] = "PositionRelativeTo"
            prop.attrib["Value"] = "FromEnd"
        prop = et.SubElement(group, "Property")
        prop.attrib["ID"] = "Position"
        prop.attrib["Value"] = "0.0"
        #Determine the offsets
        group = et.SubElement(selector, "Group")
        group.attrib["ID"] = "IntermediateSegments"
        group = et.SubElement(selector, "Group")
        group.attrib["ID"] = "EndSegment"
        prop = et.SubElement(group, "Property")
        prop.attrib["ID"] = "SegmentRef"
        prop.attrib["Value"] = "::{segName}".format(segName = self.__getRefSegment().SegName)
        if self.__getRefSegment().RelativeTo == SegRelTo.FromEnd or \
                self.__getRefSegment().SegmentType == TrackSegmentType.BA:
            prop = et.SubElement(group, "Property")
            prop.attrib["ID"] = "PositionRelativeTo"
            prop.attrib["Value"] = "FromEnd"
        prop = et.SubElement(group, "Property")
        prop.attrib["ID"] = "Position"
        prop.attrib["Value"] = "0.1"
        return XmlElement

    def _chooseRefSegment(self):
        #If one of the segments on the divert is a AB or BA it becomes the reference sector
        if self.SpurTrackSegment.SegmentType == TrackSegmentType.AB or self.SpurTrackSegment.SegmentType == TrackSegmentType.BA:
            self.RefSegment = "spur"
        elif self.BaseTrackSegment.SegmentType == TrackSegmentType.AB or self.BaseTrackSegment.SegmentType == TrackSegmentType.BA:
            self.RefSegment = "base"
        else:
            self.RefSegment = "spur"
        
    def SetSectorName(self,divCount = 0) -> None:
        self.SectorName = "gDivSector_{idx}".format(idx = divCount)

    def SecRelativeLength(self,RelativeToSpur = True) -> float:
        if RelativeToSpur:
            if self.SpurTrackSegment.RelativeTo == SegRelTo.FromStart:
                return self.SpurTrackSegment.Position + 0.09
            else:
                return self.SpurTrackSegment.segLength() - self.SpurTrackSegment.Position - 0.09
        else:
            if self.BaseTrackSegment.RelativeTo == SegRelTo.FromStart:
                return self.BaseTrackSegment.Position + 0.09
            else:
                return self.BaseTrackSegment.segLength() - self.BaseTrackSegment.Position - 0.09

#Request which configuration to use
#Get the .hw file
#Get the .sector file
#Get the Maint_init.st file
class ASProject:
     
    def __init__(self,ProjectPath,Config = "") -> None:
        self.ProjectPath = ProjectPath
        self.Config = Config
   
    def _configPath(self) -> str:
        return self.ProjectPath + "\\Physical\\" + self.Config

    def _getInputFiles(self) -> None:
        try:
            AssemblyPath = [y for x in os.walk(self._configPath()) for y in glob(os.path.join(x[0], '*.assembly'))]
            self.AssemblyPath = Path(AssemblyPath[0])
        except:
            print("Assembly file not found!")
        try:
            SectorPath = [y for x in os.walk(self._configPath()) for y in glob(os.path.join(x[0], '*.sector'))]
            self.SectorPath = Path(SectorPath[0])
        except:
            print("Sector file not found!")
        try:
            hw = [y for x in os.walk(self._configPath()) for y in glob(os.path.join(x[0], '*.hw'))]
            self.HWPath = Path(hw[0])
        except:
            print("HW file not found!")

    def __parse_rel_to_one(self,xmlElement,xmlParent) -> Diverter:
        spurSegName = ''
        spurRelTo = 'FromStart'
        spurRelPos = 0.0
        baseSegName = ''
        baseRelTo = 'FromStart'
        baseRelPos = 0.0
    
        for seg in xmlElement.findall("./Group/[@ID='TrackSegmentPosition']/Property"):
            if seg.attrib['ID'] == "SegmentRef":
                spurSegName = seg.attrib['Value'].lstrip('::')
            elif seg.attrib['ID'] == "PositionRelativeTo":
                spurRelTo = seg.attrib['Value']
            elif seg.attrib['ID'] == "Position":
                spurRelPos = seg.attrib['Value']
            
        for seg in xmlElement.findall("./Group/[@ID='Base']/Property"):
            if seg.attrib['ID'] == "SegmentRef":
                baseSegName = seg.attrib['Value'].lstrip('::')
            elif seg.attrib['ID'] == "PositionRelativeTo":
                baseRelTo = seg.attrib['Value']
            elif seg.attrib['ID'] == "Position":
                baseRelPos = seg.attrib['Value']

        self.Segments[spurSegName].Position = spurRelPos
        #I'm sure there is a faster of way converting this string to an enum, but this is what we're going with
        if spurRelTo == "FromEnd": self.Segments[spurSegName].RelativeTo = SegRelTo.FromEnd
        else: self.Segments[spurSegName].RelativeTo = SegRelTo.FromStart
        self.Segments[baseSegName].Position = baseRelPos
        if baseRelTo == "FromEnd": self.Segments[baseSegName].RelativeTo = SegRelTo.FromEnd
        else: self.Segments[baseSegName].RelativeTo = SegRelTo.FromStart
        
        return Diverter(DivReferenceType.RelToOne, self.Segments[spurSegName], self.Segments[baseSegName])
        
    def __parse_rel_to_two(self,xmlElement,xmlParent):
        firstSegSpurName = ''
        firstSegBaseName = ''
        secondSegSpurName = ''
        secondSegBaseName = ''
        for seg in xmlElement.findall("./Group/[@ID='AlignmentToFirst']/Property"):
            if seg.attrib['ID'] == "SegmentRefNewFirst":
                firstSegSpurName = seg.attrib['Value'].lstrip('::')
            elif seg.attrib['ID'] == "SegmentRefBaseFirst":
                firstSegBaseName = seg.attrib['Value'].lstrip('::')
        for seg in xmlElement.findall("./Group/[@ID='AlignmentToSecond']/Property"):
            if seg.attrib['ID'] == "SegmentRefNewSecond":
                secondSegSpurName = seg.attrib['Value'].lstrip('::')
            elif seg.attrib['ID'] == "SegmentRefBaseSecond":
                secondSegBaseName = seg.attrib['Value'].lstrip('::')
        diverts = []
        diverts.append(Diverter(DivReferenceType.RelToTwo, self.Segments[firstSegSpurName], self.Segments[firstSegBaseName]))
        diverts.append(Diverter(DivReferenceType.RelToTwo, self.Segments[secondSegSpurName], self.Segments[secondSegBaseName]))
        return diverts
    
    def SearchSegmentType(self,segName) -> TrackSegmentType:
        for module in self._hwList.findall("{namespace}Module/[@Name='{segName}']"
                    .format(
                        namespace = "{http://br-automation.co.at/AS/Hardware}",
                        segName=segName
                        )):
                return module.attrib['Type']

    def buildSegmentList(self):
        self.Segments = dict()
        for module in self._hwList.findall("{namespace}Module/[@Type='8F1I01.AA66.xxxx-1']".format(namespace = "{http://br-automation.co.at/AS/Hardware}")) \
                 + self._hwList.findall("{namespace}Module/[@Type='8F1I01.AB2B.xxxx-1']".format(namespace = "{http://br-automation.co.at/AS/Hardware}")) \
                 + self._hwList.findall("{namespace}Module/[@Type='8F1I01.BA2B.xxxx-1']".format(namespace = "{http://br-automation.co.at/AS/Hardware}")):
            for par in module.findall("{namespace}Parameter/[@ID = 'SegmentReference']".format(namespace = "{http://br-automation.co.at/AS/Hardware}")):
                segName = par.attrib['Value'].lstrip('::')
                segType = module.attrib['Type']
                self.Segments[segName] = Segment(segName,SegmentType=segType)

    def parseProject(self):
        self._getInputFiles()
        
        self.asmTree = et.parse(self.AssemblyPath)
        rt = self.asmTree.getroot()

        self.Diverts = []

        self.hwTree = et.parse(self.HWPath)
        self._hwList = self.hwTree.getroot()        
        self.buildSegmentList()

        for group in rt.findall("./Element/Group/[@ID='Tracks']"):
            for track in group.findall('./Group'):
                for ref in track.findall("./Selector/[@ID='Position']"):
                    if ref.attrib['Value'] == 'Absolute':
                        pass#(ref,track)
                    elif ref.attrib['Value'] == 'RelativeToOne':
                        self.Diverts.append(self.__parse_rel_to_one(ref,track))
                    elif ref.attrib['Value'] == 'RelativeToTwo':
                        self.Diverts += self.__parse_rel_to_two(ref,track)

        et.register_namespace('', 'http://br-automation.co.at/AS/Hardware')
        
       
    def exportProject(self):
        sectors = et.parse(self.SectorPath)
        for elem in sectors.iter():
            if(elem.text):
                elem.text = elem.text.strip()
            if(elem.tail):
                elem.tail = elem.tail.strip()
        root = sectors.getroot()

        #Generate the Sectors
        for idx,div in enumerate(self.Diverts):
            div.SetSectorName(idx)
            root = div.BuildSector(root)
            #With a relative to two divert, it will depend if there is an AB/BA segment in the divert or if it is two AA segments
            #If there is an AB or BA segment, we will just use that segment + FromStart/FromEnd +/- 90 to create the sector
            #If it's an AA segment, we'll just make a guess 


        with open("./Test.sector","w") as file:
            xmlStr = minidom.parseString(et.tostring(root,encoding='utf8').decode('utf8')).toprettyxml(indent = "    ")
            file.write(xmlStr)
        
        self._writeInitFile()

        ReportBuilder.export(Diverts=self.Diverts)

    def _writeInitFile(self):
        with open("./TestInit.st","w") as file:
            file.write("//This file was automatically generated using the Diverter Diagnostic program. Verify that the segment names and assembly name match your project values correctly\n")
            file.write("PROGRAM _INIT\n")
            file.write("DivertTestOffsets.ShSourceSector := ADR({sectorName}); //This is where the starting shuttle is located, feel free to change if your start shuttle is located elsewhere".format(sectorName = self.Diverts[0].SectorName))
            for idx,div in enumerate(self.Diverts):
                file.write("\tDivertTestOffsets.Sectors[{idx}] := {sectorName};\t//{divString}\n".format(idx = idx, sectorName = div.SectorName,divString = str(div)))
            file.write("\n")
            for idx,div in enumerate(self.Diverts):
                file.write("\tDivertTestOffsets.SegmentName1[{idx}] := '{seg1Name}';\n".format(idx = idx, seg1Name = div.SpurTrackSegment.SegName))
                file.write("\tDivertTestOffsets.SegmentName2[{idx}] := '{seg2Name}';\n".format(idx = idx, seg2Name = div.BaseTrackSegment.SegName))
                file.write("\tDivertTestOffsetsPar.Positions[{idx}] := {divTestPosition};\n".format(idx = idx, divTestPosition = str(div.DivTestPosition)))
            file.write("\n")
            file.write("\tDivertTestOffsets.Parameters := ADR(DivertTestOffsetsPar);\n")    
            file.write("\tDivertTestOffsetsPar.Velocity := 1.0;\n")
            file.write("\tDivertTestOffsetsPar.Acceleration := 20.0;\n")
            file.write("\tDivertTestOffsetsPar.Deceleration := 20.0;\n")
            file.write("\tDivertTestOffsetsPar.SettleTime := T#5s;\n")
            file.write("END_PROGRAM\n")
    
