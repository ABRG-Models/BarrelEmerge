#
# Process sensitivity analysis results gained from varying the noise applied to
# the molecular signalling gradients
#

import sys
import os
sys.path.insert (0, './include')
import numpy as np
import BarrelData as bd
import h5py
import math

basedir = '/home/seb/gdrive_usfd/data/BarrelEmerge/guidance_noise/'
# Sensitivity analysis carried out for t=30000
tpoint = 30000

table = []
for logdirname in os.listdir(basedir):
    print ('Log dir: {0}'.format(logdirname))

    spts = logdirname.split('_')
    ff_gain = 0
    ff_sigma = 0
    for pt in spts:
        if 'gain' in pt:
            ff_gain = float(pt.rsplit ('gain', 1)[-1])
        if 'sigma' in pt:
            ff_sigma = float(pt.rsplit ('sigma', 1)[-1])

    logdirname = basedir + logdirname

    # Load the dirichlet data, domcentres, etc
    bdo = bd.BarrelData()
    bdo.loadAnalaysisData = True
    bdo.loadPositions = False # required for totalarea
    bdo.loadGuidance = False
    bdo.loadSimData = True # Need sim data to do any analysis of the c values, e.g. max me - max others.
    bdo.loadDivisions = False
    try:
        print ('Loading {0}'.format(logdirname))
        bdo.load (logdirname)

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
        area_diff = area_diff / bdo.nhex
        sos_dist = np.sqrt(sos_dist.compressed()/bdo.N)
        hondadelta = hondadelta.compressed()
        # Uncomment for debug:
        print ('hondadelta: {0}'.format (hondadelta))
        print ('sos_dist shape: {0}, area_diff shape: {1}'.format (np.shape (sos_dist), np.shape (area_diff[:,0])))
        print ('sos_dist: {0}, area_diff: {1}'.format (sos_dist, area_diff))

        # So here, I have t, honda, sos at 1 time point, providing one table line.
        bdo.computeLocalization()
        print ("Localization vs. t: {0}".format (bdo.locn_vs_t))

        tableline = [ff_gain, ff_sigma, hondadelta[0], sos_dist[0], area_diff[0,0], bdo.locn_vs_t[0]]
        table.append (tableline)
    except:
        print ('Failed to load BarrelData object')
        tableline = [ff_gain, ff_sigma, math.nan, math.nan, math.nan, math.nan]
        table.append (tableline)

import csv
with open('postproc/guidance_noise.csv', 'w', newline='\n') as csvfile:
    cw = csv.writer (csvfile, delimiter=',')
    cw.writerow (['noise_gain','noise_sigma','hondadelta','sos_dist','area_diff','localization'])
    for tableline in table:
        cw.writerow (tableline)
