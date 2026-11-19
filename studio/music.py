"""Procedural background score + SFX for an episode, timed to its beats and visual events (thunder, impacts).
python3 studio/music.py 03   -> renders/ep03_music.wav/.mp3   (no external assets; pure numpy)"""
import numpy as np,json,sys,os,subprocess
from scipy.signal import butter,sosfilt,oaconvolve
SR=44100;R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));rng=np.random.default_rng(7)
N={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def hz(n):# 'D3','Eb3','F#4'
    k=N[n[0]];i=1
    while n[i] in '#b':k+=1 if n[i]=='#' else -1;i+=1
    return 440*2**((k+12*(int(n[i:])+1)-69)/12)
def T(n):return np.arange(n)/SR
def lp(x,f,o=2):return sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
def bp(x,a,b,o=2):return sosfilt(butter(o,[a,b],'band',fs=SR,output='sos'),x)
def hp(x,f,o=2):return sosfilt(butter(o,f,'high',fs=SR,output='sos'),x)
def osc(f,n,harm=6,pw=1.3,vib=.002,vh=5.2,ph0=0):
    t=T(n);ph=2*np.pi*f*t*(1+vib*np.sin(2*np.pi*vh*t+ph0));return sum(np.sin(h*ph)/h**pw for h in range(1,harm+1))
def swell(n,a,r):e=np.ones(n);na=min(n,int(a*SR));nr=min(n,int(r*SR));e[:na]=np.linspace(0,1,na)**1.5;e[n-nr:]*=np.linspace(1,0,nr)**1.5;return e
def pad(notes,n,bright=1.0,a=2.5,r=3.0,trem=0):
    x=np.zeros(n)
    for nt in notes:
        f=hz(nt)
        for dt in(-.0025,.0,.0025):x+=osc(f*(1+dt),n,harm=int(4+3*bright),pw=1.4-.3*bright,ph0=rng.uniform(0,6))
    x*=swell(n,a,r)
    if trem:x*=1-trem+trem*np.sin(2*np.pi*5.5*T(n))
    return x/len(notes)/3
def pluck(f,d=1.6):
    n=int(d*SR);t=T(n);return sum(np.sin(2*np.pi*f*h*t)*np.exp(-t*(2+h*1.8))/h for h in range(1,7))
def bell(f,d=4.0):
    n=int(d*SR);t=T(n);return sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*dc) for r,a,dc in[(1,1,1.1),(2.76,.6,1.6),(5.4,.4,2.4),(8.9,.2,3.4)])*np.minimum(1,t*200)
def kick(d=.7,f0=150,f1=42):
    n=int(d*SR);t=T(n);fr=f1+(f0-f1)*np.exp(-t*22);return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*7)
def drum(d=.5,f=95):
    n=int(d*SR);t=T(n);return np.sin(2*np.pi*f*t*(1+.5*np.exp(-t*30)))*np.exp(-t*9)+.4*bp(rng.standard_normal(n),150,2200)*np.exp(-t*20)
def boom(d=3.2):
    n=int(d*SR);t=T(n);fr=28+40*np.exp(-t*3);return (np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*1.3)+.5*lp(rng.standard_normal(n),260)*np.exp(-t*2.2)+.25*bp(rng.standard_normal(n),300,3000)*np.exp(-t*9))
def thunder(d=5.5):
    n=int(d*SR);t=T(n);crack=bp(rng.standard_normal(n),600,6000)*np.exp(-t*14)*1.0
    roll=lp(np.cumsum(rng.standard_normal(n))*.0006,180);roll=roll-np.mean(roll)
    bumps=sum(np.exp(-((t-c)**2)/(2*w*w)) for c,w in zip(np.sort(rng.uniform(.2,d*.7,6)),rng.uniform(.15,.5,6)))
    return crack*.9+ lp(rng.standard_normal(n),320)*(.6*np.exp(-t*.55)+.5*bumps*np.exp(-t*.4))+roll*np.exp(-t*.5)*3
def riser(n):
    t=T(n);u=t/(n/SR);nz=hp(rng.standard_normal(n),900)*u**2*.6;fr=90+900*u**2;return (np.sin(2*np.pi*np.cumsum(fr)/SR)*u**1.5*.6+nz)*np.minimum(1,(1-u)*30+.0)
def place(buf,x,t0,g=1.0):
    i=int(t0*SR)
    if i>=len(buf):return
    j=min(len(buf),i+len(x));buf[i:j]+=x[:j-i]*g
# scales
HIJ=['D4','Eb4','F#4','G4','A4','Bb4','C5','D5'];PENT=['D4','E4','F#4','A4','B4','D5','E5','F#5'];MIN=['D4','F4','G4','A4','C5','D5']
def seg(mood,n,seed):
    r=np.random.default_rng(seed);x=np.zeros(n);d=n/SR
    def hits(period,fn,g,jit=.15,scale=None,lo=0):
        t=lo+r.uniform(0,period)
        while t<d-.5:
            place(x,fn(hz(scale[r.integers(len(scale))])) if scale else fn(),t,g);t+=period*r.uniform(1-jit,1+jit)
    drone=lambda f,g:x.__iadd__(.4*g*(osc(f,n,3,1.0,.0015)+.5*osc(f*1.5,n,2,1.0,.002))*swell(n,3,3))
    if mood=='mystery':drone(hz('D2'),.5);x+=pad(['D3','Eb3','A3'],n,.4)*.5;hits(7,lambda f:bell(f,5),.16,scale=HIJ)
    elif mood=='grave':drone(hz('D2'),.55);x+=pad(['D3','F3','A3'],n,.5)*.6;hits(4.2,kick,.35,.05);hits(9,lambda f:bell(f/2,6),.14,scale=MIN)
    elif mood=='awe':x+=pad(['D3','A3','E4','F#4'],n,1.0,4,4)*.9;hits(.9,lambda f:pluck(f,1.4),.13,scale=PENT);hits(10,lambda f:bell(f,6),.12,scale=PENT)
    elif mood=='wonder':x+=pad(['D3','A3','B3','F#4'],n,.9,3,3)*.7;hits(.55,lambda f:pluck(f,1.0),.1,.3,PENT)
    elif mood=='grand':x+=pad(['D3','A3','D4','F#4','A4'],n,1.3,2,3)*1.0;hits(3.4,lambda:drum(.8,70),.75,.02);hits(6,lambda f:bell(f,6),.16,scale=PENT)
    elif mood=='triumph':x+=pad(['D3','A3','D4','F#4','A4','D5'],n,1.5,1.5,3)*1.1;hits(2.2,lambda:drum(.8,75),.75,.02);hits(.5,lambda f:pluck(f,1.2),.1,.2,PENT);hits(5,lambda f:bell(f,6),.17,scale=PENT)
    elif mood=='calm':x+=pad(['D3','F#3','A3','B3'],n,.7,3,3)*.8;hits(5,lambda f:pluck(f/2,2.4),.2,scale=PENT)
    elif mood=='warm':x+=pad(['D3','A3','B3','E4'],n,.9,2.5,3)*.85;hits(1.6,lambda f:pluck(f,1.6),.14,.25,PENT)
    elif mood=='sad':x+=pad(['D3','F3','A3','C4'],n,.5,3,3.5,.12)*.8;hits(6.5,lambda f:bell(f/2,6),.13,scale=MIN)
    elif mood=='dread':
        drone(hz('D1')*2,.6);x+=pad(['D3','Eb3','A3'],n,.3,3,3,.3)*.55;x+=.05*bp(r.standard_normal(n),3000,5200)*(.5+.5*np.sin(2*np.pi*.18*T(n)))
        bpm=52;t0=0
        while t0<d-.6:place(x,kick(.7,110,38),t0,.28+.3*t0/d);place(x,kick(.7,110,38),t0+.28,.17+.2*t0/d);t0+=60/bpm*(1-.25*t0/d)
    elif mood=='cold':drone(hz('D1')*2,.45);hits(5,lambda f:bell(f*2,6),.1,scale=['A4','D5','Eb5'])
    elif mood=='tense':
        x+=pad(['D3','Eb3','G#3'],n,.4,2,2,.25)*.6;t0=0;bpm=84
        while t0<d-.4:place(x,kick(.6,120,40),t0,.38);t0+=60/bpm
        hits(.36,lambda f:pluck(f,.3),.045,.05,['D5','D5','Eb5'])
    elif mood=='war':
        x+=pad(['D2','A2','D3','Eb3'],n,1.0,.6,1.5,.15)*1.5;bpm=132;b=60/bpm;t0=0;k=0
        pat=[1,0,.6,0,1,.5,.6,0,1,0,.6,.5,1,0,.7,.5]
        while t0<d-.3:
            v=pat[k%16]
            if v:place(x,drum(.6,62 if k%4==0 else 100),t0,1.0*v)
            k+=1;t0+=b/2
        hits(2*b*4,lambda:thunder(5),.5,.4)
    elif mood=='teaser':x+=pad(['D3','A3','Bb3','F4'],n,.8,2,3)*.7;hits(1.3,lambda f:pluck(f,1.4),.13,.3,HIJ)
    return x
def build(ep):
    tim=json.load(open(f'{R}/build/ep{ep}/engine_timings.json'));durs=[b['duration'] for b in tim];starts=np.concatenate([[0],np.cumsum(durs)])
    total=float(starts[-1])+2;n=int(total*SR);mix=np.zeros(n);M=MOODS[ep]
    for i,b in enumerate(tim):
        beat=b['beat'];mood=M.get(beat,'calm');t0=starts[i];nn=int((durs[i]+3.0)*SR);s=seg(mood,nn,1000+beat)
        s*=np.minimum(1,np.arange(nn)/(SR*2.2))*np.minimum(1,np.arange(nn)[::-1]/(SR*2.2))  # 2.2 s crossfade
        place(mix,s,t0-1.1 if t0>1.1 else 0,.9)
        if beat in RISE[ep]:  # suspense build into the next beat
            L=int(min(5.0,durs[i])*SR);place(mix,riser(L)*.5,t0+durs[i]-L/SR+.2)
        if beat in HIT[ep]:place(mix,boom(),t0+durs[i]+.05,.9)
    # visual-event SFX from the shot list
    sh=json.load(open(f'{R}/episodes/ep{ep}/shots.json'));last=-9
    for s in sh:
        fx=(s.get('sc') or {}).get('fx',[]);at=s['at']
        if at-last<1.2:continue
        kinds=[(x['t'],x.get('src','')) for x in fx]
        if any('lightning' in k[1] or 'thunder' in k[1] or k[0]=='bolt' for k in kinds):place(mix,thunder(5.5),at,.85);last=at
        elif any(k[0]=='shock' for k in kinds):place(mix,boom(2.6),at,.7);last=at
        elif any(k[0]=='flash' for k in kinds):place(mix,boom(1.8),at,.45);last=at
    mix*=np.minimum(1,np.arange(n)[::-1]/(SR*3.0))  # tail fade
    wet=oaconvolve(mix,(rng.standard_normal(int(2.2*SR))*np.exp(-T(int(2.2*SR))*2.2))*.012,mode='full')[:n];mix=mix+.8*wet
    L=mix;Rr=np.concatenate([np.zeros(int(.012*SR)),mix[:-int(.012*SR)]])*.95
    st=np.stack([L,Rr],1);st/=np.max(np.abs(st))*1.1
    import wave;out=f'{R}/renders/ep{ep}_music';os.makedirs(f'{R}/renders',exist_ok=True)
    pcm=(st*32767).astype('<i2');w=wave.open(out+'.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes());w.close()
    subprocess.check_call(['ffmpeg','-loglevel','error','-y','-i',out+'.wav','-af','loudnorm=I=-20:TP=-2','-b:a','192k',out+'.mp3']);print('music',out,round(total),'s')
MOODS={'03':{1:'sad',2:'grand',3:'awe',4:'tense',5:'dread',6:'tense',7:'war',8:'dread',9:'sad',10:'grave',11:'calm',12:'triumph',13:'calm',14:'warm',15:'sad',16:'sad',17:'mystery',18:'sad',19:'warm',20:'mystery',21:'warm',22:'grave',23:'awe',24:'wonder',25:'grand',26:'warm',27:'triumph',28:'warm',29:'dread',30:'calm'},
'01':{1:'mystery',2:'mystery',3:'grave',4:'awe',5:'grave',6:'wonder',7:'grand',8:'grand',9:'calm',10:'dread',11:'dread',12:'tense',13:'tense',14:'sad',15:'warm',16:'war',17:'tense',18:'dread',19:'cold',20:'tense',21:'triumph',22:'sad',23:'calm',24:'mystery',25:'teaser'}}
RISE={'03':{3,5,6,22},'01':{3,9,15,19,20}};HIT={'03':{3,22},'01':{4,15,20,24}}
if __name__=='__main__':build(sys.argv[1])
