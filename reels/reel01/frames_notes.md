# Reel 1 "Did Shiva Make Humans?": approval stills, notes

- 24 shots (avg 3.3 s, 1.8 to 6.1 s), one 1080x1920 still per shot taken at 55% of the shot: `library/showcase/reel01_frames/000_s01.jpg` to `023_s24.jpg`, plus contact sheets `sheet_00..03.jpg` (6 per sheet, shot number + spoken line).
- Briefs: `reels/reel01/briefs.json` (made by `reels/reel01/briefs_gen.py`, which also places every face at 38-50% of the frame height). Then validate (0 errors), shot_plan, shots, and `qa_report.json`.
- Title card "Did Shiva Make Humans?" is on frame 000 in two big lines (14-35% of the height). Brahma's face sits just below it at about 50%.
- Stack layout is used only for Vishnu/Brahma (s05) and Goddess/Brahma bowing (s18). Every other two-figure shot uses a window pan or a fixed window.
- Ardhanarishvara always uses `flip:-1`, so the male (Shiva) half is on the figure's right.

## Known weak spots
- s03 "sons had rejected him": the kumara rig has no back view. After the turn the sons still face the camera, and only a sideways glance and walking away show the rejection.
- s09: seated Shiva is a little cut at the right edge of the window, and his seat floats slightly above the snow (the subtitle box hides most of it).
- s14/s15 (split): the `light_beam` seam is faint. The split reads through the blue (male) and rose-gold (female) glows and the cross-fade from Shiva to ardha on "changed". There is no dedicated split-light effect.
- The ardha rig is static (standing, calm), so there are no gestures in s15-s17 and s24. Variety comes from framing (full figure, head close-up with name plate, wide cosmos).
- s13: the Goddess "open" pose looks a little stiff.

## Workarounds
- Owner ban: no sparkles. "Creation" uses halo rings, glows, light orbs (s19) and gold `embers` motes (s20) instead.
- Rock "seat" objects under seated Shiva were too pale or low to read. In s23 Shiva now stands. s04 sits on clouds and mountains.
- Sons: `kumara` (listed for reel 1 in reels/cast.json) was used even though it is not in the --cast list given to reel_setup.

## Engine and tool changes
- `engine/main.js` (VERTICAL only): `vFaceY` now knows seated rigs (sit, sitpray, Brahma on his lotus: face about 195*s above y instead of 300*s), so the 9:16 window frames seated faces correctly. EP6 still 040_b04_12 has the same md5 before and after (911ca8b7...).
- `studio/validate_brief.py`: the same seated-face rule in the 9:16 face check.
- `studio/ep_frames.py`: vertical contact sheets now have 6 tiles each, captioned with the shot number, id and narration from briefs.json.
- Limit: `vFaceY` assumes a standing face at 300*s for every rig. The real offset ranges from about 265*s (manu) to 313*s (adishakti), so window framing can be off by a few percent.
