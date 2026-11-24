# Reel 4 "Narada's Maya Test": approval stills, notes

- 30 shots (avg 2.75 s, 1.2 to 4.7 s), one 1080x1920 still per shot taken at 55% of the shot: `library/showcase/reel04_frames/000_s01.jpg` to `029_s30.jpg`, plus contact sheets `sheet_00..04.jpg` (6 per sheet, shot number + spoken line).
- Briefs: `reels/reel04/briefs.json`, made by `reels/reel04/briefs_gen.py` (same method as reel 1: faces solved to 38-50% of the frame height, narration = the spoken words of `reels/build/reel04/words.json`). Then validate (0 errors), shot_plan, shots, and `qa_report.json`.
- Setup: `python3 studio/reel_setup.py reel04 --title "Narada's Maya Test" --cast narada,narada_g,narada_old,vishnu,kanya,balak,balika`.
- Title card "Narada's Maya Test" is on frame 000 in two lines. Narada's face sits just below it at about 50%.
- Stack layout is used only for s24 ("back in Vaikuntha, standing before Vishnu": Vishnu above, Narada below). The other two-figure shots use a window pan (s02, s10, s12) or a fixed window.

## Story treatment
- Vaikuntha: blue-gold cloudscape, gold pillars, temple gateway (`palace_gate`) and a name plate on "Vaikuntha" (s05). The sky turns violet whenever "Maya" is said (s04, s07, s28, s30).
- The river world: a bright morning vista with the river visible behind a sand bank. The far plane holds only low hills (mountain bases sit on the horizon), so the river is never covered.
- The house on the sand is a new paper object, `hut` (see Engine changes). It shows up in s16-s23 and as a faint dream house in s27.
- Time passing: there are fade transitions s15→s16→s17→s18→s19. The sky goes spring, then autumn on "Years" (s17: a blossom tree next to an autumn tree, falling petals), then summer as a father (s18), then autumn as a grandfather (s19). s18 and s19 share the same frame and dissolve into each other, so the young householder becomes the white-bearded grandfather and the children shrink into grandchildren.
- The flood is stylised, not frightening. The sky cross-fades to soft gray on "day ... gray" (s21). Storm `r:0` uses slate blue with rain and a far lightning fork, with no red. A paper `wave_ocean` rises on "flooded". In s23 the wife and daughter slide out of frame with the wave and fade on "family".
- Dream: s14 shows a faint Vishnu behind Narada fading into mist on "Vishnu". In s27 the wife and children appear one by one as they are named, then dissolve on "none".
- "Slips away like sand" (s29): golden grains (new `sand_drift`) stream out of Narada's open hands and drift away.

## Known weak spots
- s03: "He asked for water" is shown only by Vishnu's open, empty hand. There is no water-pot object.
- s06: Brahma is not in the reel 4 `--cast` list. He appears only as a faint (45%) memory figure for "his father, Brahma", the same kind of exception as kumara in reel 1. Owner to confirm.
- s17: the falling petals (classic `petals`) are small at phone size. The seasons read mainly through the sky and the two trees.
- s23: the daughter is half cut by the right edge as she is swept away. The wife's open arms read as reaching rather than being carried.
- s26 "stunned": the narada rig's surprise face is mild. The shock reads through the straight stare, the open mouth and a pale ring.
- s04: the halo on "answer" fades in after the still time. Narada's face looks a little stern.

## Workarounds
- Owner ban on sparkles: the diamond-shaped `embers` looked like glitter at phone size, so the house (s16) uses a warm glow and the sand uses the new round-grain `sand_drift`. Light effects are glows, halo rings and violet `energy_swirl` only.
- Children faces: the balak/balika rigs carry the face about 195*s above the feet, not the 300*s the validator and `vFaceY` assume. In the family shots the adults' faces sit at about 38-40% and the children are at s .7-.84, so the children's faces clear the subtitle box. `briefs_gen.py` does not "lift" children off the ground, which would make them float.

## Requests (not done here)
- character-designer (`engine/v2_cast.js`, not edited): a stronger `surprise` for narada (wider eyes, raised brows) for "stunned".
- engine/tools: the 9:16 face rule (`vFaceY` in engine/main.js, `face_cropped_v` in studio/validate_brief.py) should know the child rigs (face about 195*s, like seated rigs). Today the validator only warns for them.
- scene/effects: a small water-pot (lota/kalash) object would make "asked for water / never brought it / where is the water?" visible.

## Engine changes (additive only; engine/main.js and engine/v2_cast.js untouched)
- `engine/paper_scenes.js`: new layer object `hut`. It is a mud house on a plinth with a thatched roof, an arched door, a window and a mango-leaf toran. Options: `w`, `h`, `col`, `roof`, `lamp:true` (warm light inside), `toran:false`.
- `engine/paper_fx.js`: new pfx `sand_drift`, a stream of round sand grains blowing from (0,0) toward +x and up (`w` = stream length).
- EP6 still `040_b04_12` has md5 911ca8b7eb021a467f2f7afc1e4ae7af before and after both changes.
