#
# Plot the 2D and heatmap graphs for the combined sensitivity analysis figure
#

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
fnt = {'family' : 'Arial', 'weight' : 'regular', 'size' : 18 }
matplotlib.rc('font', **fnt)
# IMPORTANT for svg output of text as things that can be edited in inkscape
plt.rcParams['svg.fonttype'] = 'none'

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
eta_max=1.5

# One figure:
F1 = plt.figure (figsize=(16,12))

#
# Gamma noise
#

gammanoise = np.genfromtxt ('postproc/gamma_noise.csv', delimiter=",", names=True)
gmn = np.sort (gammanoise, order='noise_gain')

gamma_range = 4.0
gmn_noise_gain = gmn['noise_gain'] / gamma_range
gmn_honda = gmn['hondadelta']
gmn_sos = gmn['sos_dist']
gmn_area = gmn['area_diff']
gmn_locn = gmn['localization']
gmn_eta = gmn['eta']

mo=2 # miss-out how many data points at end of the next three graphs?
# Honda (Voronoi)
ax1 = F1.add_subplot(3,3,1)
l1, = ax1.plot(gmn_noise_gain[:-mo], gmn_honda[:-mo], 'o-', markersize=12, color=col.red, label='Honda $\delta$')
# Eta (Pattern)
ax2 = F1.add_subplot(3,3,4)
l2, = ax2.plot(gmn_noise_gain[:-mo], gmn_eta[:-mo], 's-', markersize=12, color=col.black, label='$\eta$')
# Omega (Localisation)
ax3 = F1.add_subplot(3,3,7)
l3, = ax3.plot(gmn_noise_gain[:-mo], gmn_locn[:-mo], 'h-', markersize=12, color=col.gray60, label='Locn $\omega$')

# this is an inset axes over the third axis
#ax3_1 = plt.axes([.2, .24, .1, .06])
#ax3_1.plot(gmn_noise_gain[:-10], gmn_eta[:-10], 's-', markersize=8, color=col.b#lack, label='$\eta$')
#ax3_1.tick_params(axis='both', which='major', labelsize=14)

#
# Guidance noise
#

guidenoise = np.genfromtxt ('postproc/guidance_noise.csv', delimiter=",", names=True)
gdn_honda = np.zeros([5, 5], dtype=float)
gdn_sos = np.zeros([5, 5], dtype=float)
gdn_area = np.zeros([5, 5], dtype=float)
gdn_locn = np.zeros([5, 5], dtype=float)
gdn_eta = np.zeros([5, 5], dtype=float)

guide_range = 3.0 # Range of guidance molecule expression - goes from -1.5 to +1.5
idx_g1 = { 0.03/guide_range : int(0),  0.06/guide_range: int(1), 0.15/guide_range : int(2), 0.6/guide_range : int(3), 1.5/guide_range : int(4)}
idx_s1 = {0.015 : int(0), 0.022: int(1), 0.03 : int(2), 0.06: int(3), 0.1 : int(4)}
gdn_xlbl = (['.01', '.02', '.05', '.2', '.5'])
gdn_ylbl = (['.015', '.022', '.03', '.06', '.1'])

for gdn in guidenoise:
    r = idx_s1[gdn['noise_sigma']]
    c = idx_g1[gdn['noise_gain']/guide_range]
    gdn_honda[r,c] = gdn['hondadelta']
    gdn_sos[r,c] = gdn['sos_dist']
    gdn_area[r,c] = gdn['area_diff']
    gdn_locn[r,c] = gdn['localization']
    gdn_eta[r,c] = gdn['eta']
# Add graphs for guidance noise

# Honda
ax4 = F1.add_subplot(3,3,2)
im4 = ax4.imshow (gdn_honda, cmap='inferno_r', origin='lower', vmin=honda_min, vmax=honda_max, interpolation='nearest')
# Eta
ax5 = F1.add_subplot(3,3,5)
im5 = ax5.imshow (gdn_eta,  cmap='inferno_r', origin='lower', vmin=eta_min,  vmax=eta_max,  interpolation='nearest')
# Localization
ax6 = F1.add_subplot(3,3,8)
im6 = ax6.imshow (gdn_locn,  cmap='inferno', origin='lower', vmin=locn_min,  vmax=locn_max,  interpolation='nearest')

#
# Sensitivity to changes to one guidance input; guidance phi/mag modification sensitivity
#

guide1 = np.genfromtxt ('postproc/sensitivity_guide1.csv', delimiter=",", names=True)

g1_honda = np.zeros([5, 5], dtype=float)
g1_sos = np.zeros([5, 5], dtype=float)
g1_area = np.zeros([5, 5], dtype=float)
g1_locn = np.zeros([5, 5], dtype=float)
g1_eta = np.zeros([5, 5], dtype=float)

idx_p1 = {-34.0 : int(0), -14.0: int(1), 6.0 : int(2), 26.0: int(3), 46.0 : int(4)}
idx_g1 = {  0.1 : int(0),   0.5: int(1), 1.0 : int(2), 2.0 : int(3), 10.0 : int(4)}

for g1 in guide1:
    r = idx_p1[g1['phi1']]
    c = idx_g1[g1['gain1']]
    g1_honda[r,c] = g1['hondadelta']
    g1_sos[r,c] = g1['sos_dist']
    g1_area[r,c] = g1['area_diff']
    g1_locn[r,c] = g1['localization']
    g1_eta[r,c] = g1['eta']

# Honda
ax7 = F1.add_subplot(3,3,3)
im7 = ax7.imshow (g1_honda, cmap='inferno_r', vmin=honda_min, vmax=honda_max, interpolation='nearest')
# Pattern
ax8 = F1.add_subplot(3,3,6)
im8 = ax8.imshow (g1_eta,  cmap='inferno_r', vmin=eta_min,  vmax=eta_max,  interpolation='nearest')
# Localization
ax9 = F1.add_subplot(3,3,9)
im9 = ax9.imshow (g1_locn,  cmap='inferno', vmin=locn_min,  vmax=locn_max,  interpolation='nearest')

#
# Axis tweaking
#

# Params:
lw = 1.5 # line width
lp = 27  # label pad

# Set equal aspect ratio for any given axes
def equal_aspect (ax):
    ratio = 1.0
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)

for axis in ['top','bottom','left','right']:
  ax1.spines[axis].set_linewidth(lw)
  ax1.tick_params(width=lw)
  ax2.spines[axis].set_linewidth(lw)
  ax2.tick_params(width=lw)
  ax3.spines[axis].set_linewidth(lw)
  ax3.tick_params(width=lw)
  ax4.spines[axis].set_linewidth(lw)
  ax4.tick_params(width=lw)
  ax5.spines[axis].set_linewidth(lw)
  ax5.tick_params(width=lw)
  ax6.spines[axis].set_linewidth(lw)
  ax6.tick_params(width=lw)
  ax7.spines[axis].set_linewidth(lw)
  ax7.tick_params(width=lw)
  ax8.spines[axis].set_linewidth(lw)
  ax8.tick_params(width=lw)
  ax9.spines[axis].set_linewidth(lw)
  ax9.tick_params(width=lw)

ax1.set_xlabel ('$\\nu_{\gamma}$')
ax1.set_ylabel ('$\delta$', rotation=0, labelpad=lp)
ax2.set_xlabel ('$\\nu_{\gamma}$')
ax2.set_ylabel ('$\eta$', rotation=0, labelpad=lp)
ax3.set_xlabel ('$\\nu_{\gamma}$')
ax3.set_ylabel ('$\omega$', rotation=0, labelpad=lp)
ax1.set_ylim ((honda_min,honda_max))
ax2.set_ylim ((eta_min,eta_max)) # locn, omega
ax3.set_ylim ((locn_min,locn_max))

ax1.set_xticks([0, 0.2])
ax1.set_xticklabels(['0','.2'])
ax2.set_xticks([0, 0.2])
ax2.set_xticklabels(['0','.2'])
ax3.set_xticks([0, 0.2])
ax3.set_xticklabels(['0','.2'])

ax1.set_yticks ([0.1, 0.2, 0.3, 0.4])
ax1.set_yticklabels (['.1', '.2', '.3', '.4'])
ax2.set_yticks ([0, 0.5, 1.0, 1.5])
ax2.set_yticklabels (['0', '.5', '1', '1.5'])
ax3.set_yticks ([0.2, 0.4, 0.6])
ax3.set_yticklabels (['.2', '.4', '.6'])


equal_aspect (ax1)
equal_aspect (ax2)
equal_aspect (ax3)

ax4.set_xticks ([0,1,2,3,4])
ax4.set_xticklabels (gdn_xlbl)
ax4.set_yticks ([0,1,2,3,4])
ax4.set_yticklabels (gdn_ylbl)
ax4.set_xlabel('$\\nu_{\\rho}$')
ax4.set_ylabel('$\\sigma_{\\rho}$', rotation=0, labelpad=lp-15)

ax5.set_xticks ([0,1,2,3,4])
ax5.set_xticklabels (gdn_xlbl)
ax5.set_yticks ([0,1,2,3,4])
ax5.set_yticklabels (gdn_ylbl)
ax5.set_xlabel('$\\nu_{\\rho}$')
ax5.set_ylabel('$\\sigma_{\\rho}$', rotation=0, labelpad=lp-15)

ax6.set_xticks ([0,1,2,3,4])
ax6.set_xticklabels (gdn_xlbl)
ax6.set_yticks ([0,1,2,3,4])
ax6.set_yticklabels (gdn_ylbl)
ax6.set_xlabel('$\\nu_{\\rho}$')
ax6.set_ylabel('$\\sigma_{\\rho}$', rotation=0, labelpad=lp-15)

ax7.set_xticks ([0,1,2,3,4])
ax7.set_xticklabels (['.1', '.5', 1, 2, 10])
ax7.set_yticks ([0,1,2,3,4])
ax7.set_yticklabels ([-34, -14, 6, 26, 46])
ax7.set_xlabel('$G_{\\rho_1}$')
ax7.set_ylabel('$\\phi_{\\rho_1}$', rotation=0, labelpad=lp-10)

ax8.set_xticks ([0,1,2,3,4])
ax8.set_xticklabels (['.1', '.5', 1, 2, 10])
ax8.set_yticks ([0,1,2,3,4])
ax8.set_yticklabels ([-34, -14, 6, 26, 46])
ax8.set_xlabel('$G_{\\rho_1}$')
ax8.set_ylabel('$\\phi_{\\rho_1}$', rotation=0, labelpad=lp-10)

ax9.set_xticks ([0,1,2,3,4])
ax9.set_xticklabels (['.1', '.5', 1, 2, 10])
ax9.set_yticks ([0,1,2,3,4])
ax9.set_yticklabels ([-34, -14, 6, 26, 46])
ax9.set_xlabel('$G_{\\rho_1}$')
ax9.set_ylabel('$\\phi_{\\rho_1}$', rotation=0, labelpad=lp-10)

# Deal with colorbars here. Manual fiddling to get position correct
cb_height = 0.33333 * 0.72
cb_wid = 0.01
cb_xpos = 0.92

cb_ax = F1.add_axes([cb_xpos, 0.731, cb_wid, cb_height])
cbar = F1.colorbar (im4, cax=cb_ax)
cbar.set_ticks ([0.1, 0.2, 0.3, 0.4])
cbar.set_ticklabels (['.1', '.2', '.3', '.4'])

cb_ax2 = F1.add_axes([cb_xpos, 0.406, cb_wid, cb_height])
cbar2 = F1.colorbar (im5, cax=cb_ax2)
cbar2.set_ticks ([0, 0.5, 1, 1.5])
cbar2.set_ticklabels (['0', '.5', '1', '1.5'])

cb_ax3 = F1.add_axes([cb_xpos, 0.081, cb_wid, cb_height])
cbar3 = F1.colorbar (im6, cax=cb_ax3)
cbar3.set_ticks ([0.2, 0.4, 0.6])
cbar3.set_ticklabels (['.2', '.4', '.6'])

#for axis in ['top','bottom','left','right']:
#  cb_ax.spines[axis].set_linewidth(lw)
#  cb_ax.tick_params(width=lw)
#  cb_ax2.spines[axis].set_linewidth(lw)
#  cb_ax2.tick_params(width=lw)
#  cb_ax3.spines[axis].set_linewidth(lw)
#  cb_ax3.tick_params(width=lw)

# save and show
F1.subplots_adjust (left=0.125, bottom=0.1, right=1.4, top=0.9, wspace=0.05, hspace=0.05)
plt.tight_layout()
plt.savefig('plots/fig_sens.svg', transparent=True)
plt.show()
