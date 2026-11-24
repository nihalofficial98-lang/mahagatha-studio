# Reel 3 "Madhu and Kaitabha": approval stills, notes

- 31 shots (avg 2.85 s, 1.1 to 4.6 s), one 1080x1920 still per shot taken at 55% of the shot: `library/showcase/reel03_frames/000_s01.jpg` to `030_s31.jpg`, plus contact sheets `sheet_00..05.jpg` (6 per sheet, shot number + spoken line).
- Setup: `python3 studio/reel_setup.py reel03 --title "Madhu and Kaitabha" --cast madhu,kaitabha,vishnu,vishnu_rest,nidra,hayagriva2,brahma` ("lotus" in reels/cast.json is Brahma's seat / a prop, not a rig).
- Briefs: `reels/reel03/briefs.json`, made by `reels/reel03/briefs_gen.py` (same method as reel 1: faces placed at 38-50% of the height). Validate 0 errors, then shot_plan, shots, `qa_report.json`.
- Title card "Madhu and Kaitabha" on frame 000; Vishnu's face sits just below it at about 50%, the two brothers dark behind him.
- Stack layout only for Vishnu vs a brother: s02 (Vishnu / Madhu), s16 (Hayagriva / Kaitabha taking over from Madhu), s21 (Kaitabha / Vishnu).
- Look: bright cloudscape skies (blue-gold, violet-orange for the fight, indigo-silver for Yoga Nidra), a bright blue water surface (`waterfront` fx with lighter colours) for the primordial ocean, white mist in the near corners. Light comes from glows, halo rings and divine rays; no sparkles.
- Subtitles are the engine's burned-in words from `reels/build/reel03/words.json` (spoken "5,000" and "Hayagriv"); the name plate also says "Hayagriv" to match the voice.
- Beheading (s26) is stylised: the brothers sit small on Vishnu's thighs, the Sudarshan chakra spins beside him, and on "beheaded" a white flash and the brothers fade out. No blood, no severed heads.

## Known weak spots
- s06 earwax: the tiny brothers stand in the air beside Vishnu's head (on Shesha's hoods); there is no "crawling" motion and the amber glow is faint.
- s08 / s25 growth uses `ds` (scale grows over the shot), so the still shows them mid-growth; the growth is only visible in motion.
- s11: Brahma's face is at about 32% (above the 38-50% rule) to keep the falling Vedas off both faces. The Vedas (books fx) are large paper books; there is no "hiding" action, only Madhu's sneer and raised hand.
- s09 / s10: the brothers do not physically grip the lotus stem; the shake is the camera shake + Brahma's fear.
- s23: the yantra (`magic_circle`) used as the "trap" is big and fills the bottom of the frame under the subtitles.
- s29: the four Veda books across the top are large and slightly heavy for the frame.
- Vishnu's mace "laid down" (s03, s18) is shown by the mace leaving his hand when the pose changes (open / namaste); there is no mace object lying on the ground.
- Opening shots and the boon scenes use the normal `vishnu` rig; s15-s16 use `hayagriva2` (as cast.json lists).

## Requests (character-designer / engine, not done here)
- vishnu_rest: a mood/ear anchor would allow the brothers to emerge exactly from the ear.
- validator: `face_cropped_v` assumes a standing face (300*s) for vishnu_rest (real head ~205*s above y, offset left), which gives a false warning in s14.
- A small `veda` prop (books fx with a scale parameter) would make s07/s11/s29 lighter.

## Engine and tool changes
- None. engine/main.js, engine/v2_cast.js and the studio tools are unchanged, so EP6 is untouched. No video rendered.
