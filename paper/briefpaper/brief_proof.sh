#!/bin/bash

#
# This script builds the proof versions of the PDF: all black.
#

cat > sebcolour.tex <<EOF
% Colours for the proof PDF
\definecolor{colcmnt}        {rgb} {0, 0, 0}
\definecolor{colmpfour}      {rgb} {0, 0, 0}
\definecolor{colmptwo}       {rgb} {0, 0, 0}
\definecolor{colmetrics}     {rgb} {0, 0, 0}
\definecolor{colmpthreepred} {rgb} {0, 0, 0}
\definecolor{colmpsix}       {rgb} {0, 0, 0}
\definecolor{colmpfive}      {rgb} {0, 0, 0}
\definecolor{colmpone}       {rgb} {0, 0, 0}
\definecolor{colmpthreepar}  {rgb} {0, 0, 0}
\definecolor{colmpthreesens} {rgb} {0, 0, 0}
EOF

xelatex -jobname=barrels_proof brief.tex
bibtex barrels_proof.aux
xelatex -jobname=barrels_proof brief.tex
xelatex -jobname=barrels_proof brief.tex
