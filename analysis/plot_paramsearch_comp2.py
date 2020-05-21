#
# A script to plot heatmaps from the table generated by
# process_paramsearch.py. This uses code in include/plotparam.py. It
# plots heatmaps for several quality metrics (honda, sos differences,
# area differences) of the pattern at a given simulation timepoint for
# all of the 180 different combinations of the epsilon, alphabeta and
# D parameters in the model (alphabeta is alpha/beta). It can also
# plots maps of the actual patterns which give rise to the quality
# metrics, so that the pattern can be eyeballed alongside the
# heatmaps. This is very useful in evaluating how well the metrics
# represent the 'goodness' of the pattern.
#

# To access argv and also include the include dir
import sys
sys.path.insert (0, './include')
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import paramplot as pp

# Set plotting defaults
matplotlib.use('TkAgg') # cleaner likely to work
fnt = {'family' : 'DejaVu Sans', 'weight' : 'regular', 'size' : 12 }
matplotlib.rc('font', **fnt)

#
# Load Data
#

# Cols in sdata are: k,D,alphabeta,alpha,beta,epsilon,t,hondadelta,sos_dist,area_diff
sdata = np.genfromtxt ('postproc/paramsearch_k3_comp2.csv', delimiter=",", names=True)
# sdata is a numpy 'structured array' with named fields.

#
# Plot Data
#

# All D and ab possible values:
D_vals = [ 0.01, 0.0251, 0.0631, 0.1585, 0.3981, 1.0 ]
ab_vals = [ 0.01, 0.0631, 0.3981, 2.51189, 15.849, 100.0 ]

compute_param_tuples = 1
if compute_param_tuples:

    # Lets have a little function to set up param_tuples automatically.

    # Set the centre box parameters
    F = 0.01    # doesn't change
    _ab = 0.3981 # then 0.3981 #2.51189# 0.3981   # centre ab - vary with row
    _D = 0.0631  # centre D - vary with col

    ab_idx = ab_vals.index(_ab)
    D_idx = D_vals.index(_D)

    print ('ab_idx = {0}, D_idx = {1}'.format (ab_idx, D_idx))

    # Init param_tuples
    param_tuples = []
    for i in range (0, 9):
        param_tuples.append ((0.0, 0.0, 0.0))

    for r in range(0,3):
        ab_idx_ = (ab_idx + r - 1) if ((ab_idx + r - 1) >= 0) else len(ab_vals)-1
        _ab = ab_vals[ab_idx_]
        for c in range(0,3):
            D_idx_ = (D_idx + c - 1) if ((D_idx + c - 1) >= 0) else len(D_vals)-1
            print('D_idx_: {0}'.format(D_idx_ ))
            _D = D_vals[D_idx_]
            param_tuples[r*3+c] = (F, _ab, _D)

    print ('param_tuples: {0}'.format (param_tuples))
else:
    # Manually set the list
    # F, ab, D
    #param_tuples = [ (1, 0.3981, 0.3981) ]
    param_tuples = [ (10, 15.849, 1) ]

# Set the timepoint for which we'll plot
timepoint = 25000

# Make a filename
if param_tuples:
    fileend = 't{0}_F{1}_ab{2}_D{3}'.format(timepoint,param_tuples[0][0],param_tuples[0][1],param_tuples[0][2])
else:
    fileend = 't{0}'.format(timepoint)

F1 = plt.figure (figsize=(20,12))
#                        col        x    y            k  t
pp.paramplot (sdata, F1, 'F', 'D', 'alphabeta', 3, timepoint, param_tuples);
plt.savefig('plots/comp2_{0}_heatmaps.png'.format(fileend))

# Optional map plots:
#F2 = plt.figure (figsize=(20,12))
#pp.mapplot (F2, timepoint, param_tuples, True)
#plt.savefig('plots/comp2_{0}_patterns.png'.format(fileend))

plt.show()
exit (0)
