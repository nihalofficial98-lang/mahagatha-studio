# What the Mahagatha engine can render (read this before designing a scene)

Canvas 1280x720 logical (CX=640). Subtitles sit in the bottom ~18% (y>590): keep faces/action out of that band.
A shot = {start word cue, camera move, grade, shake, scene}. A scene = {bg, figs, fxb (effects BEHIND figures), fx (effects in FRONT)}.

## Camera (per shot, from -> to, eased)
`cam: {from:{z,x,y,r}, to:{z,x,y,r}}`  z = zoom (1.0 wide … 1.25 close; up to ~3 on a head close-up via figure scale), x/y = pan in px (±60 typical, ±120 big), r = roll in radians (±0.01 subtle, ±0.05 dutch-angle drama). `shake` 0–8 (1 = gentle breathing handheld, 4–8 = impact), `tilt` constant roll.
Parallax: backgrounds move with depth factors (far 0.1–0.3, mid 0.5, figures 1.0); effects images accept `par` (0 = glued to the far sky … 1 = moves with the figures, >1 = foreground that slides faster than the actors: use 1.3–1.6 for foreground silhouettes).

## Backgrounds (bg)
coded: cel(warm|cool heaven clouds), storm(r=0..1 red storm), voidR(black-red void with embers), night, dusk, moon, palace, dawn, amber, cosmos(rgb,spin), sea/cosmicsea(gold,gy,ga), plain, yagna(fire=0..1: pillars+havan kund+garlands), kailash(mx moon position), garden.
painted (Gemini, parallax zoom, `bg('img',src=…)`): yagna2, kailash2, cosmic_sea, garden, palace, cosmos, heaven_clouds, storm_red (library/pilot/backgrounds). Painted ones are opt-in (PAINTED_BG=1) and take particles on top (fire, embers, dust, stars, petals, lantern glow).

## Characters (coded rigs, front/3-4, planted; poses: calm, rage, lunge, flee, idle, pray/sit variants per character)
Shiva(+rage), Vishnu(4-arm, Hayagriva, reclining on Shesha), Brahma(4 faces), Daksha, 7 rishis, Narada, Adishakti, Manu, Brahmi, Madhu, Kaitabha, Harihara, Ardhanarishvara. Params: x,y,s(scale),flip,pose,expr{brow,eye},head:true (close-up bust),aura(rgb),dark,vx(slide),lx. Painted rigged Shiva puppet (`shiva_p`) exists but is NOT the approved look.
Library cut-outs (146 Gemini characters in library/puppets/*) exist for static/breathing use only (no limb animation).

## Effects (fx / fxb)
text, name(pill label), glow(r,rgb,ga), orbs, sparkle, petals, shock(rings), flash(w,rgb), bolt, crack, ribbon, beam, light/rays, flames, fire(pit), pillar, infinity, scales, trident, heart, tears, threads, outline, egg, books(vedas), gunas, element, lotus, bluemountain, waterfront, vaikuntha, clock, dim(ga).
Gemini effect/object images via `{'t':'fximg','src':…,'x','y','w','alpha','blend':'lighter','spin','grow','vx','par'}`: 91 in library/fx (fire_tall/small/ring, lightning_bolt_a/b/forks, thunder_flash, explosion_burst, shockwave_ring, smoke_plume, embers, sparkles_gold, sudarshan_chakra(=golden wheel), trident_plain, arrow_single(=the arrow), magic_circle, halo_ring, divine_rays, light_beam, energy_swirl, whirlpool_churn, element_agni/jal/vayu/prithvi/akash, om_symbol, lotus_pond_leaf, cloud_*, mountain_peak, mandara_mountain, tree_banyan/mango/palm/parijat, havan_kund, throne, palace_gate, temple_bell, kalash_pot, cosmic_egg, book_veda, crown_gold, kaustubha_gem, bow_and_arrow, sword_straight, axe_parashu, vajra_indra, chariot, boulder, waterfall, wave_ocean, river_bend, ashram_hut, star_field, snow_flakes, rain_streaks …). Fade-in is `c` (cue index) + `d` (fade seconds). Use `blend:'lighter'` for light/fire, normal blend for solid objects.

## Grades / mood (shot `grade`)
cel(neutral), night(blue), dark(vignette-heavy), red(wrath), amb(amber/golden), or an rgba() string. Keep one colour idea per beat.

## Timing rules
Shots start on spoken WORDS (cue words from the script) or line fractions, never on seconds. Shot length 1.0–6.5 s, average 2.6–4.2 s. At a fast voice (+15–20% vs guide) keep list/enumeration shots ≥1 s: merge or hold, do not flash.
## Not possible today (put under "asset/feature requests" and the producer will build it)
limb-animated walking, multi-view (side/back) characters, lip-sync, true 3D, water simulation, crowds with individual motion.

## Shot plan (what the scene director writes: episodes/epNN/shot_plan.json)
`python3 studio/studio.py shots NN` builds shots.json from it, timed to the owner's voice, and validates (unknown character/effect/background, missing assets, words not in the voice, shots <1.0 s or >6.5 s, extreme camera, effects waiting on missing cue words).
```
{"episode":"04","shots":[ {
  "id":"s012",
  "at": {"t":71.20,"word":"काट"}            // PREFERRED: absolute seconds from voice_timeline.md + the spoken word (checked)
       | {"beat":6,"word":"काट"}            // first occurrence of the word in that beat
       | {"beat":6,"line":2,"frac":0.4},     // or a line fraction
  "cues": ["काट"],                           // words that effects with "c":0 / "c":1 fade in on (in order)
  "bg": {"k":"yagna","fire":0.9} | "cosmos" | {"k":"img","src":"bgp_yagna"},
  "figs": [ {"who":"shiva","x":420,"y":670,"s":1.45,"pose":"rage","expr":{"brow":-0.95},"aura":"255,70,40","flip":-1} ],
  "fxb": [ ...effects BEHIND the characters ],
  "fx":  [ {"t":"img","src":"lightning_forks","x":900,"y":250,"w":380,"alpha":0.7,"blend":"lighter","par":1.3}, {"t":"text","s":"…","x":640,"y":300,"size":70,"c":0,"d":0.8} ],
  "cam": {"from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.1,"x":-20,"y":-8,"r":0.004}},
  "grade":"night", "shake":2, "note":"why this shot"
  // or a hand-coded exception: "custom":"name_in_custom_shots_py", "args":{...}
} ] }
```
Image effects: `"t":"img","src":"<name>"` where name is any library/fx image (e.g. `fire_tall`), `lib_<character>` (cut-out) or `bgp_<background>`; the builder copies it into the engine automatically. `par` = parallax depth (0.1–0.3 far sky, 0.5–0.8 mid set pieces, 1.0 actors, 1.3–1.6 foreground). Every beat needs a shot at its start. Hand-coded exceptions: write a function in `episodes/epNN/custom_shots.py` that returns the engine scene dict `{bg,figs,fx,fxb}` and reference it with `custom`.

## Required parameters of effects that crash or vanish without them (builder now checks the first three)
- `threads`: `x`,`y` (start) and `to`: [[x,y],...] (end points); optional `rgb`, `bend`. `orbs`: `items`: [{`c` (cue index), `x0`,`y0`,`x1`,`y1`, `r`, `rgb`, `dur`, `arc`, `keep`}]. `beam`: `x`,`y`,`len` (a vertical light column rising from the point), optional `w`. `infinity`: `x`,`y`, `c`,`d`.
- `text`: `s`,`x`,`y`,`size`,`c`,`d`. `name`: `s`,`x`,`y`. `glow`: `x`,`y`,`r`,`rgb`,`ga`. `shock`: `x`,`y`,`c`,`rgb`,`max`. `flash`: `c`,`w`,`rgb`. `sparkle`: `x`,`y`,`n`,`rx`,`ry`.
- Image effects (`fximg`): `alpha` is the MAXIMUM opacity reached after the fade-in (`c`/`d`); never give a fade-in an `alpha` of 0.
- Known weak library images (visible rectangles or odd scale): `mountain_peak` (has a box background), `stars_gold_big` (huge at w>400), flower/petal clusters over w>700. Prefer `star_field`, `halo_ring`, `divine_rays`, `cloud_*`.

## Character acting (coded rig, from EP6 on)
Every character is a jointed vector rig (head, eyes, brows, mouth, shoulders, elbows, hands, knees, feet). Per figure in a shot:
- `acts:[{c:<cue index>,pose:'namaste|bow|point|raise|open|plead|flee|lunge|sit|hold',d:<seconds>,mood:{...},tilt:<rad>}]` blends to the pose on that spoken word.
- `walk:<speed>` (leg and arm swing) with `vx` drift; `mx,my` + `mc,md` move on a cue; `bow`, `kneel` with `bc,bd`; `fo,fd` fade out.
- `mood:{smile,sad,surp,mouth,lx,ly,blink}` face; anger via `expr:{brow:-0.9}`; `tilt` head turn.
- Brahma: `hd:{l,r,b,t}` sprouts the left, right, back and top faces on cues.
- Coded cast: shiva, vishnu, brahma (4 faces), daksha, narada (veena prop), manu, brahmi, adishakti, sati, prasuti, diti, danu, asikli, villager, villager_w, kumara (child), jaya, vijaya, kashyapa, indra, surya, chandra, hiranyaksha, hiranyakashipu, ravana, rishi0-6, madhu, kaitabha.
- `episodes/epNN/action_plan.json` (written by the action-director agent) is merged into the shots by build_shots.py.
- Act easing: `acts[i].e` = 'spring' (overshoots and settles, good for arrivals and bows) or 'antic' (a small wind-up the opposite way first). `talk:<0..1>` on a figure opens the mouth in a speech rhythm and adds a slight head sway while the shot plays.
- Policy: painted cut-outs (img) only for characters who stand or appear without acting (e.g. demons, guards, crowd devas); anyone who acts is a coded rig.
