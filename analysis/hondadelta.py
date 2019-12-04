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

# Load the dirichlet data, domcentres, etc
[t1, hondadelta, edgedev, numdoms, domarea, domcentres, dirichcentre, sos_dist, mapdiff, area_diff] = ld.readDirichData (logdirname)

# Timestep is 0.0001
dt = 0.0001
t1 = t1 * dt

# The ID colour maps
do_maps = 0
if do_maps:
    # Read the data
    (x, y, t, cmatrix, amatrix, nmatrix, idmatrix, tarea) = ld.readSimDataFiles (logdirname)
    for tg in range(0,23,4):
        idstring = 'id{0}'.format(tg*1000);
        f1 = pt.surface (idmatrix[:,tg], x, y, 0, idstring)
        # Plot centroids:
        f1.plot (domcentres[tg][:,0], domcentres[tg][:,1], 'o')

vert = True
horz = False
gfits, s_resid = dc.domcentres_analyse (domcentres, vert)
gfits_h, s_resid_h = dc.domcentres_analyse (domcentres, horz)

pf = h5py.File(logdirname+'/positions.h5', 'r')
totalarea = np.array(pf['area']);
print ('total area: {0}'.format (totalarea))

# And plot this longhand here:
F1 = plt.figure (figsize=(9,8))

# Clean zeros out of honda delta and sos_distances
hondadelta = np.ma.masked_equal (hondadelta, 0)
sos_dist =  np.ma.masked_equal (sos_dist, 0)
mask_combined = np.invert(hondadelta.mask | sos_dist.mask)
#print ('mask {0}'.format(mask_combined))
# Apply the mask to the time:
t1_masked = t1[mask_combined].T
mapdiff = mapdiff[mask_combined].T
area_diff = area_diff[mask_combined].T
area_diff = area_diff / np.max(area_diff)

print ('t1 shape {0}, t1_masked shape {1}'.format(np.shape(t1),np.shape(t1_masked)))
# Remove the masked values:

sos_dist = sos_dist.compressed()
hondadelta = hondadelta.compressed()

print ('sos_dist shape: {0}, area_diff shape: {1}'.format (np.shape (sos_dist), np.shape (area_diff[:,0])))

xmax = max(t1_masked)
xmax = xmax[0]
print ('xmax = {0}'.format(xmax))
ax1 = F1.add_subplot(1,1,1)
l1, = ax1.plot(t1_masked, hondadelta, 'o', markersize=12, color=col.black, label='Honda $\delta$')
l2, = ax1.plot((0,xmax), (0.003, 0.003), '--', color=col.black, linewidth=3, label="threshold")

ax2 = ax1.twinx()
l3, = ax2.plot(t1_masked, sos_dist, 's', markersize=12, color=col.blue, label='$\Sigma d^2$')
l4, = ax2.plot(t1_masked, mapdiff, 'v', markersize=12, color=col.red, label='mapdiff')

l5, = ax2.plot(t1_masked, area_diff[:,0]*sos_dist, '^', markersize=12, color=col.green, label='area_diff * sos_dist')

sos_min = np.min(sos_dist)
sos_end = sos_dist[-1]

# Objective is the value 1-sos_min/sos_end, which tends to 0 as the
# pattern is as good at the end as it is at the "best" point, possibly
# multiplied by the honda delta value at the end of the simulation,
# and possibly multiplied by the minimum of the pattern.
obj1 = (1. - sos_min/sos_end)
obj2 = (1. - sos_min/sos_end) * np.min(sos_dist)
obj3 = (1. - sos_min/sos_end) * np.min(sos_dist) * hondadelta[-1]

print ('obj1: {0}, obj2: {1}, obj3: {2}'.format (obj1,obj2,obj3))

#l2, = ax1.plot(t1, edgedev, 'o', label='Edge deviation')
#l3, = ax1.plot(t1, domarea/totalarea[0], 'go', label='Domain area proportion')
#l5, = ax1.plot(t1, s_resid, 's', label='Summed residuals to vert. line fits')
#l7, = ax1.plot(t1, s_resid_h, 's', label='Summed residuals to horz. line fits')
#ax1.set_title ('Honda Dirichletiform measure');
ax1.set_xlabel ('Simulation time')
ax1.set_ylabel ('Honda $\delta$ measure')
ax2.set_ylabel ('$\Sigma d^2$')
ax2.tick_params (axis='y', labelcolor=col.blue)
ax1.set_xlim ((0,xmax))
ax1.set_ylim ((0,0.25))
ax2.set_ylim ((0,5))
ax1.set_xticks ((0,0.5*xmax,xmax))
#plt.legend()

#ax2 = F1.add_subplot(1,1,1, sharex=ax1, frameon=False)
#l4, = ax2.plot(t1, numdoms, 'ro', label='Number of domains')
#ax2.yaxis.tick_right()
#ax2.yaxis.set_label_position("right")
#ax2.set_ylabel ('Num doms')
#plt.legend((l1, l2, l3, l4), ('Honda Delta','Edge deviation','Domain area prop.','Number of doms'), loc='right')

plt.tight_layout()

plt.savefig('hondadelta.svg', transparent=True)

plt.show()
