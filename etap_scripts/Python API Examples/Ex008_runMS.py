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


# connect (start DataHub first)
print("Connecting...")
e = etap.etapClient()

# Please replace ip address and port with the one shown in DataHub
e.connect("10.10.1.122", 50000, "Example-ANSI")

# ping
print("Pinging...")
pingResult = e.ping()
print(str(pingResult))

# Run MS
print("Running Auto Motor Starting...")

revisionName = "Base"
configName = "Normal"
studyCase = "MS-Dyn"
presentation = "Study View"
outputFile = "Untitled"
getOnlineData = False
numMotorStart = 1
studyType = 'Dynamic'
whatIf1 = "NA"
whatIf2 = "NA"
whatIf3 = "NA"

result = e.studies.runMS(revisionName, configName, studyCase, presentation, outputFile, getOnlineData, numMotorStart, studyType, whatIf1, whatIf2, whatIf3)

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


def I_Syn1(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT current FROM msacceleration WHERE id = 'Syn1';")
    rows = cur.fetchall()
    return rows

def V_Syn1(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT busv FROM msacceleration WHERE id = 'Syn1';")
    rows = cur.fetchall()
    return rows
    
def I_Mtr7(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT current FROM msacceleration WHERE id = 'Mtr7';")
    rows = cur.fetchall()
    return rows

def V_Mtr7(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT busv FROM msacceleration WHERE id = 'Mtr7';")
    rows = cur.fetchall()
    return rows

def I_Pump1(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT current FROM msacceleration WHERE id = 'Pump 1';")
    rows = cur.fetchall()
    return rows

def V_Pump1(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT busv FROM msacceleration WHERE id = 'Pump 1';")
    rows = cur.fetchall()
    return rows



# Main function: Plot voltage magnitudes and angles
database = report_path
print(database)
conn = create_connection(database)
with conn:
    print("Visualizing currents and bus voltages of motors.")
    import matplotlib.pyplot as plt
    import numpy as np
    
    yDataMatrix = [0,1,2,3,4,5]

    yDataMatrix[0] = I_Syn1(conn)
    yDataMatrix[1] = V_Syn1(conn)
    yDataMatrix[2] = I_Mtr7(conn)
    yDataMatrix[3] = V_Mtr7(conn)
    yDataMatrix[4] = I_Pump1(conn)
    yDataMatrix[5] = V_Pump1(conn)

fig = plt.figure()


matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(1, 2, 1)
plt.plot(yDataMatrix[2], color='b')
#matplotlib.pyplot.ylim(90, 100)
plt.title('Mtr7')
plt.xlabel('Time(10ms)')
plt.ylabel('Amps')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)


matplotlib.rcParams.update({'font.size': 18})
ax = fig.add_subplot(1, 2, 2)
plt.plot(yDataMatrix[3], color='b')
matplotlib.pyplot.ylim(85, 100)
plt.title('Mtr7')
plt.xlabel('Time(10ms)')
plt.ylabel('Voltage (%)')
plt.subplots_adjust(hspace = 0.5, wspace = 0.4)

wm = plt.get_current_fig_manager()
wm.window.state('zoomed')
plt.show()
