import os
import sys
sys.path.insert (0, './include')
import numpy as np
import matplotlib.pyplot as plt
# Import data loading code:
import BarrelData as bd
# Import my plotting code:
import plot as pt
import sebcolour as sc

def content():
    # Get target x/y hex to show trace for and the time step to show the
    # map for from the arguments:
    if len(sys.argv) < 3:
        print('Provide logdirname and time index (in sim steps) on cmd line.')
        exit(1)
    logdirname = sys.argv[1].rstrip ('/')
    print ('basename: {0}'.format(os.path.basename(logdirname)))
    # time index
    ti = int(sys.argv[2])

    # Read the data
    bdo = bd.BarrelData()
    # Set True for inter-lines:
    bdo.loadAnalysisData = True
    bdo.loadDivisions = False
    # If loadGuidance is True, then expt id map will be plotted:
    bdo.loadGuidance = False
    bdo.loadSimData = True
    bdo.loadTimeStep = ti
    bdo.loadHexFlags = True
    bdo.load (logdirname)

    # Compute max of c
    maxc = np.max (bdo.c, axis=0)

    # Either use the precomputed ID map:
    c_id = bdo.id_c[:,0]
    # or compute it here:
    # c_id_int = np.argmax (bdo.c, axis=0)
    # c_id = c_id_int[:,0].astype(np.float32) / np.float32(bdo.N)

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
    if ti < 5000:
        sf.showScalebar = True
    else:
        sf.showScalebar = False
    sf.showAxes = False
    sf.sb1 = [-1.3, -0.9]
    sf.sb2 = [-0.3, -0.9]
    sf.sbtext = ''
    sf.sbtpos = [-1.1, -1.1]
    sf.sblw = 5
    sf.sbfs = 48
    if ti > 12000:
        sf.showNames = True
    else:
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

    # Add two contours, for different levels of localization
    #sf.addContour (maxc[:,0], 0.8, 'white', 1.0);
    #sf.addContour (maxc[:,0], 0.4, 'grey', 1.6);

    # Or single contour for each field
    for ii in range(0,bdo.N):
        c = bdo.c[ii,:,0]
        sf.addContour (c, 0.5, 'white', 1.0, ii, False);

    sf.addOuterBoundary()

    mapname = 'plots/{0}_c_id_{1:06d}.png'.format(os.path.basename(logdirname), ti)
    plt.savefig (mapname, dpi=300, transparent=True)

    plt.show()

# Allows another py script to import this script and run it.
if __name__ == '__main__':
    content()
