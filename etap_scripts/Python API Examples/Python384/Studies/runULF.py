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

"""Example for running ULF.

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
import requests



# connect (start DataHub first)
print("Connecting...")
baseAddress = "http://10.10.1.71:50000"
e = etap.api.connect(baseAddress)


# ping
print("Pinging...")
pingResult = e.application.ping()
print(str(pingResult))

# Run unbalanced LF
print("Running ULF...")
#Parameters:
#revisionName: string: Revision name (e.g., "Base")
revisionName = "Base"
#configName: string: Configuration name (e.g., "Normal")
configName = "Normal"
#studyCase: string: Study case name (e.g., "ULF")
studyCase = "ULF"
presentation = "Study View"
#outputReport: string: Output report name (e.g., "Untitled")
outputReport = "Untitled"
getOnlineData = False
onlineConfigOnly = False
'''
whatIfCommands = {
  "Commands": [
    "string"
  ]
}

whatIfCommands = {
  "Commands": [
    "OPEN CB2"
  ]
  
}
'''
#response = e.studies.runULF(revisionName, configName, studyCase, presentation, outputReport, getOnlineData, onlineConfigOnly, whatIfCommands)
response = e.studies.runULF(revisionName, configName, studyCase, presentation, outputReport, getOnlineData, onlineConfigOnly)

'''
try:    
    response = e.studies.runULF(revisionName, configName, studyCase, presentation, outputReport, getOnlineData, onlineConfigOnly)
except (requests.exceptions.HTTPError, ValueError, NameError) as exception:
    # handle error here
    #print(exception.response.content)
'''
print(response)   # json str
# e.g.
# '{"ReportPath":"E:\\FG1p5-Rel\\Example-ANSI\\Untitled.UL1S"}'

P_Dict = json.loads(response)  # Python Dict
#print(P_Dict)
P_Value = P_Dict["ReportPath"]
print(P_Value)
a = '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">'
b = '</string>'
result = a + P_Value + b


# Get path of the report
report_path = ET.fromstring(result).text
print(report_path)


# Function definition: Create connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# Function definition: Get voltage magnitudes and angles of ABC phases
def Va_mag(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT voltmaga FROM lf3phr WHERE type != ' ' AND kV !=0;")
    rows = cur.fetchall()
    return rows

def Vb_mag(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT voltmagb FROM lf3phr WHERE type != ' ' AND kV !=0;")
    rows = cur.fetchall()
    return rows

def Vc_mag(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT voltmagc FROM lf3phr WHERE type != ' ' AND kV !=0;")
    rows = cur.fetchall()
    return rows
def Va_ang(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT voltanga FROM lf3phr WHERE type != ' ' AND kV !=0;")
    rows = cur.fetchall()
    return rows
def Vb_ang(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT voltangb FROM lf3phr WHERE type != ' ' AND kV !=0;")
    rows = cur.fetchall()
    return rows
def Vc_ang(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT voltangc FROM lf3phr WHERE type != ' ' AND kV !=0;")
    rows = cur.fetchall()
    return rows
    
def BusNoLabel(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT DISTINCT idfrom FROM lf3phr WHERE type != ' ' AND kV !=0;")
    rows = cur.fetchall()
    return rows

# Main function: Plot voltage magnitudes and angles of ABC phases
database = report_path
conn = create_connection(database)
with conn:
    print("Visualizing magnitudes and angles of voltages.")
    yDataMatrix = [0,1,2,3,4,5,6]

    yDataMatrix[0] = Va_mag(conn)
    yDataMatrix[1] = Vb_mag(conn)
    yDataMatrix[2] = Vc_mag(conn)
    yDataMatrix[3] = Va_ang(conn)
    yDataMatrix[4] = Vb_ang(conn)
    yDataMatrix[5] = Vc_ang(conn)
    yDataMatrix[6] = BusNoLabel(conn)

def convertTuple(tup): 
    str = functools.reduce(operator.add, (tup)) 
    return str


Index = []
print('Print bus numbers and names')
for BusNo in yDataMatrix[6]:
    index = yDataMatrix[6].index(BusNo)
    print(str(index) + ' --> ' + convertTuple(BusNo))
    Index.append(index)

Va_mag = []
for j in yDataMatrix[0]:
    a=np.asscalar(np.array(j))
    Va_mag.append(a)

Vb_mag = []
for j in yDataMatrix[1]:
    a=np.asscalar(np.array(j))
    Vb_mag.append(a)

Vc_mag = []
for j in yDataMatrix[2]:
    a=np.asscalar(np.array(j))
    Vc_mag.append(a)

Va_ang = []
for j in yDataMatrix[3]:
    a=np.asscalar(np.array(j))
    Va_ang.append(a)

Vb_ang = []
for j in yDataMatrix[4]:
    a=np.asscalar(np.array(j))
    Vb_ang.append(a)

Vc_ang = []
for j in yDataMatrix[5]:
    a=np.asscalar(np.array(j))
    Vc_ang.append(a)


from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Initialize figure with subplots
fig = make_subplots(
    rows=2, cols=3, subplot_titles=('V magnitudes for Phase A', 'V magnitudes for Phase B',
                                    'V magnitudes for Phase C', 'V angles for Phase A',
                                    'V angles for Phase B', 'V angles for Phase C')
)

fig.add_trace(
    go.Bar(x=Index, y=Va_mag,
                    name='Va_mag'),
    row=1, col=1)

fig.add_trace(
    go.Bar(x=Index, y=Vb_mag,
                    name='Vb_mag'),
    row=1, col=2)

fig.add_trace(
    go.Bar(x=Index, y=Vc_mag,
                    name='Vc_mag'),
    row=1, col=3)

fig.add_trace(
    go.Bar(x=Index, y=Va_ang,
                    name='Va_ang'),
    row=2, col=1)

fig.add_trace(
    go.Bar(x=Index, y=Vb_ang,
                    name='Vb_ang'),
    row=2, col=2)

fig.add_trace(
    go.Bar(x=Index, y=Vc_ang,
                    name='Vc_ang'),
    row=2, col=3)

# Update xaxis properties
fig.update_xaxes(title_text="Bus No.", row=1, col=1)
fig.update_xaxes(title_text="Bus No.", row=1, col=2)
fig.update_xaxes(title_text="Bus No.", row=1, col=3)
fig.update_xaxes(title_text="Bus No.", row=2, col=1)
fig.update_xaxes(title_text="Bus No.", row=2, col=2)
fig.update_xaxes(title_text="Bus No.", row=2, col=3)

# Update yaxis properties
fig.update_yaxes(title_text="Va_mag (%)", row=1, col=1)
fig.update_yaxes(title_text="Vb_mag (%)", row=1, col=2)
fig.update_yaxes(title_text="Vc_mag (%)", row=1, col=3)
fig.update_yaxes(title_text="Va_ang (degree)", row=2, col=1)
fig.update_yaxes(title_text="Vb_ang (degree)", row=2, col=2)
fig.update_yaxes(title_text="Vc_ang (degree)", row=2, col=3)


fig.update_layout(title_text="Bus Voltage Magnitudes/Angles")

fig.show()
