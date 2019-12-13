# To access argv and also include the include dir
import os
import sys
sys.path.insert (0, './include')
import numpy as np
import BarrelData as bd
import plot as pt
import matplotlib.pyplot as plt

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
bdo.load (logdirname)

print ('basename: {0}'.format(os.path.basename(logdirname)))
winwidth = 20
winheight = 11
if os.path.basename(logdirname) == '52N2M_thalguide_fgfdup':
    winwidth = 22
    winheight = 14.3
pl = pt.RDPlot (winwidth, winheight)
pl.fs = 16
pl.fs2 = 24
pl.showAxes = False
pl.showNames = False

pl.showScalebar = False
pl.sb1 = [-1.3, -0.8]
pl.sb2 = [-0.3, -0.8]
pl.sbtext = '1 mm'
pl.sbtpos = [-1.1, -1.1]
pl.sblw = 5
pl.sbfs = 48

pl.cmap = plt.cm.gray

print ("bdo.g shape: {0}".format (np.shape(bdo.g)))
f1 = pl.surface (bdo.g[:,mi], bdo.x, bdo.y)

mapname = 'plots/{0}_guide_m{1}.png'.format(os.path.basename(logdirname), mi)
plt.savefig (mapname, dpi=300, transparent=True)

plt.show()
