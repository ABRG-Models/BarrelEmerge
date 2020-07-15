#
# Process sensitivity analysis results gained from varying the first molecular
# signalling gradient's phi and gain.
#

import sys
import os
sys.path.insert (0, './include')
import numpy as np
import BarrelData as bd
import h5py
import math

# Sensitivity analysis carried out for t=30000
tpoint = 30000

table = []

for br in ['b', 'c', 'd']:

    modified_barrel = '{0}4'.format(br)
    basedir = '../logs/sensitivity_gamma_{0}/'.format(modified_barrel)

    for logdirname in os.listdir(basedir):
        print ('Log dir: {0}'.format(logdirname))

        # Get gamma_i/j from filename.
        spts = logdirname.split('_')
        ff_gamma_i = 0
        ff_gamma_j = 0
        for pt in spts:
            if 'i' in pt:
                ff_gamma_i = float(pt.rsplit ('i', 1)[-1])
            if 'j' in pt:
                ff_gamma_j = float(pt.rsplit ('j', 1)[-1])

        logdirname = basedir + logdirname

        # Load the dirichlet data, domcentres, etc
        bdo = bd.BarrelData()
        bdo.loadTimeStep = tpoint
        bdo.loadAnalaysisData = True
        bdo.loadPositions = False # required for totalarea
        bdo.loadGuidance = True # For adjacency
        bdo.loadHexFlags = True # also for adjacency
        bdo.loadSimData = True # Need sim data to do any analysis of the c values, e.g. max me - max others.
        bdo.loadDivisions = False
        try:
            bdo.load (logdirname)
        except:
            print ('Failed to load BarrelData object')
            exit (1)

        # Construct the data
        hondadelta = np.ma.masked_equal (bdo.honda, 0)
        sos_dist =  np.ma.masked_equal (bdo.sos_dist, 0)
        mask_combined = np.invert(hondadelta.mask | sos_dist.mask)
        t1_masked = bdo.t_steps[mask_combined].T
        t1 = t1_masked[:,0]
        mapdiff = bdo.mapdiff[mask_combined].T
        area_diff = bdo.area_diff[mask_combined].T
        area_diff = area_diff / bdo.nhex
        sos_dist = np.sqrt(sos_dist.compressed()/bdo.N)
        hondadelta = hondadelta.compressed()
        bdo.computeLocalization()
        bdo.computeAdjacencyMeasure()

        # Make a data table line for the CSV output
        barrel_id = 0
        if modified_barrel == 'b4':
            barrel_id = 1
        elif modified_barrel == 'c4':
            barrel_id = 2
        elif modified_barrel == 'd4':
            barrel_id = 3
        eta = area_diff[0,0] * bdo.mean_adjacency_differencemag[0] / bdo.mean_adjacency_arrangement[0]
        tableline = [barrel_id, ff_gamma_i, ff_gamma_j, hondadelta[0], sos_dist[0], area_diff[0,0], bdo.locn_vs_t[0], eta]
        table.append (tableline)

import csv
with open('postproc/sensitivity_gammas.csv', 'w', newline='\n') as csvfile:
    cw = csv.writer (csvfile, delimiter=',')
    cw.writerow (['barrel','gamma_i','gamma_j','hondadelta','sos_dist','area_diff','localization','eta'])
    for tableline in table:
        cw.writerow (tableline)
