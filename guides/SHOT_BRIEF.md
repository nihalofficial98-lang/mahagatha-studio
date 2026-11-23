# Shot brief (one JSON object per shot) — the contract between the Opus designers and Sonnet

File: `episodes/epNN/briefs.json` = `{"episode":"NN","shots":[ ... ]}`. Full worked example: `guides/shot_brief_example.json`.
Check: `python3 studio/validate_brief.py NN` (rejects vague or incomplete briefs). Convert: `python3 studio/brief_to_plan.py NN` → `shot_plan.json`.
Names (backgrounds, objects, cast, poses, emo, effects) must come from `python3 studio/engine_vocab.py`.

| field | owner | content |
|---|---|---|
| `id` | cinematographer | `bBB_N` (beat, shot number) |
| `beat` | cinematographer | beat number |
| `start` | cinematographer | `{"t": seconds, "word": "spoken word"}` from `episodes/epNN/voice_timeline.md` (must be the shot's first word) |
| `duration` | cinematographer | seconds, 1.0–6.5 (until the next shot's start) |
| `narration` | cinematographer | exact spoken words of this shot |
| `meaning` | cinematographer | what the narration means in the story (a sentence) |
| `why` | cinematographer | why this picture shows that meaning (a sentence, no vague words) |
| `camera` | cinematographer | `{shot, lens, move, from:{z,x,y,r}, to:{z,x,y,r}, shake, motivation}`; shot ∈ wide medium close extreme_close insert two_shot ots pov low_angle high_angle top establishing; lens ∈ wide normal tele; move ∈ push_in pull_out pan_left pan_right tilt_up tilt_down dolly_left dolly_right crane_up crane_down static handheld dutch orbit |
| `focus` | cinematographer | `{subject, depth: shallow|deep}` |
| `transition_in` | cinematographer | cut fade wipe iris flash |
| `layers` | scene designer | ≥ 2 of `{d: far|mid|near, contents: "words", fog, haze, blur, dark, items:[{o, x, y, s, ...}]}`; far needs fog ≥ 0.3; `from_background:true` when the background itself draws that plane |
| `background` | scene designer | `{k, ...params, change:{word, bg2:{k,...} | to:{param:value}, d}}` |
| `mood` | scene designer | `{emotion, grade, palette?}` |
| `characters` | action director | `[{who, x, y, s, flip, pose, emo, mood?, head?, look: who|x, talk?, actions:[{word, pose?, emo?, mood?, tilt?, look?, turn?, d, e?}], walk?:{word, to_x, d, speed}, turn_on?: word}]` |
| `effects` | effects designer | `[{k (pfx name or engine fx), word?, x, y, w, alpha, par, behind?, ..., meaning}]` |

Rules the validator enforces: every listed word is in the narration and (when the voice exists) spoken at `start.t`; every character has an emotion and acts, looks or talks;
faces stay above y 590 through the whole camera move; no two consecutive shots with the same camera move; no third identical frame in a row; no empty frame.
