> **Start with [WORKFLOW.md](WORKFLOW.md)** — the only supported way to make an episode. Older notes below may be outdated.

# Mahagatha Studio

Free, automated pipeline that turns Puranic stories (book "Mahagatha") into dramatic Hindi animated videos:
**plan → script → voiceover files → direction (shot list) → frames → QA → render (1080p / 4K) → learn.**
Everything runs on free tools: Python, Node + headless Chromium (Playwright), ffmpeg, edge-tts (guide voice).

## One-time setup
```bash
pip install edge-tts pillow playwright markdown && playwright install chromium
npm install            # fonts
sudo apt install ffmpeg
```

## The daily loop (what you and I each do)
| # | Step | Command | Who |
|---|------|---------|-----|
| 1 | Plan episode from the next stories | edit `library/EPISODE_PLAN.md` | Claude |
| 2 | Scaffold | `python3 studio/studio.py new 03 "title"` | Claude |
| 3 | Write script (fresh Hindi, beats + emotion cues) | `episodes/ep03/script.md` | Claude |
| 4 | Lint script (8–10 min rule, beats, cues) | `studio.py check 03` | Claude |
| 5 | Voiceover files: tagged (AI voice) + clean (you read) | `studio.py voice-docs 03` → `voiceovers/` | Claude → you |
| 6 | Your recording | save as `voiceovers/ep03.mp3` | **You** |
| 7 | Guide voice + word timings (stand-in) | `studio.py tts 03` | auto |
| 8 | Direct: shot list from spoken-word triggers | `episodes/ep03/shots.py` → `studio.py shots 03` | Claude |
| 9 | Look at every shot | `studio.py stills 03` → `build/ep03/sheets/` | Claude |
| 10 | Automated QA gate | `studio.py qa 03` | auto |
| 11 | Render | `studio.py render 03` (`--res 4k`) | auto |
| 12 | QA on the video (freezes/black) | `studio.py qa 03 --video renders/ep03_1080p.mp4` | auto |
| 13 | Your feedback → system memory | `studio.py feedback 03 "…" --cat visual` | you/Claude |

The system improves itself through **three ratchets** (see ARCHITECTURE.md): the feedback log → backlog, the QA rules,
and the versioned asset gallery.

## Layout
```
studio/      CLI (studio.py), TTS, renderer, QA, gallery, shot toolkit
engine/      the film engine: art.js (figures, textures), scenes.js (backgrounds, FX), main.js (timeline, subtitles, camera)
episodes/    epNN/{script.md, shots.py, episode.json, feedback.md}
library/     CHARACTERS.md, BACKLOG.md, rules.json, feedback.jsonl, CHANGELOG.md, gallery/vX.Y.Z/
guides/      SCRIPT_STYLE, DIRECTION, CINEMATOGRAPHY, RUNBOOK (the craft rules)
source/      book text by story; voiceovers/ → scripts for you + your recordings
```
