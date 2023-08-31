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
 * Visualize convolution kernels on same grid as Barrel sim
 *
 * Author: Seb James
 * Date: June 2020
 */
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>

#include <morph/Visual.h>
#include <morph/VisualDataModel.h>
#include <morph/HexGridVisual.h>
#include <morph/HexGrid.h>
#include <morph/ReadCurves.h>
#include <morph/tools.h>
#include <morph/Random.h>
#include <morph/Scale.h>
#include <morph/vec.h>

int main(int argc, char** argv)
{
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " kernel_width (Try 0.04 as a good example)\n";
        return -1;
    }

    std::stringstream ss;
    float sigma = 0.0f;
    ss << argv[1];
    ss >> sigma;

    // This should match the hextohex you're using in the configs. Mostly, that's 0.03 in BarrelEmerge.
    float hextohex_d = 0.03f;

    int rtn = 0;

    morph::Visual v(800,600,"Convolution window");
    v.zNear = 0.001;
    v.setSceneTransZ (-9.0f);

    try {
        std::string pwd = morph::Tools::getPwd();
        std::cout << "pwd: " << pwd << "\n";
        std::string curvepath = "./boundaries/rat_barrels/wb_110405_Dirichlet.svg";
        if (pwd.substr(pwd.length()-5) == "build") {
            curvepath = "./../boundaries/rat_barrels/wb_110405_Dirichlet.svg";
        }
        morph::ReadCurves r(curvepath);

        morph::HexGrid hg(hextohex_d, 4, 0);
        hg.setBoundary (r.getCorticalPath());

        // Populate a vector of floats with data
        std::vector<float> data (hg.num(), 0.0f);
        morph::RandUniform<float> rng;
        for (float& d : data) {
            d = rng.get();
        }

        // Create a circular HexGrid to contain the Gaussian convolution kernel
        morph::HexGrid kernel(hextohex_d, 20.0f*sigma, 0);
        kernel.setCircularBoundary (6.0f*sigma);
        std::vector<float> kerneldata (kernel.num(), 0.0f);
        // Once-only parts of the calculation of the Gaussian.
        float one_over_sigma_root_2_pi = 1 / sigma * 2.506628275;
        float two_sigma_sq = 2.0f * sigma * sigma;
        // Gaussian dist. result, and a running sum of the results:
        float gauss = 0;
        float sum = 0;
        for (auto& k : kernel.hexen) {
            // Gaussian profile based on the hex's distance from centre, which is
            // already computed in each Hex as Hex::r
            gauss = (one_over_sigma_root_2_pi * std::exp ( -(k.r*k.r) / two_sigma_sq ));
            kerneldata[k.vi] = gauss;
            sum += gauss;
        }
        // Renormalise
        for (auto& k : kernel.hexen) { kerneldata[k.vi] /= sum; }

        // A vector for the result
        std::vector<float> convolved (hg.num(), 0.0f);

        // Call the convolution method from HexGrid:
        hg.convolve (kernel, kerneldata, data, convolved);

        // Visualize the 3 maps
        morph::vec<float, 3> offset = { -1.1, 0.0, 0.0 };
        auto hgv = std::make_unique<morph::HexGridVisual<float>>(&hg, offset);
        v.bindmodel (hgv);
        hgv->setScalarData (&data);
        hgv->finalize();
        auto gridId = v.addVisualModel (hgv);
        offset[1] += hg.depth()/2.0f;
        offset[0] += (hg.width()/2.0f);
        auto hgv_k = std::make_unique<morph::HexGridVisual<float>>(&kernel, offset);
        v.bindmodel (hgv_k);
        hgv_k->setScalarData (&kerneldata);
        hgv_k->finalize();
        v.addVisualModel (hgv_k);
        offset[0] += (hg.width()/2.0f);
        offset[1] -= hg.depth()/2.0f;
        auto hgv_c = std::make_unique<morph::HexGridVisual<float>>(&hg, offset);
        v.bindmodel (hgv_c);
        hgv_c->setScalarData (&convolved);
        hgv_c->finalize();
        auto gridId2 = v.addVisualModel (hgv_c);

        // Divide existing scale by 10:
        float newGrad = gridId->zScale.getParams(0)/10.0;
        // Set this in a new zscale object:
        morph::Scale<float> zscale;
        zscale.setParams (newGrad, 0);
        // And set it back into the visual model:
        gridId->setZScale (zscale);
        gridId->reinit();
        gridId2->setZScale (zscale);
        gridId2->reinit();

        v.render();

        while (v.readyToFinish == false) {
            glfwWaitEventsTimeout (0.018);
            v.render();
        }

    } catch (const std::exception& e) {
        std::cerr << "Caught exception reading trial.svg: " << e.what() << std::endl;
        std::cerr << "Current working directory: " << morph::Tools::getPwd() << std::endl;
        rtn = -1;
    }

    return rtn;
}
