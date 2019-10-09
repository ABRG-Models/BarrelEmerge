#!/bin/zsh

# Run simulations on a rectangular domain.
#
# To see how the Honda measure changes wrt epsilon

# Check we're running from BarrelEmerge dir
CURDIR=$(pwd | awk -F '/' '{print $NF}')
echo "CURDIR: $CURDIR"

if [ ! $CURDIR = "BarrelEmerge" ]; then
    echo "Run from the base BarrelEmerge directory; i.e. ./scripts/$0"
    exit 1
fi

for EPSILON in $(seq 25 25 300); do

    JSON="voronoi_vs_epsilon_${EPSILON}.json"

    echo "i: $i, epsilon = ${EPSILON}"

    cat > configs/${JSON} <<EOF
{
    // Global simulation parameters
    "steps" : 100000,
    "logevery": 1000,
    "overwrite_logs": true,
    "hextohex_d" : 0.015,
    "svgpath" : "./boundaries/whiskerbarrels.svg",
    "boundaryFalloffDist" : 0.01,
    "D" : 0.2,
    "E" : 0.0,

    // Exponent parameters
    "k" : 3,
    "l" : 1,

    // Timestep. Defaults to 0.00001 if omitted here
    "dt" : 0.00001,

    "contour_threshold" : 0.2,

    "do_dirichlet_analysis" : true,

    "aNoiseGain" : 0.2,
    "aInitialOffset" : 0.2,

    "tc": [
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-2.5, -2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.5, -2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.5, -2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 0.5, -2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 1.5, -2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 2.5, -2.5] },
        //
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-2.5, -1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.5, -1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.5, -1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 0.5, -1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 1.5, -1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 2.5, -1.5] },
        //
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-2.5,  -0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.5,  -0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.5,  -0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 0.5,  -0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 1.5,  -0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 2.5,  -0.5] },
        //
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-2.5, 0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.5, 0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.5, 0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 0.5, 0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 1.5, 0.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 2.5, 0.5] },
        //
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-2.5, 1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.5, 1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.5, 1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 0.5, 1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 1.5, 1.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 2.5, 1.5] },
        //
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-2.5, 2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.5, 2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.5, 2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 0.5, 2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 1.5, 2.5] },
        { "alpha" : 3, "beta" : 20, "epsilon" : ${EPSILON}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [ 2.5, 2.5] }
    ], // end tc

    // Array of parameters for the guidance molecules
    "guidance": [
        {
            "shape"  : "Linear1D",
            "time_onset" : 0,
            "gain"   : 1.0,
            "phi"    : -90, // From high at bottom to low at top
            "width"  : 0.1,
            "offset" : 0.0 // 0.65
        },
        {
            "shape"  : "Linear1D",
            "time_onset" : 0,
            "gain"   : 1.0,
            "phi"    : 0, // From high at right to low at left
            "width"  : 0.1,
            "offset" : 0.0
        }
    ] // end guidance
}
EOF

    # Computation only version of the sim prog:
    ./build/sim/james_dncompc configs/${JSON}
    RTN=$?
    if [ $RTN -ne "0" ]; then
        echo "Exiting"
        exit 1
    fi

done

# Success/completion
exit 0
