#!/bin/zsh

# Run the simulation for the two main results using the configurations
# in configs/rat/. You can either run this script (making sure to
# close the window after each simulation finishes (keep an eye on
# stdout) OR you can copy the command lines and run them yourself, one
# by one. To run without the graphical window, add 'c' to the end of
# the command; e.g.:
# ./build/sim/james_comp2c ./configs/rat/41N2M_thalguide_Fig1.json

# Check we're running from BarrelEmerge dir
CURDIR=$(pwd | awk -F '/' '{print $NF}')
echo "CURDIR: $CURDIR"

if [ ! $CURDIR = "BarrelEmerge" ]; then
    echo "Run from the base BarrelEmerge directory; i.e. ./scripts/$0"
    exit 1
fi

# Fig 1, main image
echo "Running simulation for Fig 1..."
CONFIG="./configs/rat/41N2M_thalguide_Fig1.json"
# If using james_comp2 fails because you didn't compile with OpenGL,
# try james_comp2c instead of james_comp2:
./build/sim/james_comp2 ${CONFIG}

# Fig 4b, Fgf misexpression
echo "Running simulation for Fig 4b..."
CONFIG="./configs/rat/41N2M_thalguide_Fig4ab.json"
./build/sim/james_comp2 ${CONFIG}

# Fig 4c, Whisker trimming
echo "Running simulation for Fig 4cd..."
CONFIG="./configs/rat/41N2M_thalguide_Fig4cd.json"
./build/sim/james_comp2 ${CONFIG}

# Success/completion
exit 0
