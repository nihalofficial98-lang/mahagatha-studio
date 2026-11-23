"""Exact subtitles from a recognizer's word timestamps: python3 studio/make_srt_ts.py <script.txt> <timestamps.json> <out.srt>
Cue text = the ORIGINAL script phrases (punctuation kept); times = matched recognizer words."""
import sys,json,numpy as np
sys.path.insert(0,__file__.rsplit('/',1)[0]);import import_timestamps as T,make_srt as M
script,tsf,out=sys.argv[1:4];U=M.phrases(script);asr=T.parse(tsf)
words=[(k,w) for k,u in enumerate(U) for w in u.split()];pair=T.match([w for _,w in words],asr);ns=len(words)
st=np.full(ns,np.nan);en=np.full(ns,np.nan)
for i,j in pair.items():st[i]=asr[j][1];en[i]=asr[j][2]
print(f'matched {int(np.sum(~np.isnan(st)))}/{ns} script words')
cues=[];i=0
for k,u in enumerate(U):
    n=len(u.split());s=st[i:i+n];e=en[i:i+n];i+=n;ok=~np.isnan(s)
    cues.append([float(s[ok].min()),float(e[ok].max()),u] if ok.any() else None)
for k,c in enumerate(cues):   # phrase with no matched word: borrow neighbours
    if c is None:
        a=next((cues[q][1] for q in range(k-1,-1,-1) if cues[q]),0);b=next((cues[q][0] for q in range(k+1,len(cues)) if cues[q]),a+1);cues[k]=[a,b,U[k]]
tot=asr[-1][2]
for k,c in enumerate(cues):
    nxt=cues[k+1][0] if k+1<len(cues) else tot+1;c[0]=max(0,c[0]-.04);c[1]=min(c[1]+.2,nxt-.02)
    if c[1]-c[0]<.5:c[1]=c[0]+.5
open(out,'w',encoding='utf-8').write('\n'.join(f'{k+1}\n{M.ts(a)} --> {M.ts(b)}\n{M.wrap(t)}\n' for k,(a,b,t) in enumerate(cues)))
print(len(cues),'cues; first',cues[0][:2],'last',cues[-1][:2])
