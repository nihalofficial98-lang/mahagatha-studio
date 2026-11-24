#!/usr/bin/env python3
"""Prepare reels from the owner's voice AI exports (reels/inputs/reelNN.mp3 + reelNN.json, ElevenLabs word-timestamp format).
Writes reels/build/reelNN/{words.json, subs.srt, report.txt}. Subtitles = exactly what was spoken (from the JSON), never the script.
usage: python3 studio/reel_prepare.py [NN ...]   (default: all)"""
import json, re, sys, pathlib, subprocess, difflib
root = pathlib.Path(__file__).resolve().parent.parent
inp, out = root/'reels/inputs', root/'reels/build'
plain = (root/'deliverables/reels/Reels_Voiceover_Plain.txt').read_text(encoding='utf-8')
blocks = re.split(r'^=== .*? ===\n', plain, flags=re.M)[1:]          # script narration per reel
def words_of(js):
    seg = js['segments']; ws = []
    for s in seg:
        for w in s['words']:
            t = w['text']
            if not t.strip(): continue
            ws.append({'w': t.strip(), 'start': round(w['start_time'], 3), 'end': round(w['end_time'], 3)})
    return ws
def norm(t): return re.sub(r"[^a-z0-9']", '', t.lower())
def cues(ws, maxw=6, maxc=36, maxdur=3.2):
    res, cur = [], []
    def flush():
        if cur: res.append(list(cur)); cur.clear()
    for i, w in enumerate(ws):
        if cur:
            gap = w['start'] - cur[-1]['end']
            txt = ' '.join(x['w'] for x in cur + [w])
            if len(cur) >= maxw or len(txt) > maxc or w['end'] - cur[0]['start'] > maxdur or gap > 0.45: flush()
        cur.append(w)
        if re.search(r'[.?!]["”]?$', w['w']) or (re.search(r'[,;:]$', w['w']) and len(cur) >= 3): flush()
    flush(); return res
def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02}:{int(m):02}:{int(s):02},{int(round((s-int(s))*1000)):03}"
for n in ([int(a) for a in sys.argv[1:]] or range(1, 8)):
    js = json.load(open(inp/f'reel{n:02}.json', encoding='utf-8')); ws = words_of(js)
    d = out/f'reel{n:02}'; d.mkdir(parents=True, exist_ok=True)
    json.dump(ws, open(d/'words.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    srt = []
    for k, c in enumerate(cues(ws), 1):
        srt.append(f"{k}\n{ts(c[0]['start'])} --> {ts(c[-1]['end'])}\n{' '.join(x['w'] for x in c)}\n")
    (d/'subs.srt').write_text('\n'.join(srt), encoding='utf-8')
    dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(inp/f'reel{n:02}.mp3')]).decode())
    spoken = [norm(w['w']) for w in ws]; script = [norm(w) for w in re.sub(r'\[[^\]]*\]', '', blocks[n-1]).split()]
    diff = [l for l in difflib.unified_diff(script, spoken, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
    rep = f"reel{n:02}: audio {dur:.2f}s, last word ends {ws[-1]['end']}s, {len(ws)} words, {len(srt)} subtitle cues\nword differences vs script (- script / + spoken): {len(diff)}\n" + ' '.join(diff)
    (d/'report.txt').write_text(rep, encoding='utf-8'); print(rep.split('\n')[0], '|', rep.split('\n')[1], '|', ' '.join(diff)[:160])
