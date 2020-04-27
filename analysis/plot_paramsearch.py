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
from mpl_toolkits.axes_grid1 import AxesGrid
import sebcolour
col = sebcolour.Colour

# Set plotting defaults
fs = 12
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

F1 = plt.figure (figsize=(18,12))

# Cols in sdata are: k,D,alphabeta,alpha,beta,epsilon,t,hondadelta,sos_dist,area_diff
sdata = np.genfromtxt ('postproc/paramsearch_k3_dncomp.csv', delimiter=",", names=True)
# sdata is a 'structured array'

# Get max/min for data ranges
sos_max = max(sdata[:]['sos_dist'])
sos_min = min(sdata[:]['sos_dist'])
print ('sos max/min: {0}/{1}'.format (sos_max, sos_min))
area_max = max(sdata[:]['area_diff'])
area_min = min(sdata[:]['area_diff'])
honda_max = max(sdata[:]['hondadelta'])
honda_min = min(sdata[:]['hondadelta'])

# Extent of the data range for plotting
plot_extent = [-0.5, 5.5, -0.5, 5.5]

ttarg = 15000
# Plot heatmaps where we extract rows where epsilon = 100, t = 25000
# Can cycle through epsilon and t.
i = 1
for epstarg in [50, 100, 150, 200, 300]:

    mapdat = sdata[np.logical_and(sdata[:]['epsilon'] == epstarg,
                                  sdata[:]['t'] == ttarg)]

    # Now sort mapdat on cols of interest
    mapdat = np.sort (mapdat, order=('alphabeta','D'))

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
    #print (ab6x6)

    #print (hond6x6)
    # This shows hondadelta ordered by alphabeta on y and D on x
    ax = F1.add_subplot(3,5,i)
    #nonnan = ~np.isnan(hond6x6)
    #h = hond6x6[nonnan]
    #print (h)
    # NB: An alternative to imshow() is pcolor()
    im = ax.imshow (hond6x6, cmap='hot', vmin=honda_min, vmax=honda_max,
                    extent=plot_extent, interpolation='none')
    tlist = []
    for j in range(0,6): tlist.append('{0:.2f}'.format(D6x6[0,j]))
    plt.xticks ([0,1,2,3,4,5], tlist)
    tlist = ['']
    for j in range(0,5): tlist.append('{0:.1f}'.format(ab6x6[j,0]))
    # Special for 100:
    tlist.append('{0:d}'.format(int(ab6x6[5,0])))
    plt.yticks ([-0.5,0,1,2,3,4,5], tlist)
    if epstarg == 50:
        ax.set_ylabel('alphabeta : honda')
    ax.set_title('$\epsilon$={0}'.format(epstarg))
#    if epstarg == 300:
#        F1.colorbar(im, ax=ax)
    ax.set_xlabel('D')

    ax1 = F1.add_subplot(3,5,5+i)
    im1 = ax1.imshow (sos6x6, cmap='plasma', vmin=sos_min, vmax=sos_max,
                    extent=plot_extent, interpolation='nearest')
    tlist = []
    for j in range(0,6): tlist.append('{0:.2f}'.format(D6x6[0,j]))
    plt.xticks ([0,1,2,3,4,5], tlist)
    tlist = ['']
    for j in range(0,5): tlist.append('{0:.1f}'.format(ab6x6[j,0]))
    # Special for 100:
    tlist.append('{0:d}'.format(int(ab6x6[5,0])))
    plt.yticks ([-0.5,0,1,2,3,4,5], tlist)
    if epstarg == 50:
        ax1.set_ylabel('alphabeta : sos')
#    if epstarg == 300:
#        F1.colorbar(im1, ax=ax1)
    ax1.set_xlabel('D')

    ax2 = F1.add_subplot(3,5,10+i)
    im2 = ax2.imshow (area6x6, cmap='hot', vmin=area_min, vmax=area_max,
                    extent=plot_extent, interpolation='nearest')
    tlist = []
    for j in range(0,6): tlist.append('{0:.2f}'.format(D6x6[0,j]))
    plt.xticks ([0,1,2,3,4,5], tlist)
    tlist = ['']
    for j in range(0,5): tlist.append('{0:.1f}'.format(ab6x6[j,0]))
    # Special for 100:
    tlist.append('{0:d}'.format(int(ab6x6[5,0])))
    plt.yticks ([-0.5,0,1,2,3,4,5], tlist)
    if epstarg == 50:
        ax2.set_ylabel('alphabeta : areadiff')
#    if epstarg == 300:
#        F1.colorbar(im2, ax=ax2)
    ax2.set_xlabel('D')

    i += 1

# Deal with colorbars here. Manual fiddling to get position correct
cb_height = 0.151
cb_wid = 0.01
cb_xpos = 0.92
cb_ax = F1.add_axes([cb_xpos, 0.692, cb_wid, cb_height])
cbar = F1.colorbar (im, cax=cb_ax)

cb_ax1 = F1.add_axes([cb_xpos, 0.42, cb_wid, cb_height])
cbar1 = F1.colorbar (im1, cax=cb_ax1)

cb_ax2 = F1.add_axes([cb_xpos, 0.148, cb_wid, cb_height])
cbar2 = F1.colorbar (im2, cax=cb_ax2)


plt.show()
exit (0)
