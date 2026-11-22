# Trimurti: new paper-cut painterly look (frames)

These are new coded rigs for Brahma, Vishnu on Shesha, and Shiva. They don't use `engine/`. The style is layered flat-vector paper-cut: bold shapes, ink outlines, paper drop shadows, gold, indigo and saffron, ornate jewellery and flaming halos.

- `chars_new.js`: the drawing kit. It has the faces (eyes that blink, a talking mouth, third eye), crowns, halo, IK arms, hands with mudras, props and the serpent tubes and hoods.
- `trimurti_rigs.js`: the three rigs, backgrounds and scenes. Every parameter is a pure function of `t` plus params, so the same code animates.
  - Brahma: `sprout`, `rot` (faces turn), `bless`, `lift`, `talk`, `blink`, `glow`, `lotusGlow`
  - Vishnu: `blink` (1 = yoganidra), `smile`, `lx`, `sway`, `bias` (hoods lean), `rise`, `lotus` (navel lotus), `chakra`, `glow`
  - Shiva: `blink`, `third`, `raise`, `lift` (trident), `ganga`, `moon`, `smile`, `glow`
- `frames.json`: the list of key frames `{name, scene, t, p, cam}`.
- `showcase.html`: open it in a browser to see a live animated preview, for example `showcase.html#vishnu`.

Regenerate (Chromium through Playwright):

    node library/showcase/trimurti/render_frames.js        # writes frames/*.png at 1920x1080
    ONLY=shiva node library/showcase/trimurti/render_frames.js   # renders a subset
    python3 library/showcase/trimurti/contact_sheet.py      # writes frames/contact_sheet.jpg
