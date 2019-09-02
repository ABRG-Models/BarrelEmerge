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

using namespace morph;
using namespace std;

#define READIT true

int main()
{
    int rtn = 0;
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
            HdfData d("../logs/25N2M_withcomp_realmap/dv_12000.h5", READIT);
            d.read_contained_vals ("/dv_id", f);
        }

        // The code to actually test:
        list<morph::DirichVtx<float>> vertices;
        list<list<morph::DirichVtx<float> > > domains = morph::ShapeAnalysis<float>::dirichlet_vertices (&hg, f, vertices);

#if 1
        // Draw it up.
        vector<double> fix(3, 0.0);
        vector<double> eye(3, 0.0);
        eye[2] = 0.12; // This also acts as a zoom. more +ve to zoom out, more -ve to zoom in.
        vector<double> rot(3, 0.0);
        double rhoInit = 1.7;
        morph::Gdisplay disp(700, 700, 0, 0, "A boundary", rhoInit, 0.0, 0.0);
        disp.resetDisplay (fix, eye, rot);
        disp.redrawDisplay();

        // plot stuff here.
        array<float,3> offset = {{0, 0, 0}};
        array<float,3> offset2 = {{0, 0, 0.001}};
        array<float,3> cl_b = morph::Tools::getJetColorF (0.78);
        float sz = hg.hexen.front().d;
        for (auto h : hg.hexen) {
            array<float,3> cl_a = morph::Tools::getJetColorF (f[h.vi]);
            disp.drawHex (h.position(), offset, (sz/2.0f), cl_a);
            if (h.boundaryHex) {
                disp.drawHex (h.position(), offset2, (sz/12.0f), cl_b);
            }
        }

        array<float,3> cl_c = morph::Tools::getJetColorF (0.98);
        for (auto verti : vertices) {
            array<float,3> posn = {{0,0,0.002}};
            posn[0] = verti.v.first;
            posn[1] = verti.v.second;
            disp.drawHex (posn, offset2, (sz/8.0f), cl_c);
        }

        array<float,3> offset3 = {{0, 0, 0.001}};
        array<float,3> cl_d = morph::Tools::getJetColorF (0.7);
        array<float,3> cl_e = morph::Tools::getJetColorF (0.01);
        for (auto dom_outer : domains) {
            for (auto dom_inner : dom_outer) {
                // Draw the paths
                for (auto path : dom_inner.pathto_next) {
                    array<float,3> posn = {{0,0,0.003}};
                    posn[0] = path.first;
                    posn[1] = path.second;
                    disp.drawHex (posn, offset3, (sz/16.0f), cl_d);
                }
                for (auto path : dom_inner.pathto_neighbour) {
                    array<float,3> posn = {{0,0,0.003}};
                    posn[0] = path.first;
                    posn[1] = path.second;
                    disp.drawHex (posn, offset3, (sz/16.0f), cl_e);
                }
            }
        }

        // To avoid the annoying failure to draw, first sleep a while...
        usleep (100000);
        disp.redrawDisplay();

        unsigned int sleep_seconds = 10;
        cout << "Sleep " << sleep_seconds << " s before closing display..." << endl;
        while (sleep_seconds--) {
            usleep (1000000); // one second
        }
        disp.closeDisplay();
#endif

    } catch (const exception& e) {
        cerr << "Caught exception: " << e.what() << endl;
        cerr << "Current working directory: " << Tools::getPwd() << endl;
        rtn = -1;
    }
    return rtn;
}
