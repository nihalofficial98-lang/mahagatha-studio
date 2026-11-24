#!/usr/bin/env bash
# Mux a finished EP6 video's video stream with the mixed sound (the owner's voice is already inside the mix).
#   usage:  episodes/ep06/sound/mix.sh <video.mp4> [out.mp4]
#   env:    AUDIO=path to the mix (default: ep06_sound_preview.mp3 next to this script)
#           PAD=seconds of last-frame hold appended so the end-logo conch/boom tail is heard (default 0 = cut at video length)
# NOT to be run until the owner has approved the sound AND the final video render is finished.
# The original video file is never modified; the output must be a different path.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VIDEO="${1:?usage: mix.sh <video.mp4> [out.mp4]}"
OUT="${2:-${VIDEO%.*}_sound.mp4}"
AUDIO="${AUDIO:-$HERE/ep06_sound_preview.mp3}"
PAD="${PAD:-0}"
[ -f "$VIDEO" ] || { echo "no such video: $VIDEO"; exit 1; }
[ -f "$AUDIO" ] || { echo "no such audio: $AUDIO"; exit 1; }
[ "$OUT" != "$VIDEO" ] || { echo "out must differ from the input video"; exit 1; }

if [ "$PAD" != "0" ]; then
  # re-encodes the video (needed to extend the last frame)
  nice -n 19 ffmpeg -y -v error -i "$VIDEO" -i "$AUDIO" \
    -filter_complex "[0:v]tpad=stop_mode=clone:stop_duration=${PAD}[v]" \
    -map "[v]" -map 1:a:0 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
else
  # video stream copied untouched, audio replaced
  nice -n 19 ffmpeg -y -v error -i "$VIDEO" -i "$AUDIO" \
    -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
fi
echo "wrote $OUT"
