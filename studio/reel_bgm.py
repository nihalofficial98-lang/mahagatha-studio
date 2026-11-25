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
def cosmic(dur,seed):
    """Divine/interstellar: pipe-organ drone + steady organ ostinato. Constant level, no vibrato, no tremolo, no swells."""
    rng=np.random.default_rng(seed);n=int(dur*SR);t=np.arange(n)/SR;root=50+seed%3
    def organ(fr,tt):return sum(a*np.sin(2*np.pi*fr*h*tt) for h,a in((1,1),(2,.6),(3,.35),(4,.25),(6,.15),(8,.08)))
    drone=sum(organ(f(root+k),t) for k in(-24,-12,-5,0))*.25     # fixed sustained chord, constant
    # steady choir "ooh" pad on the same chord (no vibrato, constant), high airy shimmer, sparse soft bells
    ch=np.zeros(n)
    for k in(0,7,12,16,19):
        for dt in(-5,5):ch+=sum(np.sin(2*np.pi*f(root+12+k)*2**(dt/1200)*h*t)/h**1.3 for h in range(1,12))
    ch=bp(ch,500,1200)+.5*bp(ch,1800,2800)+.4*lp(ch,300)
    ch*=.35/np.max(np.abs(ch))
    shim=sum(np.sin(2*np.pi*f(root+36+k)*t) for k in(0,7,12))*.025
    bells=np.zeros(n);x=3.0
    while x<dur-3:
        fr=f(root+24+rng.choice([0,7,12,14,16,19]));L=int(4*SR);tt=np.arange(L)/SR
        bl=sum(am*np.sin(2*np.pi*fr*r*tt)*np.exp(-tt*dc) for r,am,dc in((1,1,.9),(2,.4,1.4),(3,.2,2)))*np.minimum(1,tt*300)
        a=int(x*SR);e=min(L,n-a);bells[a:a+e]+=bl[:e]*.09;x+=rng.uniform(4,8)
    wet=reverb(ch*.5+bells,3.0)
    mix=drone*.9+ch*.5+shim+bells+wet*.5
    fade=np.minimum(1,np.minimum(t/2,(dur-t)/3));mix*=fade
    return mix/np.max(np.abs(mix))
def dark(dur,seed):
    """Cruel/dark: steady sub drone, dissonant low cluster (minor 2nd + tritone), cold hollow tone, rare deep gong hits. Constant level, no swells or wobble."""
    rng=np.random.default_rng(seed);n=int(dur*SR);t=np.arange(n)/SR;root=33+seed%3
    sub=np.sin(2*np.pi*f(root)*t)+.5*np.sin(2*np.pi*f(root)*2*t)
    cl=np.zeros(n)
    for k in(0,1,6,13):   # root, minor 2nd, tritone, minor 9th: harsh and cold
        cl+=sum(np.sin(2*np.pi*f(root+12+k)*h*t)/h**1.2 for h in range(1,9))
    cl=lp(cl,1800);cl/=np.max(np.abs(cl))
    hol=bp(rng.standard_normal(n),180,420)*8      # hollow cold wind-like bed, constant
    hol/=np.max(np.abs(hol))
    gong=np.zeros(n);x=6.0
    while x<dur-4:
        fr=f(root+rng.choice([0,1,6]));L=int(5*SR);tt=np.arange(L)/SR
        g=sum(am*np.sin(2*np.pi*fr*r*tt)*np.exp(-tt*dc) for r,am,dc in((1,1,.5),(1.47,.6,.7),(2.09,.5,.9),(3.3,.3,1.4)))*np.minimum(1,tt*400)
        a=int(x*SR);e=min(L,n-a);gong[a:a+e]+=g[:e];x+=rng.uniform(9,14)
    gong/=np.max(np.abs(gong))+1e-9
    wet=reverb(cl*.3+gong*.8,3.5)
    mix=sub*.55+cl*.35+hol*.12+gong*.5+wet*.45
    fade=np.minimum(1,np.minimum(t/2,(dur-t)/3));mix*=fade
    return mix/np.max(np.abs(mix))
def ks(fr,L,rng,decay=.996,bright=.5):
    N=int(SR/fr);buf=rng.uniform(-1,1,N)*1.0;out=np.zeros(L)
    for i in range(L):
        out[i]=buf[i%N];buf[i%N]=decay*(bright*buf[i%N]+(1-bright)*buf[(i+1)%N])
    return out
def nolan(dur,seed):
    """Nolan/Zimmer style (original): ticking clock, endlessly rising Shepard tone, huge low organ-brass hits."""
    rng=np.random.default_rng(seed);n=int(dur*SR);t=np.arange(n)/SR;root=38
    sh=np.zeros(n);T0=40.0
    for k in range(8):
        ph=((t/T0)+k/8)%1.0;fr=f(root)*2**(ph*8)      # 8 octaves glide, wrap
        amp=np.sin(np.pi*ph)**2;sh+=amp*np.sin(2*np.pi*np.cumsum(fr)/SR)
    sh=lp(sh,2500)/8
    drone=sum(np.sin(2*np.pi*f(root-12+k)*h*t)/h for k in(0,7) for h in(1,2,3,4))*.3
    tick=np.zeros(n);k=0.0
    while k<dur-1:
        a=int(k*SR);L=int(.08*SR);tt=np.arange(L)/SR
        tick[a:a+L]+=np.sin(2*np.pi*1900*tt)*np.exp(-tt*90)+.4*lp(rng.standard_normal(L),6000)*np.exp(-tt*120);k+=1.0 if k<dur*.5 else .5
    hits=np.zeros(n);x=8.0
    while x<dur-3:
        a=int(x*SR);L=int(4*SR);tt=np.arange(L)/SR
        h=sum(np.sin(2*np.pi*f(root-12+k2)*q*tt)/q for k2 in(0,7,12) for q in(1,2,3))*np.exp(-tt*1.2)+lp(rng.standard_normal(L),500)*np.exp(-tt*3)
        e=min(L,n-a);hits[a:a+e]+=h[:e]*np.minimum(1,tt[:e]*200);x+=rng.uniform(10,14)
    wet=reverb(hits*.8+drone*.3,3.0)
    mix=sh*.35+drone*.5+tick*.5+hits*.7+wet*.5
    mix*=np.minimum(1,np.minimum(t/2,(dur-t)/3));return mix/np.max(np.abs(mix))
def spielberg(dur,seed):
    """Spielberg/Williams style (original): warm string bed, a heroic French-horn theme, harp glints, wonder."""
    rng=np.random.default_rng(seed);n=int(dur*SR);t=np.arange(n)/SR;root=50
    chords=[[0,4,7,12],[-3,0,4,9],[-5,-1,2,7],[0,4,7,12]]   # I vi V I-ish
    pad=np.zeros(n);bar=6.0
    for s0 in range(0,n,int(bar*SR)):
        L=min(int((bar+1.5)*SR),n-s0);tt=np.arange(L)/SR;c=chords[(s0//int(bar*SR))%4]
        v=sum(sum(np.sin(2*np.pi*f(root+k+12)*(1+dt)*q*tt)/q**1.2 for q in range(1,9))for k in c for dt in(-.003,.003))
        e=np.minimum(1,tt/1.2)*np.minimum(1,(L/SR-tt)/1.5);pad[s0:s0+L]+=lp(v,3500)*e
    pad/=np.max(np.abs(pad))
    th=[(0,2),(4,1),(7,1),(9,2),(7,1),(4,1),(2,2),(4,1),(5,1),(7,3),(0,2),(2,1),(4,1),(7,2),(12,2),(11,1),(9,1),(7,4)]  # original theme, (semitone,beats)
    mel=np.zeros(n);x=2.0;bt=.62;i=0
    while x<dur-3:
        k,b=th[i%len(th)];L=int(b*bt*SR*1.15);tt=np.arange(L)/SR
        h=lp(sum(np.sin(2*np.pi*f(root+12+k)*q*tt)/q for q in range(1,10)),1800)*np.minimum(1,tt*12)*np.minimum(1,(L/SR-tt)*10)
        a=int(x*SR);e=min(L,n-a);mel[a:a+e]+=h[:e];x+=b*bt;i+=1
        if i%len(th)==0:x+=2.5
    harp=np.zeros(n);x=1.0
    while x<dur-2:
        fr=f(root+24+rng.choice([0,4,7,12]));L=int(2.5*SR);tt=np.arange(L)/SR
        h=sum(np.sin(2*np.pi*fr*q*tt)*np.exp(-tt*(2+q))/q for q in range(1,5))
        a=int(x*SR);e=min(L,n-a);harp[a:a+e]+=h[:e];x+=rng.uniform(2.5,5)
    mel/=np.max(np.abs(mel))
    wet=reverb(pad*.3+mel*.5+harp*.2,2.6)
    mix=pad*.4+mel*.45+harp*.12+wet*.5
    mix*=np.minimum(1,np.minimum(t/2,(dur-t)/3));return mix/np.max(np.abs(mix))
def tarantino(dur,seed):
    """Tarantino-style (original): spaghetti-western/surf cool - twangy reverb guitar riff, fat bass, tight drums, a lonely whistle."""
    rng=np.random.default_rng(seed);n=int(dur*SR);t=np.arange(n)/SR;bpm=104;sp=60/bpm/2;root=40
    riff=[0,0,3,0,5,0,3,7,0,0,3,0,5,3,2,0]   # E-minor-ish, original riff
    gt=np.zeros(n);bs=np.zeros(n);dr=np.zeros(n);i=0;x=0.0
    while x<dur-1:
        k=riff[i%16];a=int(x*SR);L=int(.55*SR)
        if a+L<n:
            g=ks(f(root+24+k),L,rng,.998,.5)*np.exp(-np.arange(L)/SR*3.5);gt[a:a+L]+=g
            bs[a:a+L]+=np.sin(2*np.pi*f(root+k-12)*np.arange(L)/SR)*np.exp(-np.arange(L)/SR*5)*(1 if i%2==0 else .6)
        if i%4==0 and a+int(.3*SR)<n:
            tt=np.arange(int(.3*SR))/SR;dr[a:a+len(tt)]+=np.sin(2*np.pi*(130+120*np.exp(-tt*40))*tt)*np.exp(-tt*14)
        if i%4==2 and a+int(.2*SR)<n:
            tt=np.arange(int(.2*SR))/SR;dr[a:a+len(tt)]+=.5*hp(rng.standard_normal(len(tt)),1500)*np.exp(-tt*25)
        if i%2==1 and a+int(.06*SR)<n:
            tt=np.arange(int(.06*SR))/SR;dr[a:a+len(tt)]+=.15*hp(rng.standard_normal(len(tt)),6000)*np.exp(-tt*80)
        x+=sp;i+=1
    wh=np.zeros(n);x=8.0
    for _ in range(int(dur//16)):
        for k,b in((0,.8),(3,.4),(5,.4),(7,1.5)):
            L=int(b*SR*.95);tt=np.arange(L)/SR;v=np.sin(2*np.pi*f(root+36+k)*tt*(1+.004*np.sin(2*np.pi*6*tt)))*np.minimum(1,tt*20)*np.minimum(1,(L/SR-tt)*10)
            a=int(x*SR);e=min(L,n-a)
            if e>0:wh[a:a+e]+=v[:e]*.3
            x+=b
        x+=16-3.1
    wet=reverb(gt*.8+wh*.5,1.8)
    mix=gt*.5+bs*.5+dr*.5+wh*.35+wet*.6
    mix*=np.minimum(1,np.minimum(t/1,(dur-t)/2));return mix/np.max(np.abs(mix))
def lament(dur,seed):
    """Dark low bass bed, distant muted trumpet playing a slow sad minor melody, deep gongs for death and cruelty."""
    rng=np.random.default_rng(seed);n=int(dur*SR);t=np.arange(n)/SR;root=31
    bass=np.sin(2*np.pi*f(root)*t)+.6*np.sin(2*np.pi*f(root)*2*t)+.25*np.sin(2*np.pi*f(root+7)*t)
    bass=bass/np.max(np.abs(bass))
    hol=lp(sum(np.sin(2*np.pi*f(root+12+k)*h*t)/h for k in(0,3,7) for h in(1,2,3)),700);hol/=np.max(np.abs(hol))
    # sad minor melody (original), (semitone from root, beats); trumpet = bright saw lowpassed, soft slow attack, slight scoop
    mel=[(12,3),(15,1),(14,2),(10,2),(12,4),(None,2),(15,2),(17,2),(15,1),(14,1),(12,2),(10,2),(7,5),(None,3)]
    tr=np.zeros(n);x=5.0;bt=.9;i=0
    while x<dur-6:
        k,b=mel[i%len(mel)];i+=1
        if k is not None:
            L=int(b*bt*SR*1.05);tt=np.arange(L)/SR;fr=f(root+24+k)*(1-.02*np.exp(-tt*14))
            ph=2*np.pi*np.cumsum(fr*(1+.003*np.sin(2*np.pi*5*tt)))/SR
            v=lp(sum(np.sin(q*ph)/q**.9 for q in range(1,14)),2200)
            v*=np.minimum(1,tt*5)*np.minimum(1,(L/SR-tt)*4)
            a=int(x*SR);e=min(L,n-a);tr[a:a+e]+=v[:e]
        x+=b*bt
        if i%len(mel)==0:x+=6
    tr/=np.max(np.abs(tr))+1e-9
    gong=np.zeros(n);x=9.0
    while x<dur-5:
        fr=f(root+rng.choice([0,0,3,-2]));L=int(7*SR);tt=np.arange(L)/SR
        g=sum(am*np.sin(2*np.pi*fr*r*tt)*np.exp(-tt*dc) for r,am,dc in((1,1,.35),(1.47,.7,.5),(2.09,.6,.7),(2.9,.4,1.0),(4.1,.25,1.5)))*np.minimum(1,tt*300)+.2*lp(rng.standard_normal(L),800)*np.exp(-tt*4)
        a=int(x*SR);e=min(L,n-a);gong[a:a+e]+=g[:e];x+=rng.uniform(11,16)
    gong/=np.max(np.abs(gong))+1e-9
    far=reverb(tr,4.5);far=lp(far,2200)      # distance: mostly reverb, dulled
    mix=bass*.6+hol*.18+tr*.12+far*.55+gong*.55+reverb(gong,3.5)*.3
    mix*=np.minimum(1,np.minimum(t/3,(dur-t)/4));return mix/np.max(np.abs(mix))
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
