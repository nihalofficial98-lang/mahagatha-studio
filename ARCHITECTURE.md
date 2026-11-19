# Architecture

## Data flow
`script.md` → (parse cues) `beats.json` → (edge-tts) `audio/NN.mp3 + timings.json` (word timestamps)
→ tempo fit to `target_sec` → `engine_timings.json`.
`shots.py` → `shots.json` (each shot starts on a **spoken word**; inner cues also trigger on words).
Chromium loads the engine, `seek(T)` draws frame T deterministically; frames → ffmpeg → parts → concat + voice mux.
With your own recording only `timings.json` changes (Whisper alignment, roadmap #5); shots re-time automatically
because every trigger is a word, not a second.

## Engine (engine/)
- `art.js` — utilities (parallax `layer`, glow, rays, dust), painterly cloud/ridge textures, figure renderer
  (`drawFig`: cut-out body + lighting + rim light; `drawHead` close-ups; `drawBrahma`; `drawBull`), cast `CH`, `palace`, `post` (bloom, grade, grain, vignette).
- `scenes.js` — data-driven scene: `{bg, figs[], fx[]}`. Backgrounds `BG.*`, effects (`text`, `name`, `flames`, `shock`, `bolt`, `beam`, `orbs`, `ribbon`, `icon`…), special scenes `tower`, `earth`, `map`, `pillars`.
- `main.js` — timeline, word-cue resolution, dissolves, serif subtitles, camera.
- `shots.js` — hand-built shots from the first sample (beats 6, 9, 10 of ep02).
To add a character: add a spec to `CH` in art.js; add a scene to the gallery; bump `engine/VERSION`; run `studio.py gallery`.

## How the system improves over time (the three ratchets)
1. **Feedback → backlog.** Every complaint/idea is logged (`studio.py feedback`). `studio.py learn` regenerates `library/BACKLOG.md`
   (open items by category + the standing roadmap). Work the backlog top-down before each new batch of episodes.
2. **QA rules.** Each repeated complaint becomes a machine check in `library/rules.json` / `studio.py qa`
   (cue words found, video length 8–10 min, shot length 1–6.5 s and average 2.6–4.2 s, no identical consecutive shots, no frozen picture > 4 s, no black frames).
   Rules only tighten. An episode cannot be published while `qa` fails.
3. **Versioned gallery.** `studio.py gallery` renders every character, pose, expression, and background to `library/gallery/vX.Y.Z/`.
   Compare folders across versions to *see* the art improving; each engine change gets a CHANGELOG entry.

## Roadmap
See `library/BACKLOG.md` (quadruped rig, walk cycles, richer faces, more backgrounds, own-voice alignment, speed/GPU, pixel-level QA).
