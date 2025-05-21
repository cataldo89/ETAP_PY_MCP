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

"""Example for the EtapClient > Scenario > run section.

USAGE:
    - Configure the 'setUp' function before running the tests
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

# Scenario
import etap.api
baseAddress = "http://192.168.1.87:50000"
e = etap.api.connect(baseAddress)

# Runs the specified scenario and returns any alerts generated from the study.
# NOTE: may generate a dialog in ETAP.
# Code may not return until dialog is cleared.
# scenarioName	string	Scenario name (e.g., "AF-1-Phase")
# id	string	Scenario ID (e.g., "AF-1-Phase")
# getOnlineData	string	Whether or not to get online data for the study (e.g., "False")
# whatIfCommands	(NoType)	List of what-if commands
scenarioName = "AF-1-Phase"
id = "AF-1-Phase"
getOnlineData = False
whatIfCommands = {
    "Commands": [
        "string"
    ]
}
response = e.scenario.run(id, getOnlineData, whatIfCommands)
print(response)
# returns nothing
