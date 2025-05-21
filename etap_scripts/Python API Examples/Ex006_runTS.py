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

import etap
import sqlite3
import xml.etree.ElementTree as ET
from sqlite3 import Error
import matplotlib
import functools
import operator
# connect (start DataHub first)
print("Connecting...")

e = etap.etapClient()

# Please replace ip address and port with the one shown in DataHub
e.connect("10.10.1.122", 50000, "Example-ANSI")
# ping
print("Pinging...")
pingResult = e.ping()
print(str(pingResult))
# Run TS
print("Running TS...")
revisionName = "Base"
configName = "Normal"
studyCase = "TS"
presentation = "Study View"
outputFile = "Untitled"
getOnlineData = True
whatIf1 = "NA"
whatIf2 = "NA"
whatIf3 = "NA"
result = e.studies.runTS(revisionName,configName,studyCase,presentation,outputFile,getOnlineData,whatIf1,whatIf2,whatIf3);
print(result)
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
   cur.execute(r"SELECT VoltMag FROM LFR WHERE TYPE != 0 and Time = 5.0;")
   rows = cur.fetchall()
   return rows
def Vang(conn):
   cur = conn.cursor()
   cur.execute(r"SELECT VoltAng FROM LFR WHERE TYPE != 0 and Time = 5.0;")
   rows = cur.fetchall()
   return rows
def BusNoLabel(conn):
   cur = conn.cursor()
   cur.execute(r"SELECT IDFrom FROM LFR WHERE TYPE != 0 and Time = 5.0;")
   rows = cur.fetchall()
   return rows
# Main function: Plot voltage magnitudes and angles
database = report_path
conn = create_connection(database)
with conn:
   print("Visualizing magnitudes and angles of voltages.")
   import matplotlib.pyplot as plt
   import numpy as np
   yDataMatrix = [0,1,2]
   yDataMatrix[0] = Vmag(conn)
   yDataMatrix[1] = Vang(conn)
   yDataMatrix[2] = BusNoLabel(conn)
def convertTuple(tup):
   str = functools.reduce(operator.add, (tup))
   return str
print('Print bus numbers and names')
for BusNo in yDataMatrix[2]:
   index = yDataMatrix[2].index(BusNo)
   print(str(index) + ' --> ' + convertTuple(BusNo))
fig = plt.figure()

matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(1, 2, 1)
height = []
for j in yDataMatrix[0]:
   a=np.asscalar(np.array(j))
   height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height)
plt.title('Bus Voltage Magnitudes at Stop Time')
plt.xlabel('Bus No.')
plt.ylabel('V_mag (%)')
plt.subplots_adjust(wspace = 0.4)

matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(1, 2, 2)
height = []
for j in yDataMatrix[1]:
   a=np.asscalar(np.array(j))
   height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height)
plt.title('Bus Voltage Angles at Stop Time')
plt.xlabel('Bus No.')
plt.ylabel('V_ang (degree)')
plt.subplots_adjust(wspace = 0.4)

wm = plt.get_current_fig_manager()
wm.window.state('zoomed')
plt.show()

