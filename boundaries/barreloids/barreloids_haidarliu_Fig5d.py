# Read barreloids_vanderloos_dia_only.csv and graph, along with
# labels. Output 4 sets of gammas assuming two orthogonal signals.

import numpy as np
import matplotlib
matplotlib.use ('TKAgg', warn=False, force=True)
import matplotlib.pyplot as plt

from scipy.spatial import Voronoi, voronoi_plot_2d, ConvexHull

# First load data
import csv

import math

# The dictionary of data
D = {}

# Params for the output text
epsilon = 200
alpha = 3
beta = 20
xinit = -0.16
yinit = 0.0
sigmainit = 0.0
gaininit = 1.0

maxx = -1000.0
maxy = -1000.0
minx = 1000.0
miny = 1000.0
labels = []
xar = []
yar = []

# A rotational transformation is applied with this many degrees:
phi = 105
#phi = 0

# Compute cos(phi) and sin(phi)
pr = phi/360.0 * 2.0 * math.pi # "phi in radians"
cosphi = math.cos(pr)
sinphi = math.sin(pr)

# gmax/gmin delimit the ranges that I want for the guidance
# gradient interactions. I'll compute this so that four guidance
# gradients are made use of in the cortex.
gmax = 2.0
gmin = 0.0

with open('barreloids_haidarliu_Fig5d.csv') as csvDataFile:
    csvReader = csv.reader (csvDataFile)

    # First run reads the raw x/y values out and transform them.
    for row in csvReader:
        if row[0] == 'x': continue # skip header
        x = float(row[0])
        y = float(row[1])
        # Transform here:
        x_ = x * cosphi - y * sinphi
        y_ = y * cosphi + x * sinphi
        xar.append(x_)
        yar.append(y_)
        labels.append(row[2])

    # Run through and find max x and max y,
    for i in range(0,len(xar)):
        if xar[i] > maxx: maxx = xar[i]
        if yar[i] > maxy: maxy = yar[i]
        if xar[i] < minx: minx = xar[i]
        if yar[i] < miny: miny = yar[i]

    # Now compute the gradients
    for i in range(0,len(xar)):
        x = xar[i]
        y = yar[i]
        lbl = labels[i]
        # compute g1 to g4 - 4 gradients (combine into two later if required)
        #g1 = x*(gmax/maxx)
        #g2 = (maxx-x)*(gmax/maxx)
        #g3 = y*(gmax/maxy)
        #g4 = (maxy-y)*(gmax/maxy)
        gd = (gmax-gmin)/(maxx-minx)
        g1 = gd * (x + maxx - minx)
        x_ = minx - x + maxx
        print ('minx: {0} maxx: {1}, x: {2} x_: {3}'.format (minx, maxx, x, x_))
        g2 = gd * (x_ + maxx - minx)
        gd = (gmax-gmin)/(maxy-miny)
        g3 = gd * (y + maxy - miny)
        y_ = miny - y + maxy
        g4 = gd * (y_ + maxy - miny)

        # stick in a np array
        ar = np.array((x,y,g1,g2,g3,g4,0)) # last entry is for area, filled later
        # stick array in a dictionary keyed by lbl
        D[lbl] = ar

# Read the boundary points
bndry_x = []
bndry_y = []
bndry_idstr = []
with open('barreloids_haidarliu_Fig5d_boundary.csv') as csvDataFile:
    csvReader = csv.reader (csvDataFile)
    for row in csvReader:
        if row[0] == 'op': continue # skip header
        idstr = row[0]
        x = float(row[1])
        y = float(row[2])
        x_ = x * cosphi - y * sinphi
        y_ = y * cosphi + x * sinphi
        bndry_x.append(x_)
        bndry_y.append(y_)
        bndry_idstr.append(idstr)

# Produce guidance interactions for 4 gradients (two opposing pairs, orthogonally
# arranged) or two orthogonal gradients for which interactions will be positive or
# negative.
show_four = 0 # Else show two

# Draw a scatter graph
fs = 24
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)
#matplotlib.rcParams['text.usetex'] = True
F0 = plt.figure (figsize=(15,15))

gw = 6
gs = F0.add_gridspec (gw, gw)

ax0 = F0.add_subplot (gs[:-1,:-1])

#ax_r = F0.add_subplot (gs[:-1,gw-1])
#ax_d = F0.add_subplot (gs[gw-1,:-1])


txt_xoff = 0.003
txt_yoff = -0.015

g1qui = np.array([])
g2qui = np.array([])
g3qui = np.array([])
g4qui = np.array([])
xqui = np.array([])
yqui = np.array([])
omitx = np.array([]) # x and y of 'omit' list
omity = np.array([])
small_size = ["D2","E7","E8","E9","E9","E10","E11","E12","E13","D6","D7","D8","D9","D9","D10","D11","D12","C10","C9","C8","C7","C6"]
omit = ["R1","R2","R3","R4","R5"]
for d in D: # Care, requires that there are no duplicate labels

    # Build lists for quiver plots
    if not d in omit:
        g1qui = np.append(g1qui, D[d][2])
        g2qui = np.append(g2qui, D[d][3])
        g3qui = np.append(g3qui, D[d][4])
        g4qui = np.append(g4qui, D[d][5])
        xqui = np.append(xqui, D[d][0])
        yqui = np.append(yqui, D[d][1])
    else:
        g1qui = np.append(g1qui, 0.0)
        g2qui = np.append(g2qui, 0.0)
        g3qui = np.append(g3qui, 0.0)
        g4qui = np.append(g4qui, 0.0)
        xqui = np.append(xqui, D[d][0])
        yqui = np.append(yqui, D[d][1])
        omitx = np.append(omitx, D[d][0])
        omity = np.append(omity, D[d][1])

    if show_four:
        print ('Fixme')
    else:
        if (g1qui[-1]-g2qui[-1])<0.01:
            algn = 'left'
            if d in small_size:
                txt_xoff = 0.03
            else:
                txt_xoff = 0.03
        else:
            algn = 'right'
            if d in small_size:
                txt_xoff = -0.03
            else:
                txt_xoff = -0.03

    fs_small = 14
    fs_large = 18
    if d == 'a':
        ax0.text (D[d][0]+txt_xoff, D[d][1]+txt_yoff, r'$\alpha$', horizontalalignment=algn, fontsize=fs_large)
    elif d == 'b':
        ax0.text (D[d][0]+txt_xoff, D[d][1]+txt_yoff, r'$\beta$', horizontalalignment=algn, fontsize=fs_large)
    elif d == 'c':
        ax0.text (D[d][0]+txt_xoff, D[d][1]+txt_yoff, r'$\gamma$', horizontalalignment=algn, fontsize=fs_large)
    elif d == 'd':
        ax0.text (D[d][0]+txt_xoff, D[d][1]+txt_yoff, r'$\delta$', horizontalalignment=algn, fontsize=fs_large)
    elif d in small_size:
        ax0.text (D[d][0]+txt_xoff, D[d][1]+txt_yoff, '{0}'.format(d), horizontalalignment=algn, fontsize=fs_small)
    elif d in omit:
        print ('omit {0}'.format(d))
    else:
        ax0.text (D[d][0]+txt_xoff, D[d][1]+txt_yoff, '{0}'.format(d), horizontalalignment=algn, fontsize=fs_large)

sm = 12 # scalemult

if show_four:
    ax0.quiver (xqui, yqui, g1qui, 0, color='r', width=0.003, scale=gmax*sm)
    ax0.quiver (xqui, yqui, -g2qui, 0, color='m', width=0.003, scale=gmax*sm)
    ax0.quiver (xqui, yqui, 0, g3qui, color='b', width=0.003, scale=gmax*sm)
    ax0.quiver (xqui, yqui, 0, -g4qui, color='c', width=0.003, scale=gmax*sm)
else:
    ax0.quiver (xqui, yqui, g1qui-g2qui, 0, color='b', width=0.006, scale=gmax*sm)
    ax0.quiver (xqui, yqui, 0, g3qui-g4qui, color='g', width=0.006, scale=gmax*sm)

# Plot the actual centres:
ax0.scatter (xqui, yqui, c='k', s=70, marker='o')
ax0.scatter (omitx, omity, c='grey', s=70, marker='o')

# Plot boundary
ax0.plot (bndry_x, bndry_y, c='grey', marker='None', linestyle='--', linewidth=2, label='boundary')
# Optionally add labels
#for ii in range(0,len(bndry_x)):
#    ax0.text (bndry_x[ii]+txt_xoff, bndry_y[ii]+txt_yoff, bndry_idstr[ii])

# Plot AP axis. Maybe use pyplot.arrow to make these
ap = np.array(([[-0.04185,-0.0133],[0.3425,0.1232]]))
x__ = ap[:,0] * cosphi - ap[:,1] * sinphi
y__ = ap[:,1] * cosphi + ap[:,0] * sinphi
ap[:,0] = x__
ap[:,1] = y__
ax0.plot (ap[:,0], ap[:,1], c='grey', marker='None', linestyle='-.', linewidth=2)

fs2 = 42
# Anterior
txt1 = [0.15, 1.15]
x__ = txt1[0] * cosphi - txt1[1] * sinphi
y__ = txt1[1] * cosphi + txt1[0] * sinphi
ax0.text (x__,y__,'ant.',fontsize=fs2, horizontalalignment='center', verticalalignment='center')

# Posterior
txt2 = [1.58, 0.8]
x__ = txt2[0] * cosphi - txt2[1] * sinphi
y__ = txt2[1] * cosphi + txt2[0] * sinphi
ax0.text (x__,y__,'post.',fontsize=fs2, horizontalalignment='center', verticalalignment='center')

# Lateral by the stragglers 0.14v-0.1
txt3 = [1.3, 1.75]
x__ = txt3[0] * cosphi - txt3[1] * sinphi
y__ = txt3[1] * cosphi + txt3[0] * sinphi
ax0.text (x__,y__,'lat.',fontsize=fs2, horizontalalignment='center', verticalalignment='center')

# Medial
txt4 = [0.6, 0.4]
x__ = txt4[0] * cosphi - txt4[1] * sinphi
y__ = txt4[1] * cosphi + txt4[0] * sinphi
ax0.text (x__+0.1,y__+0.01,'med.',fontsize=fs2, horizontalalignment='center', verticalalignment='center')

# Plot voronoi
vpts = np.vstack((xqui,yqui)).T
print ('vpts shape: {0}'.format(np.shape(vpts)))

vor = Voronoi (vpts, incremental=True)

# One way to get a "full" voronoi diagram is to add points manually to produce the right vertices.
ar = np.array(([[0.3341, -0.07811], \
                [-0.021,-0.079], \
                [0.065,-0.108], \
                [0.1236, -0.1096], \
                [0.2056, -0.1194], \
                [0.2953, -0.1292], \
                [0.3475, -0.0287], \
                [0.3569, 0.0731], \
                [0.3694, 0.1368], \
                [0.3749, 0.2129], \
                [0.3530, 0.2938], \
                [0.2961, 0.3490], \
                [0.2555, 0.3833], \
                [0.2180, 0.3992], \
                [0.1845, 0.4078], \
                [0.1509, 0.4128], \
                [0.1158, 0.4188], \
                [0.0870, 0.4066], \
                [0.0503, 0.4078], \
                [-0.0092, 0.3773], \
                [-0.0321, 0.3261], \
                [-0.0471, 0.2770], \
                [-0.0513, 0.2565], \
                [-0.0497, 0.2213], \
                [-0.0798, 0.1677], \
                [-0.0878, 0.1246], \
                [-0.0948, 0.0768], \
                [-0.042, -0.0005]]))

# Transform points
x__ = ar[:,0] * cosphi - ar[:,1] * sinphi
y__ = ar[:,1] * cosphi + ar[:,0] * sinphi
ar[:,0] = x__
ar[:,1] = y__

vor.add_points (ar)

vpts2 = vor.points

# A method for finding areas/volumes of the Voronoi regions
def voronoi_volumes (v):
    vol = np.zeros (v.npoints)
    for i, reg_num in enumerate (v.point_region):
        indices = v.regions[reg_num]
        if -1 in indices: # some regions can be opened
            vol[i] = np.inf
        else:
            vol[i] = ConvexHull (v.vertices[indices]).volume
    return vol

txt_xoff = txt_xoff+0.01
areas = voronoi_volumes (vor)
print ('areas shape: {0}'.format(np.shape(areas)))
print ('vpts2 shape: {0}'.format(np.shape(vpts2)))

areas_by_pos = np.vstack ((areas, vpts2.T)).T
print ('areas_by_pos: {0}'.format (areas_by_pos))

# For each barreloid, find nearest position in areas_by_pos and record the area of the
# barreloid's voronoi region in D
areatotal = 0
for d in D:
    x = D[d][0]
    y = D[d][1]
    mindist = 1e8
    abest = np.array([])
    for a in areas_by_pos:
        if np.isinf (a[0]):
            continue
        dist = (x-a[1])*(x-a[1]) + (y-a[2])*(y-a[2])
        if dist < mindist:
            mindist = dist
            abest = a
    if abest.size > 0:
        # Print? (too messy)
        # ax0.text (abest[1], abest[2], abest[0])
        # Store
        D[d][6] = abest[0]
        areatotal = areatotal + abest[0]

meanarea = areatotal / len(D)

# Add the Voronoi boundaries to the diagram
show_voronoi_in_grey = True
if show_voronoi_in_grey:
    voronoi_plot_2d (vor, ax=ax0, show_vertices=False, show_points=False, line_colors='grey', line_width=2, line_alpha=0.05)

xbord = 0.3
ybord = 0.3

ax0.set_xlim([minx-xbord, maxx+xbord])
ax0.set_ylim([miny-ybord, maxy+ybord])
ax0.yaxis.set_ticks_position('both')
ax0.xaxis.set_ticks_position('both')
# Tick labels on top, not bottom:
ax0.xaxis.set_tick_params (labeltop=True,labelbottom=False)

#ax_r.plot ([0,1],[miny,maxy],'-',color='b')
#ax_r.set_xlabel ('Mol. B')
#ax_r.yaxis.tick_right()
#ax_r.yaxis.set_ticks_position('both')
#ax_d.plot ([minx,maxx],[0,1],'-',color='r')
#ax_d.xaxis.set_ticks_position('both')
#ax_d.set_ylabel ('Mol. A')
#ax_d.set_xlim([minx-xbord, maxx+xbord])
#ax_r.set_ylim([miny-ybord, maxy+ybord])

ax0.set_xlabel('Axis 1 [mm]', labelpad=20)
ax0.xaxis.set_label_position('top')
#ax_d.set_xlabel('Axis 1 [mm]', labelpad=20)

ax0.set_ylabel('Axis 2 [mm]')
#ax_r.set_ylabel('Axis 2 [mm]', labelpad=10)
#ax_r.yaxis.set_label_position('right')

# Axes on/off
ax0.set_axis_off()

#F0.subplots_adjust (wspace=0.2, hspace=0.2)

plt.savefig ('barreloids_haidarliu_Fig5d_graph.svg', transparent=True)

# To scale the gain by the area of each barreloid, set to 1
area_to_gain = 0

# Output the text for the config file
omit_from_config = ["E11","D11","R1","R2","R3","R4","R5"]
for d in D:
    gaininit = 1.0
    if area_to_gain:
        gaininit = (D[d][6]/meanarea)
    if d in omit_from_config:
        print ("// Omit {0} as there is no corresponding barrel visible, or it's a rhinal barrel.".format(d))
    else:
        if show_four:
            print ('{{ "alpha" : {0}, "beta" : {1}, "epsilon" : {2}, "xinit" : {3},   "yinit" : {4}, "sigmainit" : {5}, "gaininit" : {6}, "gamma" : [{7}, {8}, {9}, {10}] , "name" : "{11}" }}, // {11}'.format(alpha, beta, epsilon, xinit, yinit, sigmainit, gaininit, D[d][2], D[d][3], D[d][4], D[d][5], d, D[d][6]))
        else:
            print ('{{ "alpha" : {0}, "beta" : {1}, "epsilon" : {2}, "xinit" : {3},   "yinit" : {4}, "sigmainit" : {5}, "gaininit" : {6}, "gamma" : [{7}, {8}], "name" : "{9}" }}, // {9}'.format(alpha, beta, epsilon, xinit, yinit, sigmainit, gaininit, (D[d][2]-D[d][3]), (D[d][4]-D[d][5]), d))


plt.show();
