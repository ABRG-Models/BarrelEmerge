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

# Which time step to analyse for
keytime = 22

uds = []
lrs = []
hondadeltas = []
s_resids_v = []
gfits_v = []
s_resids_h = []
gfits_h = []

# Get target x/y hex to show trace for and the time step to show the
# map for from the arguments:
logdirbase = "/home/seb/gdrive_usfd/data/BarrelEmerge/rel_guide_strengths_sq_edge_UD"

do_maps = 1
fcount = 0
if do_maps:
    # Create a figure
    fs = 12
    fnt = {'family' : 'DejaVu Sans',
           'weight' : 'regular',
           'size'   : fs}
    matplotlib.rc('font', **fnt)
    F0 = plt.figure (figsize=(21,18))
    fcount = 0

for ud in np.linspace(0,0.1,11):

    logdirname = "{0}{1:.2f}".format (logdirbase, ud)
    print ('logdirname: {0}'.format(logdirname))

    # Load the dirichlet data, domcentres, etc
    [t1, hondadelta, edgedev, numdoms, domarea, domcentres, ddoms] = ld.readDirichData (logdirname)

    print ('hondadeltas: {0}'.format(hondadelta))

    # The ID colour maps
    if do_maps:
        fcount = fcount + 1
        # Read the data
        (x, y, t, cmatrix, amatrix, nmatrix, idmatrix, tarea) = ld.readSimDataFiles (logdirname)
        # Plot one plot only:
        ax0 = F0.add_subplot (4, 3, fcount)
        ax0.set_title('UD{0:0.1f} / LR{1:0.1f}'.format(ud, 1-ud))
        # Plot regions:
        ax0.scatter (x, y, c=idmatrix[:,keytime], marker='h', cmap=plt.cm.plasma)
        ax0.set_xlim([-1.1,1.1])
        ax0.set_ylim([-0.6,0.6])
        # Plot centroids:
        ax0.plot (domcentres[keytime][:,0], domcentres[keytime][:,1], 'o', color='blue')
        print ('ddoms shape: {0}'.format(np.shape(ddoms)))
        ddoms_sz = np.shape(ddoms)[1]
        for i in range(0,ddoms_sz):
            if ddoms[keytime][i,0] != 0 and ddoms[keytime][i,1] != 0:
                ax0.plot (ddoms[keytime][i,0], ddoms[keytime][i,1], 'o', color='red')
        ax0.set_aspect('equal')


    vert = True
    horz = False
    gfit_v, s_resid_v = dc.domcentres_analyse (domcentres, vert)
    gfit_h, s_resid_h = dc.domcentres_analyse (domcentres, horz)

    pf = h5py.File(logdirname+'/positions.h5', 'r')
    totalarea = np.array(pf['area']);

    # Insert data for time=keytime into overall containers
    hondadeltas.append(hondadelta[keytime])
    s_resids_v.append(s_resid_v[keytime])
    s_resids_h.append(s_resid_h[keytime])
    gfits_v.append(gfit_v[keytime])
    gfits_h.append(gfit_h[keytime])
    uds.append(ud)
    lrs.append(1-ud)

# And plot this longhand here:
F1 = plt.figure (figsize=(8,8))

ax1 = F1.add_subplot(1,1,1)
l1, = ax1.plot(uds, hondadeltas, 'o-', label='Honda Delta')
l2, = ax1.plot(uds, s_resids_v, 's-', label='Summed residuals to vert. line fits')
l3, = ax1.plot(uds, gfits_v, '*-', label='inv. verticality (0:vertical)')
l4, = ax1.plot(uds, s_resids_h, 's-', label='Summed residuals to horz. line fits')
l5, = ax1.plot(uds, gfits_h, '*-', label='inv. horz (0:horz)')
ax1.set_title ('Shape analysis');
ax1.set_ylabel ('Num')
ax1.set_xlabel ('Up-down grad. gain')
#ax1.set_ylim([-0.1, 1.0])

plt.legend((l1, l2, l3, l4, l5), ('Honda Delta', 'Summed resid.', 'inv. vert.', 'Summed resid (h).', 'inv. horz.'), loc='right')

F0.tight_layout()
F1.tight_layout()

plt.show()
