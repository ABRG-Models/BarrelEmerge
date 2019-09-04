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
#include <cmath>
using std::atan2;

#define DBGSTREAM std::cout
#define DEBUG 1
#include "morph/MorphDbg.h"

#include "morph/ShapeAnalysis.h"

#include "morph/MathConst.h"

using namespace morph;
using namespace std;

#define READIT true

#if 1

float line_length (const pair<float, float>& coord0, const pair<float, float>& coord1)
{
    float c01 = sqrt ((coord0.first - coord1.first) * (coord0.first - coord1.first)
                      + (coord0.second - coord1.second) * (coord0.second - coord1.second));
    return c01;
}

/*!
 * For the three coordinates c0, c1, c2, compute the angle at coordinate number @angleFor
 * (counting from 0).
 *
 * To go to morph::tools or morph::maths or something.
 */
float
compute_angle (const pair<float, float>& c0,
               const pair<float, float>& c1,
               const pair<float, float>& c2,
               const unsigned int angleFor)
{
    float angle = -1.0f;
    if (angleFor == 0) {
        angle = atan2 (c2.second - c0.second, c2.first - c0.first)
            - atan2 (c1.second - c0.second, c1.first - c0.first);

    } else if (angleFor == 1) {
        angle = atan2 (c0.second - c1.second, c0.first - c1.first)
            - atan2 (c2.second - c1.second, c2.first - c1.first);

    } else if (angleFor == 2) {
        angle = atan2 (c1.second - c2.second, c1.first - c2.first)
            - atan2 (c0.second - c2.second, c0.first - c2.first);

    } else {
        throw runtime_error ("Ask for the angle around coord 0, 1 or 2 please.");
    }

    return angle;
}

/*!
 * Take a set of Dirichlet vertices defining exactly one Dirichlet
  * domain and compute a metric for the Dirichlet-ness of the vertices
 * after Honda1983.
 */
float
dirichlet_analyse_single_domain (list<DirichVtx<float> >& domain)
{
    DBG("called");
    float metric = 0.0f;

    // Now I know the ORDER of the vertices in domain I can proceed...
    // Now loop around the list computing the lines
    typename list<DirichVtx<float>>::iterator dv = domain.begin();
    typename list<DirichVtx<float>>::iterator dvnext = dv;
    typename list<DirichVtx<float>>::iterator dvprev = domain.end();
    while (dv != domain.end()) {

        DBG ("-- Domain --");

        pair<float, float> Ai = dv->v;
        pair<float, float> Bi = dv->vn;
        DBG ("Vertex A_i: (" << Ai.first << "," << Ai.second << ")");
        DBG ("Vertex B_i: (" << Bi.first << "," << Bi.second << ")");

        dvnext = ++dv;
        if (dvnext == domain.end()) {
            dvnext = domain.begin();
        }
        pair<float, float> Aip1 = dvnext->v;
        DBG ("Vertex A_i+1: (" << Aip1.first << "," << Aip1.second << ")");

        pair<float, float> Aim1;
        if (dvprev == domain.end()) {
            dvprev--;
            Aim1 = dvprev->v;
            dvprev = domain.begin();
        } else {
            Aim1 = dvprev->v;
            ++dvprev;
        }
        DBG ("Vertex A_i-1: (" << Aim1.first << "," << Aim1.second << ")");

        // Reset dv back one
        dv--;

        /*
         * 1. Compute phi, the angle Bi Ai Ai-1 using law of cosines
         */
        float phi = compute_angle (Bi, Ai, Aim1, 1);
        float theta = morph::PI_F - phi;
        DBG ("phi = " << phi << " and theta = " << theta);

        /*
         * 2. Compute the line P_i wrt to Ai and Ai+1
         */
        // 2a Project A_i+1 onto the line P_i to get the length to a point Pi on line Pi.
        float Aip1Ai = line_length (Aip1, Ai);
        // Distance that we'll travel from Ai to get to the new point Pi.
        float AiPi = Aip1Ai * cos (theta);
        // 2b Determine the coordinates of point Pi using theta and the angle from the x axis to
        // Aip1.
        float xi = atan2 ((Aip1.second - Ai.second), (Aip1.first - Ai.first));
        DBG ("xi is " << xi);

        float deltax = AiPi * cos (theta + xi);
        DBG ("deltax from Ai to Pi is " << deltax);
        float deltay = AiPi * sin (theta + xi);
        DBG ("deltay from Ai to Pi is " << deltay);

        pair<float, float> Pi = Ai;
        Pi.first += deltax;
        Pi.second += deltay;

        DBG ("Point Pi: " << Pi.first << "," << Pi.second << ")");
        dv->P_i = Pi;

        /*
         * 3. Use A_i and P_i to compute gradient/offset of the
         * line equation that passes through point A_i. Store in
         * this->m and this->c (or whatever is suitable).
         */
        if (dv->P_i.first == Ai.first) {
            dv->m = dv->P_i.second < Ai.second ? numeric_limits<float>::lowest() : numeric_limits<float>::max();
            dv->c = numeric_limits<float>::max();
            // And if c is max(), then it's a vertical line from
            // A_i through P_i which means that P_i.first ==
            // A_i.first and P_i.second can be anything.

        } else {
            dv->m = (dv->P_i.second - Ai.second) / (dv->P_i.first - Ai.first);
            dv->c = Ai.second - dv->m * Ai.first;
        }
        DBG ("Pi line gradient is m=" << dv->m << ", offset is c=" << dv->c);

        ++dv;
    }

    float num_vtx = static_cast<float>(domain.size());
    return metric/num_vtx;
}

/*!
 * Take a list of Dirichlet domains and compute a metric for the Dirichlet-ness of the vertices
 * after Honda1983.
 *
 * To go into morph::ShapeAnalysis
 */
float
dirichlet_analyse (list<list<DirichVtx<float> > >& doms)
{
    float metric = 0.0;
    auto di = doms.begin();
    while (di != doms.end()) {
        metric += dirichlet_analyse_single_domain (*di);
        ++di;
    }
    // return the arithmetic mean Dirichlet-ness measure
    return metric/(float)doms.size();
}
#endif

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
            HdfData d("../logs/25N2M_withcomp_realmap/c_14000.h5", READIT);
            d.read_contained_vals ("/dr", f);
        }

        // The code to actually test:
        list<morph::DirichVtx<float>> vertices;
        list<list<morph::DirichVtx<float> > > domains = morph::ShapeAnalysis<float>::dirichlet_vertices (&hg, f, vertices);

        // Carry out the analysis.
        float analysis = dirichlet_analyse (domains);
        cout << "Result of analysis: " << analysis << endl;

#if 1
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
        float sz = hg.hexen.front().d;
        for (auto h : hg.hexen) {
            array<float,3> cl_a = morph::Tools::getJetColorF (f[h.vi]);
            disp.drawHex (h.position(), offset, (sz/2.0f), cl_a);
            // On boundary draw small marker hex.
            if (h.boundaryHex) {
                disp.drawHex (h.position(), offset2, (sz/10.0f), cl_b);
            }
        }

#if 0
        // Output vertices
        for (auto verti : vertices) {
            cout << "Vertex: (" << verti.v.first << "," << verti.v.second  << ")"
                 << " with f=" << verti.f
                 << " edges[" << verti.neighb.first << "," << verti.neighb.second << "]" << endl;
        }
#endif

#if 0
        // Draw all vertices
        array<float,3> cl_c = morph::Tools::getJetColorF (0.98);
        for (auto verti : vertices) {
            array<float,3> posn = {{0,0,0.002}};
            posn[0] = verti.v.first;
            posn[1] = verti.v.second;
            disp.drawHex (posn, offset2, (sz/4.0f), cl_c);
        }
#endif

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
                for (auto dom_inner : dom_outer) {
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
                    disp.drawHex (posn1, offset3, (sz/4.0f), cl_g);

                    posn1[0] = dom_inner.P_i.first;
                    posn1[1] = dom_inner.P_i.second;
                    disp.drawHex (posn1, offset3, (sz/4.0f), cl_h);
                    // Draw a line from Ai to Pi
                    disp.drawLine ((double)posn1[0], (double)posn1[1], 0.006,
                                   (double)dom_inner.v.first, (double)dom_inner.v.second, 0.006,
                                   0.8, 0.05, 0.2,   0.3);

                }
            }
            ++count;
        }
# if 0
        // A colour index
        array<float,3> posn1 = {{-0.67,00.54,0.003}};
        disp.drawHex (posn1, offset3, (sz*2.0f), morph::Tools::getJetColorF (0.32));
        posn1[1] -= 0.1;
        disp.drawHex (posn1, offset3, (sz*2.0f), morph::Tools::getJetColorF (0.36));
        posn1[1] -= 0.1;
        disp.drawHex (posn1, offset3, (sz*2.0f), morph::Tools::getJetColorF (0.52));
# endif

        // To avoid the annoying failure to draw, first sleep a while...
        usleep (100000);
        disp.redrawDisplay();

        unsigned int sleep_seconds = 1000;
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
