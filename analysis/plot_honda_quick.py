# To access argv and also include the include dir
import sys
sys.path.insert (0, './include')
import numpy as np
# Import data loading code
#import load as ld
import BarrelData as bd
# Import MY plotting code:
import plot as pt
import matplotlib
import matplotlib.pyplot as plt
# Direct HDF5 access
import h5py
# My domcentres linear fit code:
import domcentres as dc
import sebcolour
col = sebcolour.Colour

# Set plotting defaults
fs = 32
fnt = {'family' : 'Arial',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

# IMPORTANT for svg output of text as things that can be edited in inkscape
plt.rcParams['svg.fonttype'] = 'none'

# And plot this longhand here:
F1 = plt.figure (figsize=(9,12))

t1_masked = np.load ('postproc/honda_t.npy')
hondadelta = np.load ('postproc/honda_delta.npy')
area_diff =  np.load ('postproc/area_diff.npy')
sos_dist =  np.load ('postproc/sos_dist.npy')
map_diff =  np.load ('postproc/map_diff.npy')
locn_vs_t =  np.load ('postproc/locn_vs_t.npy')
adjacency_arrangement =  np.load ('postproc/adjacency_arrangement.npy')
adjacency_differencemag =  np.load ('postproc/adjacency_differencemag.npy')

xmax = max(t1_masked)
xmax = xmax[0]
print ('xmax = {0}'.format(xmax))

ax1 = F1.add_subplot(3,1,1)

l1, = ax1.plot(t1_masked, hondadelta, 'o', markersize=12, color=col.red, label='Honda $\delta$')

# 0.054 is Senft and Woolsey's result for barrels (mouse 0,054, other rodents about 0.055)
l2, = ax1.plot((0,xmax), (0.055, 0.055), '--', color=col.red, linewidth=3, label="good (S&W)")

show_mapdiff = 0
if show_mapdiff:
    ax4 = ax1.twinx()
    l5, = ax4.plot(t1_masked, map_diff, 's', markersize=12, color=col.blue)
show_sos = 0
if show_sos:
    ax4 = ax1.twinx()
    l5, = ax4.plot(t1_masked, sos_dist, 's', markersize=12, color=col.blue)

ax2 = F1.add_subplot(3,1,2)
l3, = ax2.plot(t1_masked, area_diff, 's', markersize=12, color=col.black)

ax3 = ax2.twinx()
l4, = ax3.plot(t1_masked, locn_vs_t, 'h', markersize=12, color=col.gray60)

ax5 = F1.add_subplot(3,1,3)
l5, = ax5.plot(t1_masked, adjacency_arrangement, '^', markersize=12, color=col.blue, label='Arr.')
ax5.set_ylabel('Arr.')
ax5.set_xlabel ('time (10k steps)')
ax6 = ax5.twinx()
l6, = ax6.plot(t1_masked, adjacency_differencemag, 'v', markersize=12, color=col.purple, label='Diff mag.')
ax6.set_ylabel('Diff. mag.')
ax5.legend(loc='center', prop={'size': 12})
ax6.legend(loc='center right', prop={'size': 12})

ax2.set_xlabel ('time (10k steps)')
ax1.set_ylabel ('$\delta$', rotation=0, labelpad=30)
ax2.set_ylabel ('$\eta$', rotation=0, labelpad=30)
ax3.set_ylabel ('$\omega$', rotation=0, labelpad=30)
ax2.tick_params (axis='y', labelcolor=col.black)
ax1.set_xlim ((0,xmax))
ax1.set_ylim ((0,0.35))
ax2.set_ylim ((0,1.2))
ax3.set_ylim ((0,0.28))
ax2.set_xlim ((0,xmax))

lw = 2
for axis in ['top','bottom','left','right']:
  ax1.spines[axis].set_linewidth(lw)
  ax1.tick_params(width=lw)
  ax2.spines[axis].set_linewidth(lw)
  ax2.tick_params(width=lw)
  ax3.spines[axis].set_linewidth(lw)
  ax3.tick_params(width=lw)

plt.tight_layout()

plt.savefig('plots/hondadelta.svg', transparent=True)

plt.show()
