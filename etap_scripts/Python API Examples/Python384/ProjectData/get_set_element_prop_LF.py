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

"""Example for getting and setting element property with running LF.

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

import plotly.graph_objects as go
import plotly.offline
import webbrowser

# Function definition: Create connection
def create_connection(db_file):
	"""Create connection to database

	Args:
		db_file (str): database file with path

	Returns:
		connection object: connection to database
	"""   
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn

# connect (start DataHub first)
print("Connecting...")
baseAddress = "http://10.10.1.71:50000"
e = etap.api.connect(baseAddress)

# ping
print("Pinging...")
pingResult = e.application.ping()
print(str(pingResult))

# list of what-if commands
dataCommands = []


# LF Parameters
# revisionName: string: Revision name (e.g., "Base")
revisionName = "Base"
# configName: string: Configuration name (e.g., "Normal")
configName = "Normal"
# studyCase: string: Study case name (e.g., "LF Report")
studyCase = "LF Report"
presentation = "Study View"
# outputReport: string: Output report name (e.g., "Untitled")
outputReport = "Untitled"
# getOnlineData: string: Whether or not to get online data for the study (e.g,. "False")
getOnlineData = False
onlineConfigOnly = False
# whatIfCommands: (NoType): List of what-if commands (e.g., {"Commands": ["OPEN Tie A","OPEN Tie B","OPEN Tie C"]} )
whatIfCommands = {
    "Commands": [
        "string"
    ]
}

xArray = []
yArray = []

elementType = "XFORM2W"
elementName = "T2"
fieldName = "AnsiPosZ"
#fieldName = "AnsiZeroZ"

# Get and save current value
print("\nGetting original element property: ", elementType + " / " + elementName + " / " + fieldName)
response = e.projectdata.getelementprop(elementType, elementName, fieldName)
P_Dict = json.loads(response)
originalValue = P_Dict["Value"]
print("originalValue",  originalValue)

a = ''
b = ''
result = ''
posZ = 5
number_of_iter = 10
resultElementName = "Sub2A"
	
for iter in range(number_of_iter):
	value = str(posZ)

	print("\nSetting element property: ", elementType + " / " + elementName + " / " + fieldName + " / " + value)
	response = e.projectdata.setelementprop(elementType, elementName, fieldName, value)
	print("response",  response)

	print("Run LF study")

	# Runs an load flow study. The output report location is returned in the response body.
	response = e.studies.runLF(
		revisionName, configName, studyCase, presentation, outputReport, getOnlineData, onlineConfigOnly, whatIfCommands)
	P_Dict = json.loads(response)  # Python Dict
	P_Value = P_Dict["ReportPath"]
	a = '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">'
	b = '</string>'
	result = a + P_Value + b

	report_path = ET.fromstring(result).text

	# Get some resutl from DB for an element as an example
	database = report_path
	conn = create_connection(database)
	cur = conn.cursor()
	sqlite_select_query = "SELECT VoltMag FROM LFR WHERE TYPE != 0 AND kV !=0 AND IDFrom = '" +  resultElementName + "';"
	cur.execute(sqlite_select_query)
	records = cur.fetchall()
	for row in records:
		yArray.append(row[0]) # should have one row
		print("Get VoltMag of " + resultElementName)
		print("[" + str(posZ) + ", " + str(row[0]) + "]")
	xArray.append(posZ)

	posZ = posZ + 0.5

# Setting back original value
print("\nSetting back original value: ", elementType + " / " + elementName + " / " + fieldName + " / " + originalValue)
response = e.projectdata.setelementprop(elementType, elementName, fieldName, originalValue)
print("response",  response)

config = {
		"displayModeBar": True,
		"modeBarButtonsToRemove": ["logomark", "select2d", "lasso2d"],
		"scrollZoom": True,
		"editable": False,
		"showLink":False,
		"displaylogo": False
	}
line_width = 1.5

fig = go.Figure()

plot_data = go.Scatter(
		x = xArray, y = yArray,
		mode = "lines",
		name = resultElementName,
		line = dict(
			width = line_width,
			color = "Red",
		),
		showlegend = True,
		hovertext = "VoltMag - " + resultElementName,
		hoverinfo = "x+y+text",
)
fig.add_trace(plot_data)

range_slider_bgcolor_dark = "#2c3236"

fig.update_layout(
	title = {
		"text": "VoltMag vs " + fieldName,
		"yref": "paper",
		"y" : 1,
		"yanchor" : "bottom",
		"pad": {"l": 40, "b": 15},
	},
	xaxis = dict(
		rangeslider = dict(
			visible = True,
			thickness = 1/20,
			bgcolor = range_slider_bgcolor_dark,
		),
		title = fieldName,
	),
	yaxis = dict(
		title ="VoltMag",
	),
	template = "plotly_dark",
)

plotly.offline.plot(fig, filename = "ProperyChangeTest.html", auto_open = True, config = config)
