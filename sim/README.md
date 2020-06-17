## Simulation source code

I'll just list the most important source code files here.

### james1.cpp

Contains the main() function for the simulation. Compiled with
different compiler flags to create several binaries, including:

* james0 - Karbowsi-Ermentrout in 2D
* james_comp2 - The main model discussed in the paper. Adds competition.
* james_comp2c - Like james_comp2, but with no graphics; computation only.

### rd_james.h

Contains the base class for the simulation. This implements the
Karbowski-Ermentrout system in 2D.

### rd_james_comp2.h

Extends RD_James with competition.

### convKernel.cpp

Compiles a program which shows the covolution-with-a-Gaussian used to
add noise to guidance fields for Fig 3.

### randomgammas.cpp

A utility program to generate good random numbers. Used by some of the scripts.
