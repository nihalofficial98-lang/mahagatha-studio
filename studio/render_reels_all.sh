cd /home/user/mahagatha-studio
for r in reel17 reel08 reel16 reel18 reel19 reel20 reel21 reel22 reel23 reel24 reel25 reel26 reel27 reel28; do
  if [ -f renders/${r}_1080x1920.mp4 ]; then echo "skip $r" >> build/render_done.txt; continue; fi
  python3 studio/render_chunks.py $r --res 1080p --fps 24 --workers 4 --chunk 150 > /tmp/render_$r.log 2>&1
  echo "$r $(date +%T) $(tail -1 /tmp/render_$r.log | cut -c1-80)" >> build/render_done.txt
done
echo ALLDONE >> build/render_done.txt
