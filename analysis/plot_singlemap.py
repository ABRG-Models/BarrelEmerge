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
    print('Provide logdirname on cmd line please. Optionally provide time index.')
    exit(1)
logdirname = sys.argv[1]

if len(sys.argv) > 2:
    ti = int(sys.argv[2])
else:
    ti = -1

# Read the data
(x, y, t, cmatrix, amatrix, nmatrix, idmatrix, tarea) = ld.readSimDataFiles (logdirname)
#for tg in range(0,4,4):
idstring = 'id{0}'.format(0);
print ('idstring: {0}'.format(idstring))

# Plot one of the a matrices:
shp = np.shape(idmatrix)
print ('idmatrix shape: {0}'.format(shp))
if ti == -1:
    ti = shp[1]-1
print ('ti = {0}'.format(ti))
f1 = pt.surface (idmatrix[:,ti], x, y, 0, idstring)


plt.show()
