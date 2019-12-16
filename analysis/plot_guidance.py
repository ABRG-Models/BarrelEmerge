# To access argv and also include the include dir
import os
import sys
sys.path.insert (0, './include')
import numpy as np
import BarrelData as bd
import plot as pt
import matplotlib.pyplot as plt
import sebcolour as sc

# Get target x/y hex to show trace for and the time step to show the
# map for from the arguments:
if len(sys.argv) < 2:
    print('Provide logdirname on cmd line please. Optionally provide molecule index.')
    exit(1)
logdirname = sys.argv[1].rstrip ('/')

# molecule index
if len(sys.argv) > 2:
    mi = int(sys.argv[2])
else:
    mi = 0

# Read the data
bdo = bd.BarrelData()
bdo.loadSimData = False
bdo.loadAnalysisData = False
bdo.loadGuidance = True
bdo.loadPositions = True
bdo.loadHexFlags = True
bdo.load (logdirname)

# Plot a surface
import Surface as surf
sf = surf.Surface (12, 11)
sf.associate(bdo)

sf.z = (bdo.g[:,mi]/3.0)+0.5
sf.cmap = plt.cm.Greys
if mi == 0:
    sf.showScalebar = True
else:
    sf.showScalebar = False

sf.showAxes = False
sf.sb1 = [-1, -1]
sf.sb2 = [0, -1]
sf.sbtext = ''
sf.sbtpos = [-0.45, -1.1]
sf.sblw = 2
sf.sbfs = 48
sf.showNames = False
col = sc.Colour()
sf.boundarylw = 1.0
sf.boundaryColour = col.gray25
sf.boundaryOuterHexColour = col.gray83
sf.showBoundaries = False
sf.plotPoly()
sf.addOuterBoundary()

mapname = 'plots/{0}_guide_m{1}.png'.format(os.path.basename(logdirname), mi)
plt.savefig (mapname, dpi=300, transparent=True)

plt.show()
