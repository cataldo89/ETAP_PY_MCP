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

"""Example for the EtapClient > Application > filepaths section.

USAGE:
    - Configure the 'setUp' function before running the tests
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

# Application
import etap.api
baseAddress = "http://10.10.1.84:65285"
e = etap.api.connect(baseAddress)



# Returns select folder and file paths from ETAP.
response = e.application.filepaths()
print(response)
# e.g. 
# {
#   "PathCurrentDirectory": "E:\\Cypress4Rel",
#   "PathTempPath": "C:\\Users\\John.Doe\\AppData\\Local\\Temp\\",
#   "PathAppData": "C:\\Users\\John.Doe\\AppData\\Roaming",
#   "PathAppDataLocal": "C:\\Users\\John.Doe\\AppData\\Local",
#   "PathAppDataCommon": "C:\\ProgramData",
#   "AssemblyGetExecutingAssembly": "E:\\Cypress4Rel\\DataHubServiceLibrary.dll"
# }
