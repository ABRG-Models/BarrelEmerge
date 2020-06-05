import sys
sys.path.insert (0, './include')
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import lines
import sebcolour as sc

# Set plotting defaults
matplotlib.use('TkAgg') # cleaner likely to work
fnt = {'family' : 'DejaVu Sans', 'weight' : 'regular', 'size' : 14 }
matplotlib.rc('font', **fnt)

sdata = np.genfromtxt ('postproc/sensitivity_gammas.csv', delimiter=",", names=True)

F1, axs = plt.subplots(4, 3, sharey=False, figsize=(9,12))
# axs = ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9), (ax10, ax11, ax12))

honda_c4 = np.zeros([5, 5], dtype=float)
sos_c4 = np.zeros([5, 5], dtype=float)
area_c4 = np.zeros([5, 5], dtype=float)
locn_c4 = np.zeros([5, 5], dtype=float)

honda_b4 = np.zeros([5, 5], dtype=float)
sos_b4 = np.zeros([5, 5], dtype=float)
area_b4 = np.zeros([5, 5], dtype=float)
locn_b4 = np.zeros([5, 5], dtype=float)

honda_d4 = np.zeros([5, 5], dtype=float)
sos_d4 = np.zeros([5, 5], dtype=float)
area_d4 = np.zeros([5, 5], dtype=float)
locn_d4 = np.zeros([5, 5], dtype=float)

# These come from the output of plot_paramsearch_paper.py and ensure that colour ranges match across figures:
honda_min=0.016603905707597733
honda_max=0.40066197514533997
area_min=0.2837541796379569
area_max=1.0
locn_min=0.041788052869136255
locn_max=0.7319451998375573
sos_min=2.9542248615230577
sos_max=3.350204398214124

bc = int(0) # 'barrel counter'
for br in ['b', 'c', 'd']:

    modified_barrel = '{0}4'.format(br)
    barrel_id = 0
    if modified_barrel == 'b4':
        barrel_id = 1
    elif modified_barrel == 'c4':
        barrel_id = 2
    elif modified_barrel == 'd4':
        barrel_id = 3

    # Create a subset of sdata for modified_barrel
    bdata = sdata[sdata[:]['barrel'] == barrel_id]

    honda = np.zeros([5, 5], dtype=float)
    sos = np.zeros([5, 5], dtype=float)
    area = np.zeros([5, 5], dtype=float)
    locn = np.zeros([5, 5], dtype=float)

    # Sort bdata on gamma_i then gamma_j (CARE: May need to look at order)
    np.sort (bdata, axis=0, order='gamma_i')

    mcount = int(0)
    for s in bdata:
        # How to convert to row and col? no need, if we sort on gamma_i and
        # gamma_j then use a counter:
        r = mcount//5
        c = mcount%5
        honda[r,c] = s['hondadelta']
        sos[r,c] = s['sos_dist']
        area[r,c] = s['area_diff']
        locn[r,c] = s['localization']
        mcount += int(1)

    # Use same min/maxes as produced by the parameter search?
    im1 = axs[0][bc].imshow (honda, cmap='inferno_r', vmin=honda_min, vmax=honda_max, interpolation='nearest')
    axs[0][bc].set_title('{0} $\delta$'.format(modified_barrel))
    #axs[0][bc].set_xticks ([0,1,2,3,4])
    #axs[0][bc].set_xticklabels ([0.1, 0.5, 1, 2, 10])
    #axs[0][bc].set_yticks ([0,1,2,3,4])
    #axs[0][bc].set_yticklabels ([-34, -14, 6, 26, 46])
    axs[0][bc].set_xlabel('$\gamma_i$')
    axs[0][bc].set_ylabel('$\gamma_j$')

    im2 = axs[1][bc].imshow (sos,   cmap='inferno_r', vmin=sos_min,   vmax=sos_max,   interpolation='nearest')
    axs[1][bc].set_title('{0} SOS'.format(modified_barrel))
    #axs[1][bc].set_xticks ([0,1,2,3,4])
    #axs[1][bc].set_xticklabels ([0.1, 0.5, 1, 2, 10])
    #axs[1][bc].set_yticks ([0,1,2,3,4])
    #axs[1][bc].set_yticklabels ([-34, -14, 6, 26, 46])
    axs[1][bc].set_xlabel('$\gamma_i$')
    #axs[1][bc].set_ylabel('$\gamma_j$')

    im3 = axs[2][bc].imshow (area,  cmap='inferno_r', vmin=area_min,  vmax=area_max,  interpolation='nearest')
    axs[2][bc].set_title('{0} $\eta$'.format(modified_barrel))
    #axs[2][bc].set_xticks ([0,1,2,3,4])
    #axs[2][bc].set_xticklabels ([0.1, 0.5, 1, 2, 10])
    #axs[2][bc].set_yticks ([0,1,2,3,4])
    #axs[2][bc].set_yticklabels ([-34, -14, 6, 26, 46])
    axs[2][bc].set_xlabel('$\gamma_i$')
    #axs[2][bc].set_ylabel('$\gamma_j$')

    im4 = axs[3][bc].imshow (locn,  cmap='inferno', vmin=locn_min,  vmax=locn_max,  interpolation='nearest')
    axs[3][bc].set_title('{0} $\omega$'.format(modified_barrel))
    #axs[3][bc].set_xticks ([0,1,2,3,4])
    #axs[3][bc].set_xticklabels ([0.1, 0.5, 1, 2, 10])
    #axs[3][bc].set_yticks ([0,1,2,3,4])
    #axs[3][bc].set_yticklabels ([-34, -14, 6, 26, 46])
    axs[3][bc].set_xlabel('$\gamma_i$')
    #axs[3][bc].set_ylabel('$\gamma_j$')

    bc += int(1)

F1.subplots_adjust (left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.05, hspace=0.05)
plt.tight_layout()
plt.savefig('plots/sensitivity_gamma.svg')
plt.show()
