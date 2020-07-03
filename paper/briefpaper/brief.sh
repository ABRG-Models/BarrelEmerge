#!/bin/bash

cat > sebcolour.tex <<EOF
% Colours for revisions
\definecolor{colcmnt}        {rgb} {1,      0,      0}      % blue
\definecolor{colmpfour}      {rgb} {0.220,  0.463,  0.114}  % blue
\definecolor{colmptwo}       {rgb} {0.235,  0.471,  0.847}  % green
\definecolor{colmetrics}     {rgb} {0.8353, 0.1255, 0.1255} % red
\definecolor{colmpthreepred} {rgb} {0.8235, 0.4275, 0.0}    % orange
\definecolor{colmpsix}       {rgb} {0.8,    0.1,    0.8}    % purple
\definecolor{colmpfive}      {rgb} {0.3882, 0.0745, 0.7098} % purple2
\definecolor{colmpone}       {rgb} {0.7098, 0.0745, 0.6431} % pink
\definecolor{colmpthreepar}  {rgb} {0,      0,      0.3}    % blueblack
\definecolor{colmpthreesens} {rgb} {0,      0.2,    0}      % greenblack
EOF

xelatex brief.tex
bibtex brief.aux
xelatex brief.tex
xelatex brief.tex
