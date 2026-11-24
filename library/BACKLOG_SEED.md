## Standing roadmap (engine, priority order)
1. Side/back views of characters (true turn instead of the paper flip `turnc`).
2. Mouth shapes driven by word timings (closer to lip-sync than `talk`).
3. More animals (cow, lion, deer, Garuda, serpent as a character) and a quadruped walk.
4. More scene objects (river bank, ashram hut, chariot, throne room, battlefield) as paper OBJ entries.
5. Speed: cache static layers per shot (render is ~6 h for 8 min on 4 cores).
6. Pixel QA: automatic face-visible and subtitle-overlap check on rendered frames.
7. Vertical 9:16 reel renderer (chapters A/B/C from beats.json `reel`; framing window, subtitle safe area, end card: guides/BEATS_SCHEMA.md "Reels").
8. Cue-id anchors in shot briefs (`{"beat":"B07","cue":"flower_falls"}`) resolved per language; English align (`build/epNN/en/timings.json`) and render.
