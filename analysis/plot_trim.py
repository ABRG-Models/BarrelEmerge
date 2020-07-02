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
F1 = plt.figure (figsize=(10,8.5))

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

ax1 = F1.add_subplot(2,1,1)
ax2 = F1.add_subplot(2,1,2)

xmax = max(tdc3[:]['eps_mult'])
xmin = min(tdc3[:]['eps_mult'])

others_size = 6
main_size = 12
m_width = 3

col_c3 = col.blue2
col_b3 = col.blue3
col_c2 = col.navy
col_c4 = col.cobalt
col_d2 = col.royalblue2
col_d3 = col.cornflowerblue


l1_map = ax1.plot([map_mult,map_mult], [0, 0.26], '--', color=col.black)
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdb3[:]['area'], 'v-', markersize=others_size, color=col_b3, label='B3')
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdc2[:]['area'], '^-', markersize=others_size, color=col_c2, label='C2')
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdc4[:]['area'], 'v-', markersize=others_size, color=col_c4, label='C4')
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdd2[:]['area'], '^-', markersize=others_size, color=col_d2, label='D2')
l1_1, = ax1.plot(tdb3[:]['eps_mult'], tdd3[:]['area'], 'v-', markersize=others_size, color=col_d3, label='D3')
l1, = ax1.plot(tdc3[:]['eps_mult'], tdc3[:]['area'], 's-', markersize=main_size, linewidth=m_width, color=col_c3, label='C3')
ax1.set_ylim([0,0.26])

ax1.text (0.54, 0.028, r'$A_{C3}$', fontsize=24, horizontalalignment='left', color=col_c3);
ax1.text (0.65, 0.07, r'$A_{B3}$', fontsize=18, horizontalalignment='left', color=col_b3);
ax1.text (0.72, 0.15, r'$A_{C2}$', fontsize=18, horizontalalignment='left', color=col_c2);
ax1.text (0.92, 0.19, r'$A_{C4}$', fontsize=18, horizontalalignment='left', color=col_c4);
ax1.text (0.78, 0.15, r'$A_{D2}$', fontsize=18, horizontalalignment='left', color=col_d2);
ax1.text (0.84, 0.15, r'$A_{D3}$', fontsize=18, horizontalalignment='left', color=col_d3);


l2_map = ax2.plot([map_mult,map_mult], [0, 0.11], '--', color=col.black)
l2_1, = ax2.plot(tdb3[:]['eps_mult'], tdb3[:]['hondadeltaj']/tdb3[:]['area'], 'v-', markersize=others_size, color=col_b3, label='B3')
l2_2, = ax2.plot(tdb3[:]['eps_mult'], tdd3[:]['hondadeltaj']/tdd3[:]['area'], 'v-', markersize=others_size, color=col_d3, label='D3')
l2_thresh, = ax2.plot((xmin,xmax), (0.055, 0.055), '--', color=col.red, linewidth=3, label="good (S&W)")
l2, = ax2.plot(tdc3[:]['eps_mult'], tdc3[:]['hondadeltaj']/tdc3[:]['area'], 's-', markersize=main_size, linewidth=m_width, color=col_c3, label='C3')

print ('eps_mult from all : {0}'.format(ad[:]['eps_mult']))
print ('hondadelta from all : {0}'.format(ad[:]['hondadelta']))
l2_overall, = ax2.plot(ad[:]['eps_mult'], ad[:]['hondadelta'], 'o-', markersize=main_size, linewidth=m_width, color=col.red, label='All')

ax2.text (0.72, 0.01, r'$\frac{\delta_{C3}}{A_{C3}}$', fontsize=24, horizontalalignment='left', color=col_c3);
ax2.text (0.77, 0.04, r'$\frac{\delta_{B3}}{A_{B3}}$', fontsize=18, horizontalalignment='left', color=col_b3);
ax2.text (0.85, 0.07, r'$\frac{\delta_{D3}}{A_{D3}}$', fontsize=18, horizontalalignment='left', color=col_d3);
ax2.text (0.51, 0.086, r'Honda-$\delta$', fontsize=18, horizontalalignment='left', color=col.red);


ax2.set_ylim([0,0.11])

ax1.set_xlim([0.5,1.0])
ax2.set_xlim([0.5,1.0])

ax1.set_xlabel ('$m$')
ax1.set_ylabel ('$Area$', labelpad=35)
ax2.set_xlabel ('$m$')
ax2.set_ylabel ('$\delta$', labelpad=22, rotation=0)

lw = 2; ll = 6
for axis in ['top','bottom','left','right']:
  ax1.spines[axis].set_linewidth(lw)
  ax1.tick_params(length=ll, width=lw)
  ax2.spines[axis].set_linewidth(lw)
  ax2.tick_params(length=ll, width=lw)

dx = 0/72.; dy = -10/72.
offset = matplotlib.transforms.ScaledTranslation (dx, dy, F1.dpi_scale_trans)
for label in ax1.xaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)
for label in ax2.xaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)

plt.tight_layout()

plt.savefig('plots/whisker_trim.svg', transparent=True)

plt.show()
