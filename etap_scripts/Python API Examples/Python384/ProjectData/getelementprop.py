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

"""Example for the EtapClient > ProjectData > getElementProp section.

USAGE:
    - Configure the 'setUp' function before running the tests
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

# Project Data
import etap.api
import json
baseAddress = "http://10.10.1.1:60000"
e = etap.api.connect(baseAddress)


# Get value of a field of the property of an element
# Args:
#    elementType (str): The type of element
#    elementName (str): The name of element
#    fieldName (str): The name of the field of element property
# Returns:
#    str: value or empty string '' for failure

result = e.projectdata.getelementprop("XFORM2W", "T2", "AnsiPosZ")
Dict = json.loads(result)
print(result)
#print(Dict["Value"])
# e.g.
# {"Value":"6.900000"}
