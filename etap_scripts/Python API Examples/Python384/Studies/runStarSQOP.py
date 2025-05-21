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



"""Example for running StarSQOP.
Please go to Menu--> Tools--> Options--> Edit current etaps ini, and add the following ini entries under [Etap PowerStation]:
OutputToSQLite=1
Save the file and restart ETAP. 

USAGE:
    - Configure the 'setUp' function before running the example
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

import etap.api
import sqlite3
import xml.etree.ElementTree as ET
from sqlite3 import Error
import functools 
import operator
import json
import numpy as np
import csv


# connect (start DataHub first)
print("Connecting...")
baseAddress = "http://192.168.1.87:50000"
e = etap.api.connect(baseAddress)


# ping
print("Pinging...")
pingResult = e.application.ping()
print(str(pingResult))

# Run HA
print("Running StarSQOP...")
# Parameters
# revisionName: string: Revision name (e.g., "Base")
revisionName = "Base"
# configName: string: Configuration name (e.g., "Normal")
configName = "Emergency"
# studyCase: string: Study case name (e.g., "HA")
studyCase = "SQOP"
# presentation: string: Presentation name (e.g., "Study View")
presentation = "OLV1"
# outputReport	string	Output report name (e.g., "Untitled")
outputReport = "Untitled"
# Energized Bus ID (e.g., "LVBus")
busID = "Bus3"
# Fault type (e.g., "3-Phase", "Line-to-Ground", "Line-to-Line", "Line-to-Line-to-Ground")
faultType = "Line-to-Ground"

response = e.studies.runStarSQOP(revisionName, configName, studyCase, presentation, outputReport, busID, faultType)

print(response)   # json str
# '{"SQOPEventFile":"D:\\Loads\\FG1.6-Rel\\Example-ANSI\\Untitled_StarSQOPEvents.csv"}'

#P_Dict = json.loads(response)  # Python Dict
#print(P_Dict)
#P_Value = P_Dict["SQOPEventFile"]
P_Value = response
print(P_Value)

# print content in output report
with open(P_Value, newline='') as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(row)