# Make the whisker trimming line plot (barrel area vs epsilon, etc)

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
import matplotlib.transforms

# Set plotting defaults
fs = 26
fnt = {'family' : 'Arial',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

# IMPORTANT for svg output of text as things that can be edited in inkscape
plt.rcParams['svg.fonttype'] = 'none'

# And plot this longhand here:
F1 = plt.figure (figsize=(10,6))

## load data from csv
trimdata = np.genfromtxt ('postproc/whisker_trim_individual.csv', delimiter=",", names=True)
td = np.sort (trimdata, order='barrel')

alldata = np.genfromtxt ('postproc/whisker_trim_overall.csv', delimiter=",", names=True)
ad = np.sort (alldata, order='eps_mult')

# Show an example map for this multiplier
map_mult = 0.64

# Get per-barrel results
# barrels of interest are: B3, C2, C3, C4, D2, D3
#              TC indices:  8, 12, 13, 14, 22, 23
tdc3 = td[td[:]['barrel_index'] == 13] # C3
tdb3 = td[td[:]['barrel_index'] == 8]  # B3
tdc2 = td[td[:]['barrel_index'] == 12]
tdc4 = td[td[:]['barrel_index'] == 14]
tdd2 = td[td[:]['barrel_index'] == 22]
tdd3 = td[td[:]['barrel_index'] == 23]

ax1 = F1.add_subplot(1,1,1)

xmax = max(tdc3[:]['eps_mult'])
xmin = min(tdc3[:]['eps_mult'])

others_size = 6
main_size = 12
m_width = 3

col_c3 = col.black
col_b3 = col.blue3
col_c2 = col.navy
col_c4 = col.cobalt
col_d2 = col.royalblue2
col_d3 = col.cornflowerblue
col_others = col.gray50


l1_map = ax1.plot([map_mult,map_mult], [0, 0.16], '--', color=col.gray70)

# Compute mean values of the neighbouring areas:
others = np.vstack ((tdb3[:]['area'], tdc2[:]['area'], tdc4[:]['area'], tdd2[:]['area'], tdd3[:]['area']))
mn_oth = np.mean(others, axis=0)

l1_1, = ax1.plot(tdb3[:]['eps_mult'], mn_oth, 'o-', markersize=main_size, linewidth=m_width, color=col_others, label='Neighbours')
l1, = ax1.plot(tdc3[:]['eps_mult'], tdc3[:]['area'], 's-', markersize=main_size, linewidth=m_width, color=col_c3, label='C3')

ax1.set_xlim([0.5,1.0])
ax1.set_ylim([0,0.16])

ax1.text (0.55, 0.022, 'C3', fontsize=24, horizontalalignment='left', color=col.black);
ax1.text (0.67, 0.144, 'Neighbours', fontsize=24, horizontalalignment='left', color=col.black);


ax1.set_xlabel ('$m$')
ax1.set_ylabel ('$Area$', labelpad=25)

lw = 2; ll = 6
for axis in ['top','bottom','left','right']:
  ax1.spines[axis].set_linewidth(lw)
  ax1.tick_params(length=ll, width=lw)

# Shift x axis labels down a bit
dx = 0/72.; dy = -10/72.
offset = matplotlib.transforms.ScaledTranslation (dx, dy, F1.dpi_scale_trans)
for label in ax1.xaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)

plt.tight_layout()

plt.savefig('plots/whisker_trim.svg', transparent=True)

plt.show()
