# Reel 5 "Shiva Born From Anger": approval stills, notes

- 36 shots (avg 2.47 s, 1.18 to 4.36 s), one 1080x1920 still per shot taken at 55% of the shot: `library/showcase/reel05_frames/000_s01.jpg` to `035_s36.jpg`, plus contact sheets `sheet_00..05.jpg` (6 per sheet, shot number + spoken line).
- Setup: `python3 studio/reel_setup.py reel05 --title "Shiva Born From Anger" --cast brahma,kumara,rudra,shiva,vishnu`.
- Briefs: `reels/reel05/briefs.json`, made by `reels/reel05/briefs_gen.py` (same method as reels 1-4: faces solved to 38-50% of the height, narration = the spoken words of `reels/build/reel05/words.json`; new key `_fix` keeps a hand-placed y for the crowd). Validate 0 errors, then shot_plan, shots, `qa_report.json`. No cue misses.
- Title card "Shiva Born From Anger" is on frame 000 in two lines. The newborn Rudra (fire halo) stands just below it with his face at about 50%.
- Stack layout only twice: s20 "Tell me my name" (Rudra above, Brahma below) and s31 "Eleven Rudras stood before Brahma" (the eleven in three rows above, Brahma on his lotus below). The other two-figure shots use a window pan (s23 naming, s28 the request) or a fixed window.
- Subtitles are the engine's burned-in words (spoken "being" for the script's "beam", "Mahadev").

## Story treatment
- Brahmaloka: blue-gold cloudscape, gold pillars, white cloud corners. The Kumaras get a softer blue-rose sky, the "infinite" a violet-gold sky with a glowing infinity sign (s11).
- Four sons from the mind (s05): a ring of light opens round Brahma's head on "mind" and the four boy sages fade in at the foot of his lotus, two on "four", two on "sons". Name plates: Brahma, Kumaras, Rudra, Mahadev, Eleven Rudras; Creator / Preserver / Destroyer for the trinity line.
- "Fill the world" (s07): the clouds under Brahma cross-fade to a green valley with a river.
- Refusal: folded hands on "folded", heads turned aside on "no" (s08); a turning gold wheel (birth and death) above them in s10, and again over Brahma in s32 ("mortals who die and are born again").
- Anger: the sky turns bright fire-orange on "rage" (s15), never dark. The birth (s16): forehead glow, flames and a light column from Brahma's forehead with a small fire-haloed Rudra rising in it. s17: Rudra walks out of the light column, eyes flaring red. s18/s20: red eyes, roar, shock rings.
- "red / roaring / rud" (s22): the words appear in the sky on their spoken words; "rud" is big and gold-brown.
- Naming (s23): Brahma raises his blessing hand on "Rudra", Rudra's eyes calm. s24: on "Shiva" Rudra cross-fades into the familiar Shiva (blue halo, trishul, Vasuki); "Mahadev" plate.
- Copies (s29-s30): beings with his shape and a fire halo fade in around Shiva one after another; a ring of undying light on "immortal". s33: two copies stand faint behind him.
- Leaving (s34-s36): the hall cross-fades to the white Himalaya by day; Shiva folds his hands, walks off into mist, and the reel ends on the meditating god with his fire halo and a halo ring on "never".

## Known weak spots
- Brahma sits on the lotus (pose `sit`) when he is still (s04, s05, s16, s19-s21, s25, s31, s32) but stands to gesture (s07, s13, s14, s23, s28), because the seated lotus rig cannot move its arms. The switch is never on a hard cut between two Brahma shots of the same moment, but it is visible across the reel.
- s10/s32: the wheel of birth and death is the small classic `icon cycle`; pale against white clouds.
- s14: Brahma half cut at the left edge; the Kumaras walk off facing the camera (no back view, same as reel 1).
- s16: the fire column is the flat classic `beam`; the forehead flames look like a crown of fire. The rising Rudra reads well.
- s18: the roar shows red eyes and heavy brows; the head close-up's mouth stays nearly closed.
- s22: the still shows "red" and "roaring"; "rud" appears on the last word, after the still time.
- s29/s30/s33: the copies are the rudra rig (fire halo, no trishul or serpent), as cast.json lists for the eleven Rudras. Owner to confirm.
- s36: the final meditating god is the rudra rig (fire halo, no trishul) because the shiva rig in `sitpray` draws its trishul floating above his head. It reads as a callback to "born from anger", but the halo changes from blue (s24-s35) to fire.
- Average shot length 2.47 s is just under the 2.6 s guideline (fast lines like "Brahma created, / Vishnu preserved," are single shots).

## Requests (not done here; engine/v2_cast.js not edited)
- character-designer: seated Brahma on the lotus with gesture poses (open / point / raise / plead), so he does not have to stand up to talk.
- character-designer: shiva in `sitpray` should lay the trishul beside him (or honour `prop:'none'`), so the final shot can use the shiva rig.
- character-designer: rudra `head:true` with a real open-mouth roar (`mood {anger:1, mouth:0.8}` barely opens it).
- effects: a soft-edged fire column / forehead-burst pfx, and a paper wheel-of-life prop bolder than `icon cycle`.

## Engine and tool changes
- None. engine/main.js, engine/v2_cast.js, engine/paper_*.js and the studio tools are unchanged, so EP6 is untouched. No video rendered.
