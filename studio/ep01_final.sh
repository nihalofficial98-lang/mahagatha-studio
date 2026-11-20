#!/bin/bash
# EP1 1080p only: wait for render -> compressed copy under 400 MB with the proper name
cd /home/user/mahagatha-studio; L=/tmp/ep01_final.log
while pgrep -f "^python3 studio/studio.py render 01" >/dev/null; do sleep 10; done
if [ -f renders/ep01_1080p.mp4 ]; then
  echo "1080p done $(date)" >> $L
  ffmpeg -loglevel error -y -i renders/ep01_1080p.mp4 -c:v libx264 -preset fast -crf 19 -maxrate 4.9M -bufsize 10M -an -movflags +faststart renders/EP01_Srishti_Ka_Janm_Aur_Madhu_Kaitabh_1080p.mp4
  echo "SHARE READY $(date)" >> $L
else echo "1080p FAILED $(date)" >> $L; fi
