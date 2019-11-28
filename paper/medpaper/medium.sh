#!/bin/bash

xelatex medium.tex
bibtex medium.aux
xelatex medium.tex
xelatex medium.tex
