# Bright palette (EP7 and later only)

Owner decision: future episodes use a BRIGHT look. EP6 stays as rendered (earthy).

Rules
- Backgrounds: clean sky blues, fresh greens, warm gold / pink sunsets. No brown or olive wash.
- Grade: lighter, more saturated, cleaner; low grain, no brown tint.
- Far depth layers still fade (2-3 layers), but toward light blue / pale gold, not grey-brown.
- Keep from the reference style: leaf-cluster trees, layered haze, paper texture on characters, thick outlines, glow layers on sunsets.
- Engine, timeline, subtitles, camera, animation stay unchanged.

Implementation (do NOT change engine files while an EP6 render is running):
- Add an opt-in `palette: "bright"` field in episodes/epNN/episode.json, read by engine/paper_scenes.js and the grade in engine/main.js.
- Default (no field) = current earthy look, so EP6 re-renders stay identical.
- Ask the owner for 2-3 frames of a bright video to match exact colours before building.
