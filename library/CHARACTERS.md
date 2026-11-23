# Cast (coded paper-cut rigs in engine/v2_cast.js; exact names: `python3 studio/engine_vocab.py`)
Sheet for any of them: `python3 studio/cast_sheet.py <names> [--out DIR]` → <name>_faces.jpg (neutral, angry, sad, surprised, joy), _poses.jpg (stand, walk, bow, point, pray) and, for story forms, _forms.jpg. Groups: `devas`, `jyotirlinga`.

| name | identity cues |
|---|---|
| brahma | 4 heads (3 visible + sprouting `hd` faces), white beard, red dhoti, book/kamandalu, lotus seat |
| vishnu | blue, 4 arms (chakra, conch, mace, lotus), yellow dhoti, kirita without horns; hayagriva = horse-headed form; vishnu_rest = reclining on Shesha |
| shiva | ash-blue, jata with crescent, third eye + tripundra, tiger skin, Vasuki, trishul (+ rage form). `point` / `rpoint` point with the LEFT hand (trishul stays in the right): use flip:-1 to point to the right |
| daksha, manu, indra, surya, chandra, kashyapa, narada (veena), kumara (child sage) | crowns/hair/cloth per spec |
| adishakti, sati, brahmi, prasuti, diti, danu, asikli, villager_w | sari + choli colour sets, bindi |
| rishi0-6 | the seven sages (vasishtha, marichi, atri, angirasa, pulastya, pulaha, kratu): distinct beard, hair, cloth, prop |
| jaya, vijaya | door guardians, helmet, mace |
| madhu, kaitabha, hiranyaksha, hiranyakashipu, ravana | asuras: horns/wild hair, red eyes, armour, weapon |
| villager | turban, gamcha |
| harihara, ardha | fused forms (half Vishnu/Shiva; Ardhanarishvara) |
| boar, swan | animal forms, paper-cut: Varaha = slate-blue boar, ivory tusks, gold crown + necklace with red gem (pose dig/run); Hamsa = white layered-feather swan, gold crown, red-gold neck band (Brahma), beak tip at (210,-196)*s, `rot` tilts it, `glide` slows the wings |
| agni, vayu | devas crowd (EP6): Agni = ember skin, flame-crest crown, red dhoti, fire halo; Vayu = sky-blue dhoti, white wind scarf, fan crest |
| ketaki | the speaking ketaki flower: cream-gold bracts, gentle face with bindi on its heart (emo/mood/talk work), `wither` 0..1 or `wc`/`wd` cue, `fall:1` drops petals; x,y = base of the flower |

New character checklist (character-designer): spec in CAST + name in V2NAMES, sheet rendered and looked at, line added here.
