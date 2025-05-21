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

"""Example for running MS.

USAGE:
    - Configure the 'setUp' function before running the example
    - Start ETAP 
    - Open Example-RT-Industrial
    - While in Motor Acceleration mode, selected the "MS study case
    - Uncheck "Skip Tabulated Plots" and click "OK"
    - Start DataHub
    - Run with [F5]

"""

# MS-Dyn Study Case--> Uncheck 'Skip Tabulated Plots'
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
baseAddress = "http://10.10.2.36:60000"
e = etap.api.connect(baseAddress)


# ping
print("Pinging...")
pingResult = e.application.ping()
print(str(pingResult))

# Run MS
print("Running Auto Motor Starting...")
# Paremeters
# revisionName: string: Revision name (e.g., "Base")
revisionName = "Base"
# configName: string: Configuration name (e.g., "Normal")
configName = "Normal"
# studyCase: string: Study case name (e.g., "MS-Dyn")
studyCase = "MS"
# presentation: string: Presentation name (e.g., "Study view")
presentation = "Sys Monitor"
# outputReport: string: Output report name (e.g., "Untitled")
outputReport = "Untitled"
# getOnlineData: string: Whether or not to get online data for the study (e.g., "False")
getOnlineData = False
# onlineConfigOnly: string: Whether or not to use online config only for the study (e.g., "False")
onlineConfigOnly = False
# numMotorStart: string: Number of motors that should be started (e.g., "1")
numMotorStart = 1
# studyType: string: Motor starting study type (e.g., "Static", "Dynamic")
studyType = "Static"  # TODO : 'studyType' should be an enum
# whatIfCommands: (NoType): List of what-if commands (e.g., {"Commands": ["OPEN Tie A","OPEN Tie B","OPEN Tie C"]} )
whatIfCommands = {
    "Commands": [
        "string"
    ]
}

response = e.studies.runMS(revisionName, configName, studyCase, presentation,
                                outputReport, getOnlineData, onlineConfigOnly, numMotorStart, studyType, whatIfCommands)


#print(response)   # json str
# '{"ReportPath":"E:\\FG1p5-Rel\\Example-ANSI\\Untitled.MS1S"}'
P_Dict = json.loads(response)  # Python Dict
#print(P_Dict)
P_Value = P_Dict["ReportPath"]
print(P_Value)
FilePath = str(P_Value)
print(FilePath)
#"D:\Loads\FG1.5-Rel\Example-ANSI\Untitled_Mtr7.MS1S;D:\Loads\FG1.5-Rel\Example-ANSI\Untitled_Mtr2.MS1S;D:\Loads\FG1.5-Rel\Example-ANSI\Untitled_Pump 1.MS1S;D:\Loads\FG1.5-Rel\Example-ANSI\Untitled_Syn1.MS1S;"
OnePath = FilePath.split(";")  # remove trailing ';' char 
print(OnePath)
a = '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">'
b = '</string>'
result = a + OnePath[0] + b

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


# Function definition: Get currents and bus voltages
    
def I_CrshC5(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT current FROM msacceleration WHERE id = 'Crusher C5';")
    rows = cur.fetchall()
    return rows

def V_CrshC5(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT busv FROM msacceleration WHERE id = 'Crusher C5';")
    rows = cur.fetchall()
    return rows


# Main function: Plot voltage magnitudes and angles
database = report_path
print(database)
conn = create_connection(database)
with conn:
    print("Visualizing currents and bus voltages of motors.")

    
    yDataMatrix = [0,1]

    
    yDataMatrix[0] = I_CrshC5(conn)
    yDataMatrix[1] = V_CrshC5(conn)


A = []
for j in yDataMatrix[0]:
    a=np.asscalar(np.array(j))
    A.append(a)

V = []
for j in yDataMatrix[1]:
    a=np.asscalar(np.array(j))
    V.append(a)

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.offline

# Initialize figure with subplots
fig = make_subplots(
    # rows=1, cols=2, subplot_titles=('Mtr7', 'Mtr7')
    rows=1, cols=2, subplot_titles=('Crusher C5', 'Crusher C5')
)

fig.add_trace(
    go.Scatter(y=A,
                    mode='lines',
                    name='A'),
    row=1, col=1)

fig.add_trace(
    go.Scatter(y=V,
                    mode='lines',
                    name='V'),
    row=1, col=2)

# Update xaxis properties
fig.update_xaxes(title_text='Time(10ms)', row=1, col=1)
fig.update_xaxes(title_text='Time(10ms)', row=1, col=2)


# Update yaxis properties
fig.update_yaxes(title_text='Amps', row=1, col=1)
fig.update_yaxes(title_text='Voltage (%)', row=1, col=2)


fig.show()
