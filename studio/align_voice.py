"""Align a recorded/generated voiceover (one file for the whole episode) to the script, WITHOUT any speech model.
 usage: python3 studio/align_voice.py <ep> <voice-file> [--out build/epNN]
 Writes build/epNN/audio/NN.mp3 (one clip per beat, cut from the user's audio) + timings.json in the same format the TTS step wrote,
 so shots.py / the renderer follow the voice (voice is never stretched; visuals are matched to it).
 Method: speech/silence detection -> chunks; dynamic programming assigns chunks to script lines (expected length ~ text weight,
 boundaries prefer the longest pauses); word times are spread across the voiced time of each line."""
import sys,os,json,subprocess,re,math
import numpy as np
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));SR=16000
def load(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',path,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True);return np.frombuffer(p.stdout,dtype='<f4')
def chunks(x,hop=.01):
    n=int(SR*hop);m=len(x)//n;f=x[:m*n].reshape(m,n);e=10*np.log10((f**2).mean(1)+1e-10)
    k=np.ones(3)/3;e=np.convolve(e,k,'same');lo,hi=np.percentile(e,10),np.percentile(e,95);thr=lo+.35*(hi-lo);sp=e>thr
    # close tiny gaps (stop consonants) and drop tiny blips
    idx=np.flatnonzero(np.diff(np.r_[0,sp.astype(int),0]));seg=[[a*hop,b*hop] for a,b in zip(idx[::2],idx[1::2])]
    out=[]
    for s in seg:
        if out and s[0]-out[-1][1]<.14:out[-1][1]=s[1]
        else:out.append(s)
    return [c for c in out if c[1]-c[0]>.09]
def wt(word):
    w=re.sub(r'[^ऀ-ॿ\w]','',word)
    if re.search(r'[A-Za-z]',w):return float(max(1,len(re.findall(r'[aeiouy]+',w.lower()))))   # English: ~syllables
    base=len(re.findall(r'[क-हक़-य़ऄ-औॲ]',w));mat=len(re.findall(r'[ा-्ँ-ः]',w))
    return max(1.0,base+.3*mat)
def align(units,ch,rate=None):
    N=len(ch);K=len(units);W=np.array([sum(wt(w) for w in u.split()) for u in units]);dur=np.array([c[1]-c[0] for c in ch]);cum=np.r_[0,np.cumsum(dur)]
    gap=np.array([ch[i+1][0]-ch[i][1] for i in range(N-1)]+[0.0])
    r=rate or cum[-1]/W.sum();INF=1e18;f=np.full((K+1,N+1),INF);bk=np.zeros((K+1,N+1),int);f[0,0]=0;span=14
    for k in range(1,K+1):
        for j in range(k,N+1):
            best=INF;bi=0
            for i in range(max(k-1,j-span),j):
                if f[k-1,i]>=INF:continue
                D=cum[j]-cum[i];c=f[k-1,i]+3.0*math.log(max(D,.05)/(W[k-1]*r))**2
                if i>0:c+=1.2/(1+gap[i-1]/.25)   # boundaries want to be at long pauses
                if c<best:best,bi=c,i
            f[k,j]=best;bk[k,j]=bi
    j=N;res=[]
    for k in range(K,0,-1):i=bk[k,j];res.append((i,j));j=i
    return res[::-1],r,W
def main():
    ep=sys.argv[1];voice=sys.argv[2];out=os.path.join(R,'build/ep'+ep)
    if '--out' in sys.argv:out=os.path.abspath(sys.argv[sys.argv.index('--out')+1])
    B=json.load(open(f'{R}/build/ep{ep}/beats.json',encoding='utf-8'))['scenes']
    units=[];own=[]
    for bi,sc in enumerate(B):
        for si,seg in enumerate(sc['narration']):units.append(seg['t']);own.append((bi,si))
    x=load(voice);total=len(x)/SR;ch=chunks(x)
    asg,r,W=align(units,ch)
    if len(ch)>len(units)*8:print('note: many pauses detected; check the result table')
    asg,r2,W=align(units,ch,rate=float(np.median([sum(c[1]-c[0] for c in ch[i:j])/W[k] for k,(i,j) in enumerate(asg)])))
    lines=[]
    for k,(i,j) in enumerate(asg):
        sub=ch[i:j];D=sum(c[1]-c[0] for c in sub);words=units[k].split();ws=[wt(w) for w in words];tot=sum(ws);acc=0;wl=[]
        def at(p):
            for c in sub:
                d=c[1]-c[0]
                if p<=d:return c[0]+p
                p-=d
            return sub[-1][1]
        for w,wv in zip(words,ws):
            a=at(D*acc/tot);acc+=wv;b=at(D*acc/tot);wl.append((w,a,b))
        lines.append({'start':sub[0][0],'end':sub[-1][1],'words':wl,'rate':D/(W[k]*r2)})
    # beats
    bs={};
    for k,(bi,si) in enumerate(own):bs.setdefault(bi,[]).append(k)
    starts=[];
    for bi in sorted(bs):
        f=lines[bs[bi][0]]['start'];prev=lines[bs[bi-1][-1]]['end'] if bi>0 else 0.0;starts.append(max(prev+(f-prev)*.5 if f-prev<.6 else f-.2,0) if bi>0 else 0.0)
    ends=starts[1:]+[total];os.makedirs(out+'/audio',exist_ok=True);T=[]
    for bi in sorted(bs):
        a,b=starts[bi],ends[bi];n=f'{bi:02d}'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a:.3f}','-t',f'{b-a:.3f}','-i',voice,'-ac','1','-ar','44100','-b:a','192k',f'{out}/audio/{n}.mp3'],check=True)
        wl=[{'text':(re.sub(r'[^\w\u0900-\u097F]','',w) or w),'start':round(s-a,3),'end':round(e-a,3)} for k in bs[bi] for (w,s,e) in lines[k]['words']]
        T.append({'audio':round(b-a,6),'duration':round(b-a,6),'words':wl,'beat':B[bi]['beat']})
    json.dump(T,open(out+'/timings.json','w'),ensure_ascii=False)
    print(f'voice {total:.1f}s ({total/60:.2f} min), {len(units)} lines, {len(B)} beats, speaking rate fit ok')
    bad=0
    for k,l in enumerate(lines):
        flag=' <-- check' if not .6<l['rate']<1.6 else ''
        if flag:bad+=1
        print(f'B{B[own[k][0]]["beat"]:02d}.{own[k][1]} {l["start"]:7.2f}-{l["end"]:7.2f}  x{l["rate"]:.2f}{flag}  {units[k][:48]}') if ('-v' in sys.argv or flag) else None
    print('lines needing a look:',bad)
    if '--out' not in sys.argv:
        ef=f'{R}/episodes/ep{ep}/episode.json';d=json.load(open(ef));d['target_sec']=round(total,1);d['voice']='user';json.dump(d,open(ef,'w'),ensure_ascii=False)
    return lines,own
if __name__=='__main__':main()
