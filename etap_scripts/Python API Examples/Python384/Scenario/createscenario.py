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

"""Example for the EtapClient > Scenario > createscenario section.

USAGE:
    - Configure the 'setUp' function before running the tests
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

# Scenario
import etap.api
baseAddress = "http://10.10.1.88:60000"
e = etap.api.connect(baseAddress)
scenarioID = "Scenario-LF"
system = "Network Analysis"
presentation = "Study View"
revisionName = "Base"
configName = "Normal"
studyMode = "Load Flow"
studyType = "Load Flow"
studyCase = "LF Report"
outputReport = "Untitled"

# Creates a new scenario. Returns boolean True or False 
result = e.scenario.createscenario(scenarioID, system, presentation, revisionName, configName, studyMode, studyType, studyCase, outputReport)
print(result)
