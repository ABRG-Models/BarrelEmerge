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
[t1, hondadelta, edgedev, numdoms, domarea, domcentres] = ld.readDirichData (logdirname)

print ('domcentres shape: {0}'.format(np.shape (domcentres)[0]))

# What does this want to do? Return, for a given timestep (or for every timestep), the average verticalness of the lines of best fit to groups of centres.
def domcentres_analyse (dc, isvert=True):
    numtc = np.shape(dc)[0]
    tc = 0
    linefits = []
    while tc < numtc:
        if isvert:
            #print ('tc: {1}; ALL x: {0}'.format(dc[tc,:,0], tc))
            #print ('tc: {1}; ALL y: {0}'.format(dc[tc,:,1], tc))
            print ('-----tc:{0}------'.format(tc))
            F2 = plt.figure (figsize=(20,4))
            count = int(1)
            for i in range(0,25,5):
                # Note: Swap around x and y, so that vertical lines will come out with m=0 (approx)
                ly = dc[tc,i:5+i,0] # x
                lx = dc[tc,i:5+i,1] # y
                A = np.vstack([lx, np.ones(len(lx))]).T
                #m, c, resid = np.linalg.lstsq (A, ly, rcond=None)
                m = 0
                c = 0
                out = np.linalg.lstsq (A, ly, rcond=None)
                m, c = out[0]
                # FIxme: FIgure out what out[1] and out[3] mean.

                print ('out: {0}'.format(out))
                print ('y = {0} x + {1}'.format(m,c))
                a2 = F2.add_subplot(1,5,count)
                _ = a2.plot(lx, ly, 'o', label='Original data', markersize=10)
                _ = a2.plot(lx, m*lx + c, 'r', label='Fitted line')
                a2.set_xlim([-0.6, 0.6])
                a2.set_ylim([-0.8, 0.8])
                _ = a2.legend()
                count = count + int(1)
            plt.show()

        tc = tc + 1
    return linefits

lfits = domcentres_analyse (domcentres)


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
