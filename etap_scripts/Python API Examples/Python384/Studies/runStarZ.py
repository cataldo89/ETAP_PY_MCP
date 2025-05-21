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

"""Example for running StarZ.

USAGE:
    - Configure the 'setUp' function before running the example
    - Start ETAP 
    - Open Example-StarZ
    - Start DataHub
    - Run with [F5]

"""

# This script should use "Example-StarZ" instead of "Example-ANSI"
import etap.api
import sqlite3
import xml.etree.ElementTree as ET
from sqlite3 import Error
import functools 
import operator
import json
import numpy as np


# connect (start DataHub first)
print("Connecting...")
baseAddress = "http://192.168.1.87:50000"
e = etap.api.connect(baseAddress)


# ping
print("Pinging...")
pingResult = e.application.ping()
print(str(pingResult))


# Run StarZ
print("Running StarZ...")
# Parameters
# revisionName: string: Revision name (e.g., "Base")
revisionName = "Base"
# configName: string: Configuration name (e.g., "Normal")
configName = "Normal"
# studyCase: string: Study case name (e.g., "L1-LG")
studyCase = "L1-LG"
# outputReport: string: Output report name (e.g., "L1-LG")
outputReport = "L1-LG"

response = e.studies.runStarZ(revisionName, configName, studyCase, outputReport)

print(response)
# E:\ETAPS\Cypress4Rel\Example-StarZ\L1-LG.SZ3S
