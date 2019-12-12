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
bdo.gammaColourScheme = 'redblue'
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
sf.showNames = False
sf.showBoundaries = False

print ('bdo.a shape: {0}'.format (np.shape(bdo.a)))
for t in range(0,bdo.t_steps.size):

    # Either use the precomputed ID map:
    a_id_int = np.argmax (bdo.a[:,:,t], axis=0)
    #print ('a_id_int shape: {0}'.format (np.shape(a_id_int)))
    a_id = a_id_int.astype(np.float32) / np.float32(bdo.N)

    # Compute the colour map
    colmap = np.zeros([bdo.nhex,3], dtype=float)
    ii = 0
    for oneid in a_id:
        colmap[ii] = bdo.gammaColour_byid[oneid]
        ii = ii + 1

    sf.c = colmap # assign the colour map computed above
    if sf.showNames == True:
        print ('domcentres shape: {0}'.format (np.shape (bdo.domcentres)))
        sf.domcentres = bdo.domcentres[t]
        print ('sf.domcentres shape: {0}'.format (np.shape (sf.domcentres)))
    if sf.showBoundaries == True:
        print ('domdivision shape: {0}'.format (np.shape (bdo.domdivision)))
        sf.domdivision = bdo.domdivision

    sf.plotPoly()

    # A single contour for each field
    for ii in range(0,bdo.N):
        a = bdo.a[ii,:,t]
        a_norm = a/np.max(a)
        sf.addContour (a_norm, 0.7, 'white', 1.0);

    mapname = 'plots/{0}_a_id_{1:06d}.png'.format(os.path.basename(logdirname), t)
    plt.savefig (mapname, dpi=300, transparent=False)
    sf.resetFig()
