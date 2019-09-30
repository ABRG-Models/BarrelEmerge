import numpy as np
# Import data loading code
import load as ld
# Import plotting code
import plot as pt
import matplotlib
import matplotlib.pyplot as plt
# To access argv:
import sys
# Direct HDF5 access
import h5py

# Set plotting defaults
fs = 12
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

# Get target x/y hex to show trace for and the time step to show the
# map for from the arguments:
if len(sys.argv) < 2:
    print('Provide logdirname on cmd line please.')
    exit(1)
logdirname = sys.argv[1]

# The ID colour map s
do_maps = 1
if do_maps:
    # Read the data
    (x, y, t, cmatrix, amatrix, nmatrix, idmatrix, tarea) = ld.readSimDataFiles (logdirname)
    for tg in range(0,23,4):
        idstring = 'id{0}'.format(tg*1000);
        pt.surface (idmatrix[:,tg], x, y, 0, idstring)

# Also load the dirichlet stuff
[t1, hondadelta, edgedev, numdoms, domarea, domcentres] = ld.readDirichData('../logs/25N2M_withcomp_realmap/')


pf = h5py.File(logdirname+'/positions.h5', 'r')
totalarea = np.array(pf['area']);
print ('total area: {0}'.format (totalarea))

# And plot this longhand here:
F1 = plt.figure (figsize=(8,8))

ax1 = F1.add_subplot(1,1,1)
l1, = ax1.plot(t1, hondadelta, 'o-', label='Honda Delta')
l2, = ax1.plot(t1, edgedev, 'o-', label='Edge deviation')
l3, = ax1.plot(t1, domarea/totalarea[0], 'go-', label='Domain area proportion')
ax1.set_title ('Shape analysis');

ax2 = F1.add_subplot(1,1,1, sharex=ax1, frameon=False)
l4, = ax2.plot(t1, numdoms, 'ro-', label='Number of domains')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax2.set_ylabel ('Num doms')

plt.legend((l1, l2, l3, l4), ('Honda Delta','Edge deviation','Domain area prop.','Number of doms'), loc='right')

plt.show()
