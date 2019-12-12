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

    #
    # Initialise; set up member attributes (in pythonese, 'instance attributes')
    #
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
        # The colourmap to use when plotting z values vs x,y (i.e., when c is empty)
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
        self.c = np.array([]) # colour array. rgb triplets
        self.id_byname = {}
        self.nhex = 0
        # Set true once figure is set up and ready to be plotted into
        self.ready = False
        # The line width for contour plots...
        self.contourLinewidth = 1.0
        # ...and the colour
        self.contourColour = "white"

    #
    # Associate the important information in the BarrelData object
    # with this Surface object. This involves copying in selected
    # parts of the BarrelData object.
    #
    def associate (self, BarrelDataObject):
        self.hextohex_d = BarrelDataObject.hextohex_d
        self.hexrad = self.hextohex_d/np.sqrt(3)
        self.x = BarrelDataObject.x
        self.y = BarrelDataObject.y
        self.nhex = BarrelDataObject.nhex
        self.id_byname = BarrelDataObject.id_byname
        self.gammaColour_byid = BarrelDataObject.gammaColour_byid
        # FIXME: These are different for different sims and may have variable shape
        #self.domcentres = BarrelDataObject.domcentres
        #self.domdivision = BarrelDataObject.domdivision

    #
    # Initialisation code for the figure onto which the surface will be drawn
    #
    def initFig (self):
        # Create the actual figure.
        fnt = {'family' : 'DejaVu Sans',
               'weight' : 'regular',
               'size'   : self.fs}
        matplotlib.rc ('font', **fnt)
        self.F1 = plt.figure (figsize=(self.width,self.height))
        self.f1 = self.F1.add_subplot (1,1,1)
        self.ready = True

    def resetFig (self):
        #self.F1.clf()
        #self.f1 = self.F1.add_subplot (1,1,1)
        # plt.cla() worked, so perhaps self.F1.cla() would work
        self.f1.cla()

    def addContour (self, contourData, contourLevel, colour="white", width=1.0):
        if contourLevel == 0:
            self.f1.tricontour (self.x, self.y, contourData, linewidths=width, colors=colour)
        else:
            self.f1.tricontour (self.x, self.y, contourData, linewidths=width, colors=colour, levels=[contourLevel])

    #
    # Plot using polygons
    #
    def plotPoly (self):
        if self.ready == False:
            self.initFig()

        # Either: Plot z values using self.cmap...
        if self.c.size == 0:
            for i in range(self.nhex):
                clr = self.cmap(self.z[i])
                ec = clr if self.showHexEdges == False else 'none'
                hex = RegularPolygon((self.x[i], self.y[i]), numVertices=6, radius=self.hexrad,
                                     facecolor=clr, edgecolor=ec)
                self.f1.add_patch (hex)
        else: # ... or plot provided colours
            for i in range(self.nhex):
                ec = self.c[i] if self.showHexEdges == False else 'none'
                hex = RegularPolygon((self.x[i], self.y[i]), numVertices=6, radius=self.hexrad,
                                     facecolor=self.c[i], edgecolor=ec)
                self.f1.add_patch (hex)

        self.f1.axis (np.array ([min(self.x),max(self.x),min(self.y),max(self.y)])*1.0)
        print ('xlim: {0}, ylim: {1}'.format(self.f1.get_xlim(), self.f1.get_ylim()))
        #self.f1.set_aspect (np.diff(self.f1.get_xlim())/np.diff(self.f1.get_ylim()))

        if self.showScalebar == True:
            self.f1.plot ([self.sb1[0],self.sb2[0]], [self.sb1[1],self.sb2[1]], color=self.sbcolour, linewidth=self.sblw)
            self.f1.text (self.sbtpos[0], self.sbtpos[1], self.sbtext, fontsize=self.sbfs)

        if self.showAxes == False:
            self.f1.set_axis_off()
        else:
            self.f1.set_xlabel ('x (mm)')
            self.f1.set_ylabel ('y (mm)')

        if self.showBoundaries == True:
            for bnd1 in self.domdivision:
                for bnd in bnd1:
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

            print ('In Surface. domcentres shape: {0}'.format (self.domcentres))
            for dc in self.domcentres:
                print('dc: {0}'.format(dc))

                # Compute a greyscale colour for the text from the raw index:
                cidx = np.float32(count)/np.float32(N)
                # or using the sum of the rgb values
                cidx = (self.gammaColour_byid[cidx][0] + self.gammaColour_byid[cidx][1] + self.gammaColour_byid[cidx][2]) / 3.0

                # Transfer from background lightness to text colour via a sigmoid:
                cout = 1.0 / ( 1.0 + np.exp(-80.0*(cidx-0.3)));

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

                #print ('cidx for {0} is {1} and cout is {2}'.format (thechar, cidx, cout))
                #print ('dc shape: {0}'.format (np.shape(dc)))
                self.f1.text (dc[0], dc[1], thechar, fontsize=self.fs2, verticalalignment='center', horizontalalignment='center', color=cmap_(cout))

                count = count + 1
