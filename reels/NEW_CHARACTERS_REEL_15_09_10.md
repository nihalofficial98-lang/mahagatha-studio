# New characters / objects needed for reel15 (Garuda), reel09 (Bhasmasura), reel10 (Indra, Diti, Marutas)

Status: setup + prepare done for all three (reels/reel15, reel09, reel10 have reel.json, reels/build/reelNN has words.json, subs.srt, timings.json, beats.json). `cast` in each reel.json is empty. Briefs NOT written: waiting for the character designer (Opus). Checked against `python3 studio/engine_vocab.py`, engine/v2_cast.js, library/CHARACTERS.md, reels/cast.json.

Already available (no work): vishnu, vishnu_rest, shiva, narada, indra (prop vajra, crown), indra_thin, kashyapa, diti (EP rig), hiranyaksha, hiranyakashipu, boar, agni, vayu, villager(_w), asikli, Shesha snake tube + snakeHead helper (engine/v2_cast.js ~l.377-410), PK.vajra, PK.sword, PK.chakra, gada, pfx (embers, energy_swirl, divine_rays, ground_crack, halo_ring, havan_kund, sand_drift, boulder, cloud_white_cluster...).
NOTE: **parvati is NOT in the engine** (only listed in library/SERIES_PLAN.md); `sati` / `adishakti` rigs exist and could be recoloured.

## Characters (new rigs)
| name | story role | look (iconography) | poses / props / animation needed | reels |
|---|---|---|---|---|
| garuda | hero; "half bird, half man" son of Vinata; carries the Amrut; later Vishnu's mount | Man-bird: human torso, strong arms, golden-orange/ruby body, white face and chest? (classic: red wings, golden body, white face), eagle beak, crown/kirita small, big feathered wings (spread, folded, flap), taloned feet. Big (towering), can be a flying form seen from side | stand, fly (side, flap cycle), hover, bow/namaste (to Vishnu), glide with pot in talons/hands, wing-spread power pose, carrying Vishnu on his shoulders/back (Vishnu seated on his back, Garuda flip:-1 ok); one golden feather detaches and falls (prop `feather_gold`); moods calm, joy, fear(freeze), determined | reel15 |
| vinata | Garuda's mother, slave of the snakes | Gentle woman in dull/faded sari (saffron-brown), tired eyes, no jewellery except thin bangles, hair tied; later radiant freed | stand, sit, plead, grief, joy (freed), namaste; chains/shackle or bound-wrists prop, optional | reel15 |
| naga / kadru_naga (crowd) + kadru | the snakes who keep Vinata as a slave; guard Amrut (two snakes) | Hooded cobra-people or true snakes: dark green/black, hood with pattern, red tongue, gold eyes; reuse snakeTube/snakeHead. `nagas` crowd of 3-5, plus two large guard serpents in the fire ring. Kadru optional (not named in the spoken audio of reel15; only "the snakes") | coil, rise hood, hiss, slither, bow before pot, release chains; guard snakes (big, 2, eyes fixed) | reel15 |
| bhasmasura (+ early form vrikasura) | the demon devotee, blessed by Shiva; burns himself | Asura: dark red-brown skin, horns/wild hair, small tilak + rudraksha as a devotee in the first part; sword in hand; red eyes; after boon: aura of ash-grey glowing right hand. Two looks: `vrikasura` (ascetic, thin, matted hair, tapasya) and `bhasmasura` (same face, ash-grey streaks, glowing hand) | sit-meditate (tapasya, ages), sword at own neck (self-sacrifice), kneel/plead, point/reach (hand raised to touch head), chase (run), stare at Parvati, dance (copying Mohini), hand on head, turn to ash: `ash` effect (body desaturates, crumbles to pile of ash, particles) | reel09 |
| mohini | Vishnu in female form; dances | Beautiful woman, Vishnu-blue/dark-teal skin (so the viewer reads Vishnu), red-gold sari, golden ornaments, jasmine garland, long braid, bindi, kirita-like small crown; graceful | dance poses (tribhanga, hand-on-head pose, spin), stand, laugh, beckon (`come`), Vishnu-to-Mohini transformation (shimmer/dissolve with `vishnu`) | reel09 |
| parvati | Shiva's wife; the demon wants her | Fair/golden, red sari with gold, bindi, long hair, crown small, gentle; walking down a hill | stand, walk, sit, surprise, fear | reel09 |
| marut (crowd) + embryo | 49 children born from the cut pieces; "Maruda" cry | Small bright storm-spirit babies: 7 x 7 shown as a grid/crowd; blue-gold tints, tiny crowns, crying mouths, lightning/wind swirl; plus `embryo` (unborn child in the womb, glowing, curled) | embryo curled in womb glow; embryo cut in 7 then 49 pieces (pieces move apart, each still alive, mouths crying); babies crowd bursts out; stand beside Indra as warriors (small adult storm gods: grown form) | reel10 |
| diti_pregnant | Diti late pregnancy, asleep | Existing `diti` rig with a large belly option and a sleeping pose (eyes closed, lying), feet unwashed (dusty feet) | lie/sleep pose, sit tapasya, rise from sleep, belly glow (womb cut-away view: stylised inner sac) | reel10 |

## Objects / effects (new)
| name | where | look | animation | reels |
|---|---|---|---|---|
| amrut_pot (`kalasha_amrut`) | held/carried by Garuda, set before snakes | Gold pot with glowing pearly-white/pale-gold liquid, lid, glow | glow pulse, carry, set down | reel15 |
| fire_ring | gods' guard around Amrut | Ring of flames, animated flame tongues, vertical wall of fire; Garuda crashes through | flicker loop, part/extinguish (Garuda drinks rivers / wing wind) | reel15 |
| spinning_blades | gods' guard | Ring of sharp steel discs/blades, fast rotation with motion blur arcs | spin, Garuda shrinks through the gap | reel15 |
| guard_snakes (2) | see nagas | large serpents | strike, fall | reel15 |
| feather_gold | Garuda's feather | One long golden feather, glints | float down, rotate | reel15 |
| vajra (large, thrown) | Indra throws at Garuda; Indra cuts the embryo | PK.vajra exists as a held prop: needs a thrown/flying version with lightning crackle and a trail; a large version for the womb cut (flash) | throw arc, impact flash, flash-cut slice effect | reel15, reel10 |
| womb_view | reel10 | Stylised warm glow sac / inner view, not anatomical: soft red-gold bubble with a curled glowing child silhouette; Indra small inside with Vajra | pulse, slice flash | reel10 |
| boon_glow / ash_effect | reel09 | glowing right hand (ember-grey); ash particles that become a pile; `ash_pile` prop | hand glow on, body to ash, ash settle | reel09 |
| ten_directions chase bg | reel09 | Reuse existing backgrounds: mountain, forest, desert, sky; no new asset needed; speed lines pfx if available | | reel09 |
| Vaikuntha / Kailash bg | reel09 | Vishnu's abode (gold, lotus, white clouds) and Kailash snow peak: check library bg list | | reel09 |
| hut / ashram bg + hill | reel10, reel09 | Existing `villager`/ashram backgrounds likely suffice; please confirm | | reel10, reel09 |

## Notes for the designer
- Everything coded in the same paper-cut style (engine/v2_cast.js, PK kit), no AI images; sheets via `python3 studio/cast_sheet.py <names>`; owner approves the sheets before briefs.
- Subtitle words as spoken: "Amrut", "vahana", "Vrikasura", "Bhasmasura", "Mohini", "Maruda" (spoken without a space; the script had "Ma ruda"), "Marutas", "49" (script "forty-nine").
- After the sheets are approved the Sonnet pipeline resumes: set `cast` in reels/reelNN/reel.json, write briefs.json (reels/reel07/briefs_gen.py layout), validate_brief, brief_to_plan, build_shots, ep_frames, qa_report, frames_notes.md, contact sheet library/showcase/reelNN_frames.
