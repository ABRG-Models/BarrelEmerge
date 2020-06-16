#!/bin/bash

# This calls all the intermediate processing scripts which are
# required to plot the figures for the paper.

python process_honda.sh ../logs/41N2M_thalguide_Fig1

python process_sensitivity_guide1.py

python process_gamma_noise.py

python process_guidance_noise.py

python process_paramsearch_comp2.py
