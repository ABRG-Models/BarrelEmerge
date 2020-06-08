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
