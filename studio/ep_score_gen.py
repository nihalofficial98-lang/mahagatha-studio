"""Generate full-length mood tracks for an episode: python3 studio/ep_score_gen.py ep07 472"""
import sys,os,subprocess,wave,numpy as np
sys.path.insert(0,os.path.dirname(__file__))
import reel_bgm as B
ep,dur=sys.argv[1],float(sys.argv[2])
moods={'bgm':B.make,'tense':B.tense,'cosmic':B.cosmic,'dark':B.dark,'lament':B.lament,'war':B.war}
for k,fn in moods.items():
    x=fn(dur,7);x=x/max(1e-9,np.max(np.abs(x)))
    w=f'/tmp/{ep}_{k}.wav'
    with wave.open(w,'wb') as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(B.SR);o.writeframes((x*32000).astype('<i2').tobytes())
    subprocess.check_call(['ffmpeg','-y','-v','error','-i',w,'-b:a','192k',f'{B.R}/renders/bgm/{ep}_{k}.mp3']);print(k,flush=True)
