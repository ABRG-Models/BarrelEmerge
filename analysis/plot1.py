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

# Set plotting defaults
fs = 12
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
[t1, hondadelta, edgedev, numdoms, domarea, domcentres] = ld.readDirichData (logdirname)

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
F1 = plt.figure (figsize=(8,8))

ax1 = F1.add_subplot(1,1,1)
l1, = ax1.plot(t1, hondadelta, 'o-', label='Honda Delta')
l2, = ax1.plot(t1, edgedev, 'o-', label='Edge deviation')
l3, = ax1.plot(t1, domarea/totalarea[0], 'go-', label='Domain area proportion')
l5, = ax1.plot(t1, s_resid, 's-', label='Summed residuals to vert. line fits')
l6, = ax1.plot(t1, gfits, '*-', label='inv. verticality (0:vertical)')
l7, = ax1.plot(t1, s_resid_h, 's-', label='Summed residuals to horz. line fits')
l8, = ax1.plot(t1, gfits_h, '*-', label='inv. horz (0:horz)')
ax1.set_title ('Shape analysis');

ax2 = F1.add_subplot(1,1,1, sharex=ax1, frameon=False)
l4, = ax2.plot(t1, numdoms, 'ro-', label='Number of domains')
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax2.set_ylabel ('Num doms')

plt.legend((l1, l2, l3, l4, l5, l6, l7, l8), ('Honda Delta','Edge deviation','Domain area prop.','Number of doms', 'Summed resid.', 'inv. vert.', 'Summed resid (h).', 'inv. horz.'), loc='right')

plt.show()
