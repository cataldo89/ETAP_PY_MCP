import etap.api
from etap.api.other.etap_client import EtapClient
import sqlite3
import xml.etree.ElementTree as ET
from sqlite3 import Error
import matplotlib
import functools
import operator

# connect (start DataHub first)
print("Connecting...")
e = EtapClient()

# Please replace ip address and port with the one shown in DataHub
baseAddress = "http://192.168.1.87:50000"
try:
    e.connect(baseAddress)
    print("Connected to ETAP API")
except Exception as connect_error:
    print(f"Failed to connect to ETAP API: {connect_error}")
    exit()

# list of what-if commands
dataCommands = []

# Run load flow
print("Running load flow...")
outputReport = "LF Report"

try:
    result = e.studies.runLF("Base", "Normal", outputReport, "Untitled", False, dataCommands, "NA", "NA")
    if result is None:
        raise ValueError("The result from runLF is None. Please check the parameters and ensure the ETAP server is running properly.")
except Exception as e:
    print(f"Error running load flow: {e}")
    exit()

# Ensure the result is not None and valid XML
try:
    report_path = ET.fromstring(result).text
except Exception as e:
    print(f"The result from runLF is not a valid XML string: {e}")
    exit()

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
    cur.execute(r"SELECT VoltMag FROM LFR WHERE TYPE != 0;")
    rows = cur.fetchall()
    return rows

def Vang(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT VoltAng FROM LFR WHERE TYPE != 0;")
    rows = cur.fetchall()
    return rows

def BusNoLabel(conn):
    cur = conn.cursor()
    cur.execute(r"SELECT IDFrom FROM LFR WHERE TYPE != 0;")
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

matplotlib.rcParams.update({'font.size': 22})
ax = fig.add_subplot(1, 2, 1)
height = []
for j in yDataMatrix[0]:
    a = np.asscalar(np.array(j))
    height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height)
plt.title('Bus Voltage Magnitudes')
plt.xlabel('Bus No.')
plt.ylabel('V_mag (%)')
plt.subplots_adjust(wspace = 0.4)

matplotlib.rcParams.update({'font.size': 22})
ax = fig.add_subplot(1, 2, 2)
height = []
for j in yDataMatrix[1]:
    a = np.asscalar(np.array(j))
    height.append(a)
y_pos = np.arange(len(height))
plt.bar(y_pos, height)
plt.title('Bus Voltage Angles')
plt.xlabel('Bus No.')
plt.ylabel('V_ang (degree)')
plt.subplots_adjust(wspace = 0.4)

wm = plt.get_current_fig_manager()
wm.window.state('zoomed')
plt.show()
