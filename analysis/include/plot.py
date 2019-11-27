#
# A small library of plotting functions for the RD systems
#
# In fact, this needs to be a class, with members such as overall
# width, height etc.
#

import numpy as np
import matplotlib
matplotlib.use ('TKAgg', warn=False, force=True)
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class RDPlot:

    # Note: Can't have multiple __init__ overloads.
    def __init__ (self, width, height):
        # Overall figure width and height
        self.width = width
        self.height = height

    # Member attributes

    # Should the axes be shown or not?
    showAxes = True

    # Flag to show ID names or not, for some methods
    showNames = True

    # If the graph wants a title
    title = ''

    # Default colour map
    cmap = plt.cm.jet

    # Default fontsize
    fs = 12
    # A second fontsize
    fs2 = 20

    def trace (self, dmatrix, ix, t, title):
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : self.fs}
        matplotlib.rc('font', **fnt)
        trace0 = dmatrix[0,ix,:] # c0
        trace1 = dmatrix[1,ix,:] # c1
        F1 = plt.figure (figsize=(self.width,self.height))
        f1 = F1.add_subplot(1,1,1)
        f1.plot (t,trace0)
        f1.plot (t,trace1)
        f1.set_title(title)

    def trace2 (self, nmatrix, ix, t, title):
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : self.fs}
        matplotlib.rc('font', **fnt)
        trace0 = nmatrix[ix,:]
        F1 = plt.figure (figsize=(self.width,self.height))
        f1 = F1.add_subplot(1,1,1)
        f1.plot (t,trace0)
        f1.set_title(title)

    def trace3 (self, a, c, n, ix, t, title):
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : self.fs}
        matplotlib.rc('font', **fnt)
        trace0 = n[ix,:]
        trace1 = a[0,ix,:] # a0
        trace2 = a[1,ix,:] # a1
        trace3 = c[0,ix,:] # c0
        trace4 = c[1,ix,:] # c1
        F1 = plt.figure (figsize=(self.width,self.height))
        f1 = F1.add_subplot(1,1,1)
        f1.plot (t,trace0,marker='o')
        f1.plot (t,trace1,marker='o')
        f1.plot (t,trace2,marker='o')
        f1.plot (t,trace3,marker='o')
        f1.plot (t,trace4,marker='o')
        f1.legend (('n','a0','a1','c0','c1'))
        f1.set_title(title)

    # Plot a 2d scalar function as a colour map
    def surface (self, dmatrix, x, y):
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : self.fs}
        matplotlib.rc('font', **fnt)

        F1 = plt.figure (figsize=(self.width, self.height))
        f1 = F1.add_subplot(1,1,1)

        if not self.title == "":
            f1.set_title (self.title)
        f1.scatter (x, y, c=dmatrix, marker='h', cmap=self.cmap)

        if self.showAxes == False:
            f1.set_axis_off()

        return f1

    # ...with names (and axes) as an option
    def surface_withnames (self, dmatrix, x, y, ix, title, idnames, domcentres):
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : self.fs}
        matplotlib.rc('font', **fnt)
        F1 = plt.figure (figsize=(self.width,self.height))
        f1 = F1.add_subplot(1,1,1)

        f1.scatter (x, y, c=dmatrix, marker='h', cmap=self.cmap)

        if self.showAxes == False:
            f1.set_axis_off()
        else:
            f1.set_xlabel('x (mm)')
            f1.set_ylabel('y (mm)')

        if self.showNames == True:
            count = 0
            idn_arr = []
            for idn in idnames:
                idn_arr.append(idn)
                print ('{0}'.format(idn))
                count = count + 1
            N = count
            count = 0
            cmap_ = matplotlib.cm.get_cmap('Greys')
            for dc in domcentres:
                print('dc: {0}'.format(dc))

                # Compute a greyscale colour for the text
                cidx = count/N
                clow = 0.2
                cmid = 0.31
                chi = 0.7
                if cidx > clow and cidx < cmid:
                    cidx = clow
                if cidx >= cmid and cidx < chi:
                    cidx = chi
                # Place the text label for the barrel
                if idn_arr[count] == 'a':
                    thechar = r'$\alpha$'
                elif idn_arr[count] == 'b':
                    thechar = r'$\beta$'
                elif idn_arr[count] == 'c':
                    thechar = r'$\gamma$'
                elif idn_arr[count] == 'd':
                    thechar = r'$\delta$'
                else:
                    thechar = idn_arr[count]

                f1.text (dc[0], dc[1], thechar, fontsize=self.fs2, verticalalignment='center', horizontalalignment='center', color=cmap_(cidx))

                count = count + 1

        return f1

    # ...with names, no axes
    def surface_withnames_noaxis (self, dmatrix, x, y, ix, title, idnames, domcentres):
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : self.fs}
        matplotlib.rc('font', **fnt)
        F1 = plt.figure (figsize=(self.width,self.height))
        f1 = F1.add_subplot(1,1,1)
        #f1.set_title(title)
        f1.scatter (x, y, c=dmatrix, marker='h', cmap=self.cmap)

        # no good, contour depends on it being a meshgrid. Have to DIY.
        #print ('dmatrix shape: {0}'.format(np.shape(dmatrix)))
        #f1.contour (x, y, dmatrix, [0.5])

        #f1.set_xlabel('x (mm)')
        #f1.set_ylabel('y (mm)')
        f1.set_axis_off()
        count = 0
        idn_arr = []
        for idn in idnames:
            idn_arr.append(idn)
            print ('{0}'.format(idn))
            count = count + 1
        N = count
        count = 0
        #cmap_ = matplotlib.cm.get_cmap('Greys')
        for dc in domcentres:
            print('dc: {0}'.format(dc))

            # Compute a greyscale colour for the text
            cidx = count/N
            clow = 0.2
            cmid = 0.31
            chi = 0.7
            if cidx > clow and cidx < cmid:
                cidx = clow
            if cidx >= cmid and cidx < chi:
                cidx = chi
            # Place the text label for the barrel
            if idn_arr[count] == 'a':
                thechar = r'$\alpha$'
            elif idn_arr[count] == 'b':
                thechar = r'$\beta$'
            elif idn_arr[count] == 'c':
                thechar = r'$\gamma$'
            elif idn_arr[count] == 'd':
                thechar = r'$\delta$'
            else:
                thechar = idn_arr[count]

            ## This don't work as there are 2 doms, so centroid is wrong for text.
            ##f1.text (dc[0], dc[1], thechar, fontsize=self.fs2, verticalalignment='center', horizontalalignment='center', color=cmap(cidx))

            count = count + 1
        return f1

    # Like surface, but make it a 3d projection
    def surface2 (self, dmatrix, x, y, ix, title):
        fs = 12
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : fs}
        matplotlib.rc('font', **fnt)
        F1 = plt.figure (figsize=(self.width,self.height))
        f1 = F1.add_subplot(1,1,1, projection='3d')
        f1.set_title(title)
        f1.scatter (x, y, dmatrix, c=dmatrix, marker='h', cmap=self.cmap)
        #f1.scatter (x[ix], y[ix], s=32, marker='o', color='k')

    # Plot all the surfaces (c, a, j and n) in a subplot. Save a jpeg so that we can make a movie.
    def surfaces (self, cmatrix, amatrix, jmatrix, nmatrix, x, y, title):
        fs = 12
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : fs}
        matplotlib.rc('font', **fnt)
        N = np.size(cmatrix, 0)
        print ('N={0}'.format(N))
        F1 = plt.figure (figsize=(N*6,N*8))
        for i in range(0,N):
            f1 = F1.add_subplot(3,N,1+i, projection='3d')
            f1.scatter (x, y, cmatrix[i,:], c=cmatrix[i,:], marker='h', cmap=self.cmap)
            f1.set_title('c{0}'.format(i))
            f1.set_zlim(0,1)
            f2 = F1.add_subplot(3,N,N+1+i, projection='3d')
            f2.scatter (x, y, amatrix[i,:], c=amatrix[i,:], marker='h', cmap=self.cmap)
            f2.set_title('a{0}'.format(i))
            f2.set_zlim(0,1)

        # There's only one n
        f3 = F1.add_subplot(3,N,(2*N)+1, projection='3d')
        f3.scatter (x, y, nmatrix, c=nmatrix, marker='h', cmap=self.cmap)
        #f3.scatter (x, y, nmatrix, marker='o')
        f3.set_title('n'.format(i))
        f3.set_zlim(0,1)
