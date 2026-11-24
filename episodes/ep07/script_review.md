# EP07 script review [hi] - verdict: FIX (6 blocking)

## Scorecard
```
EP07 script check [hi]  timing: 0.367 s/word
  length               8.92 min (1458 words)                     8-10 min                       ok
  cue tags             28/28 beats                               every beat                     ok
  beat variety         12 short / 3 mid / 13 long, run 2         >=3 S >=3 L                    ok
  beats match          28 json / 28 script                       same ids, same order           ok
  teaser               18 s                                      10-20 s, first                 ok
  chapters             3 story chapters                          3                              ok
    C1                 176 s B02-B09                             2.5-3.2 min                    ok
    C2                 152 s B10-B18                             2.5-3.2 min                    ok
    C3                 189 s B19-B28                             2.5-3.2 min                    ok
  hook                 B01 at 0 s                                ok
  first stakes         B03 at 28 s                               <= 60 s                        ok
  max re-hook gap      82 s (from 4:23)                          <= 90 s                        ok
  climax               B26 at 7:54 (89%)                         in last chapter                ok
  payoff after climax  B27 +0 s                                  <= 30 s                        ok
  after climax         50 s = 9%                                 <= 15%                         ok
  planted question     B01 -> B27                                ok
  reels                A 2.9 / B 2.5 / C 3.2 min                 ok
RESULT: PASS (0 errors, 0 warnings)
```
The checker passes. The blocking items below are retention-checklist items it cannot judge.

## Blocking fixes (must do before recording)
1. **B01 teaser** (planted question, triple hook). Two questions are planted: "why did he agree" and "what does the biggest gift cost". The second is abstract, and only B28 answers it, vaguely. Line 2 also gives away both outcomes, so the hook has no snapback. Replace the whole beat with one question (same word count, about 55):
   - Context: "एक असुर ने अपना शरीर दे दिया। एक देवता ने अपनी आँख।"
   - Lean: "और दोनों बार, बदले में दुनिया को वह मिला, जो तलवार से कभी नहीं मिलता।"
   - Snapback: "पर जिसने स्वर्ग को बल से छीना था, वह अपनी जान देने को ख़ुद क्यों राज़ी हो गया?"
   - In beats.json, set planted_question.answered_in to B09 (the answer is there, not in B27) and update the text to the single question. B27 is not honestly an "answer" beat. B09 answers the why, and B28 states the resolved line. Change B27 roles to ["payoff"].
2. **B09** (interpretive line). "वही उदारता, उसकी हार भी बनी, और उसकी जीत भी" is not source plot. The source gives no "win" for Bala. It says his selfless act sanctified his body. The "क्योंकि उसका दिल किसी को ना नहीं कह पाता था" line is fine, because it is grounded in "never refused a request" and "generous enough to offer himself". Replace the last line with: "उसने जान इसलिए दी, क्योंकि उसका दिल किसी को ना नहीं कह पाता था। जिस उदारता ने उसे हराया, उसी ने उसकी देह को अनमोल बना दिया।" This keeps the bridge and stays within the source (selfless act -> sanctified body).
3. **B14** (re-hook is a label and repeats B13). "चौरासी में से इक्कीस। इक्कीस में से नौ..." restates B13's last paragraph. "छँटाई होती गई" implies someone was sorting, which the source does not say. "अब हर रत्न का जन्म सुनिए" is a label, not a question. This is also the dullest stretch of the video (B13-B16, about 80 s of listing). Replace with (about 28 words): "नौ रत्न, और नौ अलग अंग। सबसे हैरान करने वाला रत्न बना उसकी आवाज़ से। कौन-सा? पहले हड्डियों से शुरू करें।" This plants a real question that B16 pays off. Delete the B13 sentence "वह देह... बाला धरती पर फैल गया था" (about 25 words) so the numbers are not told twice.
4. **B15** (unsupported inference, and it breaks reel B). "देवताओं ने इंद्रधनुष में जो लाल, हरे और नीले रंग देखे थे, वे इन्हीं रत्नों के थे" links the rainbow colours to the gems. The source never makes that link. It also omits yellow, and a stranger who only saw reel B has never heard of the rainbow. The line "वही आँखें, जो कभी देवताओं को देखकर उदार हो उठी थीं" is also invented. Cut both lines (saves about 35 words) and use: "उसकी आँखों से नीलम। एक अंग, एक रत्न।" Also drop "यज्ञ की आग में जलती" before "हड्डियों" (embellishment): "उसकी हड्डियों से हीरे बने।"
5. **B20 / B28 / B27** (reel C is not standalone, and its stakes are never paid).
   - B20 opens with "हर असुर बाला जैसा उदार नहीं था". A reel-C viewer does not know Bala. Replace the line with "सारे असुर उदार नहीं थे। ज़्यादातर तो देवताओं को सताते और इंसानों को मारते थे।"
   - B28 recaps "बाला ने देह दी, और दुनिया को नौ रत्न मिले", which means nothing to a reel-C-only viewer. Replace with: "बाला नाम के असुर ने यज्ञ में अपनी देह दी, और दुनिया को नौ रत्न मिले। विष्णु ने आँख दी, और संसार को सुदर्शन। सबसे बड़ा तोहफ़ा, दोनों बार, अपना कुछ देकर ही मिला।" (The question line stays.)
   - B27 says "बाला के बनाए हर रत्न से ज़्यादा दमक रही थी". Change it to "किसी भी रत्न से ज़्यादा दमक रही थी". The stakes from B20 (demons ruining the worlds) also go unanswered. Source: "You can combat every chaos in Brahmanda with this." Add to Shiva's speech: "इससे तुम हर संकट से लड़ सकोगे।"
6. **B19** (C3 hook is muddled). "एक हज़ार कमल चढ़ाए, और फिर भी हज़ार पूरे नहीं हुए" contradicts itself. It also spoils the B23 turn without creating a question. Replace with three lines:
   - Context: "विष्णु, जो सृष्टि को पालते हैं, एक दिन थक गए।"
   - Lean: "उन्होंने शिव की ऐसी पूजा शुरू की, जैसी किसी ने नहीं की थी।"
   - Snapback: "और हज़ार कमलों में से बस एक कमल कम पड़ गया।"

## Should fix
7. **B02** has only two lines and no true snapback, but it works as a hook ("अपनी हार की चाबी"). Optional third line: "और वह चाबी थी एक वादा।" (about 6 words).
8. **B11** repeats B09 ("इतनी अद्भुत", the heavenly-voice echo). Cut "उन्हें यक़ीन नहीं हो रहा था... अद्भुत निकली" and "आकाशवाणी के शब्द... भंडार" (saves about 30 words). In reel B this is dead time before the fall.
9. **B10** is a long single sentence that reveals the gems before the question. Suggested: "बाला नाम के दानी असुर ने स्वर्ग जीता, फिर अपनी देह यज्ञ में दे दी। और जो देह बची, उसे देवता स्वर्ग तक ले जा नहीं पाए। क्यों?" It also makes reel B standalone by naming the sacrifice.
10. **B17 framing**. This is acceptable storyteller framing, not source plot, but "जो उन्हें तलवार से कभी न मिलता" is a counterfactual. Soften it to "देवताओं ने चाल से जिस असुर की जान ली, उसी की देह से धरती को ऐसा ख़ज़ाना मिला, जो किसी जीत से नहीं मिलता।" The last sentence ("आज भी जब कोई नवरत्न...") repeats B18. Cut one of the two (saves about 22 words).
11. **B16**. "वही आवाज़, जिसने कहा था, 'मैं तैयार हूँ'" is a callback that reel B does not have. Change it to "वही आवाज़, जिसने यज्ञ में कहा था, 'मैं तैयार हूँ'।" Cut the filler "ये नाम सुनने में छोटे हैं, पर..." or tighten it.
12. **B20 "स्त्रियों का अपमान"**. The softening of "defiling women" is acceptable for a family audience and is not a factual distortion. "स्त्रियों पर अत्याचार करते थे" is closer to the source and equally safe. **B27 (106 words)** is under the 110 hard cap and the checker passes, but it is dense. Optional split: B27a ends at "...उन्होंने उन्हें एक सुनहरा चक्र दिया।" (about 38 words). B27b starts "उसमें दो गोल घेरे..." (about 65 words). Add a new B27 cue so the chakra visual lands.

## Reel check
- **A**: hook "बाला नाम का एक असुर, इंद्र को हराकर, स्वर्ग का राजा बन बैठा। और तभी उसने अनजाने में, अपनी हार की चाबी..." | payoff B08 + B09 | bridge "वही उदारता, उसकी हार भी बनी, और उसकी जीत भी" (fix 2) | stranger test: ok. All names are introduced.
- **B**: hook B10 (fix 9) | payoff B17 | bridge B18 "हर रत्न में, एक उदार असुर का बलिदान चमकता है" | stranger test: fails until fixes 4 and 11 are applied (the rainbow and "मैं तैयार हूँ" depend on reel A). B13-B16 is a list with no conflict.
- **C**: hook B19 (fix 6) | payoff B27 | bridge B28 | stranger test: fails on "बाला" (B20, B27, B28) and on the unpaid stakes (fix 5). Otherwise it is the strongest reel.
- **Triple hooks** (quoted as three lines each):
  - Teaser: current lines "एक असुर ने अपना शरीर दे दिया। एक देवता ने अपनी आँख।" / "एक से नौ रत्न निकले, दूसरे को सुदर्शन चक्र मिला।" / "पर जिसने स्वर्ग को बल से छीना था..." Two questions and an answer leak (fix 1).
  - C1: lines 1 and 2 only (B02).
  - C2: one run-on line (B10).
  - C3: muddled (B19).
- The teaser does not give away the answer to the "why" question. It does give away the two outcomes.
- **Standalone check**: there is no next-episode tease. B28 is a resolved line plus a comment question.
- **Facts checked against the source**:
  - B15's link between the rainbow colours and the gems is not in the source. Cut it (fix 4).
  - The B09 "जीत" claim is not in the source (fix 2).
  - Everything else in B13, B15 and B16 matches story 12: 84, 21 and 9, and the nine organ-to-gem pairs.
  - B22-B27 match story 13. This includes 999, Kamalanayana and the 108 edges.
- **Retention checklist**:
  - Stakes are concrete in C1 (B03, 0:28) and in C3 (B20). The B20 stakes become concrete once the chakra payoff covers them.
  - The set-piece (B06 yagna request) starts at about 1:31 (about 17%), well before 35%.
  - The post-climax part is answer + feeling + bridge, not a lecture.

## Timing map
T 0:00-0:18 | C1 0:18-3:14 | C2 3:14-5:46 | C3 5:46-8:55 | first stakes 0:28 (B03), set-piece (B06) about 1:31 (17%), re-hook gap at most 82 s, climax B26 7:54 (89%), payoff immediately after, post-climax 50 s (9%). Fixes 3, 8, 10 and 11 free roughly 110 words (about 40 s). Use that room for the B20/B28/B19 additions (about +45 words) and keep the total at 8.5-9 min.
