#!/usr/bin/env python3
"""reel_prepare for reels whose voice files live in voiceovers/reels/<slug>/: python3 studio/reel_prepare2.py reel17:reel17_sudarshana ...
Copies mp3+json to reels/inputs/<id>.mp3/.json and writes reels/build/<id>/{words.json,subs.srt} (subtitles = exactly what was spoken)."""
import json,re,sys,shutil,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parent.parent
def words_of(js):
    return [{'w':w['text'].strip(),'start':round(w['start_time'],3),'end':round(w['end_time'],3)} for s in js['segments'] for w in s['words'] if w['text'].strip()]
def cues(ws,maxw=6,maxc=36,maxdur=3.2):
    res,cur=[],[]
    def fl():
        if cur:res.append(list(cur));cur.clear()
    for w in ws:
        if cur:
            gap=w['start']-cur[-1]['end'];txt=' '.join(x['w'] for x in cur+[w])
            if len(cur)>=maxw or len(txt)>maxc or w['end']-cur[0]['start']>maxdur or gap>.45:fl()
        cur.append(w)
        if re.search(r'[.?!]["”]?$',w['w']) or (re.search(r'[,;:]$',w['w']) and len(cur)>=3):fl()
    fl();return res
def ts(t):
    h,r=divmod(t,3600);m,s=divmod(r,60);return f"{int(h):02}:{int(m):02}:{int(s):02},{int(round((s-int(s))*1000)):03}"
for a in sys.argv[1:]:
    rid,slug=a.split(':');src=root/'voiceovers/reels'/slug
    shutil.copy(src/f'{slug}.mp3',root/f'reels/inputs/{rid}.mp3');shutil.copy(src/f'{slug}.json',root/f'reels/inputs/{rid}.json')
    ws=words_of(json.load(open(src/f'{slug}.json',encoding='utf-8')));d=root/f'reels/build/{rid}';d.mkdir(parents=True,exist_ok=True)
    json.dump(ws,open(d/'words.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    srt=[f"{k}\n{ts(c[0]['start'])} --> {ts(c[-1]['end'])}\n{' '.join(x['w'] for x in c)}\n" for k,c in enumerate(cues(ws),1)]
    (d/'subs.srt').write_text('\n'.join(srt),encoding='utf-8');print(rid,len(ws),'words',ws[-1]['end'],'s')
