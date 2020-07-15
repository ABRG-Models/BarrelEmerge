#!/bin/bash

#LOGDIR=~/gdrive_usfd/data/BarrelEmerge
LOGDIR=../logs

# Call the paper figure plotting scripts. Note that these generate PNG
# and SVG files which I then incorporate into Inkscape drawings, to
# generate the final figures. Find output in ./plots/

# Fig 1 C
python plot_cid.py ${LOGDIR}/41N2M_thalguide_Fig1  1000
python plot_cid.py ${LOGDIR}/41N2M_thalguide_Fig1 10000
python plot_cid.py ${LOGDIR}/41N2M_thalguide_Fig1 30000

# Fig 1 D
python plot_honda_quick.py

python plot_paramsearch_paper.py

python plot_FigSensitivity.py

# Sensitivity example maps:
# Fig 3 B i
python plot_cid.py ${LOGDIR}/gamma_noise/gammanoise_gain1.0/ 30000

# Fig 3 B ii
python plot_cid.py ${LOGDIR}/guidance_noise/gmn_gain0.6_sigma0.022/ 30000

# Fig 3 B iii
python plot_cid.py ${LOGDIR}/sensitivity_guide1/sa_comp2_p1_6_g1_0.1/ 30000

# Fig 3 B iv
python plot_cid.py ${LOGDIR}/sensitivity_guide1/sa_comp2_p1_46_g1_1.0/ 30000

# Fig 4 A

# Fig 4 B

# Fig 4 C
python plot_cid.py ${LOGDIR}/whisker_trim/whisktrim_C3_mult_0.86/ 30000

# Fig 4 D
python plot_trim_areaonly.py
