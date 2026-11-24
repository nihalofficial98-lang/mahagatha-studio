# Languages (English first from EP07; Hindi optional)

OWNER DECISION: from EP07 onward all scripts, voiceovers and subtitles are in **English**. EP01-EP06 were made in Hindi and stay as they are. Hindi remains available as an optional second language (and EP07's `script.hi.md` is kept as a reference).

## Files
```
episodes/epNN/episode.json    "language": "en" | "hi"  (primary language; default en for NN>=7, hi for NN<=6)
episodes/epNN/beats.json      structure, shared by all languages (guides/BEATS_SCHEMA.md); "languages": ["en"]
episodes/epNN/script.en.md    English script (primary from EP07). script.md is a link to the primary-language script so the align/voice pipeline is unchanged
episodes/epNN/script.hi.md    Hindi script (EP01-06 primary via script.md; optional second language later)
library/voice_profile.json    pace per language (seconds per script word); English 0.40 is an ESTIMATE until calibrated
```
Old episodes (EP06) have only `script.md`; that is read as Hindi.

## Order of work
1. English: script-editor writes beats.json + `script.en.md` -> `studio.py check NN` (checks the primary language) -> script-doctor -> fixes -> **owner approves** -> owner records the English voice.
2. Hindi (optional, only if the owner asks): `script.hi.md` against the same beats.json -> `studio.py check NN --lang hi` -> script-doctor. Deliverables go in `deliverables/hindi_reference/`.

## English style (primary)
- Plain spoken English, owner's reel style (`guides/REEL_STYLE.md`): short past-tense sentences, one action or image each; mostly indirect speech, short quotes where a god speaks; no filler, no moral lecture.
- Mild emotion cues in brackets, one per beat: `**B07** [calm, firm]`. Never shouting. Cues: slow, mysterious, grand, grave, calm, measured, firm, pitiful, fast, angry, explosive, whispering, pleading, cold, tender.
- **Numbers as words** ("one hundred and eight", "nine hundred and ninety-nine"). The speech recognizer writes what is spoken; digits would not match the script and the subtitles would drift.
- **No standalone dashes** (" - " or " — " as a separate token): use a comma or a full stop. Prefer no hyphenated compounds either; if one is needed ("lotus-eyed"), use it consistently.
- **Names**: one spelling per name, from `names.<id>.en` (Bala, Indra, Vishnu, Shiva, Kamalanayana, Sudarshana, Navaratnas). No diacritics, no alternate spellings in the same episode. Re-introduce every name in one line in every chapter.
- At most one Sanskrit term per chapter and only when it is explained in the same line ("a yagna, a fire ritual"). Prefer the English idea to the title. No Devanagari anywhere in the English script.
- Every cue id's `anchor.en` phrase must occur in the English text of its beat (the checker verifies it).
- English hook titles: `deliverables/EPNN_YouTube_Hook_Titles.txt` (6 titles, curiosity-led, never promising something the video does not show).

## English as an adaptation (when one language is written from the other)
- Write each beat fresh for the target ear, keeping the beat's intent, roles, emotion and cue ids. Same story facts, same structure; different sentences.
- **Per-beat time budget is the same** (`budget_sec`), so word counts differ: English 0.40 s/word (about 1,200-1,500 words for 8-10 min), Hindi 0.367 s/word (about 1,310-1,630).

## Pace and calibration
`library/voice_profile.json` holds seconds per script word per language. The English value (0.40) is an estimate. After the owner's first English recording is aligned (`build/epNN/timings.json`): `python3 studio/script_check.py NN --calibrate`; from then on `check` uses the measured pace. `PACE=0.38` overrides it for one run.

## Pipeline per language
- The primary language uses `build/epNN/timings.json`; a second language would use `build/epNN/<lang>/timings.json` (not wired for align/render yet).
- Shots are reused across languages through `beat` + `cue_id`: the brief says *what* happens at `flower_falls`; each language's timings say *when*.

## English subtitles (render and SRT)
- Subtitles are always exactly what the owner said: words and times come from the recognizer's word-timestamp JSON (`studio.py align NN voice.mp3 --timestamps words.json` -> `hide_unspoken.py`). The script supplies the spelling and punctuation; unspoken script words are hidden, extra spoken words are added.
- **Group size**: the film renderer shows one line at a time, a group of words each at most about **42 characters** (Hindi: 30), grouped by the word timestamps (a pause over 0.25 s or a beat change starts a new group). The word being spoken is highlighted, earlier words of the group are bright, later ones dim. Font stack for Latin text: `NSerLat` (optional bundled file `engine/fonts/noto-serif-latin-latin-600-normal.woff2`), Noto Serif, Source Serif 4, Georgia, Liberation Serif, DejaVu Serif, then the Devanagari font and `serif`. Hindi episodes keep the original stack and render identically.
- **SRT export** (`make_srt.py`, `make_srt_ts.py`): cues are sentence/phrase pieces split at `. ? ! , ` and then in the middle, **at most about 42 characters per line, 2 lines per cue**.
- Word text in `timings.json` drops surrounding punctuation but keeps inner apostrophes and hyphens in English words (Bala's, lotus-eyed). Punctuation-only tokens are hidden.
- The pipeline matches script words to recognizer words by fuzzy alignment on letters (case and punctuation ignored); that is language-agnostic. Spell numbers as words so they match.
