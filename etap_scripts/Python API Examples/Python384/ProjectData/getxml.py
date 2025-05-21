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

"""Example for the EtapClient > ProjectData > getxml section.

USAGE:
    - Configure the 'setUp' function before running the tests
    - Start ETAP 
    - Open Example-ANSI
    - Start DataHub
    - Run with [F5]

"""

# Project Data
import etap.api
baseAddress = "http://10.10.1.84:65285"
e = etap.api.connect(baseAddress)

# Returns XML for the current ETAP project. NOTE: the first call to this method takes longer than subsequent calls.
result = e.projectdata.getxml()
print(result)
# e.g.
# <?xml version="1.0"?><PDE Flat="0" ProjectName="Example-ANSI" PartialExported="0" Merge="0" ProjectGUID="{DC092292-1D34-4CD7-8FFF-6E31547B0BB7}" DisplayEquipment="1"><PROJECTINFO ProjectTitle="Example" Location="Irvine, California" ContractNo="OTI-12345678" Date="08/28/2020" Engineer="Operation Technology, Inc." Revision="Base" Standard="0" Frequency="60.000000" UnitSystem="1" Config="Normal"/><COMPONENTS/><LAYOUT><BUS EnclosureData="&lt;EnclosureData&gt;&lt;EnclosureItem EnclosureID=&quot;Bus1-2&quot; EnclosureType=&quot;1&quot; ElectrodeCo ...
