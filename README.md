# BarrelEmerge

This is a simulation of the growth of axons which demonstrates how the
whisker barrel field pattern can selforganize in the presence of only
two orthogonal molecular guidance cues. It is the code behind the
eLife paper:

*"Modelling the Emergence of Whisker Barrels"*

The emergence of whisker barrels is demonstated in a modified
Karbowski-Ermentrout-like axon branching population model.

For instructions on reproducing the results of the paper, see the
README.md file in the paper/scripts subdirectory.

Before you do that, you'll need to build this simulation code, which
is compiled against our library of research software,
morphologica. So, first, obtain and build morphologica (it has its own
README.md with instructions). morphologica can be obtained here on
github:

https://github.com/ABRG-Models/morphologica/tree/papers/BarrelEmerge_eLife

(Note that I've linked to you a particular branch of morphologica, in
case any future changes there break the compilation of this version of
BarrelEmerge).

Once you've compiled and installed morphologica, you can compile
BarrelEmerge:

```bash
cd BarrelEmerge
mkdir build
pushd build
cmake ..
make -j4 # or however many cores you have
# (no need to install, you'll run the simulations in place)
popd
```

**Note:** You'll ideally have an OpenMP-capable compiler. You'll
probably need libomp as well, because Armadillo uses that if OpenMP is
present. You get these both for free with gcc on a modern Linux
computer; on a Mac, you will have to install libomp from source.

Now you can read how to reproduce the experiments. To reproduce all of
the results, see ./scripts/README.md. To graph the resulting data, see
./analysis/README.md.

To reproduce, and simultaneously view, the main result, as presented
in Fig. 1C, you can run one simulation:

```bash
./build/sim/james_comp2 ./configs/rat/41N2M_thalguide_Fig1.json
```

**Note:** The simulation is computationally demanding. It takes about
  10 minutes to run the Fig. 1C simulation on a 6-core gaming laptop
  (with a Core i9 intel processor and when compiled with OpenMP to use
  all the cores). Be prepared to wait on a lesser machine!

If you have any trouble, please post an issue on github at
https://github.com/ABRG-Models/BarrelEmerge/issues and I will do my
best to help.

Seb James, July 2020.
