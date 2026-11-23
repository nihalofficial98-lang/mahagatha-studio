# Prompt to paste (owner)

**Start an episode**
```
Make episode NN about <story / source/story_XX.txt>. Follow WORKFLOW.md: use the producer agent; script-editor writes the script,
emotion-tagged voiceover script and hook titles; then stop and wait for my mp3 + word-timestamp JSON.
```

**After recording**
```
Episode NN: here are the voice <path/to/voice.mp3> and the word timestamps <path/to/words.json>. Continue WORKFLOW.md from step 3
(align, then characters first; stop for my approval of the character sheets).
```

**Approvals / feedback**
```
Episode NN: character sheets approved.            |  Episode NN: frames approved, render it.
Episode NN frames: <shot id>: <what is wrong>.  (the producer routes it to the agent that owns that field)
```
