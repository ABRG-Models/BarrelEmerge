#!/bin/bash

xelatex paper.tex
bibtex paper.aux
xelatex paper.tex
xelatex paper.tex
