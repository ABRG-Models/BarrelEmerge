#!/bin/sh
touch MovieS1.mp4
ffmpeg -r 10 -i 41N2M_thalguide_eps150_movie_c_id_%06d.png -vb 5MB -s hd1080 -vcodec mpeg4 MovieS1.mp4 -y
