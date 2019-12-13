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
if len(sys.argv) < 3:
    print('Provide logdirname and time index (in sim steps) on cmd line.')
    exit(1)
logdirname = sys.argv[1].rstrip ('/')
print ('basename: {0}'.format(os.path.basename(logdirname)))
# time index
ti = int(sys.argv[2])

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

# Perhaps put this logic into BarrelData:
#
# Compute the colour map
maxa = np.max (bdo.a, axis=0)
# Find integer TC id of max a for each hex:
a_id_int = np.argmax (bdo.a, axis=0)
# Convert to the equivalent single precision float:
a_id = a_id_int[:,0].astype(np.float32) / np.float32(bdo.N)
# Create a colour map of zeros
colmap = np.zeros([bdo.nhex,3], dtype=float)
# And fill in the colours:
ii = 0
for oneid in a_id:
    colmap[ii] = bdo.gammaColour_byid[oneid]
    ii = ii + 1

# Plot a surface
import Surface as surf
sf = surf.Surface (12, 11)
sf.associate(bdo)

sf.c = colmap # assign the colour map computed above
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
sf.showHexEdges = False
sf.plotPoly()

print ('a shape: {0}'.format(np.shape(bdo.a)))
for ii in range(0,bdo.N):
    a = bdo.a[ii,:,0]
    a_norm = a/np.max(a)
    sf.addContour (a_norm, 0.7, 'white', 1.0);

mapname = 'plots/{0}_a_id_{1:06d}.png'.format(os.path.basename(logdirname), ti)
plt.savefig (mapname, dpi=300, transparent=True)
#plt.show()
