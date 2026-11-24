"""Turn APPROVED shot briefs into the builder's shot plan (then build_shots.py makes shots.json, timed to the voice).
  python3 studio/brief_to_plan.py NN [--brief B] [--out P]   # default: episodes/epNN/briefs.json -> episodes/epNN/shot_plan.json
  (reels: NN = reel02 / _test -> reels/<id>/; the brief's optional `vertical` block becomes the shot's `vert`)
It refuses to run while validate_brief.py reports errors. Mapping is mechanical: every word in the brief becomes a cue
(in spoken order) and each action/effect/background change fires on its cue index."""
import json,sys,os,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import validate_brief as VB,engine_vocab as V,project as PJ
R=VB.R;norm=VB.norm
TR_DX={'cut':0}
def convert(s,vert=False):
    nw=VB.words_of(s['narration']);cues=[]
    def cue(w):
        """index of word w in this shot's cue list; cues are kept in the order they are spoken"""
        w=norm(w)
        if w not in cues:cues.append(w)
        return w
    used=[]
    for f in s['characters']:
        for a in f.get('actions',[]):used.append(a['word'])
        if f.get('walk'):used.append(f['walk']['word'])
        if f.get('turn_on'):used.append(f['turn_on'])
        used+=list((f.get('engine_cues') or {}).values())
    for e in s['effects']:
        if e.get('word'):used.append(e['word'])
    ch=s['background'].get('change')
    if ch:used.append(ch['word'])
    pos=lambda w:next((i for i,x in enumerate(nw) if VB.has_word([x],w)),999)
    for w in sorted(set(norm(u) for u in used),key=pos):cue(w)
    ci=lambda w:cues.index(norm(w))
    xs={f['who']:f.get('x',640) for f in s['characters']}
    def look(f,target):
        tx=xs.get(target,640) if isinstance(target,str) else target
        return round((1 if tx>f.get('x',640) else -1)*.8*(f.get('flip',1)),2)
    figs=[]
    for f in s['characters']:
        g={k:v for k,v in f.items() if k in('who','x','y','s','flip','pose','emo','head','aura','k','prop','halo','lotus','hd','talk','dark','bow','kneel')}
        mood=dict(f.get('mood') or {})
        if f.get('look'):mood['lx']=look(f,f['look'])
        if mood:g['mood']=mood
        acts=[]
        for a in f.get('actions',[]):
            x={'c':ci(a['word']),'d':a.get('d',.6)}
            for k in('pose','emo','tilt','e'):
                if k in a:x[k]=a[k]
            m=dict(a.get('mood') or {})
            if a.get('look'):m['lx']=look(f,a['look'])
            if a.get('turn') is not None:m['turn']=a['turn']
            if m:x['mood']=m
            acts.append(x)
        if acts:g['acts']=acts
        if f.get('walk'):w=f['walk'];g['walkTo']={'x':w['to_x'],'c':ci(w['word']),'d':w.get('d',2),'sp':w.get('speed',1)}
        if f.get('turn_on'):g['turnc']=ci(f['turn_on']);g['turnd']=f.get('turn_d',.5)
        g.update(f.get('engine') or {})          # raw engine figure keys (mx/my/md, wd, fall, rot, glide, a, fd, ...)
        for k,w in (f.get('engine_cues') or {}).items():g[k]=ci(w)   # cue keys fired on a spoken word (mc, wc, fo, ac, kc, bc)
        figs.append(g)
    fx=[];fxb=[]
    for e in s['effects']:
        k=e.get('k') or e.get('t');x={'t':'pfx','k':k} if k in V.PFX else {'t':k}
        x.update({kk:v for kk,v in e.items() if kk not in('k','t','word','meaning','behind')})
        if e.get('word'):x['c']=ci(e['word']);x.setdefault('d',.6)
        (fxb if e.get('behind') else fx).append(x)
    bg={k:v for k,v in s['background'].items() if k!='change'}
    plan={'id':s['id'],'at':{'t':s['start']['t'],'word':s['start']['word']},'cues':cues,'bg':bg,'figs':figs,'fx':fx,'fxb':fxb,
          'cam':{'from':s['camera']['from'],'to':s['camera']['to']},'grade':s['mood']['grade'],
          'layers':[{k:v for k,v in l.items() if k not in('contents','from_background')} for l in s['layers'] if l.get('items')],
          'note':f"{s['camera']['shot']} {s['camera']['move']}: {s['why']}"}
    if not plan['layers']:del plan['layers']
    if vert:                                  # 9:16 reels: portrait window / stack layout (engine/main.js VERTICAL); default focus = focus.subject
        v=dict(s.get('vertical') or {})
        if 'focus' not in v and v.get('mode')!='stack' and s['focus'].get('subject') in xs:v['focus']=s['focus']['subject']
        if v:plan['vert']=v
    if s['camera'].get('shake'):plan['shake']=s['camera']['shake']
    if ch:
        plan['bgc']=ci(ch['word']);plan['bgd']=ch.get('d',1.2)
        if ch.get('bg2'):plan['bg2']=ch['bg2']
        else:plan['bgTo']=ch['to']
    tr=s['transition_in']
    if tr=='cut':plan['dx']=0
    elif tr!='fade':plan['tr']=tr
    return plan
def main():
    import argparse;a=argparse.ArgumentParser();a.add_argument('ep');a.add_argument('--brief');a.add_argument('--out');x=a.parse_args();ep=x.ep
    p=x.brief or f'{PJ.edir(ep)}/briefs.json';b=json.load(open(p,encoding='utf-8'))
    errs,_=VB.check(b,ep)
    if errs:print('\n'.join('ERROR '+e for e in errs));sys.exit('brief not valid: fix it (python3 studio/validate_brief.py %s)'%ep)
    vert=PJ.fmt(ep)=='vertical'
    out={'episode':ep,'shots':[convert(s,vert) for s in b['shots']]}
    dst=x.out or f'{PJ.edir(ep)}/shot_plan.json';json.dump(out,open(dst,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print(f"{len(out['shots'])} shots -> {dst}\nnext: python3 studio/build_shots.py {ep}")
if __name__=='__main__':main()
