#!/bin/bash

# Use convert to snip out bits of the rendered latex into png images
# suitable for Google docs

# Basic Karbowski
convert -verbose -density 450 -trim "poster_equations.pdf[0]" -quality 100 -antialias -flatten -crop 1850x700+950+1275 "WBEqns_01_to_03.jpg" &

convert -verbose -density 450 -trim "poster_equations.pdf[0]" -quality 100 -antialias -flatten -crop 1850x245+950+2040 "WBEqns_04_to_04.jpg" &

convert -verbose -density 450 -trim "poster_equations.pdf[0]" -quality 100 -antialias -flatten -crop 1850x245+950+2400 "WBEqns_05_to_05.jpg" &

# With competition
convert -verbose -density 450 -trim "poster_equations.pdf[0]" -quality 100 -antialias -flatten -crop 1850x800+950+2900 "WBEqns_06_to_08.jpg" &

convert -verbose -density 450 -trim "poster_equations.pdf[0]" -quality 100 -antialias -flatten -crop 1850x225+950+3850 "WBEqns_09_to_09.jpg" &

wait
