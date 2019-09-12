/*
 * A program to view the guidance gradients, without running the simulation
 *
 * Author: Seb James <seb.james@sheffield.ac.uk>
 *
 * Date: Sept 2019
 */

/*!
 * This will be passed as the template argument for RD_plot and RD and
 * should be defined when compiling.
 */
#ifndef FLT
// Check CMakeLists.txt to change to double or float
# error "Please define FLT when compiling (hint: See CMakeLists.txt)"
#endif

/*!
 * General STL includes
 */
#include <iostream>
#include <fstream>
#include <vector>
#include <list>
#include <string>
#include <limits>

/*!
 * Include the reaction diffusion class (only rd_james.h is required)
 */
#include "rd_james.h" // 2D Karbowski, no additional competition/features

/*!
 * Include display and plotting code
 */
# include "morph/display.h"
# include "morph/RD_Plot.h"
using morph::RD_plot;

/*!
 * Included for directory manipulation code
 */
#include "morph/tools.h"

/*!
 * I'm using JSON to read in simulation parameters
 */
#include <json/json.h>

using namespace std;

int main (int argc, char **argv)
{
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " /path/to/params.json [/path/to/logdir]" << endl;
        return 1;
    }
    string paramsfile (argv[1]);

    /*
     * Set up JSON code for reading the parameters
     */

    // Test for existence of the JSON file.
    ifstream jsonfile_test;
    int srtn = system ("pwd");
    if (srtn) {
        cerr << "system call returned " << srtn << endl;
    }
    jsonfile_test.open (paramsfile, ios::in);
    if (jsonfile_test.is_open()) {
        // Good, file exists.
        jsonfile_test.close();
    } else {
        cerr << "json config file " << paramsfile << " not found." << endl;
        return 1;
    }

    // Parse the JSON
    ifstream jsonfile (paramsfile, ifstream::binary);
    Json::Value root;
    string errs;
    Json::CharReaderBuilder rbuilder;
    rbuilder["collectComments"] = false;
    bool parsingSuccessful = Json::parseFromStream (rbuilder, jsonfile, &root, &errs);
    if (!parsingSuccessful) {
        // report to the user the failure and their locations in the document.
        cerr << "Failed to parse JSON: " << errs;
        return 1;
    }

    /*
     * Get simulation-wide parameters from JSON
     */
    const float hextohex_d = root.get ("hextohex_d", 0.01).asFloat();
    const float boundaryFalloffDist = root.get ("boundaryFalloffDist", 0.01).asFloat();
    const string svgpath = root.get ("svgpath", "./ellipse.svg").asString();

    // Used to initialise a
    const double aNoiseGain = root.get ("aNoiseGain", 0.1).asDouble();
    const double aInitialOffset = root.get ("aInitialOffset", 0.1).asDouble();

    const FLT dt = static_cast<FLT>(root.get ("dt", 0.00001).asDouble());

    const FLT contour_threshold = root.get ("contour_threshold", 0.6).asDouble();

    const double D = root.get ("D", 0.1).asDouble();
    const FLT k = root.get ("k", 3).asDouble();

    bool do_fgf_duplication = root.get ("do_fgf_duplication", false).asBool();

    // Thalamocortical populations array of parameters:
    const Json::Value tcs = root["tc"];
    unsigned int N_TC = static_cast<unsigned int>(tcs.size());
    if (N_TC == 0) {
        cerr << "Zero thalamocortical populations makes no sense for this simulation. Exiting."
             << endl;
        return 1;
    }

    // Guidance molecule array of parameters:
    const Json::Value guid = root["guidance"];
    unsigned int M_GUID = static_cast<unsigned int>(guid.size());

    const bool scale_a = root.get ("scale_a", true).asBool();

    // Window IDs
    unsigned int guide_id = 0xffff;
#if 0
    unsigned int a_id = 0xffff;
    unsigned int guidegrad_x_id = 0xffff;
    unsigned int guidegrad_y_id = 0xffff;
#endif
    // Create some displays
    vector<morph::Gdisplay> displays;
    vector<double> fix(3, 0.0);
    vector<double> eye(3, 0.0);
    eye[2] = 0.12; // This also acts as a zoom. more +ve to zoom out, more -ve to zoom in.
    vector<double> rot(3, 0.0);

    // A plot object.
    RD_plot<FLT> plt(fix, eye, rot);

    double rhoInit = root.get ("rhoInit", 1.0).asDouble(); // This is effectively a zoom control. Increase to zoom out.
    double thetaInit = 0.0;
    double phiInit = 0.0;

    string worldName("j");
    unsigned int windowId = 0;
    string winTitle = "";

    const unsigned int win_width = root.get ("win_width", 800).asUInt();
    unsigned int win_height = static_cast<unsigned int>(0.8824f * (float)win_width);

    // SW - Contours. Always plot
    winTitle = worldName + ": Guidance molecules"; // 0
    displays.push_back (morph::Gdisplay (win_width * (M_GUID>0?M_GUID:1), win_height, 100, 300,
                                         winTitle.c_str(), rhoInit, thetaInit, phiInit));
    displays.back().resetDisplay (fix, eye, rot);
    displays.back().redrawDisplay();
    guide_id = windowId++;

#if 0
    winTitle = worldName + ": a[0] to a[N]"; // 1
    displays.push_back (morph::Gdisplay (win_width*N_TC, win_height, 100, 900, winTitle.c_str(),
                                         rhoInit, thetaInit, phiInit, displays[0].win));
    displays.back().resetDisplay (fix, eye, rot);
    displays.back().redrawDisplay();
    a_id = windowId++;

    winTitle = worldName + ": Guidance gradient (x)";//5
    displays.push_back (morph::Gdisplay (win_width*N_TC, win_height, 100, 1800, winTitle.c_str(),
                                         rhoInit, thetaInit, phiInit, displays[0].win));
    displays.back().resetDisplay (fix, eye, rot);
    displays.back().redrawDisplay();
    guidegrad_x_id = windowId++;

    winTitle = worldName + ": Guidance gradient (y)";//6
    displays.push_back (morph::Gdisplay (win_width*N_TC, win_height, 100, 1800, winTitle.c_str(),
                                         rhoInit, thetaInit, phiInit, displays[0].win));
    displays.back().resetDisplay (fix, eye, rot);
    displays.back().redrawDisplay();
    guidegrad_y_id = windowId++;
#endif
    /*
     * Instantiate and set up the model object
     */
    RD_James<FLT> RD;

    RD.svgpath = svgpath;
    RD.logpath = "";

    // NB: Set .N, .M BEFORE RD.allocate().
    RD.N = N_TC; // Number of TC populations
    RD.M = M_GUID; // Number of guidance molecules that are sculpted

    // Set up timestep
    RD.set_dt (dt);

    // Control the size of the hexes, and therefore the number of hexes in the grid
    RD.hextohex_d = hextohex_d;

    // Boundary fall-off distance
    RD.boundaryFalloffDist = boundaryFalloffDist;

    RD.aNoiseGain = aNoiseGain;
    RD.aInitialOffset = aInitialOffset;

    // After setting N and M, we can set up all the vectors in RD:
    RD.allocate();

    // After allocate(), we can set up parameters:
    RD.set_D (D);

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
        cout << "Set xinit["<<i<<"] to " << gp.x << endl;
        gp.y = v.get("yinit", 0.0).asDouble();
        RD.initmasks.push_back (gp);
    }

    // Index through guidance molecule parameters:
    for (unsigned int j = 0; j < guid.size(); ++j) {
        Json::Value v = guid[j];
        // What guidance molecule method will we use?
        string rmeth = v.get ("shape", "Sigmoid1D").asString();
        DBG ("guidance modelecule shape: " << rmeth);
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
        DBG ("guidance modelecule gain: " << RD.guidance_gain.back());
        RD.guidance_phi.push_back (v.get("phi", 1.0).asDouble());
        RD.guidance_width.push_back (v.get("width", 1.0).asDouble());
        RD.guidance_offset.push_back (v.get("offset", 1.0).asDouble());
    }

    // Set up the interaction parameters between the different TC
    // populations and the guidance molecules (aka gamma).
    int paramRtn = 0;
    for (unsigned int i = 0; i < tcs.size(); ++i) {
        Json::Value tcv = tcs[i];
        Json::Value gamma = tcv["gamma"];
        for (unsigned int j = 0; j < guid.size(); ++j) {
            // Set up gamma values using a setter which checks we
            // don't set a value that's off the end of the gamma
            // container.
            cout << "Set gamma for guidance " << j << " over TC " << i << " = " << gamma[j] << endl;
            paramRtn += RD.setGamma (j, i, gamma[j].asDouble());
        }
    }

    if (paramRtn && M_GUID>0) {
        cerr << "Something went wrong setting gamma values" << endl;
        return paramRtn;
    }

    // Now have the guidance molecule densities and their gradients computed, call init()
    RD.init();

    vector<vector<FLT> > gx = plt.separateVectorField (RD.g, 0);
    vector<vector<FLT> > gy = plt.separateVectorField (RD.g, 1);
    FLT ming = 1e7;
    FLT maxg = -1e7;

    // Plot gradients of the guidance effect g.
    plt.scalarfields (displays[guide_id], RD.hg, RD.rho);
    displays[guide_id].redrawDisplay();

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
    cout << "min g = " << ming << " and max g = " << maxg << endl;

    // Now plot fields and redraw display
#if 0
    plt.scalarfields (displays[guidegrad_x_id], RD.hg, gx, ming, maxg);
    displays[guidegrad_x_id].redrawDisplay();
    plt.scalarfields (displays[guidegrad_y_id], RD.hg, gy, ming, maxg);
    displays[guidegrad_y_id].redrawDisplay();
#endif
    // At step 0, there's no connection/contour information to show,
    // but we can save the initial branching.
#if 0
    if (scale_a) {
        plt.scalarfields (displays[a_id], RD.hg, RD.a); // scale between min and max
    } else {
        plt.scalarfields (displays[a_id], RD.hg, RD.a, 0.0); // scale between 0 and max
    }
#endif
    // Ask for a keypress before exiting so that the final images can be studied
    int a;
    cout << "Press any key[return] to exit.\n";
    cin >> a;

    return 0;
};
