"""Render a sound_cues.json into a finished score with REAL sampled instruments (General MIDI soundfont via fluidsynth) plus procedural SFX,
timed to the owner's voice and ducked under it.   python3 studio/score.py 93
Outputs: renders/epNN_score_music_only.mp3, renders/epNN_score_with_voice.mp3 (and the stems' mix wav)."""
import json,sys,os,subprocess,re,math,tempfile
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter,sosfilt,oaconvolve
import pretty_midi
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import music as M   # boom(), riser(), thunder(), bell() procedural sounds
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));SR=44100;SF='/usr/share/sounds/sf2/FluidR3_GM.sf2'
PC={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def pcof(n):
    v=PC[n[0]]
    for ch in n[1:]:v+=1 if ch=='#' else -1 if ch=='b' else 0
    return v%12
MODES={'bhairav':[0,1,4,5,7,8,11],'yaman':[0,2,4,6,7,9,11],'marwa':[0,1,4,6,7,9,11],'malkauns':[0,3,5,8,10],'darbari':[0,2,3,5,7,8,10],'todi':[0,1,3,6,7,8,11],'bhairavi':[0,1,3,5,7,8,10],
 'minor':[0,2,3,5,7,8,10],'phrygian':[0,1,3,5,7,8,10],'dorian':[0,2,3,5,7,9,10],'lydian':[0,2,4,6,7,9,11],'harmonic minor':[0,2,3,5,7,8,11],'major':[0,2,4,5,7,9,11]}
# (keyword, GM program 0-based, motif base midi note)
INST=[('tremolo',44,50),('strings',48,50),('choir',52,50),('voice',53,62),('organ',19,62),('harp',46,62),('flute',73,74),('santoor',15,74),('timpani',47,38),('tuba',58,38),('taiko',116,38),
      ('sitar',104,50),('tanpura',104,38),('bell',14,74),('shehnai',111,74),('cello',42,50),('horn',60,50),('trombone',57,50),('pad',89,50),('bansuri',73,74),('pan',75,74),('brass',61,50),('piano',0,62)]
def inst_of(name):
    n=(name or '').lower()
    for k,p,b in INST:
        if k in n:return p,b
    return 48,50
def degree_note(d,mode,key,base):
    sc=MODES.get((mode or 'minor').lower(),MODES['minor']);L=len(sc);i=d-1
    return base+(pcof(key)-pcof('D'))+sc[i%L]+12*(i//L)
def chord_notes(ch,base):
    if re.match(r'^[A-G][#b]?\d$',ch):                                  # single note with octave, e.g. D5
        return [12*(int(ch[-1])+1)+pcof(ch[:-1])]
    m=re.match(r'^([A-G][#b]?)(m)?(?:/([A-G][#b]?))?$',ch)
    if not m:return [base]
    r=pcof(m.group(1));rt=36+r;mid=base+((r-pcof('D'))%12);third=3 if m.group(2) else 4
    ns=[mid,mid+third,mid+7]
    if m.group(3):ns.append(36+pcof(m.group(3)))
    else:ns.append(rt)
    return ns
def fs_render(pm,tail):
    with tempfile.TemporaryDirectory() as td:
        mid=td+'/a.mid';wav=td+'/a.wav';pm.write(mid)
        subprocess.run(['fluidsynth','-ni','-q','-R','0','-C','0','-g','0.9','-F',wav,'-r',str(SR),SF,mid],check=True,capture_output=True)
        sr,x=wavfile.read(wav);x=x.astype(np.float32)/32768.0
    return x if x.ndim==2 else np.stack([x,x],1)
def lp(x,f):return sosfilt(butter(2,f,'low',fs=SR,output='sos'),x,axis=0)
def hp(x,f):return sosfilt(butter(2,f,'high',fs=SR,output='sos'),x,axis=0)
def env(n,fi,fo,hard_end):
    e=np.ones(n);a=int(min(n,fi*SR));
    if a>0:e[:a]=np.linspace(0,1,a)**1.5
    b=int(min(n,fo*SR))
    if hard_end and b>0:e[n-b:]*=np.linspace(1,0,b)**1.5
    return e
def addp(a,b):
    n=max(len(a),len(b));o=np.zeros((n,2),np.float32);o[:len(a)]+=a;o[:len(b)]+=b;return o
def stereo(x):return x if x.ndim==2 else np.stack([x,x],1)
# --- procedural sounds (stereo) ---
def gong(d=6.0,f=62):
    n=int(d*SR);t=np.arange(n)/SR;x=sum(a*np.sin(2*np.pi*f*r*t+np.sin(t*3)*0.3)*np.exp(-t*dc) for r,a,dc in[(1,1,.5),(1.52,.7,.7),(2.3,.5,.9),(3.1,.4,1.3),(4.6,.25,1.8)])*np.minimum(1,t*60);return stereo(x*.5)
def shankh(d,f=146.8):
    n=int(d*SR);t=np.arange(n)/SR;ph=2*np.pi*f*t*(1+.004*np.sin(2*np.pi*5*t))
    x=sum(np.sin(h*ph)/h**1.1 for h in range(1,9))*(np.minimum(1,t/.5)*np.minimum(1,(d-t)/.8));nz=np.random.default_rng(1).standard_normal(n);nz=sosfilt(butter(2,[900,2500],'band',fs=SR,output='sos'),nz)*.05
    return stereo((x*.35+nz)*(np.minimum(1,t/.5)*np.minimum(1,(d-t)/.8)))
def shimmer(d):
    n=int(d*SR);x=np.zeros(n);r=np.random.default_rng(int(d*1000))
    for k in range(8):
        f=[587.3,659.3,740,880,987.8,1174.7][r.integers(6)]*r.choice([1,2]);t0=r.uniform(0,d*.7);b=M.bell(f,2.5)[:n-int(t0*SR)]*.3;x[int(t0*SR):int(t0*SR)+len(b)]+=b
    return stereo(x*np.minimum(1,np.arange(n)/(SR*.3)))
def whoosh(d,up=True):
    n=int(d*SR);t=np.arange(n)/SR;u=t/d;nz=np.random.default_rng(2).standard_normal(n);y=sosfilt(butter(2,[500,6000],'band',fs=SR,output='sos'),nz)*(u**2 if up else (1-u)**2)*.5;return stereo(y)
def hum(d):
    n=int(d*SR);t=np.arange(n)/SR;x=(np.sin(2*np.pi*55*t)+.5*np.sin(2*np.pi*110.5*t)+.3*np.sin(2*np.pi*165*t+t))*.35;nz=sosfilt(butter(2,[200,900],'band',fs=SR,output='sos'),np.random.default_rng(3).standard_normal(n))*.12*(.6+.4*np.sin(2*np.pi*.08*t));return stereo((x+nz)*np.minimum(1,t/3)*np.minimum(1,(d-t)/3))
def mk(prog,notes,tempo=60,is_drum=False):
    pm=pretty_midi.PrettyMIDI(initial_tempo=tempo);i=pretty_midi.Instrument(program=prog,is_drum=is_drum)
    for p,s,e,v in notes:i.notes.append(pretty_midi.Note(velocity=int(max(1,min(127,v))),pitch=int(p),start=float(s),end=float(e),))
    pm.instruments.append(i);return pm
def render_cue(c,key,speech):
    a=c['from']['t'];b=c['to']['t'];d=max(.2,b-a);role=c['role'];I=c.get('intensity',4);vel=38+I*8;ins=(c.get('instrument') or '').lower();prog,base=inst_of(ins);mode=c.get('mode') or 'minor';bpm=c.get('bpm') or 60
    k=c.get('key') or key;fi=c.get('fade_in',.8);fo=c.get('fade_out',1.2);sfx=(c.get('sfx') or '').lower();deg=c.get('degrees') or [];ch=c.get('chords') or [];pat=(c.get('pattern') or '').lower()
    gate=True;x=None;beat=60.0/bpm
    if role=='silence':return None
    if role=='ambience' or 'hum' in sfx:x=hum(d+1);gate=False
    elif role=='sfx' or (role in('hit',) and not ins):
        if 'gong' in sfx:x=gong(min(7,d+3));gate=False
        elif 'shankh' in sfx:x=shankh(d)
        elif 'shimmer' in sfx:x=shimmer(d)
        elif 'bell' in sfx:x=fs_render(mk(14,[(86,0,1.0,vel)]),2);gate=False
        elif 'whoosh' in sfx:x=whoosh(d)
        elif 'thunder' in sfx:x=stereo(M.thunder(min(6,d+2))*.5);gate=False
        else:x=stereo(M.boom(min(4,d+1)));gate=False
    elif role=='hit':
        p=mk(prog,[(base,0,min(d,2.5),min(127,vel+25))],bpm);x=addp(fs_render(p,2),stereo(M.boom(min(3.5,d+1.5))*.9));gate=False
    elif role=='riser':
        x=stereo(M.riser(int(d*SR))*.55)
        if prog in(48,44) and (ch or deg):
            seq=[chord_notes(cc,base) for cc in ch] if ch else [[degree_note(dd,mode,k,base)] for dd in deg];notes=[];steps=max(8,int(d/(beat/2)));st=d/steps
            for i in range(steps):
                for n_ in seq[i%len(seq)][:3]:notes.append((n_+12,i*st,i*st+st*1.4,30+int(60*i/steps)))
            x=addp(x[:int(d*SR)],fs_render(mk(prog,notes,bpm),1.0)[:int(d*SR)])
        gate=True
    elif role=='pulse':
        notes=[]
        if 'roll' in pat:
            t_=0;n_=0
            while t_<d:notes.append((base,t_,t_+.12,40+int(80*t_/d)));t_+=.09;n_+=1
        else:
            t_=0
            while t_<d-.2:notes+= [(base,t_,t_+.3,vel+10),(base,t_+beat*.28,t_+beat*.28+.3,vel-10)];t_+=beat*(1.0 if 'heart' in pat else .5)
        x=fs_render(mk(47,notes,bpm),1.0)
    elif role in('motif',) and deg and 'sustain' not in pat:
        rh=c.get('rhythm') or [1]*len(deg);rh=(rh+[1]*len(deg))[:len(deg)];tot=sum(rh);t_=0;notes=[]
        for dd,r_ in zip(deg,rh):
            dur=d*r_/tot;notes.append((degree_note(dd,mode,k,base),t_,t_+dur*(1.15 if ('choir' in ins or 'voice' in ins or 'flute' in ins) else 1.6),vel));t_+=dur
        x=fs_render(mk(prog,notes,bpm),2.0);gate=False
    elif role in('ostinato',):
        seq=[degree_note(dd,mode,k,base) for dd in deg] if deg else None;notes=[];st=beat/2;t_=0;i=0
        if seq:
            while t_<d-.1:notes.append((seq[i%len(seq)]+(12 if prog==46 else 0),t_,t_+st*2.2,vel));t_+=st;i+=1
        else:
            bars=[chord_notes(cc,base) for cc in ch];seg=d/len(bars)
            for j,bn in enumerate(bars):
                for n_ in bn:notes.append((n_,j*seg,(j+1)*seg+.4,vel))
        x=fs_render(mk(prog,notes,bpm),1.5)
    else:   # bed / sustained motif / tuba cluster / tanpura
        notes=[]
        if 'tanpura' in ins:
            sa=36+(pcof(k)-pcof('D'))%12;seq=[sa+7,sa+12,sa+12,sa];t_=0;i=0
            while t_<d:notes.append((seq[i%4],t_,t_+3.2,vel-8));t_+=1.45;i+=1
        elif ch:
            seg=d/len(ch)
            for j,cc in enumerate(ch):
                for n_ in chord_notes(cc,base):notes.append((n_,j*seg,(j+1)*seg+.5,vel))
        elif deg:
            for dd in deg:notes.append((degree_note(dd,mode,k,base),0,d+.3,vel))
        else:
            for n_ in(base,base+7,base+12):notes.append((n_,0,d+.3,vel))
        x=fs_render(mk(prog,notes,bpm),2.0)
    n=int(min(len(x),(d+(0 if gate else 2.5))*SR+int(.6*SR)));x=x[:n]*env(n,fi,fo if gate else 0.3,gate)[:,None]
    gain=10**((I-5)*1.6/20)*10**((c.get('duck_db',0))/40)
    return a,x*gain
def build(ep):
    Rr=R;tim=json.load(open(f'{Rr}/build/ep{ep}/timings.json',encoding='utf-8'));cues=json.load(open(f'{Rr}/episodes/ep{ep}/sound_cues.json',encoding='utf-8'));key=cues.get('key','D')
    total=sum(t['duration'] for t in tim);tail=max([c['to']['t'] for c in cues['cues']]+[total])+1.5;n=int(tail*SR);mus=np.zeros((n,2),np.float32)
    sp=np.zeros(n)  # speech mask from word times
    off=0.0
    for t in tim:
        for w in t['words']:sp[int((off+w['start'])*SR):int((off+w['end'])*SR)]=1
        off+=t['duration']
    k_=np.ones(int(.35*SR))/int(.35*SR);spd=np.convolve(sp,k_,'same');spd=np.minimum(1,spd*1.6)
    for c in cues['cues']:
        r=render_cue(c,key,sp)
        if r is None:continue
        a,x=r;i=int(a*SR);j=min(n,i+len(x));mus[i:j]+=x[:j-i]
    # reverb on the music bus
    ir=(np.random.default_rng(4).standard_normal(int(2.4*SR))*np.exp(-np.arange(int(2.4*SR))/SR*2.0)*.01)
    wet=np.stack([oaconvolve(mus[:,ch],ir,mode='full')[:n] for ch in(0,1)],1);mus=mus+.7*wet
    # voice-pocket ducking: 3 bands, mids ducked harder while the voice speaks
    lo=lp(mus,220);hi=hp(mus,4200);mid=mus-lo-hi
    g_mid=1-spd*(1-10**(-9/20));g_edge=1-spd*(1-10**(-4/20));mus=lo*g_edge[:,None]+hi*g_edge[:,None]+mid*g_mid[:,None]
    # explicit silences (also kills reverb tails)
    g=np.ones(n)
    for c in cues['cues']:
        if c['role']=='silence':
            a=int(c['from']['t']*SR);b=int(c['to']['t']*SR);depth=0.0 if c.get('intensity',0)==0 else .12;f=int(.06*SR)
            seg=np.ones(b-a)*depth;seg[:f]=np.linspace(1,depth,f);seg[-f:]=np.linspace(depth,1,f)
            g[a:b]=np.minimum(g[a:b],seg)
    mus=mus*g[:,None]
    # voice
    vf=f'{Rr}/build/ep{ep}/voice_full.wav'
    lst=''.join(f"file '{Rr}/build/ep{ep}/audio/{i:02d}.mp3'\n" for i in range(len(tim)));open(f'{Rr}/build/ep{ep}/vlist2.txt','w').write(lst)
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{Rr}/build/ep{ep}/vlist2.txt','-ar',str(SR),'-ac','2',vf],check=True)
    sr,v=wavfile.read(vf);v=v.astype(np.float32)/32768.0
    vv=np.zeros((n,2),np.float32);m=min(n,len(v));vv[:m]=v[:m]
    mask=sp>0;rv=np.sqrt((vv[mask]**2).mean()) if mask.any() else .1;rm=np.sqrt((mus[mask]**2).mean())+1e-6
    kk=rv*10**(-14/20)/rm;mus=mus*kk
    pk=np.abs(mus).max();mix=mus+vv;mx=np.abs(mix).max()
    gfin=.9/mx;mix*=gfin;mus*=gfin   # normalise the whole mix to a healthy level (peak 0.9)
    os.makedirs(f'{Rr}/renders',exist_ok=True)
    def save(x,name):
        wavfile.write(f'/tmp/{name}.wav',SR,(np.clip(x,-1,1)*32767).astype(np.int16));subprocess.run(['ffmpeg','-v','error','-y','-i',f'/tmp/{name}.wav','-b:a','192k',f'{Rr}/renders/{name}.mp3'],check=True)
    save(mus,f'ep{ep}_score_music_only');save(mix,f'ep{ep}_score_with_voice');print('ok: music',round(len(mus)/SR,1),'s; music RMS during speech is 14 dB under the voice')
if __name__=='__main__':build(sys.argv[1])
