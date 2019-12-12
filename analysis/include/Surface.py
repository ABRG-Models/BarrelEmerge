#
# A class to plot a surface of hexes, with optional contours, dividing
# lines, etc.
#

import numpy as np
import matplotlib
matplotlib.use ('TKAgg', warn=False, force=True)
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

class Surface:

    def __init__ (self, width, height):
        # Overall figure width and height
        self.width = width
        self.height = height
        # Default fontsize
        self.fs = 12
        # A second fontsize
        self.fs2 = 20
        # Should the axes be shown or not?
        self.showAxes = True
        # Flag to show ID names or not
        self.showNames = True
        # Show boundaries between the hexes of different regions?
        self.showBoundaries = False
        # Should it be a 3d projection?
        self.threeDimensions = False
        # If the graph wants a title
        self.title = ''
        # Default colour map
        self.cmap = plt.cm.jet
        # Scale bar parameters
        self.showScalebar = False
        # Scale bar coordinate 1
        self.sb1 = [0,0]
        # Scale bar coordinate 2
        self.sb2 = [1,0]
        # The label text for the scalebar
        self.sbtext = '1 unit'
        # Scale bar position
        self.sbtpos = [0.5, -0.1]
        # Scale bar fontsize
        self.sbfs = 18
        # Scale bar line width
        self.sblw = 4
        # Scale bar colour
        self.sbcolour = 'k'
        # The hex to hex distance between adjacent hexes
        self.hextohex_d = 0.03
        # The hex radius - the distance from the centre to one of the vertices of the hex
        self.hexrad = 0.1
        # Should the hex edges be visible?
        self.showHexEdges = False
        # The data to plot
        self.x = np.array([])
        self.y = np.array([])
        self.z = np.array([]) # For 3-D surface plots
        self.c = np.array([]) # colour. rgb triplets
        self.id_byname = {}
        self.nhex = 0
        # Set true once figure is set up and ready to be plotted into
        self.ready = False
        # The line width for contour plots...
        self.contourLinewidth = 1.0
        # ...and the colour
        self.contourColour = "white"

    # Associate the important information in the BarrelData object.
    def associate (self, BarrelDataObject):
        self.hextohex_d = BarrelDataObject.hextohex_d
        self.hexrad = self.hextohex_d/np.sqrt(3)
        self.x = BarrelDataObject.x
        self.y = BarrelDataObject.y
        self.nhex = BarrelDataObject.nhex
        self.id_byname = BarrelDataObject.id_byname
        self.domcentres = BarrelDataObject.domcentres
        self.domdivision = BarrelDataObject.domdivision

    def initFig (self):
        # Create the actual figure.
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : self.fs}
        matplotlib.rc ('font', **fnt)
        self.F1 = plt.figure (figsize=(self.width,self.height))
        self.f1 = self.F1.add_subplot (1,1,1)
        self.ready = True

    def addContour (self, contourData, contourLevel, colour="white", width=1.0):
        if contourLevel == 0:
            self.f1.tricontour (self.x, self.y, contourData, linewidths=width, colors=colour)
        else:
            self.f1.tricontour (self.x, self.y, contourData, linewidths=width, colors=colour, levels=[contourLevel])

    def plotPoly (self):
        # Plot using polygons
        if self.ready == False:
            self.initFig()

        for i in range(self.nhex):
            ec = self.c[i] if self.showHexEdges == False else 'none'
            hex = RegularPolygon((self.x[i], self.y[i]), numVertices=6, radius=self.hexrad,
                                 facecolor=self.c[i], edgecolor=ec)
            self.f1.add_patch (hex)

        self.f1.axis (np.array ([min(self.x),max(self.x),min(self.y),max(self.y)])*1.0)
        self.f1.set_aspect (np.diff(self.f1.get_xlim())/np.diff(self.f1.get_ylim()))

        if self.showScalebar == True:
            self.f1.plot ([self.sb1[0],self.sb2[0]], [self.sb1[1],self.sb2[1]], color=self.sbcolour, linewidth=self.sblw)
            self.f1.text (self.sbtpos[0], self.sbtpos[1], self.sbtext, fontsize=self.sbfs)

        if self.showAxes == False:
            self.f1.set_axis_off()
        else:
            self.f1.set_xlabel ('x (mm)')
            self.f1.set_ylabel ('y (mm)')

        for bnd1 in self.domdivision:
            #print ('bnd1 shape: {0}'.format(np.shape(bnd1)))
            for bnd in bnd1:
                #print ('bnd: {0}'.format(bnd))
                for bnd0 in bnd:
                    self.f1.plot (bnd0[0,:],bnd0[1,:], color='k', marker='None', linewidth=1)

        if self.showNames == True:
            count = 0
            idn_arr = []
            for idn in self.id_byname:
                idn_arr.append(idn)
                #print ('{0}'.format(idn))
                count = count + 1
            N = count
            count = 0
            cmap_ = matplotlib.cm.get_cmap('Greys')
            for dc in self.domcentres[0]:
                #print('dc: {0}'.format(dc))

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

                self.f1.text (dc[0], dc[1], thechar, fontsize=self.fs2, verticalalignment='center', horizontalalignment='center', color=cmap_(cidx))

                count = count + 1
