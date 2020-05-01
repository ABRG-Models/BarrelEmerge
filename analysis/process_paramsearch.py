#
# A script to extract results from the parameter search HDF5 files and
# write a csv table as output. The csv table is then used in
# plot_paramsearch.py
#

# To access argv and also include the include dir
import sys
import os
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
#import domcentres as dc
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
#
# This needs modifying to use the data in $HOME/paramexplore. There
# are 180 directories for each of the 4 full runs.
#
# Timepoints are 1, 5000, 10000, 15000, 20000, 25000
#
# Filename format is like: pe_dncomp_D0.0631_ep300_ab0.01_k3
basedir = '/home/seb/gdrive_usfd/data/BarrelEmerge/paramexplore/'
table = []
for logdirname in os.listdir(basedir):

    logdirname = basedir + logdirname
    print ('Log dir: {0}'.format(logdirname))
    if 'comp2' in logdirname:
        print ('comp2, omit')
        continue

    print ('dncomp file; PROCESS')

    # Load the dirichlet data, domcentres, etc
    bdo = bd.BarrelData()
    bdo.loadAnalaysisData = True
    bdo.loadPositions = False # required for totalarea
    bdo.loadGuidance = False
    bdo.loadSimData = False
    bdo.loadDivisions = False
    bdo.load (logdirname)

    # The ID colour maps
    do_maps = 0
    if do_maps:
        # Read the data
        for tg in range(0,23,4):
            idstring = 'id{0}'.format(tg*1000);
            f1 = pt.surface (bdo.id_c[:,tg], bdo.x, bdo.y, 0, idstring)
            # Plot centroids:
            f1.plot (bdo.domcentres[tg][:,0], bdo.domcentres[tg][:,1], 'o')

    #vert = True
    #horz = False
    #gfits, s_resid = dc.domcentres_analyse (bdo.domcentres, vert)
    #gfits_h, s_resid_h = dc.domcentres_analyse (bdo.domcentres, horz)

    #print ('total area: {0}'.format (bdo.totalarea))

    # Clean zeros out of honda delta and sos_distances and make a mask
    hondadelta = np.ma.masked_equal (bdo.honda, 0)
    sos_dist =  np.ma.masked_equal (bdo.sos_dist, 0)
    mask_combined = np.invert(hondadelta.mask | sos_dist.mask)
    # Apply the mask to the time:
    t1_masked = bdo.t_steps[mask_combined].T
    #print ('t1_masked: {0}'.format (t1_masked))
    t1 = t1_masked[:,0]
    #print ('t1: {0}'.format (t1))
    mapdiff = bdo.mapdiff[mask_combined].T
    area_diff = bdo.area_diff[mask_combined].T
    area_diff = area_diff / np.max(area_diff)

    #print ('t shape {0}, t1_masked shape {1}'.format(np.shape(bdo.t),np.shape(t1_masked)))
    # Remove the masked values:
    #print ('t: {0}'.format (bdo.t)) # real t in seconds
    sos_dist = sos_dist.compressed()
    hondadelta = hondadelta.compressed()
    print ('hondadelta: {0}'.format (hondadelta))
    print ('sos_dist shape: {0}, area_diff shape: {1}'.format (np.shape (sos_dist), np.shape (area_diff[:,0])))
    print ('sos_dist: {0}, area_diff: {1}'.format (sos_dist, area_diff))

    # So here, I have t, honda, sos at 6 time points

    # Whatabout k, D, alpha, beta, alpha/beta and epsilon?
    print ('k={0}, D={1}, alpha={2}, beta={3}, alphabeta={4}, epsilon={5}'.format(bdo.k, bdo.D, bdo.meanalpha, bdo.meanbeta, (bdo.meanalpha/20.0), bdo.meanepsilon))

    # So, for each line in hondadeta/t/sos_dist, we can output a line of the table.
    for hd in range (0, len(hondadelta)):
        tableline = [bdo.k, bdo.D, (bdo.meanalpha/20.0), bdo.meanalpha, bdo.meanbeta, bdo.meanepsilon, t1[hd], hondadelta[hd], sos_dist[hd], area_diff[hd,0]]
        table.append (tableline)

import csv
with open(('paramsearch_k{0}.csv'.format(bdo.k)), 'w', newline='\n') as csvfile:
    cw = csv.writer (csvfile, delimiter=',')
    cw.writerow (['k','D','alphabeta','alpha','beta','epsilon','t','hondadelta','sos_dist','area_diff'])
    for tableline in table:
        cw.writerow (tableline)
