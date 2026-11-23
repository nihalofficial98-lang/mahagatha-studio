# Render (Sonnet) — exact steps, only after `episodes/epNN/APPROVED` exists

1. Inputs check (prints the plan, changes nothing):
   `python3 studio/render_chunks.py NN --check`
   Expected: `EPNN: <seconds>s, <frames> frames, <chunks> chunks, <done> already done, <todo> to render`. Any `STOP:` line → report it to the producer, do nothing else.
2. Subtitles spot-check (3 frames, ~1 min): `python3 studio/ep_frames.py NN --out build/epNN/subcheck --only 0,<middle>,<last>`; open the 3 jpgs: the subtitle words must be the words spoken at that moment.
3. Render (run as ONE normal background Bash task, timeout 7200000 ms; ~45 min per minute of video on 4 cores):
   `python3 studio/render_chunks.py NN`
   It saves each 600-frame chunk in `build/epNN/chunks/` when finished. If the task stops (timeout, container idle), run the SAME command again: finished chunks are never re-rendered. Do not poll; when it ends, read the last 5 lines of its output.
4. Subtitles file: `python3 studio/make_srt_ts.py deliverables/EPNN_<Title>_Voiceover_Script_Without_Tags.txt <words.json> renders/epNN.srt`
5. Final check: `python3 studio/studio.py qa NN --video renders/epNN_1080p.mp4` → must print `QA PASS`. Report: file paths, duration, QA line.
