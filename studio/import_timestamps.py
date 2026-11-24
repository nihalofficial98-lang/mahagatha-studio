"""Use REAL word timestamps (from a speech recognizer: ElevenLabs Speech-to-Text/Scribe JSON, Whisper JSON, or an SRT file)
to time the episode to the voiceover. The recognizer's words may be spelled differently from the script; they are matched
to the script words by fuzzy sequence alignment, and unmatched script words are interpolated between matched neighbours.
 usage: python3 studio/import_timestamps.py <ep> <voice-file> <timestamps.json|.srt> [--out build/epNN]"""
import sys,os,json,re,subprocess,difflib,unicodedata
import numpy as np
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(w):
    w=unicodedata.normalize('NFC',w).lower();w=re.sub(r'[​-‍﻿]','',w);w=re.sub(r'[^\wऀ-ॿ]','',w)
    w=w.replace('ॐ','ओम').replace('़','')   # Om sign -> ओम ; nukta
    w=re.sub(r'[ँं]','',w)  # chandrabindu/anusvara (often written differently)
    return w
def disp(w):
    """subtitle text of a script word: punctuation stripped. Latin (English) words keep an inner apostrophe/hyphen (Bala's, lotus-eyed); Devanagari unchanged."""
    if re.search(r'[A-Za-z]',w):
        return re.sub(r"^[^\w]+|[^\w]+$",'',re.sub(r"[^\w'’-]",'',w).replace('’',"'")).strip("'-")
    return re.sub(r'[^\wऀ-ॿ]','',w)
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
        t=str(x.get('text',x.get('word',''))).strip()
        if x.get('type','word')!='word' or not t or t.startswith('['):return   # skip spacing and [audio events]
        a=x.get('start',x.get('start_time'));b=x.get('end',x.get('end_time'))
        if a is None or b is None:return
        ws.append((t,float(a),float(b)))
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
    if '--max-time' in sys.argv:mt=float(sys.argv[sys.argv.index('--max-time')+1]);asr=[w for w in asr if w[1]<mt]
    words=[(bi,si,w) for bi,sc in enumerate(B) for si,seg in enumerate(sc['narration']) for w in seg['t'].split()]
    pair=match([w[2] for w in words],asr);ns=len(words);st=np.full(ns,np.nan);en=np.full(ns,np.nan)
    for i,j in pair.items():st[i]=asr[j][1];en[i]=asr[j][2]
    used=set(pair.values());extras=[];run=[]
    for j,w in enumerate(asr):
        if j in used:
            if len(run)>=2:extras.append({'start':asr[run[0]][1],'end':asr[run[-1]][2],'text':' '.join(asr[k][0] for k in run),'after_script_word':max([i for i,jj in pair.items() if jj<run[0]]+[-1])})
            run=[]
        else:run.append(j)
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
    if '--cut-extras' in sys.argv and extras:
        nxt=lambda t:min([st[k] for k in range(ns) if st[k]>t]+[1e9]);cuts=[(max(0,x['start']-.04),min(x['end']+.12,nxt(x['end'])-.02)) for x in extras if x['end']-x['start']>.5]
        keep=[];cur=0.0
        for a,b in cuts:keep.append((cur,a));cur=b
        keep.append((cur,None));fc=[];lab=[]
        for k,(a,b) in enumerate(keep):
            fc.append(f"[0:a]atrim=start={a:.3f}"+(f":end={b:.3f}" if b else "")+f",asetpts=PTS-STARTPTS,afade=t=in:d=.015,afade=t=out:st=0:d=0[a{k}]" if False else f"[0:a]atrim=start={a:.3f}"+(f":end={b:.3f}" if b else "")+f",asetpts=PTS-STARTPTS[a{k}]");lab.append(f'[a{k}]')
        tv=os.path.join(out,'voice_trimmed.mp3');os.makedirs(out,exist_ok=True)
        subprocess.run(['ffmpeg','-v','error','-y','-i',voice,'-filter_complex',';'.join(fc)+';'+''.join(lab)+f'concat=n={len(keep)}:v=0:a=1[o]','-map','[o]','-b:a','192k',tv],check=True)
        def sh(t):return t-sum(min(max(t-a,0),b-a) for a,b in cuts)
        st=np.array([sh(t) for t in st]);en=np.array([sh(t) for t in en]);voice=tv;extras=[];print('cut',len(cuts),'spoken heading(s) out of the audio:',[(round(a,1),round(b,1)) for a,b in cuts])
    total=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',voice]))
    bi_idx={};[bi_idx.setdefault(w[0],[]).append(k) for k,w in enumerate(words)]
    starts=[];
    for bi in sorted(bi_idx):
        f=st[bi_idx[bi][0]];prev=en[bi_idx[bi-1][-1]] if bi>0 else 0.0
        for x in extras:                      # spoken words not in the script (a heading) belong to the START of this beat
            if bi>0 and prev-.05<=x['start']<f:f=min(f,x['start']+.2)
        starts.append(0.0 if bi==0 else (prev+(f-prev)*.5 if f-prev<.6 else f-.2))
    ends=starts[1:]+[total];os.makedirs(out+'/audio',exist_ok=True);T=[]
    for bi in sorted(bi_idx):
        a,b=starts[bi],ends[bi];subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a:.3f}','-t',f'{b-a:.3f}','-i',voice,'-ac','1','-ar','44100','-b:a','192k',f'{out}/audio/{bi:02d}.mp3'],check=True)
        T.append({'audio':round(b-a,6),'duration':round(b-a,6),'beat':B[bi]['beat'],'words':[{'text':(disp(words[k][2]) or words[k][2]),'start':round(st[k]-a,3),'end':round(en[k]-a,3)}|({'hide':1} if not re.search(r'\w',words[k][2]) else {}) for k in bi_idx[bi]]})
    json.dump(T,open(out+'/timings.json','w'),ensure_ascii=False);json.dump(extras,open(out+'/extras.json','w'),ensure_ascii=False,indent=1)
    print('extra spoken words not in the script:',[(round(x['start'],1),x['text']) for x in extras][:8])
    print(f'timed to the recognizer: voice {total:.1f}s ({total/60:.2f} min), {len(B)} beats')
    if '--out' not in sys.argv:
        ef=f'{R}/episodes/ep{ep}/episode.json';d=json.load(open(ef));d['target_sec']=round(total,1);d['voice']='user';json.dump(d,open(ef,'w'),ensure_ascii=False)
if __name__=='__main__':main()
