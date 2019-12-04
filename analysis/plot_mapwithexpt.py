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
    print('Provide logdirname on cmd line please. Optionally provide time index.')
    exit(1)
logdirname = sys.argv[1]

# time index
if len(sys.argv) > 2:
    ti = int(sys.argv[2])
else:
    ti = -1

shownames = 0
if len(sys.argv) > 3:
    shownames = int(sys.argv[3])

# Guidance and expt_barrel_id
(x, y, gmatrix, exptmatrix) = ld.readGuidance (logdirname)

# Read the data
(x, y, t, cmatrix, amatrix, nmatrix, idmatrix, tarea, idnames, domcentres) = ld.readSimDataFiles (logdirname)
#for tg in range(0,4,4):
idstring = 'id{0}'.format(0);
print ('idstring: {0}'.format(idstring))

# Plot one of the matrices:
shp = np.shape(idmatrix)
print ('idmatrix shape: {0}'.format(shp))
if ti == -1:
    ti = shp[1]-1
print ('ti = {0}'.format(ti))

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
if shownames > 0:
    pl.showNames = True

do_scalebar = False
if do_scalebar:
    if os.path.basename(logdirname) == '52N2M_thalguide_fgfdup':
        pl.showScalebar = True
        pl.sb1 = [0, -0.6]
        pl.sb2 = [0.5, -0.6]
        pl.sbtext = '0.5 mm'
        pl.sbtpos = [0.0, -0.8]
        pl.sblw = 5
        pl.sbfs = 48
    else:
        pl.showScalebar = True
        pl.sb1 = [-0.8, -0.8]
        pl.sb2 = [-0.1, -0.8]
        pl.sbtext = '0.7 mm'
        pl.sbtpos = [-0.7, -1]
        pl.sblw = 5
        pl.sbfs = 48

f1 = pl.surface_withnames (idmatrix[:,ti], x, y, 0, idstring, idnames, domcentres[ti,:,:])

# FIXME: Remove exptmatrix entries with -1, and corresponding x,y.
# Clean zeros out of honda delta and sos_distances
exptmatrix = np.ma.masked_equal (exptmatrix, -1.0)
mask_combined = np.invert(exptmatrix.mask)
# Apply the mask to the time:
x = x[mask_combined].T
y = y[mask_combined].T

f2 = pl.surface_withnames (exptmatrix.compressed(), x, y, 0, idstring, idnames, domcentres[ti,:,:])

# Put saving into the class?
mapname = '{0}_{1}.png'.format(os.path.basename(logdirname), ti)
plt.savefig (mapname, dpi=300, transparent=True)

plt.show()
