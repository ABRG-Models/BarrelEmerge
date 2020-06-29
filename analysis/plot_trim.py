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

# Set plotting defaults
fs = 26
fnt = {'family' : 'Arial',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

# IMPORTANT for svg output of text as things that can be edited in inkscape
plt.rcParams['svg.fonttype'] = 'none'

# And plot this longhand here:
F1 = plt.figure (figsize=(10,12))

## load data from csv
trimdata = np.genfromtxt ('postproc/whisker_trim_individual.csv', delimiter=",", names=True)
td = np.sort (trimdata, order='barrel')

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

ax1 = F1.add_subplot(3,1,1)
ax2 = F1.add_subplot(3,1,3)
ax3 = F1.add_subplot(3,1,2)

xmax = max(tdc3[:]['eps_mult'])
xmin = min(tdc3[:]['eps_mult'])

others_size = 6
main_size = 12

col_b3 = col.blue3
col_c2 = col.navy
col_c4 = col.cobalt
col_d2 = col.royalblue2
col_d3 = col.cornflowerblue


l1_map = ax1.plot([map_mult,map_mult], [0, 0.26], '-.', color=col.black)
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdb3[:]['area'], 'o', markersize=others_size, color=col_b3, label='B3')
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdc2[:]['area'], 'o', markersize=others_size, color=col_c2, label='C2')
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdc4[:]['area'], 'o', markersize=others_size, color=col_c4, label='C4')
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdd2[:]['area'], 'o', markersize=others_size, color=col_d2, label='D2')
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdd3[:]['area'], 'o', markersize=others_size, color=col_d3, label='D3')
l1, = ax1.plot(tdc3[:]['eps_mult'], tdc3[:]['area'], 'o', markersize=main_size, color=col.red, label='C3')
ax1.set_ylim([0,0.26])

l2_map = ax2.plot([map_mult,map_mult], [0, 0.06], '-.', color=col.black)
l2_1, = ax2.plot(tdb3[:]['eps_mult'], tdb3[:]['hondadelta'], 'o', markersize=others_size, color=col_b3, label='B3')
l2_2, = ax2.plot(tdb3[:]['eps_mult'], tdd3[:]['hondadelta'], 'o', markersize=others_size, color=col_d3, label='D3')
l2_thresh, = ax2.plot((xmin,xmax), (0.055, 0.055), '--', color=col.red, linewidth=3, label="good (S&W)")
l2, = ax2.plot(tdc3[:]['eps_mult'], tdc3[:]['hondadelta'], 'o', markersize=main_size, color=col.red, label='C3')
ax2.set_ylim([0,0.06])

l3_map = ax3.plot([map_mult,map_mult], [0, 0.2], '-.', color=col.black)
l3_1, = ax3.plot(tdb3[:]['eps_mult'], tdb3[:]['area_diff'], 'o', markersize=others_size, color=col_b3, label='B3')
l3_1, = ax3.plot(tdb3[:]['eps_mult'], tdc2[:]['area_diff'], 'o', markersize=others_size, color=col_c2, label='C2')
l3_1, = ax3.plot(tdb3[:]['eps_mult'], tdc4[:]['area_diff'], 'o', markersize=others_size, color=col_c4, label='C4')
l3_1, = ax3.plot(tdb3[:]['eps_mult'], tdd2[:]['area_diff'], 'o', markersize=others_size, color=col_d2, label='D2')
l3_1, = ax3.plot(tdb3[:]['eps_mult'], tdd3[:]['area_diff'], 'o', markersize=others_size, color=col_d3, label='D3')
l3, = ax3.plot(tdc3[:]['eps_mult'], tdc3[:]['area_diff'], 'o', markersize=main_size, color=col.red, label='C3')
ax3.set_ylim([0,0.2])

ax1.set_xlim([0.5,1.0])
ax2.set_xlim([0.5,1.0])
ax3.set_xlim([0.5,1.0])


ax1.set_xlabel ('$\epsilon_m$')
ax1.set_ylabel ('$\Omega$', labelpad=30)
ax2.set_xlabel ('$\epsilon_m$')
ax2.set_ylabel ('$\delta$', labelpad=16)
ax3.set_xlabel ('$\epsilon_m$')
ax3.set_ylabel ('$\Delta\Omega$', labelpad=30)

lw = 2
for axis in ['top','bottom','left','right']:
  ax1.spines[axis].set_linewidth(lw)
  ax1.tick_params(width=lw)
  ax2.spines[axis].set_linewidth(lw)
  ax2.tick_params(width=lw)
  ax3.spines[axis].set_linewidth(lw)
  ax3.tick_params(width=lw)

plt.tight_layout()

plt.savefig('plots/whisker_trim.svg', transparent=True)

plt.show()
