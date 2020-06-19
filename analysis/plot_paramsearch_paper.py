#
# Like plot_paramsearch_comp2.py, but tailored to produce the paper's Figure 2.
#

# To access argv and also include the include dir
import sys
sys.path.insert (0, './include')
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import paramplot as pp
# Import data loading code:
import BarrelData as bd
import sebcolour as sc

# Set plotting defaults
matplotlib.use('TkAgg') # cleaner likely to work
fnt = {'family' : 'Arial', 'weight' : 'regular', 'size' : 14 }
matplotlib.rc('font', **fnt)

# IMPORTANT for svg output of text as things that can be edited in inkscape
plt.rcParams['svg.fonttype'] = 'none'

# sdata is a numpy 'structured array' with named fields.
# Cols in sdata are: k,D,alphabeta,alpha,beta,epsilon,t,hondadelta,sos_dist,area_diff
sdata = np.genfromtxt ('postproc/paramsearch_k3.0_comp2.csv', delimiter=",", names=True)

# Manually set the list param_tuples
#                 F,    ab,   D
param_tuples = [ (0.03, 0.06, 0.03), (0.48, 0.18, 0.12), (0.48, 0.18, 1.0) ]

# Set the timepoint for which we'll plot
timepoint = 30000

F1 = plt.figure (figsize=(20,10))
pp.paramplot_pub (sdata, F1, 'alphabeta', 'D', 'F', 3, timepoint, param_tuples, 0, 0, 'inferno');
plt.savefig('plots/paramsweep.svg')

do_maps = 0
if do_maps:
    # map plots to go under the param sweep colour grids
    map_i = 1 # map index
    for pt in param_tuples:

        logdirname = '/home/seb/gdrive_usfd/data/BarrelEmerge/paramexplore_comp2/pe_comp2_D{2}_F{0}_ab{1}_k3'.format (pt[0], pt[1], pt[2])
        print ('Plotting image from log dir {0}'.format(logdirname))
        # Read the data
        bdo = bd.BarrelData()
        # Set True for inter-lines:
        bdo.loadAnalysisData = True
        bdo.loadDivisions = False
        # If loadGuidance is True, then expt id map will be plotted:
        bdo.loadGuidance = False
        bdo.loadSimData = True
        bdo.loadTimeStep = timepoint
        bdo.loadHexFlags = True
        bdo.load (logdirname)
        # Compute max of c
        maxc = np.max (bdo.c, axis=0)
        # Use the precomputed ID map:
        c_id = bdo.id_c[:,0]
        # Compute the colour map
        colmap = np.zeros([bdo.nhex,3], dtype=float)
        ii = 0
        for oneid in c_id:
            colmap[ii] = bdo.gammaColour_byid[oneid]
            ii = ii + 1
        # Plot a surface
        import Surface as surf
        sf = surf.Surface (12, 11)
        sf.associate(bdo)
        sf.c = colmap # assign the colour map computed above
        sf.sb1 = [-1.3, -0.9]
        sf.sb2 = [-0.3, -0.9]
        sf.sbtext = ''
        sf.sbtpos = [-1.1, -1.1]
        sf.sblw = 5
        sf.sbfs = 48
        sf.showNames = False
        sf.domcentres = bdo.domcentres[0]
        col = sc.Colour()
        sf.boundarylw = 1.0
        sf.boundaryColour = col.black
        sf.boundaryOuterHexColour = col.gray50
        sf.showBoundaries = True
        if sf.showBoundaries == True:
            sf.domdivision = bdo.domdivision
        sf.textid = False
        sf.plotPoly()
        # A single contour for each field
        #for ii in range(0,bdo.N):
        #    c = bdo.c[ii,:,0]
        #    sf.addContour (c, 0.5, 'white', 1.0, ii, False);
        # The nice grey outer boundary
        sf.addOuterBoundary()

        mapname = 'plots/paramsweep_map_{0}.png'.format (map_i)
        plt.savefig (mapname, dpi=300, transparent=True)

        map_i += 1
