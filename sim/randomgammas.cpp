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

#include <morph/Random.h>
#include <iostream>
#include <sstream>

int main (int argc, char** argv)
{
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " max random value (a float)\n";
        return -1;
    }

    float rmax = 0.0f;
    std::stringstream ss;
    ss << argv[1];
    ss >> rmax;

    morph::RandUniform<float> rng(0.0f, rmax);

    for (unsigned int i = 0; i < 82; ++i) {
        std::cout << rng.get() << " ";
    }
    std::cout << "\n";

    return 0;
}
