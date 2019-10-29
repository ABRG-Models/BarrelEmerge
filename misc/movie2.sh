#!/bin/bash

if [ ! -z ${1} ]; then
    pushd ${1}
fi

for i in contours maxval; do
    touch ${i}2.mp4
    ffmpeg -framerate 60 -i ${i}_%05d.png -vb 5MB -vcodec mpeg4 ${i}2.mp4 -y
done
