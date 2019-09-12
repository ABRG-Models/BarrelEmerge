//
// Load HexGrid and regions data from h5. Run Dirichlet analysis code on them.
//

#include "morph/HexGrid.h"
#include "morph/ReadCurves.h"
#include "morph/display.h"
#include "morph/tools.h"
#include <iostream>
#include <vector>
#include <list>
#include <unistd.h>

#define DBGSTREAM std::cout
#define DEBUG 1
#include "morph/MorphDbg.h"

#include "morph/ShapeAnalysis.h"

#include "morph/MathConst.h"

using namespace morph;
using namespace std;

#define READIT true

int main (int argc, char** argv)
{
    int rtn = 0;

    int viewnum = 0;
    if (argc > 1) {
        viewnum = atoi(argv[1]);
    }

    try {
        // Load from file
        string path = "../logs/25N2M_withcomp_realmap/hexgrid.h5";
        HexGrid hg (path);

        cout << hg.extent() << endl;

        cout << "Number of hexes in grid:" << hg.num() << endl;
        cout << "Last vector index:" << hg.lastVectorIndex() << endl;

        // Make up a variable.
        vector<float> f (hg.num(), 0.1f);
        {
            HdfData d("../logs/25N2M_withcomp_realmap/c_16000.h5", READIT);
            d.read_contained_vals ("/dr", f);
        }

        // The code to actually test:
        list<morph::DirichVtx<float>> vertices;
        list<morph::DirichDom<float>> domains = morph::ShapeAnalysis<float>::dirichlet_vertices (&hg, f, vertices);

        // Carry out the analysis.
        vector<pair<float, float>> d_centres;
        float analysis = morph::ShapeAnalysis<float>::dirichlet_analyse (domains, d_centres);
        cout << "Result of analysis: " << analysis << endl;
        cout << d_centres.size() << " Ps" << endl;

        // Draw it up.
        vector<double> fix(3, 0.0);
        vector<double> eye(3, 0.0);
        eye[2] = 0.12; // This also acts as a zoom. more +ve to zoom out, more -ve to zoom in.
        vector<double> rot(3, 0.0);
        double rhoInit = 1.7;
        morph::Gdisplay disp(1600, 1600, 0, 0, "A boundary", rhoInit, 0.0, 0.0);
        disp.resetDisplay (fix, eye, rot);
        disp.redrawDisplay();

        // plot stuff here.
        array<float,3> offset = {{0, 0, 0}};
        array<float,3> offset2 = {{0, 0, 0.001}};
        array<float,3> cl_b = {{1.,1.,1.}};
        array<float,3> cl_b2 = {{0.5,0.5,0.5}};
        array<float,3> cl_red2 = {{0.5,0.0,0.05}};
        array<float,3> cl_gn2 = {{0.0,0.5,0.05}};
        array<float,3> cl_bl2 = {{0.0,0.05,0.5}};
        float sz = hg.hexen.front().d;
        for (auto h : hg.hexen) {
            array<float,3> cl_a = morph::Tools::getJetColorF (f[h.vi]);
            disp.drawHex (h.position(), offset, (sz/2.0f), cl_a);
            // On boundary draw small marker hex.
            if (h.boundaryHex()) {
                disp.drawHex (h.position(), offset2, (sz/10.0f), cl_b);
            }
            if (h.getUserFlag(0)==true && h.getUserFlag(1)==false) {
                disp.drawHex (h.position(), offset2, (sz/6.0f), cl_b2);
            }
            if (h.getUserFlag(1)==true) {
                disp.drawHex (h.position(), offset2, (sz/6.0f), cl_gn2);
            }
        }

        // Draw Dirichlet domains
        array<float,3> offset3 = {{0, 0, 0.001}};
        array<float,3> cl_d = {{ 1.0, 0, 0  }};
        array<float,3> cl_e = {{ 0, 0, 0 }};
        array<float,3> cl_f = {{ 0, 0, 0.8f }};
        array<float,3> cl_g = {{ 0.5f, 0, 0.8f }};
        array<float,3> cl_h = {{ 0.3f, 0.6f, 0.1f }};
        unsigned int count = 0;
        for (auto dom_outer : domains) {
            if (count == (unsigned int)viewnum) {
                for (auto dom_inner : dom_outer.vertices) {
                    // Draw the paths
                    for (auto path : dom_inner.pathto_next) {
                        array<float,3> posn = {{0,0,0.003}};
                        posn[0] = path.first;
                        posn[1] = path.second;
                        disp.drawHex (posn, offset3, (sz/6.0f), cl_d);
                    }
                    for (auto path : dom_inner.pathto_neighbour) {
                        array<float,3> posn = {{0,0,0.003}};
                        posn[0] = path.first;
                        posn[1] = path.second;
                        disp.drawHex (posn, offset3, (sz/8.0f), cl_e);
                    }
                    // Draw the vertices
                    array<float,3> posn1 = {{dom_inner.v.first,dom_inner.v.second,0.004}};
                    disp.drawHex (posn1, offset3, (sz/4.0f), cl_f);
                    posn1[0] = dom_inner.vn.first;
                    posn1[1] = dom_inner.vn.second;
                    // Neighbour vertices
                    disp.drawHex (posn1, offset3, (sz/4.0f), cl_g);

                    posn1[0] = dom_inner.P_i.first;
                    posn1[1] = dom_inner.P_i.second;
                    disp.drawHex (posn1, offset3, (sz/8.0f), cl_h);
                    // Draw a line from Ai to Pi
                    disp.drawLine ((double)posn1[0], (double)posn1[1], 0.006,
                                   (double)dom_inner.v.first, (double)dom_inner.v.second, 0.006,
                                   0.8, 0.05, 0.2,   0.3);


                }
            }
            // Draw best P for each domain
            array<float,3> posn2 = {{d_centres[count].first, d_centres[count].second, 0.003}};
            disp.drawHex (posn2, offset3, (sz/4.0f), cl_d);

            ++count;
        }

        // To avoid the annoying failure to draw, first sleep a while...
        usleep (100000);
        disp.redrawDisplay();

        unsigned int sleep_seconds = 1000;
        cout << "Sleep " << sleep_seconds << " s before closing display..." << endl;
        while (sleep_seconds--) {
            usleep (1000000); // one second
        }
        disp.closeDisplay();

    } catch (const exception& e) {
        cerr << "Caught exception: " << e.what() << endl;
        cerr << "Current working directory: " << Tools::getPwd() << endl;
        rtn = -1;
    }
    return rtn;
}
