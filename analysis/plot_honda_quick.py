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
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

# And plot this longhand here:
F1 = plt.figure (figsize=(9,8))

t1_masked = np.load ('postproc/honda_t.npy')/10000
hondadelta = np.load ('postproc/honda_delta.npy')
area_measure =  np.load ('postproc/area_measure.npy')

xmax = max(t1_masked)
xmax = xmax[0]
print ('xmax = {0}'.format(xmax))
ax1 = F1.add_subplot(1,1,1)
l1, = ax1.plot(t1_masked, hondadelta, 'o', markersize=12, color=col.red, label='Honda $\delta$')

l2, = ax1.plot((0,xmax), (0.055, 0.055), '--', color=col.red, linewidth=3, label="good (S&W)")
#l3, = ax1.plot((0,xmax), (0.15, 0.15), '-.', color=col.black, linewidth=3, label="awful (non Dirichlet)")

ax2 = ax1.twinx()

l4, = ax2.plot(t1_masked, area_measure, 's', markersize=12, color=col.black)

ax1.set_xlabel ('10k steps')
ax1.set_ylabel ('$\delta$',rotation=0)
ax2.set_ylabel ('$\sigma$',rotation=0)
ax2.tick_params (axis='y', labelcolor=col.black)
ax1.set_xlim ((0,xmax))
ax1.set_ylim ((0,0.3))
ax2.set_ylim ((0,500))
ax1.set_xticks ((0,1,2))
ax1.set_yticks ((0,0.1,0.2,0.3))
ax2.set_yticks ((0,200,400))

plt.tight_layout()
suffix= '_quick'
plt.savefig('plots/hondadelta{0}.svg'.format(suffix), transparent=True)

plt.show()
