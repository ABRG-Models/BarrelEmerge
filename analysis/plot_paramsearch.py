#
# A script to extract results from the parameter search HDF5 files and
# write a csv table as output.
#

# To access argv and also include the include dir
import sys
import csv
sys.path.insert (0, './include')
import numpy as np
# Import MY plotting code:
import plot as pt
import matplotlib
import matplotlib.pyplot as plt
import sebcolour
col = sebcolour.Colour

# Set plotting defaults
fs = 32
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)
F1 = plt.figure (figsize=(9,8))

# Cols in sdata are: k,D,alphabeta,alpha,beta,epsilon,t,hondadelta,sos_dist,area_diff
sdata = np.genfromtxt ('postproc/paramsearch_k3_dncomp.csv', delimiter=",", names=True)
# sdata is a 'structured array'

ttarg = 25000
# Plot heatmaps where we extract rows where epsilon = 100, t = 25000
# Can cycle through epsilon and t.
i = 1
for epstarg in [50, 100, 150, 200, 300]:

    mapdat = sdata[np.logical_and(sdata[:]['epsilon'] == epstarg,
                                  sdata[:]['t'] == ttarg)]

    # Now sort mapdat on cols of interest
    #print (mapdat)
    print ('sort..')
    mapdat = np.sort (mapdat, order=('alphabeta','D'))

    print ('take logs')
    # Take log of Dcol and abcol as these vary exponentially
    #logD = np.log (mapdat[:]['D'])
    #logab = np.log (mapdat[:]['alphabeta'])
    #mapdat[:]['D'] = logD
    #mapdat[:]['alphabeta'] = logab
    #print (mapdat)

    # Need to reshape hond from 36x1 into 6x6
    hond6x6 = mapdat[:]['hondadelta'].reshape((6, 6))
    sos6x6 = mapdat[:]['sos_dist'].reshape((6, 6))
    area6x6 = mapdat[:]['area_diff'].reshape((6, 6))
    # Can heat map these to prove the ordering is sensible:
    D6x6 =  mapdat[:]['D'].reshape((6, 6))
    ab6x6 =  mapdat[:]['alphabeta'].reshape((6, 6))

    print (hond6x6)
    # This shows hondadelta ordered by alphabeta on y and D on x
    ax = F1.add_subplot(3,5,i)
    ax.imshow(hond6x6, cmap='hot', interpolation='nearest')
    ax1 = F1.add_subplot(3,5,5+i)
    ax1.imshow(sos6x6, cmap='hot', interpolation='nearest')
    ax2 = F1.add_subplot(3,5,10+i)
    ax2.imshow(area6x6, cmap='hot', interpolation='nearest')

    i += 1
plt.show()
exit (0)
