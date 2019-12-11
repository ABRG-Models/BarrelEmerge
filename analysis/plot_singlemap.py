import os
import sys
sys.path.insert (0, './include')
import numpy as np
import matplotlib.pyplot as plt
# Import data loading code:
import BarrelData as bd
# Import my plotting code:
import plot as pt

# Get target x/y hex to show trace for and the time step to show the
# map for from the arguments:
if len(sys.argv) < 2:
    print('Provide logdirname on cmd line please. Optionally provide time index (in sim steps).')
    exit(1)
logdirname = sys.argv[1].rstrip ('/')

# time index
if len(sys.argv) > 2:
    ti = int(sys.argv[2])
else:
    ti = -1

shownames = 0
if len(sys.argv) > 3:
    shownames = int(sys.argv[3])

# Read the data
bdo = bd.BarrelData()
# Set True for inter-lines:
bdo.loadAnalysisData = True
bdo.loadDivisions = True
# If loadGuidance is True, then expt id map will be plotted:
bdo.loadGuidance = True
bdo.loadSimData = True
bdo.loadTimeStep = ti
bdo.load (logdirname)

idstring = 'id{0}'.format(0);
print ('idstring: {0}'.format(idstring))

# Plot one of the matrices:
shp = np.shape(bdo.id_c)
if ti == -1:
    mi = shp[1]-1 # matrix index
else:
    mi = 0
print ('mi = {0}'.format(mi))

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
if bdo.loadAnalysisData == False or bdo.loadDivisions == False:
    f1 = pl.surface_withnames (bdo.id_c[:,mi], bdo.x, bdo.y, 0, idstring, bdo.idnames, bdo.domcentres[mi,:,:])
else:
    f1 = pl.surface_withnames_andboundaries (bdo.id_c[:,mi], bdo.x, bdo.y, 0, idstring, bdo.idnames, bdo.domcentres[mi,:,:], bdo.domdivision[mi])

mapname = 'plots/{0}_{1}_sim.png'.format(os.path.basename(logdirname), ti)
plt.savefig (mapname, dpi=300, transparent=True)

if bdo.loadGuidance == True:
    # Remove exptmatrix entries with -1, and corresponding x,y:
    exptmatrix = np.ma.masked_equal (bdo.expt_id, -1.0)
    mask_combined = np.invert(exptmatrix.mask)
    # Apply the mask to x/y vectors
    x = bdo.x[mask_combined].T
    y = bdo.y[mask_combined].T

    f2 = pl.surface_withnames (exptmatrix.compressed(), x, y, 0, idstring, bdo.idnames, bdo.domcentres[mi,:,:])

    mapname = 'plots/{0}_{1}_expt.png'.format(os.path.basename(logdirname), ti)
    plt.savefig (mapname, dpi=300, transparent=True)

plt.show()
