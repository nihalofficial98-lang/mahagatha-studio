# How Episode 01 Was Made: Full Technical Walkthrough

**Deliverable:** one 9 min 47 s, 1080p, 24 fps animated Hindi video with word-synced subtitles
**Cost:** zero (all tools free, no paid APIs)
**Where it ran:** a temporary Linux cloud container (4 CPU cores, no GPU)

---

## 1. The goal and the constraints

You asked for an automated, free way to turn a script into a stylised animated video, for a series of Puranic stories. The constraints shaped almost every decision:

| Constraint | Consequence |
|---|---|
| Must be free | No paid video AI, no paid voices, no paid stock libraries. |
| Hindi narration | Needed a Hindi-capable voice and a proper Devanagari font in the video. |
| Specific look (your reference screenshots: flat 2D cutout characters, rim-lit, layered painted backgrounds, cinematic lighting) | Ruled out stock footage and generic text templates. |
| 6–10 minutes per video | Drives script length (≈1,100 Hindi words) and render time. |
| You record the voice yourself | The video must later be re-timed to your audio, so the pipeline is built around *timings*, not around a fixed voice. |
| Cloud sandbox with a restricted network | Several free services were unreachable and needed workarounds (section 3). |

## 2. The options I considered, and why I chose the one I did

| Option | Verdict |
|---|---|
| Free text-to-video AI (Wan, LTX, CogVideoX on free Kaggle/Colab GPU) | Too slow, 5–10 s clips, inconsistent characters, hard to automate. Kept only as a possible future add-on. |
| Stock footage (Pexels) + captions | Doesn't match your illustrated style. (I did allow Pexels hosts in the network settings early on, but never used them.) |
| AI-generated images with a flat-vector LoRA | Best fidelity to your reference, but characters drift between shots and I had no GPU or access to Hugging Face from the sandbox. |
| Text/kinetic-typography templates | My first prototype idea, dropped as soon as you showed the mythological style. |
| **Code-drawn 2D puppets and painted scenes, rendered from a headless browser** | **Chosen.** Fully free, deterministic, consistent characters across all shots, real animation (blinking, brows, bow draw), fully automatable. |

The chosen approach is "a film that is a pure function of time": one function `seek(t)` draws the exact frame for any time `t`. Because it is deterministic, frames can be rendered in any order, in parallel, and re-rendered identically.

## 3. Environment, network and the workarounds I needed

**Tools already in the container:** Python 3.13, Node 22, ffmpeg, Chromium with Playwright (used from Node).

**Network:** outbound access goes through a proxy with an allow-list.
- PyPI and npm worked. Hugging Face, Pexels, Bing speech, and jsDelivr initially did not.
- I asked for (and you approved) allow-listing `speech.platform.bing.com`, `api.pexels.com`, `videos.pexels.com` and `images.pexels.com` through the environment settings.
- **Gotcha:** even after allow-listing, `edge-tts` failed with a DNS error, because its HTTP library (aiohttp) ignores the proxy environment variables. Fix: pass the proxy explicitly (`Communicate(..., proxy=os.environ["HTTPS_PROXY"])`) and point `SSL_CERT_FILE` at the sandbox CA bundle.
- Hugging Face and Azure CDN stay blocked. That blocks Whisper models, which matters for the next step (re-timing to *your* voice, see section 14).

**Fonts:** the container had no Devanagari font. I installed `@fontsource/noto-sans-devanagari` from npm and copied the two `.woff2` files (weights 400 and 700) into `engine/fonts/`, loaded with `@font-face`. Chromium's canvas then shapes Hindi conjuncts and matras correctly.

## 4. Pipeline overview

```
PDF (21 stories)
  └─ pdftotext → one text file per story (source/story_NN.txt)
        └─ my own original Hindi script per episode  (episodes/ep01/script.md)
              ├─ emotion-directed version for you     (script_emotion.md / script_clean)
              └─ parse_script.py → beats.json (25 beats, 80 expressive segments)
                    └─ tts.py (edge-tts, word-level timings) → audio + timings.json
                          └─ render_ep.js (3 parallel Chromium workers)
                                ├─ engine.html: seek(t) draws every frame
                                │     (shots + cuts from shots_ep01.json, subtitles from timings)
                                └─ ffmpeg: frames → H.264, concat parts, mux voice
                                       └─ renders/ep01_draft.mp4  (110 MB, 1080p)
```

## 5. Step 1: reading the book and planning episodes

- The PDF was *Mahagatha: 100 Tales from the Puranas* (stories 1–21, 88 pages). `pdftotext -layout` extracted ≈19,500 words; a small script split it per story using the table-of-contents headings, and measured each story's length (329 to 1,911 words).
- **How I used it:** only to confirm *which events happen*. The Hindi scripts are my own retelling, with my own structure and wording. They are not a translation of the author's text.
- **Episode grouping:** a video needs about 850–1,350 Hindi words. Short stories were paired by theme as "Part 1 / Part 2"; long ones stand alone. Result: 21 stories → 13 episodes (`episode_plan.md`). Episode 01 pairs story 1 (creation) and story 2 (Madhu and Kaitabha), because the first ends on a cliffhanger that leads into the second.

## 6. Step 2: writing the script

- Structure: a hook (the "nothing existed" opening), two labelled parts, a mid-story cliffhanger, escalating dramatic beats, a reflective close and a teaser for Episode 2.
- It is divided into **25 numbered "beats"**. A beat is one narrative unit and later becomes the unit of timing (each beat's audio length drives its scene length).
- **Length discipline (a mistake I corrected):** the first draft was ≈1,240 words. Rendered with the guide voice it would have run 11.7 minutes, over your 10-minute cap. I cut ≈110 words of low-value lines (a subscribe plug, a cycle-of-creation aside, and so on) → ≈1,100 words. Rule going forward: about 1,100 words for ≤10 minutes.
- Emotion direction for your voice session was added afterwards as a separate document (mood, pace, voice quality, pauses, stressed words, and tag-annotated paste-ready text).

## 7. Step 3: the voiceover (guide voice and timings)

I used **edge-tts** (Microsoft's free neural voices), voice `hi-IN-MadhurNeural`. It streams audio *and* `WordBoundary` events, which give the exact start/end of every spoken word. Those timings are what make the subtitles and cuts sync.

**Making the guide voice expressive:** the free Hindi voices have no emotion styles, so expression is created through prosody:
1. `parse_script.py` reads each beat's cue ("[धीमे]", "[फुसफुसाकर]", "[क्रोध]", …) and maps it to **rate / pitch / volume** (for example whisper = slower, −6 Hz, quieter; anger = faster, +3 Hz, louder).
2. Each *line* becomes a separate segment, synthesised independently, with its own pause afterwards. The last line of a beat is slightly slower.
3. Segments are padded with silence (`ffmpeg apad`), concatenated per beat, and word timestamps are shifted by each segment's offset. Total: **25 beats, 80 segments, ≈4 minutes of synthesis**.

**Problems found and fixed:**
- `rate="0%"` is rejected by edge-tts (it requires a sign: `+0%`). It crashed beat 12. Fixed by always formatting signed values.
- The first pacing made the episode 13 minutes. I lightened the slow cues, shortened pauses, and trimmed the script → 10.39 minutes.
- To land under 10 minutes without another full regeneration, the render step applies `atempo=1.06` (pitch-preserving) to the voice and divides every timing by 1.06 → **9 min 47 s**.

## 8. Step 4: the animation engine (`engine/engine.html`)

A single HTML page, drawn with Canvas 2D, built by `build_engine.py` from three parts (base engine, `ep_scenes.js`, and timeline code).

**Resolution and sharpness**
- Logical drawing space is 1280×720; the canvas is 1920×1080 with a ×1.5 transform, so everything stays vector-crisp.
- Characters are drawn to a 2× offscreen canvas and scaled down, which keeps edges clean.

**Layers and camera:** background layers have a depth value, which gives parallax when the camera moves. Each shot has its own slow push or pan.

**Character rig (`drawChar`)**
- A skeleton-lite puppet: legs, dhoti (swaying cloth), torso with sash, head, and two arms solved with **2-bone inverse kinematics** so hands reach targets for each pose (idle, bow draw, point, plead, folded, greet, fist).
- **Expression system:** eyebrow tilt (worried ↔ angry), eye openness, iris look direction, automatic blinking, mouth (smile ↔ frown), open mouth that animates while "talking", head tilt, and torso lean.
- **Specs per character:** colours, crown/horns/fangs/antennae/horse head. Cast so far: Abhimanyu (earlier sample), Yudhishthira, Drona-style, Vishnu, **Hayagriva** (horse head), **Madhu** (violet asura), **Kaitabha** (green asura with antennae).
- **Lighting:** a rim-light is made with a hard canvas shadow offset (colour = light colour, blur 0), then a `source-atop` gradient pass adds warm light from the side and darkening toward the feet. This is what makes flat shapes feel lit like your reference.
- Separate hand-drawn figures: **Brahma** (four heads, four arms, kamandala and mala), **Vishnu reclining on Shesha** (five-hooded serpent, navel lotus that grows and opens to reveal Brahma).

**Environment systems**
- Ocean (animated wave lines and sun reflection), clouds, sun glow and god-rays (additive blending), moon, stars, dust, falling petals, embers, mist, splashes, birds, flags, torches, a bonfire, a palace with lit windows, and trees with red flowers (the last few were built for the earlier Mahabharata sample).
- All motion is a function of time and a seeded random generator, so every frame is reproducible.

**Scene library for this episode (23 scenes):** void with a rising light point, Om with expanding rings, the three gunas orbiting then five element icons, Narayana on the waters, the golden egg and the lotus, the egg splitting into heaven/sky/earth, the Vedas rising, Madhu and Kaitabha emerging and growing, the confrontation, the lotus shaking and the Vedas falling, Brahma pleading, Nidra and the opening eyes, the 5,000-year battle (with a Devanagari year counter), the trick, the trap, the giant Vishnu and "मधुसूदन", the earth rising with twelve glowing plates ("मेदिनी"), the ominous ending, and the teaser card.

## 9. Step 5: subtitles

- Drawn on the canvas in `Noto Sans Devanagari` Bold, 40 px, over a bottom gradient.
- Words come from the TTS `WordBoundary` data. A line group breaks on: a beat change, a silence gap >0.25 s, or about 34 characters.
- The **current word is highlighted gold**, spoken words are bright, upcoming words are dim. Subtitles hide during long gaps.

## 10. Step 6: editing: making it "engaging" (shots, cuts, cutaways)

Initially each beat was one 25-second shot (23 shots). You asked for more scenes, so I added an **edit decision list** (`make_shots_ep01.py` → `shots_ep01.json`):
- Each shot now has a list of **cuts**. Every cut is a camera *focus*: zoom level plus a start and end centre point (for example a push-in on Brahma's worried face, then the asuras' faces, then wide again).
- The animation underneath keeps running continuously (it is driven by the parent shot's clock), so cuts feel like cutting between cameras filming the same live scene.
- Three **cutaway shots** were added: a starfield fly-through, glowing asura eyes and a wide-eyed shock close-up, and water ripples.
- Transitions: a 0.6 s cross-dissolve between different shots, a 0.14 s dissolve between cuts, fade-in at the start and fade-out at the end.
- Result: **23 shots → 87 cuts**, roughly one cut every 6–7 seconds.
- Focus centres are clamped so the camera never shows outside the drawn area.

## 11. Step 7: rendering

`render_ep.js` does the following:
1. Rebuilds the voice track: per beat, `atempo` then padded to the beat's length, then concatenated into `voice.wav`.
2. Splits the ≈14,100 frames into **3 equal ranges** and launches **3 worker processes**, each with its own headless Chromium at 1920×1080.
3. For every frame the worker calls `seek(t)`, takes a JPEG screenshot (quality 93) and pipes it into its own ffmpeg (`libx264 -preset veryfast -crf 21 -pix_fmt yuv420p`).
4. When all workers finish: ffmpeg concatenates the 3 parts without re-encoding (`-c copy`) and muxes the voice as AAC 192 kbps.

**Performance:** ≈36 frames per second in total, **572 seconds** wall-clock for the whole episode. Output: 110 MB, H.264 + AAC, 586.6 s.

## 12. Quality control process

I never rendered blind. At each stage I rendered still frames and built **contact sheets** (a small Pillow script tiles many frames into one image) to review.

Bugs caught this way:
- Eyebrows were mirrored (the "worried" brow looked angry): the inner end was on the wrong side of the face.
- A glowing orb sat behind the title text, and Brahma was cropped at the top of the lotus shot.
- A dark overlay bar appeared on the right edge of the plea scene; the year-counter label was far from its number; Kaitabha was cropped at the right edge.
- The teaser's trident overlapped the title.
- Two earlier sample issues: oversized flat clouds and a hazy "blurry glow" rim-light, both fixed in the engine.

After rendering, I extracted frames from the **final MP4** (not the engine) at four timestamps to confirm picture, subtitles and sync in the finished file, and checked codec, resolution, frame rate and duration with `ffprobe`.

## 13. Delivery problems (and what worked)

- Chat file cards didn't open for you at first.
- The **Google Drive connector** limits a call to ≈3.1 MB of file data, so large videos can't be uploaded through it, but scripts (text) can, converted to Google Docs from HTML.
- A published **Artifact** page can hold files up to 15 MB each, so it carries a 360p, 14 MB **review copy**. The full 110 MB file was sent as a chat attachment.
- The reliable long-term route for full-quality files is a **GitHub Release** (up to 2 GB per file).

## 14. What's built, and what's still missing for daily automation

| Built | Not yet built |
|---|---|
| Script → beats → timed guide voice → 1080p render, one command | **Re-timing to your own recorded voice.** Planned: speech recognition (Whisper) on your audio, matched to the script text so the *script's* words are displayed with *your* timings. Blocked today because model hosts are not reachable from the sandbox; needs one more network approval. |
| Cut-based editing, cutaway library, expression system | **Persistent storage.** This container is temporary. A private GitHub repo must be linked so a scheduled daily run can start from a clean machine. |
| 25-beat emotion script, paste-ready for AI voice tools | **Scheduled daily job and notification**, and an episode tracker page. |
| Review-copy and script delivery path | **A bigger character/location library** for later episodes (Shiva, Narada, Daksha, Sati, and so on). |

## 15. File map

```
/home/user/story-videos/
  episode_plan.md               21 stories → 13 episodes
  PROCESS.md                    the intended daily process
  source/                       PDF, extracted text, one file per story, index.json
  episodes/ep01/
    script.md                   final trimmed script with beat markers
    script_emotion.md           emotion-directed script + paste-ready versions
    script_clean.html           clean version uploaded to Drive
  engine/
    parse_script.py             script → beats.json (cues → prosody)
    tts.py                      beats.json → audio + word timings (edge-tts)
    ep_scenes.js                scene library, Brahma/Vishnu/Shesha, cutaways
    build_engine.py             assembles engine.html (1080p, rig upgrades, timeline, subtitles)
    engine.html                 generated; the page that draws every frame
    make_shots_ep01.py          the edit decision list → shots_ep01.json
    render_ep.js                parallel renderer + mux
    still_ep.js / sheet.py      still-frame and contact-sheet QA tools
    fonts/                      Noto Sans Devanagari (400, 700)
  build/ep01/                   beats.json, timings.json, audio, parts, logs
  renders/                      ep01_draft.mp4 (110 MB), ep01_review.mp4 (14 MB)
/home/user/hindi-video/         the earlier prototype (Abhimanyu sample, first engine)
```

## 16. How to reproduce Episode 01 from scratch

```bash
cd story-videos
python3 engine/parse_script.py episodes/ep01/script.md build/ep01/beats.json
SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python engine/tts.py build/ep01/beats.json build/ep01
python3 engine/make_shots_ep01.py
python3 engine/build_engine.py
node engine/render_ep.js build/ep01 engine/shots_ep01.json renders/ep01.mp4 3 24
```

## 17. Honest limitations

- Characters are clean flat puppets, not the richly painted look of the reference screenshots. Consistency and movement are good; detail is simpler.
- Action is suggested with camera moves, expressions, flashes and scale changes. There are no full walk cycles or sword choreography.
- The guide voice is synthetic. It exists so you can judge visuals and timing; your recording will replace it.
- Some shots (the giant Hayagriva) are a stylised compromise.
- The cut list is hand-authored per episode (by me); it isn't yet fully automatic from the script alone.
