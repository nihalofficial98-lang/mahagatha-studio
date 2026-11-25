"""Scene-by-scene score: mixes existing music tracks under a reel's voice following reels/<reel>/score.json (cue trapezoids + silence holds)."""
import json,sys,subprocess,wave,numpy as np,os
SR=44100;R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(p,dur):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',p,'-f','s16le','-ac','1','-ar',str(SR),'-'])
    x=np.frombuffer(raw,'<i2').astype(float)/32768;n=int(dur*SR);x=np.pad(x,(0,max(0,n-len(x))))[:n];return x
def main(reel):
    sc=json.load(open(f'{R}/reels/{reel}/score.json'));src=f"{R}/{sc['video']}"
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]));n=int(dur*SR);t=np.arange(n)/SR
    mix=np.zeros(n)
    for c in sc['cues']:
        e=np.clip(np.minimum((t-c['start'])/c['in'],(c['end']-t)/c['out']),0,1);e=np.sin(e*np.pi/2)**1.0
        mix+=load(f"{R}/{c['track']}",dur)*e*c['g']
    for h in sc.get('holds',[]):
        d=np.minimum((t-h['start'])/h['fade'],(h['end']-t)/h['fade']);d=np.clip(d,0,1)
        mix*=1-d*(1-h['floor'])
    mix/=max(1e-9,np.max(np.abs(mix)))
    w=f'/tmp/{reel}_score.wav'
    with wave.open(w,'wb') as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(SR);o.writeframes((mix*32000).astype('<i2').tobytes())
    out=f"{R}/{sc['out']}"
    fc=(f"[1:a]volume={sc['master']}[m];[0:a]asplit[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=5:attack=40:release=500[md];"
        "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
    subprocess.check_call(['ffmpeg','-y','-v','error','-i',src,'-i',w,'-filter_complex',fc,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k',out]);print(out)
if __name__=='__main__':main(sys.argv[1])
