# What the engine can render (verified on stills, Nov 2026)

Everything is drawn by code in the browser canvas (paper-cut look: gradient fill, soft drop shadow, ink edge). No images.
The exact names below are read from the engine by `python3 studio/engine_vocab.py`; if a name is not printed there it does not exist.
Canvas: 1280x720 plan space (CX=640), rendered at 1.5x = 1080p. Subtitles live in the band y > 590: faces must stay above it.
Reels (9:16, `format:"vertical"`): the same 1280x720 frame shown through a portrait window (405 wide at zoom 1) on the focus figure, or a 2-figure `stack`; output 720x1280 / 1080x1920. Shot key `vert` (brief `vertical`): guides/BEATS_SCHEMA.md (Reels).

## Files
`engine/art.js` (helpers, grade/post) · `engine/paper_kit.js` + `library/characters/shiva/shiva_v2.js` + `engine/v2_cast.js` (character rig, CAST)
· `engine/main.js` (timeline, word cues, subtitles, camera, transitions) · `engine/scenes.js` (scene, figures, classic fx)
· `engine/v2_scenes.js` (yagna/kailash/garden/cosmicsea backgrounds, egg/books/gunas/... fx) · `engine/paper_scenes.js` (paper backgrounds,
paper OBJECTS, depth layers, default foregrounds) · `engine/paper_fx.js` (24 paper props/effects, scene assembly). `studio/build.py` joins them.

## Shot (in shots.json, written by build_shots.py from shot_plan.json)
- Starts on a spoken word; `cues` = words inside the shot; anything with `c:i` fades in on cue i over `d` seconds.
- `cam:{from:{z,x,y,r},to:{...}}` eased over the shot; z 1.0 wide … 1.3 close (higher only for head close-ups), x/y ±120, r ±0.05. `shake` 0-8, `tilt`.
- `grade`: cel warm red night pal cool dark amb earth void, or an rgba() tint.
- Transition into the shot: `tr`: fade (default dissolve) | wipe (torn-paper edge sweeps left to right) | iris (circle opens) | flash (white bloom); `dx` = seconds; `dx:0` = hard cut.

## Backgrounds (`bg:{k:...}`)
vista (sky, ridge colours, river, trees, ground) · cloudscape · cosmos (rgb, spin) · pillar (fire column, `ct` crack cue) · storm (r 0..1)
· voidR · plain · amber · dusk · earth (strata) · sea · kailash · palace · yagna (fire 0..1) · garden · cosmicsea · cel · night · moon · dawn.
- Far ridges of `vista` are blurred and hazed; trees on ridges are the paper tree object.
- Default foreground (in FRONT of the actors, blurred, darker, bottom corners only) for vista, kailash, cloudscape, amber, dusk, garden, storm, palace. Turn off with `bg.fore:false`; replaced automatically when the shot has its own `near` layer.
- Background change on a word: `bg2:{k:...}` + `bgc` (cue index) + `bgd` (seconds) cross-fades to a new background; or `bgTo:{param:value}` + `bgc`/`bgd` tweens numeric parameters (e.g. storm `r` 0→1, yagna `fire` 0.2→1).

## Depth layers (`layers`, owner rule: 2-3 planes per scene)
`layers:[{d:'far'|'mid'|'near', par, fog, haze, blur, dark, items:[{o, x, y, s, ...}]}]`
- Defaults: far par .2 fog .55 blur 1.2 (+ haze band) · mid par .55 fog .22 · near par 1.35 blur 1.6 dark .55 (drawn in front of the actors).
- `fog` mixes colours toward `haze` (lighter/bluer = farther); `dark` mixes toward a silhouette colour; `blur` = shallow focus.
- Objects (x, y = base on the ground, s = scale): `tree` (kind round | banyan | palm | pine, col, trunk, flowers) · `rock` (col, moss)
  · `cloud` (col) · `mountain` (h, w, col, snow:false, trees) · `pillar` (h, w, col) · `wall` (w, h, col: palace wall with arches) · `shrub` (col, flowers) · `hill` (w, h, col).

## Characters (coded rigs; names from engine_vocab: cast)
brahma (3 visible faces + `hd` sprouting faces), vishnu, hayagriva, vishnu_rest (reclining on Shesha), shiva, daksha, manu, narada (veena), adishakti, brahmi, sati, prasuti, diti, danu, asikli,
kashyapa, indra, surya, chandra, agni, vayu, kumara (child sage), jaya, vijaya, villager, villager_w, madhu, kaitabha, hiranyaksha, hiranyakashipu, ravana, rishi0-6, harihara, ardha (Ardhanarishvara), boar, swan, ketaki (speaking flower: emo/mood/talk, `wither` or `wc`/`wd`, `fall`).
Figure keys: `x,y` (feet), `s`, `flip` (1 faces right, -1 left), `pose`, `head:true` (bust close-up), `aura`, `dark`, `fo/fd` fade-out.
- Poses: stand namaste open point rpoint raise plead bow hold flee lunge sit sitpray lie lie2 (+ shiva calm/rage). Shiva points with his LEFT hand (flip:-1 to point right); rpoint = furious lunge + point. Blend on a word: `acts:[{c, pose, d, e:'spring'|'antic', emo, mood, tilt}]`.
- Faces: `emo` preset = calm joy anger rage sad grief surprise fear shame pride doubt devotion (on the figure or on an act). Fine control `mood:{smile, sad, surp, anger, mouth, lx, ly, blink, turn}`
  (lx/ly = where the eyes look -1..1, turn = head three-quarter turn -1..1). Anger = red eyes + heavy brows + frown (no fangs). Sad adds a tear.
- Movement: `walk:<speed>` + `vx` (walk while drifting) · `walkTo:{x, c, d, sp}` walks to x starting on cue c, legs swing only while moving
  · `mx,my,mc,md` slide on a cue · `bow` (lean angle) + `bc,bd` · `kneel` + `kc` · `tilt` (head) · `talk:0..1` (mouth + head sway).
- Turning round: `turnc:<cue>` + `turnd` flips the figure (paper-puppet turn) on that word.
- Character sheet for approval: `python3 studio/cast_sheet.py <names>` → full figure, 5 faces, 5 poses.

## Paper props / effects (`{"t":"pfx","k":<name>, x, y, w, alpha, c, d, par, spin, vx, vy, grow, rot, flip}`)
boulder · cloud_white_cluster · crown_gold · divine_rays · embers · energy_swirl · flower_petals (= the ketaki flower; `wither` 0..1 or `wc`/`wd` cue, `fall:1` petals drop, `glow`)
· ground_crack (grows with its fade-in) · halo_ring · havan_kund (with fire) · light_beam · lightning_bolt_a · lightning_forks · magic_circle (yantra)
· mandara_mountain (tall peak) · mist_wisps · om_symbol · palace_gate (temple gateway) · red_energy_pulse · smoke_plume · sudarshan_chakra
· water_splash · wave_ocean · whirlpool_churn. Old plans that say `{"t":"img","src":name}` or `fximg` are converted to pfx automatically.

## Classic effects (`fx` in front, `fxb` behind the actors)
text, name (name plate), glow, orbs, petals, shock, flash, bolt, crack, ribbon, beam, light, flames, fire, pillar, infinity, scales, trident, tears,
threads, outline, egg, books, gunas, element, lotus, bluemountain, waterfront, vaikuntha, clock, dim (used in EP6). Older ones still in the code but
not re-checked in this pass (render a still before relying on them): skull, arrow, frost, icon, asuras, ban, body, cycle, flame, kids, lotusI, person, vortex. Required params: threads x,y,to · orbs items · beam x,y,len · infinity x,y · text s,x,y,size.
Banned by the owner: hearts, stars, sparkles.

## Not possible (ask Opus to build it before planning a shot that needs it)
true side/back views of characters, lip-sync to phonemes, running/fighting choreography beyond poses, crowds with individual motion,
water/cloth simulation, 3D camera, animals other than boar and swan.
