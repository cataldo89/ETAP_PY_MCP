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

"""Example for running LF.

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
baseAddress = "http://192.168.1.87:50000"
e = etap.api.connect(baseAddress)


# ping
print("Pinging...")
pingResult = e.application.ping()
print(str(pingResult))


# list of what-if commands
dataCommands = []


# Run LF
print("Running load flow...")
# Parameters
revisionName = "Base"
configName = "Normal"
studyCase = "LF Report"
presentation = "Study View"
outputReport = "Untitled"
getOnlineData = False
onlineConfigOnly = False
whatIfCommands = {"Commands": ["string"]}

# Runs an load flow study. The output report location is returned in the response body.
response = e.studies.runLF(
    revisionName, configName, studyCase, presentation, outputReport, getOnlineData, onlineConfigOnly, whatIfCommands)

P_Dict = json.loads(response)  # Python Dict
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
def Vmag(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT VoltMag FROM LFR WHERE TYPE != 0 AND kV !=0;")
    rows = cur.fetchall()
    return rows

def Vang(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT VoltAng FROM LFR WHERE TYPE != 0 AND kV !=0;")
    rows = cur.fetchall()
    return rows
    
def BusNoLabel(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT IDFrom FROM LFR WHERE TYPE != 0 AND kV !=0;")
    rows = cur.fetchall()
    return rows


# Main function: Plot voltage magnitudes and angles
database = report_path
conn = create_connection(database)
with conn:
    print("Visualizing magnitudes and angles of voltages.")
    yDataMatrix = [0,1,2]

    yDataMatrix[0] = Vmag(conn)
    yDataMatrix[1] = Vang(conn)
    yDataMatrix[2] = BusNoLabel(conn)
    
def convertTuple(tup): 
    str = functools.reduce(operator.add, (tup)) 
    return str

Index = []
print('Print bus numbers and names')
for BusNo in yDataMatrix[2]:
    index = yDataMatrix[2].index(BusNo)
    print(str(index) + ' --> ' + convertTuple(BusNo))
    Index.append(index)

vmag = []
for j in yDataMatrix[0]:
    a = np.array(j).item()  # ✅ CORREGIDO: Reemplazo de `asscalar()`
    vmag.append(a)

vang = []
for j in yDataMatrix[1]:
    b = np.array(j).item()  # ✅ CORREGIDO: Reemplazo de `asscalar()`
    vang.append(b)


# Add traces
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.offline


# Initialize figure with subplots
fig = make_subplots(
    rows=1, cols=2, subplot_titles=("Bus Voltage Magnitudes", "Bus Voltage Angles")
)

fig.add_trace(
    go.Bar(x=Index, y=vmag, name='vmag'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=Index, y=vang, name='vang'),
    row=1, col=2
)

# Update xaxis properties
fig.update_xaxes(title_text="Bus No.", row=1, col=1)
fig.update_xaxes(title_text="Bus No.", row=1, col=2)

# Update yaxis properties
fig.update_yaxes(title_text="V_mag (%)", row=1, col=1)
fig.update_yaxes(title_text="V_ang (degree)", row=1, col=2)

fig.update_layout(title_text="Bus Voltage Magnitudes/Angles")

fig.show()
