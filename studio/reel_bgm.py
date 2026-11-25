"""Divine BGM (choir pad + harp + deep drone, pure numpy) mixed under a reel's voice.
python3 studio/reel_bgm.py reel15 [reel09 ...]  -> renders/<reel>_bgm_1080x1920.mp4 (video copied, voice kept)"""
import numpy as np,sys,os,subprocess,wave,zlib
from scipy.signal import butter,sosfilt,fftconvolve
SR=44100;R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(m):return 440*2**((m-69)/12)
def bp(x,a,b):return sosfilt(butter(2,[a,b],'band',fs=SR,output='sos'),x)
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
        e=np.ones(L);a=int(2.5*SR);e[:a]=np.linspace(0,1,a)**1.5;r=int(3*SR);e[-r:]*=np.linspace(1,0,r)
        pad[s:s+L]+=c*e
    drone=lp(sum(np.sin(2*np.pi*f(root-12)*k*np.arange(n)/SR)/k for k in(1,2,3)),400)*.5
    hp=harp(root,dur,rng,seed%3*6+60)
    wet=reverb(pad*1.0+hp*.8)
    mix=pad*.55+drone*.25+hp*.5+wet*.9
    fade=np.minimum(1,np.minimum(np.arange(n)/(2*SR),(n-np.arange(n))/(3*SR)));mix*=fade
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
