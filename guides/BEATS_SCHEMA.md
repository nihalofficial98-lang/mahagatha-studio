# beats.json: the language-neutral episode structure

`episodes/epNN/beats.json` is written by **script-editor** before any words, reviewed by **script-doctor**, and shared by every language (`script.hi.md`, `script.en.md`). Shots, reels and timings hang off its ids, never off words. `python3 studio/studio.py new NN "title"` writes a skeleton; `python3 studio/studio.py check NN [--lang en]` validates it against the script.

Worked example (EP06 as recorded, analysis only): `library/examples/ep06_beats_example.json`
-> `python3 studio/script_check.py 06 --beats library/examples/ep06_beats_example.json` shows exactly why EP06 sagged.

## Top level
| key | type | meaning |
|---|---|---|
| `episode` | "07" | episode number |
| `title` | {hi, en} | titles per language |
| `languages` | ["hi"] or ["hi","en"] | languages that have a script |
| `planted_question` | {text, planted_in, answered_in} | the one question of the whole episode; beat ids; planted in T/C1, answered in C3 |
| `names` | {id: {hi, en, line:{hi,en}}} | every character/object id with its spelling per language and a one-line re-introduction |
| `cues` | {cue_id: {meaning, anchor:{hi,en}}} | semantic shot anchors (see below) |
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
| `emotion` | {"hi":"तेज़","en":"fast"} | the reading cue per language; the script's `[cue]` must exist |
| `cue_ids` | ["flower_falls"] | semantic anchors in this beat (unique in the episode) |
| `characters` | ["brahma","ketaki"] | who is on screen / named in this beat |
| `names_introduced` | ["ketaki"] | names introduced (or re-introduced) here in one line; the language's spelling must appear in the beat text |
| `vertical` (optional) | {"focus":"brahma","note":"keep flower centre"} | 9:16 reel framing hint (see Reels) |

Checker rules tied to roles: first beat of the video = `hook`; first `stakes` <= 60 s; gaps between `hook/stakes/plant/rehook/turn/climax` <= 90 s; every chapter starts with `hook`, has `setup`, `turn` (or `climax`), `payoff`, ends with `bridge`; exactly one `climax` (in C3); a `payoff` within 30 s after it; time after the climax <= 15%; `recap` <= 40 words; `question` only in C3 or X; role `tease` is an error (no next-episode pointer). Numbers: `library/script_rules.json`.

## Cue ids (shot anchors)
Old briefs anchor a shot to a Hindi word (`"start": {"t": 0.14, "word": "ब्रह्मा"}`). That breaks for English (different words, different times). New rule:
```json
"cues": {"flower_falls": {"meaning": "a Ketaki flower drifts down past the swan",
                          "anchor": {"hi": "एक केतकी का फूल", "en": "a single white flower"}}}
```
A shot brief refers to `{"beat": "B07", "cue": "flower_falls"}`. For each language the anchor phrase is looked up inside that beat of that language's timings. Until the brief tools read cue ids, the brief writer copies the anchor word from `python3 studio/script_check.py NN --anchors hi` into `start.word` (same as today). Use snake_case ids that describe the picture, not the words.

## Minimal example
```json
{"episode": "07", "title": {"hi": "...", "en": "..."}, "languages": ["hi"],
 "planted_question": {"text": "Why did the generous asura lose?", "planted_in": "B01", "answered_in": "B21"},
 "names": {"bali": {"hi": "बलि", "en": "Bali", "line": {"hi": "बलि, असुरों का राजा", "en": "Bali, king of the asuras"}}},
 "cues": {"three_steps": {"meaning": "the dwarf grows to the sky", "anchor": {"hi": "तीन क़दम", "en": "three steps"}}},
 "chapters": [{"id": "T", "kind": "teaser"}, {"id": "C1", "kind": "chapter", "reel": "A"},
              {"id": "C2", "kind": "chapter", "reel": "B"}, {"id": "C3", "kind": "chapter", "reel": "C"}],
 "beats": [{"id": "B01", "chapter": "T", "reel": null, "intent": "cold open + planted question", "roles": ["hook", "plant"],
            "budget_sec": 15, "emotion": {"hi": "तेज़, रहस्यमयी", "en": "fast, mysterious"}, "cue_ids": [],
            "characters": ["bali"], "names_introduced": ["bali"]}]}
```

## Reels (9:16): requirement only, NOT built yet
The engine renders 16:9 (1280x720 plan -> 1080p). Reels A/B/C are cut from the same beats later. What the vertical renderer will need (record it now, build it later):
- **Cut list** = beats with `reel` = A/B/C, in order; teaser excluded; reel C includes X.
- **Framing**: 1080x1920 output = a 9:16 window that moves over the 16:9 plan, or a re-layout. Each shot's main subject must be inside the window; `vertical.focus` names the subject to follow (default: `focus.subject` of the shot brief).
- **Safe areas**: subtitles inside the middle band (top ~ 62-78% of height, clear of platform UI at the bottom ~ 20% and right ~ 15%); on-screen names above the subtitles; nothing important in the top 10%.
- **Audio**: the reel uses the same voice slice (beat start/end from `build/epNN/timings.json`), music re-faded at the cut.
- **End card**: 2-3 s "full story on the channel" card after the bridge line (art, no AI images).
