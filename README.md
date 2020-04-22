# BarrelEmerge

Emergence of whisker barrels with modified Karbowski-Ermentrout-like axon branching population model

For instructions on reproducing the results of papers, see the
README.md file in the paper/briefpaper subdirectory.

Before you do that, you'll need to build this simulation code, which
is compiled against our library of research software,
morphologica. So, first, obtain and build morphologica (it has its own
README.md with instructions). morphologica can be obtained here on
github:

https://github.com/ABRG-Models/morphologica/tree/master/

(Note that I've linked to you a particular branch of morphologica, in
case any future changes there break the compilation of this version of
BarrelEmerge).

Once you've compiled and installed morphologica, you can compile BarrelEmerge:

```bash
cd BarrelEmerge
mkdir build
pushd build
cmake ..
make -j4 # or however many cores you have
# (no need to install, you'll run the simulations in place)
popd
```

If you have any trouble, please post an issue on github at
https://github.com/ABRG-Models/BarrelEmerge/issues and I will do my
best to help.

Seb James, January 2020.
