#!/bin/bash

xelatex supp.tex
bibtex supp.aux
xelatex supp.tex
xelatex supp.tex
