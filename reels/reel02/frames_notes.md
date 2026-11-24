# Reel 2 "Why Go to Kashi?": approval stills, notes

- 36 shots (avg 2.4 s, 1.22 to 4.18 s; dense narration, one image per spoken idea), one 1080x1920 still per shot at 55% of the shot: `library/showcase/reel02_frames/000_s01.jpg` to `035_s36.jpg`, plus contact sheets `sheet_00..05.jpg` (6 per sheet, shot number + spoken line).
- Briefs: `reels/reel02/briefs.json` made by `reels/reel02/briefs_gen.py` (same method as reel 1: faces solved to 38-50% height; brahma5 head-sprout `hd` cues computed from spoken words). Validate 0 errors, then shot_plan, shots, `qa_report.json`.
- Setup: `reel_setup.py reel02 --title "Why Go to Kashi?" --cast brahma5,brahma,narada,brahmi,cow,mare,duck,doe,rishi1,rishi2,shiva,kapali`. Pilgrims use `villager`/`villager_w` (not in the cast list, like kumara in reel 1).
- Title card on frame 000 over Kashi at sunrise (ghat walls, temple tower, river, rays); pilgrims' faces at ~50%. The reel ends on the same pilgrims (bookend).
- Stack layout only once: s20 Shiva in fury (top) / Brahma begging (bottom).
- Restraint on the desire beat: s08 violet curse-mist, s10 a still sideways stare (no smile, no Brahmi in frame), s11 Brahmi far away with a pillar between them, eyes lowered, turning away; s12 she walks off alone.
- The cut (s21): no blood, no blade on screen: white flash over the crown + cross-fade brahma5 -> four-headed brahma (eyes closed). Head -> skull (s30) is a soft light cross-fade; skull fall (s33) = kapali skull -> kapali none + `skull` fx on the ground + light ring.
- Animal forms (s15-s17) face left (flip -1), each with Brahmi's necklace; s17 shows cow and mare small behind the doe with halo rings for "a hundred forms".

## Known weak spots
- s21: the light_beam slash is not visible in the still; the cut reads via the flash and the head cross-fade.
- Kapali holds the head/skull in the hand on the SCREEN LEFT, i.e. his anatomical right hand, but the narration says "left hand" (s06, s24, s25, s29-s32). **Request (character-designer): move the kapali prop to the other hand (`handAt(...,+1)`) in engine/v2_cast.js.** Not changed here.
- s15-s17: animals are raised so their heads clear the subtitle band, so their feet float a little above the meadow ground.
- s07: the Narada name plate appears on the spoken name, after the still time.
- Figures in Kashi shots stand on the vista river path (reads as wading at the ghat). No ghat-steps background exists.
- validate_brief warns on s16 (duck) because its face check assumes 300*s for every rig; animal heads are ~115-215*s above the feet.

## Engine and tool changes
- None. engine/main.js and engine/v2_cast.js untouched (EP6 unaffected).
