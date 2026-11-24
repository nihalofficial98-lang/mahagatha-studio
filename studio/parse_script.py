"""script.md -> beats.json (scenes for tts.py). Each beat = one scene; lines become expressive segments."""
import re, json, sys
src, out = sys.argv[1], sys.argv[2]
CUES = [  # keyword -> (rate, pitch, vol)
 ("फुसफुसाकर", ("-7%", "-6Hz", "-10%")), ("क्रोध", ("+4%", "+3Hz", "+10%")), ("हँसी", ("+3%", "+4Hz", "+10%")),
 ("गिड़गिड़ा", ("+2%", "+4Hz", "+5%")), ("घबराहट", ("+8%", "+3Hz", "+5%")), ("तेज़", ("+8%", "+2Hz", "+8%")),
 ("भव्य", ("+0%", "+0Hz", "+10%")), ("गंभीर", ("-4%", "-5Hz", "+0%")), ("रहस्यमयी", ("-6%", "-4Hz", "-5%")),
 ("आग्रह", ("+2%", "+2Hz", "+0%")), ("ठंडा", ("-6%", "-6Hz", "-5%")), ("शांत", ("+0%", "-3Hz", "+0%")),
 ("करुण", ("-10%", "-3Hz", "-5%")), ("विस्फोट", ("+6%", "+4Hz", "+15%")), ("धमाका", ("+6%", "+4Hz", "+15%")), ("दृढ़", ("+0%", "-3Hz", "+5%")), ("स्नेह", ("-4%", "+0Hz", "+0%")), ("विचारमग्न", ("-6%", "-3Hz", "+0%")), ("भारी", ("-8%", "-5Hz", "+5%")), ("चिंतन", ("+0%", "-3Hz", "+0%")), ("धीमे", ("-4%", "-3Hz", "+0%")), ("टीज़र", ("+0%", "-2Hz", "+0%")),
]
CUES_EN = [  # English cue keywords (guide-voice stand-in only; the owner records the real voice)
 ("whisper", ("-7%", "-6Hz", "-10%")), ("angry", ("+4%", "+3Hz", "+10%")), ("pleading", ("+2%", "+4Hz", "+5%")),
 ("fast", ("+8%", "+2Hz", "+8%")), ("grand", ("+0%", "+0Hz", "+10%")), ("grave", ("-4%", "-5Hz", "+0%")),
 ("mysterious", ("-6%", "-4Hz", "-5%")), ("cold", ("-6%", "-6Hz", "-5%")), ("calm", ("+0%", "-3Hz", "+0%")),
 ("slow", ("-10%", "-3Hz", "-5%")), ("explosive", ("+6%", "+4Hz", "+15%")), ("firm", ("+0%", "-3Hz", "+5%")), ("tender", ("-4%", "+0Hz", "+0%")),
 ("measured", ("-2%", "-2Hz", "+0%")),
]
def cue_params(cue):
    for k, v in CUES + CUES_EN:
        if k in cue: return (f"{int(v[0][:-1])+10:+d}%",)+v[1:]
    return ("+10%", "+0Hz", "+0%")
beats, cur = [], None
for raw in open(src, encoding="utf-8").read().split("\n"):
    line = raw.strip()
    m = re.match(r"\*\*B(\d+)\*\*\s*(\[[^\]]*\])?", line)
    if m:
        cur = {"beat": int(m.group(1)), "cue": m.group(2) or "", "lines": []}; beats.append(cur); continue
    if cur is None or not line or line.startswith(("#", "---", "*समाप्त", "*The End")) :
        if line.startswith(("##", "---")): cur = None if line.startswith("---") else cur
        continue
    cur["lines"].append(line)
scenes = []
for b in beats:
    rate, pitch, vol = cue_params(b["cue"]); segs = []
    for ln in b["lines"]:
        if re.fullmatch(r"\((…|लंबा विराम)\)", ln):
            if segs: segs[-1]["pause"] += 0.7 if "लंबा" in ln else 0.35
            continue
        ln = re.sub(r"\[[^\]]*\]", "", ln).replace("**", "").strip()
        if ln: segs.append({"t": ln, "rate": rate, "pitch": pitch, "vol": vol, "pause": 0.15})
    if segs:
        segs[-1]["pause"] += 0.2; segs[-1]["rate"] = f"{int(rate[:-1]) - 3:+d}%"
    scenes.append({"beat": b["beat"], "narration": segs})
HI = bool(re.search(r"[\u0900-\u097F]", open(src, encoding="utf-8").read()))
json.dump({"voice": "hi-IN-MadhurNeural" if HI else "en-US-GuyNeural", "scenes": scenes}, open(out, "w"), ensure_ascii=False, indent=1)
print(len(scenes), "beats,", sum(len(s["narration"]) for s in scenes), "segments")
