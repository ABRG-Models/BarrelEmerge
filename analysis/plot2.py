# To access argv and also include the include dir
import sys
sys.path.insert (0, './include')
import numpy as np
# Import data loading code
import load as ld
# Import MY plotting code:
import plot as pt
import matplotlib
import matplotlib.pyplot as plt
# Direct HDF5 access
import h5py
# My domcentres linear fit code:
import domcentres as dc

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

# Read the data
(x, y, t, cmatrix, amatrix, nmatrix, idmatrix, tarea) = ld.readSimDataFiles (logdirname)
#for tg in range(0,4,4):
idstring = 'id{0}'.format(0);
print ('idstring: {0}'.format(idstring))
print ('amatrix shape: {0}'.format(np.shape(amatrix)))
f1 = pt.surface (amatrix[0,:,0], x, y, 0, idstring)
# Plot centroids:
#f1.plot (domcentres[tg][:,0], domcentres[tg][:,1], 'o')


plt.show()
