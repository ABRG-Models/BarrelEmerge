## Scripts

Scripts to re-generate the simulation data presented in the paper. To
run these scripts, you must first build the software in a directory
called build/. See the top level README.md for instructions.

If you run all of the scripts listed here, then you will have
generated all the data to reproduce the results in our paper.

I would suggest running just main_results.sh first, which only takes
about 15 minutes and allows you to watch the simulation as it computes.

### main_results.sh

This runs two simulations; the simulation whose results are presented
in Fig. 1 and the sim which is shown in Fig. 4. Examine this script to
see how to run the simulations one by one.

### paramexplore_comp2.sh

Runs the Fig 1 simulation 216 times with different values of the
parameters D, epsilon(aka F) and alpha/beta. Care! This will take
about a day on a fast computer.

### multirun_anoiseless.sh, multirun_anoise.sh and multirun_comp2.sh

Run these three scripts to generate 10 runs of the Fig 1 sim, with
varying levels of initial noise in a_i(t=0).

### gamma_noise.sh

Runs the simulation with varying levels of noise in the interaction
(gamma) parameters (Fig 3).

### guidance_noise.sh

Runs the simulation with varying levels of noise in the guidance
fields (Fig 3).

### sensitivity_guide1.sh

Runs the simulation with perturbations to the guidance fields (Fig 3).
