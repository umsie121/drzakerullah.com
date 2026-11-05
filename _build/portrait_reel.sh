#!/bin/bash
# Builds the phone (portrait 2:3) cut of the hero reel from assets/video/reel.mp4.
# Single-person shots are framed on the person; the two-person podcast shot is split
# top/bottom (Mr Ullah on top, clear of the headline). Run from the repo root.
set -e
IN=assets/video/reel.mp4; OUT=${1:-assets/video}
W=1080; H=1620; HALF=810; SLOW=1.25; F=0.4
UP="scale=$W:$H:flags=lanczos,unsharp=5:5:0.7:5:5:0"
# type start end params
#   full  : crop-x of a 720x1080 window
#   split : top-x top-y bottom-x bottom-y of two 800x600 windows
SHOTS=(
  "split 0.0 2.4 0 220 1120 200"
  "full 3.0 4.65 610"
  "full 7.0 8.35 290"
  "full 12.8 14.05 950"
  "full 14.45 16.0 590"
)
fc=""; i=0
for s in "${SHOTS[@]}"; do
  read t a b p1 p2 p3 p4 <<<"$s"
  base="[0:v]trim=$a:$b,setpts=(PTS-STARTPTS)*$SLOW"
  if [ "$t" = full ]; then
    fc+="$base,crop=720:1080:$p1:0,$UP,fps=25,format=yuv420p,settb=1/25[s$i];"
  else
    fc+="$base,split[t$i][b$i];"
    fc+="[t$i]crop=800:600:$p1:$p2,scale=$W:$HALF:flags=lanczos[tt$i];"
    fc+="[b$i]crop=800:600:$p3:$p4,scale=$W:$HALF:flags=lanczos[bb$i];"
    fc+="[tt$i][bb$i]vstack,drawbox=x=0:y=$((HALF-3)):w=$W:h=6:color=0x221019:t=fill,unsharp=5:5:0.7:5:5:0,fps=25,format=yuv420p,settb=1/25[s$i];"
  fi
  d[$i]=$(echo "($b-$a)*$SLOW" | bc); i=$((i+1))
done
n=$i; prev=s0; off=0
for ((i=1; i<n; i++)); do
  off=$(echo "$off+${d[$((i-1))]}-$F" | bc)
  fc+="[$prev][s$i]xfade=transition=fade:duration=$F:offset=$off[x$i];"; prev=x$i
done
ffmpeg -v error -y -i $IN -filter_complex "${fc%;}" -map "[$prev]" -an -c:v libx264 -profile:v high -crf 21 -preset slow -movflags +faststart -pix_fmt yuv420p $OUT/reel-portrait.mp4
ffmpeg -v error -y -i $OUT/reel-portrait.mp4 -an -c:v libvpx-vp9 -b:v 0 -crf 33 -row-mt 1 $OUT/reel-portrait.webm
ffmpeg -v error -y -ss 0.6 -i $OUT/reel-portrait.mp4 -frames:v 1 -q:v 3 $OUT/reel-portrait-poster.jpg
