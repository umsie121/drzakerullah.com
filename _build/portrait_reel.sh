#!/bin/bash
# build a portrait (2:3) phone reel from reel.mp4: single-person shots, each framed on the person
set -e
IN=assets/video/reel.mp4; OUT=${1:-assets/video}
# start end crop-x   (crop is 720x1080 of the 1920x1080 source)
SHOTS=("3.0 4.65 610" "7.0 8.35 290" "11.1 12.55 725" "12.8 14.05 950" "14.45 16.0 590")
F=0.4; fc=""; n=${#SHOTS[@]}; i=0
for s in "${SHOTS[@]}"; do read a b x <<<"$s"
  fc+="[0:v]trim=$a:$b,setpts=(PTS-STARTPTS)*1.25,crop=720:1080:$x:0,fps=25,format=yuv420p,settb=1/25[s$i];"; d[$i]=$(echo "($b-$a)*1.25"|bc); i=$((i+1)); done
prev="s0"; off=0
for ((i=1;i<n;i++)); do off=$(echo "$off+${d[$((i-1))]}-$F"|bc); fc+="[$prev][s$i]xfade=transition=fade:duration=$F:offset=$off[x$i];"; prev="x$i"; done
fc=${fc%;}
ffmpeg -v error -y -i $IN -filter_complex "$fc" -map "[$prev]" -an -c:v libx264 -profile:v high -crf 24 -preset slow -movflags +faststart -pix_fmt yuv420p $OUT/reel-portrait.mp4
ffmpeg -v error -y -i $OUT/reel-portrait.mp4 -an -c:v libvpx-vp9 -b:v 0 -crf 36 -row-mt 1 $OUT/reel-portrait.webm
ffmpeg -v error -y -ss 0.5 -i $OUT/reel-portrait.mp4 -frames:v 1 -q:v 4 $OUT/reel-portrait-poster.jpg
