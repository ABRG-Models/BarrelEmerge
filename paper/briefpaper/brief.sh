#!/bin/bash

xelatex brief.tex
bibtex brief.aux
xelatex brief.tex
xelatex brief.tex
