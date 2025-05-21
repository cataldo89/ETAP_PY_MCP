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

"""Example for the EtapClient > ProjectData > sendpdexml section.

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


'''
<PDE Flat="1" ProjectName="Example-ANSI" PartialExported="1" Merge="0" AppVersion="20.5.0" ProjectGUID="{DC092292-1D34-4CD7-8FFF-6E31547B0BB7}" DisplayEquipment="1">
	<COMPONENTS>
		<XFORM2W ID="MyElement" LocX_D2D="5600" LocY_D2D="7048" LocX="56" LocY="70"/>
	</COMPONENTS>
	<CONNECTIONS></CONNECTIONS>
	<ASSOCIATIONS></ASSOCIATIONS>
</PDE>
'''
# Create a two-winding transformer element on OLV.
#response = e.projectdata.sendpdexml("<PDE Flat='1' ProjectName='Example-ANSI' PartialExported='1' Merge='0' AppVersion='20.5.0' ProjectGUID='{DC092292-1D34-4CD7-8FFF-6E31547B0BB7}' DisplayEquipment='1'><COMPONENTS><XFORM2W ID='MyElement' LocX_D2D='5600' LocY_D2D='7048' LocX='56' LocY='70'/></COMPONENTS><CONNECTIONS></CONNECTIONS><ASSOCIATIONS></ASSOCIATIONS></PDE>")
response = e.projectdata.sendpdexml("PFBERSBGbGF0PScxJyBQcm9qZWN0TmFtZT0nRXhhbXBsZS1BTlNJJyBQYXJ0aWFsRXhwb3J0ZWQ9JzEnIE1lcmdlPScwJyBBcHBWZXJzaW9uPScyMC41LjAnIFByb2plY3RHVUlEPSd7REMwOTIyOTItMUQzNC00Q0Q3LThGRkYtNkUzMTU0N0IwQkI3fScgRGlzcGxheUVxdWlwbWVudD0nMSc+PENPTVBPTkVOVFM+PFhGT1JNMlcgSUQ9J015RWxlbWVudCcgTG9jWF9EMkQ9JzU2MDAnIExvY1lfRDJEPSc3MDQ4JyBMb2NYPSc1NicgTG9jWT0nNzAnLz48L0NPTVBPTkVOVFM+PENPTk5FQ1RJT05TPjwvQ09OTkVDVElPTlM+PEFTU09DSUFUSU9OUz48L0FTU09DSUFUSU9OUz48L1BERT4=")
print(response)
# e.g.
# {"Value":"True"}



