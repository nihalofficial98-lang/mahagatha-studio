# Mahagatha Studio — how an episode is made (one way, nothing else)

Style: bright, clear, layered paper-cut look (the EP6 look). **All art is drawn by code** — no AI-generated images anywhere.

## Steps
1. **Script** — Claude writes the verified script and the emotion-tagged voiceover script (`deliverables/EPNN_…`).
2. **Voice + timeline** — the owner records the voiceover and sends the **mp3 and the word-timestamp JSON**. Nothing starts before both are in.
3. **Align** — `python3 studio/import_timestamps.py NN voiceovers/epNN_voice.mp3 <timeline.json>`, then `python3 studio/hide_unspoken.py NN <timeline.json>`
   (script lines the narrator skipped are hidden, sentences he added are shown, so subtitles = exactly what is spoken).
4. **Characters first (Opus)** — build/adjust the cast specs the episode needs (`engine/v2_cast.js` `CAST`, `engine/paper_kit.js`). Owner approves the character sheet.
5. **Frames (Opus)** — one frame per shot: `python3 studio/ep_frames.py NN --out library/showcase/epNN_frames`. Story beats must read visually: background, characters, expression and effects change with the narration. Owner approves the frames.
6. **Video (Sonnet)** — only after the owner's go-ahead. Check subtitles on a few frames first. Render in resumable chunks (see below).
7. **Deliver** — `renders/epNN_1080p.mp4` + `.srt`.

## Render rules (so nothing is lost)
- 1080p, 30 fps, 4 workers. ~6 h for 8 min on this container; run as a normal background task (`timeout 7200000`) and relaunch when it stops. Detached processes die when the container idles.
- Render in 600-frame chunks, each saved when finished (`build/epNN/ch2/chNN.mp4`), then concat + mux the voice. Never re-render finished chunks.
- Do not poll; one status line when asked.

## Rules
- No Gemini/AI images. Effects, backgrounds, characters are code.
- Subtitle text = what the audio says (from the JSON), not just the script.
- Never start a long job without every input (script, mp3, timeline JSON, approved frames).

## Known TODO before the next episode
- EP6 shots still reference 102 `fximg` effects (library/fx images were Gemini and are now deleted): replace with code-drawn paper-cut effects in `engine/paper_scenes.js` and drop the painted-image code from `engine/v2_scenes.js`.
- Engine pass with Opus: walking, eyes/brows/expressions and scene-changing backgrounds as one reusable system.
