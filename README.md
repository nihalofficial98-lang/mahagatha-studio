# Mahagatha Studio

2D paper-cut animated Puranic videos (English narration from EP07; EP01-06 Hindi), drawn entirely by code (headless Chromium canvas → ffmpeg).

- **How to make an episode:** [WORKFLOW.md](WORKFLOW.md) (the only supported way) · start prompt: [guides/PROMPT_TEMPLATE.md](guides/PROMPT_TEMPLATE.md)
- **What the engine can draw:** [library/ENGINE_CAPABILITIES.md](library/ENGINE_CAPABILITIES.md) (names: `python3 studio/engine_vocab.py`)
- **Shot brief schema:** [guides/SHOT_BRIEF.md](guides/SHOT_BRIEF.md) · script rules: [guides/SCRIPT_STYLE.md](guides/SCRIPT_STYLE.md) · render steps for Sonnet: [guides/RENDER.md](guides/RENDER.md)

## Setup (once)
```bash
pip install pillow numpy && npm install -g playwright && npx playwright install chromium   # + ffmpeg
```

## Layout
```
.claude/agents/  producer, script-editor (sonnet) · character-designer, cinematographer, scene-designer, action-director, effects-designer (opus) · qa-reviewer (sonnet)
engine/          the film engine (see ENGINE_CAPABILITIES.md "Files"); studio/build.py joins it into one HTML page
studio/          pipeline scripts: studio.py (new/check/align/qa), import_timestamps, hide_unspoken, make_timeline, cast_sheet,
                 validate_brief, brief_to_plan, build_shots, ep_frames, render_chunks, make_srt_ts, engine_vocab
episodes/epNN/   script.md, episode.json, cast.json, briefs.json, shot_plan.json, shots.json, qa_report.json, STATUS.md, NEXT.md, APPROVED
build/epNN/      voice pieces, timings, render chunks (not edited by hand)
library/         ENGINE_CAPABILITIES.md, CHARACTERS.md, character sheets, plans (EPISODE_PLAN, SERIES_PLAN), feedback
source/          the book, one file per story · deliverables/ scripts for the owner · renders/ finished videos
```
