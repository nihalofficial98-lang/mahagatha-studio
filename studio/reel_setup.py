#!/usr/bin/env python3
"""Turn a prepared reel (voice + word timings) into a project the episode pipeline can build and render in 9:16.
  python3 studio/reel_setup.py reel02 [--title "Why Do People Go to Kashi?"] [--cast brahma,shiva]
  python3 studio/reel_setup.py _test --like reel02          (test project: reel02 voice/words, its own briefs)
Needs reels/inputs/reelNN.mp3 and reels/build/reelNN/words.json (python3 studio/reel_prepare.py NN makes words.json).
Writes / updates:
  reels/<id>/reel.json        {reel, title, full_title, audio, words, cast, format:"vertical", fps:24, title_sec, duration}
                              title = first-frame text (2-4 words, shown big from frame 0), full_title = the upload title
  reels/build/<id>/timings.json, beats.json, audio/00.mp3   (one beat = the whole reel; words = the spoken words, exactly)
Then: briefs.json -> validate_brief.py <id> -> brief_to_plan.py <id> -> build_shots.py <id> -> ep_frames.py <id> (vertical stills)
-> owner approves -> reels/<id>/APPROVED -> render_chunks.py <id> (see guides/RENDER.md, Reels)."""
import os,re,sys,json,shutil,argparse,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import project as P
R=P.R
def titles(n):
    p=f'{R}/deliverables/reels/Reels_Voiceover_Plain.txt'
    if not os.path.exists(p):return None,None
    hs=re.findall(r'^=== (.*?) \| (.*?) ===$',open(p,encoding='utf-8').read(),flags=re.M)
    return hs[n-1] if 0<n<=len(hs) else (None,None)
def main():
    a=argparse.ArgumentParser();a.add_argument('id');a.add_argument('--like');a.add_argument('--title');a.add_argument('--full-title');a.add_argument('--cast');x=a.parse_args()
    rid=x.id
    if not P.is_reel(rid):sys.exit("STOP: a reel id starts with 'reel' (reel02) or '_' (_test)")
    src=x.like or rid;m_=re.match(r'reel(\d+)$',src)
    if not m_:sys.exit('STOP: use --like reelNN to say whose voice and words this project uses')
    n=int(m_[1]);E=P.edir(rid);Bd=P.bdir(rid);os.makedirs(E,exist_ok=True);os.makedirs(Bd+'/audio',exist_ok=True)
    mf=P.meta_file(rid);meta=json.load(open(mf,encoding='utf-8')) if os.path.exists(mf) else {}
    t1,t2=titles(n)
    meta.setdefault('reel',f'{n:02d}');meta.setdefault('title',t1 or '');meta.setdefault('full_title',t2 or '')
    meta.setdefault('audio',f'reels/inputs/reel{n:02d}.mp3');meta.setdefault('words',f'reels/build/reel{n:02d}/words.json')
    meta.setdefault('cast',[]);meta.setdefault('format','vertical');meta.setdefault('fps',24);meta.setdefault('title_sec',2.5)
    if x.title:meta['title']=x.title
    if x.full_title:meta['full_title']=x.full_title
    if x.cast:meta['cast']=[c.strip() for c in x.cast.split(',') if c.strip()]
    au=f"{R}/{meta['audio']}";wf=f"{R}/{meta['words']}"
    if not os.path.exists(au):sys.exit(f"STOP: voice missing: {meta['audio']}")
    if not os.path.exists(wf):subprocess.run([sys.executable,f'{R}/studio/reel_prepare.py',str(n)],check=True)
    ws=json.load(open(wf,encoding='utf-8'))
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',au]).decode())
    meta['duration']=round(dur,3);meta.pop('target_sec',None)
    bad=[w['w'] for w in ws if len(w['w'].split())!=1]
    if bad:sys.exit(f'STOP: words with spaces inside {bad[:5]} (fix words.json)')
    words=[{'text':w['w'],'start':w['start'],'end':w['end']} for w in ws]
    json.dump([{'beat':1,'audio':round(dur,3),'duration':round(dur,3),'words':words}],open(Bd+'/timings.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    segs=[];cur=[]
    for w in ws:
        cur.append(w['w'])
        if re.search(r'[.?!]["”]?$',w['w']):segs.append(cur);cur=[]
    if cur:segs.append(cur)
    json.dump({'voice':'user','scenes':[{'beat':1,'narration':[{'t':' '.join(s)} for s in segs]}]},open(Bd+'/beats.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    shutil.copy(au,Bd+'/audio/00.mp3')
    assert ' '.join(' '.join(s) for s in segs).split()==[w['w'] for w in ws]
    json.dump(meta,open(mf,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    tw=len(meta['title'].split())
    print(f"{rid}: {dur:.2f}s voice, {len(ws)} words in {len(segs)} sentences -> {os.path.relpath(Bd,R)}/timings.json, beats.json, audio/00.mp3")
    print(f"title card: '{meta['title']}' ({tw} words{'; the owner style is 2-4 words' if not 2<=tw<=4 else ''}), {meta['title_sec']} s; cast {meta['cast'] or 'NOT SET'}")
    print(f"word times for the briefs (start.t / start.word): {os.path.relpath(Bd,R)}/timings.json")
    print(f"next: write {os.path.relpath(E,R)}/briefs.json, then python3 studio/validate_brief.py {rid}")
if __name__=='__main__':main()
