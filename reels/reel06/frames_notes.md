# Reel 6 "Why Say Swaha?": approval stills, notes

- 36 shots (avg 2.29 s, 1.3 to 4.1 s), one 1080x1920 still per shot taken at 55% of the shot: `library/showcase/reel06_frames/000_s01.jpg` to `035_s36.jpg`, plus contact sheets `sheet_00..05.jpg` (6 per sheet, shot number + spoken line). The average is below the 2.6 s rule because the narration is made of many short lines (reel 4 was 2.75 s). No video rendered.
- Setup: `python3 studio/reel_setup.py reel06 --title "Why Say Swaha?" --cast agni,brahma,deva_thin,deva_thin2,indra_thin,kama,vishnu,prakriti,swaha,villager,villager_w`.
- Briefs: `reels/reel06/briefs.json`, made by `reels/reel06/briefs_gen.py` (same method as reels 1-4: faces solved to 38-50% of the frame height, narration = the spoken words of `reels/build/reel06/words.json`; spoken "yajna", "yajnas", "Kamadev"). Validate 0 errors, then shot_plan, shots and `qa_report.json`.
- Title card "Why Say Swaha?" is on frame 000 in two lines; Agni's face sits just below it at about 50%, standing behind the blazing fire altar.
- Stack layout only where two places or two speakers meet: s04 and s14 (heaven above, earth below), s19 (Kamadev above blaming, Agni below), s26 (Vishnu above advising, Brahma below praying).

## Story treatment
- Earth: a bright morning village yard (vista, banyan, flowering tree, thatched `hut`) with the brick `havan_kund` and its warm gold fire. Offerings are round gold light motes (`orbs`) falling into the fire.
- Brahmaloka: blue-gold cloudscape with gold pillars, the gold gateway (`palace_gate`) and Brahma on his lotus; a name plate on "Brahmaloka" (s07). The starving gods get a pale lilac-gray version of the same heaven (s03, s08, s15, s16).
- The earth-to-heaven path: a `light_beam` column rises from the fire altar at the bottom of the frame to the gateway of Brahmaloka at the top.
  - s13 "carried them to heaven": Agni rides up the column with raised arms, motes climbing past him (how it was meant to work).
  - s17 "nothing reached heaven": smoke and motes rise from the altar and vanish into a gray mist; a thin god sits above on a cloud looking down.
  - s23 "he could not carry them": motes drift up from Agni and fade in a gray sky.
  - s28 "to carry offerings from earth to heaven": Swaha rises up the column and the motes reach the gate, which lights up with a halo ring.
  - s32 "without it ... would not reach": the village woman's offering turns into gray smoke.
- Names on screen when spoken: Swaha (s02, s30), Brahma, Brahmaloka, Yajna, Agni, Indra, Kamadev, Vishnu, Prakriti.
- Swaha is created in s27: she fades in beside Prakriti in a warm light on "created".
- Ending: s36 merges "Then he gave Swaha in marriage to Agni, and the two were never parted." (a separate 1.6 s last shot fell inside the engine's 1 s end fade): Agni and Swaha with folded hands inside a marigold ring, faint Brahma blessing behind, then one merged fire glow and rising motes on "never".

## Known weak spots
- s34 "a tree without fruit": a plain leafy tree on a pale field; nothing explicitly shows the missing fruit.
- s35 "a snake without venom": there is no snake rig or object; the shot shows only "a man without knowledge" (puzzled villager, empty hands, faint empty halo ring).
- s06 / s18: the "Brahma" and "Kamadev" plates fade in on the spoken word, just after the still time, so they are faint in the stills (correct in motion).
- s23: the failing offering motes are small at phone size; the meaning reads mostly through Agni's pleading pose and the gray sky.
- s21 / s30: head close-ups of Agni and Swaha are large; the subtitle box sits on the chest.
- The havan kund fire is white-hot in its core (the engine's additive fire); the warm gold comes from the glow around it.

## Owner to confirm
- Humans: `villager` and `villager_w` are not in the reel 6 list of reels/cast.json. They are the humans who hold the yajna (s02, s04, s10, s11, s14, s32, s35), added as an exception like Brahma in reel 4.
- Stack orientation: the brief's example was "earth ritual above, heaven below". s04 and s14 use heaven above and earth below, so the stack matches the offering path that always goes up. To swap them, reverse `vertical.stack` in those two shots in briefs_gen.py.

## Workarounds
- Seated villagers (`sitpray`) floated in the air at a 38-50% face height, because a seated face is only ~195*s above the feet. All humans now stand (namaste / open hands to pour).
- s03: the starving gods sit on cloud banks (explicit `_fixed` placement in briefs_gen.py), so they do not float.
- The `flames` fx drew a large orange block over Agni's body in s22. It was removed; the fire is the big altar with a glow.
- Light effects are glows, halo rings, divine rays and round motes only (no sparkles or embers).

## Requests (not done here)
- character-designer (`engine/v2_cast.js` not edited): a small paper snake (naga) for "a snake without venom"; seated pose variants for villager/villager_w that sit on the ground at reel scale.
- scene/effects: a `fruit` option for the `tree` object (fruit on/off) for "a tree without fruit".
- engine (`engine/paper_fx.js` smoke_plume): clamp the highlight arc radius to >= 0. Today one `arc` call gets a negative radius (FX_ERRORS line in ep_frames; nothing visible).

## Engine changes
- None. engine/main.js, engine/v2_cast.js, engine/paper_*.js and the studio tools were not edited in this pass, so EP6 is untouched.
