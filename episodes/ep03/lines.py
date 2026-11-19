"""Maps every narration line (segment) of each beat to start/end seconds (from build/ep03/timings.json) so shots can be timed to the spoken lines."""
import os,json
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def load(ep='ep03'):
    B=json.load(open(f'{ROOT}/build/{ep}/beats.json',encoding='utf-8'))['scenes'];T=json.load(open(f'{ROOT}/build/{ep}/timings.json',encoding='utf-8'));out={}
    for bi,(sc,tm) in enumerate(zip(B,T)):
        words=tm['words'];idx=0;L=[]
        for seg in sc['narration']:
            n=len(seg['t'].split());a=words[min(idx,len(words)-1)]['start'];b=words[min(idx+n-1,len(words)-1)]['end'];L.append({'start':a,'end':b,'n':n,'w0':idx,'text':seg['t']});idx+=n
        out[sc['beat']]={'lines':L,'dur':tm['duration'],'words':words}
    return out
if __name__=='__main__':
    import sys;D=load(sys.argv[1] if len(sys.argv)>1 else 'ep03')
    for b,v in D.items():
        print(f'B{b:02d} dur {v["dur"]:.1f}')
        for i,l in enumerate(v['lines']):print(f'   L{i} {l["start"]:5.1f}-{l["end"]:5.1f} ({l["end"]-l["start"]:.1f}s) {l["text"][:60]}')
