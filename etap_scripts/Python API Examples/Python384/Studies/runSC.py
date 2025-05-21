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

"""Example for running SC.

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


# connect (start DataHub first)
print("Connecting...")
baseAddress = "http://10.10.1.71:50000"
e = etap.api.connect(baseAddress)


# ping
print("Pinging...")
pingResult = e.application.ping()
print(str(pingResult))


# Run SC
print("Running SC...")
# Parameters
# revisionName: string: Revision name (e.g., "Base")
revisionName = "Base"
# configName: string: Configuration name (e.g., "Normal")
configName = "Normal"
# studyCase: string: Study case name (e.g., "ANSI Duty")
studyCase = "IEC - Duty"
# presentation: string: Presentation name (e.g., "Study view")
presentation = "Study View"
# outputReport: string: Output report name (e.g., "SC")
outputReport = "SC"
# getOnlineData: string: Whether or not to get online data for the study (e.g., "False")
getOnlineData = False
onlineConfigOnly = False
# studyType: string: e.g. "ANSI 1 Phase Device Duty", "ANSI Device Duty", "ANSI All Fault Interrupting", "IEC Device Duty", "IEC Transient Fault Current"
studyType = "IEC Transient Fault Current"
# whatIfCommands: (NoType): List of what-if commands (e.g., {"Commands": ["OPEN Tie A","OPEN Tie B","OPEN Tie C"]} )
whatIfCommands = {
    "Commands": [
        "string"
    ]
}
response = e.studies.runSC(revisionName, configName, studyCase, presentation,
                                    outputReport, getOnlineData, onlineConfigOnly, studyType, whatIfCommands)


#print(response)   # json str
# '{"ReportPath":"E:\FG1p5-Rel\Example-ANSI\Untitled.SA4S"}'
P_Dict = json.loads(response)  # Python Dict
#print(P_Dict)
P_Value = P_Dict["ReportPath"]
print(P_Value)
a = '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">'
b = '</string>'
result = a + P_Value + b


# Get path of the report
report_path = ET.fromstring(result).text

# Function definition: Create connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# Function definition: Get voltage magnitudes and angles
def T(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT [T(s)] FROM SCIEC363 WHERE FaultedBus='Main Bus';")
    rows = cur.fetchall()
    return rows

def I(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT ikA FROM SCIEC363 WHERE FaultedBus='Main Bus';")
    rows = cur.fetchall()
    return rows

# Main function: Plot voltage magnitudes and angles
database = report_path
conn = create_connection(database)
with conn:
    print("Visualizing Total Fault Current at Main Bus vs Fault Time.")
    yDataMatrix = [0,1]

    yDataMatrix[0] = T(conn)
    yDataMatrix[1] = I(conn)

T = []
for j in yDataMatrix[0]:
    a=np.asscalar(np.array(j))
    T.append(a)

I = []
for j in yDataMatrix[1]:
    b=np.asscalar(np.array(j))
    I.append(b)

# Add traces
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.offline

# Initialize figure with subplots
fig = make_subplots(
    rows=1, cols=1, subplot_titles=("Total Fault Current")
)

fig.add_trace(
    go.Scatter(x=T, y=I,
                    mode='lines',
                    name='vmaga'),
    row=1, col=1)

# Update xaxis properties
fig.update_xaxes(title_text="Fault Time (s)", row=1, col=1)

# Update yaxis properties
fig.update_yaxes(title_text="Total Fault Current at Main Bus (A)", row=1, col=1)

fig.update_layout(title_text="Total Fault Current at faulted bus")

fig.show()