#ifdef COPYLEFT
/*
 *  This file is part of BarrelEmerge.
 *
 *  BarrelEmerge is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  BarrelEmerge is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with BarrelEmerge.  If not, see <https://www.gnu.org/licenses/>.
 */
#endif

/*
 * A program to just carry out the Honda Dirichlet analysis on a suitable svg file.
 *
 * Author: Seb James <seb.james@sheffield.ac.uk>
 *
 * Date: Dec 2019
 */

/*!
 * This will be passed as the template argument for RD_Plot and RD and
 * should be defined when compiling.
 */
#ifndef FLT
// Check CMakeLists.txt to change to double or float
# error "Please define FLT when compiling (hint: See CMakeLists.txt)"
#endif

#include<list>
using std::list;
#include<vector>
using std::vector;
#include <string>
using std::string;
#include <utility>
using std::pair;
#include <iostream>
using std::cout;
using std::cerr;
using std::endl;

#define DEBUG 1
#define DEBUG2 1
#define DBGSTREAM std::cout
#include "morph/MorphDbg.h"

#include "morph/DirichVtx.h"
using morph::DirichVtx;
#include "morph/DirichDom.h"
using morph::DirichDom;
#include "morph/ShapeAnalysis.h"
#include "morph/ReadCurves.h"
using morph::ReadCurves;
#include "morph/HexGrid.h"
using morph::HexGrid;
#include "morph/Hex.h"
using morph::Hex;
#include "morph/BezCurvePath.h"
using morph::BezCurvePath;

int main (int argc, char **argv)
{
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " /path/to/file.svg" << endl;
        return 1;
    }

    // Path to svg
    string svgpath = argv[1];

    // Create HexGrid...
    float hextohex_d = 0.03; // reinstate Json for these params?
    float hexspan = 6;
    HexGrid* hg = new HexGrid (hextohex_d, hexspan, 0);
    // Read the curves which make a boundary
    ReadCurves r;
    r.init (svgpath);
    // Set the boundary in the HexGrid
    hg->setBoundary (r.getCorticalPath());
    // Compute the distances from the boundary
    hg->computeDistanceToBoundary();
    // Vector size comes from number of Hexes in the HexGrid
    unsigned int nhex = hg->num();

    vector<FLT> expt_barrel_id;
    for (unsigned int h = 0; h<nhex; h++) {
        expt_barrel_id.push_back ((FLT)-1.0f);
    }

    // Set up the barrel regions
    list<BezCurvePath<FLT>> ers = r.getEnclosedRegions();
    float theid = 0.0;
    for (auto& er : ers) {
        pair<float, float> regCentroid; // Don't use it for now...
        vector<list<Hex>::iterator> regHexes = hg->getRegion (er, regCentroid);
        string idstr("unknown");
        if (er.name.substr(0,3) == "ol_") { // "ol_" for "outline"
            idstr = er.name.substr(3);
        }
        if (idstr != "unknown") {
            // In this program, we don't care which ID is which, just that each one is different.
            theid += 0.1f;
            for (auto rh : regHexes) {
                DBG ("Setting hex["<<rh->vi<<"] to " << theid);
                expt_barrel_id[rh->vi] = theid;
            }
        }
    }

    list<DirichVtx<FLT>> vertices;
    list<DirichDom<FLT>> domains;
    vertices.clear();
    // Find the vertices and construct domains
    domains = morph::ShapeAnalysis<FLT>::dirichlet_vertices (hg, expt_barrel_id, vertices);
    cout << "There are " << vertices.size() << " vertices" << endl;
    cout << "There are " << domains.size() << " domains" << endl;
    // Carry out the analysis.
    vector<pair<float, float>> d_centres;
    float expt_honda = morph::ShapeAnalysis<float>::dirichlet_analyse (domains, d_centres);
    cout << "These barrels have Honda delta = " << expt_honda << endl;

    delete hg;

    return 0;
};
