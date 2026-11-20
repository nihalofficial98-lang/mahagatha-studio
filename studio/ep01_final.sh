#!/bin/bash
# EP1 1080p only (no 4K): render -> music -> compressed share copies
cd /home/user/mahagatha-studio; L=/tmp/ep01_final.log
while pgrep -f "^python3 studio/studio.py render 01" >/dev/null; do sleep 15; done
if [ -f renders/ep01_1080p.mp4 ]; then
  echo "1080p done $(date)" >> $L
  python3 studio/music.py 01 >> $L 2>&1
  ffmpeg -loglevel error -y -i renders/ep01_1080p.mp4 -c:v libx264 -preset veryfast -crf 24 -maxrate 6M -bufsize 12M -an renders/ep01_1080p_share.mp4
  ffmpeg -loglevel error -y -i renders/ep01_1080p_share.mp4 -i renders/ep01_music.mp3 -c:v copy -c:a aac -b:a 192k -shortest renders/ep01_1080p_share_with_music.mp4
  echo "SHARE READY $(date)" >> $L
else echo "1080p FAILED $(date)" >> $L; fi
