/*
 * This program is intended to facilite the study of a reaction
 * diffusion system which is guided by M guidance molecules, whose
 * expression gradients drive N thalamocortical axon types to make
 * connections in an elliptical region.
 *
 * Author: Seb James <seb.james@sheffield.ac.uk>
 *
 * Date: June 2019
 */

/*!
 * This will be passed as the template argument for RD_Plot and RD and
 * should be defined when compiling.
 */
#ifndef FLT
// Check CMakeLists.txt to change to double or float
# error "Please define FLT when compiling (hint: See CMakeLists.txt)"
#endif

#include <iostream>
#include <fstream>
#include <vector>
#include <list>
#include <string>
#include <sstream>
#include <limits>
#include <cmath>
#include <chrono>

//! Include the relevant reaction diffusion class
#if defined DIVNORM
#include "rd_james_divnorm.h"
#elif defined DNCOMP2
#include "rd_james_dncomp2.h"
#elif defined DNCOMP
#include "rd_james_dncomp.h"
#elif defined COMP2
#include "rd_james_comp2.h"
#else
#include "rd_james.h" // 2D Karbowski, no additional competition/features
#endif

#include "morph/ShapeAnalysis.h"
using morph::ShapeAnalysis;
#include "morph/Hex.h"
using morph::Hex;
#include "morph/HexGrid.h"
using morph::HexGrid;
#include "morph/HdfData.h"
using morph::HdfData;

#ifdef COMPILE_PLOTTING
# include <GLFW/glfw3.h>
# include "morph/Scale.h"
using morph::Scale;
# include "morph/ColourMap.h"
using morph::ColourMapType;
# include "morph/Visual.h"
using morph::Visual;
# include "morph/VisualDataModel.h"
using morph::VisualDataModel;
# include "morph/HexGridVisual.h"
using morph::HexGridVisual;

// Alias VisualDataModel<FLT>* as VdmPtr, to neaten code
typedef morph::VisualDataModel<FLT>* VdmPtr;

# include <morph/MathAlgo.h>
using morph::MathAlgo;

using namespace std;
using namespace std::chrono;
using std::chrono::steady_clock;

//! Helper function to save PNG images
void savePngs (const std::string& logpath, const std::string& name,
               unsigned int frameN, Visual& v) {
    std::stringstream ff1;
    ff1 << logpath << "/" << name<< "_";
    ff1 << std::setw(5) << std::setfill('0') << frameN;
    ff1 << ".png";
    v.saveImage (ff1.str());
}

//! Take the first element of the array and create a vector<vector<FLT>> to plot
vector<vector<FLT> > separateVectorField (vector<array<vector<FLT>, 2> >& f,
                                          unsigned int arrayIdx) {
    vector<vector<FLT> > vf;
    for (array<vector<FLT>, 2> fia : f) {
        vector<FLT> tmpv = fia[arrayIdx];
        vf.push_back (tmpv);
    }
    return vf;
}
#endif

//! Included for directory manipulation code
#include "morph/tools.h"

//! A jsoncpp-wrapping class for configuration.
#include "morph/Config.h"

using namespace std;

/*!
 * main(): Run a simulation, using parameters obtained from a JSON
 * file.
 *
 * Open and read a simple JSON file which contains the parameters for
 * the simulation, such as number of guidance molecules (M), guidance
 * parameters (probably get M from these) and so on.
 *
 * Sample JSON:
 * {
 *   // Overall parameters
 *   "steps":5000,                // Number of steps to simulate for
 *   "logevery":20,               // Log data every logevery steps.
 *   "svgpath":"./ellipse.svg",   // The boundary shape to use
 *   "hextohex_d":0.01,           // Hex to hex distance, determines num hexes
 *   "boundaryFalloffDist":0.01,
 *   "D":0.1,                     // Global diffusion constant
 *   // Array of parameters for N thalamocortical populations:
 *   "tc": [
 *     // The first TC population
 *     {
 *       "alpha":3,
 *       "beta":3
 *     },
 *     // The next TC population
 *     {
 *       "alpha":3,
 *       "beta":3
 *     } // and so on.
 *   ],
 *   // Array of parameters for the guidance molecules
 *   "guidance": [
 *     {
 *       "shape":"Sigmoid1D", // and so on
 *       "gain":0.5,
 *       "phi":0.8,
 *       "width":0.1,
 *       "offset":0.0,
 *     }
 *   ]
 * }
 *
 * A file containing JSON similar to the above should be saved and its
 * path provided as the only argument to any of the binaries compiled
 * from this code.
 */
int main (int argc, char **argv)
{
    // Randomly set the RNG seed
    srand (morph::Tools::randomSeed());

    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " /path/to/params.json [/path/to/logdir]" << endl;
        return 1;
    }
    string paramsfile (argv[1]);

    // Set up a morph::Config object for reading configuration
    morph::Config conf(paramsfile);
    if (!conf.ready) {
        cerr << "Error setting up JSON config: " << conf.emsg << endl;
        return 1;
    }

    /*
     * Get simulation-wide parameters from JSON
     */
    const unsigned int steps = conf.getUInt ("steps", 1000UL);
    if (steps == 0) {
        cerr << "Not much point simulating 0 steps! Exiting." << endl;
        return 1;
    }
    const unsigned int logevery = conf.getUInt ("logevery", 100UL);
    if (logevery == 0) {
        cerr << "Can't log every 0 steps. Exiting." << endl;
        return 1;
    }
    const float hextohex_d = conf.getFloat ("hextohex_d", 0.01f);
    const float hexspan = conf.getFloat ("hexspan", 4.0f);
    const float boundaryFalloffDist = conf.getFloat ("boundaryFalloffDist", 0.01f);
    const string svgpath = conf.getString ("svgpath", "./ellipse.svg");
    bool overwrite_logs = conf.getBool ("overwrite_logs", false);
    // Do we carry out dirichlet analysis? Default to true, because it's computationally cheap.
    bool do_dirichlet_analysis = conf.getBool ("do_dirichlet_analysis", true);
    string logpath = conf.getString ("logpath", "fromfilename");
    string logbase = "";
    if (logpath == "fromfilename") {
        // Using json filename as logpath
        string justfile = paramsfile;
        // Remove trailing .json and leading directories
        vector<string> pth = morph::Tools::stringToVector (justfile, "/");
        justfile = pth.back();
        morph::Tools::searchReplace (".json", "", justfile);
        // Use logbase as the subdirectory into which this should go
        logbase = conf.getString ("logbase", "logs/");
        if (logbase.back() != '/') {
            logbase += '/';
        }
        logpath = logbase + justfile;
    }
    if (argc == 3) {
        string argpath(argv[2]);
        cerr << "Overriding the config-given logpath " << logpath << " with " << argpath << endl;
        logpath = argpath;
        if (overwrite_logs == true) {
            cerr << "WARNING: You set a command line log path.\n"
                 << "       : Note that the parameters config permits the program to OVERWRITE LOG\n"
                 << "       : FILES on each run (\"overwrite_logs\" is set to true)." << endl;
        }
    }

    // Used to initialise a
    const double aNoiseGain = conf.getDouble ("aNoiseGain", 0.1);
    const double aInitialOffset = conf.getDouble ("aInitialOffset", 0.1);

    const FLT dt = static_cast<FLT>(conf.getDouble ("dt", 0.00001));

    const FLT contour_threshold = conf.getDouble ("contour_threshold", 0.6);

    const double D = conf.getDouble ("D", 0.1);
    const FLT k = conf.getDouble ("k", 3.0);

#if defined DNCOMP || defined DNCOMP2
    const FLT l = conf.getDouble ("l", 1.0);
    const FLT m = conf.getDouble ("m", 1e-8);
    const double E = conf.getDouble ("E", 0.0);
    DBG2 ("E is set to " << E);
#endif

#if defined COMP2
    const double F = conf.getDouble ("F", 0.0);
#endif

    bool do_fgf_duplication = conf.getBool ("do_fgf_duplication", false);

    DBG ("steps to simulate: " << steps);

    // Thalamocortical populations array of parameters:
    const Json::Value tcs = conf.getArray ("tc");
    unsigned int N_TC = static_cast<unsigned int>(tcs.size());
    if (N_TC == 0) {
        cerr << "Zero thalamocortical populations makes no sense for this simulation. Exiting."
             << endl;
        return 1;
    }

    // Guidance molecule array of parameters:
    const Json::Value guid = conf.getArray("guidance");
    unsigned int M_GUID = static_cast<unsigned int>(guid.size());

#ifdef COMPILE_PLOTTING

    // Parameters from the config that apply only to plotting:
    const unsigned int plotevery = conf.getUInt ("plotevery", 10UL);

    // If true, then write out the logs in consecutive order numbers,
    // rather than numbers that relate to the simulation timestep.
    const bool vidframes = conf.getBool ("vidframes", false);
    unsigned int framecount = 0;

    // Which windows to plot?
    const bool plot_guide = conf.getBool ("plot_guide", true);
    const bool plot_contours = conf.getBool ("plot_contours", true);
    const bool plot_a_contours = conf.getBool ("plot_a_contours", true);
    const bool plot_a = conf.getBool ("plot_a", true);
    //const bool scale_a = conf.getBool ("scale_a", true);
    const bool plot_c = conf.getBool ("plot_c", true);
    //const bool scale_c = conf.getBool ("scale_c", true);
    const bool plot_n = conf.getBool ("plot_n", true);
    const bool plot_dr = conf.getBool ("plot_dr", true);
    //const bool scale_n = conf.getBool ("scale_n", true);
    const bool plot_guidegrad = conf.getBool ("plot_guidegrad", false);

    const unsigned int win_width = conf.getUInt ("win_width", 1025UL);
    unsigned int win_height = static_cast<unsigned int>(0.8824f * (float)win_width);

    // Set up the morph::Visual object
    Visual plt (win_width, win_height, "James-Wilson barrel simulation");
    plt.zNear = 0.001;
    plt.zFar = 50;
    plt.fov = 45;
    plt.setZDefault (-10.0f);
    // Set a dark blue background (black is the default). This value has the order
    // 'RGBA', though the A(alpha) makes no difference.
    plt.bgcolour = {0.0f, 0.0f, 0.2f, 1.0f};
    // You can lock movement of the scene
    plt.sceneLocked = conf.getBool ("sceneLocked", false);
    // You can set the default scene x/y/z offsets
    plt.setZDefault (conf.getFloat ("z_default", -10.0f));
    plt.setSceneTransXY (conf.getFloat ("x_default", 0.0f),
                         conf.getFloat ("y_default", 0.0f));
    // Make this larger to "scroll in and out of the image" faster
    plt.scenetrans_stepsize = 0.5;
    cout << "Success configuring the morph::Visual object!" << endl;
#endif

    /*
     * Instantiate and set up the model object
     */
#if defined DIVNORM
    RD_James_divnorm<FLT> RD;
#elif defined DNCOMP2
    RD_James_dncomp2<FLT> RD;
#elif defined DNCOMP
    RD_James_dncomp<FLT> RD;
#elif defined COMP2
    RD_James_comp2<FLT> RD;
#else
    RD_James<FLT> RD;
#endif

    RD.svgpath = svgpath;
    RD.logpath = logpath;

    // NB: Set .N, .M BEFORE RD.allocate().
    RD.N = N_TC; // Number of TC populations
    RD.M = M_GUID; // Number of guidance molecules that are sculpted

    // Set up timestep
    RD.set_dt (dt);

    // Control the size of the hexes, and therefore the number of hexes in the grid
    RD.hextohex_d = hextohex_d;
    RD.hexspan = hexspan;

    // Boundary fall-off distance
    RD.boundaryFalloffDist = boundaryFalloffDist;

    RD.aNoiseGain = aNoiseGain;
    RD.aInitialOffset = aInitialOffset;

    // After setting N and M, we can set up all the vectors in RD:
    RD.allocate();

    // After allocate(), we can set up parameters:
    RD.set_D (D);

#if defined DNCOMP || defined DNCOMP2
    DBG2 ("Setting RD.l to " << l);
    RD.l = l;
    RD.m = m;
# ifndef E_A_DIVN
    if (E > 0.0) {
        cerr << "ERROR: You have E>0.0, but you are using a binary without the code to compute E div n" << endl;
        exit (1);
    }
# endif
    RD.E = E;
#endif

#if defined COMP2
    RD.F = F;
#endif

    RD.contour_threshold = contour_threshold;
    RD.k = k;
    RD.doFgfDuplication = do_fgf_duplication;

    // Index through thalamocortical fields, setting params:
    for (unsigned int i = 0; i < tcs.size(); ++i) {
        Json::Value v = tcs[i];
        RD.alpha[i] = v.get("alpha", 0.0).asDouble();
        RD.beta[i] = v.get("beta", 0.0).asDouble();

        // Sets up mask for initial branching density
        GaussParams<FLT> gp;
        gp.gain = v.get("gaininit", 1.0).asDouble();
        gp.sigma = v.get("sigmainit", 0.0).asDouble();
        gp.x = v.get("xinit", 0.0).asDouble();
        DBG2 ("Set xinit["<<i<<"] to " << gp.x);
        gp.y = v.get("yinit", 0.0).asDouble();
        RD.initmasks.push_back (gp);
#if defined DNCOMP || defined DNCOMP2
        RD.epsilon[i] = v.get("epsilon", 0.0).asDouble();
        DBG2 ("Set RD.epsilon["<<i<<"] to " << RD.epsilon[i]);
#endif
#if defined DNCOMP2
        RD.xi[i] = v.get("xi", 0.0).asDouble();
        DBG2 ("Set RD.xi["<<i<<"] to " << RD.xi[i]);
#endif
    }

    // Index through guidance molecule parameters:
    for (unsigned int j = 0; j < guid.size(); ++j) {
        Json::Value v = guid[j];
        // What guidance molecule method will we use?
        string rmeth = v.get ("shape", "Sigmoid1D").asString();
        DBG2 ("guidance molecule shape: " << rmeth);
        if (rmeth == "Sigmoid1D") {
            RD.rhoMethod[j] = FieldShape::Sigmoid1D;
        } else if (rmeth == "Linear1D") {
            RD.rhoMethod[j] = FieldShape::Linear1D;
        } else if (rmeth == "Exponential1D") {
            RD.rhoMethod[j] = FieldShape::Exponential1D;
        } else if (rmeth == "Gauss1D") {
            RD.rhoMethod[j] = FieldShape::Gauss1D;
        } else if (rmeth == "Gauss2D") {
            RD.rhoMethod[j] = FieldShape::Gauss2D;
        } else if (rmeth == "CircLinear2D") {
            RD.rhoMethod[j] = FieldShape::CircLinear2D;
        }
        // Set up guidance molecule method parameters
        RD.guidance_gain.push_back (v.get("gain", 1.0).asDouble());
        DBG2 ("guidance modelecule gain: " << RD.guidance_gain.back());
        RD.guidance_phi.push_back (v.get("phi", 1.0).asDouble());
        RD.guidance_width.push_back (v.get("width", 1.0).asDouble());
        RD.guidance_offset.push_back (v.get("offset", 1.0).asDouble());
        RD.guidance_time_onset.push_back (v.get("time_onset", 0).asUInt());
    }

    // Which of the gammas is the "group" defining gamma?
    const unsigned int groupgamma = conf.getUInt ("groupgamma", 0UL);

    // Set up the interaction parameters between the different TC
    // populations and the guidance molecules (aka gamma).
    int paramRtn = 0;
    for (unsigned int i = 0; i < tcs.size(); ++i) {
        Json::Value tcv = tcs[i];
        Json::Value gamma = tcv["gamma"];
        Json::Value tcname = tcv["name"];
        for (unsigned int j = 0; j < guid.size(); ++j) {
            // Set up gamma values using a setter which checks we
            // don't set a value that's off the end of the gamma
            // container.
            DBG2 ("Set gamma for guidance " << j << " over TC " << i << " = " << gamma[j]);
            paramRtn += RD.setGamma (j, i, gamma[j].asDouble(), groupgamma);
        }
        // Make a map of name to float id value
        RD.tcnames[(FLT)i/(FLT)tcs.size()] = tcname.asString();
    }

    if (paramRtn && M_GUID>0) {
        cerr << "Something went wrong setting gamma values" << endl;
        return paramRtn;
    }

    // Now have the guidance molecule densities and their gradients computed, call init()
    RD.init();

    /*
     * Now create a log directory if necessary, and exit on any
     * failures.
     */
    if (morph::Tools::dirExists (logpath) == false) {
        morph::Tools::createDir (logpath);
        if (morph::Tools::dirExists (logpath) == false) {
            cerr << "Failed to create the logpath directory "
                 << logpath << " which does not exist."<< endl;
            return 1;
        }
    } else {
        // Directory DOES exist. See if it contains a previous run and
        // exit without overwriting to avoid confusion.
        if (overwrite_logs == false
            && (morph::Tools::fileExists (logpath + "/params.json") == true
                || morph::Tools::fileExists (logpath + "/guidance.h5") == true
                || morph::Tools::fileExists (logpath + "/positions.h5") == true)) {
            cerr << "Seems like a previous simulation was logged in " << logpath << ".\n"
                 << "Please clean it out manually, choose another directory or set\n"
                 << "overwrite_logs to true in your parameters config JSON file." << endl;
            return 1;
        }
    }

    // As RD.allocate() as been called (and log directory has been
    // created/verified ready), positions can be saved to file.
    RD.savePositions();
    RD.saveHG();
    // Save the guidance molecules now.
    RD.saveGuidance();

#ifdef COMPILE_PLOTTING

    // Data scaling parameters
    float _m = 0.2;
    float _c = 0.0;
    // Z position scaling - how hilly/bumpy the visual will be.
    Scale<FLT> zscale; zscale.setParams (_m/10.0f, _c/10.0f);
    // The second is the colour scaling.
    Scale<FLT> cscale; cscale.setParams (_m, _c);

    // HERE, add HexGridVisuals...
    unsigned int c_ctr_grid = 0; // one only
    unsigned int a_ctr_grid = 0;
    unsigned int dr_grid = 0;
    vector<unsigned int> guide_grids;
    vector<unsigned int> guidegrad_grids;

    // Spatial offset
    array<float, 3> spatOff;
    float xzero = 0.0f;

    // The a variable
    vector<unsigned int> agrids;
    unsigned int side = static_cast<unsigned int>(floor (sqrt (RD.N)));
    if (plot_a) {
        spatOff = {xzero, 0.0, 0.0 };
        for (unsigned int i = 0; i<RD.N; ++i) {
            spatOff[0] = xzero + RD.hg->width() * (i/side);
            spatOff[1] = RD.hg->width() * (i%side);
            unsigned int idx = plt.addVisualModel (new HexGridVisual<FLT> (plt.shaderprog,
                                                                           RD.hg,
                                                                           spatOff,
                                                                           &RD.a[i],
                                                                           zscale,
                                                                           cscale,
                                                                           ColourMapType::Plasma));

            agrids.push_back (idx);
        }
        xzero = spatOff[0] + RD.hg->width();
    }

    // The c variable
    vector<unsigned int> cgrids;
    if (plot_c) {
        spatOff = {xzero, 0.0, 0.0 };
        for (unsigned int i = 0; i<RD.N; ++i) {
            spatOff[0] = xzero + RD.hg->width() * (i/side);
            spatOff[1] = RD.hg->width() * (i%side);
            unsigned int idx = plt.addVisualModel (new HexGridVisual<FLT> (plt.shaderprog,
                                                                           RD.hg,
                                                                           spatOff,
                                                                           &RD.c[i],
                                                                           zscale,
                                                                           cscale,
                                                                           ColourMapType::Plasma));
            cgrids.push_back (idx);
        }
        xzero = spatOff[0] + RD.hg->width();
    }

    // n
    unsigned int ngrid = 0;
    if (plot_n) {
        spatOff = { xzero, 0.0, 0.0 };
        ngrid = plt.addVisualModel (new HexGridVisual<FLT> (plt.shaderprog,
                                                            RD.hg,
                                                            spatOff,
                                                            &RD.n,
                                                            zscale,
                                                            cscale,
                                                            ColourMapType::Plasma));
        xzero += RD.hg->width();
    }

    // Contours
    // Z position scaling - how hilly/bumpy the visual will be. This is totally unhilly!
    Scale<FLT> null_zscale; null_zscale.setParams (0.0f, 0.0f);
    // The second is the colour scaling.
    Scale<FLT> ctr_cscale; ctr_cscale.setParams (1.0f, 0.0f);
    vector<FLT> zeromap (RD.nhex, static_cast<FLT>(0.0));
    if (plot_contours) {
        spatOff = { xzero, 0.0, 0.0 };
        // special scaling for contours. flat in Z, but still colourful
        c_ctr_grid = plt.addVisualModel (new HexGridVisual<FLT> (plt.shaderprog,
                                                                 RD.hg,
                                                                 spatOff,
                                                                 &zeromap,
                                                                 null_zscale,
                                                                 ctr_cscale,
                                                                 ColourMapType::RainbowZeroBlack));
        xzero += RD.hg->width();
    }

    if (plot_a_contours) {
        spatOff = { xzero, 0.0, 0.0 };
        a_ctr_grid = plt.addVisualModel (new HexGridVisual<FLT> (plt.shaderprog,
                                                                 RD.hg,
                                                                 spatOff,
                                                                 &zeromap,
                                                                 null_zscale,
                                                                 ctr_cscale,
                                                                 ColourMapType::RainbowZeroBlack));
        xzero += RD.hg->width();
    }

    if (plot_dr && do_dirichlet_analysis == true) {
        spatOff = { xzero, 0.0, 0.0 };
        dr_grid = plt.addVisualModel (new HexGridVisual<FLT> (plt.shaderprog,
                                                              RD.hg,
                                                              spatOff,
                                                              &zeromap,
                                                              null_zscale,
                                                              ctr_cscale,
                                                              ColourMapType::Rainbow));
        xzero += RD.hg->width();
    }

    // guidance expression
    if (plot_guide) {
        spatOff = { xzero, 0.0, 0.0 };
        // The second is the colour scaling.
        Scale<FLT> gd_cscale;
        //gd_cscale.setParams (_m, _c);
        gd_cscale.do_autoscale = true;
        // Plot gradients of the guidance effect g.
        for (unsigned int j = 0; j<RD.M; ++j) {
            plt.addVisualModel (new HexGridVisual<FLT> (plt.shaderprog,
                                                        RD.hg,
                                                        spatOff,
                                                        &RD.rho[j],
                                                        null_zscale,
                                                        gd_cscale,
                                                        ColourMapType::Monochrome,
                                                        (FLT)(j+1)/(FLT)RD.M));
            spatOff[1] += RD.hg->depth();
        }
        xzero += RD.hg->width();
    }


    // Now plot fields and redraw display
    if (plot_guidegrad) {
        spatOff = { xzero, 0.0, 0.0 };
        for (unsigned int j = 0; j<RD.M; ++j) {

            // gradient of guidance expression
            vector<vector<FLT> > gx = separateVectorField (RD.g[j], 0);
            vector<vector<FLT> > gy = separateVectorField (RD.g[j], 1);
            FLT ming = 1e7;
            FLT maxg = -1e7;
            if (plot_guidegrad) {
                // Determine scale of gx and gy so that a common scale can be
                // applied to both gradient_x and gradient_y.
                for (unsigned int hi=0; hi<RD.nhex; ++hi) {
                    Hex* h = RD.hg->vhexen[hi];
                    if (h->onBoundary() == false) {
                        for (unsigned int i = 0; i<RD.N; ++i) {
                            if (gx[i][h->vi]>maxg) { maxg = gx[i][h->vi]; }
                            if (gx[i][h->vi]<ming) { ming = gx[i][h->vi]; }
                            if (gy[i][h->vi]>maxg) { maxg = gy[i][h->vi]; }
                            if (gy[i][h->vi]<ming) { ming = gy[i][h->vi]; }
                        }
                    }
                }
                DBG2 ("min g = " << ming << " and max g = " << maxg);
            }

            // Convert to a scaling object
            float gg_m, gg_c;
            gg_m = 1.0f/(float)(maxg-ming);
            gg_c = -(gg_m * ming);
            // The second is the colour scaling.
            Scale<FLT> ggd_cscale; ggd_cscale.setParams (gg_m, gg_c);

            // Create the grids
            plt.addVisualModel (new HexGridVisual<FLT> (plt.shaderprog,
                                                        RD.hg,
                                                        spatOff,
                                                        &gx[j],
                                                        null_zscale,
                                                        ggd_cscale,
                                                        ColourMapType::Viridis));
            spatOff[0] += RD.hg->width();
            plt.addVisualModel (new HexGridVisual<FLT> (plt.shaderprog,
                                                        RD.hg,
                                                        spatOff,
                                                        &gy[j],
                                                        null_zscale,
                                                        ggd_cscale,
                                                        ColourMapType::Viridis));
            spatOff[0] -= RD.hg->width();
            spatOff[1] += RD.hg->depth();
        }
        xzero += RD.hg->width() + 2.0f;
    }

#if 0
    FLT mindivg = 1e7;
    FLT maxdivg = -1e7;
    if (plot_divg) {
        for (unsigned int hi=0; hi<RD.nhex; ++hi) {
            Hex* h = RD.hg->vhexen[hi];
            if (h->onBoundary() == false) {
                for (unsigned int i = 0; i<RD.N; ++i) {
                    // FIXME only dealing with divg_over3d[0] here!
                    if (RD.divg_over3d[0][i][h->vi]>maxdivg) { maxdivg = RD.divg_over3d[0][i][h->vi]; }
                    if (RD.divg_over3d[0][i][h->vi]<mindivg) { mindivg = RD.divg_over3d[0][i][h->vi]; }
                }
            }
        }
        DBG2 ("min div(g) = " << mindivg << " and max div(g) = " << maxdivg);
    }
    if (plot_divg) {
        // FIXME
        // addVisualModel
    }
    if (plot_divJ) {
        // addVisualModel
    }
#endif

    // Saving of t=0 images in log folder
    if ((RD.M > 0 && plot_guide) || plot_a) {
        savePngs (logpath, "sim", 0, plt);
    }

    // if using plotting, then set up the render clock
    steady_clock::time_point lastrender = steady_clock::now();

    // A pointer to access the data layer of HexGridVisual objects.
    VisualDataModel<FLT>* mdlptr = (VdmPtr)0;

#endif // COMPILE_PLOTTING

    // Start the loop
    bool finished = false;
    while (finished == false) {
        // Step the model
        RD.step();

#ifdef COMPILE_PLOTTING

        if ((RD.stepCount % plotevery) == 0) {
            DBG2("Plot at step " << RD.stepCount);
            // Do a plot of the ctrs as found.
            vector<FLT> ctrmap = ShapeAnalysis<FLT>::get_contour_map (RD.hg, RD.c, RD.contour_threshold);

            if (do_dirichlet_analysis == true) {
                RD.dirichlet();
                DBG2 ("dirich_value = " << RD.honda);
            }

            if (plot_contours) {
                mdlptr = (VdmPtr)plt.getVisualModel (c_ctr_grid);
                mdlptr->updateData (&ctrmap);
            }

            if (plot_a_contours) {
                vector<FLT> actrmap = ShapeAnalysis<FLT>::get_contour_map (RD.hg, RD.a, RD.contour_threshold);
                mdlptr = (VdmPtr)plt.getVisualModel (a_ctr_grid);
                mdlptr->updateData (&actrmap);
            }

            if (plot_a) {
                for (unsigned int i = 0; i<RD.N; ++i) {
                    mdlptr = (VdmPtr)plt.getVisualModel (agrids[i]);
                    mdlptr->updateData (&RD.a[i]);
                }
            }
            if (plot_c) {
                for (unsigned int i = 0; i<RD.N; ++i) {
                    mdlptr = (VdmPtr)plt.getVisualModel (cgrids[i]);
                    mdlptr->updateData (&RD.c[i]);

                }
            }
            if (plot_n) {
                mdlptr = (VdmPtr)plt.getVisualModel (ngrid);
                mdlptr->updateData (&RD.n);
            }
            if (plot_dr && do_dirichlet_analysis) {
                mdlptr = (VdmPtr)plt.getVisualModel (dr_grid);
                mdlptr->updateData (&RD.regions);
            }
            // Then add:
            //plt.plot_dirichlet_boundaries (displays[n_id], RD.hg, vv);

            // With the new all-in-one-window OpenGL format, there's only one savePngs
            // call at a time.
            if (vidframes) {
                savePngs (logpath, "sim", framecount, plt);
                ++framecount;
            } else {
                savePngs (logpath, "sim", RD.stepCount, plt);
            }
        }

        // rendering the graphics.
        steady_clock::duration sincerender = steady_clock::now() - lastrender;
        if (duration_cast<milliseconds>(sincerender).count() > 17) { // 17 is about 60 Hz
            glfwPollEvents();
            plt.render();
            lastrender = steady_clock::now();
        }
#endif // COMPILE_PLOTTING

        // Save data every 'logevery' steps
        if (RD.stepCount == 1 || (RD.stepCount % logevery) == 0) {
            DBG ("Logging data at step " << RD.stepCount);
            RD.save();

            // Fixme. Save the hex contours in their own file. Each Hex has a save() method.
            vector<list<Hex> > sv_ctrs = ShapeAnalysis<FLT>::get_contours (RD.hg, RD.c, RD.contour_threshold);

            if (do_dirichlet_analysis == true) {
                // We HAVE to RD.dirichlet again, in case the frequency at which we're plotting is
                // different from the frequency at which we're loggin.
                RD.dirichlet();
                RD.saveDirichletDomains();
            }
        }

        if (RD.stepCount > steps) {
            finished = true;
        }
    }

    // Save out the sums.
    RD.savesums();

    // Before saving the json, we'll place any additional useful info
    // in there, such as the FLT. If float_width is 4, then
    // results were computed with single precision, if 8, then double
    // precision was used. Also save various parameters from the RD system.
    conf.set ("float_width", (unsigned int)sizeof(FLT));
    string tnow = morph::Tools::timeNow();
    conf.set ("sim_ran_at_time", tnow.substr(0,tnow.size()-1));
    conf.set ("hextohex_d", RD.hextohex_d);
    conf.set ("D", RD.get_D());
    conf.set ("k", RD.k);
    conf.set ("dt", RD.get_dt());
    // Call our function to place git information into root.
    conf.insertGitInfo ("sim/");
    // Store the binary name and command argument into root, too.
    if (argc > 0) { conf.set("argv0", argv[0]); }
    if (argc > 1) { conf.set("argv1", argv[1]); }

    // We'll save a copy of the parameters for the simulation in the log directory as params.json
    const string paramsCopy = logpath + "/params.json";
    conf.write (paramsCopy);
    if (conf.ready == false) {
        cerr << "Warning: Something went wrong writing a copy of the params.json: " << conf.emsg << endl;
    }

#if 0 // Extracting contours is unnecessary and, at present, buggy (see morphologica Issue#20)
    // Extract contours
    vector<list<Hex> > ctrs = ShapeAnalysis<FLT>::get_contours (RD.hg, RD.c, RD.contour_threshold);
    {
        // Write each contour to a contours.h5 file
        stringstream ctrname;
        ctrname << logpath << "/contours.h5";
        HdfData ctrdata(ctrname.str());
        unsigned int nctrs = ctrs.size();
        ctrdata.add_val ("/num_contours", nctrs);
        for (unsigned int ci = 0; ci < nctrs; ++ci) {
            vector<FLT> vx, vy;
            auto hi = ctrs[ci].begin();
            while (hi != ctrs[ci].end()) {
                vx.push_back (hi->x);
                vy.push_back (hi->y);
                ++hi;
            }
            stringstream ciss;
            ciss << ci;
            string pth = "/x" + ciss.str();
            ctrdata.add_contained_vals (pth.c_str(), vx);
            pth[1] = 'y';
            ctrdata.add_contained_vals (pth.c_str(), vy);

            // Generate hex grids from contours to obtain the size of the region enclosed by the contour
            HexGrid* hg1 = new HexGrid (RD.hextohex_d, RD.hexspan, 0, morph::HexDomainShape::Boundary);
            hg1->setBoundary (ctrs[ci]);
            pth[1] = 'n';
            ctrdata.add_val(pth.c_str(), hg1->num());
            delete hg1;
        }

        // Also extract the boundary of the main, enclosing hexgrid and write that.
        list<Hex> outerBoundary = RD.hg->getBoundary();
        vector<FLT> vx, vy;
        auto bi = outerBoundary.begin();
        while (bi != outerBoundary.end()) {
            vx.push_back (bi->x);
            vy.push_back (bi->y);
            ++bi;
        }
        ctrdata.add_contained_vals ("/xb", vx);
        ctrdata.add_contained_vals ("/yb", vy);
    }
#endif

#ifdef COMPILE_PLOTTING
    cout << "Ctrl-c or press x in graphics window to exit.\n";
    plt.keepOpen();
#endif

    return 0;
};
