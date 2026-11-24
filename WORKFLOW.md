# Mahagatha Studio — how an episode is made (the only way)

Output: a 2D paper-cut Puranic video narrated in English from EP07 (EP01-06 are Hindi) (bright EP6 look), 1280x720 plan rendered to 1080p, subtitles = exactly what the owner says.
**All art is code** (no AI images). Opus designs; Sonnet runs mechanical steps from written instructions. Agents live in `.claude/agents/`.
To start: paste the prompt in `guides/PROMPT_TEMPLATE.md`.

| # | Step | Who (model) | Command / output | Gate |
|---|------|-------------|------------------|------|
| 1 | Structure + script, reviewed, then tagged scripts + hook titles | script-editor (sonnet) -> script-doctor (sonnet) -> script-editor | `episodes/epNN/beats.json` + `script.en.md` (`script.md` links to it; EP01-06: `script.hi.md`) -> `episodes/epNN/script_review.md` -> `deliverables/EPNN_*` ; `python3 studio/studio.py check NN` | check RESULT: PASS, review READY, **owner approves the script** |
| 1b | Hindi (optional second language, only if the owner asks) | script-editor -> script-doctor | `script.hi.md` on the same beats.json; `studio.py check NN --lang hi` (guides/LANGUAGES.md) | same gates |
| 2 | **Owner records** the voice and sends the **mp3 + word-timestamp JSON** | owner | — | nothing below starts without BOTH files |
| 3 | Align voice + subtitles | producer (sonnet) | `python3 studio/studio.py align NN <voice.mp3> --timestamps <words.json>` → `python3 studio/hide_unspoken.py NN <words.json>` → `python3 studio/make_timeline.py NN` | `build/epNN/timings.json`, `episodes/epNN/voice_timeline.md` exist |
| 4 | Characters first | character-designer (opus) | `episodes/epNN/cast.json`, `python3 studio/cast_sheet.py <names>` → `library/characters/sheets/` | **owner approves the sheets** |
| 5 | Shot briefs | cinematographer → scene-designer → action-director → effects-designer (opus) | `episodes/epNN/briefs.json` (schema `guides/SHOT_BRIEF.md`); `python3 studio/validate_brief.py NN` | 0 errors |
| 6 | Frames (one per shot) | producer (sonnet) runs, qa-reviewer (sonnet) checks, Opus agents fix | `python3 studio/brief_to_plan.py NN` → `python3 studio/build_shots.py NN` → `python3 studio/ep_frames.py NN` → `library/showcase/epNN_frames/`; `episodes/epNN/qa_report.json` | qa pass, then **owner approves the frames** → producer writes `episodes/epNN/APPROVED` |
| 7 | Video | Sonnet, following `episodes/epNN/NEXT.md` (from `guides/RENDER.md`) | `python3 studio/render_chunks.py NN` → `renders/epNN_1080p.mp4`; subtitles `renders/epNN.srt` | only with APPROVED |
| 8 | Deliver | producer | mp4 + srt + hook titles | — |

## How to tell where we are
no beats.json/script or no READY review → 1 · no `build/epNN/timings.json` → 2/3 · no cast.json or sheets not approved → 4 · briefs.json invalid → 5 · no qa pass or no APPROVED → 6 · APPROVED but no `renders/epNN_1080p.mp4` → 7.

## Rules
- Script shape (guides/SCRIPT_STYLE.md): 15 s teaser + 3 stand-alone chapters of 2.5-3.2 min (= reels A/B/C) ; length from the measured voice pace (`library/voice_profile.json`, re-measure with `python3 studio/script_check.py NN --calibrate` after aligning). Episodes are standalone: no next-episode tease; reels end resolved.
- Never start a long job (render) without every input: shots.json, timings.json, the voice pieces, APPROVED. `render_chunks.py` refuses otherwise.
- Subtitle text = the words in the owner's audio (import_timestamps + hide_unspoken), never just the script.
- Every frame: story matches the subtitle, faces above the subtitles, ≥ 2 depth planes, nothing flat or empty (qa-reviewer checklist).
- Only use names printed by `python3 studio/engine_vocab.py`; anything missing is built by Opus first (engine work).
- No polling of long jobs; one status line when asked. Render runs as a normal background task and resumes from finished chunks.
