"""Divine BGM (choir pad + harp + deep drone, pure numpy) mixed under a reel's voice.
python3 studio/reel_bgm.py reel15 [reel09 ...]  -> renders/<reel>_bgm_1080x1920.mp4 (video copied, voice kept)"""
import numpy as np,sys,os,subprocess,wave,zlib
from scipy.signal import butter,sosfilt,fftconvolve
SR=44100;R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(m):return 440*2**((m-69)/12)
def bp(x,a,b):return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
def hp(x,c):return sosfilt(butter(2,c,'high',fs=SR,output='sos'),x)
def lp(x,c):return sosfilt(butter(2,c,'low',fs=SR,output='sos'),x)
# progression in semitone offsets from root: i, VI, III, VII style modal (Dorian/Aeolian) -> serene, devotional
PROG=[[0,7,12,15,19],[-4,3,8,12,15],[3,10,15,19,22],[-2,5,10,14,17]]
SCALE=[0,2,3,5,7,8,10,12,14,15,17,19]
def choir(n,notes,rng):
    t=np.arange(n)/SR;out=np.zeros(n)
    for m in notes:
        for dt in(-6,0,6):   # chorus detune (cents)
            fr=f(m)*2**(dt/1200);vib=1+.004*np.sin(2*np.pi*(5+rng.uniform(-.4,.4))*t+rng.uniform(0,6))
            ph=2*np.pi*np.cumsum(fr*vib)/SR
            out+=sum(np.sin(h*ph)/h**1.1 for h in range(1,14))
    # vowel formants "aah/oh"
    v=bp(out,650,900)*1.0+bp(out,1000,1300)*.6+bp(out,2400,3100)*.15+lp(out,400)*.5
    return v/ (len(notes)*3)
def harp(root,dur,rng,tempo):
    n=int(dur*SR)+SR*3;y=np.zeros(n);step=60/tempo/2;i=0;tt=1.0
    pat=[0,2,4,2,5,4,2,3]
    while tt<dur-1:
        ch=PROG[int(tt//8)%4];base=[m+root for m in ch]
        deg=pat[i%8];m=root+SCALE[(deg*1)%len(SCALE)]+12 if rng.random()<.35 else base[deg%len(base)]+12
        fr=f(m);k=int(3*SR);te=np.arange(k)/SR
        s=sum(np.sin(2*np.pi*fr*h*te)*np.exp(-te*(1.6+h*1.3))/h**1.2 for h in range(1,8))
        s*=np.minimum(1,te*400)*(.6+.4*rng.random())
        a=int(tt*SR);y[a:a+k]+=s[:max(0,min(k,n-a))] if a+k<=n else s[:n-a]
        tt+=step*(1 if rng.random()<.8 else 2);i+=1
    return y[:int(dur*SR)]
def reverb(x,sec=3.2):
    n=int(sec*SR);rng=np.random.default_rng(3);ir=rng.standard_normal(n)*np.exp(-np.arange(n)/SR*2.2);ir=lp(ir,5000)
    wet=fftconvolve(x,ir)[:len(x)];wet/=np.max(np.abs(wet))+1e-9;return wet
def make(dur,seed):
    rng=np.random.default_rng(seed);root=[50,52,48,53][seed%4]   # D3,E3,C3,F3
    n=int(dur*SR);seg=8*SR;pad=np.zeros(n)
    for s in range(0,n,seg):
        ch=PROG[(s//seg)%4];L=min(seg+3*SR,n-s)
        m=[root+x for x in ch];c=choir(L,m,rng)
        e=np.ones(L);a=min(L,int(2.5*SR));e[:a]=np.linspace(0,1,a)**1.5;r=min(L,int(3*SR));e[-r:]*=np.linspace(1,0,r)
        pad[s:s+L]+=c*e
    drone=lp(sum(np.sin(2*np.pi*f(root-12)*k*np.arange(n)/SR)/k for k in(1,2,3)),400)*.5
    hp=harp(root,dur,rng,seed%3*6+60)
    wet=reverb(pad*1.0+hp*.8)
    mix=pad*.55+drone*.25+hp*.5+wet*.9
    fade=np.minimum(1,np.minimum(np.arange(n)/(2*SR),(n-np.arange(n))/(3*SR)));mix*=fade
    return mix/np.max(np.abs(mix))
def tense(dur,seed):
    """Suspense/drama: sub drone, dissonant string cluster with tremolo, heartbeat, risers, hits."""
    rng=np.random.default_rng(seed);n=int(dur*SR);t=np.arange(n)/SR;root=38+seed%3
    sub=np.sin(2*np.pi*f(root)*t)*(.7+.3*np.sin(2*np.pi*.1*t))
    cl=np.zeros(n)
    for m in(root+12,root+13,root+18,root+19):   # minor-2nd / tritone cluster
        ph=2*np.pi*np.cumsum(f(m)*(1+.003*np.sin(2*np.pi*4.5*t+m)))/SR
        cl+=sum(np.sin(h*ph)/h for h in range(1,10))
    cl=lp(cl,2500)*(.35+.65*(.5+.5*np.sin(2*np.pi*(.07+.02*(seed%3))*t)))*(.5+.5*np.sin(2*np.pi*9*t)*.5+.25)
    cl*=np.minimum(1,t/6)**2*(1+.8*t/dur)/1.8      # slowly intensifies
    hb=np.zeros(n);bpm=62+36*np.arange(n)/n/SR*0
    k=0.0
    while k<dur-1:
        for off,g in((0,1),(.32,.6)):
            a=int((k+off)*SR);L=int(.35*SR);tt=np.arange(L)/SR
            if a+L<n:hb[a:a+L]+=g*np.sin(2*np.pi*(95-120*tt)*tt)*np.exp(-tt*11)
        k+=1.0-.45*k/dur                            # heartbeat speeds up
    hits=np.zeros(n)
    for c in np.arange(7,dur-2,rng.uniform(9,13)):   # distant impacts + risers
        a=int(c*SR);L=int(3*SR)
        if a+L>=n:break
        tt=np.arange(L)/SR;noise=lp(rng.standard_normal(L),900)
        hits[a:a+L]+=(np.sin(2*np.pi*(60-20*tt)*tt)+noise*.5)*np.exp(-tt*2.2)
        a0=max(0,a-int(3*SR));rl=a-a0;rn=bp(rng.standard_normal(rl),500,3000)*np.linspace(0,1,rl)**3;hits[a0:a]+=rn*.4
    wet=reverb(cl+hits*.7,2.8)
    mix=sub*.5+cl*.7+hb*.8+hits*.9+wet*.7
    fade=np.minimum(1,np.minimum(t/2,(dur-t)/3));mix*=fade
    return mix/np.max(np.abs(mix))
def war(dur,seed):
    """Battle: taiko/war drums with driving rhythm, low brass-like power drone, cymbal-like noise swells, rising tempo."""
    rng=np.random.default_rng(seed);n=int(dur*SR);t=np.arange(n)/SR;root=38+seed%3
    def drum(freq,L,g,dec):
        tt=np.arange(L)/SR;return g*(np.sin(2*np.pi*(freq+freq*1.4*np.exp(-tt*30))*tt)+.25*lp(rng.standard_normal(L),1500)*np.exp(-tt*40))*np.exp(-tt*dec)
    dr=np.zeros(n);bpm=96.;b=0.0;i=0
    # pattern per bar of 8 eighths: big=low taiko, mid=hi taiko
    PAT=[(1,1.0),(0,0),(1,.55),(1,.7),(2,.9),(0,0),(1,.6),(2,.8)]
    while b<dur-.6:
        kind,g=PAT[i%8]
        if kind:
            L=int(.55*SR);a=int(b*SR)
            if a+L<n:dr[a:a+L]+=drum(55 if kind==1 else 95,L,g*(.8+.2*rng.random()),7 if kind==1 else 11)
        if i%16==0 and b>2:   # crash + roll before each phrase
            for j in range(6):
                a=int((b-.5+j*.08)*SR);L=int(.25*SR)
                if 0<=a and a+L<n:dr[a:a+L]+=drum(120,L,.25+.08*j,16)
        bpm=96+34*b/dur;b+=60/bpm/2;i+=1
    # drums + plain steady bass (sub + 2nd harmonic, constant level)
    br=np.sin(2*np.pi*f(root)*t)+.5*np.sin(2*np.pi*f(root)*2*t)
    br/=np.max(np.abs(br))
    dn=dr/np.max(np.abs(dr))
    mix=dn*1.0+br*.35
    mix=np.tanh(mix*1.6)
    fade=np.minimum(1,np.minimum(t/.6,(dur-t)/2.5));mix*=fade
    return mix/np.max(np.abs(mix))
def run(reel,seed):
    src=f'{R}/renders/{reel}_1080x1920.mp4';out=f'{R}/renders/{reel}_bgm_1080x1920.mp4'
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
    m=make(dur,seed);w=f'/tmp/{reel}_bgm.wav'
    with wave.open(w,'wb') as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(SR);o.writeframes((m*32000).astype('<i2').tobytes())
    # music ~ -20 dB under voice, ducked further while voice speaks
    fc=("[1:a]volume=0.22[m];[0:a]asplit[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600[md];"
        "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
    subprocess.check_call(['ffmpeg','-y','-v','error','-i',src,'-i',w,'-filter_complex',fc,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k',out])
    print(out)
if __name__=='__main__':
    for r in sys.argv[1:]:run(r,zlib.crc32(r.encode())%1000)
