# Changelog
## 5.0.0 (Nov 2026) — production system
- All art code-drawn: 24 paper props/effects in engine/paper_fx.js (same names as the removed image effects, EP6 plan unchanged); painted-image code removed.
- Depth: paper objects (tree, rock, cloud, mountain, pillar, wall, shrub, hill) with fog/haze/blur, `layers` far/mid/near, default blurred foregrounds.
- Story-driven backgrounds: `bg2` cross-fade and `bgTo` tween on a word. Transitions: wipe, iris, flash.
- Acting: emotion presets (`emo`), head turn (`mood.turn`), paper flip-turn (`turnc`), `walkTo`, anger via mood.
- Pipeline: shot brief schema + validate_brief.py + brief_to_plan.py; engine_vocab.py as the single list of names; cast_sheet.py; resumable render_chunks.py; 8 agents.
## 4.0.0 (ep02 v4)
- Cut-out figures, data-driven scenes, word-cue triggers, pipeline CLI, QA gate.
