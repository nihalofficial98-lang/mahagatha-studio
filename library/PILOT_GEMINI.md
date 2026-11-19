# Pilot: 1-minute test with Gemini image model ("Nano Banana")

Goal: judge whether AI-painted art (cut into parts and rigged) looks better than our code-drawn v2 characters.
Owner decisions: skip voice in videos (subtitles only), videos 8–10 min, review by numbered frame sheets BEFORE any render, 4K only after approval.

## Setup needed (owner does this once, then starts a NEW session on this repo)
Environment settings → Network secrets: host `generativelanguage.googleapis.com`, header `x-goog-api-key`, value = the Gemini key.
(The first key was pasted in chat — delete it in Google AI Studio and use a new one.)

## Pilot plan (≈1 min of video, based on EP3 B05–B07: Shiva meditating → rage → Vishnu faces him)
1. Shiva: painted calm + angry portrait (flat painted-vector style like the reference video), front view; owner design rules in library/feedback.jsonl (red glowing eyes, heavy brows, plain frown, NO fangs/face lines, only crescent moon on hair, tiger skin, third eye, ash lines, serpent, trident+damaru).
2. Split Shiva into parts (head, jata, torso, upper arms, forearms, hands, skirt, legs, trident) with transparent backgrounds; inpaint hidden areas.
3. Add a sprite-puppet renderer to engine (parts + pivots, same poses as engine/v2_cast.js).
4. Yagna hall as 3 depth layers (far wall, pillars, floor) for parallax.
5. Make a 1-minute subtitle-only test (720p) + numbered frame sheet; compare against the current code-drawn version.

Existing assets: engine/v2_cast.js (cast + glue), engine/v2_scenes.js (settings/effects), episodes/ep01 & ep03 (shots + scripts), studio/review_sheets.py (numbered frame sheets), library/characters/{shiva,vishnu}/ (approved sheets).
