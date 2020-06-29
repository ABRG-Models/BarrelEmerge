#
# A script to plot heatmaps from the table generated by
# process_paramsearch_comp2.py. This uses code in include/plotparam.py. It
# plots heatmaps for several quality metrics (honda, sos differences,
# area differences) of the pattern at a given simulation timepoint for
# all of the 180 different combinations of the F, alphabeta and
# D parameters in the model (alphabeta is alpha/beta). It can also
# plots maps of the actual patterns which give rise to the quality
# metrics, so that the pattern can be eyeballed alongside the
# heatmaps. This is very useful in evaluating how well the metrics
# represent the 'goodness' of the pattern.
#
# This version works with the narrowed parameter sweep which the first sweep
# showed was necessary.
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
fnt = {'family' : 'DejaVu Sans', 'weight' : 'regular', 'size' : 10 }
matplotlib.rc('font', **fnt)

#
# Load Data
#

# Cols in sdata are: k,D,alphabeta,alpha,beta,epsilon,t,hondadelta,sos_dist,area_diff
sdata = np.genfromtxt ('postproc/paramsearch_k3.0_comp2_linmax.csv', delimiter=",", names=True)
# sdata is a numpy 'structured array' with named fields.

#
# Plot Data
#

# All D and ab possible values:
D_vals = [ 0.03, 0.06, 0.12, 0.25, 0.5, 1.0 ]
ab_vals = [ 0.06, 0.18, 0.55, 1.6, 5.0, 15 ]
#F_vals = [ 0.03, 0.08, 0.19, 0.48, 1.2, 3.0 ] # 7.5 is next.

compute_param_tuples = 1
if compute_param_tuples:

    # Lets have a little function to set up param_tuples automatically.

    # Set the centre box parameters
    F = 1.2    # doesn't change
    _ab = 0.18 # then 0.3981 #2.51189# 0.3981   # centre ab - vary with row
    _D = 0.5  # centre D - vary with col

    ab_idx = ab_vals.index(_ab)
    D_idx = D_vals.index(_D)

    print ('ab_idx = {0}, D_idx = {1}'.format (ab_idx, D_idx))

    # Init param_tuples
    param_tuples = []
    for i in range (0, 9):
        param_tuples.append ((0.0, 0.0, 0.0))

    # This sets up param_tuples suitable for the 'F in cols' view of the param space
    for r in range(0,3):
        ab_idx_ = (ab_idx + r - 1) if ((ab_idx + r - 1) >= 0) else len(ab_vals)-1
        _ab = ab_vals[ab_idx_]
        for c in range(0,3):
            D_idx_ = (D_idx + c - 1) if ((D_idx + c - 1) >= 0) else len(D_vals)-1
            print('D_idx_: {0}'.format(D_idx_ ))
            _D = D_vals[D_idx_]
            param_tuples[r*3+c] = (F, _ab, _D)

    # Fixme: Can set up alternatives if necessary

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
pp.paramplot (sdata, F1, 'F', 'D', 'alphabeta', 3, timepoint, param_tuples, 0, 0, 'plasma');
plt.savefig('plots/comp2_linmax_{0}_heatmaps_Fcols.png'.format(fileend))

F2 = plt.figure (figsize=(20,12))
pp.paramplot (sdata, F2, 'alphabeta', 'D', 'F', 3, timepoint, param_tuples, 0, 0, 'plasma');
plt.savefig('plots/comp2_linmax_{0}_heatmaps_abcols.png'.format(fileend))

F3 = plt.figure (figsize=(20,12))
pp.paramplot (sdata, F3, 'D', 'alphabeta', 'F', 3, timepoint, param_tuples, 0, 0, 'plasma');
plt.savefig('plots/comp2_linmax_{0}_heatmaps_Dcols.png'.format(fileend))

# Optional map plots:
do_map_plots = 0
if do_map_plots:
    F4 = plt.figure (figsize=(20,12))
    pp.mapplot (F4, timepoint, param_tuples, '/home/seb/paramexplore_comp2_linmax')
    plt.savefig('plots/comp2_linmax_{0}_patterns.png'.format(fileend))

plt.show()
exit (0)