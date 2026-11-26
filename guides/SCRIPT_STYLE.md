# Script style (retention-first; English is the primary language from EP07, Hindi optional)

The book gives only plot facts; every word is original. One episode = **one full video (8-10 min) that is also three stand-alone reels (2.5-3.2 min each)**. Structure lives in `episodes/epNN/beats.json` (schema: `guides/BEATS_SCHEMA.md`), words live in `script.en.md` (primary from EP07) / `script.hi.md` (`guides/LANGUAGES.md`). `python3 studio/studio.py check NN` prints the scorecard; `script-doctor` reviews it.

## Length (hard rule)
- Video **8-10 min** (aim 8.5-9.5). Minutes come from the pace in `library/voice_profile.json` (seconds per script word, per language), not a guess. **English (primary from EP07): 0.40 s/word, an ESTIMATE until the first English recording is measured, so about 1,200-1,500 words** (aim 1,275-1,425). Hindi (EP01-06, optional second language): 0.367 s/word measured on EP06 = ~1,310-1,630 words. The checker prints minutes for the language it checks.
- After every recording: `python3 studio/script_check.py NN --calibrate` (add `--lang hi` for Hindi) updates the pace; the first English recording turns the estimate into a measurement.

> Two formats: `story` (dramatised retelling, e.g. EP6) and `explainer` (question-driven, source-cited, see `guides/LONG_STYLE.md`). Set `format` in episode.json. Reels follow `guides/REEL_STYLE.md`.

## Shape: teaser + 3 chapters (+ optional close)
| Part | Length | Must contain |
|---|---|---|
| **T** teaser | 10-20 s (aim 15) | the strongest image + the **planted question**. Never the answer. Not in any reel. |
| **C1** reel A | 150-192 s | hook in the first 10 s, names in one line each, **stakes by 0:60 of the video**, setup, turn, mini-payoff, bridge line |
| **C2** reel B | 150-192 s | its own hook + one-line re-introductions, escalation, turn, payoff, bridge line |
| **C3** reel C | 150-192 s | hook + re-introductions, turn, **climax**, payoff (= answer to the planted question) **within 30 s of the climax**, recap <= 40 words, bridge = short resolved closing line + comment question; **no next-episode tease** (the episode is standalone) |
| **X** close (optional) | <= 25 s | sign-off only; belongs to reel C |

Each chapter is a **full mini-story**: someone wants something, something stands in the way, it turns, it pays off, and a bridge line closes it (the reel ends RESOLVED; at most a light forward pull, never an open cliffhanger). A stranger who sees only reel B must understand it.
- **Re-introduce names in every chapter in one line** ("Brahma, who made this world, ..."). Never "as we saw earlier" / "in the last part" (Hindi: "जैसा हमने देखा"): restate the fact in one line instead.
- **One planted question** for the whole episode: asked in T/C1, answered in C3 (`planted_question` in beats.json). Each chapter may also have its own small question, answered inside the chapter.
- The **bridge** of C1/C2 is a resolved closing line (the verdict, the result, the image that sums the chapter up), not a question to the audience and not a cliffhanger; a light forward pull is allowed. The comment question appears **only** in the last chapter's bridge (or X). **Never point to the next episode or story anywhere**: every episode is standalone.

## Pace inside the episode
- **Stakes by the first minute**: what can be lost, by whom, said plainly.
- **Re-hook every 60-90 s**: a new question, a reveal, a turn, a threat. Mark them in beats.json (`hook`, `stakes`, `plant`, `rehook`, `turn`, `climax`); the checker fails any gap > 90 s.
- **Vary beat length**: mix short punch beats (English 12-35 words, ~5-14 s; Hindi 15-40) with scene beats (English 50-85 words, ~20-34 s; Hindi 60-100). At least 3 of each; never more than 3 beats of the same band in a row; no beat over 95 words (Hindi 110).
- **Start late, leave early**: open chapters inside the action, not with "Let us start from the beginning". Descriptions (worlds, cosmos) get one short beat, not two long ones.
- **Ending**: payoff within 30 s of the climax; everything after the climax <= 15% of the video; recap <= 40 words; no list of earlier episodes.
- **Hook never gives away the answer.** Promise it ("What was decided that day has never changed"), don't state it.

## Triple hook (teaser and every chapter's first 10 s)
Each hook is 1-3 lines and has three parts, in this order:
1. **Context** - the very first line says what this is about (audio, on-screen text/subtitle and the first visual all agree). Context delayed to the second half of the first sentence loses viewers.
2. **Lean** - make them want more: a proof/stat, a pain point or wish they have, or something surprising. Opens the curiosity loop.
3. **Contrarian snapback** - one line that pulls the other way from where the lean was heading (the expected answer is wrong, the hero is the culprit, the safe thing was the danger). Do not give away the answer.
Test: read only the first 1-2 sentences aloud - is the context clear at once, and does it make you lean in?
Example (EP6, shown in English): context "Brahma made the whole universe, so why does he have not a single temple?" -> lean "The reason is not a curse. It was one small flower." -> snapback "And the flower did not lie. It was made to lie." (check against the source story before using). Hindi original lines: "ब्रह्मा ने पूरा ब्रह्मांड रचा, फिर भी उनका एक भी मंदिर क्यों नहीं?" / "वजह कोई श्राप नहीं, एक छोटा-सा फूल था।" / "और उस फूल ने झूठ बोला नहीं था, उससे बुलवाया गया था।"

## Lines (unchanged)
- Short lines, one new idea or image per sentence: every sentence is a possible cut (3-4 s).
- Dialogue in quotes; each speaker has a distinct rhythm. Names appear on screen when spoken.
- One emotion cue per beat: `**B07** [calm, firm]`. Keep the cues mild and readable, never shouting. English cues (never slow/whispering/hush/soft: see guides/VOICE_TAGS.md): mysterious, grand, grave, calm, firm, serious, curious, surprised, angry, sad, cold, excited, urgent, tense, dramatic, fast (Hindi equivalents for the Hindi version: धीमे, रहस्यमयी, भव्य, गंभीर, शांत, दृढ़, करुण, तेज़, क्रोध, विस्फोट, फुसफुसाकर, गिड़गिड़ाते हुए, ठंडा, स्नेह).
- English script: plain spoken English; short sentences, one action each (`guides/REEL_STYLE.md`); numbers written as words ("nine hundred and ninety-nine", so the speech recognizer and the subtitles match); no standalone dashes; no Devanagari; one spelling per name (`names.*.en`); at most one Sanskrit term per chapter, explained in the same line. Hindi script (optional second language): no English words. Details: `guides/LANGUAGES.md`.
- No AI images anywhere: all art is code.

## Shot cues
Shots anchor to **beat id + cue id** (`flower_falls`), not to a spoken word, so the same briefs serve both languages. Every visual moment that needs an exact cut gets a cue id in beats.json with an anchor phrase per language that occurs in that beat's text (`studio.py check` verifies it; `script_check.py NN --anchors en` prints the mapping for brief writers).

## Reels (9:16) - requirement, not built yet
Each chapter is cut as a vertical reel later. Write with that in mind: the hook line works without the teaser, the main subject of each beat can sit in the centre third, and on-screen names/subtitles must fit the vertical safe area. Details in `guides/BEATS_SCHEMA.md`.

## Retention checklist (script-doctor and script-editor both run it)
1. Teaser <= 20 s, ends on the planted question, does NOT give the answer.
2. Stakes stated plainly before 0:60.
3. Each chapter: triple hook (context, lean, snapback) / hook line in the first 10 s, names re-introduced in one line, setup, turn, payoff, bridge line. No back-references.
4. No gap > 90 s without a hook/turn/reveal (scorecard "max re-hook gap").
5. Short and long beats alternate; no beat > 110 words.
6. The big set-piece (chase, race, battle) starts before 35% of the video.
7. Climax in C3; payoff within 30 s; post-climax <= 15%; recap <= 40 words.
8. Comment question only at the very end; no next-episode tease anywhere (standalone episode).
9. Every chapter is 2.5-3.2 min; total 8-10 min at the measured pace.
10. Read each reel alone: would a stranger understand who, what they want, and why it matters?

- **Hook = opposite notion (owner's rule):** the first 2 to 3 lines say the reverse of what people believe about the character, then the story breaks the old belief. See guides/REEL_STYLE.md.

- **Close the loop (owner, most important):** the LAST lines of every reel and episode must spin back to the hook: repeat the hook's key claim in a new light, now that the viewer knows the story (for example hook "Shiva killed Yama to save a boy" -> ending "Shiva killed Yama to save one sixteen-year-old boy. Because of this he is called Kalantaka"). The ending is never a new topic and never a vague "what do you think?". Before sending any script, check the first line against the last line and fix it if they do not connect.
