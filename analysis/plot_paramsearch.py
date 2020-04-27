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
import paramplot

# Set plotting defaults
#matplotlib.use('TkAgg') # cleaner likely to work
#matplotlib.use('Qt5Agg') # Ugly, sometimes default
matplotlib.use('TkCairo') # Install pycairo to be able to use this
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
##F2 = plt.figure (figsize=(20,12))
##F3 = plt.figure (figsize=(20,12))
#                               col          x            y
paramplot.paramplot (sdata, F1, 'epsilon',   'D',         'alphabeta');
##paramplot.paramplot (sdata, F2, 'D',         'alphabeta', 'epsilon');
##paramplot.paramplot (sdata, F3, 'alphabeta', 'epsilon',   'D');

plt.show()
exit (0)
