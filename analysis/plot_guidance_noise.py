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
fnt = {'family' : 'DejaVu Sans', 'weight' : 'regular', 'size' : 12 }
matplotlib.rc('font', **fnt)

sdata = np.genfromtxt ('postproc/guidance_noise.csv', delimiter=",", names=True)

# Loop through data, making up 4 graphs for the different metrics
F1, ((ax1, ax2, ax3, ax4)) = plt.subplots(1, 4, sharey=False, figsize=(12,4))

# Have 5 angles and 5 gains (currently)
honda = np.zeros([5, 5], dtype=float)
sos = np.zeros([5, 5], dtype=float)
area = np.zeros([5, 5], dtype=float)
locn = np.zeros([5, 5], dtype=float)
eta = np.zeros([5, 5], dtype=float)

idx_g1 = { 0.03 : int(0),  0.06: int(1), 0.15 : int(2), 0.6 : int(3), 1.5 : int(4)}
idx_s1 = {0.015 : int(0), 0.022: int(1), 0.03 : int(2), 0.06: int(3), 0.1 : int(4)}

xlbl = (['.03', '.06', '.15', '.6', '1.5'])
ylbl = (['.015', '.022', '.03', '.06', '.1'])

for s in sdata:
    r = idx_s1[s['noise_sigma']]
    c = idx_g1[s['noise_gain']]
    honda[r,c] = s['hondadelta']
    sos[r,c] = s['sos_dist']
    area[r,c] = s['area_diff']
    locn[r,c] = s['localization']
    eta[r,c] = s['eta']

# These come from the output of plot_paramsearch_paper.py:
honda_min=0.016603905707597733
honda_max=0.40066197514533997
area_min=0.2837541796379569
area_max=1.0
locn_min=0.041788052869136255
locn_max=0.7319451998375573
sos_min=2.9542248615230577
sos_max=3.350204398214124
eta_min=0
eta_max=600

# Use same min/maxes as produced by the parameter search?
im1 = ax1.imshow (honda, cmap='inferno_r', origin='lower', vmin=honda_min, vmax=honda_max, interpolation='nearest')
ax1.set_title('Honda $\delta$')
ax1.set_xticks ([0,1,2,3,4])
ax1.set_xticklabels (xlbl)
ax1.set_yticks ([0,1,2,3,4])
ax1.set_yticklabels (ylbl)
ax1.set_xlabel('Noise mag.')
ax1.set_ylabel('Noise $\sigma$')

im2 = ax2.imshow (sos,   cmap='inferno_r', origin='lower', vmin=sos_min,   vmax=sos_max,   interpolation='nearest')
ax2.set_title('SOS')
ax2.set_xticks ([0,1,2,3,4])
ax2.set_xticklabels ([0.1, 0.5, 1, 2, 10])
ax2.set_xticklabels (xlbl)
ax2.set_yticks ([0,1,2,3,4])
ax2.set_yticklabels (ylbl)
ax2.set_xlabel('Noise mag.')

im3 = ax3.imshow (eta,  cmap='inferno_r', origin='lower', vmin=eta_min,  vmax=eta_max,  interpolation='nearest')
ax3.set_title('$\eta$')
ax3.set_xticks ([0,1,2,3,4])
ax3.set_xticklabels (xlbl)
ax3.set_yticks ([0,1,2,3,4])
ax3.set_yticklabels (ylbl)
ax3.set_xlabel('Noise mag.')

im4 = ax4.imshow (locn,  cmap='inferno', origin='lower', vmin=locn_min,  vmax=locn_max,  interpolation='nearest')
ax4.set_title('Localization $\omega$')
ax4.set_xticks ([0,1,2,3,4])
ax4.set_xticklabels (xlbl)
ax4.set_yticks ([0,1,2,3,4])
ax4.set_yticklabels (ylbl)
ax4.set_xlabel('Noise mag.')

F1.subplots_adjust (left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.05, hspace=0.05)
plt.tight_layout()
plt.savefig('plots/guidance_noise.svg')
plt.show()
