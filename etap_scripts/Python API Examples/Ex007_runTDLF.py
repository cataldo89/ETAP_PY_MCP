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
import matplotlib
import xml.etree.ElementTree as ET
from sqlite3 import Error

# connect (start DataHub first)
print("Connecting...")
e = etap.etapClient()

# Please replace ip address and port with the one shown in DataHub
e.connect("10.10.1.122", 50000, "Example-ANSI")

# ping
print("Pinging...")
pingResult = e.ping()
print(str(pingResult))

# Run TDULF
print("Running TDULF...")

revisionName = "Base"
configName = "Normal"
studyCase = "TDSimulation"
presentation = "Study View"
outputFile = "TDSimulation"
getOnlineData = False
whatIf1 = "NA"
whatIf2 = "NA"
whatIf3 = "NA"

result = e.studies.runTDLF(revisionName, configName, studyCase, presentation, outputFile, getOnlineData, whatIf1, whatIf2, whatIf3)

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
   import matplotlib.pyplot as plt
   import numpy as np
   yDataMatrix = [0,1,2,3,4,5]

   yDataMatrix[0] = Va_mag(conn)
   yDataMatrix[1] = Vb_mag(conn)
   yDataMatrix[2] = Vc_mag(conn)
   yDataMatrix[3] = Va_ang(conn)
   yDataMatrix[4] = Vb_ang(conn)
   yDataMatrix[5] = Vc_ang(conn)

fig = plt.figure()
matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(2, 3, 1)
plt.plot(yDataMatrix[0], color='r')
matplotlib.pyplot.ylim(97.350, 97.700)
plt.title('V magnitudes for Phase A at Bus 5', y=1.08)
plt.xlabel('Time (h)')
plt.ylabel('Va_mag (%)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(2, 3, 2)
plt.plot(yDataMatrix[1], color='g')
matplotlib.pyplot.ylim(97.350, 97.700)
plt.title('V magnitudes for Phase B at Bus 5', y=1.08)
plt.xlabel('Time (h)')
plt.ylabel('Vb_mag (%)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(2, 3, 3)
plt.plot(yDataMatrix[2], color='b')
matplotlib.pyplot.ylim(97.350, 97.700)
plt.title('V magnitudes for Phase C at Bus 5', y=1.08)
plt.xlabel('Time (h)')
plt.ylabel('Vc_mag (%)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(2, 3, 4)
plt.plot(yDataMatrix[3], color='r')
plt.title('V angles for Phase A at Bus 5', y=1.08)
plt.xlabel('Time (h)')
plt.ylabel('Va_ang (degree)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(2, 3, 5)
plt.plot(yDataMatrix[4], color='g')
plt.title('V angles for Phase B at Bus 5', y=1.08)
plt.xlabel('Time (h)')
plt.ylabel('Vb_ang (degree)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(2, 3, 6)
plt.plot(yDataMatrix[5], color='b')
plt.title('V angles for Phase C at Bus 5', y=1.08)
plt.xlabel('Time (h)')
plt.ylabel('Vc_ang (degree)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

wm = plt.get_current_fig_manager()
wm.window.state('zoomed')
plt.show()
