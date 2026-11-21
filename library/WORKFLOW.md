# New workflow: the voice leads, the video follows (agreed with the owner)

1. **Script** — Claude writes the episode script (episodes/epNN/script.md). The owner reads it and verifies/edits it. Length rule: video 8–10 min (aim 8.5–9.5).
2. **Voiceover script** — Claude gives the tagged script (emotion tags per line, no beat numbers) as .txt files: `deliverables/EPNN_…_Script_With_Emotion_Tags.txt` (+ plain).
3. **Owner generates the voiceover** from that script (one audio file for the whole episode) and sends it. The voice may be a little faster than the guide voice: that is fine.
4. **Exact word times** — no speech model can be downloaded on the build server, so the owner exports word timestamps from a recognizer (ElevenLabs *Speech to Text* → upload the voiceover, language Hindi → export JSON with word timestamps, or SRT; Whisper JSON / CapCut or YouTube SRT also work). Measured: with a messy transcript the importer recovers word times to a median of 0.003 s. The model-free estimate (no timestamps file) can drift by seconds and must not be used for final subtitles.
5. **Claude aligns and builds** — `python3 studio/studio.py align NN <voice file> --timestamps <file>` (cuts per-beat clips and times every line/word to the real recognizer output), then `studio.py shots NN` → `qa NN` → `stills NN` (numbered frame sheets for approval) → `render NN` (the owner's voice is INCLUDED; do not use --silent).
6. **Visuals are matched to the voice, never the voice to the video.** No time-stretching of the voice (`target_sec` is set to the voice length, tempo 1.0). Shots are re-timed to the actual line/word times; if a shot is too short at the faster pace, shorten/merge shots, do not slow the voice.
7. Review order stays: numbered frame sheets → 1080p review video → 4K only after approval. Files sent in chat must be ≤ 400 MB (compress copies; keep the full file on the server).

Recording tips that make the alignment accurate: leave a clear pause (≥0.5 s) between sentences/lines and ~1 s between beats; keep the spoken words the same as the script.
Measured on test voices: pause-based estimate was only reliable when pauses were uniform (it failed on the owner's real recording); matching to a reference voice was good on synthetic voices (median ≈0.05-0.1 s) but squeezed the last lines of the owner's real clip. Recognizer timestamps are the reliable path.

## Pace of the owner's ElevenLabs voice
Measured on EP1: 0.43 s per script word (489 s for 1,138 words). Target 8.5–9.5 min = 1,190–1,325 words. Check with `PACE=0.43 python3 studio/studio.py check NN`.
Do NOT put section headings (`भाग 1 …`) or metadata lines in the voiceover text: they get read aloud. The tagged voiceover file for generation contains narration lines only.
The scene-director agent (`.claude/agents/scene-director.md`) writes the shot brief from the verified script while the owner generates the voice; shots are then built against the voice timestamps.

## Every video must stand alone and open on a hook (owner rule)
- No recap lines ("last time…"). Open directly on a hook: 3–4 punchy lines that promise the strangest/most shocking parts of THIS story, then one short context beat that introduces the characters for a first-time viewer.
- The series continuity lives only in the end teaser.
- With every script, also give 8–10 YouTube hook-title options (Hindi + Hinglish/English), grouped by angle (shock, mystery, question), plus a thumbnail text idea.

## Script style (owner's reference: two explainer-style videos, from EP4 on)
- Cold-open hook that leaves a question open (what happened / who said what / what it cost), in 2–3 plain sentences. No recap, no greeting, no channel or source mentions, no verse/chapter citations.
- Then give the stakes and just enough context in simple words so the video stands alone.
- Spoken, conversational Hindi: short sentences mixed with longer ones; turns like "पर…", "और यहाँ एक दिलचस्प बात है…", "अब सोचिए…", "याद रखिए…"; pose the obvious question and then answer it.
- Concrete, memorable details (numbers, names, what exactly happened) and callbacks to things the viewer already knows (why Brahma has four faces, Kashi, etc.).
- Build in steps; each step answers the previous one and opens the next.
- End with the payoff, then one question to the audience, then the teaser.
Old literary-style EP4 draft kept as episodes/ep04/script_v1_literary.md.
