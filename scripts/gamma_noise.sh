#!/bin/zsh

# Explore the sensitivity of the 41N2M system from the paper to its
# gamma inputs. Add random noise to all the gammas, to varying levels.

# Check we're running from BarrelEmerge dir
CURDIR=$(pwd | awk -F '/' '{print $NF}')
echo "CURDIR: $CURDIR"

if [ ! $CURDIR = "BarrelEmerge" ]; then
    echo "Run from the base BarrelEmerge directory; i.e. ./scripts/$0"
    exit 1
fi

# Model parameters - these should match model in Fig 1 of the paper.
k=3
D=0.5
EPS=1.2
ALPHA=3.6
BETA=16.67
DT=0.0001
HEXHEXD=0.03
# Boundary fall off distance - should be at least 3 times HEXHEXD
BFD=0.1
# Noise on a
ANG=0.2 # gain
ANO=0.2 # offset

CONFIG_DIR="configs/rat/gamma_noise"

PHI1=6
GAIN1=1.0
PHI2=-84
GAIN2=1.0

# Test:
#for g in `./build/sim/randomgammas 0.01`; do
#    echo "Random gamma: ${g}"
#done
#exit 0

# Barrel B4
for gamma_noise_mag in 0.001 0.002 0.005 0.01 0.02 0.05 0.1 0.2 0.3 0.4 0.5 0.55 0.6 0.65 0.7 0.75 1.0 1.5 2.0 2.5; do
    JSON="gammanoise_gain${gamma_noise_mag}.json"

    # Now generate 82 random numbers to add to the gammas, below. Do
    # this using a custom c++ progam, which will output 82 numbers on
    # stdout according to cmd line arguments.
    GN=() # empty array for gamma noise
    for g in `./build/sim/randomgammas ${gamma_noise_mag}`; do
        #echo "Random gamma: $((g))"
        GN+=($((g)))
    done
    #echo "GN[1]: $((GN[1]))"

    cat > ${CONFIG_DIR}/${JSON} <<EOF
{
    "steps" : 30000,
    "logevery": 30000,
    "overwrite_logs": true,
    "logbase" : "./logs/gamma_noise/",
    "hextohex_d" : ${HEXHEXD}, // Hex to hex distance, determines num hexes
    "svgpath" : "./boundaries/rat_barrels/wb_110405_Dirichlet.svg",
    "boundaryFalloffDist" : ${BFD},
    "G" : 1.0,     // gamma gain
    "dt" : ${DT}, // Timestep. Defaults to 0.00001 if omitted here

    // Initial conditions parameters
    "aNoiseGain" : ${ANG},
    "aInitialOffset" : ${ANO},

    "mNoiseGain" : 0.0,

    // Parameters that will vary
    "D" : ${D},
    "k" : ${k},    // Exponent on a
    // Also: alpha, beta, epsilon; see gamma list below

    // Array of parameters for N thalamocortical populations.
    // Noise magnitude: ${gamma_noise_mag}
    "tc": [
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-2.0+GN[1])),               $((0.08297875929160803+GN[2]))], "name" : "a" }, // a
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-1.841803677231407+GN[3])), $((0.5955182340971339+GN[4]))], "name" : "A1" }, // A1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-1.5766667867404216+GN[5])), $((0.8026650330176572+GN[6]))], "name" : "A2" }, // A2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-1.3229961206880625+GN[7])), $((1.006728138855208+GN[8]))], "name" : "A3" }, // A3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-1.0786832474038208+GN[9])), $((1.2453982728569302+GN[10]))], "name" : "A4" }, // A4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-1.5844170937774447+GN[11])), $((-0.6347093364107037+GN[12]))], "name" : "b" }, // b
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-1.429349946121596+GN[13])), $((-0.11059706135929037+GN[14]))], "name" : "B1" }, // B1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-1.0972823920313275+GN[15])), $((0.07734661081184946+GN[16]))], "name" : "B2" }, // B2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-0.8099920474672921+GN[17])), $((0.3399097533912725+GN[18]))], "name" : "B3" }, // B3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-0.5865031913897942+GN[19])), $((0.6101032224741925+GN[20]))], "name" : "B4" }, // B4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-0.9942346059227621+GN[21])), $((-1.4045569920900212+GN[22]))], "name" : "c" }, // c
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-0.9686071613071959+GN[23])), $((-0.7666815324426732+GN[24]))], "name" : "C1" }, // C1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-0.586423738301838+GN[25])), $((-0.6271724432962702+GN[26]))], "name" : "C2" }, // C2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-0.17997842955291926+GN[27])), $((-0.3945562892438259+GN[28]))], "name" : "C3" }, // C3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.004934757689654623+GN[29])), $((-0.07282464925911292+GN[30]))], "name" : "C4" }, // C4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.1649578956687497+GN[31])), $((0.3412494181486343+GN[32]))], "name" : "C5" }, // C5
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.21421992832302666+GN[33])), $((0.799862666426935+GN[34]))], "name" : "C6" }, // C6
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.26218951193176776+GN[35])), $((1.1715461833621803+GN[36]))], "name" : "C7" }, // C7
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.33726853993680656+GN[37])), $((1.4886078363126574+GN[38]))], "name" : "C8" }, // C8
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.40919131586503565+GN[39])), $((1.8171952179208173+GN[40]))], "name" : "C9" }, // C9
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-0.3072392928763717+GN[41])), $((-1.9381596935842134+GN[42]))], "name" : "d" }, // d
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-0.43567894000290097+GN[43])), $((-1.415767013494814+GN[44]))], "name" : "D1" }, // D1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((-0.0012243177344666845+GN[45])), $((-1.2870289629201288+GN[46]))], "name" : "D2" }, // D2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.595325752177874+GN[47])), $((-1.164354839691761+GN[48]))], "name" : "D3" }, // D3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.848405242531084+GN[49])), $((-0.7748322941280898+GN[50]))], "name" : "D4" }, // D4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.9184912923921059+GN[51])), $((-0.34774238093098786+GN[52]))], "name" : "D5" }, // D5
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.9695900511135901+GN[53])), $((0.01236833575836993+GN[54]))], "name" : "D6" }, // D6
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.9108447397408347+GN[55])), $((0.36784618960465654+GN[56]))], "name" : "D7" }, // D7
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.8658048696529359+GN[57])), $((0.764054051589858+GN[58]))], "name" : "D8" }, // D8
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.9262515102858337+GN[59])), $((1.0895948643062088+GN[60]))], "name" : "D9" }, // D9
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.9919727455227539+GN[61])), $((1.4412635454208589+GN[62]))], "name" : "D10" }, // D10
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((0.5242198246896889+GN[63])), $((-2.0+GN[64]))], "name" : "E1" }, // E1
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((1.3370373323610558+GN[65])), $((-1.9926063552933613+GN[66]))], "name" : "E2" }, // E2
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((1.9015589553746204+GN[67])), $((-1.7052622130395196+GN[68]))], "name" : "E3" }, // E3
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((2.0+GN[69])),                $((-1.2458372556900064+GN[70]))], "name" : "E4" }, // E4
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((1.9730105641076467+GN[71])), $((-0.733403905101111+GN[72]))], "name" : "E5" }, // E5
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((1.7773685477785337+GN[73])), $((-0.32800135109841433+GN[74]))], "name" : "E6" }, // E6
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((1.7752691611496592+GN[75])), $((0.09208957206744639+GN[76]))], "name" : "E7" }, // E7
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((1.7554451998566696+GN[77])), $((0.53224240264211+GN[78]))], "name" : "E8" }, // E8
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((1.7187892777721283+GN[79])), $((0.9430795811620478+GN[80]))], "name" : "E9" }, // E9
        { "alpha" : ${ALPHA}, "beta" : ${BETA}, "epsilon" : ${EPS}, "xinit" : -0.16,   "yinit" : 0.0, "sigmainit" : 0.0, "gaininit" : 1.0, "gamma" : [$((1.810673189604652+GN[81])), $((1.2894098145790438+GN[82]))], "name" : "E10" }
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
    echo "./build/sim/james_comp2c ${CONFIG_DIR}/${JSON}"
    ./build/sim/james_comp2c ${CONFIG_DIR}/${JSON}
    RTN=$?
    if [ $RTN -ne "0" ]; then
        echo "Config: ${CONFIG_DIR}/${JSON} FAILED. Moving on to next."
    fi
done

# Success/completion
exit 0
