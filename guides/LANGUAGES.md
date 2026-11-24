# Languages (Hindi first, English optional)

## Files
```
episodes/epNN/beats.json      structure, shared by all languages (guides/BEATS_SCHEMA.md)
episodes/epNN/script.hi.md    Hindi script (master). script.md is a link to it so the existing align/voice pipeline is unchanged
episodes/epNN/script.en.md    English adaptation: same beat ids B01..Bnn, own words, own [cue]
library/voice_profile.json    pace per language (seconds per script word), measured from the owner's recordings
```
Old episodes (EP06) have only `script.md`; that is read as Hindi.

## Order of work
1. Hindi: script-editor writes beats.json + script.hi.md -> script-doctor -> fixes -> `studio.py check NN` passes -> **owner approves** -> owner records.
2. English (optional, only after the Hindi is approved): script-editor writes `script.en.md` against the same beats.json -> `studio.py check NN --lang en` -> script-doctor -> owner records the English voice.

## English is an adaptation, not a translation
- Write each beat fresh for an English ear, keeping the beat's intent, roles, emotion and cue ids. Same story facts, same structure; different sentences.
- **Per-beat time budget is the same** (`budget_sec`), so words differ: English pace is provisionally 0.40 s/word (about 1,200-1,500 words for 8-10 min) until the first English recording is measured with `python3 studio/script_check.py NN --lang en --calibrate`.
- **Names**: one spelling per name, from `names.<id>.en` (Brahma, Vishnu, Shiva, Ketaki flower). No diacritics, no alternate spellings in the same episode.
- **No transliteration clutter**: no Devanagari, no italic Sanskrit glosses, at most one Sanskrit term per chapter and only when it is explained in the same line ("a jyotirlinga, a pillar of pure light"). Prefer the English idea ("the keeper of the world") to the title ("Palankarta").
- Dialogue stays short and spoken; each god keeps a distinct voice.
- English cues in brackets: `**B07** [fast, thrilling]`. Every cue id's `anchor.en` phrase must occur in the English text of its beat (the checker verifies).
- English hook titles go in `deliverables/EPNN_YouTube_Hook_Titles_EN.txt`.

## Pipeline per language
- Same alignment pipeline, separate timings: Hindi uses `build/epNN/timings.json` (unchanged). English timings are planned at `build/epNN/en/timings.json`; the checker and `--calibrate` already read that path. Wiring `studio.py align --lang en` and an English render (own subtitles, same shots) is **not built yet**: today only Hindi is aligned and rendered.
- Shots are reused across languages through `beat` + `cue_id`: the brief says *what* happens at `flower_falls`; each language's timings say *when*. Shot lengths stretch or shrink with the beat's duration in that language.
- Subtitles are always exactly what the owner said in that language (import_timestamps + hide_unspoken).
