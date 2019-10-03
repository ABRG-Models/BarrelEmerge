#
# A library of HDF5 data loading routines
#

import numpy as np
from pathlib import Path
import h5py
import re

def readDirichData (logdir):

    # Take off any trailing directory slash
    logdir = logdir.rstrip ('/')
    #print ('logdir: {0}'.format(logdir))
    p = Path(logdir+'/')
    #print ('dir files'.format(p))
    globstr = 'dirich_*.h5'
    files = list(p.glob(globstr))
    files.sort()
    #print ('Files: {0}'.format(files))
    numtimes = len(files)

    # Create the time series to return. Values to be filled in from dirich_*.h5 file names
    t = np.zeros([numtimes], dtype=int)

    # To hold the honda values
    honda = np.zeros([numtimes], dtype=float)
    # To hold the edgedeviation
    edgedev = np.zeros([numtimes], dtype=float)
    # To hold a count of number of domains
    numdoms = np.zeros([numtimes], dtype=float)
    # The area of the grid that is detected Dirichlet domains
    domarea = np.zeros([numtimes], dtype=float)
    # Coordinates of the putative centre of the domain. Need to open first file to get N.
    #print ('h5py open {0}'.format(files[0]))
    f = h5py.File(files[0], 'r')
    N = list(f['N'])[0]
    # Domain centres using centroid method:
    domcentre = np.zeros([numtimes, N, 2], dtype=float)
    # Dirichlet domain putative centres, Honda method:
    dirichcentre = np.zeros([numtimes, N, 2], dtype=float)

    fi = 0
    for filename in files:

        f = h5py.File(filename, 'r')

        #print ('Search {0} with RE pattern {1}'.format(filename, (logdir+'/dirich_(.*).h5')))
        idxsearch = re.search(logdir+'/dirich_(.*).h5', '{0}'.format(filename))
        thetime = int('{0}'.format(idxsearch.group(1)))
        t[fi] = thetime

        # Get the Honda Dirichlet value (the overall value)
        honda[fi] = list(f['honda'])[0]

        # Coordinates, but need to re-cast them so that they have all ids. Or do I do that in the C++?
        dom_id_list = list(f['reg_centroids_id'])
        domcentre[fi, :, 0] = list(f['reg_centroids_x'])
        domcentre[fi, :, 1] = list(f['reg_centroids_y'])
        #print ('x coords: {0}'.format(domcentre[fi, :, 0]))

        # Now process the domains.
        nondomset = set(['honda', 'N', 'reg_centroids_id', 'reg_centroids_x', 'reg_centroids_y', 'reg_centroids_id_all'])
        kset = set(f.keys()) # dom000, dom001, dom002, etc, honda
        domset = kset.difference(nondomset); # Removes 'honda'

        # The number of domains in the pattern at this stage in the simulation
        numdoms[fi] = len(domset)

        edgedev[fi] = 0
        for dom in domset:
            edgedev[fi] += list(f[dom]['edgedev'])[0]
            domarea[fi] += list(f[dom]['area'])[0]
            #print('P: {0}'.format(list(f[dom]['P'])))
            # store domcentre for each domain domcentre[fi]
            #print ('{0}'.format(dom_id_list))
            domid = dom_id_list.index(list(f[dom]['f'])[0])
            dirichcentre[fi, domid, 0] = f[dom]['P'][0]
            dirichcentre[fi, domid, 1] = f[dom]['P'][1]

        edgedev[fi] = edgedev[fi] / len(domset)

        fi = fi + 1

    return [t, honda, edgedev, numdoms, domarea, domcentre, dirichcentre]
#
# Load and read all the c_NNNNN.h5 files in logdir which contain a, c,
# etc. Also reads x and y data which is stored in positions.h5.
#
def readSimDataFiles (logdir):

    # Take off any trailing directory slash
    logdir = logdir.rstrip ('/')
    print ('logdir: {0}'.format(logdir))

    # Read x and y first
    pf = h5py.File(logdir+'/positions.h5', 'r')
    x = np.array(pf['x']); # HDF5 dataset object converted into numpy array
    y = np.array(pf['y']);
    totalarea = np.array(pf['area']);
    print ('HexGrid area: {0}'.format(totalarea))

    # From ../logs get list of c_*.h5 files
    p = Path(logdir+'/')
    globstr = 'c_*.h5'
    files = list(p.glob(globstr))
    # Ensure file list is in order:
    files.sort()

    numtimes = len(files)
    print ('Have {0} files/timepoints which are: {1}'.format(numtimes,files))

    # Create the time series to return. Values to be filled in from c_*.h5 file names
    t = np.zeros([numtimes], dtype=int)

    # Count up how many c files we have in each time point once only:
    f = h5py.File(files[0], 'r')
    klist = list(f.keys())
    numcs = 0
    numhexes = 0
    for k in klist:
        if k[0] == 'c':
            numcs = numcs + 1
            numhexes = len(f[k])

    # We're expecting the data from this file to be a matrix with c0,
    # c1 etc as cols and spatial index as rows, all relating to a
    # single time point.
    print ('Creating empty 3d matrix of dims [{0},{1},{2}]'.format (numcs, numhexes, numtimes))
    cmatrix = np.zeros([numcs, numhexes, numtimes], dtype=float)
    # There are as many 'a's as 'c's:
    amatrix = np.zeros([numcs, numhexes, numtimes], dtype=float)
    # The n matrix is 2-D; there is only one n.
    nmatrix = np.zeros([numhexes, numtimes], dtype=float)
    # Same for id matrix
    idmatrix = np.zeros([numhexes, numtimes], dtype=float)

    fileidx = 0
    for filename in files:

        print ('Search {0} with RE pattern {1}'.format(filename, (logdir+'/c_(.*).h5')))

        # Get the time index from the filename with a reg. expr.
        idxsearch = re.search(logdir+'/c_(.*).h5', '{0}'.format(filename))
        thetime = int('{0}'.format(idxsearch.group(1)))
        t[fileidx] = thetime
        #print ('Time {0}: {1}'.format(fileidx, thetime))

        f = h5py.File(filename, 'r')
        klist = list(f.keys())

        for k in klist:
            #print ('Key: {0} fileidx: {1}'.format(k, fileidx))
            if k[0] == 'c':
                cnum = int(k[1:])
                cmatrix[cnum,:,fileidx] = np.array(f[k])
            elif k[0] == 'a':
                anum = int(k[1:])
                amatrix[anum,:,fileidx] = np.array(f[k])
            elif k[0] == 'n':
                nmatrix[:,fileidx] = np.array(f[k])
            elif k[0] == 'd' and k[1] == 'r':
                if np.array(f[k]).size > 0:
                    idmatrix[:,fileidx] = np.array(f[k])

        fileidx = fileidx + 1

    return (x, y, t, cmatrix, amatrix, nmatrix, idmatrix, totalarea)

#
# targ is a container of a target x,y coordinate. x and y are the
# vectors of positions of the hexes in the hexgrid. This returns the
# index to the hex which is closest to targ.
#
def selectIndex(x, y, targ):
    # Now a quick plot of a select hex by time
    # Find index nearest given x and y:
    x_targ = targ[0]#-0.11
    y_targ = targ[1]# 0.4
    rmin = 10000000
    ix = 10000000
    for idx in range(0,len(x)):
        r_ = np.sqrt((x[idx] - x_targ)*(x[idx] - x_targ) + (y[idx] - y_targ)*(y[idx] - y_targ))
        if r_ < rmin:
            rmin = r_
            ix = idx
    return ix
