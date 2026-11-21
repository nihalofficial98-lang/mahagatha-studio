"""Verify that every cue/shot anchor (time + word) really sits on that word in the owner's voiceover.
python3 studio/check_cues.py 93 episodes/ep93/sound_cues.json"""
import json,sys,os,re
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(w):return re.sub(r'[^\wऀ-ॿ]','',w)
def main():
    ep=sys.argv[1];cues=json.load(open(sys.argv[2],encoding='utf-8'));T=json.load(open(f'{R}/build/ep{ep}/timings.json',encoding='utf-8'))
    W=[];off=0.0
    for t in T:
        W+=[(norm(w['text']),off+w['start'],off+w['end']) for w in t['words']];off+=t['duration']
    total=off;ok=bad=skip=0
    for c in cues.get('cues',[]):
        for k in('from','to'):
            a=c.get(k)
            if not isinstance(a,dict) or 't' not in a:skip+=1;continue
            if a.get('word') is None:ok+=1;continue
            w=norm(a['word']);ei=2 if a.get('edge')=='end' else 1;near=[r[ei] for r in W if r[0]==w or r[0].startswith(w) or w.startswith(r[0])]
            d=min([abs(ts-a['t']) for ts in near],default=None)
            if d is not None and d<=.6:ok+=1
            else:bad+=1;print(f"MISMATCH {c['id']}.{k}: word '{a['word']}' claimed at {a['t']}s; closest real occurrence {'none' if d is None else f'{d:.2f}s away'}")
            if a['t']>total+.5:print(f"NOTE past the end of the voice (intended tail?) {c['id']}.{k}: {a['t']}s > {total:.1f}s")
    print(f'anchors checked: {ok} ok, {bad} mismatched, {skip} without absolute time')
main()
