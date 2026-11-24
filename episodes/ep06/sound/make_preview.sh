#!/usr/bin/env bash
# Mix the voice + the five rendered stems into ep06_sound_preview.mp3 (about -16 LUFS, true peak <= -1.5 dB).
# Run AFTER render_sound.py. Low priority, 1 thread. Does not touch any video.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
VOICE="$ROOT/voiceovers/ep06_voice.mp3"
S="$HERE/stems"
for f in bed motif pulse ambience sfx; do [ -f "$S/$f.wav" ] || { echo "missing $S/$f.wav (run render_sound.py first)"; exit 1; }; done

# per-stem trims in dB (tweak here after listening)
BED="${BED:-0}"; MOTIF="${MOTIF:-0}"; PULSE="${PULSE:-0}"; AMB="${AMB:-0}"; SFX="${SFX:-0}"

nice -n 19 ffmpeg -y -v error -threads 1 \
  -i "$VOICE" -i "$S/bed.wav" -i "$S/motif.wav" -i "$S/pulse.wav" -i "$S/ambience.wav" -i "$S/sfx.wav" \
  -filter_complex "
[0:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[v];
[1:a]aresample=44100,volume=${BED}dB[a1];
[2:a]aresample=44100,volume=${MOTIF}dB[a2];
[3:a]aresample=44100,volume=${PULSE}dB[a3];
[4:a]aresample=44100,volume=${AMB}dB[a4];
[5:a]aresample=44100,volume=${SFX}dB[a5];
[a1][a2][a3][a4][a5]amix=inputs=5:normalize=0:duration=longest,alimiter=limit=0.9[m];
[v][m]amix=inputs=2:normalize=0:duration=longest,loudnorm=I=-16:TP=-1.5:LRA=11[o]" \
  -map "[o]" -ar 44100 -c:a libmp3lame -b:a 256k "$HERE/ep06_sound_preview.mp3"
echo "wrote $HERE/ep06_sound_preview.mp3"
