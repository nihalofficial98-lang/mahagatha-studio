# EP6 final stills (paper-cut look)

One still per shot for all 221 shots of EP6, named `NNN_<shotid>.jpg` (1920x1080, rendered at 2560x1440, JPG quality 84). `sheet_NN.jpg` are contact sheets of 20 frames each.

## Regenerate
```
python3 studio/ep_frames.py 06 --out library/showcase/ep06_frames --q 84            # all 221 (about 25 min)
python3 studio/ep_frames.py 06 --out /tmp/check --only 0-19,45                      # a few shots
```
This needs no network. It reads `episodes/ep06/shots.json` and `voice_timeline.md` and takes each frame at 55% of its shot. A run with `--only` writes its own sheets, numbered from 00.

## What was improved
- One shared paper-cut body draws every character (`engine/v2_cast.js` `drawHuman`, built on `engine/paper_kit.js`). It has the Opus torso, ink-outlined IK arms with armlets and bangles, and hands chosen from the pose: rest, raised abhaya, pointing, joined in namaste, jnana when seated, or gripping a prop. Legs are cloth-covered with front-view feet and anklets. Lower garments are a dhoti with a pleat fan, a short dhoti, a sari with pleats and a border, or a tiger skin, and seated figures get crossed legs. Each character is a `CAST` spec that sets colours, build, hair (cap, jata, turban, wild, long, Shiva's bun), crown (kirita, raja, Indra fan crest, Chandra moon crest, asura spikes, Brahma's jata-mukuta), necklaces (hara, pearls, rudraksha, tulsi, vanamala), sash, sacred thread, uttariya, armour, halo or sun disk, and a prop (gada, sword, vajra, veena, kamandalu, mala, lotuses, trishul).
- Brahma stands, walks or points with three heads and four arms (Veda, mala, kamandalu) when the shot sets `lotus:false`. Otherwise he is the Opus seated lotus hero with a halo. Shiva uses the same body, with jata locks, the bun and crescent moon (no water stream), Vasuki, tiger skin and trishul. Vishnu has four arms with chakra, shankha, gada and lotus, a vanamala to the knees, and a kirita with no horns.
- Head close-ups now have a real bust (shoulders, chest, jewellery, Vasuki for Shiva) on their own canvas band, so the old straight cut line under the chest is gone. They are slightly smaller, with smaller halos.
- Faces show anger more strongly (thicker, lower inner brows, red eyes, frown). Sadness is clearer too: inner brows sit higher, the lids droop, a tear appears from sad 0.32, and the mouth turns down further.
- Backgrounds (`engine/paper_scenes.js`): cloud banks are built from puffs of different sizes and heights with no repeated arches, and have rim light and bottom shade. Cosmos has cut-paper mandalas, nebula ribbons and ringed planets. Plain has a framed mandala with corner arcs. Vista has lit ridge edges and paper trees. Storm has paper lightning and rain. Sea and dusk have foam curls. Pillar has cloud banks at the top and bottom. Kailash has a cloud layer between its ranges. The palace is a new paper-cut hall with cusped arches, pillars, lamps, a toran and a carpet.
- Effects: the name pill is now a gold-edged plate, and shock rings have cut petals. Flames and the lotus effect are drawn as paper cut-outs. The swan and boar get an ink edge. Halo, chakra and aura glows are smaller, so frames no longer look washed out.
- Composition: the faces of four tiny figures were in the subtitle band, so they were moved up (shots 061, 069, 088, 104). Two shots had text over a crown: the Daksha name plate moved beside his head (205), and "आपका जवाब?" moved left of Brahma (215).

## Known weak shots
- 096_b07_2, 174_b13_2: the painted boulder/crack image covers much of the frame and does not match the paper-cut style.
- 086_b06_11, 161_b12_4: the divine-rays image is very bright behind the pillar.
- 095_b07_1, 123_b08_14, 137_b10_2: a large smoke-plume image washes over the scene.
- 097_b07_3: the swan is still the simpler old rig (ink-edged now) and sits inside a bright rays image.
- 205-210 (Daksha) and 038/116/124 (Brahma) close-ups: at s 2.1-2.2 the top of the crown touches the frame.
- 202_b14_17 and 160/165: the figures are very small next to the pillar or gate, as planned for scale.
