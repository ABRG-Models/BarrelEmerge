# Extract barrel areas, area diffs and honda deltas for experiment in which the
# C row whiskers' epsilons were reduced from its original value of 1.2.
#

import sys
import os
sys.path.insert (0, './include')
import numpy as np
import BarrelData as bd
import h5py
import math

# analysis carried out for t=30000
tpoint = 30000

# Two tables, one for overall metrics, one for individual measures
table = []
table_ind = []

basedir = '../logs/whisker_rowtrim/'

# The epsilon for the unmodified barrels in the sim
epsilon = 1.2

for logdirname in os.listdir(basedir):
    print ('Log dir: {0}'.format(logdirname))

    # Get the epsilon multiplier for row C from the filename
    eps_mult = float(logdirname.rsplit ('_', 1)[-1])
    print ('epsilon multiplier is {0}'.format (eps_mult))

    eps_modified = eps_mult * epsilon

    logdirname = basedir + logdirname
    print ('logdirname is now {0}'.format (logdirname))

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

    # Construct the data that we want, for each value of eps_mult
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
    eta = area_diff[0,0] * bdo.mean_adjacency_differencemag[0] / bdo.mean_adjacency_arrangement[0]

    tableline = [eps_mult, epsilon, eps_modified, hondadelta[0], sos_dist[0], area_diff[0,0], bdo.locn_vs_t[0], eta]
    table.append (tableline)

    # Now the individual data. Trimmed row C3, so barrels of interest are: c,  C1, C2, C3, C4, C5, C6, C7, C8, C9
    #                                                          TC indices: 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
    print ('AA honda_delta_j: {0}'.format(bdo.honda_delta_j[0]))
    print ('AA area_diffs: {0}'.format(bdo.area_diffs))
    print ('AA barrel_areas: {0}'.format(bdo.barrel_areas))
    print ('AA name_by_index: {0}'.format(bdo.name_by_index))
    #
    for i in [10,11,12,13,14,15,16,17,18,19]:
        try:
            hond_dj = bdo.honda_delta_j[0][int(i)]
        except:
            hond_dj = math.nan
        print ('name_by_index: {0}'.format (bdo.name_by_index[i]))
        tableline = [eps_mult, epsilon, eps_modified, bdo.name_by_index[i], i, hond_dj, bdo.area_diffs[int(i)][0], bdo.barrel_areas[int(i)][0]]
        print ('TL: {0}'.format(tableline))
        table_ind.append (tableline)

import csv
with open('postproc/whisker_rowtrim_overall.csv', 'w', newline='\n') as csvfile:
    cw = csv.writer (csvfile, delimiter=',')
    cw.writerow (['eps_mult','epsilon','eps_modified','hondadelta','sos_dist','area_diff','localization','eta'])
    for tableline in table:
        cw.writerow (tableline)
with open('postproc/whisker_rowtrim_individual.csv', 'w', newline='\n') as csvfile:
    cw = csv.writer (csvfile, delimiter=',')
    cw.writerow (['eps_mult','epsilon','eps_modified','barrel','barrel_index','hondadeltaj','area_diff','area'])
    for tableline in table_ind:
        cw.writerow (tableline)
