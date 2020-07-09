#!/bin/bash

# Now the one with all pink changes, for reviewers
cat > sebcolour.tex <<EOF
% Colours for reviewers
\definecolor{colcmnt}        {rgb} {0.7098, 0.0745, 0.6431}
\definecolor{colmpfour}      {rgb} {0.7098, 0.0745, 0.6431}
\definecolor{colmptwo}       {rgb} {0.7098, 0.0745, 0.6431}
\definecolor{colmetrics}     {rgb} {0.7098, 0.0745, 0.6431}
\definecolor{colmpthreepred} {rgb} {0.7098, 0.0745, 0.6431}
\definecolor{colmpsix}       {rgb} {0.7098, 0.0745, 0.6431}
\definecolor{colmpfive}      {rgb} {0.7098, 0.0745, 0.6431}
\definecolor{colmpone}       {rgb} {0.7098, 0.0745, 0.6431}
\definecolor{colmpthreepar}  {rgb} {0.7098, 0.0745, 0.6431}
\definecolor{colmpthreesens} {rgb} {0.7098, 0.0745, 0.6431}
EOF

xelatex -jobname=barrels_review brief.tex
bibtex barrels_review.aux
xelatex -jobname=barrels_review brief.tex
xelatex -jobname=barrels_review brief.tex
