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

## Reels (9:16 vertical, `reels/reelNN/`; format comes from reel.json, `--format vertical` forces it)
0. Setup (once per reel): `python3 studio/reel_prepare.py NN` (words.json + subs.srt) → `python3 studio/reel_setup.py reelNN --title "2-4 words" --cast a,b`
   (writes reels/reelNN/reel.json and reels/build/reelNN/timings.json, beats.json, audio/00.mp3; voice tempo stays 1.0).
1. Briefs → shots: `python3 studio/validate_brief.py reelNN` → `python3 studio/brief_to_plan.py reelNN` → `python3 studio/build_shots.py reelNN`.
2. Stills for approval (1080x1920 with title card + subtitles): `python3 studio/ep_frames.py reelNN` → `library/showcase/reelNN_frames/` (+ `sheet_NN.jpg`).
3. Timing test, no APPROVED needed: `python3 studio/render_chunks.py reelNN --res 720p --seconds 5 --chunk 30` → `renders/reelNN_720x1280_first5s.mp4`.
4. After the owner approves (`reels/reelNN/APPROVED`): `python3 studio/render_chunks.py reelNN --check`, then ONE background task
   `python3 studio/render_chunks.py reelNN` (1080x1920, 24 fps) or `--res 720p` (720x1280) → `renders/reelNN_1080x1920.mp4`.
   Chunks: `reels/build/reelNN/chunks_v1080p/`; same resume rule (run the same command again). ~1.4 s per frame per worker at 720p.
5. Subtitles file for upload: `reels/build/reelNN/subs.srt` (same grouping as the burned-in subtitles).
