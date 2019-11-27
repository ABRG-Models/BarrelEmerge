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
import os

# Get target x/y hex to show trace for and the time step to show the
# map for from the arguments:
if len(sys.argv) < 2:
    print('Provide logdirname on cmd line please. Optionally provide molecule index.')
    exit(1)
logdirname = sys.argv[1]

# molecule index
if len(sys.argv) > 2:
    mi = int(sys.argv[2])
else:
    mi = 0

# Read data
(x, y, gmatrix) = ld.readGuidance (logdirname)

# Plot guidance...
shp = np.shape(gmatrix)
print ('gmatrix shape: {0}'.format(shp))

print ('basename: {0}'.format(os.path.basename(logdirname)))
winwidth = 12
winheight = 11
if os.path.basename(logdirname) == '52N2M_thalguide_fgfdup':
    winwidth = 22
    winheight = 14.3
pl = pt.RDPlot (winwidth, winheight)
pl.fs = 16
pl.fs2 = 24
pl.showAxes = False
pl.showNames = False
if mi==0:
    pl.cmap = plt.cm.Blues
else:
    pl.cmap = plt.cm.Reds

f1 = pl.surface (gmatrix[:,mi], x, y)

# Put saving into the class?
mapname = '{0}_guide{1}.png'.format(os.path.basename(logdirname), mi)
plt.savefig (mapname, dpi=300, transparent=True)

plt.show()
