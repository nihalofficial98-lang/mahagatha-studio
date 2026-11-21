# What the sound engine can render (read before writing a cue sheet)

## Engine (studio/music.py today, studio/score.py when the sampled engine is ready)
Output: stereo 44.1 kHz WAV/MP3 timed to the episode timeline; mixed UNDER the owner's voice.

### Layers it can build
- **bed**: sustained pad / drone (tanpura-style drone, string pad, choir pad, organ pad), with swell in/out.
- **pulse**: heartbeat / taiko / dhol / pakhawaj / timpani patterns at a given bpm (patterns: heartbeat, march, gallop, syncopated, roll).
- **motif**: a short melodic phrase (list of scale degrees + rhythm) in a chosen instrument; can be transposed/varied when it returns.
- **arp/ostinato**: repeating figure over chords (strings ostinato, santoor/harp arpeggio, plucked tick).
- **riser / reverse swell / sub drop**: tension builders and releases.
- **hit / braam / impact**: timpani/taiko hit, brass braam, sub boom with tail.
- **sfx**: thunder (near/far), wind, fire crackle, water/flood, temple bell, gong, shankh (conch), ghungroo, damaru roll, footsteps, stone/skull clatter, magic shimmer, sparkle, whoosh.
- **ambience**: continuous background (yagna fire, Kailash wind, river, cosmic hum, night crickets).
- **silence**: explicit drop-out (all music stops, optional single sustained tone).

### Instruments (General MIDI names when the sampled engine is installed; otherwise procedural approximations)
strings ensemble, cello, violin, contrabass, tremolo strings, pizzicato, harp, flute (bansuri-like), pan flute, shehnai (Shanai), sitar, santoor (dulcimer/harpsichord-like), tanpura (plucked drone), veena (plucked), choir aahs, voice oohs, organ, french horn, trombone, tuba, brass section, timpani, taiko drum, melodic tom, tabla-like hand drums (woodblock/agogo/tom), tubular bells, tinkle bell, glockenspiel, celesta, synth pad.

### Modes / ragas (as note sets; the engine builds melodies from scale degrees 1–7)
bhairav, yaman, marwa, malkauns, darbari, todi, bhairavi, plus western: minor, phrygian, dorian, lydian, harmonic minor.

## Cue-sheet schema (sound_cues.json)
```
{ "episode": "04", "key": "D", "bpm_family": "slow|mid|fast",
  "leitmotifs": { "shiva": {"instrument":"french horn","mode":"malkauns","degrees":[1,3,4,1],"rhythm":[1,1,2,4]}, ... },
  "cues": [ {
     "id": "c01", "role": "bed|pulse|motif|ostinato|riser|hit|sfx|ambience|silence",
     "from": {"t": 71.20, "word":"काट"}   // PREFERRED: absolute seconds from voice_timeline.md plus the word | or {"beat":1,"line":0,"frac":0.0} when no timeline yet
     "to":   {"t": 74.80, "word":"दिया"},
     "instrument": "tremolo strings", "mode": "malkauns", "key": "D", "bpm": 72,
     "pattern": "heartbeat|march|gallop|roll|sustain|arp_up|arp_down|…",
     "chords": ["Dm","Bb","Gm","A"],          // one per bar, optional
     "degrees": [1,2,3,5],                    // optional motif notes
     "intensity": 0-10, "fade_in": 1.0, "fade_out": 2.0,
     "sfx": "thunder_near|thunder_far|wind|fire|flood|bell|gong|shankh|damaru|ghungroo|skull|shimmer|whoosh|boom",
     "duck_db": -5, "note": "why this cue is here (story point)"
  } ],
  "requests": ["anything the engine cannot do yet"] }
```
Rules: cues may overlap (layers). Keep average music intensity 3–6 under speech, up to 9–10 only in gaps/climaxes. Always list a "silence" cue before the biggest reveal word.
