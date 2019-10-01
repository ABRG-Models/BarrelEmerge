import numpy as np
# Import data loading code
import load as ld
# Import MY plotting code:
import plot as pt
import matplotlib
import matplotlib.pyplot as plt
# To access argv:
import sys
# Direct HDF5 access
import h5py

#
# Functions
#

# Is @apositiveint a square number?
def is_square(apositiveint):
    x = apositiveint // 2
    seen = set([x])
    while x * x != apositiveint:
        x = (x + (apositiveint // x)) // 2
        if x in seen:
            return False
        seen.add(x)
    return True

# Do a linear fit, returning the square of the gradient and the sum of the residuals
def do_fit (lx, ly):
    A = np.vstack([lx, np.ones(len(lx))]).T
    out = np.linalg.lstsq (A, ly, rcond=None)
    m, c = out[0]
    gradsq = (m*m)
    resid = 0.0
    if out[1].size > 0:
        resid = out[1][0]
    return gradsq, resid

# What does this want to do? Return, for a given timestep (or for every timestep), the average verticalness of the lines of best fit to groups of centres.
def domcentres_analyse (dc, isvert=True):

    sos_gradients = []
    summed_residuals = []
    numt = np.shape(dc)[0]
    N = int(np.shape(dc)[1])
    # is N a square number?
    if is_square(N) == False:
        print ('domcentres_analyse current coded only for square arrays of domains (could be fixed)')
        return sos_gradients, summed_residuals
    n = int(np.sqrt(N))

    tt = 0 # timepoint
    while tt < numt:
        # sum of the square of the gradient for all 5 in a column
        sos_gradient = 0.0
        # The sum of the residuals for 5 linear fits
        sum_resid = 0.0
        if isvert:
            for i in range(0,N,n):
                # Note: Swap around x and y, so that truly vertical lines will come out with m=0 (approx)
                ly = dc[tt,i:n+i,0] # x
                lx = dc[tt,i:n+i,1] # y
                gradsq, resid = do_fit (lx, ly)
                sos_gradient = sos_gradient + gradsq
                sum_resid = sum_resid + resid
        else:
            for i in range(0,n):
                # For n=5; if i=0, indices: 0,5,10,15,20
                #          if i=1, indices: 1,6,11,16,21 etc.
                lx = dc[tt,i:N-n+1+i:n,0] # x
                ly = dc[tt,i:N-n+1+i:n,1] # y
                gradsq, resid = do_fit (lx, ly)
                #print ('gradsq: {0}, resid: {1}'.format(gradsq, resid))
                sos_gradient = sos_gradient + gradsq
                sum_resid = sum_resid + resid

        print ('Sum of squared gradients: {0}, sum of residuals: {1}'.format (sos_gradient, sum_resid))
        # For this time-point, append the sum of the squared gradients
        # - closer to 0 means closer to a perfect, rectangular grid
        sos_gradients.append (sos_gradient)
        # For this time-point, append the sum of the
        # residuals. Smaller means better aligned centroids.
        summed_residuals.append (sum_resid)

        tt = tt + 1

    return sos_gradients, summed_residuals


#
# Script
#

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

# This print seemed to avoid a python bug
print ('domarea: {0}'.format(domarea))

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
gfits, s_resid = domcentres_analyse (domcentres, vert)
gfits_h, s_resid_h = domcentres_analyse (domcentres, horz)

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
