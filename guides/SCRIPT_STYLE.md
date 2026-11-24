# Script style (retention-first; Hindi first, English as its own adaptation)

The book gives only plot facts; every word is original. One episode = **one full video (8-10 min) that is also three stand-alone reels (2.5-3.2 min each)**. Structure lives in `episodes/epNN/beats.json` (schema: `guides/BEATS_SCHEMA.md`), words live in `script.hi.md` / `script.en.md` (`guides/LANGUAGES.md`). `python3 studio/studio.py check NN` prints the scorecard; `script-doctor` reviews it.

## Length (hard rule)
- Video **8-10 min** (aim 8.5-9.5). Minutes come from the owner's measured pace in `library/voice_profile.json`, not a guess: Hindi **0.367 s/word** (EP06: 478 s for 1,303 words), so **~1,310-1,630 Hindi words** (aim 1,390-1,550). The old "870-1,050 words" figure was wrong (it assumed 0.575 s/word; EP06 came out at 7.97 min).
- After every recording: `python3 studio/script_check.py NN --calibrate` updates the pace.

## Shape: teaser + 3 chapters (+ optional close)
| Part | Length | Must contain |
|---|---|---|
| **T** teaser | 10-20 s (aim 15) | the strongest image + the **planted question**. Never the answer. Not in any reel. |
| **C1** reel A | 150-192 s | hook in the first 10 s, names in one line each, **stakes by 0:60 of the video**, setup, turn, mini-payoff, bridge line |
| **C2** reel B | 150-192 s | its own hook + one-line re-introductions, escalation, turn, payoff, bridge line |
| **C3** reel C | 150-192 s | hook + re-introductions, turn, **climax**, payoff (= answer to the planted question) **within 30 s of the climax**, recap <= 40 words, bridge = closing question + next-episode tease |
| **X** close (optional) | <= 25 s | sign-off only; belongs to reel C |

Each chapter is a **full mini-story**: someone wants something, something stands in the way, it turns, it pays off, and a bridge line leaves one image unresolved. A stranger who sees only reel B must understand it.
- **Re-introduce names in every chapter in one line** ("ब्रह्मा, जिन्होंने यह सृष्टि रची, ..."). Never "जैसा हमने देखा" / "as we saw earlier" / "पिछले हिस्से में": restate the fact in one line instead.
- **One planted question** for the whole episode: asked in T/C1, answered in C3 (`planted_question` in beats.json). Each chapter may also have its own small question, answered inside the chapter.
- The **bridge** of C1/C2 is a cliffhanger statement ("और तभी, उनके बीच, आसमान फट गया।"), not a question to the audience. The comment question and "next episode" tease appear **only** in the last chapter's bridge (or X).

## Pace inside the episode
- **Stakes by the first minute**: what can be lost, by whom, said plainly.
- **Re-hook every 60-90 s**: a new question, a reveal, a turn, a threat. Mark them in beats.json (`hook`, `stakes`, `plant`, `rehook`, `turn`, `climax`); the checker fails any gap > 90 s.
- **Vary beat length**: mix short punch beats (Hindi 15-40 words, ~5-15 s) with scene beats (60-100 words, ~22-37 s). At least 3 of each; never more than 3 beats of the same band in a row; no beat over 110 words.
- **Start late, leave early**: open chapters inside the action, not with "शुरू से समझते हैं". Descriptions (worlds, cosmos) get one short beat, not two long ones.
- **Ending**: payoff within 30 s of the climax; everything after the climax <= 15% of the video; recap <= 40 words; no list of earlier episodes.
- **Hook never gives away the answer.** Promise it ("उस दिन जो फ़ैसला हुआ, वह आज तक नहीं बदला"), don't state it.

## Lines (unchanged)
- Short lines, one new idea or image per sentence: every sentence is a possible cut (3-4 s).
- Dialogue in quotes; each speaker has a distinct rhythm. Names appear on screen when spoken.
- One emotion cue per beat: `**B07** [शांत, दृढ़]`. Hindi cues: धीमे, रहस्यमयी, भव्य, गंभीर, शांत, दृढ़, करुण, तेज़, क्रोध, विस्फोट, फुसफुसाकर, गिड़गिड़ाते हुए, ठंडा, स्नेह (English: slow, mysterious, grand, grave, calm, firm, pitiful, fast, angry, explosive, whispering, pleading, cold, tender).
- Hindi script: no English words. English script: rules in `guides/LANGUAGES.md`.
- No AI images anywhere: all art is code.

## Shot cues
Shots anchor to **beat id + cue id** (`flower_falls`), not to a Hindi word, so the same briefs serve both languages. Every visual moment that needs an exact cut gets a cue id in beats.json with an anchor phrase per language that occurs in that beat's text (`studio.py check` verifies it; `script_check.py NN --anchors hi` prints the mapping for brief writers).

## Reels (9:16) - requirement, not built yet
Each chapter is cut as a vertical reel later. Write with that in mind: the hook line works without the teaser, the main subject of each beat can sit in the centre third, and on-screen names/subtitles must fit the vertical safe area. Details in `guides/BEATS_SCHEMA.md`.

## Retention checklist (script-doctor and script-editor both run it)
1. Teaser <= 20 s, ends on the planted question, does NOT give the answer.
2. Stakes stated plainly before 0:60.
3. Each chapter: hook line in the first 10 s, names re-introduced in one line, setup, turn, payoff, bridge line. No back-references.
4. No gap > 90 s without a hook/turn/reveal (scorecard "max re-hook gap").
5. Short and long beats alternate; no beat > 110 words.
6. The big set-piece (chase, race, battle) starts before 35% of the video.
7. Climax in C3; payoff within 30 s; post-climax <= 15%; recap <= 40 words.
8. Comment question + next-episode tease only at the very end.
9. Every chapter is 2.5-3.2 min; total 8-10 min at the measured pace.
10. Read each reel alone: would a stranger understand who, what they want, and why it matters?
