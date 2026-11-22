# EP6 scene brief: "Why Does No One Worship Brahma?"

Machine-readable twin: `episodes/ep06/shot_plan.json` (221 shots, avg 2.74 s, range 1.3 to 6.1 s). Every shot is anchored to a spoken word and time from the provisional `voice_timeline.md` and will be re-timed to the owner's voice.

## Design rules applied
- Characters: coded jointed rig only (brahma, vishnu, shiva, daksha, narada, indra, surya, chandra, kashyapa, rishi1-4, madhu, kaitabha, villager, villager_w, kumara, hiranyaksha as the stand-in asura). No `img`/`lib_*` people.
- Faces: full figures stay at y 560 to 690 with s 0.3 to 1.5. Head close-ups use head:true at y 335 to 340, s 1.4 to 2.2. Tiny figures sit at y 590 to 650 so a tilt-up or pull-out never crops them. I checked each one against the builder's crown/chin formula.
- No hearts, stars or sparkles. The "heart" line in B15 is only a plain warm glow.
- Backgrounds are coded only: vista (dusk, blue day, pale morning, red), cloudscape (dawn pink, blue day, dusk, grey-blue sorrow), earth (digging), pillar (with `ct` crack in B11), cosmos in six colour variants, plus storm, voidR, sea, amber, kailash, palace, dusk, plain. No `bgp_*`.
- Gemini objects used only where code would look worse: `flower_petals` (stand-in for the ketaki), `crown_gold`, `sudarshan_chakra`, `om_symbol`, `lightning_*`, `ground_crack`, `smoke_plume`, `energy_swirl`, `whirlpool_churn`, `magic_circle`, `halo_ring`, `divine_rays`, `palace_gate`, `havan_kund`, `boulder`, `mandara_mountain`, `wave_ocean`, `water_splash`, `cloud_*`.
- Camera never repeats the same move in consecutive shots. Roll or dutch tilt is used only for instability (quarrel, dizziness, B05). Shake 5 to 8 appears only on impacts (pillar eruption, pillar crack, Shiva's "Liar!", trident strike).
- Staging: heroes face right (flip 1); threats and the one being addressed face left (flip -1). Where two faces talk, the speaker's face is the larger one.
- Anger is red eyes plus heavy brow (`expr.brow` -0.9) with thunder bolt images in the background. No red crack line.
- Subtitle band y>590: faces and key action stay above it. Only feet, ground effects and fire bases go lower.

## Colour script
| Beat | Idea |
|---|---|
| B01 | Hook: near-black, one warm point (egg, pillar, flower), a red glow on "lie" |
| B02 | Gold (Brahma), blue (Vishnu), pale ash (Shiva), then rising red as the quarrel builds |
| B03 | Dusk saffron for Brahma's pride, cool blue for Vishnu's calm; heads cut on dark plains |
| B04 | Brahma's body: violet and rose cosmos with gold, wide worlds (sea, mountains, green valley, womb, elements, void) |
| B05 | Vishnu's body: blue and gold infinity, galaxies, clocks, countless eggs, kaleidoscope, green stalk, gold lotus |
| B06 | Muted grey to wrath red, then the gold pillar |
| B07 | Alternating: earth browns (boar) and white-blue sky (swan) |
| B08 | Dusk violet turning dark red as ambition takes hold |
| B09 | Night blue for the flower, ember brown for Brahma's persuasion |
| B10 | Amber triumph, blue humility, a red glow starting at the pillar's foot |
| B11 | Pillar cracks, gold Om, flames go red, Shiva with thunder behind |
| B12 | Red to amber as anger turns to explanation; the Jyotirlinga is gold |
| B13 | Storm red for the verdict, calm green valley, empty courtyard, amber for the flower rule |
| B14 | Grey-blue sorrow, then Daksha's crimson |
| B15 | Calm dusk, warm gold teaser |

## Beat by beat (shot ids refer to shot_plan.json)
Notation `t word` is the anchor from the timeline.

**B01 Hook (fast, mysterious).** Wide, human-scale and detail shots are all present.
- b01_1 0.09 ब्रह्मा: Brahma on lotus, four faces open on "ब्रह्मांड" 1.17, the egg appears.
- b01_2 2.82 फिर: lone Brahma, rishis walk past; light dims on "नहीं".
- b01_3 6.07 जवाब: head close-up, red glow on "झूठ".
- b01_4 8.29 और: ketaki flower insert (witness).
- b01_5 11.62 यह and b01_6 14.01 स्तंभ: pillar wide, light flares at top and bottom on आदि and अंत.
- b01_7 18.47 और: Shiva in storm, name on "शिव" 19.28.
- b01_8 21.40 सुनाया: Shiva (high) and bowed Brahma (low).

**B02 Three gods and the quarrel (slow, then rising).**
- b02_1 to b02_5: the three gods, then each in his own colour and name pill on "ब्रह्मा", "विष्णु", "शिव".
- b02_6 to b02_7: the question "कौन बड़ा?", then fire between the rivals on "आग".
- b02_8 to b02_11: devas receive the news, run in (walk), see the rivals.
- b02_12 to b02_14: face-to-face heads, voice rings on "आवाज़ें", red sky on "ग़ुस्सा".

**B03 Dialogue (anger, tension).** Two coded figures with eye contact, intercut with head close-ups.
- Brahma left (flip 1), Vishnu right (flip -1); Brahma walks past on "ब्रह्मा" 65.27.
- Vishnu is cool blue; Brahma red-brown; Vishnu's world-in-hand on "नाज़ुक".
- Memory insert on the sea for "मधु"/"कैटभ", chakra on "मारा".
- Closes on both raising fists, shock ring on "कैसी".

**B04 Vishnu enters Brahma (grand).**
- Brahma opens arms ("शरीर"); Vishnu walks into him and fades out on "भीतर/गए".
- From 123.62 "दस": cosmos with swirling galaxies and the text "दस लाख लोक".
- Worlds, one per phrase: sea ("समुद्र"), mountains with a long tilt ("पर्वत"), living valley ("साँस"), seed of life ("जीव"), elements ("तत्व"), the void with a faint secret ("राज़"), "ख़ालीपन" filling with light on "भ्रम".
- Vishnu steps out, folds his hands on "सचमुच", then opens his arms for the reverse challenge on "झाँकिए".

**B05 Brahma enters Vishnu (awe, then panic).**
- Brahma walks in and fades; frozen, with faces sprouting on "थम".
- Infinity sign on "अनंत", ten swirling galaxies on "आकाशगंगाएँ", giant planet, constellations (threads and orbs), three clocks on "बीता/आता/आने", countless eggs.
- Head close-up with dizzy dutch tilt, kaleidoscope rings, Vishnu's serene face as the Infinite.
- Panic with a flee pose and walk, then the green stalk (beam rising) and the navel lotus. Brahma's faces open again on "प्रकट".

**B06 Weapons and the pillar (fast, thunderous).**
- Heads in dispute; level scales on "बराबर".
- Weapons rise on "हथियार" (chakra + fire circle); devas back away (flee + walk).
- Pillar bg erupts on "स्तंभ" 239.33 with shake 5; tilt-ups on "ऊपर/नीचे"; extreme wide on "छोर".
- Devas set the condition; Vishnu looks down on "जड़" and Brahma up on "चोटी"; both bow on "मान".

**B07 Boar and swan (thrilling).** Alternating earth and sky.
- b07_1 to b07_2: Vishnu crouches in smoke, then digs, sinking in the earth bg (ground crack).
- b07_3 to b07_4: Brahma lifts his arms, then rises through the cloud decks.
- b07_5 shows both on the pillar; b07_6 to b07_9 alternate earth and sky; b07_10 to b07_12 show the endless pillar.
- b07_13 to b07_15: the tired swan sees petals fall; the ketaki enters on "केतकी" 296.21.

**B08 The flower and the thought (dangerous).**
- Flower held in the beak (hold pose), then speaks on its own.
- "ऊपरी ऊँचाइयाँ" echoes around him; extreme close-up.
- Flower gets a halo, a crown (victory) and a smile. The sky reddens on "चाहत".

**B09 Persuasion (tense).**
- Alternating flower inserts and Brahma close-ups.
- The golden "महानता" glow on 367.35; the flower sags, then nods on "गई".

**B10 The lie (sly, then triumphant).**
- Descent, Vishnu waiting with devas, bows on "झुकाकर".
- Brahma's four faces open one by one on "चारों/मुखों/मिलकर"; flower offered, hollow ring when it speaks.
- Vishnu folds his hands on "जोड़" while a red glow starts at the pillar base.

**B11 The pillar cracks (explosive).**
- Silence 409.01, crack on "चटक" 411.24 (bg pillar `ct`, shake 7).
- Gold Om with rings on "ओम"; flames red on "लाल".
- Dark silhouette on "धुंध", Shiva revealed on "शिव" 420.32 (red eyes, thunder in the background).
- Pointing on "उँगली"; "झूठे!" head close-up with two thunder bolts on 426.16/426.63.
- Reaction heads on "सब सन्न".

**B12 Jyotirlinga (grave).**
- "शिवलिंग" 438.65 and "ज्योतिर्लिंग" 441.02 name pills, halo and rays.
- Infinity and a huge circle on "परब्रह्म"; blinded faces on "इंद्रिय".
- Scale shot of two specks on "छोटी"; the three gods equal under threads of light on "बराबर".
- Anger returns on "ब्रह्मा", then Brahma kneels on "हरेगा".

**B13 Judgement (firm, heavy).**
- Trident raised on "त्रिशूल" 475.29, struck on "मारा" 476.32 (shake 8).
- Calm "यह श्राप नहीं है"; green valley for "प्रकृति".
- Devas walk away leftward on "नकारेंगे"; lamps die in the empty courtyard on "पूजा".
- Thunder on "गरजे", flower withers on "झूठी"; ketaki over the havan kund, then a devotee with the "ban" icon on "नहीं".

**B14 The answer and Daksha (still, deep).**
- Lonely Brahma on lotus; world-lights drawn away on "छीन".
- Fear head on "डर"; Vishnu in light against Brahma in shadow on "ठीक वहीं".
- Shrinking Brahma on "वही"; Narada's curse on "श्राप", fifth head on "पाँचवाँ", flower on "झूठ".
- Many temple gates, then one dim gate on "गिने-चुने".
- Shiva walks away; Daksha revealed by a pan on "घूर", his name on "दक्ष" 562.77; tears and red glow; trident emblem on "काटा".
- The red wave and the crimson tide closing the frame on "निगलने".

**B15 Audience question and teaser (calm).**
- Brahma looks at us; two choices (bowing Vishnu in light, shadowed Brahma with flower) on "सच" and "झूठ"; "आपका जवाब?" on "कमेंट".
- Teaser: an asura silhouette brightens on "असुर" 594.71; warm glow on "दिल"; he opens his hands to petitioners on "ना"; dims on "हरा".

## Pacing notes
- Fast sections where merging may be needed at a faster voice (+15 to 20 %): B02 b02_13 to b02_14 (2.2 s and 3.3 s), B06 b06_6 to b06_8 (3.2 s, 1.35 s, 2.9 s), B07 b07_1 to b07_4 (1.9 s, 1.7 s, 1.9 s, 2.5 s), B11 b11_2 to b11_3 (1.7 s, 1.9 s), B13 b13_1 to b13_2 (1.9 s, 1.6 s), B04 b04_7 (1.6 s). If a shot falls under 1.0 s, merge it into the next one.
- Longest shot is b05_13 (6.07 s, intentionally held: the Infinite speaks and the text builds). Keep it under 6.5 s.
- Pauses used for cuts: 1.69 s before B02, 1.77 s before B03, 1.68 s before B04, 1.74 s before B05, 1.68 s before B06, 1.65 s before B07, 1.76 s before B11, 1.79 s before B12 and B13.

## Asset and feature requests
A. **Boar form for Vishnu** (B07 b07_1, b07_2, b07_6, b07_8). No boar exists. Request a coded `boar` effect or a Gemini `varaha` image (dark-green boar with tusks, digging) to play behind or over the Vishnu rig, then drop the rig to a smaller silhouette. Today the plan shows a crouch in smoke and a digging pose in the earth background.
B. **Swan form for Brahma** (b07_3, b07_4, b07_9, b07_13, b08_1, b08_x). Same: a coded `swan` or Gemini `hamsa` image (white swan, wings spread) that can carry Brahma's head, with the flower as a beak prop in B08.
C. **Ketaki flower image** (B01, B07 to B10, B13, B14, B15). `flower_petals` is a placeholder. A white-yellow screw-pine bract with one long pale petal would read correctly; the plan uses the name `ketaki_flower` in notes, but the file name in the plan is still `flower_petals`.
D. **Victory key** (b08_12 "चाबी"): small coded `key` icon for the golden key of victory; currently a crown stands in for it.
E. **Shivalinga column** (B12): optional coded `lingam` effect (oval top on the pillar) to read as a shivalinga on "शिवलिंग"; for now the pillar background plus the name pill carries it.
F. **Brahma standing with hd:t** (b14_12 fifth head): confirm the top face draws above the crown; if not, lower y by 40.
G. **Pose stand-in asura** (B15): `hiranyaksha` is a placeholder for the next episode's generous asura; replace once the new character exists.
H. **Action-director notes**: all `acts` blocks are staged with poses only (namaste, bow, point, raise, open, plead, flee, lunge, hold, sit). Gesture detail, eye-line on "देखा/घूर", and walk starts are left to the action-director.
