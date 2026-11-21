# New workflow: the voice leads, the video follows (agreed with the owner)

1. **Script** — Claude writes the episode script (episodes/epNN/script.md). The owner reads it and verifies/edits it. Length rule: video 8–10 min (aim 8.5–9.5).
2. **Voiceover script** — Claude gives the tagged script (emotion tags per line, no beat numbers) as .txt files: `deliverables/EPNN_…_Script_With_Emotion_Tags.txt` (+ plain).
3. **Owner generates the voiceover** from that script (one audio file for the whole episode) and sends it. The voice may be a little faster than the guide voice: that is fine.
4. **Claude aligns and builds** — `python3 studio/studio.py align NN <voice file>` (cuts per-beat clips, finds every line and word time in the owner's audio; no speech model needed), then `studio.py shots NN` → `qa NN` → `stills NN` (numbered frame sheets for approval) → `render NN` (the owner's voice is INCLUDED; do not use --silent).
5. **Visuals are matched to the voice, never the voice to the video.** No time-stretching of the voice (`target_sec` is set to the voice length, tempo 1.0). Shots are re-timed to the actual line/word times; if a shot is too short at the faster pace, shorten/merge shots, do not slow the voice.
6. Review order stays: numbered frame sheets → 1080p review video → 4K only after approval. Files sent in chat must be ≤ 400 MB (compress copies; keep the full file on the server).

Recording tips that make the alignment accurate: leave a clear pause (≥0.5 s) between sentences/lines and ~1 s between beats; keep the spoken words the same as the script.
Measured accuracy (test on a known voice, also at +12 % speed): line start/end within ≈0.03 s, words ≈0.05 s typical, ≈0.18 s worst.
