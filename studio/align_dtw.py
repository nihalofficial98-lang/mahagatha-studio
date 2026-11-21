"""Word-level alignment of a recorded voiceover by matching it to a guide-voice reference (edge-tts, which gives exact word times)
with banded dynamic time warping on MFCC features. No speech model needed.
 usage: python3 studio/align_dtw.py <ep> <voice-file> [--out build/epNN] [--ref <refdir>]
 Reads build/epNN/beats.json. Writes <out>/audio/NN.mp3 (per-beat clips of the user's audio) + <out>/timings.json (word times in the user's audio)."""
import sys,os,json,subprocess,re
import numpy as np
from numba import njit
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));SR=16000;HOP=320;WIN=400
def load(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',path,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True);return np.frombuffer(p.stdout,dtype='<f4')
def mel_fb(n_mels=40,n_fft=512,fmin=80,fmax=7600):
    mel=lambda f:2595*np.log10(1+f/700);inv=lambda m:700*(10**(m/2595)-1);pts=inv(np.linspace(mel(fmin),mel(fmax),n_mels+2));b=np.floor((n_fft+1)*pts/SR).astype(int);fb=np.zeros((n_mels,n_fft//2+1))
    for i in range(1,n_mels+1):
        l,c,r=b[i-1],b[i],b[i+1]
        for k in range(l,c):fb[i-1,k]=(k-l)/max(c-l,1)
        for k in range(c,r):fb[i-1,k]=(r-k)/max(r-c,1)
    return fb
FB=mel_fb()
def feats(x):
    n=1+(len(x)-WIN)//HOP;idx=np.arange(WIN)[None,:]+HOP*np.arange(n)[:,None];f=x[idx]*np.hamming(WIN);S=np.abs(np.fft.rfft(f,512))**2;M=np.log(S@FB.T+1e-10)
    k=np.arange(40);dct=np.cos(np.pi/40*(k[None,:]+.5)*np.arange(1,13)[:,None]);C=M@dct.T;e=np.log((f**2).sum(1)+1e-10)
    C=(C-C.mean(0))/(C.std(0)+1e-6);e=(e-e.mean())/(e.std()+1e-6);return np.concatenate([C,1.5*e[:,None]],1).astype(np.float64)
@njit(cache=True)
def band_dtw(A,B,lo,W):
    n=A.shape[0];m=B.shape[0];K=2*W+1;INF=1e18;D=np.full((n,K),INF);P=np.zeros((n,K),np.int8)
    for i in range(n):
        for k in range(K):
            j=lo[i]+k
            if j<0 or j>=m:continue
            c=0.0
            for q in range(A.shape[1]):
                d=A[i,q]-B[j,q];c+=d*d
            c=np.sqrt(c);best=INF;bp=0
            if i==0 and j==0:best=0.0;bp=0
            if i>0:
                kk=j-lo[i-1]   # vertical (i-1,j)
                if 0<=kk<K and D[i-1,kk]<best:best=D[i-1,kk];bp=1
                kk=j-1-lo[i-1] # diagonal
                if 0<=kk<K and D[i-1,kk]<best:best=D[i-1,kk];bp=2
            if k>0 and D[i,k-1]<best:best=D[i,k-1];bp=3   # horizontal (i,j-1)
            if best<INF:D[i,k]=best+c;P[i,k]=bp
    return D,P
def run_dtw(A,B,anchors_ref,anchors_usr,W=150):
    n=len(A);t=np.arange(n)*HOP/SR;g=np.interp(t,anchors_ref,anchors_usr);lo=(np.round(g*SR/HOP).astype(np.int64)-W)
    D,P=band_dtw(A,B,lo,W);K=2*W+1;i=n-1;j=len(B)-1;k=j-lo[i]
    if not(0<=k<K) or D[i,k]>=1e17:k=int(np.argmin(D[i]));j=lo[i]+k
    mp=np.zeros(n);cnt=np.zeros(n)
    while i>=0:
        mp[i]+=j;cnt[i]+=1
        if i==0 and j==0:break
        b=P[i,j-lo[i]]
        if b==1:i-=1
        elif b==2:i-=1;j-=1
        elif b==3:j-=1
        else:break
    cnt[cnt==0]=1;m=mp/cnt*HOP/SR;return np.maximum.accumulate(m)
def speech_mask(x):
    n=len(x)//HOP;f=x[:n*HOP].reshape(n,HOP);e=10*np.log10((f**2).mean(1)+1e-10);e=np.convolve(e,np.ones(3)/3,'same');lo,hi=np.percentile(e,10),np.percentile(e,95);m=e>lo+.33*(hi-lo)
    k=np.ones(5)>0;return np.convolve(m.astype(float),np.ones(5)/5,'same')>.35   # bridge tiny gaps (stop consonants)
def speech_dtw(A,Bf,xr,xu,W=500):
    """DTW on speech frames only (pauses removed on both sides) -> map from reference time to user time."""
    ma=speech_mask(xr)[:len(A)];mb=speech_mask(xu)[:len(Bf)];ia=np.flatnonzero(ma);ib=np.flatnonzero(mb);As=A[ia];Bs=Bf[ib]
    n=len(As);m=len(Bs);ratio=m/n
    g=(np.arange(n)*ratio).astype(np.int64);lo=g-W
    D,P=band_dtw(As,Bs,lo,W);K=2*W+1;i=n-1;j=m-1;k=j-lo[i]
    if not(0<=k<K) or D[i,k]>=1e17:k=int(np.argmin(D[i]));j=lo[i]+k
    mp=np.zeros(n);cnt=np.zeros(n)
    while i>=0:
        mp[i]+=j;cnt[i]+=1
        if i==0 and j==0:break
        b=P[i,j-lo[i]]
        if b==1:i-=1
        elif b==2:i-=1;j-=1
        elif b==3:j-=1
        else:break
    cnt[cnt==0]=1;mp=np.maximum.accumulate(mp/cnt)
    # reference frame (speech index) -> user frame (original index) ; fill pauses by interpolation on frame index
    ur=np.interp(np.arange(len(A)),ia,ib[np.clip(np.round(mp).astype(int),0,m-1)]) if False else None
    uframe_for_ref_speech=ib[np.clip(np.round(mp).astype(int),0,m-1)]
    out=np.interp(np.arange(len(A)),ia,uframe_for_ref_speech.astype(float))
    return np.maximum.accumulate(out)*HOP/SR,ma,mb
def make_ref(ep,refdir):
    if not os.path.exists(refdir+'/timings.json'):subprocess.run(['python3',f'{R}/studio/tts.py',f'{R}/build/ep{ep}/beats.json',refdir],check=True)
    T=json.load(open(refdir+'/timings.json'));parts=[];
    for i,t in enumerate(T):
        subprocess.run(['ffmpeg','-v','error','-y','-i',f'{refdir}/audio/{i:02d}.mp3','-af',f"apad=pad_dur={max(0,t['duration']-t['audio']):.3f}",'-t',f"{t['duration']:.3f}",'-ar','16000','-ac','1',f'{refdir}/audio/p{i:02d}.wav'],check=True);parts.append(f"file '{refdir}/audio/p{i:02d}.wav'\n")
    open(refdir+'/l.txt','w').write(''.join(parts));subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',refdir+'/l.txt','-c','copy',refdir+'/ref.wav'],check=True);return T,refdir+'/ref.wav'
def main():
    ep=sys.argv[1];voice=sys.argv[2];out=os.path.join(R,'build/ep'+ep);refdir=f'/tmp/ref{ep}'
    if '--out' in sys.argv:out=os.path.abspath(sys.argv[sys.argv.index('--out')+1])
    if '--ref' in sys.argv:refdir=os.path.abspath(sys.argv[sys.argv.index('--ref')+1])
    os.makedirs(refdir,exist_ok=True);Tr,refwav=make_ref(ep,refdir)
    B=json.load(open(f'{R}/build/ep{ep}/beats.json',encoding='utf-8'))['scenes']
    xr=load(refwav);xu=load(voice);A=feats(xr);Bf=feats(xu)
    # coarse anchors: start/end of the speech of each beat is found by a first DTW pass without band knowledge -> use proportional map, then refine twice
    m,ma,mb=speech_dtw(A,Bf,xr,xu);ar=np.arange(len(A))*HOP/SR;au=m
    f=lambda t:float(np.interp(t,ar,au))
    off=0.0;starts=[];Tn=[]
    bst=[];off=0.0
    for t in Tr:bst.append(off);off+=t['duration']
    total=len(xu)/SR;ustarts=[]
    for i,t in enumerate(Tr):
        w=t['words'];first=bst[i]+w[0]['start'];prev=bst[i-1]+Tr[i-1]['words'][-1]['end'] if i>0 else 0.0
        uf=f(first);up=f(prev) if i>0 else 0.0;ustarts.append(0.0 if i==0 else (up+uf)/2 if uf-up<.6 else uf-.2)
    uends=ustarts[1:]+[total];os.makedirs(out+'/audio',exist_ok=True);T=[];flag=0
    for i,t in enumerate(Tr):
        a,b=ustarts[i],uends[i];subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a:.3f}','-t',f'{b-a:.3f}','-i',voice,'-ac','1','-ar','44100','-b:a','192k',f'{out}/audio/{i:02d}.mp3'],check=True)
        wl=[]
        for w in t['words']:
            s=f(bst[i]+w['start']);e=f(bst[i]+w['end']);wl.append({'text':w['text'],'start':round(max(0,s-a),3),'end':round(max(s,e)-a,3)})
        for q in range(1,len(wl)):
            if wl[q]['start']<wl[q-1]['start']:wl[q]['start']=wl[q-1]['start']
        T.append({'audio':round(b-a,6),'duration':round(b-a,6),'words':wl,'beat':B[i]['beat']})
    json.dump(T,open(out+'/timings.json','w'),ensure_ascii=False)
    print(f'DTW aligned: voice {total:.1f}s ({total/60:.2f} min), reference {len(xr)/SR:.1f}s, {len(Tr)} beats, mean path speed ratio {total/(len(xr)/SR):.2f}')
    if '--out' not in sys.argv:
        ef=f'{R}/episodes/ep{ep}/episode.json';d=json.load(open(ef));d['target_sec']=round(total,1);d['voice']='user';json.dump(d,open(ef,'w'),ensure_ascii=False)
if __name__=='__main__':main()
