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
bdo.loadSimData = True # For localization and a
bdo.loadDivisions = False
bdo.load (logdirname)
bdo.computeLocalization() # can then get bdo.locn_vs_t

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
t1_masked = bdo.t_steps[mask_combined].T
mapdiff = bdo.mapdiff[mask_combined].T
area_diff = bdo.area_diff[mask_combined].T
# area_diff makes sense normalized by nhex
area_diff = area_diff / bdo.nhex

# a vs t.
print ('a shape {0}'.format(np.shape(bdo.a)))
# a shape: (i, hex, times).
a_vs_t = np.zeros([np.shape(bdo.a)[0], np.shape(bdo.a)[2]], dtype=float)
c_vs_t = np.zeros([np.shape(bdo.a)[0], np.shape(bdo.a)[2]], dtype=float)
print ('a_vs_t shape {0}'.format(np.shape(a_vs_t)))
# For each i, sum over hexes.
for i in range(0, np.shape(bdo.a)[0]):
    for t in range(0, np.shape(bdo.a)[2]):
        a_vs_t[i,t] = np.sum(bdo.a[i,:,t])
        c_vs_t[i,t] = np.sum(bdo.c[i,:,t])
np.save ('postproc/a_vs_t.npy', a_vs_t)
np.save ('postproc/c_vs_t.npy', c_vs_t)

print ('t shape {0}, t1_masked shape {1}'.format(np.shape(bdo.t),np.shape(t1_masked)))
# Remove the masked values:

sos_dist = sos_dist.compressed()
hondadelta = hondadelta.compressed()

print ('sos_dist shape: {0}, area_diff shape: {1}'.format (np.shape (sos_dist), np.shape (area_diff[:,0])))

# Show graph in 10 k steps
t1_masked = t1_masked / 10000

np.save ('postproc/honda_t.npy', t1_masked)
np.save ('postproc/honda_delta.npy', hondadelta)
np.save ('postproc/area_diff.npy', area_diff)
np.save ('postproc/map_diff.npy', mapdiff)
np.save ('postproc/locn_vs_t.npy', bdo.locn_vs_t)
