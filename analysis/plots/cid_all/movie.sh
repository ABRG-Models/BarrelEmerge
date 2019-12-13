#!/bin/sh
touch 41N2M_thalguide_eps150_movie_c_id.mp4
ffmpeg -r 10 -i 41N2M_thalguide_eps150_movie_c_id_%06d.png -vb 5MB -vcodec mpeg4 41N2M_thalguide_eps150_movie_c_id.mp4 -y
