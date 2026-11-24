# Handoff — where EP6 stands (read this first after any pause)

State at the time of writing (all committed on branch `claude/amazing-heisenberg-cs6b4t`):
- Done: repo cleaned (no Gemini images, EP1-5 removed), agents + brief validator + code-drawn effects/depth/animation engine, EP6 voice aligned with the owner's timeline JSON (`build/ep06/timings.json`, `renders/ep06_hi_exact.srt`), EP6 character sheets approved (`library/showcase/ep06_cast/`, `episodes/ep06/cast.json`).
- Done: 183 shot briefs written (`episodes/ep06/briefs.json`, all with depth layers).
- In progress: validate briefs (`python3 studio/validate_brief.py 06`), convert (`studio/brief_to_plan.py`), build shots (`studio/build_shots.py 06`), regenerate engine timings, render one frame per shot (`python3 studio/ep_frames.py 06 --out library/showcase/ep06_frames_v2`), QA (`qa_report.json`), fix weak frames.
- Next after owner approves the frames: video render at 720p / 24 fps (try for 1-2 h), chunked and resumable (`studio/render_chunks.py`, needs `episodes/ep06/APPROVED`). Time a few seconds first.
- Owner rules: no AI images; never start a long job without every input; short replies; frames are reviewed before any video; Sonnet for simple work, Opus for design/engine.
- If engine_timings.json looks stale: `PREPARE_ONLY=1 TARGET_SEC=478.4 NODE_PATH=$(npm root -g) node studio/render_ep.js build/ep06 episodes/ep06/shots.json /dev/null 4 30`.

## Palette
- Owner decision: future episodes keep the EP6 earthy look (current engine defaults). No bright palette.

## Script builder v2 (for EP07 onward; EP06 untouched)
- New flow: script-editor drafts `beats.json` + `script.hi.md` -> script-doctor (`episodes/epNN/script_review.md`) -> fix -> owner approves -> owner records. English optional after Hindi approval (`guides/LANGUAGES.md`).
- `studio.py check NN` now prints a retention scorecard (`studio/script_check.py`; rules `library/script_rules.json`, pace `library/voice_profile.json` = 0.367 s/word measured on EP06, so 8-10 min = ~1,310-1,630 Hindi words). Self-test: `python3 studio/script_check.py --selftest`.
- Why EP06 sagged: `python3 studio/script_check.py 06 --beats library/examples/ep06_beats_example.json` (19 errors; rewrite plan inside the file).
- Not built yet: cue-id resolver in the brief tools, English align/render, 9:16 reel renderer (requirements in `guides/BEATS_SCHEMA.md`).
