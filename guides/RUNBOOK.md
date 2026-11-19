# Daily runbook (batch of 7 episodes ≈ 1 week of posts)
1. `git pull`; read `library/BACKLOG.md`; fix top engine item if it blocks this batch.
2. For each episode: new → script → check → voice-docs → (send scripts to the voice artist) → shots → stills → fix → qa.
3. When `voiceovers/epNN.mp3` arrives: align → render 1080p (review) → qa --video → render 4K for posting.
4. Collect feedback → `studio.py feedback` → `learn`. Commit with the CHANGELOG entry.
Render cost today: ~80 min for 8.5 min at 4K on 4 cores; 1080p ≈ 25 min. GPU runner would cut this a lot (roadmap #6).
