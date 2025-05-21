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

"""Example for running TDLF.

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


# Run TDULF
print("Running TDULF...")
# Parameters
# revisionName: string: Revision name (e.g., "Base")
revisionName = "Base"
# configName: string: Configuration name (e.g., "Normal")
configName = "Normal"
# studyCase: string: Study case name (e.g., "TDSimulation")
studyCase = "TDSimulation"
# presentation: string: Presentation name (e.g., "Study view")
presentation = "Study View"
# outputReport: string: Output report name (e.g., "TDSimulation")
outputReport = "TDSimulation"
# getOnlineData: string: Whether or not to get online data for the study (e.g., "False")
getOnlineData = False
onlineConfigOnly = False
# whatIfCommands: (NoType): List of what-if commands (e.g., {"Commands": ["OPEN Tie A","OPEN Tie B","OPEN Tie C"]} )
whatIfCommands = {
    "Commands": [
        "string"
    ]
}
response = e.studies.runTDLF(revisionName, configName, studyCase, presentation,
                                    outputReport, getOnlineData, onlineConfigOnly, whatIfCommands)


#print(response)   # json str
# '{"ReportPath":"E:\FG1p5-Rel\Example-ANSI\TDSimulation.TU1S"}'
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
def Va_mag(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT VPhA FROM tdbusresult WHERE BusIID='485042';")
    rows = cur.fetchall()
    return rows

def Vb_mag(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT VPhB FROM tdbusresult WHERE BusIID='485042';")
    rows = cur.fetchall()
    return rows

def Vc_mag(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT VPhC FROM tdbusresult WHERE BusIID='485042';")
    rows = cur.fetchall()
    return rows
def Va_ang(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT AngPhA FROM tdbusresult WHERE BusIID='485042';")
    rows = cur.fetchall()
    return rows
def Vb_ang(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT AngPhB FROM tdbusresult WHERE BusIID='485042';")
    rows = cur.fetchall()
    return rows
def Vc_ang(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT AngPhC FROM tdbusresult WHERE BusIID='485042';")
    rows = cur.fetchall()
    return rows


# Main function: Plot voltage magnitudes and angles of ABC phases
database = report_path
conn = create_connection(database)
with conn:
    print("Visualizing time series(24h) voltages")
    yDataMatrix = [0,1,2,3,4,5]

    yDataMatrix[0] = Va_mag(conn)
    yDataMatrix[1] = Vb_mag(conn)
    yDataMatrix[2] = Vc_mag(conn)
    yDataMatrix[3] = Va_ang(conn)
    yDataMatrix[4] = Vb_ang(conn)
    yDataMatrix[5] = Vc_ang(conn)

vmaga = []
for j in yDataMatrix[0]:
    a=np.asscalar(np.array(j))
    vmaga.append(a)

vmagb = []
for j in yDataMatrix[1]:
    a=np.asscalar(np.array(j))
    vmagb.append(a)

vmagc = []
for j in yDataMatrix[2]:
    a=np.asscalar(np.array(j))
    vmagc.append(a)

vanga = []
for j in yDataMatrix[3]:
    b=np.asscalar(np.array(j))
    vanga.append(b)

vangb = []
for j in yDataMatrix[4]:
    b=np.asscalar(np.array(j))
    vangb.append(b)


vangc = []
for j in yDataMatrix[5]:
    b=np.asscalar(np.array(j))
    vangc.append(b)

# Add traces
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.offline


# Initialize figure with subplots
fig = make_subplots(
    rows=2, cols=3, subplot_titles=("V magnitudes for Phase A at Bus 5",
                                    "V magnitudes for Phase B at Bus 5",
                                    "V magnitudes for Phase C at Bus 5",
                                    "V angles for Phase A at Bus 5",
                                    "V angles for Phase B at Bus 5",
                                    "V angles for Phase C at Bus 5")
)

fig.add_trace(
    go.Scatter( y=vmaga,
                    mode='lines',
                    name='vmaga'),
    row=1, col=1)

fig.add_trace(
    go.Scatter( y=vmagb,
                    mode='lines',
                    name='vmagb'),
    row=1, col=2)

fig.add_trace(
    go.Scatter( y=vmagc,
                    mode='lines',
                    name='vmagc'),
    row=1, col=3)

fig.add_trace(
    go.Scatter( y=vanga,
                    mode='lines',
                    name='vanga'),
    row=2, col=1)

fig.add_trace(
    go.Scatter( y=vangb,
                    mode='lines',
                    name='vangb'),
    row=2, col=2)

fig.add_trace(
    go.Scatter( y=vangc,
                    mode='lines',
                    name='vangc'),
    row=2, col=3)

# Update xaxis properties
fig.update_xaxes(title_text="Time (h)", row=1, col=1)
fig.update_xaxes(title_text="Time (h)", row=1, col=2)
fig.update_xaxes(title_text="Time (h)", row=1, col=3)
fig.update_xaxes(title_text="Time (h)", row=2, col=1)
fig.update_xaxes(title_text="Time (h)", row=2, col=2)
fig.update_xaxes(title_text="Time (h)", row=2, col=3)

# Update yaxis properties
fig.update_yaxes(title_text="Va_mag (%)", row=1, col=1)
fig.update_yaxes(title_text="Vb_mag (%)", row=1, col=2)
fig.update_yaxes(title_text="Vc_mag (%)", row=1, col=3)
fig.update_yaxes(title_text="Va_ang (degree)", row=2, col=1)
fig.update_yaxes(title_text="Vb_ang (degree)", row=2, col=2)
fig.update_yaxes(title_text="Vc_ang (degree)", row=2, col=3)


fig.update_layout(title_text="Voltage Magnitudes/Angles at Bus 5")

fig.show()