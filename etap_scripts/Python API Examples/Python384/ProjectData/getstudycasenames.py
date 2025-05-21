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

"""Example for the EtapClient > ProjectData > getstudycasenames section.

USAGE:
    - Configure the 'setUp' function before running the tests
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

# Project Data
import etap.api
baseAddress = "http://10.10.1.71:50000"
e = etap.api.connect(baseAddress)


# Returns the list of all bus names
result = e.projectdata.getstudycasenames()
print(result)
# e.g.
# {"Default":["AF","CD","OCP","CA","CSD","CSDAC","DCAF","BS","DCLF","DCSC","Distrib_LF","Distrib_SC","SF","FMSR","HA","ILS","LoadAlloc","LF 100A","MS-Static","OPF","Train","RA","ANSI Duty","SM","SZM","AGC","SO","SSM","TDSimulation","TS","ULF","SC3Ph","VS","VVO"],"NonDefault":["AF IEC","AF 1-Phase","ArcF_LL","AF Decay","AF 4 Cycle","ArcF_3Ph","AF HalfCycle","ArcF_LG","DCAF PAUKERT","DCAF MAX","DCAF STOKES","Discharge","LF Report","LF 200 DF","LF 100B","Case200Sum","MS-Dyn","IEC 909","IEC 1-Phase","ANSI-Min","IEC - Duty","ANSI-Max","Max","ANSI-4Cycle","AF Star Auto","SQOP","StarZ-1Fault","TDPrediction","ShortTime","Case200 X","UnifiedLF"]}
