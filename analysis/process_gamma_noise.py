#
# Process sensitivity analysis results gained from varying the noise applied to
# the gamma interaction parameters
#

import sys
import os
sys.path.insert (0, './include')
import numpy as np
import BarrelData as bd
import h5py
import math

basedir = '/home/seb/gdrive_usfd/data/BarrelEmerge/gamma_noise/'
# Sensitivity analysis carried out for t=30000
tpoint = 30000

table = []
for logdirname in os.listdir(basedir):
    print ('Log dir: {0}'.format(logdirname))

    spts = logdirname.split('_')
    ff_gain = 0
    for pt in spts:
        if 'gain' in pt:
            ff_gain = float(pt.rsplit ('gain', 1)[-1])
    logdirname = basedir + logdirname

    # Load the dirichlet data, domcentres, etc
    bdo = bd.BarrelData()
    bdo.loadAnalaysisData = True
    bdo.loadPositions = False # required for totalarea
    bdo.loadGuidance = True # For adjacency
    bdo.loadHexFlags = True # also for adjacency
    bdo.loadSimData = True # Need sim data to do any analysis of the c values, e.g. max me - max others.
    bdo.loadDivisions = False
    try:
        print ('Loading {0}'.format(logdirname))
        bdo.load (logdirname)

        # Clean zeros out of honda delta and sos_distances and make a mask
        hondadelta = np.ma.masked_equal (bdo.honda, 0)
        sos_dist =  np.ma.masked_equal (bdo.sos_dist, 0)
        mask_combined = np.invert(hondadelta.mask | sos_dist.mask)
        t1_masked = bdo.t_steps[mask_combined].T
        t1 = t1_masked[:,0]
        mapdiff = bdo.mapdiff[mask_combined].T
        area_diff = bdo.area_diff[mask_combined].T
        sos_dist = np.sqrt(sos_dist.compressed()/bdo.N)
        hondadelta = hondadelta.compressed()
        bdo.computeLocalization()
        bdo.computeAdjacencyMeasure()
        # Eta is a combined measure
        eta = area_diff[0,0] * bdo.mean_adjacency_differencemag[0] / bdo.mean_adjacency_arrangement[0]

        tableline = [ff_gain, hondadelta[0], sos_dist[0], area_diff[0,0], bdo.locn_vs_t[0], eta]
        table.append (tableline)
    except:
        print ('Failed to load BarrelData object')
        tableline = [ff_gain, math.nan, math.nan, math.nan, math.nan, math.nan]
        table.append (tableline)

import csv
with open('postproc/gamma_noise.csv', 'w', newline='\n') as csvfile:
    cw = csv.writer (csvfile, delimiter=',')
    cw.writerow (['noise_gain','hondadelta','sos_dist','area_diff','localization','eta'])
    for tableline in table:
        cw.writerow (tableline)
