"""Use REAL word timestamps (from a speech recognizer: ElevenLabs Speech-to-Text/Scribe JSON, Whisper JSON, or an SRT file)
to time the episode to the voiceover. The recognizer's words may be spelled differently from the script; they are matched
to the script words by fuzzy sequence alignment, and unmatched script words are interpolated between matched neighbours.
 usage: python3 studio/import_timestamps.py <ep> <voice-file> <timestamps.json|.srt> [--out build/epNN]"""
import sys,os,json,re,subprocess,difflib,unicodedata
import numpy as np
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(w):
    w=unicodedata.normalize('NFC',w).lower();w=re.sub(r'[​-‍﻿]','',w);w=re.sub(r'[^\wऀ-ॿ]','',w)
    w=w.replace('़','')          # nukta
    w=re.sub(r'[ँं]','',w)  # chandrabindu/anusvara (often written differently)
    return w
def parse_srt(txt):
    out=[]
    for blk in re.split(r'\n\s*\n',txt.strip()):
        ls=[l for l in blk.strip().split('\n') if l.strip()]
        for i,l in enumerate(ls):
            m=re.match(r'(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)',l)
            if m:
                g=list(map(int,m.groups()));a=g[0]*3600+g[1]*60+g[2]+g[3]/1000;b=g[4]*3600+g[5]*60+g[6]+g[7]/1000;ws=' '.join(ls[i+1:]).split()
                if ws:
                    L=np.array([max(1,len(w)) for w in ws],float);c=np.r_[0,np.cumsum(L)]/L.sum()
                    for k,w in enumerate(ws):out.append((w,a+(b-a)*c[k],a+(b-a)*c[k+1]))
    return out
def parse(path):
    txt=open(path,encoding='utf-8-sig').read()
    if path.lower().endswith('.srt'):return parse_srt(txt)
    d=json.loads(txt);ws=[]
    def add(x):
        t=x.get('text',x.get('word',''));
        if x.get('type','word')!='word' or not str(t).strip():return
        ws.append((str(t).strip(),float(x['start']),float(x['end'])))
    if isinstance(d,dict) and 'words' in d:[add(x) for x in d['words']]
    elif isinstance(d,dict) and 'segments' in d:
        for sg in d['segments']:[add(x) for x in sg.get('words',[])]
    elif isinstance(d,dict) and 'transcripts' in d:
        for tr in d['transcripts']:[add(x) for x in tr.get('words',[])]
    elif isinstance(d,list):[add(x) for x in d]
    if not ws:raise SystemExit('could not find word timestamps in '+path)
    return ws
def sim(a,b):
    if not a or not b:return 0.0
    if a==b:return 1.0
    return difflib.SequenceMatcher(None,a,b).ratio()
def match(script,asr):
    S=[norm(w) for w in script];A=[norm(w[0]) for w in asr];n,m=len(S),len(A);GAP=-.45
    M=np.zeros((n+1,m+1));M[:,0]=np.arange(n+1)*GAP;M[0,:]=np.arange(m+1)*GAP;P=np.zeros((n+1,m+1),np.int8)
    for i in range(1,n+1):
        for j in range(1,m+1):
            s=sim(S[i-1],A[j-1]);sc=(s*2-1) if s>=.5 else -1.0   # good match positive, bad match negative
            c=[M[i-1,j-1]+sc,M[i-1,j]+GAP,M[i,j-1]+GAP];k=int(np.argmax(c));M[i,j]=c[k];P[i,j]=k
    i,j=n,m;pair={}
    while i>0 and j>0:
        k=P[i,j]
        if k==0:
            if sim(S[i-1],A[j-1])>=.5:pair[i-1]=j-1
            i-=1;j-=1
        elif k==1:i-=1
        else:j-=1
    return pair
def main():
    ep,voice,tsf=sys.argv[1],sys.argv[2],sys.argv[3];out=os.path.join(R,'build/ep'+ep)
    if '--out' in sys.argv:out=os.path.abspath(sys.argv[sys.argv.index('--out')+1])
    B=json.load(open(f'{R}/build/ep{ep}/beats.json',encoding='utf-8'))['scenes'];asr=parse(tsf)
    words=[(bi,si,w) for bi,sc in enumerate(B) for si,seg in enumerate(sc['narration']) for w in seg['t'].split()]
    pair=match([w[2] for w in words],asr);ns=len(words);st=np.full(ns,np.nan);en=np.full(ns,np.nan)
    for i,j in pair.items():st[i]=asr[j][1];en[i]=asr[j][2]
    ok=np.flatnonzero(~np.isnan(st));print(f'matched {len(ok)} of {ns} script words ({100*len(ok)/ns:.0f}%) to recognizer words ({len(asr)})')
    if len(ok)<ns*.5:raise SystemExit('too few words matched: is this the right episode / transcript?')
    # fill gaps by interpolation weighted by word length
    L=np.array([max(1,len(norm(w[2]))) for w in words],float)
    i=0
    while i<ns:
        if np.isnan(st[i]):
            j=i
            while j<ns and np.isnan(st[j]):j+=1
            a=en[i-1] if i>0 else (st[j]-L[i:j].sum()*.2 if j<ns else 0);b=st[j] if j<ns else a+L[i:j].sum()*.2;c=np.r_[0,np.cumsum(L[i:j])]/L[i:j].sum()
            for k in range(i,j):st[k]=a+(b-a)*c[k-i];en[k]=a+(b-a)*c[k-i+1]
            i=j
        else:i+=1
    st=np.maximum.accumulate(st);en=np.maximum(en,st+.05)
    total=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',voice]))
    bi_idx={};[bi_idx.setdefault(w[0],[]).append(k) for k,w in enumerate(words)]
    starts=[];
    for bi in sorted(bi_idx):
        f=st[bi_idx[bi][0]];prev=en[bi_idx[bi-1][-1]] if bi>0 else 0.0
        starts.append(0.0 if bi==0 else (prev+(f-prev)*.5 if f-prev<.6 else f-.2))
    ends=starts[1:]+[total];os.makedirs(out+'/audio',exist_ok=True);T=[]
    for bi in sorted(bi_idx):
        a,b=starts[bi],ends[bi];subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a:.3f}','-t',f'{b-a:.3f}','-i',voice,'-ac','1','-ar','44100','-b:a','192k',f'{out}/audio/{bi:02d}.mp3'],check=True)
        T.append({'audio':round(b-a,6),'duration':round(b-a,6),'beat':B[bi]['beat'],'words':[{'text':(re.sub(r'[^\wऀ-ॿ]','',words[k][2]) or words[k][2]),'start':round(st[k]-a,3),'end':round(en[k]-a,3)} for k in bi_idx[bi]]})
    json.dump(T,open(out+'/timings.json','w'),ensure_ascii=False)
    print(f'timed to the recognizer: voice {total:.1f}s ({total/60:.2f} min), {len(B)} beats')
    if '--out' not in sys.argv:
        ef=f'{R}/episodes/ep{ep}/episode.json';d=json.load(open(ef));d['target_sec']=round(total,1);d['voice']='user';json.dump(d,open(ef,'w'),ensure_ascii=False)
if __name__=='__main__':main()
