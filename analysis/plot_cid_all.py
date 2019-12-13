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
    print('Provide logdirname on cmd line.')
    exit(1)
logdirname = sys.argv[1].rstrip ('/')
print ('basename: {0}'.format(os.path.basename(logdirname)))
# time index
ti = -1

# Read the data
bdo = bd.BarrelData()
# Set True for inter-lines:
bdo.loadAnalysisData = True
bdo.loadDivisions = True
# If loadGuidance is True, then expt id map will be plotted:
bdo.loadGuidance = False
bdo.loadSimData = True
bdo.loadTimeStep = ti
bdo.load (logdirname)

# Plot a surface
import Surface as surf
sf = surf.Surface (12, 11)
sf.associate(bdo)

sf.showScalebar = True
sf.showAxes = False
sf.sb1 = [-1.3, -0.8]
sf.sb2 = [-0.3, -0.8]
sf.sbtext = '1 mm'
sf.sbtpos = [-1.1, -1.1]
sf.sblw = 5
sf.sbfs = 48
sf.showNames = True
sf.showBoundaries = False

for t in range(0,bdo.t_steps.size):

    # Compute max of c
    maxc = np.max (bdo.c[:,:,t], axis=0)

    # Either use the precomputed ID map:
    c_id = bdo.id_c[:,t]

    # Compute the colour map
    colmap = np.zeros([bdo.nhex,3], dtype=float)
    ii = 0
    for oneid in c_id:
        colmap[ii] = bdo.gammaColour_byid[oneid]
        ii = ii + 1

    sf.c = colmap # assign the colour map computed above
    if sf.showNames == True:
        sf.domcentres = bdo.domcentres[t]
    if sf.showBoundaries == True:
        sf.domdivision = bdo.domdivision

    sf.plotPoly()

    # A single contour for each field
    for ii in range(0,bdo.N):
        c = bdo.c[ii,:,t]
        sf.addContour (c, 0.5, 'white', 1.0);

    mapname = 'plots/cid_all/{0}_c_id_{1:06d}.png'.format(os.path.basename(logdirname), t)
    plt.savefig (mapname, dpi=300, transparent=False)
    sf.resetFig()
