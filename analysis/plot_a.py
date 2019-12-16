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
bdo.loadAnalysisData = False
bdo.loadDivisions = False
# If loadGuidance is True, then expt id map will be plotted:
bdo.loadGuidance = False
bdo.loadSimData = True
bdo.loadTimeStep = ti
bdo.load (logdirname)

#maxa = np.max (bdo.a, axis=0)

# Plot a surface
import Surface as surf
sf = surf.Surface (12, 11)
sf.associate(bdo)

# Plot a single field using a colour map
sf.z = 2.0*bdo.a[0,:,0] # 13 should be barrel/barreloid C4
sf.showScalebar = False
sf.showAxes = False
sf.sb1 = [-1.3, -0.8]
sf.sb2 = [-0.3, -0.8]
sf.sbtext = '1 mm'
sf.sbtpos = [-1.1, -1.1]
sf.sblw = 5
sf.sbfs = 48
sf.showNames = False
sf.showBoundaries = False
sf.cmap = plt.cm.Greys
sf.plotPoly()

mapname = 'plots/{0}_a_{1:06d}.png'.format(os.path.basename(logdirname), ti)
plt.savefig (mapname, dpi=300, transparent=True)
plt.show()
