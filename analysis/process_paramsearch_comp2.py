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
import math

# Set plotting defaults
fs = 32
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

# Process files with these param combinations only:
D_vals = [ 0.03, 0.06, 0.12, 0.25, 0.5, 1.0 ]
ab_vals = [ 0.06, 0.18, 0.55, 1.6, 5.0, 15 ]
F_vals = [ 0.03, 0.08, 0.19, 0.48, 1.2, 3.0 ]
k_vals = [ 3.0 ]

# Get target x/y hex to show trace for and the time step to show the
# map for from the arguments:
#
# This needs modifying to use the data in $HOME/paramexplore. There
# are 180 directories for each of the 4 full runs.
#
# Timepoints are 1, 5000, 10000, 15000, 20000, 25000
#
# Filename format is like: pe_dncomp_D0.0631_ep300_ab0.01_k3
# Filename format is like: pe_comp2_D0.0631_F1_ab0.01_k3
basedir = '/home/seb/gdrive_usfd/data/BarrelEmerge/paramexplore_comp2/'
#basedir = '/home/seb/paramexplore_comp2/'
table = []
for logdirname in os.listdir(basedir):

    print ('Log dir: {0}'.format(logdirname))
    if 'dncomp' in logdirname:
        print ('dncomp, omit')
        continue
    elif 'comp2' in logdirname:
        print ('comp2 file; PROCESS')
    else:
        print ('unknown file; continue')
        continue

    # Process logdir name to get params, in case that run failed (this
    # then allows me to insert a line in the table with NANs for those
    # parameters)
    # pe_comp2_D0.0251_F1_ab15.849_k3
    spts = logdirname.split('_')
    ff_D = 0 # ff for 'From Filename'
    ff_ep = 0
    ff_ab = 0
    ff_a = 0
    ff_b = 0
    ff_F = 0
    ff_k = 0
    for pt in spts:
        #print ('part of string: {0}'.format(pt))
        if 'pe' in pt:
            continue
        if 'comp2' in pt:
            continue
        if 'D' in pt:
            # D0.01
            ff_D = float(pt.rsplit ('D', 1)[-1])
        if 'ep' in pt:
            # epblah
            ff_ep = float(pt.rsplit ('ep', 1)[-1])
        if 'ab' in pt:
            # alphabeta
            ff_ab = float(pt.rsplit ('ab', 1)[-1])
            ff_a = ff_ab * 20
            ff_b = 3.0 / ff_ab
        if 'F' in pt:
            # F
            ff_F = float(pt.rsplit ('F', 1)[-1])
        if 'k' in pt:
            # k
            ff_k = float(pt.rsplit ('k', 1)[-1])

    print ('FF: D{0} ep{1} ab{2} F{3} k{4}'.format (ff_D, ff_ep, ff_ab, ff_F, ff_k))

    if (ff_D in D_vals and ff_F in F_vals and ff_ab in ab_vals and ff_k in k_vals):
        print ("That's a valid set")
    else:
        print ("D={0}, F={1}, ab={2} is NOT part of this process sweep".format(ff_D, ff_F, ff_ab))
        continue


    #if ff_k == 1.0:
    #    print ('Ignoring k=1 for now')
    #    continue;

    logdirname = basedir + logdirname

    # Load the dirichlet data, domcentres, etc
    bdo = bd.BarrelData()
    bdo.loadAnalaysisData = True
    bdo.loadPositions = False # required for totalarea
    bdo.loadGuidance = False
    bdo.loadSimData = True # Need sim data to do any analysis of the c values, e.g. max me - max others.
    bdo.loadDivisions = False
    try:
        bdo.load (logdirname)
    except:
        print ('Failed to load BarrelData object; continue to next')
        # Or maybe add a table line(s) with NANs to aid producing heatmaps and show where the thing failed?
        for tt in [1, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]:
            tableline = [ff_k, ff_D, ff_ab, ff_a, ff_b, ff_ep, tt, math.nan, math.nan, math.nan, ff_F, math.nan]
            table.append (tableline)
        continue

    # Check bdo params match with file name params.
    if bdo.D - ff_D > 0.0001 or bdo.meanalpha - ff_a > 0.0001 or bdo.meanbeta - ff_b > 0.0001:
        # error
        print ('BarrelDataobject params do not match filename params!')
        print ('bdo.D: {0} ff_D: {1}'.format (bdo.D, ff_D))
        print ('bdo.meanalpha: {0} ff_a: {1}'.format (bdo.meanalpha, ff_a))
        print ('bdo.meanbeta: {0} ff_b: {1}'.format (bdo.meanbeta, ff_b))
        exit (1)

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
    # Uncomment for debug:
    #print ('hondadelta: {0}'.format (hondadelta))
    #print ('sos_dist shape: {0}, area_diff shape: {1}'.format (np.shape (sos_dist), np.shape (area_diff[:,0])))
    #print ('sos_dist: {0}, area_diff: {1}'.format (sos_dist, area_diff))

    # So here, I have t, honda, sos at 6 time points

    # Whatabout k, D, alpha, beta, alpha/beta and epsilon?
    print ('k={0}, D={1}, alpha={2}, beta={3}, alphabeta={4}, epsilon={5}, F={6}'.format(bdo.k, bdo.D, bdo.meanalpha, bdo.meanbeta, (bdo.meanalpha/20.0), bdo.meanepsilon, bdo.F))

    # New analysis. For each hex, compute a localization variable which is c[i_max] - sum(c[i!=i_max])
    bdo.computeLocalization()
    print ("Localization vs. t: {0}".format (bdo.locn_vs_t))

    print ('t_steps: {0}'.format(bdo.t_steps))
    # So, for each line in hondadeta/t/sos_dist, we can output a line of the table.
    times = list(bdo.t_steps) #[1, 5000, 10000, 15000, 20000, 25000] # Fill from data?
    for hd in range (0, len(hondadelta)):
        #tableline = [bdo.k, bdo.D, (bdo.meanalpha/20.0), bdo.meanalpha, bdo.meanbeta, bdo.meanepsilon, t1[hd], hondadelta[hd], sos_dist[hd], area_diff[hd,0], bdo.F]
        tableline = [ff_k, ff_D, ff_ab, ff_a, ff_b, ff_ep, t1[hd], hondadelta[hd], sos_dist[hd], area_diff[hd,0], ff_F, bdo.locn_vs_t[hd]]
        # What did this do?
        print ('times: {0}'.format(times))
        print ('t1[hd={0}]: {1}'.format(hd, t1[hd]))
        times.remove (t1[hd])
        table.append (tableline)
    for tt in times:
        # Add nans for missing times
        tableline = [ff_k, ff_D, ff_ab, ff_a, ff_b, ff_ep, tt, math.nan, math.nan, math.nan, ff_F, math.nan]
        table.append (tableline)

import csv
with open(('postproc/paramsearch_k{0}_comp2.csv'.format(k_vals[0])), 'w', newline='\n') as csvfile:
    cw = csv.writer (csvfile, delimiter=',')
    cw.writerow (['k','D','alphabeta','alpha','beta','epsilon','t','hondadelta','sos_dist','area_diff','F','localization'])
    for tableline in table:
        cw.writerow (tableline)
