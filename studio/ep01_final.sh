#!/bin/bash
cd /home/user/mahagatha-studio; L=/tmp/ep01_final.log; echo "start $(date)" > $L
python3 studio/studio.py render 01 --workers 4 --silent > /tmp/ep01_render_1080.log 2>&1
if [ -f renders/ep01_1080p.mp4 ]; then
  echo "1080p done $(date)" >> $L
  python3 studio/music.py 01 >> $L 2>&1
  ffmpeg -loglevel error -y -i renders/ep01_1080p.mp4 -c:v libx264 -preset veryfast -crf 24 -maxrate 6M -bufsize 12M -an renders/ep01_1080p_share.mp4
  ffmpeg -loglevel error -y -i renders/ep01_1080p_share.mp4 -i renders/ep01_music.mp3 -c:v copy -c:a aac -b:a 192k -shortest renders/ep01_1080p_share_with_music.mp4
  echo "SHARE READY $(date)" >> $L
else echo "1080p FAILED $(date)" >> $L; fi
python3 studio/studio.py render 01 --res 4k --workers 4 --silent > /tmp/ep01_render_4k.log 2>&1
[ -f renders/ep01_4k.mp4 ] && echo "4K DONE $(date)" >> $L
echo "ALL DONE $(date)" >> $L
