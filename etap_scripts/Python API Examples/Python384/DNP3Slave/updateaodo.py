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

"""Example for the EtapClient > DNP3 SLAVE > updateaodo section.

USAGE:
    - Configure the 'setUp' function before running the tests
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

# Dnp3 Slave
import etap.api
baseAddress = "http://10.10.1.71:60000"
e = etap.api.connect(baseAddress)


# To confirm it is running properly.
dnp3SettingsRuntime = [
{
    "Data": {
    "AnalogOutputs": [
    [
        "0",
        "111.11",
        "132567562624938433",
        "ONLINE"
    ],
    [
        "1",
        "222.22",
        "132567562624938433",
        "ONLINE"
    ],
    [
        "2",
        "333.33",
        "132567562624938433",
        "ONLINE"
    ]
    ],
    "BinaryOutputs": [
    [
        "0",
        "false",
        "132567562624938433",
        "ONLINE"
    ],
    [
        "1",
        "false",
        "132567562624938433",
        "ONLINE"
    ],
    [
        "2",
        "false",
        "132567562624938433",
        "ONLINE"
    ]
    ]
    }
}
]

response = e.dnp3slave.updateaodo(dnp3SettingsRuntime)  
print(response)