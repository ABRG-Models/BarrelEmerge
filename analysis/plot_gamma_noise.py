import sys
sys.path.insert (0, './include')
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import lines
import sebcolour as sc
col = sc.Colour()

# Set plotting defaults
matplotlib.use('TkAgg') # cleaner likely to work
fnt = {'family' : 'DejaVu Sans', 'weight' : 'regular', 'size' : 18 }
matplotlib.rc('font', **fnt)
# IMPORTANT for svg output of text as things that can be edited in inkscape
plt.rcParams['svg.fonttype'] = 'none'

sdata = np.genfromtxt ('postproc/gamma_noise.csv', delimiter=",", names=True)
s = np.sort (sdata, order='noise_gain')

noise_gain = s['noise_gain']
honda = s['hondadelta']
sos = s['sos_dist']
area = s['area_diff']
locn = s['localization']
eta = s['eta']

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

# And plot this longhand here:
F1 = plt.figure (figsize=(5,12))

ax1 = F1.add_subplot(3,1,1)
l1, = ax1.plot(noise_gain, honda, 'o-', markersize=12, color=col.red, label='Honda $\delta$')

ax2 = F1.add_subplot(3,1,2)
l2, = ax2.plot(noise_gain, locn, 'h-', markersize=12, color=col.gray60, label='Locn $\omega$')
ax3 = F1.add_subplot(3,1,3)
l3, = ax3.plot(noise_gain, eta, 's-', markersize=12, color=col.black, label='$\eta$')

# Axis tweaking
ax1.set_xlabel ('Noise mag.')
ax1.set_ylabel ('$\delta$', rotation=0, labelpad=30)
ax2.set_xlabel ('Noise mag.')
ax2.set_ylabel ('$\omega$', rotation=0, labelpad=30)
ax3.set_xlabel ('Noise mag.')
ax3.set_ylabel ('$\eta$', rotation=0, labelpad=30)
ax1.set_ylim ((honda_min,honda_max))
ax2.set_ylim ((locn_min,locn_max)) # locn, omega

lw = 2
for axis in ['top','bottom','left','right']:
  ax1.spines[axis].set_linewidth(lw)
  ax1.tick_params(width=lw)
  ax2.spines[axis].set_linewidth(lw)
  ax2.tick_params(width=lw)
  ax3.spines[axis].set_linewidth(lw)
  ax3.tick_params(width=lw)

plt.tight_layout()

plt.savefig('plots/gamma_noise.svg', transparent=True)

plt.show()
