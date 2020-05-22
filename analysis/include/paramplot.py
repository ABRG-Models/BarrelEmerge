import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# For plotting with maps, we have to import the data-loading code
import BarrelData as bd
# For boxes:
import matplotlib.patches as patches
import sebcolour as sc

# Plot heatmaps. The parameter 'column_tag' is varied along
# columns of heat maps. 3 rows show 3 different metrics for the
# heat maps. x_tag and y_tag define which parameters are displayed
# on x and y axes. ttarg is the timepoint for which to
# display. Data is presented in the numpy structured array
# sdata. Plotting is carried out on the pyplot figure F1.
#
# If param_tuples is provided as a non-empty list of tuples in the
# format (epsilon, alphabeta, D), then boxes are drawn around the heat
# map blocks corresponding to those parameters. Use this in
# combination with the mapplot() function.
def paramplot (sdata, F, column_tag, x_tag, y_tag, ktarg, ttarg, param_tuples = [], col_trim_front = 0, col_trim_back = 0):

    print ('initial sdata shape: {0}'.format(np.shape (sdata)))

    # Analyse one k at a time
    sdata = sdata[sdata[:]['k'] == ktarg]
    print ('resulting sdata shape: {0}'.format(np.shape (sdata)))

    # param_tuples defines which parameters to plot maps for (with
    # mapplot). param_tuples should be 9 tuples max. Deal with <9, too.
    # tuple order is (epsilon/F,ab,D) regardless of what column_tag,
    # x_tag and y_tag are.

    # The competition parameter may be called F and it may be called epsilon
    if (column_tag == 'F' or x_tag == 'F' or y_tag == 'F'):
        comp_tag = 'F'
        #comp_idx = int(10) # F col is at end
        tup_idx = int(0)
    else:
        comp_tag = 'epsilon'
        #comp_idx = int(0)
        tup_idx = int(0)

    # We'll use a colidx, xidx and yidx into each tuple:
    if column_tag == comp_tag:
        colidx = tup_idx
        if x_tag == 'D':
            xidx = int(2)  # D
            yidx = int(1)  # ab
        else:
            xidx = int(1)  # ab
            yidx = int(2)  # D
    elif column_tag == 'alphabeta':
        colidx = int(1)
        if x_tag == 'D':
            xidx = int(2)  # D
            yidx = tup_idx # F/eps
        else:
            xidx = tup_idx # F/eps
            yidx = int(2)  # D
    elif column_tag == 'D':
        print ('D!!!')
        colidx = int(2)
        if x_tag == 'alphabeta':
            xidx = int(1)  # ab
            yidx = tup_idx # F/eps
        else:
            xidx = tup_idx # F/eps
            yidx = int(1)  # ab

    # Get max/min for data ranges
    sos_max = max(sdata[:]['sos_dist'])
    sos_min = min(sdata[:]['sos_dist'])
    #print ('sos max/min: {0}/{1}'.format (sos_max, sos_min))
    area_max = max(sdata[:]['area_diff'])
    area_min = min(sdata[:]['area_diff'])
    honda_max = max(sdata[:]['hondadelta'])
    honda_min = min(sdata[:]['hondadelta'])
    locn_max = max(sdata[:]['localization'])
    locn_min = min(sdata[:]['localization'])
    # Extent of the data range for plotting
    plot_extent = [-0.5, 5.5, -0.5, 5.5]

    i = 1

    colall = np.sort(np.unique(sdata[:][column_tag]))
    # Trim if necessary:
    for ci in range (0, col_trim_back):
        colall = np.delete (colall, -1)
    for ci in range (0, col_trim_front):
        colall = np.delete (colall, 0)
    print ('column params: {0} type {1}'.format(colall, type(colall)))

    print ('sorting x_all on x_tag: {0}'.format(x_tag))
    x_all = np.sort(np.unique(sdata[:][x_tag]))
    y_all = np.sort(np.unique(sdata[:][y_tag]))
    print ('x params: {0}'.format(x_all))
    print ('y params: {0}'.format(y_all))

    x_tick_list = list(range(0,len(x_all)))
    y_tick_list = list(range(0,len(y_all)))
    # Not sure why I have to subtract 0.5 from each here...
    #y_tick_list = [yt-0.5 for yt in y_tick_list]

    # A colour index, so that boxes are coloured in order
    colour_idx = 1
    boxcmap = matplotlib.cm.get_cmap('Set1') # Set1 has 9 colours

    for coltarg in colall:

        mapdat = sdata[np.logical_and(sdata[:][column_tag] == coltarg,
                                      sdata[:]['t'] == ttarg)]

        #print ('mapdat: {0}'.format(mapdat))
        #print ('{0} is {1}'.format (column_tag, coltarg))
        #print ('hond6x6 will be: {0}'.format(mapdat[:]['hondadelta']))

        # Now sort mapdat on cols of interest
        mapdat = np.sort (mapdat, order=(y_tag, x_tag))
        # Need to reshape hond from 36x1 into 6x6 (these maps are upside down
        # when reshaped, so must be flipped)
        hond6x6 = np.flip(mapdat[:]['hondadelta'].reshape((len(y_all), len(x_all))), axis=0)
        sos6x6 = np.flip(mapdat[:]['sos_dist'].reshape((len(y_all), len(x_all))), axis=0)
        area6x6 = np.flip(mapdat[:]['area_diff'].reshape((len(y_all), len(x_all))), axis=0)
        locn6x6 = np.flip(mapdat[:]['localization'].reshape((len(y_all), len(x_all))), axis=0)
        # Can heat map these to prove the ordering is sensible:
        x6x6 =  mapdat[:][x_tag].reshape((len(y_all), len(x_all)))
        y6x6 =  mapdat[:][y_tag].reshape((len(y_all), len(x_all)))

        # Do we need boxes to show which parameter combinations the
        # maps are drawn for? Is the given parameter on this graph?
        # True if the coltarg is in the param_tuples

        # Check if coltarg == any of param_tuples[:][0]
        param_indices = []
        print ('param_tuples: {0}'.format (param_tuples))
        if param_tuples:
            # In the tuple, we have (F, ab, D) which are at data cols 10, 2, 1.
            if colidx == 10:
                colidx = 0
            elif colidx == 2:
                colidx = 1
            elif colidx == 1:
                colidx = 2
            print ('colidx = {0}'.format (colidx))
            if coltarg in param_tuples[:][colidx]:
                print ('Draw box/boxes for graph in the column {0}={1}'.format(column_tag, coltarg))
                for pt in param_tuples:
                    print ('pt: {0}'.format (pt))
                    if pt[colidx] == coltarg:
                        print ('xidx={0}, yidx={1}'.format(xidx,yidx))
                        print ('Draw box at x={0}, y={1}'.format(pt[xidx],pt[yidx]))
                        # Find index of the param
                        xparam_idx = np.where (np.abs(x_all - pt[xidx]) < 0.000001)
                        yparam_idx = np.where (np.abs(y_all - pt[yidx]) < 0.000001)
                        # print ('list indices for x={0}, y={1} are {2} and {3}'.format(pt[xidx],pt[yidx], xparam_idx[0][0], yparam_idx[0][0]));
                        param_indices.append ((xparam_idx[0][0]-0.5, yparam_idx[0][0]-0.5))


        ax = F.add_subplot(4,len(colall),i)
        im = ax.imshow (hond6x6, cmap='magma_r', vmin=honda_min, vmax=honda_max,
                        extent=plot_extent, interpolation='none')
        tlist = []
        for j in range(0,len(x_all)): tlist.append('{0:.2f}'.format(x6x6[0,j]))
        # print ('Setting x tick list to: {0}->{1}'.format(x_tick_list, tlist))
        plt.xticks (x_tick_list, tlist)
        tlist = []
        for j in range(0,len(y_all)): tlist.append('{0:.2f}'.format(y6x6[j,0]))
        # print ('Setting y tick list to: {0}->{1}'.format(y_tick_list, tlist))
        plt.yticks (y_tick_list, tlist)
        if coltarg == colall[0]:
            ax.set_ylabel ('{0} : honda'.format(y_tag))
        ax.set_title ('{0}={1:.2f}'.format(column_tag,coltarg))
        ax.set_xlabel (x_tag)

        ax1 = F.add_subplot(4,len(colall),len(colall)+i)
        im1 = ax1.imshow (sos6x6, cmap='plasma_r', vmin=sos_min, vmax=sos_max,
                        extent=plot_extent, interpolation='nearest')
        tlist = []
        for j in range(0,len(x_all)): tlist.append('{0:.2f}'.format(x6x6[0,j]))
        plt.xticks (x_tick_list, tlist)
        tlist = []
        for j in range(0,len(y_all)): tlist.append('{0:.2f}'.format(y6x6[j,0]))
        plt.yticks (y_tick_list, tlist)
        if coltarg == colall[0]:
            ax1.set_ylabel('{0} : sos'.format(y_tag))
        ax1.set_xlabel(x_tag)

        ax2 = F.add_subplot(4,len(colall),(2*len(colall))+i)
        im2 = ax2.imshow (area6x6, cmap='viridis_r', vmin=area_min, vmax=area_max,
                        extent=plot_extent, interpolation='nearest')
        tlist = []
        for j in range(0,len(x_all)): tlist.append('{0:.2f}'.format(x6x6[0,j]))
        plt.xticks (x_tick_list, tlist)
        tlist = []
        for j in range(0,len(y_all)): tlist.append('{0:.2f}'.format(y6x6[j,0]))
        plt.yticks (y_tick_list, tlist)
        if coltarg == colall[0]:
            ax2.set_ylabel('{0} : areadiff'.format(y_tag))
        ax2.set_xlabel(x_tag)

        ax3 = F.add_subplot(4,len(colall),(3*len(colall))+i)
        im3 = ax3.imshow (locn6x6, cmap='viridis', vmin=locn_min, vmax=locn_max,
                              extent=plot_extent, interpolation='nearest')
        tlist = []
        for j in range(0,len(x_all)): tlist.append('{0:.2f}'.format(x6x6[0,j]))
        plt.xticks (x_tick_list, tlist)
        tlist = []
        for j in range(0,len(y_all)): tlist.append('{0:.2f}'.format(y6x6[j,0]))
        plt.yticks (y_tick_list, tlist)
        if coltarg == colall[0]:
            ax3.set_ylabel('{0} : locn'.format(y_tag))
        ax3.set_xlabel(x_tag)

        # Draw any boxes
        for pi_ in param_indices:
            rect =  patches.Rectangle (pi_, 1, 1, linewidth=2, edgecolor=boxcmap(colour_idx/9), facecolor='none')
            rect1 = patches.Rectangle (pi_, 1, 1, linewidth=2, edgecolor=boxcmap(colour_idx/9), facecolor='none')
            rect2 = patches.Rectangle (pi_, 1, 1, linewidth=2, edgecolor=boxcmap(colour_idx/9), facecolor='none')
            rect3 = patches.Rectangle (pi_, 1, 1, linewidth=2, edgecolor=boxcmap(colour_idx/9), facecolor='none')
            ax.add_patch(rect)
            ax1.add_patch(rect1)
            ax2.add_patch(rect2)
            ax3.add_patch(rect3)
            colour_idx += 1

        i += 1

    # Deal with colorbars here. Manual fiddling to get position correct
    cb_height = 0.151
    cb_wid = 0.01
    cb_xpos = 0.92
    cb_ax = F.add_axes([cb_xpos, 0.72, cb_wid, cb_height])
    cbar = F.colorbar (im, cax=cb_ax)

    cb_ax1 = F.add_axes([cb_xpos, 0.52, cb_wid, cb_height])
    cbar1 = F.colorbar (im1, cax=cb_ax1)

    cb_ax2 = F.add_axes([cb_xpos, 0.32, cb_wid, cb_height])
    cbar2 = F.colorbar (im2, cax=cb_ax2)

    cb_ax3 = F.add_axes([cb_xpos, 0.12, cb_wid, cb_height])
    cbar3 = F.colorbar (im3, cax=cb_ax3)

    F.suptitle ('time: {0}'.format(ttarg))

#
# Draw simulation barrel maps for the given parameters and time point
#
def mapplot (F, ttarg, param_tuples, comp2=False):

    #
    # Having drawn the heat maps (and identifier boxes) can now draw
    # the maps themselves on F
    #
    # Read the data
    #

    plotiter = 1
    for _pt in param_tuples:
        print ('tuple: {0}'.format(_pt))
        ep__ = _pt[0]
        ab__ = _pt[1]
        D__ = _pt[2]
        print ('F/epsilon: {0} alphabeta: {1} D: {2}'.format(ep__,ab__,D__))

        # Annoyingly, have to do a lookup here for the text strings,
        # to exactly match the format in which they were saved by the
        # c++ simulation.
        if abs(D__ - 0.01) < 0.000001:
            D_str = '0.01'
        elif abs(D__ - 0.0251) < 0.000001:
            D_str = '0.0251'
        elif abs(D__ - 0.0631) < 0.000001:
            D_str = '0.0631'
        elif abs(D__ - 0.1585) < 0.000001:
            D_str = '0.1585'
        elif abs(D__ - 0.3981) < 0.000001:
            D_str = '0.3981'
        elif abs(D__ - 1) < 0.000001:
            D_str = '1.0'
        elif abs(D__ - 0.03) < 0.000001:
            D_str = '0.03'
        elif abs(D__ - 0.06) < 0.000001:
            D_str = '0.06'
        elif abs(D__ - .12) < 0.000001:
            D_str = '0.12'
        elif abs(D__ - .25) < 0.000001:
            D_str = '0.25'
        elif abs(D__ - 0.5) < 0.000001:
            D_str = '0.5'
        elif abs(D__ - 1.0) < 0.000001:
            D_str = '1.0'
        else:
            D_str = 'unknown'

        if abs(ab__ - 0.01) < 0.000001:
            ab_str = '0.01'
        elif abs(ab__ - 0.0631) < 0.000001:
            ab_str = '0.0631'
        elif abs(ab__ - 0.3981) < 0.000001:
            ab_str = '0.3981'
        elif abs(ab__ - 2.51189) < 0.000001:
            ab_str = '2.51189'
        elif abs(ab__ - 15.849) < 0.000001:
            ab_str = '15.849'
        elif abs(ab__ - 100) < 0.000001:
            ab_str = '100'
#ab_vals = [ 0.06, 0.18, 0.55, 1.6, 5.0, 15 ]
        elif abs(ab__ - 0.06) < 0.000001:
            ab_str = '0.06'
        elif abs(ab__ - 0.18) < 0.000001:
            ab_str = '0.18'
        elif abs(ab__ - .55) < 0.000001:
            ab_str = '0.55'
        elif abs(ab__ - 1.6) < 0.000001:
            ab_str = '1.6'
        elif abs(ab__ - 5.0) < 0.000001:
            ab_str = '5.0'
        elif abs(ab__ - 15) < 0.000001:
            ab_str = '15.0'
        else:
            ab_str = 'unknown'

        F_str = 'unknown'
        if comp2 == True:
            if abs(ep__ - 0.01) < 0.000001:
                F_str = '0.01'
            elif abs(ep__ - 0.1) < 0.000001:
                F_str = '0.1'
            elif abs(ep__ - 1) < 0.000001:
                F_str = '1'
            elif abs(ep__ - 10) < 0.000001:
                F_str = '10'
            elif abs(ep__ - 100) < 0.000001:
                F_str = '100'
#F_vals = [ 0.03, 0.08, 0.19, 0.48, 1.2, 3.0 ]
            elif abs(ep__ - 0.03) < 0.000001:
                F_str = '0.03'
            elif abs(ep__ - 0.08) < 0.000001:
                F_str = '0.08'
            elif abs(ep__ - 0.19) < 0.000001:
                F_str = '0.19'
            elif abs(ep__ - 0.48) < 0.000001:
                F_str = '0.48'
            elif abs(ep__ - 1.2) < 0.000001:
                F_str = '1.2'
            elif abs(ep__ - 3.0) < 0.000001:
                F_str = '3.0'

        if comp2 == True:
            logdirname = '/home/seb/gdrive_usfd/data/BarrelEmerge/paramexplore/pe_comp2_D{0}_F{1}_ab{2}_k3'.format (D_str, F_str, ab_str)
        else:
            logdirname = '/home/seb/gdrive_usfd/data/BarrelEmerge/paramexplore/pe_dncomp_D{0}_ep{1:d}_ab{2}_k3'.format (D_str, ep__, ab_str)

        bdo = bd.BarrelData()
        # Set True for inter-lines:
        bdo.loadAnalysisData = True
        bdo.loadDivisions = False
        # If loadGuidance is True, then expt id map will be plotted:
        bdo.loadGuidance = False
        bdo.loadSimData = True
        bdo.loadTimeStep = ttarg
        bdo.loadHexFlags = True
        try:
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
            sf.showScalebar = False
            sf.showAxes = False
            sf.fs = 12
            sf.fs2 = 14
            sf.sb1 = [-1.3, -0.9]
            sf.sb2 = [-0.3, -0.9]
            sf.sbtext = ''
            sf.sbtpos = [-1.1, -1.1]
            sf.sblw = 5
            sf.sbfs = 48
            sf.drawid = True # To draw a box or something around the map in an ID colour
            boxcmap = matplotlib.cm.get_cmap('Set1') # Set1 has 9 colours
            sf.idcolour = boxcmap(plotiter/9.0);
            sf.showNames = True
            sf.domcentres = bdo.domcentres[0]
            col = sc.Colour()
            sf.boundarylw = 1.0
            sf.boundaryColour = col.black
            sf.boundaryOuterHexColour = col.gray50
            sf.showBoundaries = True
            if sf.showBoundaries == True:
                sf.domdivision = bdo.domdivision
            # plotiter goes the wrong way to get the maps on the grid
            # looking the same as the boxes on the plot, so fix
            if plotiter < 4:
                plotit = plotiter + 6
            elif plotiter < 7:
                plotit = plotiter
            elif plotiter < 10:
                plotit = plotiter - 6
            else:
                plotit = 1000 # That'll be an error then

            sf.setFig (F, 3, 3, plotit)
            sf.plotPoly()

            # Optional single contour for each field
            if 1:
                for ii in range(0,bdo.N):
                    c = bdo.c[ii,:,0]
                    sf.addContour (c, 0.5, 'white', 1.0, ii, False);

            sf.addOuterBoundary()

        except:
            print ("Failed to load the data; moving on to next...");

        plotiter += 1

    F.suptitle ('time: {0}'.format(ttarg))
