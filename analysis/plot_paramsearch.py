#
# A script to extract results from the parameter search HDF5 files and
# write a csv table as output.
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
#matplotlib.use('Qt5Agg') # Ugly, sometimes default
#matplotlib.use('TkCairo') # Install pycairo to be able to use this
fs = 12
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

#
# Load Data
#

# Cols in sdata are: k,D,alphabeta,alpha,beta,epsilon,t,hondadelta,sos_dist,area_diff
sdata = np.genfromtxt ('postproc/paramsearch_k3_dncomp.csv', delimiter=",", names=True)
# sdata is a numpy 'structured array' with named fields.

#
# Plot Data
#

F1 = plt.figure (figsize=(20,12))
F2 = plt.figure (figsize=(20,12))
#F3 = plt.figure (figsize=(20,12))

# D and ab values:
# D:   0.01 0.0251 0.0631 0.1585 0.3981 1
# ab:  0.01 0.0631 0.3981 2.51189 15.849 100

timepoint = 25000
# eps, ab, D
param_tuples = [ (150, 0.0631, 0.0251),  (150, 0.0631, 0.0631),  (150, 0.0631, 0.1585),
                 (150, 0.3981, 0.0251),  (150, 0.3981, 0.0631),  (150, 0.3981, 0.1585),
                 (150, 2.51189, 0.0251),  (150, 2.51189, 0.0631),  (150, 2.51189, 0.1585) ]
#                        col          x            y            t
pp.paramplot_withmaps (sdata, F1, 'epsilon',   'D',         'alphabeta', timepoint, F2, param_tuples);

#timepoint = 15000
#pp.paramplot (sdata, F2, 'D',         'alphabeta', 'epsilon', timepoint);
#timepoint = 5000
#pp.paramplot (sdata, F3, 'epsilon', 'D', 'alphabeta', timepoint);

plt.show()
exit (0)
