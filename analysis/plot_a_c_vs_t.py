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
fs = 24
fnt = {'family' : 'Arial',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

# IMPORTANT for svg output of text as things that can be edited in inkscape
plt.rcParams['svg.fonttype'] = 'none'

# And plot this longhand here:
F1 = plt.figure (figsize=(24,7))

t1_masked = np.load ('postproc/honda_t.npy')
a_vs_t =  np.load ('postproc/a_vs_t.npy')
c_vs_t =  np.load ('postproc/c_vs_t.npy')

xmax = max(t1_masked)
xmax = xmax[0]
print ('xmax = {0}'.format(xmax))

# Compute the colour map
# Load the dirichlet data, domcentres, etc
bdo = bd.BarrelData() # Just need this for gammaColour_byid
logdirname='/home/seb/models/BarrelEmerge/logs/41N2M_thalguide_Fig1'
bdo.loadTimeStep=10000
bdo.load (logdirname)

colmap = np.zeros([41,3], dtype=float)
count = np.float32(0.0)
for ii in range(0,41):
    oneid = count/np.float32(41)
    colmap[ii] = bdo.gammaColour_byid[oneid]
    count += np.float32(1.0)

lw = 2

ax1 = F1.add_subplot(1,3,1)
# Plot each i
for i in range(np.shape(a_vs_t)[0]):
    ax1.plot(t1_masked, a_vs_t[i,:], '-', markersize=3, color=colmap[i], label='$a_{0}$'.format(i))

ax1.set_ylabel ('$\sum_{hexes} a_i$', rotation=0, labelpad=50)
ax1.set_xlabel ('t (10k steps)')
ax1.set_xlim ((0,xmax))
ax1.set_ylim ((0,1800))
for axis in ['top','bottom','left','right']:
    ax1.spines[axis].set_linewidth(lw)
    ax1.tick_params(width=lw)

ax2 = F1.add_subplot(1,3,2)
# Plot each i
for i in range(np.shape(c_vs_t)[0]):
    ax2.plot(t1_masked, c_vs_t[i,:], '-', markersize=3, color=colmap[i], label='$c_{0}$'.format(i))

ax2.set_ylabel ('$\sum_{hexes} c_i$', rotation=0, labelpad=50)
ax2.set_xlabel ('t (10k steps)')
ax2.set_xlim ((0,xmax))
ax2.set_ylim ((0,220))
for axis in ['top','bottom','left','right']:
    ax2.spines[axis].set_linewidth(lw)
    ax2.tick_params(width=lw)

ax3 = F1.add_subplot(1,3,3)
for i in range(np.shape(c_vs_t)[0]):
    ax3.plot(t1_masked, a_vs_t[i,:]-c_vs_t[i,:], '-', markersize=3, color=colmap[i], label='$c_{0}$'.format(i))

ax3.set_ylabel ('$\sum_{hexes} (a_i-c_i)$', rotation=0, labelpad=80)
ax3.set_xlabel ('t (10k steps)')
ax3.set_xlim ((0,xmax))
ax3.set_ylim ((0,1800))
for axis in ['top','bottom','left','right']:
    ax3.spines[axis].set_linewidth(lw)
    ax3.tick_params(width=lw)


plt.tight_layout()

plt.savefig('plots/a_vs_t.svg', transparent=True)

plt.show()
