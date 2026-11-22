# What Opus did differently (and what the engine rig now copies)

Compared: `engine/v2_cast.js` + `library/characters/shiva/shiva_v2.js` (the rig EP1-EP6 used) against the Opus Trimurti showcase (`library/showcase/trimurti/`).

| Area | Old rig | Opus look | Now in the engine (`engine/paper_kit.js` = `PK`) |
|---|---|---|---|
| Shapes | One flat fill per part, no outline; parts overlapped with visible seams | Every part is a "paper-cut layer": soft drop shadow + gradient fill + ink outline (`cut()`) | Limbs, legs, torso, dhoti, tiger skin, crowns and horns get an ink outline (`inkCap`, `PK.cut`) |
| Faces | Tiny flat eyes and brows. Anger = one extra brow stroke | Lotus-petal eyes with kajal wings, sliding eyelids, cheek blush, nose, two-part lips, earrings | `drawHead` now calls `PK.face` for every character |
| Anger / sadness / surprise | One anger value that swapped the brow | Three separate controls. Anger: inner brow pulled down, thicker brow, lid slanted over the eye, iris and glow turn red, frown. Sad: inner brow raised, outer lid drooping, tear, downturned mouth. Surprise: raised brows, open mouth | `face()` takes `anger`, `sad`, `surp`, `mouth`, `smile`, `lx`, `ly`, `blink`. The EP6 `mood` and `expr.brow` values feed them unchanged |
| Hands | Ellipse palm and four blobs | Palm plus capsule fingers and thumb, outlined; abhaya, jnana, rest and grip variants | `handS` and `hand` call `PK.hand` |
| Jewellery | A rectangle band and a dot | Gold gradient bands with gems, beaded necklaces, kirita with horns and a gem band | `armband` uses `PK.band`; `headgear` uses `PK.kirita` / helmet / ink horns; Brahma uses `PK.jataMukuta` |
| Props | Flat discs | Chakra with flame petals, shankha, padma, gada and trishul, all layered and glowing | `PK.chakra`, `PK.shankha`, `PK.padma`, `PK.gada`, `PK.trishul` |
| Serpents | Round-end strokes | Tube with belly, scale marks and a real hood and face | Vasuki on Shiva uses `PK.tube` and `PK.hood` |
| Shiva's jata | A plain bun and a free-floating blue arc for Ganga | Layered locks and coiled bun, crescent moon, and Ganga flowing down along the locks | New `drawJata` |
| Light and finish | Grade only | Glows, halo, grain and a colour wash on top of the layers | Engine grade/rim already did this; the new layers pick it up |

Rule of thumb Opus followed: build every character from the same small kit of layered primitives so they all share one look, and give each one its identity through colour, crown, tilak, beard and props. New characters are a spec in `CAST` plus these primitives; no one-off drawing code.

## Vishnu sleeping pose (yoganidra)
The old pose had the head upright at the end of a horizontal body with only hair joining them, and a lower arm dangling onto the coil. Fix (in `trimurti_rigs.js` `drawVishnu`): head moved closer to the shoulders with a visible neck, tilted along the body line, and the near arm now bends up so the hand props the cheek; eyes are closed by default.

## Regenerate
```
python3 studio/ep_frames.py 06 --out library/showcase/ep06_frames   # one frame per EP6 shot
node library/showcase/trimurti/render_frames.js                      # the Trimurti hero frames
```
