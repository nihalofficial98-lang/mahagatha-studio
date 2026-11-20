#!/bin/bash
# EP1 1080p only: render -> compressed share copy (no 4K, no music)
cd /home/user/mahagatha-studio; L=/tmp/ep01_final.log
while pgrep -f "^python3 studio/studio.py render 01" >/dev/null; do sleep 15; done
if [ -f renders/ep01_1080p.mp4 ]; then
  echo "1080p done $(date)" >> $L
  ffmpeg -loglevel error -y -i renders/ep01_1080p.mp4 -c:v libx264 -preset veryfast -crf 24 -maxrate 6M -bufsize 12M -an renders/ep01_1080p_share.mp4
  echo "SHARE READY $(date)" >> $L
else echo "1080p FAILED $(date)" >> $L; fi
