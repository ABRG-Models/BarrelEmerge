# BarrelEmerge

This is a simulation of the growth of axons which demonstrates how the
whisker barrel field pattern can self-organize in the presence of only
two orthogonal molecular guidance cues. It is the code behind the
following paper (archive branch: [eLife](https://github.com/ABRG-Models/BarrelEmerge/tree/eLife)):

James, Krubitzer & Wilson. 2020. *Modelling the emergence of whisker
barrels*. eLife. DOI: https://doi.org/10.7554/eLife.55588

The emergence of whisker barrels is demonstrated in a modified
Karbowski-Ermentrout-like axon branching population model.

![Shows Fig 1 from the paper](https://github.com/ABRG-Models/BarrelEmerge/blob/master/paper/briefpaper/Fig1.png?raw=true)
*A: CO stain of the rat barrel field B: Centres of thalamic barreloids provide interaction parameters for axon bundles growing into the cortical subplate C: Cortical fields emerge D & E: Pattern quality measures*


For instructions on reproducing the results of the paper, see the
README.md file in the scripts subdirectory.

Before you do that, you'll need to build this simulation code, which
is compiled using our library of research software, morphologica.

morphologica is pulled in as a git submodule, but you'll still need to
install the dependencies for the morphologica code, which are: OpenCV,
Armadillo, OpenGL, HDF5, LAPACK and glfw.  Refer to the instructions
in the morphologica README.install files, covering installation of
dependences on Mac or Linux. On a Debian based Linux, this should
work:

```bash
sudo apt install build-essential cmake git \
                 freeglut3-dev libglu1-mesa-dev libxmu-dev libxi-dev \
                 libglfw3-dev libfreetype-dev

sudo apt install libarmadillo-dev libhdf5-dev libopencv-dev
```

With dependences installed you can build BarrelEmerge:

```bash
# Clone, making sure to get the submodules (morphologica)
git clone --recurse-submodules https://github.com/ABRG-Models/BarrelEmerge.git

# If you ALREADY did a git clone *without* --recurse-submodules, then don't panic! just do:
# cd BarrelEmerge
# git submodule init
# git submodule update

cd BarrelEmerge
mkdir build
pushd build
cmake ..
make -j4 # or however many cores you have
# (no need to install, you'll run the simulations in place)
popd
```

**Note:** You'll ideally have an OpenMP-capable compiler. You'll
probably need libomp as well, because even though my code doesn't use
the runtime part of OpenMP, Armadillo does. You get OpenMP/libomp for free with gcc on a modern Linux
computer; on a Mac, you will have to install libomp from source
(follow instructions at https://openmp.llvm.org/ finishing up with a
final `make install`).

Now you can read how to reproduce the experiments. To reproduce all of
the results, see ./scripts/README.md. To graph the resulting data, see
./analysis/README.md.

To reproduce, and simultaneously view, the main result, as presented
in Fig. 1C, you can run one simulation:

```bash
./build/sim/james_comp2 ./configs/rat/41N2M_thalguide_Fig1.json
```

**Note:** The simulation is computationally demanding. It takes about
11 minutes to run the 50000 steps of Fig. 1C simulation on a 6-core
gaming laptop (with an 8th gen Intel Core i9 processor and with the code
compiled with OpenMP to use all the cores). An older, 6th gen Core i5
laptop (2 cores) needs 23 minutes to run the same simulation.

If you have any trouble, please post an issue on github at
https://github.com/ABRG-Models/BarrelEmerge/issues and I will do my
best to help.

Seb James, September 2020.
