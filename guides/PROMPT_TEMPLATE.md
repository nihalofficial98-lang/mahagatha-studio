# Prompt to paste (owner)

**Start an episode**
```
Make episode NN about <story / source/story_XX.txt>. Follow WORKFLOW.md: use the producer agent; script-editor writes beats.json + the
Hindi script, script-doctor reviews it, script-editor fixes it (studio.py check NN must PASS); then the emotion-tagged voiceover
script and hook titles; then stop for my script approval and wait for my mp3 + word-timestamp JSON.
```

**After recording**
```
Episode NN: here are the voice <path/to/voice.mp3> and the word timestamps <path/to/words.json>. Continue WORKFLOW.md from step 3
(align, then characters first; stop for my approval of the character sheets).
```

**Approvals / feedback**
```
Episode NN: script approved.  |  Episode NN: make the English version.  |  Episode NN: character sheets approved.            |  Episode NN: frames approved, render it.
Episode NN frames: <shot id>: <what is wrong>.  (the producer routes it to the agent that owns that field)
```
