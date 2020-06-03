#
# A library of HDF5 data loading routines
#

import numpy as np
from pathlib import Path
import h5py
import re
import json

#
# This is a class to load the data generated by the BarrelEmerge
# simulations. It optionally loads different aspects of the simulation
# data (which is stored in HDF5 files), controlled by the attributes
# loadSimData, loadAnalysisData, loadTimeStep, etc. It also loads
# information stored in the params.json file which the simulation will
# record in the log directory.
#
class BarrelData:

    #
    # No arguments for the constructor
    #
    def __init__ (self):

        #
        # Attributes which control what is loaded:
        #

        # Set to True to load simulation data (a, c etc), False not to.
        self.loadSimData = True

        # Set to True to load the analysis data, False not to.
        self.loadAnalysisData = True

        # Set to True if you want to load all the domdivisions (makes the
        # loading slower). Only relevant if loadAnalysisData == True
        self.loadDivisions = False

        # Set to True if you want to load the guidance molecule data
        self.loadGuidance = False

        # Set to True if you want to load the x/y position info
        self.loadPositions = True

        # Set True to load the hex flags from the hexgrid.h5 file
        self.loadHexFlags = False

        # Set to t>=0 to load a specific time step. Otherwise, all time
        # steps are loaded.
        self.loadTimeStep = -1

        # The log directory
        self.logdir = ''

        #
        # Data attributes:
        #

        # The number of thalamocortical types
        self.N = 0

        # The number of guidance gradients
        self.M = 0

        # Number of hexes
        self.nhex = 0

        # The length of time per step. Obtained from params.json in the log directory.
        self.dt = 1.0

        # Time in steps.
        self.t_steps = np.array([])

        # Does this instance hold a time series of data or data for a
        # single time? Make it possible to load either series or single
        # time, because this avoids the lengthy waits that my original,
        # hacked together code made inevitable. The length of t will tell
        # us this. This is t_steps * dt.
        self.t = np.array([])

        # Position, total area of hexes
        self.x = np.array([])
        self.y = np.array([])
        self.totalarea = np.array([])
        # Hex flags (read from HexGrid.h5)
        self.hex_flags = np.array([], dtype=int)

        # idnames are read from the parameters json file
        self.id_byname = {}
        self.gamma_byname = {}
        self.gamma_byid = {} # indexed by a float32

        # Simulation variables
        self.a = np.array([])
        self.c = np.array([])
        self.n = np.array([])

        # The localization measure
        self.locn = np.array([])
        self.locn_vs_t = np.array([])

        # Guidance molecules
        self.g = np.array([])

        # The barrel ID of each hex, according to the drawing/experimental data
        self.expt_id = np.array([])

        # The ID of each hex based on the ID of the highest c_i
        self.id_c = np.array([])
        # The ID of each hex based on the ID of the highest a_i
        self.id_a = np.array([])

        # The Honda delta value, Shape: len(t)
        self.honda = np.array([])

        # The edge deviation value, Shape: len(t). How much the edges in the
        # pattern deviate from the straight lines which connect the
        # vertices.
        self.edgedev = np.array([])

        # The number of Dirichlet domains at time t, Shape: len(t)
        self.numdoms = np.array([])

        # The area of the Dirichlet domains/total area, Shape: len(t)
        self.domarea = np.array([])

        # Domain id list
        self.dom_id_list = np.array([])

        # Coordinates of the centroids of the domains, Shape: len(t)*N*2
        self.domcentres = np.array([])

        # Coordinates of the centres of the domains determined by Honda's
        # method, Shape: len(t)*N*2
        self.dirichcentres = np.array([])

        # The sum of squared distances between the centroids of the
        # experimental barrels and the simulated barrels. len(t)
        self.sos_dist = np.array([])

        # The 'map difference'. if Hex n expt. ID != Hex n sim. ID, then add
        # one to this, len(t). It's the proportion of hexes which are different
        # in ID to the experimental map. Lower is better. Range [0,1].
        self.mapdiff = np.array([])

        # The sum (in hexes) of the absolute difference in areas of each
        # experimental domain and simulated domain. len(t). Range [0,nhex].
        self.area_diff = np.array([])

        # The divisions between domains. All those paths that the C++ code
        # walks.
        self.domdivision = []

        self.gammaColour_byid = {}

        self.gammaColourScheme = 'greenblue'

        # Some more self attributes to set to defaults - these should
        # be modified in loadParams()
        self.hextohex_d = 0
        self.F = 0
        self.k = 0
        self.meanalpha=0
        self.meanbeta=0
        self.meanepsilon=0

        self.debug = False
    #
    # Create self.t and self.t_steps, first checking to see if they've
    # already been created.
    #
    def createTimeSeries (self, numtimes):
        # Create the time series to return based on there being numtimes steps recorded.
        if self.t_steps.size==0:
            self.t_steps = np.zeros([numtimes], dtype=int)
            self.t = np.zeros([numtimes], dtype=float)
        else:
            t_cmp = np.zeros([numtimes], dtype=int)
            if np.shape(t_cmp) == np.shape(self.t_steps):
                if self.debug:
                    print ('dirich_*.h5 files and c_*.h5 files match up.')
            else:
                print ('WARNING: dirich_*.h5 files and c_*.h5 files DO NOT match up. Re-creating t...')
                self.t_steps = np.zeros([numtimes], dtype=int)
                self.t = np.zeros([numtimes], dtype=float)

    #
    # Read id_byname and timestep
    #
    def loadParams (self):
        count = np.float32(0.0)
        with open (self.logdir+'/params.json') as f:
            jd = json.load(f)
            self.dt = jd["dt"]
            self.hextohex_d = jd["hextohex_d"]
            self.D = jd["D"]
            try:
                self.F = jd["F"]
            except:
                self.F = 0
            self.k = jd["k"]
            tc = jd["tc"]
            if self.debug:
                print ('tc length: {0}'.format(len(jd["tc"])))
            self.N = len(jd["tc"])
            sumalpha = 0
            sumbeta = 0
            sumepsilon = 0
            for i in tc:
                # Do a key-value thing
                sumalpha = sumalpha + i["alpha"]
                sumbeta = sumbeta + i["beta"]
                try:
                    sumepsilon = sumepsilon + i["epsilon"]
                except:
                    pass
                theid = count/np.float32(self.N)
                self.id_byname[i["name"]] = theid
                self.gamma_byname[i["name"]] = i["gamma"]
                self.gamma_byid[theid] = i["gamma"]
                #
                if self.gammaColourScheme == 'redblue':
                    self.gammaColour_byid[theid] = (0.5+i["gamma"][0]/4.0, 0, 0.5+i["gamma"][1]/4.0)
                else: # green blue
                    self.gammaColour_byid[theid] = (0, 0.5+i["gamma"][0]/4.0, 0.5+i["gamma"][1]/4.0)
                #print ('Setting gammaColour_byid[{0}] to {1}'.format (theid, self.gammaColour_byid[theid]))
                count = count + np.float32(1.0)
            self.meanalpha = sumalpha/count
            self.meanbeta = sumbeta/count
            self.meanepsilon = sumepsilon/count
    #
    # Load in data
    #
    def load (self, logdir_):
        # Take off any trailing directory slash
        self.logdir = logdir_.rstrip ('/')

        # Load anything relevant from JSON params data. Currently, this is the timestep, dt.
        self.loadParams()

        if self.loadGuidance == True:
            if self.debug:
                print ('readGuidance()')
            self.readGuidance()

        if self.loadPositions == True:
            if self.debug:
                print ('readPositions()')
            self.readPositions()

        if self.loadHexFlags == True:
            if self.debug:
                print ('readHexGrid()')
            self.readHexGrid()

        if self.loadAnalysisData == True:
            if self.debug:
                print ('readDirichData()')
            self.readDirichData()

        if self.loadSimData == True:
            if self.debug:
                print ('readPositions() then readSimDataFiles()')
            self.readPositions() # override position reading option in this case
            self.readSimDataFiles()

    #
    # Read hexgrid.h5 for the flags
    #
    def readHexGrid (self):
        pf = h5py.File(self.logdir+'/hexgrid.h5', 'r')
        self.hex_flags = np.array(pf['d_flags'], dtype=int)
        # Read in neighbours
        self.d_ne = np.array(pf['d_ne'], dtype=int)
        self.d_nne = np.array(pf['d_nne'], dtype=int)
        self.d_nnw = np.array(pf['d_nnw'], dtype=int)
        self.d_nw = np.array(pf['d_nw'], dtype=int)
        self.d_nsw = np.array(pf['d_nsw'], dtype=int)
        self.d_nse = np.array(pf['d_nse'], dtype=int)

    #
    # New analysis. For each hex, compute a localization variable which is
    # N*c[i_max] - sum(c[i!=i_max]) WHERE sum(c) was first normalized
    #
    # Call this function after loading data (being sure to set loadSimData
    # True)
    #
    def computeLocalization_subtractive (self):
        if self.loadSimData == False:
            print ('Error: You have to ensure that you load simulation data by setting loadSimData True before calling load()')
            return
        numtimes = np.shape(self.c)[2]
        self.locn = np.zeros([self.nhex, numtimes], dtype=float)
        self.locn_vs_t = np.zeros((numtimes), dtype=float)
        for tidx in range(0, numtimes): # Loop over all times available
            # This loop runs for each TIME
            cs = self.c[:,:,tidx]
            csum = 0.0
            allhexes_csum = 0.0 # A sum of the "localization measure" over all hexes
            hnum = int(0);
            for cc in cs.T:
                # This loop runs for each HEX
                imax = int(np.argmax(cc))
                sum_cc = np.sum(cc)
                csum = cc[imax] * self.N / sum_cc # do 41 * c_max - sum(c_others)
                for i in range(0, self.N): # np.shape(self.c)[0] should be 41
                    if i == imax:
                        continue
                    # Have to guard against the odd trash value in cc
                    if (cc[i] >= 0.0) and (cc[i] <= 1.0):
                        csum -= (cc[i] / sum_cc)
                self.locn[hnum, tidx] = csum
                hnum += 1
                # Add csum to tcsum
                allhexes_csum += csum
            # Now have tcsum for this particular t value; append it to the object:
            self.locn_vs_t[tidx] = allhexes_csum/float(self.nhex)

    # Localisation measure:
    def computeLocalization (self):
        if self.loadSimData == False:
            print ('Error: You have to ensure that you load simulation data by setting loadSimData True before calling load()')
            return
        numtimes = np.shape(self.c)[2]
        self.locn = np.zeros([self.nhex, numtimes], dtype=float)
        self.locn_vs_t = np.zeros((numtimes), dtype=float)
        for tidx in range(0, numtimes): # Loop over all times available
            # This loop runs for each TIME
            cs = self.c[:,:,tidx]
            csum = 0.0
            allhexes_csum = 0.0 # A sum of the "localization measure" over all hexes
            hnum = int(0);
            for cc in cs.T:
                # This loop runs for each HEX
                imax = int(np.argmax(cc))
                sum_cc = np.sum(cc)
                csum = cc[imax] / sum_cc
                self.locn[hnum, tidx] = csum
                hnum += 1
                # Add csum to tcsum
                allhexes_csum += csum
            # Now have tcsum for this particular t value; append it to the object:
            self.locn_vs_t[tidx] = allhexes_csum/float(self.nhex)

    #
    # Read analysis data from the dirich_*.h5 files.
    #
    def readDirichData (self):

        p = Path(self.logdir+'/')

        if self.debug:
            print ('readDirichData: loadTimeStep = {0:05d}'.format (self.loadTimeStep))
        if self.loadTimeStep > -1:
            globstr = 'dirich_{0:05d}.h5'.format (self.loadTimeStep)
        else:
            print ("WARNING: Loading data for all times, this may be slow...")
            globstr = 'dirich_*.h5'

        files = list(p.glob(globstr))
        files.sort()
        #print ('Files: {0}'.format(files))
        numtimes = len(files)

        # Check if we'll need to read domcentres
        readDomCentres = True if self.domcentres.size == 0 else False

        # Create the time series to return. Values to be filled in from dirich_*.h5 file names
        self.createTimeSeries (numtimes)

        # To hold the honda values
        self.honda = np.zeros([numtimes], dtype=float)
        # To hold the sos_distance values
        self.sos_dist = np.zeros([numtimes], dtype=float)
        self.mapdiff = np.zeros([numtimes], dtype=float)
        self.area_diff = np.zeros([numtimes], dtype=float)
        # To hold the edgedeviation
        self.edgedev = np.zeros([numtimes], dtype=float)
        # To hold a count of number of domains
        self.numdoms = np.zeros([numtimes], dtype=float)
        # The area of the grid that is detected Dirichlet domains
        self.domarea = np.zeros([numtimes], dtype=float)
        # Coordinates of the putative centre of the domain. Need to open first file to get N.
        #print ('h5py open {0}'.format(files[0]))
        f = h5py.File(files[0], 'r')
        self.N = list(f['N'])[0]
        # Domain centres using centroid method:
        if readDomCentres:
            self.domcentres = np.zeros([numtimes, self.N, 2], dtype=float)
        # Dirichlet domain putative centres, Honda method:
        self.dirichcentres = np.zeros([numtimes, self.N, 2], dtype=float)

        # Boundary around each domain. At each time, have Nd domains, each
        # of which has Nv vertices, each of which has a 'path to next'
        # list of coordinates of variable length. So what's the data
        # container to use...? Ok, so concatenate all the vertices, so
        # that each domain has a variable length list of coordinates.
        self.domdivision = [] # one element for each time.

        fi = 0
        for filename in files:

            f = h5py.File(filename, 'r')

            #print ('Search {0} with RE pattern {1}'.format(filename, (logdir+'/dirich_(.*).h5')))
            idxsearch = re.search(self.logdir+'/dirich_(.*).h5', '{0}'.format(filename))
            thetime = int('{0}'.format(idxsearch.group(1)))
            self.t_steps[fi] = thetime # Time in number of simulation steps.
            self.t[fi] = thetime * self.dt

            # Get the Honda Dirichlet value (the overall value)
            self.honda[fi] = list(f['honda'])[0]

            # The sum of squared distances between the simulated barrels and the experimentally determined pattern
            self.sos_dist[fi] = list(f['sos_distances'])[0]
            # The sum of the square of the absolute differences in area (in num
            # hexes) between the experimental and simulated barrel fields.
            self.area_diff[fi] = list(f['area_diff'])[0]
            # Another metric to determine the difference between the current pattern and the
            # experimentally observed pattern, this one is based on traced barrel boundaries.
            self.mapdiff[fi] = list(f['mapdiff'])[0]

            if readDomCentres:
                # Coordinates, but need to re-cast them so that they have all ids. Or do I do that in the C++?
                self.dom_id_list = list(f['reg_centroids_id'])
                self.domcentres[fi, :, 0] = list(f['reg_centroids_x'])
                self.domcentres[fi, :, 1] = list(f['reg_centroids_y'])
                #print ('x coords: {0}'.format(domcentres[fi, :, 0]))

            # Now process the domains.
            nondomset = set(['honda', 'N', 'reg_centroids_id', 'reg_centroids_x', 'reg_centroids_y', 'reg_centroids_id_all', 'sos_distances', 'mapdiff', 'area_diff'])
            kset = set(f.keys()) # dom000, dom001, dom002, etc, honda
            domset = kset.difference(nondomset) # Removes 'honda'

            # The number of domains in the pattern at this stage in the simulation
            self.numdoms[fi] = len(domset)

            self.edgedev[fi] = 0
            all_domboundcoords = []
            for dom in domset:
                domboundcoords = []
                self.edgedev[fi] += list(f[dom]['edgedev'])[0]
                self.domarea[fi] += list(f[dom]['area'])[0]
                #print('P: {0}'.format(list(f[dom]['P'])))
                # store domcentre for each domain domcentres[fi]
                #print ('{0}'.format(dom_id_list))
                domid = self.dom_id_list.index(list(f[dom]['f'])[0])
                self.dirichcentres[fi, domid, 0] = f[dom]['P'][0]
                self.dirichcentres[fi, domid, 1] = f[dom]['P'][1]
                # for each vertex, append coordinates onto a dom, then append the dom onto domdivision
                nonvkset = set(['P', 'area', 'edgedev', 'f', 'honda'])
                vkset0 = set(f[dom].keys())
                vkset = vkset0.difference(nonvkset)

                # This section adds a lot of time to the loading...
                if self.loadDivisions == True:
                    ptn = np.array([]) # empty array
                    for v in vkset:
                        ptn_xy = np.array(list(f[dom][v]['pathto_next_first']))
                        ptn_y = np.array(list(f[dom][v]['pathto_next_second']))
                        ptn_xy = np.vstack ((ptn_xy, ptn_y))
                        domboundcoords.append(ptn_xy)

                        ptn_xy = np.array(list(f[dom][v]['pathto_neighbour_first']))
                        ptn_y = np.array(list(f[dom][v]['pathto_neighbour_second']))
                        ptn_xy = np.vstack ((ptn_xy, ptn_y))
                        domboundcoords.append(ptn_xy)

                    all_domboundcoords.append(domboundcoords)

            if self.loadDivisions == True:
                self.domdivision.append(all_domboundcoords)

            self.edgedev[fi] = self.edgedev[fi] / len(domset)

            fi = fi + 1

    #
    # Load and read all the c_NNNNN.h5 files in logdir which contain a, c,
    # etc. Also reads x and y data which is stored in positions.h5.
    #
    def readSimDataFiles (self):

        # Do we need to read dom centres in this method?
        readDomCentres = True if self.domcentres.size == 0 else False

        # Read x and y first
        if self.loadPositions == False:
            self.readPositions() # anyway

        # From ../logs get list of c_*.h5 files
        p = Path(self.logdir+'/')

        if self.loadTimeStep > -1:
            globstr = 'c_{0:05d}.h5'.format (self.loadTimeStep)
        else:
            globstr = 'c_*.h5'

        files = list(p.glob(globstr))
        # Ensure file list is in order:
        files.sort()

        numtimes = len(files)
        if self.debug:
            print ('Have {0} files/timepoints which are: {1}'.format(numtimes,files))

        self.createTimeSeries (numtimes)

        # Count up how many c files we have in each time point once only:
        f = h5py.File(files[0], 'r')
        klist = list(f.keys())
        numcs = 0
        self.numhexes = 0
        for k in klist:
            if k[0] == 'c':
                numcs = numcs + 1
                self.nhex = len(f[k])

        # We're expecting the data from this file to be a matrix with c0,
        # c1 etc as cols and spatial index as rows, all relating to a
        # single time point.
        #print ('Creating empty 3d matrix of dims [{0},{1},{2}]'.format (numcs, numhexes, numtimes))
        self.c = np.zeros([numcs, self.nhex, numtimes], dtype=float)
        # There are as many 'a's as 'c's:
        self.a = np.zeros([numcs, self.nhex, numtimes], dtype=float)
        # The n matrix is 2-D; there is only one n.
        self.n = np.zeros([self.nhex, numtimes], dtype=float)
        # Same for id matrix
        self.id_c = np.zeros([self.nhex, numtimes], dtype=float)
        # id matrix based on a
        self.id_a = np.zeros([self.nhex, numtimes], dtype=float)

        if readDomCentres:
            self.domcentres = np.zeros([numtimes, self.N, 2], dtype=float)

        fileidx = 0
        for filename in files:
            #print ('Search {0} with RE pattern {1}'.format(filename, (self.logdir+'/c_(.*).h5')))

            # Get the time index from the filename with a reg. expr.
            idxsearch = re.search(self.logdir+'/c_(.*).h5', '{0}'.format(filename))
            thetime = int('{0}'.format(idxsearch.group(1)))
            # WARNING: re-setting self.t (as well as doing it in readDirichData)
            self.t_steps[fileidx] = thetime # Time in number of simulation steps.
            self.t[fileidx] = thetime * self.dt
            # print ('Time {0}: {1}'.format(fileidx, thetime))

            f = h5py.File(filename, 'r')
            klist = list(f.keys())

            for k in klist:
                #print ('Key: {0} fileidx: {1}'.format(k, fileidx))
                if k[0] == 'c':
                    cnum = int(k[1:])
                    self.c[cnum,:,fileidx] = np.array(f[k])
                elif k[0] == 'a':
                    anum = int(k[1:])
                    self.a[anum,:,fileidx] = np.array(f[k])
                elif k[0] == 'n':
                    self.n[:,fileidx] = np.array(f[k])
                elif k[0] == 'd' and k[1] == 'r':
                    if np.array(f[k]).size > 0:
                        self.id_c[:,fileidx] = np.array(f[k])

            # Not right yet.
            self.id_a[:,fileidx] = np.max(self.a[:,:,fileidx], axis=0)

            if readDomCentres:
                # Get domcentres, only if necessary
                dcf_filename = '{0}/dirich_{1:05d}.h5'.format(self.logdir, thetime)
                dcf = h5py.File (dcf_filename, 'r')
                self.dom_id_list = list(dcf['reg_centroids_id'])
                self.domcentres[fileidx, :, 0] = list(dcf['reg_centroids_x'])
                self.domcentres[fileidx, :, 1] = list(dcf['reg_centroids_y'])

            fileidx = fileidx + 1

    #
    # Read position data.
    #
    def readPositions (self):

        # Read x and y first
        pf = h5py.File(self.logdir+'/positions.h5', 'r')
        self.x = np.array(pf['x']) # HDF5 dataset object converted into numpy array
        self.y = np.array(pf['y'])
        self.totalarea = np.array(pf['area'])

    #
    # Read in the guidance molecules and the experimental barrel ID
    # (obtained from the drawing in inkscape of each barrel)
    #
    def readGuidance (self):

        # Read guidance expression
        gf = h5py.File(self.logdir+'/guidance.h5', 'r')
        # Count up how many c files we have in each time point once only:
        gklist = list(gf.keys())
        self.M = 0
        self.nhex = 0
        for k in gklist:
            if k[0] == 'r': # rh0, rh1 etc
                self.M = self.M + 1
                self.nhex = len(gf[k])

        self.g = np.zeros([self.nhex, self.M], dtype=float)
        for m in range (0, self.M):
            self.g[:,m] = np.array(gf['rh{0}'.format(m)])

        self.expt_id = np.array(gf['expt_barrel_id'])

    #
    # targ is a container of a target x,y coordinate. x and y are the
    # vectors of positions of the hexes in the hexgrid. This returns the
    # index to the hex which is closest to targ.
    #
    def selectIndex (x, y, targ):

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
