#!/bin/bash

xelatex brief_pp.tex
bibtex brief_pp.aux
xelatex brief_pp.tex
xelatex brief_pp.tex
