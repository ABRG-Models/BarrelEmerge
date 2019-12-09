# Read barreloids_vanderloos_dia_only.csv and graph, along with
# labels. Output 4 sets of gammas assuming two orthogonal signals.

import numpy as np
import matplotlib
matplotlib.use ('TKAgg', warn=False, force=True)
import matplotlib.pyplot as plt

# First load data
import csv

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

mx = -1.0
my = -1.0
labels = []
xar = []
yar = []

# gmax/gmin delimit the ranges that I want for the guidance
# gradient interactions. I'll compute this so that four guidance
# gradients are made use of in the cortex.
gmax = 2.0
gmin = 0.0

with open('whiskers_vanderloos.csv') as csvDataFile:
    csvReader = csv.reader (csvDataFile)

    # Run through and find max x and max y, and read x, y and label
    # into python lists
    for row in csvReader:
        if row[0] == 'x': continue # skip header
        x = float(row[0])
        y = float(row[1])
        xar.append(x)
        yar.append(y)
        labels.append(row[2])
        if x > mx: mx = x
        if y > my: my = y

    for i in range(0,len(xar)):
        x = xar[i]
        y = yar[i]
        lbl = labels[i]
        # compute g1 to g4
        g1 = x*(gmax/mx)
        g2 = (mx-x)*(gmax/mx)
        g3 = y*(gmax/my)
        g4 = (my-y)*(gmax/my)
        # stick in a np array
        ar = np.array((x,y,g1,g2,g3,g4))
        # stick array in a dictionary keyed by lbl
        D[lbl] = ar

# Output the text for the config file
for d in D:
    print ('{{ "alpha" : {0}, "beta" : {1}, "epsilon" : {2}, "xinit" : {3},   "yinit" : {4}, "sigmainit" : {5}, "gaininit" : {6}, "gamma" : [{7}, {8}, {9}, {10}] }}, // {11}'.format(alpha, beta, epsilon, xinit, yinit, sigmainit, gaininit, D[d][2], D[d][3], D[d][4], D[d][5], d))

# Draw a scatter graph
fs = 16
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)
matplotlib.rcParams['text.usetex'] = True

F0 = plt.figure (figsize=(9,7))
ax0 = F0.add_subplot (1, 1, 1)
#ax0.set_xlim([0.0, 0.43])
#ax0.set_ylim([0.03, 0.48])

text_xoff = 0.05
text_yoff = -0.2

g1qui = np.array([])
g2qui = np.array([])
g3qui = np.array([])
g4qui = np.array([])
xqui = np.array([])
yqui = np.array([])
for d in D:
    if d == 'a':
        ax0.text (D[d][0]+text_xoff, D[d][1]+text_yoff, '$\\alpha$')
    elif d == 'b':
        ax0.text (D[d][0]+text_xoff, D[d][1]+text_yoff, '$\\beta$')
    elif d == 'c':
        ax0.text (D[d][0]+text_xoff, D[d][1]+text_yoff, '$\\gamma$')
    elif d == 'd':
        ax0.text (D[d][0]+text_xoff, D[d][1]+text_yoff, '$\\delta$')
    else:
        ax0.text (D[d][0]+text_xoff, D[d][1]+text_yoff, '$\\mathsf{{ {0} }}$'.format(d))
    # Build lists for quiver plots
    g1qui = np.append(g1qui, D[d][2])
    g2qui = np.append(g2qui, D[d][3])
    g3qui = np.append(g3qui, D[d][4])
    g4qui = np.append(g4qui, D[d][5])
    xqui = np.append(xqui, D[d][0])
    yqui = np.append(yqui, D[d][1])

show_four = 1
sm = 12 # scalemult

offset_arrows = 0
if offset_arrows:
    if show_four:
        ax0.quiver (xqui-(g1qui*0.25)/(gmax*sm), yqui+0.02, g1qui, 0, color='r', width=0.003, scale=gmax*sm)
        ax0.quiver (xqui+(g2qui*0.25)/(gmax*sm), yqui+0.03, -g2qui, 0, color='m', width=0.003, scale=gmax*sm)
        ax0.quiver (xqui-0.01, yqui-(g3qui*0.25)/(gmax*sm)-0.0, 0, g3qui, color='b', width=0.003, scale=gmax*sm)
        ax0.quiver (xqui-0.02, yqui+(g4qui*0.25)/(gmax*sm)-0.0, 0, -g4qui, color='c', width=0.003, scale=gmax*sm)
    else:
        ax0.quiver (xqui, yqui, g1qui-g2qui, g3qui-g4qui, color='k', width=0.003)

    ax0.scatter (xqui, yqui, c='k', s=120, marker='o')

else:
    ax0.quiver (xqui, yqui, g1qui, 0, color='r', width=0.003, scale=gmax*sm)
    ax0.quiver (xqui, yqui, -g2qui, 0, color='m', width=0.003, scale=gmax*sm)
    ax0.quiver (xqui, yqui, 0, g3qui, color='b', width=0.003, scale=gmax*sm)
    ax0.quiver (xqui, yqui, 0, -g4qui, color='c', width=0.003, scale=gmax*sm)

    ax0.scatter (xqui, yqui, c='k', s=70, marker='o')

ax0.set_xlabel('Posterior to anterior axis [mm]')
ax0.set_ylabel('Lateral to medial axis [mm]')

F0.tight_layout()

plt.savefig ('whiskers_vanderloos_graph.png')

plt.show();
