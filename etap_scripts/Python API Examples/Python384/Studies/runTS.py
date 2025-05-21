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

"""Example for running TS.
Please go to Menu--> Tools--> Options--> Edit current etaps ini, and add the following ini entries under [Etap PowerStation]:
OutputToSQLite=1
PlotAnalyzer=1
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


# connect (start DataHub first)
print("Connecting...")
baseAddress = "http://10.10.1.67:60000"
e = etap.api.connect(baseAddress)


# ping
print("Pinging...")
pingResult = e.application.ping()
print(str(pingResult))

# Run TS
print("Running TS...")
# Parameters
# revisionName: string: Revision name (e.g., "Base")
revisionName = "Base"
# configName: string: Configuration name (e.g., "Normal")
configName = "Normal"
# studyCase: string: Study case name (e.g., "TS")
studyCase = "TS"
# presentation: string: Presentation name (e.g., "Study View")
presentation = "Study View"
# outputReport	string	Output report name (e.g., "Untitled")
outputReport = "Untitled"
# getOnlineData	string	Whether or not to get online data for the study (e.g., "False")
getOnlineData = False
#runAsync string Whether or not to return immediately without waiting for study to complete (e.g, "False")
runAsync = False
# whatIfCommands	(NoType)	List of what-if commands (e.g., {"Commands": ["OPEN Tie A","OPEN Tie B","OPEN Tie C"]} )
whatIfCommands = {
    "Commands": [
        "string"
    ]
}
response = e.studies.runTS(revisionName, configName, studyCase, presentation,
                                outputReport, getOnlineData, runAsync, whatIfCommands)



P_Dict = json.loads(response)  # Python Dict
#print(P_Dict)
P_ValueTemp = P_Dict["ReportPath"]
P_Value = P_ValueTemp[:-4]
print(P_Value)
a = '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">'
b = '</string>'
result = a + P_Value + 'tspdb' + b


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
def Freq(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT Value FROM Bus23A_Frequency_8016;")
    rows = cur.fetchall()
    return rows

def Vmag(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT Value FROM Bus23A_Voltage_8016;")
    rows = cur.fetchall()
    return rows


# Main function: Plot frequency and voltage magnitude at one bus
database = report_path
conn = create_connection(database)
with conn:
    print("Visualizing frequency and voltage magnitude at Bus23A.")
    yDataMatrix = [0,1]

    yDataMatrix[0] = Freq(conn)
    yDataMatrix[1] = Vmag(conn)
    #N1 = len(yDataMatrix[0])
    #print(N1)
    #N2 = len(yDataMatrix[0])
    #print(N2)


xaxis = []
xvalue = 0
freq_Bus23A = []
for j in yDataMatrix[0]:
    xaxis.append(xvalue/1000)
    xvalue = xvalue + 1
    a=np.asscalar(np.array(j))
    freq_Bus23A.append(a)
print("Frequency at Bus23A")
print(freq_Bus23A)
Vmag_Bus23A = []
for j in yDataMatrix[1]:
    b=np.asscalar(np.array(j))
    Vmag_Bus23A.append(b)
print("Voltage magnitude at Bus23A")
print(Vmag_Bus23A)



import time
t0 = time.time()
# Add traces
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.offline


# Initialize figure with subplots
fig = make_subplots(
    rows=1, cols=2, subplot_titles=("Frequency at Bus23A", "Voltage magnitude at Bus23A")
)


fig.add_trace(
    go.Scatter( x=xaxis, y=freq_Bus23A,
                    mode='lines',
                    name='Freq'),
    row=1, col=1)    

fig.add_trace(
    go.Scatter( x=xaxis, y=Vmag_Bus23A,
                    mode='lines',
                    name='Vmag'),
    row=1, col=2)   

# Update xaxis properties
fig.update_xaxes(title_text="time (second)", row=1, col=1)
fig.update_xaxes(title_text="time (second)", row=1, col=2)

# Update yaxis properties
fig.update_yaxes(title_text="Freq (Hz)", row=1, col=1)
fig.update_yaxes(title_text="V_mag (%)", row=1, col=2)

fig.update_layout(title_text="Frequency and Voltage magnitude at Bus23A")


t1 = time.time()
total = t1 - t0
print("Total time = " + str(total))

fig.show()
