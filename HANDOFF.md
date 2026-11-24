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
