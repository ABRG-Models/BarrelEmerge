#!/bin/zsh

# Run simulations on a rectangular domain.
#
# Start with a strong L-R guidance gradient, relative to the U-D
# guidance. Gradually move to a strong U-D gradient and weak L-R
# gradient.

# Check we're running from BarrelEmerge dir
CURDIR=$(pwd | awk -F '/' '{print $NF}')
echo "CURDIR: $CURDIR"

if [ ! $CURDIR = "BarrelEmerge" ]; then
    echo "Run from the base BarrelEmerge directory; i.e. ./scripts/$0"
    exit 1
fi

NUMSTEPS=10 # Actually, there'll be NUMSTEPS+1 simulations...
for i in $(seq 0 $NUMSTEPS); do

    UDGAIN=$(( i * 1.0/${NUMSTEPS} ))
    typeset -F 1 UDGAIN
    LRGAIN=$(( 1.0 - ($i * 1.0/${NUMSTEPS}) ))
    typeset -F 1 LRGAIN

    echo "i: $i, UD gain = ${UDGAIN}, LR gain = ${LRGAIN}"

    cat > configs/rel_guide_strengths_sq_UD${UDGAIN}.json <<EOF
{
    // Global simulation parameters
    "steps" : 24000,
    "logevery": 1000,
    "overwrite_logs": true,
    "hextohex_d" : 0.02,
    "svgpath" : "./boundaries/square.svg",
    "boundaryFalloffDist" : 0.01,
    "D" : 0.2,
    "E" : 0.0,

    // Exponent parameters
    "k" : 3,
    "l" : 1,

    // Timestep. Defaults to 0.00001 if omitted here
    "dt" : 0.00005,

    "contour_threshold" : 0.2,

    "do_dirichlet_analysis" : true,

    "aNoiseGain" : 0.2,
    "aInitialOffset" : 0.2,

    // Array of parameters for N thalamocortical populations.
    "tc": [
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-2,-2] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-1,-2] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [0,-2] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [1,-2] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [2,-2] }
        ,
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-2,-1] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-1,-1] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [0,-1] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [1,-1] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [2,-1] }
        ,
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-2,0] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-1,0] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [0,0] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [1,0] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [2,0] }
        ,
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-2,1] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-1,1] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [0,1] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [1,1] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [2,1] }
        ,
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-2,2] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [-1,2] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [0,2] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [1,2] },
        { "alpha" : 3, "beta" : 20, "epsilon" : 200,
          "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0,
          "gamma" : [2,2] }
    ], // end tc

    // Array of parameters for the guidance molecules
    "guidance": [
        {
            "shape"  : "Linear1D",
            "time_onset" : 0,
            "gain"   : ${UDGAIN},
            "phi"    : -90, // From high at bottom to low at top
            "width"  : 0.1,
            "offset" : 0.0 // 0.65
        },
        {
            "shape"  : "Linear1D",
            "time_onset" : 0,
            "gain"   : ${LRGAIN},
            "phi"    : 0, // From high at right to low at left
            "width"  : 0.1,
            "offset" : 0.0
        }
    ] // end guidance
}
EOF

    # Computation only version of the sim prog:
    ./build/sim/james_dncompc configs/rel_guide_strengths_sq_UD${UDGAIN}.json
    RTN=$?
    if [ $RTN -ne "0" ]; then
        echo "Exiting"
        exit 1
    fi

done

# Success/completion
exit 0
