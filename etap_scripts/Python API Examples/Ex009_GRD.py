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
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

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

    
    # Z-axis
    V = []   
    for i in range(1, len(X)+1): 
        TmpV = []  
        for j in range (1, len(Y)+1):
            Tmp = data[i][j].split(', ')
            if Tmp[1] is ' ':
                Tmp[1] = 100
            TmpV.append(float(Tmp[1]))
        V.append(TmpV)

    print(type(V))    # List
    print(len(V))

    Arr = np.array(V)
    print(type(Arr))
    print(Arr.shape)
    print("#################")


# 3-D plotting

fig = plt.figure()
ax = fig.gca(projection='3d')
X, Y = np.meshgrid(X, Y)

# Plot the surface.
surf = ax.plot_surface(X, Y, Arr, cmap=cm.hsv,
                       linewidth=0, antialiased=False)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
