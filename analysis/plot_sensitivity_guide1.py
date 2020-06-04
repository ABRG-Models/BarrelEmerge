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

sdata = np.genfromtxt ('postproc/sensitivity_guide1.csv', delimiter=",", names=True)

# Loop through data, making up 4 graphs for the different metrics
F1, ((ax1, ax2, ax3, ax4)) = plt.subplots(1, 4, sharey=False, figsize=(20,6))

# Have 5 angles and 3 gains (currently)
honda = np.zeros([5, 3], dtype=float)
sos = np.zeros([5, 3], dtype=float)
area = np.zeros([5, 3], dtype=float)
locn = np.zeros([5, 3], dtype=float)

idx_p1 = {-34.0 : int(0), -14.0: int(1), 6.0 : int(2), 26.0: int(3), 46.0: int(4)}
idx_g1 = {0.1 : int(0), 0.5: int(1), 1.0 : int(2)}

for s in sdata:
    r = idx_p1[s['phi1']]
    c = idx_g1[s['gain1']]
    honda[r,c] = s['hondadelta']
    sos[r,c] = s['sos_dist']
    area[r,c] = s['area_diff']
    locn[r,c] = s['localization']

# These come from the output of plot_paramsearch_paper.py:
honda_min=0.016603905707597733
honda_max=0.40066197514533997
area_min=0.2837541796379569
area_max=1.0
locn_min=0.041788052869136255
locn_max=0.7319451998375573
sos_min=2.9542248615230577
sos_max=3.350204398214124

# Use same min/maxes as produced by the parameter search?
im1 = ax1.imshow (honda, cmap='inferno_r', vmin=honda_min, vmax=honda_max, interpolation='nearest')
ax1.set_title('Honda $\delta$')
ax1.set_xticks ([0,1,2])
ax1.set_xticklabels ([0.1, 0.5, 1.0])
ax1.set_yticks ([0,1,2,3,4])
ax1.set_yticklabels ([-34, -14, 6, 26, 46])
ax1.set_xlabel('Sig. mol. gain')
ax1.set_ylabel('Sig. mol. $\phi$')

im2 = ax2.imshow (sos,   cmap='inferno_r', vmin=sos_min,   vmax=sos_max,   interpolation='nearest')
ax2.set_title('SOS')
ax2.set_xticks ([0,1,2])
ax2.set_xticklabels ([0.1, 0.5, 1.0])
ax2.set_yticks ([0,1,2,3,4])
ax2.set_yticklabels ([-34, -14, 6, 26, 46])
ax2.set_xlabel('Sig. mol. gain')

im3 = ax3.imshow (area,  cmap='inferno_r', vmin=area_min,  vmax=area_max,  interpolation='nearest')
ax3.set_title('Area $\eta$')
ax3.set_xticks ([0,1,2])
ax3.set_xticklabels ([0.1, 0.5, 1.0])
ax3.set_yticks ([0,1,2,3,4])
ax3.set_yticklabels ([-34, -14, 6, 26, 46])
ax3.set_xlabel('Sig. mol. gain')

im4 = ax4.imshow (locn,  cmap='inferno', vmin=locn_min,  vmax=locn_max,  interpolation='nearest')
ax4.set_title('Localization $\omega$')
ax4.set_xticks ([0,1,2])
ax4.set_xticklabels ([0.1, 0.5, 1.0])
ax4.set_yticks ([0,1,2,3,4])
ax4.set_yticklabels ([-34, -14, 6, 26, 46])
ax4.set_xlabel('Sig. mol. gain')

F1.subplots_adjust (left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.05, hspace=0.05)
plt.tight_layout()
plt.show()
