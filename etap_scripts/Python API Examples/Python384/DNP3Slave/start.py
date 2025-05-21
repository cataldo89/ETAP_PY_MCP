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

"""Example for the EtapClient > DNP3 SLAVE > start section.

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
IP = "10.10.1.71"
e = etap.api.connect(baseAddress)


# To confirm it is running properly.
dnp3SettingsInit = [{
    "Link": {
        "Ip": IP,
        "PortNumber": 20000,
        "LocalAddress": 10,
        "RemoteAddress": 1
    },
    "Outstation": {
        "UnsolicitedMode": "false",
        "EventBuffer": 100,
        "SolicitedConfirmTimeoutMs": 5000,
        "UnsolicitedConfirmTimeoutMs": 5000,
        "UnsolicitedRetry": 10,
        "SelectTimeoutMs": 5000,
        "MaxTxFragmentSize": 2048,
        "MaxControlsPerRequest": 100
    },
    "Database": {
        "Binary": [
            [
                "0",
                "Group1Var2",
                "Group2Var2"
            ],
            [
                "1",
                "Group1Var2",
                "Group2Var2"
            ],
            [
                "2",
                "Group1Var2",
                "Group2Var2"
            ]
        ],
        "DoubleBinary": [
            [
                "0",
                "Group3Var2",
                "Group4Var1"
            ]
        ],
        "Counter": [
            [
                "0",
                "Group20Var1",
                "Group22Var1"
            ]
        ],
        "FrozenCounter": [
            [
                "0",
                "Group21Var1",
                "Group23Var1"
            ]
        ],
        "Analog": [
            [
                "0",
                "Group30Var5",
                "Group32Var5",
                "0.1"
            ],
            [
                "1",
                "Group30Var5",
                "Group32Var5",
                "0.1"
            ],
            [
                "2",
                "Group30Var5",
                "Group32Var5",
                "0.1"
            ]
        ],
        "BinaryOutput": [
            [
                "0",
                "Group10Var2",
                "Group11Var2"
            ],
            [
                "1",
                "Group10Var2",
                "Group11Var2"
            ],
            [
                "2",
                "Group10Var2",
                "Group11Var2"
            ]
        ],
        "AnalogOutput": [
            [
                "0",
                "Group40Var3",
                "Group42Var5",
                "0.5"
            ],
            [
                "1",
                "Group40Var3",
                "Group42Var5",
                "0.5"
            ],
            [
                "2",
                "Group40Var3",
                "Group42Var5",
                "0.5"
            ]
        ]
    },
    "Class": {
        "BinaryInputs": "Class1",
        "BinaryOutputs": "Class1",
        "AnalogInputs": "Class2",
        "AnalogOutputs": "Class2",
        "Counters": "Class1",
        "DoubleBinary": "Class1",
        "FrozenCounters": "Class1"
    },
    "Data": {
        "AnalogInputs": [
            [
                "0",
                "11.11",
                "132561632244882287",
                "LOCAL_FORCED"
            ],
            [
                "1",
                "22.22",
                "132561632244882287",
                "LOCAL_FORCED"
            ],
            [
                "2",
                "33.33",
                "132561632244882287",
                "LOCAL_FORCED"
            ]
        ],
        "BinaryInputs": [
            [
                "0",
                "true",
                "132561632244882287",
                "LOCAL_FORCED"
            ],
            [
                "1",
                "true",
                "132561632244882287",
                "LOCAL_FORCED"
            ],
            [
                "2",
                "true",
                "132561632244882287",
                "LOCAL_FORCED"
            ]
        ],
        "Counters": [
            [
                "0",
                "1",
                "132561632244882287",
                "LOCAL_FORCED"
            ]
        ],
        "DoubleBinary": [
            [
                "0",
                "true",
                "132561632244882287",
                "LOCAL_FORCED"
            ]
        ],
        "FrozenCounters": [
            [
                "0",
                "1",
                "132561632244882287",
                "LOCAL_FORCED"
            ]
        ],
        "BinaryOutputs": [
            [
                "0",
                "true",
                "132561632244882287",
                "LOCAL_FORCED"
            ],
            [
                "1",
                "true",
                "132561632244882287",
                "LOCAL_FORCED"
            ],
            [
                "2",
                "true",
                "132561632244882287",
                "LOCAL_FORCED"
            ]
        ],
        "AnalogOutputs": [
            [
                "0",
                "44.44",
                "132561632244882287",
                "LOCAL_FORCED"
            ],
            [
                "1",
                "55.55",
                "132561632244882287",
                "LOCAL_FORCED"
            ],
            [
                "2",
                "66.66",
                "132561632244882287",
                "LOCAL_FORCED"
            ]
        ]
    }
}]
# You could also use some JSON Formatter to format it before putting it here.
#response = e.dnp3slave.start([{"Link":{"Ip":"10.10.1.84","PortNumber":20000,"LocalAddress":10,"RemoteAddress":1},"Outstation":{"UnsolicitedMode":"false","EventBuffer":100,"SolicitedConfirmTimeoutMs":5000,"UnsolicitedConfirmTimeoutMs":5000,"UnsolicitedRetry":10,"SelectTimeoutMs":5000,"MaxTxFragmentSize":2048,"MaxControlsPerRequest":100},"Database":{"Binary":[["0","Group1Var2","Group2Var2"],["1","Group1Var2","Group2Var2"],["2","Group1Var2","Group2Var2"]],"DoubleBinary":[["0","Group3Var2","Group4Var1"]],"Counter":[["0","Group20Var1","Group22Var1"]],"FrozenCounter":[["0","Group21Var1","Group23Var1"]],"Analog":[["0","Group30Var5","Group32Var5","0.1"],["1","Group30Var5","Group32Var5","0.1"],["2","Group30Var5","Group32Var5","0.1"]],"BinaryOutput":[["0","Group10Var2","Group11Var2"],["1","Group10Var2","Group11Var2"],["2","Group10Var2","Group11Var2"]],"AnalogOutput":[["0","Group40Var3","Group42Var5","0.5"],["1","Group40Var3","Group42Var5","0.5"],["2","Group40Var3","Group42Var5","0.5"]]},"Class":{"BinaryInputs":"Class1","BinaryOutputs":"Class1","AnalogInputs":"Class2","AnalogOutputs":"Class2","Counters":"Class1","DoubleBinary":"Class1","FrozenCounters":"Class1"},"Data":{"AnalogInputs":[["0","11.11","132561632244882287","LOCAL_FORCED"],["1","22.22","132561632244882287","LOCAL_FORCED"],["2","33.33","132561632244882287","LOCAL_FORCED"]],"BinaryInputs":[["0","true","132561632244882287","LOCAL_FORCED"],["1","true","132561632244882287","LOCAL_FORCED"],["2","true","132561632244882287","LOCAL_FORCED"]],"Counters":[["0","1","132561632244882287","LOCAL_FORCED"]],"DoubleBinary":[["0","true","132561632244882287","LOCAL_FORCED"]],"FrozenCounters":[["0","1","132561632244882287","LOCAL_FORCED"]],"BinaryOutputs":[["0","true","132561632244882287","LOCAL_FORCED"],["1","true","132561632244882287","LOCAL_FORCED"],["2","true","132561632244882287","LOCAL_FORCED"]],"AnalogOutputs":[["0","44.44","132561632244882287","LOCAL_FORCED"],["1","55.55","132561632244882287","LOCAL_FORCED"],["2","66.66","132561632244882287","LOCAL_FORCED"]]}}])
response = e.dnp3slave.start(dnp3SettingsInit)
print(response)