import os
import xml.etree.ElementTree as et
from enum import Enum 
from xml.dom import minidom
from glob import glob
from pathlib import Path

class ReportBuilder:
    @staticmethod
    def export(Diverts,Path = "./Tmp.tmp"):
        root = et.Element("Configuration")
        baseElement = et.SubElement(root,"Element",attrib={"ID":"gOffsetsReport","Type":"mpreportcore"})
        report = et.SubElement(baseElement,"Group",attrib={"ID":"MpReport"})
        ReportBuilder.__createSettings(report)
        ReportBuilder.__createPageLayouts(report)
        ReportBuilder.__createStyles(report)
        ReportBuilder.__createTables(report,Diverts)
        ReportBuilder.__createCharts(report,Diverts)
        ReportBuilder.__createContents(report,Diverts,"gMcAssembly01")
        ReportBuilder.__createReports(report,Diverts)

        with open("./DivertReport.mpreportcore","w") as file:
            xmlStr = minidom.parseString(et.tostring(root,encoding='utf8').decode('utf8')).toprettyxml(indent = "  ")
            file.write(xmlStr)
    

    @staticmethod
    def __createSettings(parent):
        settings = et.SubElement(parent,"Group",attrib={"ID":"Settings"})
        prop = et.SubElement(settings,"Property",attrib={
            "ID":"ResourceDeviceName",
            "Value":""
        })
        group = et.SubElement(settings,"Group",attrib={"ID":"LanguageDependent"})
        item = et.SubElement(group,"Group",attrib={"ID":"[0]"})
        prop = et.SubElement(item,"Property",attrib={
            "ID":"Language",
            "Value":"en"
        })
        prop = et.SubElement(item,"Property",attrib={
            "ID":"Font",
            "Value":"1"
        })

    @staticmethod
    def __createPageLayouts(parent):
        layouts = et.SubElement(parent,"Group",attrib={"ID":"PageLayouts"})
        group = et.SubElement(layouts,"Group",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(group,"Property",attrib={
            "ID":"Name",
            "Value":"Default"
        })
        prop = et.SubElement(group,"Property",attrib={
            "ID":"PageFormat",
            "Value":"1"
        })
        
    @staticmethod
    def __createStyles(parent) -> None:
        styles = et.SubElement(parent,"Group",attrib={"ID":"Styles"})
        item = et.SubElement(styles,"Group",attrib={
            "ID":"Text"
        })
        group = et.SubElement(item,"Group",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(group,"Property",attrib={
            "ID":"Name",
            "Value":"Default"
        })
        group1 = et.SubElement(item,"Group",attrib={
            "ID":"[1]"
        })
        prop = et.SubElement(group1,"Property",attrib={
            "ID":"Name",
            "Value":"Title"
        })
        prop = et.SubElement(group1,"Property",attrib={
            "ID":"Style",
            "Value":"1"
        })
        prop = et.SubElement(group1,"Property",attrib={
            "ID":"Size",
            "Value":"14"
        })
        group2 = et.SubElement(item,"Group",attrib={
            "ID":"[2]"
        })
        prop = et.SubElement(group2,"Property",attrib={
            "ID":"Name",
            "Value":"Header"
        })
        prop = et.SubElement(group2,"Property",attrib={
            "ID":"Size",
            "Value":"12"
        })
        group3 = et.SubElement(item,"Group",attrib={
            "ID":"[3]"
        })
        prop = et.SubElement(group3,"Property",attrib={
            "ID":"Name",
            "Value":"Section"
        })
        prop = et.SubElement(group3,"Property",attrib={
            "ID":"Style",
            "Value":"2"
        })
        prop = et.SubElement(group3,"Property",attrib={
            "ID":"Size",
            "Value":"12"
        })
        #Table Style
        item1 = et.SubElement(styles,"Group",attrib={
            "ID":"Table"
        })
        group = et.SubElement(item1,"Group",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(group,"Property",attrib={
            "ID":"Name",
            "Value":"Default"
        })
        #Line Style
        item2 = et.SubElement(styles,"Group",attrib={
            "ID":"Line"
        })
        group = et.SubElement(item2,"Group",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(group,"Property",attrib={
            "ID":"Name",
            "Value":"Default"
        })
        #Charts style
        item3 = et.SubElement(styles,"Group",attrib={
            "ID":"Chart"
        })
        chart = et.SubElement(item3,"Group",attrib={
            "ID":"PieChart"
        })
        group = et.SubElement(chart,"Group",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(group,"Property",attrib={
            "ID":"Name",
            "Value":"Default"
        })
        chart = et.SubElement(item3,"Group",attrib={
            "ID":"LineChart"
        })
        group = et.SubElement(chart,"Group",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(group,"Property",attrib={
            "ID":"Name",
            "Value":"Default"
        })
        chart = et.SubElement(item3,"Group",attrib={
            "ID":"BarChart"
        })
        group = et.SubElement(chart,"Group",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(group,"Property",attrib={
            "ID":"Name",
            "Value":"Default"
        })
    
    @staticmethod
    def __createTables(parent,Diverts) -> None:
        groupTables = et.SubElement(parent,"Group",attrib={
            "ID":"Tables"
        })
        for idx,div in enumerate(Diverts):
            selectorTable = et.SubElement(groupTables,"Selector",attrib={
                "ID":"[{idx}]".format(idx = idx)
            })
            prop = et.SubElement(selectorTable,"Property", attrib={
                "ID":"Name",
                "Value":"Divert{idx}".format(idx = idx + 1)
            })
            prop = et.SubElement(selectorTable,"Property", attrib={
                "ID":"TableStyle",
                "Value":"Default"
            })
            prop = et.SubElement(selectorTable,"Property", attrib={
                "ID":"TextStyle",
                "Value":"Default"
            })
            row1Group = et.SubElement(selectorTable,"Group",attrib={
                "ID":"[0]"
            })
            selectorCol0 = et.SubElement(row1Group,"Selector",attrib={
                "ID":"[0]",
                "Value":"TextId"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Source",
                "Value":""
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Width",
                "Value":"40"
            })
            selectorCol1 = et.SubElement(row1Group,"Selector",attrib={
                "ID":"[1]",
                "Value":"TextId"
            })
            prop = et.SubElement(selectorCol1,"Property", attrib={
                "ID":"Source",
                "Value":"Segment 1"
            })
            selectorCol2 = et.SubElement(row1Group,"Selector",attrib={
                "ID":"[2]",
                "Value":"TextId"
            })
            prop = et.SubElement(selectorCol2,"Property", attrib={
                "ID":"Source",
                "Value":"Segment 2"
            })
            row2Group = et.SubElement(selectorTable,"Group",attrib={
                "ID":"[1]"
            })
            selectorCol0 = et.SubElement(row2Group,"Selector",attrib={
                "ID":"[0]",
                "Value":"TextId"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Source",
                "Value":"Name"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Width",
                "Value":"40"
            })
            selectorCol1 = et.SubElement(row2Group,"Selector",attrib={
                "ID":"[1]",
                "Value":"ValueId"
            })
            valSelect = et.SubElement(selectorCol1,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(valSelect,"Property", attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Seg1Name".format(idx = idx)
            })
            selectorCol2 = et.SubElement(row2Group,"Selector",attrib={
                "ID":"[2]",
                "Value":"ValueId"
            })
            valSelect = et.SubElement(selectorCol2,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(valSelect,"Property", attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Seg2Name".format(idx = idx)
            })
            #Row 3 group
            row3Group = et.SubElement(selectorTable,"Group",attrib={
                "ID":"[2]"
            })
            selectorCol0 = et.SubElement(row3Group,"Selector",attrib={
                "ID":"[0]",
                "Value":"TextId"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Source",
                "Value":"Type"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Width",
                "Value":"40"
            })
            selectorCol1 = et.SubElement(row3Group,"Selector",attrib={
                "ID":"[1]",
                "Value":"ValueId"
            })
            valSelect = et.SubElement(selectorCol1,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(valSelect,"Property", attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Seg1Type".format(idx = idx)
            })
            selectorCol2 = et.SubElement(row3Group,"Selector",attrib={
                "ID":"[2]",
                "Value":"ValueId"
            })
            valSelect = et.SubElement(selectorCol2,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(valSelect,"Property", attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Seg2Type".format(idx = idx)
            })
            #Row 4 group
            row4Group = et.SubElement(selectorTable,"Group",attrib={
                "ID":"[3]"
            })
            selectorCol0 = et.SubElement(row4Group,"Selector",attrib={
                "ID":"[0]",
                "Value":"TextId"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Source",
                "Value":"Relative to start of segment"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Width",
                "Value":"40"
            })
            selectorCol1 = et.SubElement(row4Group,"Selector",attrib={
                "ID":"[1]",
                "Value":"ValueId"
            })
            valSelect = et.SubElement(selectorCol1,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(valSelect,"Property", attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Seg1PosRelToStart".format(idx = idx)
            })
            selectorCol2 = et.SubElement(row4Group,"Selector",attrib={
                "ID":"[2]",
                "Value":"ValueId"
            })
            valSelect = et.SubElement(selectorCol2,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(valSelect,"Property", attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Seg2PosRelToStart".format(idx = idx)
            })
            #Row 5 group
            row5Group = et.SubElement(selectorTable,"Group",attrib={
                "ID":"[4]"
            })
            selectorCol0 = et.SubElement(row5Group,"Selector",attrib={
                "ID":"[0]",
                "Value":"TextId"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Source",
                "Value":"Relative to end of segment"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Width",
                "Value":"40"
            })
            selectorCol1 = et.SubElement(row5Group,"Selector",attrib={
                "ID":"[1]",
                "Value":"ValueId"
            })
            valSelect = et.SubElement(selectorCol1,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(valSelect,"Property", attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Seg1PosRelToEnd".format(idx = idx)
            })
            selectorCol2 = et.SubElement(row5Group,"Selector",attrib={
                "ID":"[2]",
                "Value":"ValueId"
            })
            valSelect = et.SubElement(selectorCol2,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(valSelect,"Property", attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Seg2PosRelToEnd".format(idx = idx)
            })
            #Row 6 group
            row6Group = et.SubElement(selectorTable,"Group",attrib={
                "ID":"[5]"
            })
            selectorCol0 = et.SubElement(row6Group,"Selector",attrib={
                "ID":"[0]",
                "Value":"TextId"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Source",
                "Value":"Measured Configuration Mismatch"
            })
            prop = et.SubElement(selectorCol0,"Property", attrib={
                "ID":"Width",
                "Value":"40"
            })
            selectorCol1 = et.SubElement(row6Group,"Selector",attrib={
                "ID":"[1]",
                "Value":"ValueId"
            })
            valSelect = et.SubElement(selectorCol1,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(valSelect,"Property", attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Deviation".format(idx = idx)
            })
            prop = et.SubElement(selectorCol1,"Property", attrib={
                "ID":"Width",
                "Value":"50"
            })
            prop = et.SubElement(selectorCol1,"Property", attrib={
                "ID":"HorizontalAlign",
                "Value":"1"
            })
    
    @staticmethod
    def __createCharts(parent,Diverts) -> None:
        charts = et.SubElement(parent,"Group",attrib={"ID":"Charts"})
        baseSelector = et.SubElement(charts,"Selector",attrib={
            "ID":"[0]",
            "Value":"BarChart"
        })
        prop = et.SubElement(baseSelector,"Property",attrib={
            "ID":"Name",
            "Value":"DeviationBarChart"
        })
        headingSelector = et.SubElement(baseSelector,"Selector", attrib={
            "ID":"Heading",
            "Value":"SingleText"
        })
        prop = et.SubElement(headingSelector,"Property",attrib={
            "ID":"Text",
            "Value":"Diverter Offset Mismatch Measurements"
        })
        prop = et.SubElement(headingSelector,"Property",attrib={
            "ID":"HorizontalAlign",
            "Value":"1"
        })
        prop = et.SubElement(headingSelector,"Property",attrib={
            "ID":"TextStyle",
            "Value":"Section"
        })
        prop = et.SubElement(baseSelector,"Property",attrib={
            "ID":"ChartStyle",
            "Value":"Default"
        })
        prop = et.SubElement(baseSelector,"Property",attrib={
            "ID":"TextStyle",
            "Value":"Default"
        })
        prop = et.SubElement(baseSelector,"Property",attrib={
            "ID":"ShowLegend",
            "Value":"2"
        })
        #y axis group
        yAxisGroup = et.SubElement(baseSelector,"Group",attrib={
            "ID":"YAxis"
        })
        prop = et.SubElement(yAxisGroup,"Property",attrib={
            "ID":"Label",
            "Value":"Deviation (m)"
        })
        prop = et.SubElement(yAxisGroup,"Property",attrib={
            "ID":"NumberOfGridLines",
            "Value":"4"
        })
        minValSelector = et.SubElement(yAxisGroup,"Selector",attrib={
            "ID":"ItemMinValue",
            "Value":"Dynamic"
        })
        prop = et.SubElement(minValSelector,"Property",attrib={
            "ID":"ValuePV",
            "Value":"::Maint:MinDeviation"
        })
        maxValSelector = et.SubElement(yAxisGroup,"Selector",attrib={
            "ID":"ItemMaxValue",
            "Value":"Dynamic"
        })
        prop = et.SubElement(maxValSelector,"Property",attrib={
            "ID":"ValuePV",
            "Value":"::Maint:MaxDeviation"
        })
        #Graph Items
        colorList = {
            0:"",
            1:"FF0000",
            2:"7F7F7F",
            3:"800000",
            4:"FFFF00",
            5:"800080",
            6:"00FFFF",
            7:"33CC00",
            8:"FF9900",
            9:"808000",
        }
        colorCounter = 0
        for idx,div in enumerate(Diverts):
            itmGroup = et.SubElement(baseSelector,"Group",attrib={
                "ID":"[{idx}]".format(idx=idx)
            })
            selector = et.SubElement(itmGroup,"Selector",attrib={
                "ID":"Value"
            })
            prop = et.SubElement(selector,"Property",attrib={
                "ID":"ProcessVariable",
                "Value":"::Maint:TestResults[{idx}].Deviation".format(idx=idx)
            })
            if colorCounter != 0:
                prop = et.SubElement(itmGroup,"Property",attrib={
                    "ID":"ItemColor",
                    "Value":"{color}".format(color=colorList[colorCounter])
                })    
            prop = et.SubElement(itmGroup,"Property",attrib={
                "ID":"LegendText",
                "Value":"Diverter {idx}".format(idx=idx + 1)
            })
            colorCounter += 1
            if colorCounter >= 10:
                colorCounter = 0
    
    @staticmethod
    def __createContents(parent, Diverts, AssemblyName) -> None:
        contents = et.SubElement(parent,"Group",attrib={"ID":"Contents"})
        headerGroup = et.SubElement(contents,"Group",attrib={
            "ID":"[0]",
        })
        prop = et.SubElement(headerGroup,"Property",attrib={
            "ID":"Name",
            "Value":"Header"
        })
        headerItm1 = et.SubElement(headerGroup,"Selector",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(headerItm1,"Property",attrib={
            "ID":"Text",
            "Value":"Diverter Offset Results"
        })
        prop = et.SubElement(headerItm1,"Property",attrib={
            "ID":"HorizontalAlign",
            "Value":"1"
        })
        prop = et.SubElement(headerItm1,"Property",attrib={
            "ID":"NewLine",
            "Value":"FALSE"
        })
        prop = et.SubElement(headerItm1,"Property",attrib={
            "ID":"TextStyle",
            "Value":"Title"
        })
        headerItm2 = et.SubElement(headerGroup,"Selector",attrib={
            "ID":"[1]",
            "Value":"EmptyLine"
        })
        prop = et.SubElement(headerItm2,"Property",attrib={
            "ID":"Size",
            "Value":"16"
        })
        headerItm3 = et.SubElement(headerGroup,"Selector",attrib={
            "ID":"[2]"
        })
        prop = et.SubElement(headerItm3,"Property",attrib={
            "ID":"Text",
            "Value":"{asmName}".format(asmName = AssemblyName)
        })
        prop = et.SubElement(headerItm3,"Property",attrib={
            "ID":"NewLine",
            "Value":"FALSE"
        })
        prop = et.SubElement(headerItm3,"Property",attrib={
            "ID":"TextStyle",
            "Value":"Header"
        })
        headerItm4 = et.SubElement(headerGroup,"Selector",attrib={
            "ID":"[3]",
            "Value":"DateTime"
        })
        prop = et.SubElement(headerItm4,"Property",attrib={
            "ID":"HorizontalAlign",
            "Value":"2"
        })
        prop = et.SubElement(headerItm4,"Property",attrib={
            "ID":"NewLine",
            "Value":"FALSE"
        })
        prop = et.SubElement(headerItm4,"Property",attrib={
            "ID":"TextStyle",
            "Value":"Header"
        })
        headerItm5 = et.SubElement(headerGroup,"Selector",attrib={
            "ID":"[4]",
            "Value":"EmptyLine"
        })
        prop = et.SubElement(headerItm5,"Property",attrib={
            "ID":"Size",
            "Value":"14"
        })
        #Tables
        for idx,div in enumerate(Diverts):
            tableGroup = et.SubElement(contents,"Group",attrib={
                "ID":"[{idx}]".format(idx = idx + 1)
            })
            prop = et.SubElement(tableGroup,"Property",attrib={
                "ID":"Name",
                "Value":"Diverter{idx}".format(idx = idx + 1)
            })
            tblSelect = et.SubElement(tableGroup,"Selector",attrib={
                "ID":"[0]",
                "Value":"Table"
            })
            prop = et.SubElement(tblSelect,"Property",attrib={
                "ID":"Table",
                "Value":"Divert{idx}".format(idx = idx + 1)
            })
            prop = et.SubElement(tblSelect,"Property",attrib={
                "ID":"HorizontalAlign",
                "Value":"1"
            })
            tblSelect = et.SubElement(tableGroup,"Selector",attrib={
                "ID":"[1]",
                "Value":"EmptyLine"
            })
            prop = et.SubElement(tblSelect,"Property",attrib={
                "ID":"Size",
                "Value":"16"
            })
        
        #Chart
        chartGroup = et.SubElement(contents,"Group",attrib={
            "ID":"[{idx}]".format(idx = len(Diverts) + 1)
        })
        prop = et.SubElement(chartGroup,"Property",attrib={
            "ID":"Name",
            "Value":"Chart"
        })
        chartSelector = et.SubElement(chartGroup,"Selector",attrib={
            "ID":"[0]",
            "Value":"Chart"
        })
        prop = et.SubElement(chartSelector,"Property",attrib={
            "ID":"Chart",
            "Value":"DeviationBarChart"
        })
        prop = et.SubElement(chartSelector,"Property",attrib={
            "ID":"HorizontalAlign",
            "Value":"1"
        })

    @staticmethod
    def __createReports(parent,Diverts) -> None:
        reports = et.SubElement(parent,"Group",attrib={
            "ID":"Reports"
        })
        baseGroup = et.SubElement(reports,"Group",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(baseGroup,"Property",attrib={
            "ID":"Name",
            "Value":"DiverterOffsetResults"
        })
        settingsGroup = et.SubElement(baseGroup,"Group",attrib={
            "ID":"Settings"
        })
        prop = et.SubElement(settingsGroup,"Property",attrib={
            "ID":"AllowCopy",
            "Value":"TRUE"
        })
        prop = et.SubElement(baseGroup,"Property",attrib={
            "ID":"FileNamePattern",
            "Value":r"DiverterOffsets_%Y_%m_%d_%H_%M_%S.pdf"
        })
        prop = et.SubElement(baseGroup,"Property",attrib={
            "ID":"PageLayout",
            "Value":"Default"
        })
        prop = et.SubElement(baseGroup,"Property",attrib={
            "ID":"Header",
            "Value":"Header"
        })
        #Divert tables
        for idx,div in enumerate(Diverts):
            tblGroup = et.SubElement(baseGroup,"Group",attrib={
                "ID":"[{idx}]".format(idx = idx)
            })
            headerGroup = et.SubElement(tblGroup,"Group",attrib={
                "ID":"Heading"
            })
            prop = et.SubElement(headerGroup,"Property",attrib={
                "ID":"Text",
                "Value":"Diverter {idx}".format(idx = idx + 1)
            })
            prop = et.SubElement(headerGroup,"Property",attrib={
                "ID":"TextStyle",
                "Value":"Section"
            })
            contentGroup = et.SubElement(tblGroup,"Group",attrib={
                "ID":"[0]"
            })
            prop = et.SubElement(contentGroup,"Property",attrib={
                "ID":"Content",
                "Value":"Diverter{idx}".format(idx = idx + 1)
            })
        #Chart
        chartGroup = et.SubElement(baseGroup,"Group",attrib={
            "ID":"[{idx}]".format(idx = len(Diverts))
        })
        prop = et.SubElement(chartGroup,"Property",attrib={
            "ID":"StartOnNewPage",
            "Value":"TRUE"
        })
        headerGroup = et.SubElement(chartGroup,"Group",attrib={
            "ID":"Heading"
        })
        prop = et.SubElement(headerGroup,"Property",attrib={
            "ID":"TextStyle",
            "Value":"Section"
        })
        contentGroup = et.SubElement(chartGroup,"Group",attrib={
            "ID":"[0]"
        })
        prop = et.SubElement(contentGroup,"Property",attrib={
            "ID":"Content",
            "Value":"Chart"
        })
