# To access argv and also include the include dir
import os
import sys
sys.path.insert (0, './include')
import numpy as np
import BarrelData as bd
import h5py
import domcentres as dc

# Constants
vert = True
horz = False

basedir = '/home/seb/gdrive_usfd/data/BarrelEmerge/multirun_comp2/'
t=30000

hondas = []
sos = []
area = []
mapdiffs = []
locns = []
eta = []

for logdirname in os.listdir(basedir):
    print (logdirname)

    # Load the dirichlet data, domcentres, etc
    bdo = bd.BarrelData()
    bdo.loadTimeStep = t
    bdo.loadAnalaysisData = True
    bdo.loadPositions = True # for totalarea
    bdo.loadGuidance = True
    bdo.loadHexFlags = True
    bdo.loadSimData = True # For localization and a
    bdo.loadDivisions = False
    try:
        print ('load')
        bdo.load (basedir+logdirname)
        print ('loaded')
        bdo.computeLocalization() # can then get bdo.locn_vs_t
        bdo.computeAdjacencyMeasure()

        #gfits, s_resid = dc.domcentres_analyse (bdo.domcentres, vert)
        #gfits_h, s_resid_h = dc.domcentres_analyse (bdo.domcentres, horz)

        # I just want the honda delta, the area measure and the omega for t=30000
        print ('bdo.honda: {0}'.format(bdo.honda))
        print ('bdo.sos_dist: {0}'.format(bdo.sos_dist))
        print ('bdo.area_diff: {0}'.format(bdo.area_diff))
        print ('bdo.locn_vs_t: {0}'.format(bdo.locn_vs_t))
        hondas.append(bdo.honda[0])
        sos.append(bdo.sos_dist[0])
        area_diff = bdo.area_diff[0] / bdo.nhex
        area.append(area_diff)

        mapdiffs.append(bdo.mapdiff[0])
        locns.append(bdo.locn_vs_t[0])

        print ('bdo.mean_adjacency_differencemag: {0}'.format(bdo.mean_adjacency_differencemag))
        print ('bdo.mean_adjacency_arrangement: {0}'.format(bdo.mean_adjacency_arrangement))
        adjacency_arrangement = bdo.mean_adjacency_arrangement[0]
        adjacency_differencemag = bdo.mean_adjacency_differencemag[0]
        eta.append(adjacency_differencemag * area_diff / adjacency_arrangement)

    except:
        print ('exception')
        continue

print ('honda: {0} +/- {1}'.format(np.mean(hondas), np.std(hondas)))
print ('sos_dist: {0} +/- {1}'.format(np.mean(sos), np.std(sos)))
print ('area_diff: {0} +/- {1}'.format(np.mean(area), np.std(area)))
print ('eta: {0} +/- {1}'.format(np.mean(eta), np.std(eta)))
print ('map_diff: {0} +/- {1}'.format(np.mean(mapdiffs), np.std(mapdiffs)))
print ('locn: {0} +/- {1}'.format(np.mean(locns), np.std(locns)))
