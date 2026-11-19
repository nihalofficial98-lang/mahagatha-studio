#!/bin/bash
# overnight chain: EP3 finishes -> mux music; EP1 4K (fallback 1080p) -> music -> mux; logs in /tmp/overnight.log
cd /home/user/mahagatha-studio
L=/tmp/overnight.log; echo "start $(date)" > $L
while [ ! -f renders/ep03_1080p.mp4 ]; do sleep 20; done
sleep 30; echo "ep03 video ready $(date)" >> $L
ffmpeg -loglevel error -y -i renders/ep03_1080p.mp4 -i renders/ep03_music.mp3 -c:v copy -c:a aac -b:a 192k -shortest renders/ep03_1080p_with_music.mp4 && echo "ep03 muxed $(date)" >> $L
python3 studio/studio.py render 01 --res 4k --workers 4 --silent > /tmp/ep01_render.log 2>&1
if [ -f renders/ep01_4k.mp4 ]; then
  echo "ep01 4k done $(date)" >> $L; RES=4k
  ffmpeg -loglevel error -y -i renders/ep01_4k.mp4 -vf scale=1920:1080 -c:v libx264 -preset medium -crf 20 -an renders/ep01_1080p.mp4 && echo "ep01 1080p copy made $(date)" >> $L
else
  echo "ep01 4k FAILED, falling back to 1080p $(date)" >> $L
  python3 studio/studio.py render 01 --workers 4 --silent > /tmp/ep01_render_1080.log 2>&1; RES=1080p
fi
python3 studio/music.py 01 >> $L 2>&1
[ -f renders/ep01_${RES}.mp4 ] && ffmpeg -loglevel error -y -i renders/ep01_${RES}.mp4 -i renders/ep01_music.mp3 -c:v copy -c:a aac -b:a 192k -shortest renders/ep01_${RES}_with_music.mp4 && echo "ep01 muxed $(date)" >> $L
echo "ALL DONE $(date)" >> $L
