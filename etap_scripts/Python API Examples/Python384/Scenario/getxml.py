#***********************
#
# Copyright (c) 2019-2020, Operation Technology, Inc.
#
# THIS PROGRAM IS CONFIDENTIAL AND PROPRIETARY TO OPERATION TECHNOLOGY, INC. 
# ANY USE OF THIS PROGRAM IS SUBJECT TO THE PROGRAM SOFTWARE LICENSE AGREEMENT, 
# EXCEPT THAT THE USER MAY MODIFY THE PROGRAM FOR ITS OWN USE. 
# HOWEVER, THE PROGRAM MAY NOT BE REPRODUCED, PUBLISHED, OR DISCLOSED TO OTHERS 
# WITHOUT THE PRIOR WRITTEN CONSENT OF OPERATION TECHNOLOGY, INC.
#
#***********************

"""Example for the EtapClient > Scenario > getxml section.

USAGE:
    - Configure the 'setUp' function before running the tests
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

# Scenario
import etap.api
baseAddress = "http://10.10.1.84:65285"
e = etap.api.connect(baseAddress)

# Returns an XML description of the scenarios defined for the current project.
result = e.scenario.getxml()
print(result)
# e.g.
#<?xml version="1.0" encoding="utf-8"?> <scenarios xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" LastRunScenario="" Version="1"> <Scenario ID="AF-Decay" Executable="Yes" ForceSave="Yes" background="No" ToolTip="\n\n" System="Network Analysis" Presentation="Study View" Mode="STUDY_SHORTCIRCUIT ANSI ARC-FLASH" Config="Normal" StudyCase="AF Decay" Revision="Base" Output="AF-Decay" ActionTool="STUDY_SHORTCIRCUIT ANSI ARC-FLASH" Comments="" Compare="True" NewFilePath=".\AF-Decay.AAFS" Compare_benchmark=".\Output\AF-Decay.AAFS" InstructionFilePath="..\DBCompareInstr.sdf" UseETAPDefaultLibrary="True" Compare_deviationReportFile=".\AF-Decay_DBCompare.sdf" Compare_globalSummaryFile="C:\Users\nazan.roshdieh\AppData\Roaming\OTI\ETAPS\14.0.0\GlobalSummaryReport.sdf" Compare_skipRecordsThatPass="True" Compare_percentDev="0.1" Compare_skipProjInfo="True" Compare_remarks="" Compare_commandLine="" Compare_skipDates="False" Compare_autoOpen="False" IniSettings="" GetOnlineData="False" WhatIfCommands="" IsComparePlot="False" PlotCompareOutput="" MaxPlotDiff="" TotalPlotDiff="" ConfigDBID="-2080309247 , 32" PresentationDBID="-2130640895 , 9088" RevisionDBID="-268107775 , 32" StudyCaseDBID="-2056191999 , 491670" />   <Scenario ID="AF-HalfCycle

