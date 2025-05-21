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

"""
Example 04: Unbalanced load flow
This script commands ETAPto run an unbalanced load flow study.
ETAP returns the output report file path.
Since the simulation results are in output database the script also shows how to read result data
"""

import etap
import sqlite3
import xml.etree.ElementTree as ET
from sqlite3 import Error
import matplotlib
import functools
import operator


print("Connecting...")
e = etap.etapClient()
# Please replace ip address and port with the one shown in DataHub
e.connect("10.10.1.122", 50000, "Example-ANSI")

# ping
print("Pinging...")
pingResult = e.ping()
print(str(pingResult))

# Run unbalanced LF
print("Running ULF...")
result = e.studies.runULF("Base", "Normal", "ULF", "Untitled");
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

# Function definition: Get voltage magnitudes and angles of ABC phases
def Va_mag(conn):
   cur = conn.cursor()
   cur.execute(r"SELECT voltmaga FROM lf3phr WHERE type != ' ';")
   rows = cur.fetchall()
   return rows
def Vb_mag(conn):
   cur = conn.cursor()
   cur.execute(r"SELECT voltmagb FROM lf3phr WHERE type != ' ';")
   rows = cur.fetchall()
   return rows
def Vc_mag(conn):
   cur = conn.cursor()
   cur.execute(r"SELECT voltmagc FROM lf3phr WHERE type != ' ';")
   rows = cur.fetchall()
   return rows
def Va_ang(conn):
   cur = conn.cursor()
   cur.execute(r"SELECT voltanga FROM lf3phr WHERE type != ' ';")
   rows = cur.fetchall()
   return rows
def Vb_ang(conn):
   cur = conn.cursor()
   cur.execute(r"SELECT voltangb FROM lf3phr WHERE type != ' ';")
   rows = cur.fetchall()
   return rows
def Vc_ang(conn):
   cur = conn.cursor()
   cur.execute(r"SELECT voltangc FROM lf3phr WHERE type != ' ';")
   rows = cur.fetchall()
   return rows
def BusNoLabel(conn):
   cur = conn.cursor()
   cur.execute(r"SELECT idfrom FROM lf3phr WHERE type != ' ';")
   rows = cur.fetchall()
   return rows

# Main function: Plot voltage magnitudes and angles of ABC phases
database = report_path
conn = create_connection(database)
with conn:
   print("Visualizing magnitudes and angles of voltages.")
   import matplotlib.pyplot as plt
   import numpy as np
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

print('Print bus numbers and names')
for BusNo in yDataMatrix[6]:
   index = yDataMatrix[6].index(BusNo)
   print(str(index) + ' --> ' + convertTuple(BusNo))

fig = plt.figure()

matplotlib.rcParams.update({'font.size': 16})
ax = fig.add_subplot(2, 3, 1)
height = []
for j in yDataMatrix[0]:
   a=np.asscalar(np.array(j))
   height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height, color=['red'])
plt.title('V magnitudes for Phase A')
plt.xlabel('Bus No.')
plt.ylabel('Va_mag (%)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 16})
ax = fig.add_subplot(2, 3, 2)
height = []
for j in yDataMatrix[1]:
   a=np.asscalar(np.array(j))
   height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height, color=['green'])
plt.title('V magnitudes for Phase B')
plt.xlabel('Bus No.')
plt.ylabel('Vb_mag (%)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 16})
ax = fig.add_subplot(2, 3, 3)
height = []
for j in yDataMatrix[2]:
   a=np.asscalar(np.array(j))
   height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height, color=['blue'])
plt.title('V magnitudes for Phase C')
plt.xlabel('Bus No.')
plt.ylabel('Vc_mag (%)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 16})
ax = fig.add_subplot(2, 3, 4)
height = []
for j in yDataMatrix[3]:
   a=np.asscalar(np.array(j))
   height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height, color=['red'])
plt.title('V angles for Phase A')
plt.xlabel('Bus No.')
plt.ylabel('Va_ang (degree)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 16})
ax = fig.add_subplot(2, 3, 5)
height = []
for j in yDataMatrix[4]:
   a=np.asscalar(np.array(j))
   height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height, color=['green'])
plt.title('V angles for Phase B')
plt.xlabel('Bus No.')
plt.ylabel('Vb_ang (degree)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

matplotlib.rcParams.update({'font.size': 16})
ax = fig.add_subplot(2, 3, 6)
height = []
for j in yDataMatrix[5]:
   a=np.asscalar(np.array(j))
   height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height, color=['blue'])
plt.title('V angles for Phase C')
plt.xlabel('Bus No.')
plt.ylabel('Vc_ang (degree)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

wm = plt.get_current_fig_manager()
wm.window.state('zoomed')
plt.show()
