# Reproducing the results for this paper

Here's how to reproduce the results in this brief format paper. You'll
first need to compile the software - see the top level README for
instructions.

## Simulations

To reproduce the figures in this paper, you can run the
simulations, then plot the results.

Before running the simulations, you will need to modify each config
and replace the value of field "logbase". The value
"/home/seb/gdrive_usfd/data/BarrelEmerge" should instead be changed to
some directory on your computer. In the following instructions I'll
call that ${LOGBASE} or LOGBASE. You could set LOGBASE on your command
line to run the following scripts:

```bash
export LOGBASE=/home/seb/gdrive_usfd/data/BarrelEmerge
```

## Figs 1C and Fig 1D

The config for the simulation which gives the results shown in Fig 1,
panels C and D is

```
BarrelEmerge/configs/rat/41N2M_thalguide_eps150.json
```

So run the 'divisive normalization plus competition' executable on
this config:

```bash
cd BarrelEmerge
./build/sim/james_dncomp configs/rate/41N2M_thalguide_eps150.json
```

The results should be written, in HDF5 format, into the directory ${LOGBASE}/41N2M_thalguide_eps150.

## Fig1E

The results in Fig 1E come from a second simulation with a different
json config file.

Don't forget to edit "logbase" in BarrelEmerge/configs/rat/41N2M_thalguide_eps80_FgfMis.json,
then run:

```bash
cd BarrelEmerge
./build/sim/james_dncomp configs/rate/41N2M_thalguide_eps80_FgfMis.json
```

## Plots

### Fig 1A

The map of initial values [a_1(x,t=0)] can be plotted with

```bash
cd BarrelEmerge/analysis
# writeme
```

The guidance maps can be plotted with

```bash
cd BarrelEmerge/analysis
python plot_guidance.py ${LOGBASE}/41N2M_thalguide_eps150 0
python plot_guidance.py ${LOGBASE}/41N2M_thalguide_eps150 1
```

### Fig 1B

Plot Fig 1B with:

```bash
cd BarrelEmerge/boundaries/barreloids
python barreloids_haidarliu_Fig5d.py
```

This also outputs the interaction parameters on stdout in the format
in which they were then inserted into the relevant json config files.

### Fig 1C

```bash
cd BarrelEmerge/analysis
python plot_cid.py ${LOGBASE}/41N2M_thalguide_eps150 1000
python plot_cid.py ${LOGBASE}/41N2M_thalguide_eps150 10000
python plot_cid.py ${LOGBASE}/41N2M_thalguide_eps150 25000
```

### Fig 1D

```bash
cd BarrelEmerge/analysis
# Generates numbers in ./postproc and plots graph with wrong colours:
python plot_honda.py ${LOGBASE}/41N2M_thalguide_eps150
# Uses ./postproc/*.npy and plots like the paper figure:
python plot_honda_quick.py
```

### Fig 1E

```bash
cd BarrelEmerge/analysis
# Guidance:
python plot_guidance.py ${LOGBASE}/41N2M_thalguide_eps80_FgfMis 0
python plot_guidance.py ${LOGBASE}/41N2M_thalguide_eps80_FgfMis 1
# Connection density:
python plot_cid_fgfmis.py ${LOGBASE}/41N2M_thalguide_eps80_FgfMis 25000
```

## The movie

To reproduce the movie, get yourself a fast computer and (not
forgetting to edit "logbase" in the config first) run:

```bash
cd BarrelEmerge
./build/sim/james_dncomp configs/rate/41N2M_thalguide_eps150_movie.json
```

Now create all the pngs:

```bash
cd BarrelEmerge/analysis
python plot_cid_all.py ${LOGBASE}/41N2M_thalguide_eps150
```

Finally stitch the pngs together:

```bash
WRITEME. which movie script did I use from misc?
```
