# New coded characters: vishnu3, brahma3, narada3 (Opus test)

Sheets: `vishnu_sheet.jpg`, `brahma_sheet.jpg`, `narada_sheet.jpg`. Each sheet shows the old version next to the new one, 6 face expressions and 5 actions. Everything on the sheets was rendered by the real engine, using the scratch episode ep95 (`build/ep95/quick`).

## What was added (old cast untouched)
- `engine/v2_cast.js`: a new block between `/*V3BEGIN*/` and `/*V3END*/`. It adds `head3`, `hand3`, `drawHero3`, the crowns, the props and the cast entries `vishnu3`, `brahma3` and `narada3`. Five small glue edits connect it, and each one only branches when the name is one of the three new ones:
  - `poseOf` sends these three names to `poseOf3`.
  - `V2NAMES` has the three new names.
  - `v2fig` has a branch for them.
  - `v2head` has a branch for them.
  - `studio/build_shots.py` has the three names in `WHO`.
- Shiva, the shared `drawHead` and every older character are untouched.
- **Faces:** each character has its own face spec (`f3`), so the faces differ in:
  - eye width, how far the outer corner lifts or droops, eye height and the default lid cover
  - iris size, kohl flick, brow arch, thickness and asymmetry
  - nose length, width, hook or upturn
  - jaw and chin shape, lip colour, default smile and smirk
  - age lines, beard and earring type
- **Expressions:** `mood` (smile, sad, surp, mouth, lx, ly, blink) and anger (`expr.brow`, which sets `k`) now move:
  - the inner and outer brow points separately
  - the upper lid, and the lower lid on a smile, so the eyes smile too
  - the iris for gaze
  - the mouth corners
  - the mouth shape: open speech with teeth and tongue, an O for surprise, a frown for anger
  - Anger follows the owner rule: a red eye glow, heavy brows and a plain frown, with no fangs and no face lines.
  - A head yaw (`lx`, or the side faces) shifts and compresses the features to give a 3/4 turn.
- **Hands:** each hand has a palm, 4 outlined fingers and a thumb. The gestures are:
  - relax, open, point, fist (automatic when anger is high)
  - grip, used for the gada, lotus, kamandalu and veena
  - abhaya (blessing), joined-palm namaste
  - chakra on a raised finger, conch, book, mala
  - The gesture comes from the pose name (`P.g`), so `acts` blends switch it automatically.
  - New pose `bless` is available for these three.
- **Costume:**
  - A skirt-style dhoti with a pleated front fall, a border and hanging sash ends. Its hem follows the legs when walking.
  - Gold belt with a pendant, sacred thread, layered necklaces.
  - Vishnu: the Kaustubha gem, a knee-length vanamala, a tall tiered kirita, swinging pearl strings and kundalas.
  - Brahma: a maroon uttariya and three tall crowns. A fourth crown peeks out behind them, standing for the hidden fourth face.
  - Narada: a topknot wound with rudraksha, two malas, an ochre shawl, and a veena that he plays or slings on his back.
- **Motion:** these parts sway with time:
  - hair locks, beard tip, pearl strings
  - veena tassel, sash ends, garland, dhoti hem
  - Breathing and blinking use a different phase for each character.
- **Bow:** in front view this is drawn as a bow, not a sideways tilt. The torso compresses, the head pitches down and the eyes close.

## Still weak
- The sheets don't show the old and new face close-ups side by side. Only the full-body view is compared old against new.
- The body is still the house rig: a big head, short arms, and limbs built from tapered capsules. Arms are only 126 units long, so namaste and blessing poses are cramped.
- The hands read well in close-ups, but at full-figure scale (about 25 px) they shrink to small blobs. Pointing reads, and finger detail is lost.
- Brahma's expressions are subtle, because the beard and moustache hide most of the mouth. Brow and eye changes carry them.
- The side faces are dimmed copies with yaw, not real profile drawings.
- In the bow, the head drops onto the joined hands, so it reads as "bowed" but not clearly.
- Walking is the engine's leg swing. There is no weight shift or heel strike.
- There is no side or back view. The flip only mirrors the figure, so the chakra and conch change hands.
- When Narada's arms act, his veena slung on the back sticks out over his shoulder. It still looks a little odd.
- Vishnu's crown is tall, so in head close-ups at s above 1.6 the crown can go off the top of the frame. The builder's face-crop check uses a generic head height and does not know this.
- Sitting (`sit` pose) falls back to the old seated cloth and legs. It has not been designed or checked for these three.
- Expression intensity has not been tuned for long shots, where faces are small.
