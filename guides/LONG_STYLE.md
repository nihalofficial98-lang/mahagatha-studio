# Long-video style: the question-explainer (from the owner's 3 sample videos)
Samples: "Why didn't Parshuram kill Ravan?" (7:10), "Why did Sri Ram speak so harshly to Ma Sita?" (10:22), "How huge was the Varaha avatar?" (12:48).
Use `"format": "explainer"` in episodes/epNN/episode.json. The older dramatised retelling (EP6) is `"format": "story"`; both follow the chapter/reel rules in SCRIPT_STYLE.md and the triple hook.

## Shape
1. **Title and first line = one concrete question** that people already half-know ("Why didn't X do Y?", "How huge was ...?"). Line 1 restates it with stakes or a number (Earth = 12,750 km across, so how big must the boar be?). Context at once; then the lean/snapback of the triple hook ("think about it humanly", "the verse doesn't say that").
2. **Promise the method**: "To understand that we first need to look at ..." - open the loop, then go back to the source. A loop opened in the hook is paid at the end (the calculation, the verdict).
3. **Background story in short, plain steps** (curse of Jaya-Vijaya, Diti and Kashyap, Hiranyaksha) only as far as the question needs. Name every person when they appear.
4. **Evidence beats**: give the exact source and location (text, kanda/skandha, sarg/chapter, shloka) and say what it says in one plain sentence. Quote the Sanskrit line only when the owner's source pack contains it. NEVER invent a verse number; if a reference is missing, write the beat without it and list it in script_review.md as "needs source".
5. **Test popular explanations one by one**: "Some people say ... But the text does not say that." / "Here is a common explanation ... why it is interesting ... and the part it does not answer." Honest limits are good: "I could not find a text that says ...".
6. **Verdict ("my position")** near the end: 3-4 short sentences. Say what is proven, what is only interpretation. Then invite viewers to comment with direct textual evidence.
7. Optional **mid-roll slot** at about 1:00-1:45 (channel/website mention) - the owner supplies the line; keep it out of reels.

## Voice and lines
- Conversational and direct: "Now, here's something important", "Imagine that", "Remember he...", "So you can understand the problem". Rhetorical questions at turns, one idea per sentence.
- Neutral and respectful; correct myths by showing the text and, where possible, where the myth came from (oral/regional traditions, later plays), never by mocking belief.
- Modern comparisons and numbers when they make scale clear (km, football fields) - computed, not guessed.
- Mix narrative beats (the story) with analysis beats; never more than about 90 s of pure analysis without a story image or a new question.

## Reels from an explainer
Each "explanation" or story section can be cut as a reel (see REEL_STYLE.md): hook = the myth or the question; middle = text evidence; end = the verdict of that section. Mark `reel` in beats.json at writing time.

## Checks added to script-doctor
- Hook is a question or claim with the context in line 1; the promise is paid before the end.
- Every claim about "the text says" has a source reference from the source pack or is flagged "needs source".
- At least two explanations or evidence steps are tested, with one stated limit.
- A verdict beat exists and separates proof from interpretation.
