#!/bin/bash

# Call the paper figure plotting scripts. Note that this generates SVG
# files which I then incorporate into Inkscape drawings, to generate
# the final figures.

python plot_honda_quick.py

python plot_paramsearch_paper.py

python plot_FigSensitivity.py
