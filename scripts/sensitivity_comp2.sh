#!/bin/zsh

# Explore the sensitivity of the 41N2M system from the paper to its
# inputs - that means the gradients of the 2 guidance molecules (phi and
# gain) and some subset of the 82 gammas.

# Check we're running from BarrelEmerge dir
CURDIR=$(pwd | awk -F '/' '{print $NF}')
echo "CURDIR: $CURDIR"

if [ ! $CURDIR = "BarrelEmerge" ]; then
    echo "Run from the base BarrelEmerge directory; i.e. ./scripts/$0"
    exit 1
fi

PROGTAG=comp2 # NOT dccomp because in comp2 we need to vary F, not epsilon

# Model parameters - these should match model in Fig 1 of the paper.
k=3
D=0.5
F=1.2
ALPHA=3.6
BETA=16.67
DT=0.0001
HEXHEXD=0.03
# Boundary fall off distance - should be at least 3 times HEXHEXD
BFD=0.1
# Noise on a
ANG=0.2 # gain
ANO=0.2 # offset

CONFIG_DIR="configs/rat/sensitivity"

PHI2=-84
GAIN2=1.0
#PHI1=6

for PHI1 in -34 -14 6 26 46; do
    for GAIN1 in 0.1 0.5 1.0; do

            JSON="sa_${PROGTAG}_p1_${PHI1}_g1_${GAIN1}.json"

            cat > ${CONFIG_DIR}/${JSON} <<EOF
{
    "steps" : 30000,
    "logevery": 30000,
    "overwrite_logs": true,
    "logbase" : "/home/seb/gdrive_usfd/data/BarrelEmerge/sensitivity_comp2/",
    //"logbase" : "/home/seb/paramexplore_comp2/",
    "hextohex_d" : ${HEXHEXD}, // Hex to hex distance, determines num hexes
    "svgpath" : "./boundaries/rat_barrels/wb_110405_Dirichlet.svg",
    "boundaryFalloffDist" : ${BFD},
    "G" : 1.0,     // gamma gain
    "dt" : ${DT}, // Timestep. Defaults to 0.00001 if omitted here

    // Initial conditions parameters
    "aNoiseGain" : ${ANG},
    "aInitialOffset" : ${ANO},

    // Parameters that will vary
    "D" : ${D},
    "F" : ${F},
    "k" : ${k},    // Exponent on a
    // Also: alpha, beta, epsilon; see gamma list below

    // Array of parameters for N thalamocortical populations.
    "tc": [
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-2.0, 0.08297875929160803], "name" : "a" }, // a
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.841803677231407, 0.5955182340971339], "name" : "A1" }, // A1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.5766667867404216, 0.8026650330176572], "name" : "A2" }, // A2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.3229961206880625, 1.006728138855208], "name" : "A3" }, // A3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.0786832474038208, 1.2453982728569302], "name" : "A4" }, // A4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.5844170937774447, -0.6347093364107037], "name" : "b" }, // b
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.429349946121596, -0.11059706135929037], "name" : "B1" }, // B1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-1.0972823920313275, 0.07734661081184946], "name" : "B2" }, // B2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.8099920474672921, 0.3399097533912725], "name" : "B3" }, // B3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.5865031913897942, 0.6101032224741925], "name" : "B4" }, // B4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.9942346059227621, -1.4045569920900212], "name" : "c" }, // c
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.9686071613071959, -0.7666815324426732], "name" : "C1" }, // C1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.586423738301838, -0.6271724432962702], "name" : "C2" }, // C2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.17997842955291926, -0.3945562892438259], "name" : "C3" }, // C3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.004934757689654623, -0.07282464925911292], "name" : "C4" }, // C4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.1649578956687497, 0.3412494181486343], "name" : "C5" }, // C5
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.21421992832302666, 0.799862666426935], "name" : "C6" }, // C6
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.26218951193176776, 1.1715461833621803], "name" : "C7" }, // C7
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.33726853993680656, 1.4886078363126574], "name" : "C8" }, // C8
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.40919131586503565, 1.8171952179208173], "name" : "C9" }, // C9
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.3072392928763717, -1.9381596935842134], "name" : "d" }, // d
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.43567894000290097, -1.415767013494814], "name" : "D1" }, // D1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [-0.0012243177344666845, -1.2870289629201288], "name" : "D2" }, // D2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.595325752177874, -1.164354839691761], "name" : "D3" }, // D3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.848405242531084, -0.7748322941280898], "name" : "D4" }, // D4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.9184912923921059, -0.34774238093098786], "name" : "D5" }, // D5
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.9695900511135901, 0.01236833575836993], "name" : "D6" }, // D6
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.9108447397408347, 0.36784618960465654], "name" : "D7" }, // D7
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.8658048696529359, 0.764054051589858], "name" : "D8" }, // D8
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.9262515102858337, 1.0895948643062088], "name" : "D9" }, // D9
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.9919727455227539, 1.4412635454208589], "name" : "D10" }, // D10
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [0.5242198246896889, -2.0], "name" : "E1" }, // E1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [1.3370373323610558, -1.9926063552933613], "name" : "E2" }, // E2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [1.9015589553746204, -1.7052622130395196], "name" : "E3" }, // E3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [2.0, -1.2458372556900064], "name" : "E4" }, // E4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [1.9730105641076467, -0.733403905101111], "name" : "E5" }, // E5
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [1.7773685477785337, -0.32800135109841433], "name" : "E6" }, // E6
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [1.7752691611496592, 0.09208957206744639], "name" : "E7" }, // E7
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [1.7554451998566696, 0.53224240264211], "name" : "E8" }, // E8
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [1.7187892777721283, 0.9430795811620478], "name" : "E9" }, // E9
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [1.810673189604652, 1.2894098145790438], "name" : "E10" }
    ], // end tc

    // Array of parameters for the guidance molecules
    "guidance": [
        {
            "shape"  : "Linear1D", // 'x'
            "gain"   : ${GAIN1},
            "phi"    : ${PHI1},
            "width"  : 0.1,
            "offset" : 0.0
        },
        {
            "shape"  : "Linear1D", // 'y'
            "gain"   : ${GAIN2},
            "phi"    : ${PHI2}, // -84
            "width"  : 0.1,
            "offset" : 0.0
        }
    ], // end guidance

    "contour_threshold" : 0.35,

    // Visualization parameters (ignored by computation-only binaries)
    "win_width_contours": 800,
    "x_default": -3.38512,
    "y_default": -0.491072,
    "z_default": -11.5,
    "plotevery": 500,
    "vidframes": false,    // If true, number video frame saves consecutively, rather than by simulation step number
    "rhoInit": 4, // Larger to zoom out
    //
    "plot_guide" : true,
    "plot_contours" : true,
    "plot_a_contours" : false,
    "plot_a" : false,
    "plot_c" : false,
    "plot_n" : false,
    "scale_a" : false,
    "scale_c" : false,
    "scale_n" : false,

    //
    "plot_guidegrad" : false,
    "plot_divg" : false,
    "plot_divJ" : false,
    "plot_dr": true,
    "do_dirichlet_analysis": true,
    "plot_dr_with_guide" : false
}
EOF
            # A version of the sim prog:
            echo "./build/sim/james_${PROGTAG}c ${CONFIG_DIR}/${JSON}"
            ./build/sim/james_${PROGTAG}c ${CONFIG_DIR}/${JSON}
            RTN=$?
            if [ $RTN -ne "0" ]; then
                echo "Config: ${CONFIG_DIR}/${JSON} FAILED. Moving on to next."
            fi
        done
    done
done

# Success/completion
exit 0
