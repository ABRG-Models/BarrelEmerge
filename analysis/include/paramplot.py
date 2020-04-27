import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Plot heatmaps. The parameter 'column_tag' is varied along
# columns of heat maps. 3 rows show 3 differnt metrics for the
# heat maps. x_tag and y_tag define which paramters are displayed
# on x and y axes. ttarg is the timepint for which to
# display. Data is presented in the numpy structured array
# sdata. Plotting is carried out on the pyplot figure F1.
def paramplot (sdata, F1, column_tag, x_tag, y_tag, ttarg):

    show_xy = 0 # for debug
    if show_xy:
        F2 = plt.figure (figsize=(8,4))
    # Get max/min for data ranges
    sos_max = max(sdata[:]['sos_dist'])
    sos_min = min(sdata[:]['sos_dist'])
    print ('sos max/min: {0}/{1}'.format (sos_max, sos_min))
    area_max = max(sdata[:]['area_diff'])
    area_min = min(sdata[:]['area_diff'])
    honda_max = max(sdata[:]['hondadelta'])
    honda_min = min(sdata[:]['hondadelta'])
    # Extent of the data range for plotting
    plot_extent = [-0.5, 5.5, -0.5, 5.5]

    i = 1

    colall = np.sort(np.unique(sdata[:][column_tag]))
    x_all = np.sort(np.unique(sdata[:][x_tag]))
    y_all = np.sort(np.unique(sdata[:][y_tag]))
    print ('x_all: {0}'.format(x_all))

    x_tick_list = list(range(0,len(x_all)))
    y_tick_list = list(range(0,len(y_all)))
    # Not sure why I have to subtract 0.5 from each here...
    y_tick_list = [yt-0.5 for yt in y_tick_list]

    for coltarg in colall:

        mapdat = sdata[np.logical_and(sdata[:][column_tag] == coltarg,
                                      sdata[:]['t'] == ttarg)]

        # Now sort mapdat on cols of interest
        mapdat = np.sort (mapdat, order=(y_tag, x_tag))
        # Need to reshape hond from 36x1 into 6x6
        hond6x6 = mapdat[:]['hondadelta'].reshape((len(y_all), len(x_all)))
        sos6x6 = mapdat[:]['sos_dist'].reshape((len(y_all), len(x_all)))
        area6x6 = mapdat[:]['area_diff'].reshape((len(y_all), len(x_all)))
        # Can heat map these to prove the ordering is sensible:
        x6x6 =  mapdat[:][x_tag].reshape((len(y_all), len(x_all)))
        y6x6 =  mapdat[:][y_tag].reshape((len(y_all), len(x_all)))

        # In separate figure, show the x and y graphs
        if show_xy:
            imax1 = F2.add_subplot(1,2,1)
            axim1 = imax1.imshow (x6x6, cmap='hot',
                                  extent=plot_extent, interpolation='none')
            imax1.set_xlabel(x_tag)
            imax2 = F2.add_subplot(1,2,2)
            axim2 = imax2.imshow (y6x6, cmap='hot',
                                  extent=plot_extent, interpolation='none')
            imax2.set_ylabel(y_tag)
            #plt.show() ## debug

        print ('adding subplot; i={0} len(colall)={1}'.format(i,len(colall)))
        ax = F1.add_subplot(3,len(colall),i)

        im = ax.imshow (hond6x6, cmap='magma_r', vmin=honda_min, vmax=honda_max,
                        extent=plot_extent, interpolation='none')
        tlist = []
        for j in range(0,len(x_all)): tlist.append('{0:.2f}'.format(x6x6[0,j]))
        plt.xticks (x_tick_list, tlist)
        tlist = ['']
        for j in range(0,len(y_all)): tlist.append('{0:.1f}'.format(y6x6[j,0]))
        plt.yticks (y_tick_list, tlist)
        if coltarg == colall[0]:
            ax.set_ylabel('{0} : honda'.format(y_tag))
        ax.set_title('{0}={1:.2f}'.format(column_tag,coltarg))
        ax.set_xlabel(x_tag)

        ax1 = F1.add_subplot(3,len(colall),len(colall)+i)
        im1 = ax1.imshow (sos6x6, cmap='plasma_r', vmin=sos_min, vmax=sos_max,
                        extent=plot_extent, interpolation='nearest')
        tlist = []
        for j in range(0,len(x_all)): tlist.append('{0:.2f}'.format(x6x6[0,j]))
        plt.xticks (x_tick_list, tlist)
        tlist = ['']
        for j in range(0,len(y_all)): tlist.append('{0:.1f}'.format(y6x6[j,0]))
        plt.yticks (y_tick_list, tlist)
        if coltarg == colall[0]:
            ax1.set_ylabel('{0} : sos'.format(y_tag))
        ax1.set_xlabel(x_tag)

        ax2 = F1.add_subplot(3,len(colall),(2*len(colall))+i)
        im2 = ax2.imshow (area6x6, cmap='viridis_r', vmin=area_min, vmax=area_max,
                        extent=plot_extent, interpolation='nearest')
        tlist = []
        for j in range(0,len(x_all)): tlist.append('{0:.2f}'.format(x6x6[0,j]))
        plt.xticks (x_tick_list, tlist)
        tlist = ['']
        for j in range(0,len(y_all)): tlist.append('{0:.1f}'.format(y6x6[j,0]))
        plt.yticks (y_tick_list, tlist)
        if coltarg == colall[0]:
            ax2.set_ylabel('{0} : areadiff'.format(y_tag))
        ax2.set_xlabel(x_tag)

        i += 1

    # Deal with colorbars here. Manual fiddling to get position correct
    cb_height = 0.151
    cb_wid = 0.01
    cb_xpos = 0.92
    cb_ax = F1.add_axes([cb_xpos, 0.692, cb_wid, cb_height])
    cbar = F1.colorbar (im, cax=cb_ax)

    cb_ax1 = F1.add_axes([cb_xpos, 0.42, cb_wid, cb_height])
    cbar1 = F1.colorbar (im1, cax=cb_ax1)

    cb_ax2 = F1.add_axes([cb_xpos, 0.148, cb_wid, cb_height])
    cbar2 = F1.colorbar (im2, cax=cb_ax2)

    F1.suptitle ('time: {0}'.format(ttarg))
