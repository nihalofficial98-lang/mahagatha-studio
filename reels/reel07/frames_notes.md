# Reel 7 "Daksha Cursed Narada": approval stills, notes

- 34 shots (avg 2.25 s, 1.1 to 3.9 s), one 1080x1920 still per shot taken at 55% of the shot: `library/showcase/reel07_frames/000_s01.jpg` to `033_s34.jpg`, plus contact sheets `sheet_00..05.jpg` (6 per sheet, shot number + spoken line). The pace is faster than Reels 1-4 because the narration is dense (77 s, 220 words, many short sentences).
- Setup: `python3 studio/reel_setup.py reel07 --title "Daksha Cursed Narada" --cast daksha,narada,haryashva,shavalashva,asikli`.
- Briefs: `reels/reel07/briefs.json`, made by `reels/reel07/briefs_gen.py` (same method as Reel 4: hero faces solved to 40-46% of the height, narration = the spoken words of `reels/build/reel07/words.json`). Then validate (0 errors), shot_plan, shots, and `qa_report.json`. No video rendered.
- Title card "Daksha Cursed Narada" is on frame 000 in two lines, with Daksha's face just below it at about 52%.
- Stack layout only in s06 (Daksha commands above, a Haryashva listens below) and s29 (angry Daksha above, calm Narada below). The other two-figure shots use a window pan (s12, s25, s31) or a fixed window (s22, s23).

## Story treatment
- Daksha's palace: an arched sandstone wall, gold pillars and a pale stone courtyard under a clear blue-gold sky (vista + `wall`/`pillar`/`hill` layers).
- Crowds: rows of the `haryashva` (green) and `shavalashva` (violet) rigs, 3-4 rows per shot. Rows recede (smaller, higher, alpha .45-.9 so the far rows fade), e.g. s04, s07, s18, s23. Three bigger princes stand in front when the name is said (s05 "Haryashvas", s24 "Shavalashvas", name plates) and for "no answer" (s14). The crowd shots tilt the camera down a little (camera y + up to 48) until every crowd chin clears the subtitle band.
- The River Sindhu meets the sea (s08-s14, s25): a bright blue sea on the horizon, a golden sand bank with palms, and the river as a blue channel running diagonally into the sea (the new `road` object with `plain:true`). Name plate "River Sindhu" on "Sindhu".
- Leaving (s19, s26): a dusty road runs to the sunrise; the brothers walk away along it in two loose files, smaller and fainter toward the horizon. s20 "No one saw them again" shows the near-empty road while the last tiny figures fade on "saw". The Shavalashvas dissolve into mist on "vanished" (s26).
- "6,000 sons ... every single one" (s02): faint rows of green and violet sons stand behind grieving Daksha and fade on "every".
- "Never raised a hand" (s03): Narada on the clouds folds his hands (namaste) and smiles a little.
- "A higher path" (s17) and "their choice to walk it" (s30): a golden road climbing to a lit mountain / running to the horizon.
- Daksha's anger (s27 roared, s28 homes, s31 cursed): bright warm-red sky, red eyes and heavy brows (no fangs), red energy pulse and red glow. In s28 the empty unlit houses stand behind him for "who would build homes".
- "Scattered his sons across the earth" (s32): tiny green and violet princes stand far apart over a wide green land.
- Curse (s33): Narada walks with his veena under the first evening stars past a lamp-lit house that is not his, and looks back on "home".
- Closing question (s34): Narada on the clouds; gold halo on "guide", violet swirl on "thief".
- Name plates follow the voice: "Ashikli" (spoken), while the cast id is `asikli`.

## Known weak spots
- s08: the "River Sindhu" plate fires on "Sindhu", after the still time, so it is not in the still.
- s19: there is no back-view rig, so the brothers walking away face the camera three-quarter. The front walker's body is behind the subtitle box, but his face is clear.
- s15 "smirked": the head bust is big and the smirk (smile .8, eyes sideways) is subtle.
- s02 / s34: the fade on "every" and the violet swirl on "thief" come after the still time. The stills show the moment just before them.
- s18: the sky change to gray-blue on "crept" is soft. The doubt reads through the faces and the mist.
- Crowd faces sit at 43-61% of the height (rows recede upward), lower than the 38-50% hero band but all above the 64% subtitle line.
- The narada `doubt` emotion draws a tear, so the questioning shots (s12, s13) use calm + surprise/smile moods instead.

## Requests (not done here)
- character-designer (`engine/v2_cast.js`, not edited): a walking-away / back-view pose for the crowd rigs (haryashva, shavalashva); a stronger one-sided smirk for narada; a `doubt` face for narada without the tear.
- tools: `studio.py qa` does not take reel ids (it looks for `build/epreel07/timings.json`).

## Engine changes (additive only; engine/main.js and engine/v2_cast.js untouched)
- `engine/paper_scenes.js`: new layer object `road`. It is a dusty road from (x, y) with half-width `w`, narrowing to the horizon point (`ex`, `ey`) with half-width `ew`. Options: `bend` (curve), `col`, `glow` (an rgb "path of light", soft), and `plain:true`, which turns it into a river with ripple lines and no stones/ruts. It is documented in `library/ENGINE_CAPABILITIES.md`.
- EP6 still `040_b04_12` has md5 911ca8b7eb021a467f2f7afc1e4ae7af before and after the change.
