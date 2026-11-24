# beats.json: the language-neutral episode structure

`episodes/epNN/beats.json` is written by **script-editor** before any words, reviewed by **script-doctor**, and shared by every language (`script.en.md` primary from EP07, `script.hi.md` optional / EP01-06). Shots, reels and timings hang off its ids, never off words. `python3 studio/studio.py new NN "title"` writes a skeleton; `python3 studio/studio.py check NN [--lang hi]` validates (default = the primary language in `episode.json`) it against the script.

Worked example (EP06 as recorded, analysis only): `library/examples/ep06_beats_example.json`
-> `python3 studio/script_check.py 06 --beats library/examples/ep06_beats_example.json` shows exactly why EP06 sagged.

## Top level
| key | type | meaning |
|---|---|---|
| `episode` | "07" | episode number |
| `title` | {en, hi} | titles per language (`en` primary from EP07) |
| `languages` | ["en"] (default from EP07), ["en","hi"] or ["hi"] (EP01-06) | languages that have a script; the first is the primary language |
| `planted_question` | {text, planted_in, answered_in} | the one question of the whole episode; beat ids; planted in T/C1, answered in C3 |
| `names` | {id: {en, hi, line:{en,hi}}} | every character/object id with its spelling per language and a one-line re-introduction |
| `cues` | {cue_id: {meaning, anchor:{en,hi}}} | semantic shot anchors (see below) |
| `chapters` | [{id, kind, reel, title}] | in order: `T` (kind `teaser`), `C1` `C2` `C3` (kind `chapter`, reel `A` `B` `C`), optional `X` (kind `close`, reel `C`) |
| `beats` | [beat] | in script order |

## Beat
| key | example | rule |
|---|---|---|
| `id` | "B07" | same id in every language script (`**B07** [cue]`) |
| `chapter` | "C2" | one of `chapters`; chapters are continuous blocks |
| `reel` | "B" / null | reel the beat belongs to; teaser beats are `null` (full video only) |
| `intent` | "the race starts" | one line: what this beat does for the story |
| `roles` | ["hook"] | from: `hook stakes plant setup rehook turn climax payoff answer recap bridge question` (`tease` is not allowed: episodes are standalone) |
| `budget_sec` | 30 | planned length; the checker warns if the script is off by > 35% (or 6 s) |
| `emotion` | {"en":"fast","hi":"तेज़"} | the reading cue per language; the script's `[cue]` must exist |
| `cue_ids` | ["flower_falls"] | semantic anchors in this beat (unique in the episode) |
| `characters` | ["brahma","ketaki"] | who is on screen / named in this beat |
| `names_introduced` | ["ketaki"] | names introduced (or re-introduced) here in one line; the language's spelling must appear in the beat text |
| `vertical` (optional) | {"focus":"brahma","note":"keep flower centre"} | 9:16 reel framing hint (see Reels) |

Checker rules tied to roles: first beat of the video = `hook`; first `stakes` <= 60 s; gaps between `hook/stakes/plant/rehook/turn/climax` <= 90 s; every chapter starts with `hook`, has `setup`, `turn` (or `climax`), `payoff`, ends with `bridge`; exactly one `climax` (in C3); a `payoff` within 30 s after it; time after the climax <= 15%; `recap` <= 40 words; `question` only in C3 or X; role `tease` is an error (no next-episode pointer). Numbers: `library/script_rules.json`.

## Cue ids (shot anchors)
Old briefs anchor a shot to one spoken word (`"start": {"t": 0.14, "word": "ब्रह्मा"}`). That breaks when a second language is added (different words, different times). New rule:
```json
"cues": {"flower_falls": {"meaning": "a Ketaki flower drifts down past the swan",
                          "anchor": {"en": "a single white flower", "hi": "एक केतकी का फूल"}}}
```
A shot brief refers to `{"beat": "B07", "cue": "flower_falls"}`. For each language the anchor phrase is looked up inside that beat of that language's timings. Until the brief tools read cue ids, the brief writer copies the anchor word from `python3 studio/script_check.py NN --anchors en` into `start.word` (same as today). Use snake_case ids that describe the picture, not the words.

## Minimal example
```json
{"episode": "07", "title": {"en": "...", "hi": "..."}, "languages": ["en"],
 "planted_question": {"text": "Why did the generous asura lose?", "planted_in": "B01", "answered_in": "B21"},
 "names": {"bali": {"en": "Bali", "hi": "बलि", "line": {"en": "Bali, king of the asuras", "hi": "बलि, असुरों का राजा"}}},
 "cues": {"three_steps": {"meaning": "the dwarf grows to the sky", "anchor": {"en": "three steps", "hi": "तीन क़दम"}}},
 "chapters": [{"id": "T", "kind": "teaser"}, {"id": "C1", "kind": "chapter", "reel": "A"},
              {"id": "C2", "kind": "chapter", "reel": "B"}, {"id": "C3", "kind": "chapter", "reel": "C"}],
 "beats": [{"id": "B01", "chapter": "T", "reel": null, "intent": "cold open + planted question", "roles": ["hook", "plant"],
            "budget_sec": 15, "emotion": {"en": "fast, mysterious", "hi": "तेज़, रहस्यमयी"}, "cue_ids": [],
            "characters": ["bali"], "names_introduced": ["bali"]}]}
```

## Reels (9:16): built (vertical mode, Nov 2026)
The engine renders 16:9 episodes unchanged; reels use `format: "vertical"` (720x1280 at scale 1.0, 1080x1920 at 1.5, 24 fps).
**How it works**: scenes, characters and effects are still drawn in the 1280x720 16:9 frame (after the shot camera). The reel shows that
frame through a portrait **camera window** (full height x 405 wide at zoom 1) that follows the focus character (also while it walks),
or, for a dialogue, a native **stack** layout: two crops, speaker on top and listener below, split by a torn-paper seam.
Every existing scene, character and effect works; screen-space fx (`text`, `name`) must be placed near the focus x or they fall outside.

**Project**: `reels/reelNN/` = `reel.json` + `briefs.json` (+ shot_plan.json, shots.json, APPROVED); build files in `reels/build/reelNN/`.
`reel.json`: `{reel, title, full_title, audio, words, cast, format:"vertical", fps:24, title_sec:2.5, duration}`
- `title` = first-frame text, 2-4 words ("Madhu and Kaitabha"): drawn big from frame 0 for `title_sec` in the upper safe area, then fades.
- `full_title` = upload title; `audio` = reels/inputs/reelNN.mp3 (voice only); `words` = reels/build/reelNN/words.json (spoken words, exact).
- `cast` = rig names (python3 studio/engine_vocab.py; reels/cast.json lists the reel characters). `duration` is written by reel_setup.py.

**Shot brief `vertical` block** (per shot, optional): `{focus:"brahma", z:1.2, y:.45}` window on a character (z = extra zoom 1..1.8,
y = where the face sits in the window, used when z > 1); `{x:[400,880]}` pan across the frame; `{mode:"stack", stack:["shiva","brahma"]}`.
Default = window on `focus.subject` (the largest figure if none). The beat-level `vertical.focus` hint is copied into the shot brief by hand.
- Big characters: prefer s 0.85-1.1 full figures with z 1.1-1.3, or `head:true` busts; two characters further apart than ~400 need `stack`.
- First shot: keep the focus face at >= 42% of the height (y .45+) so the title card (14-35%) does not cover it; no stack in the first shot.

**Safe areas** (engine draws them): title card 14-35% of the height; subtitles centred at 70% (64-76%; stack shots: on the seam at 50%),
left-of-centre so the right ~15% stays clear; nothing important in the bottom 20% or top 14%. Subtitles = the reel word timings grouped like
reel_prepare.py / subs.srt (max 6 words, 36 chars, 2 lines), current word in gold, Latin serif (bold), dark box + outline.
`validate_brief.py` checks that the focus face is inside the window and above 64%.

**Cut list for reels cut from an episode** (not built yet): beats with `reel` = A/B/C in order (teaser excluded, reel C includes X);
audio = the voice slice of those beats (build/epNN/timings.json); end card 2-3 s after the bridge line. Today's reels are recorded
separately (reels/inputs) and run through the steps in guides/RENDER.md (Reels).
