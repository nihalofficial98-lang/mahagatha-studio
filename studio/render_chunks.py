"""Resumable final render (Sonnet runs this, only after the owner approved the frames).
  python3 studio/render_chunks.py NN [--chunk 600] [--workers 4] [--fps 30] [--check]
--check only verifies the inputs and prints the plan. Chunks are saved as build/epNN/chunks/chNNN.mp4 the moment they finish;
running the same command again renders only the missing chunks. At the end: renders/epNN_1080p.mp4 (video + owner's voice)."""
import os,sys,json,subprocess,argparse,glob,time
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,R+'/studio')
import build as B
def die(m):sys.exit('STOP: '+m)
def main():
    a=argparse.ArgumentParser();a.add_argument('ep');a.add_argument('--chunk',type=int,default=600);a.add_argument('--workers',type=int,default=4);a.add_argument('--fps',type=int,default=30);a.add_argument('--res',default='1080p',choices=['1080p','720p']);a.add_argument('--check',action='store_true');x=a.parse_args()
    ep=x.ep;E=f'{R}/episodes/ep{ep}';Bd=f'{R}/build/ep{ep}';S=E+'/shots.json'
    need=[S,Bd+'/timings.json',Bd+'/beats.json',E+'/episode.json',E+'/APPROVED']
    miss=[p for p in need if not os.path.exists(p)]
    if miss:die('missing '+', '.join(os.path.relpath(p,R) for p in miss)+'  (APPROVED is written by the producer only after the owner approves the frames)')
    nb=len(json.load(open(Bd+'/timings.json')));ma=[i for i in range(nb) if not os.path.exists(f'{Bd}/audio/{i:02d}.mp3')]
    if ma:die(f'voice pieces missing for beats {ma}: run the align step (WORKFLOW.md step 3)')
    env=dict(os.environ);env.setdefault('NODE_PATH',subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip())
    tgt=str(json.load(open(E+'/episode.json')).get('target_sec',0))
    subprocess.run(['node',R+'/studio/render_ep.js',Bd,S,'/dev/null'],env=dict(env,PREPARE_ONLY='',VOICE_ONLY='1',TARGET_SEC=tgt),check=True)
    tm=json.load(open(Bd+'/engine_timings.json'));total=sum(t['duration'] for t in tm);N=round(total*x.fps)
    C=Bd+('/chunks' if x.res=='1080p' else '/chunks720');os.makedirs(C,exist_ok=True);jobs=[(i,f0,min(N,f0+x.chunk)) for i,f0 in enumerate(range(0,N,x.chunk))]
    todo=[j for j in jobs if not os.path.exists(f'{C}/ch{j[0]:03d}.mp4')]
    print(f'EP{ep}: {total:.1f}s, {N} frames, {len(jobs)} chunks, {len(jobs)-len(todo)} already done, {len(todo)} to render')
    if x.check:return
    W,H,SC=(1920,1080,1.5) if x.res=='1080p' else (1280,720,1.0);html=B.build(SC);wenv=dict(env,ENGINE=html,VW=str(W),VH=str(H),CRF='20',JQ='92');run={}
    while todo or run:
        while todo and len(run)<x.workers:
            i,f0,f1=todo.pop(0);part=f'{C}/ch{i:03d}.part.mp4'
            run[i]=(subprocess.Popen(['node',R+'/studio/render_ep.js','--worker',Bd,S,part,str(f0),str(f1),str(x.fps)],env=wenv,stdout=subprocess.DEVNULL),part)
        time.sleep(5)
        for i,(p,part) in list(run.items()):
            if p.poll() is None:continue
            del run[i]
            if p.returncode==0 and os.path.exists(part):os.replace(part,f'{C}/ch{i:03d}.mp4');print(f'chunk {i} done')
            else:print(f'chunk {i} FAILED (exit {p.returncode}); run the command again to retry')
    have=sorted(glob.glob(C+'/ch[0-9][0-9][0-9].mp4'))
    if len(have)!=len(jobs):die(f'{len(have)}/{len(jobs)} chunks present; run the same command again')
    open(C+'/list.txt','w').write(''.join(f"file '{os.path.basename(f)}'\n" for f in have))
    os.makedirs(R+'/renders',exist_ok=True);out=f'{R}/renders/ep{ep}_{x.res}.mp4'
    subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',C+'/list.txt','-i',Bd+'/voice.wav','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',out],check=True)
    print('done',out)
if __name__=='__main__':main()
