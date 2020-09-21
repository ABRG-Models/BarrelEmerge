# Analysis scripts

These scripts analyse the HDF5 data files which the simulations
produce. For the scripts to generate the HDF5 files, see ../scripts/.

Many of the plots are generated not directly from the HDF5 files, but
from .npy or .csv files which the process_*.py scripts create.

## include/

Contains python code used by several of the scripts in this
directory. Especially BarrelData.py, which loads the HDF5 files which
the BarrelEmerge simulations produce and paramplot.py which contains
code to plot the parameter search results.

## plots/

A directory into which generated plots are written, and which also
contains some movie-making scripts.

## postproc/

Contains the output of process_*.py. The results plotted in the paper
are revision controlled in here.

## old/

Previous versions of scripts. Old stuff.

## Process scripts

This scripts process data which I generated from the simulations and
stored in a directory tree on my machine in
$HOME/gdrive_usfd/data/BarrelEmerge/

The reproduce the results, each script will need to be modified with
the path that you used to generate the simulated results.

### process_gamma_noise.py
Generates postproc/gamma_noise.csv. For plot_FigSensitivity.py (Fig. 3).

### process_guidance_noise.py
Generates postproc/guidance_noise.csv. For plot_FigSensitivity.py (Fig. 3).

### process_honda.py
Generates the files

* postproc/adjacency_arrangement.npy
* postproc/adjacency_differencemag.npy
* postproc/area_diff.npy
* postproc/a_vs_t.npy
* postproc/c_vs_t.npy
* postproc/honda_delta.npy
* postproc/honda_t.npy
* postproc/locn_vs_t.npy
* postproc/map_diff.npy
* postproc/sos_dist.npy

Used by plot_honda.py, which plots various metrics
(delta, omega, eta) vs. time for a simulation run provided as the
first argument to the script. Also used by plot_a_c_vs_t.py

### process_paramsearch_comp2.py

Processes all 216 runs from the parameter
search into the csv file postproc/paramsearch_k3.0_comp2.csv

### process_sensitivity_guide1.py

generates sensitivity_guide1.csv,
required for plot_FigSensitivity.py to plot Fig. 3 from the paper.

### process_whisker_trim.py

Process individual whisker trim data.

Generates whisker_trim_individual.csv which contains the individual
barrel metrics and whisker_trim_overall.csv which contains the overall
pattern metrics.

### process_whisker_rowtrim.py

Process whisker row trim data.

Generates whisker_rowtrim_individual.csv which contains the individual
barrel metrics and whisker_rowtrim_overall.csv which contains the
overall pattern metrics.

## Statistics scripts

stats_multirun_normal.py, stats_multirun_anoiseless.py,
stats_multirun_anoise.py and stats_ttest.py are all scripts used to
investigate the model and its sensitivity to the initial condition for
a_i. Reported in the text of the paper.

## Plot scripts

### plot_a_c_vs_t.py

Plots a graph of a and c vs. t showing that these are conserved with
time. Figure not included in paper.

### plot_aid.py

Example:
```
plot_aid.py ../logs/41N2M_thalguide_Fig1/ 30000
```

Plot a colour map of argmax(a_i) at time 30000 from the simulation results in
../logs/41N2M_thalguide_Fig1/. Adjust time to suit. Figures for
argmax(a_i) are not included in the paper.

### plot_aid_all.py

Plot a maps for all times. Used to make up movie frames (takes a long
time to run).

### plot_a.py

Example:
```
plot_a.py ../logs/41N2M_thalguide_Fig1/ ${t}
```
plots a_0 at time t. To plot a different one of the a variables
(such as a_1 or a_10), tweak the script. This is used to generate the
initial condition plot in Fig 1.B.

### plot_cid.py
```
plot_cid.py ../logs/41N2M_thalguide_Fig1/ 30000
```

Plot a colour map of argmax(c_i) at time 30000 from the simulation results in
../logs/41N2M_thalguide_Fig1/. Adjust time to suit. Used to generate
maps in Fig. 1C, Fig. 2B, Fig. 3B and Fig. 4C in the paper.

### plot_cid_all.py

Like plot_aid_all.py, but for argmax(c). Used to print frames for the
movie that accompanies the paper.

### plot_cid_fgfmis.py

Like plot_cid.py, but for the Fgf8 misexpression experiment. Fig. 4B in
the paper.

### plot_FigSensitivity.py

Plots Fig 3A from the paper, the sensitivity analysis.

### plot_guidance.py

Example:
```
python plot_guidance.py ../logs/41N2M_thalguide_Fig1/ 0 # or 1
```
Plot a greyscale map of the guidance field 0 (or 1). Used to plot
parts of Fig. 1B.

### plot_honda.py

Plot the graphs included in Fig. 1D.

### plot_locn.py

Example:
```
python plot_locn.py ../logs/41N2M_thalguide_Fig1/ ${t}
```
Plot the selectivity measure, mu(x, t). Shown in Fig. 1E.

### plot_paramsearch_paper.py

Plot the components of Fig. 2.

### plot_singlemap.py

A bit like plot_cid.py, but ALSO plots the
experimental map, in a separate window. Figures not shown in paper.

### plot_trim_areaonly.py

Plot the graph for Fig. 4D.
