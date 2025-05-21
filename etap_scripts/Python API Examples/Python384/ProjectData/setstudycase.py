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

"""Example for the EtapClient > ProjectData > setstudycase section.

USAGE:
    - Configure the 'setUp' function before running the tests
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

# Project Data
import etap.api
baseAddress = "http://10.10.1.1:50000"
e = etap.api.connect(baseAddress)

# Adds a new (or replaces an existing) study case.
response = e.projectdata.setstudycase({"activePDs": ["string"],
    "analysisType": 0,
    "boolFields": 0,
    "busLevel": 0,
    "cableGlobalTemp": 0,
    "cableLenTolerance": 0,
    "checkerAdjust": 0,
    "checkerLF": 0,
    "checkerRelay": 0,
    "checkerSC": 0,
    "commentText": "string",
    "diversityFactor": 0,
    "diversityFactorConstI": 0,
    "diversityFactorConstKVA": 0,
    "diversityFactorConstZ": 0,
    "diversityFactorGeneric": 0,
    "faultImpedanceR": 0,
    "faultImpedanceRTo": 0,
    "faultImpedanceStep": 0,
    "faultImpedanceX": 0,
    "faultInsertionGID": 0,
    "faultInsertionID": "string",
    "faultInsertionIID": 0,
    "faultLocation": 0,
    "faultLocationEnd": 0,
    "faultLocationStart": 0,
    "faultLocationStep": 0,
    "faultType": 0,
    "flashOperatedPDs": 0,
    "generationCategory": 0,
    "id": "string",
    "iid": 0,
    "issue": 0,
    "lgPhaseType": 0,
    "lineGlobalTemp": 0,
    "lineLenTolerance": 0,
    "llPhaseType": 0,
    "llgPhaseType": 0,
    "loadingCategory": 0,
    "maximumIteration": 0,
    "methodType": 0,
    "module": "string",
    "movMaximumIteration": 0,
    "movProtectionPrecision": 0,
    "ohTolerance": 0,
    "pyobject": "string",
    "reactorResistTolerance": 0,
    "referenceBusGID": 0,
    "referenceBusID": "string",
    "referenceBusIID": 0,
    "remark": "string",
    "simulationTime": 0,
    "simulationTimeOpt": 0,
    "slidingFaultTime": 0,
    "solutionPrecision": 0,
    "startingBus": 0,
    "tsStudyCaseID": "string",
    "tsStudyCaseIID": 0,
    "voltageAngle": 0,
    "voltageMagnitude": 0,
    "xfmrImpTolerance": 0
}
)
print(response)
# e.g.
# {"Result":true}