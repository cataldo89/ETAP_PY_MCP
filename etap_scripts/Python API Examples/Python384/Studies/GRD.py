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

import csv
import codecs
# write it as a new CSV file
with codecs.open("./grd.dat", 'r', 'utf-16') as f:
    reader = csv.reader(f, dialect='excel-tab')
    X = []
    Y = []
    data = []
    for row in reader:
        data.append(row)
    
    # Y-axis    
    count = 0
    for i in range(1, len(data[0])): 
        if data[0][i] is not ' ':
            Y.append(int(data[0][i]))
            count = count + 1
    print(Y)
    print(type(Y))   # List
    print(len(Y))
    

    # X-axis
    for i in range(1, len(data[:][1])): 
        Tmp = data[i][1].split(', ')
        X.append(float(Tmp[0]))
    print(X)
    print(type(X))   # List
    print(len(X))

    import numpy as np
    # Z-axis 
    V = []
    
    for i in range(1, len(X)+1): 
        TmpV = []  
        for j in range (1, len(Y)+1):
            Tmp = data[i][j].split(', ')
            if Tmp[1] is ' ':
                Tmp[1] = 100
            TmpV.append(float(Tmp[1])) 
        V.append(TmpV)     # all the X-axis

    print(type(V))    # List
    print(len(V))

    Arr = np.array(V)
    print(type(Arr))
    print(Arr.shape)
    print("#################")


import plotly.graph_objects as go


X, Y = np.meshgrid(X, Y)

fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Arr)])
fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_z=True))
fig.update_layout(autosize=True,
                  scene_camera_eye=dict(x=1.87, y=0.88, z=-0.64),
                  margin=dict(l=65, r=50, b=65, t=90)
)

fig.show()
