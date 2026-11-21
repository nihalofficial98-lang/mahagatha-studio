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
