#!/bin/bash

if [ ! -z ${1} ]; then
    pushd ${1}
fi

for i in contours connections axonbranch a_contours; do
    touch ${i}.mp4
    ffmpeg -r 20 -i ${i}_%05d.png -vb 5MB -vcodec mpeg4 ${i}.mp4 -y
done
