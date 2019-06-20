#!/bin/bash

# Use convert to snip out bits of the rendered latex into png images
# suitable for Google docs

# Basic Karbowski
convert -verbose -density 450 -trim "barrel_equations.pdf[0]" -quality 100 -antialias -flatten -crop 2950x700+390+1275 "WBEqns_01_to_03.jpg" &

convert -verbose -density 450 -trim "barrel_equations.pdf[0]" -quality 100 -antialias -flatten -crop 2950x245+390+2160 "WBEqns_04_to_04.jpg" &

convert -verbose -density 450 -trim "barrel_equations.pdf[0]" -quality 100 -antialias -flatten -crop 2950x245+390+2620 "WBEqns_05_to_05.jpg" &

# With competition
convert -verbose -density 450 -trim "barrel_equations.pdf[0]" -quality 100 -antialias -flatten -crop 2950x700+390+3070 "WBEqns_06_to_08.jpg" &

convert -verbose -density 450 -trim "barrel_equations.pdf[0]" -quality 100 -antialias -flatten -crop 2950x225+390+4000 "WBEqns_09_to_09.jpg" &

wait
