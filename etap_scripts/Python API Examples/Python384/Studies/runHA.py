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



"""Example for running HA.
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

# Please change the "File_Path" with double backslash before running.
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

# Run HA
print("Running HA...")
# Parameters
# revisionName: string: Revision name (e.g., "Base")
revisionName = "Base"
# configName: string: Configuration name (e.g., "Normal")
configName = "Normal"
# studyCase: string: Study case name (e.g., "HA")
studyCase = "HA"
# presentation: string: Presentation name (e.g., "Study View")
presentation = "Study View"
# outputReport	string	Output report name (e.g., "Untitled")
outputReport = "Untitled"
# getOnlineData	string	Whether or not to get online data for the study (e.g., "False")
getOnlineData = False
# whatIfCommands	(NoType)	List of what-if commands (e.g., {"Commands": ["OPEN Tie A","OPEN Tie B","OPEN Tie C"]} )
studyType = "Harmonic Load Flow"
whatIfCommands = {
    "Overwrite_Source_And_Load_Category": {
        "Loading_Cat": [],
        "Generation_Cat": []
    },
    "Overwrite_Utility_SC_Rating": {
        "ThreePhase_MVAsc": [],
        "ThreePhase_XoverR": [],
        "OnePhase_MVAsc": [],
        "OnePhase_XoverR": []
},
    "Outage_List_File_Path": {
        "File_Path": "D:\\runha.xlsx",
        "Base_Revision_Name": "string"
    }
}



'''
whatIfCommands = {
	"Overwrite_Source_And_Load_Category": {
		"Loading_Cat": [
			["Load1", "120", "105"],
			["VFD1", "200", "205"]
		],
		"Generation_Cat": [
			["Gen1", "90", "95"],
			["Inv1", "80", "85"]
		]
	},
	"Overwrite_Utility_SC_Rating": {
		"ThreePhase_MVAsc": [
			["U1", "100", "120"],
			["U2", "110", "130"]
		],
		"ThreePhase_XoverR": [
			["U1", "9.5", "7.8"],
			["U2", "9.6", "7.9"]
		],
		"OnePhase_MVAsc": [
			["U1", "80", "75"],
			["U2", "81", "76"]
		],
		"OnePhase_XoverR": [
			["U1", "8.5", "6.2"],
			["U2", "8.6", "6.3"]
		]
	},
	"Outage_List_File_Path": {
		"File_Path": "D:\\Delete\\HA\\outageList.xlsx"
	}
}
'''


response = e.studies.runHA(revisionName, configName, studyCase, presentation,
                                outputReport, getOnlineData, studyType, whatIfCommands)

#print(response)   # json str
# '{"ReportPath":"E:\FG1p5-Rel\Example-ANSI\Untitled.TS1S"}'


P_Dict = json.loads(response)  # Python Dict
#print(P_Dict)
P_Value = P_Dict["ReportPath"]
print(P_Value)
a = '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">'
b = '</string>'
result = a + P_Value + b


# Get path of the report
report_path = ET.fromstring(result).text

'''
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
    cur.execute(r"SELECT BusV FROM VQSensitivity;")
    rows = cur.fetchall()
    return rows

def VQSensitivity(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT VQSensitivity FROM VQSensitivity;")
    rows = cur.fetchall()
    return rows


# Main function: Plot frequency and voltage magnitude at one bus
database = report_path
conn = create_connection(database)
with conn:
    print("Visualizing BusV and VQSensitivity.")
    yDataMatrix = [0,1]

    yDataMatrix[0] = Vmag(conn)
    yDataMatrix[1] = VQSensitivity(conn)
    #N1 = len(yDataMatrix[0])
    #print(N1)
    #N2 = len(yDataMatrix[0])
    #print(N2)


xaxis = []
xvalue = 0
BusV = []
for j in yDataMatrix[0]:
    xaxis.append(xvalue/1000)
    xvalue = xvalue + 1
    a=np.asscalar(np.array(j))
    BusV.append(a)
print("BusV")
print(BusV)
VQSensitivity = []
for j in yDataMatrix[1]:
    b=np.asscalar(np.array(j))
    VQSensitivity.append(b)
print("VQSensitivity")
print(VQSensitivity)



import time
t0 = time.time()
# Add traces
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.offline


# Initialize figure with subplots
fig = make_subplots(
    rows=1, cols=2, subplot_titles=("BusV", "VQSensitivity")
)


fig.add_trace(
    go.Scatter( x=xaxis, y=BusV,
                    mode='lines',
                    name='BusV'),
    row=1, col=1)    

fig.add_trace(
    go.Scatter( x=xaxis, y=VQSensitivity,
                    mode='lines',
                    name='VQSensitivity'),
    row=1, col=2)   

# Update xaxis properties
fig.update_xaxes(title_text="time (second)", row=1, col=1)
fig.update_xaxes(title_text="time (second)", row=1, col=2)

# Update yaxis properties
fig.update_yaxes(title_text="BusV (%)", row=1, col=1)
fig.update_yaxes(title_text="VQSensitivity (1)", row=1, col=2)

fig.update_layout(title_text="BusV & VQSensitivity")


t1 = time.time()
total = t1 - t0
print("Total time = " + str(total))

fig.show()
'''