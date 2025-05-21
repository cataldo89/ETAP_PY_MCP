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

# Connects to ETAP and pings it.
# 2/11/19

import etap

# get version
print("ETAP Package Version: " + etap.getVersion())

# connect (start DataHub first)
print("Connecting...")
e = etap.etapClient()

# Please replace ip address and port with the one shown in DataHub
e.connect("10.10.1.12", 62012, "Example-ANSI")

# ping
print("Pinging...")
pingResult = e.ping()
print(str(pingResult))
