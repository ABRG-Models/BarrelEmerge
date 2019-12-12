# To access argv and also include the include dir
import sys
sys.path.insert (0, './include')
import numpy as np
# Import data loading code
#import load as ld
import BarrelData as bd
# Import MY plotting code:
import plot as pt
import matplotlib
import matplotlib.pyplot as plt
# Direct HDF5 access
import h5py
# My domcentres linear fit code:
import domcentres as dc
import sebcolour
col = sebcolour.Colour

# Set plotting defaults
fs = 32
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

# Get target x/y hex to show trace for and the time step to show the
# map for from the arguments:
if len(sys.argv) < 2:
    print('Provide logdirname on cmd line please.')
    exit(1)
logdirname = sys.argv[1]

suffix = ''
if len(sys.argv) > 2:
    suffix = '_{0}'.format(sys.argv[2])

# Load the dirichlet data, domcentres, etc
bdo = bd.BarrelData()
bdo.loadAnalaysisData = True
bdo.loadPositions = True # for totalarea
bdo.loadGuidance = False
bdo.loadSimData = False
bdo.loadDivisions = False
bdo.load (logdirname)

# The ID colour maps
do_maps = 0
if do_maps:
    # Read the data
    for tg in range(0,23,4):
        idstring = 'id{0}'.format(tg*1000);
        f1 = pt.surface (bdo.id_c[:,tg], bdo.x, bdo.y, 0, idstring)
        # Plot centroids:
        f1.plot (bdo.domcentres[tg][:,0], bdo.domcentres[tg][:,1], 'o')

vert = True
horz = False
gfits, s_resid = dc.domcentres_analyse (bdo.domcentres, vert)
gfits_h, s_resid_h = dc.domcentres_analyse (bdo.domcentres, horz)

print ('total area: {0}'.format (bdo.totalarea))

# And plot this longhand here:
F1 = plt.figure (figsize=(9,8))

# Clean zeros out of honda delta and sos_distances
hondadelta = np.ma.masked_equal (bdo.honda, 0)
sos_dist =  np.ma.masked_equal (bdo.sos_dist, 0)
mask_combined = np.invert(hondadelta.mask | sos_dist.mask)
#print ('mask {0}'.format(mask_combined))
# Apply the mask to the time:
t1_masked = bdo.t[mask_combined].T
mapdiff = bdo.mapdiff[mask_combined].T
area_diff = bdo.area_diff[mask_combined].T
area_diff = area_diff / np.max(area_diff)

print ('t shape {0}, t1_masked shape {1}'.format(np.shape(bdo.t),np.shape(t1_masked)))
# Remove the masked values:

sos_dist = sos_dist.compressed()
hondadelta = hondadelta.compressed()

print ('sos_dist shape: {0}, area_diff shape: {1}'.format (np.shape (sos_dist), np.shape (area_diff[:,0])))

xmax = max(t1_masked)
xmax = xmax[0]
print ('xmax = {0}'.format(xmax))
ax1 = F1.add_subplot(1,1,1)
l1, = ax1.plot(t1_masked, hondadelta, 'o', markersize=12, color=col.black, label='Honda $\delta$')
#l2, = ax1.plot((0,xmax), (0.003, 0.003), '-.', color=col.black, linewidth=3, label="excellent (cells)")
# 0.054 is Senft and Woolsey's result for barrels (mouse 0,054, other rodents about 0.055)
l2, = ax1.plot((0,xmax), (0.055, 0.055), '--', color=col.black, linewidth=3, label="good (S&W)")
l3, = ax1.plot((0,xmax), (0.15, 0.15), '-.', color=col.black, linewidth=3, label="awful (non Dirichlet)")

ax2 = ax1.twinx()

area_measure = area_diff[:,0]*sos_dist

#l4, = ax2.plot(t1_masked, sos_dist, '^', markersize=12, color=col.blue)
l4, = ax2.plot(t1_masked, area_measure, 'v', markersize=12, color=col.blue)

sos_min = np.min(sos_dist)
sos_end = sos_dist[-1]

#l5, = ax1.plot(t1, edgedev, 'o', label='Edge deviation')
#l6, = ax1.plot(t1, domarea/totalarea[0], 'go', label='Domain area proportion')
#l7, = ax1.plot(t1, s_resid, 's', label='Summed residuals to vert. line fits')
#l8, = ax1.plot(t1, s_resid_h, 's', label='Summed residuals to horz. line fits')

ax1.set_xlabel ('Simulation time')
ax1.set_ylabel ('Honda $\delta$ measure')
ax2.set_ylabel ('Pattern metric')
ax2.tick_params (axis='y', labelcolor=col.blue)
ax1.set_xlim ((0,xmax))
ax1.set_ylim ((0,0.3))
ax2.set_ylim ((0,500))
ax1.set_xticks ((0,0.5*xmax,xmax))
#plt.legend()

#ax2 = F1.add_subplot(1,1,1, sharex=ax1, frameon=False)
#l4, = ax2.plot(t1, numdoms, 'ro', label='Number of domains')
#ax2.yaxis.tick_right()
#ax2.yaxis.set_label_position("right")
#ax2.set_ylabel ('Num doms')
#plt.legend((l1, l2, l3, l4), ('Honda Delta','Edge deviation','Domain area prop.','Number of doms'), loc='right')

plt.tight_layout()

plt.savefig('plots/hondadelta{0}.svg'.format(suffix), transparent=True)

plt.show()
