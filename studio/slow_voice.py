"""Slow (or speed) a recorded voice without changing pitch and rescale the ElevenLabs word-timestamp JSON to match.
python3 studio/slow_voice.py in.mp3 in.json 0.95 -> in_x0.95.mp3 + in_x0.95.json"""
import sys,json,subprocess,os
mp3,js,sp=sys.argv[1],sys.argv[2],float(sys.argv[3])
base=os.path.splitext(mp3)[0]+f'_x{sp}'
subprocess.check_call(['ffmpeg','-y','-v','error','-i',mp3,'-filter:a',f'atempo={sp}','-b:a','192k',base+'.mp3'])
def scale(o):
    if isinstance(o,dict):
        return {k:(round(v/sp,3) if isinstance(v,(int,float)) and ('start' in k or 'end' in k or k.endswith('_time') or k.endswith('_times')) else scale(v)) for k,v in o.items()}
    if isinstance(o,list):
        if o and all(isinstance(x,(int,float)) for x in o):return o
        return [scale(x) for x in o]
    return o
d=json.load(open(js))
def walk(o):
    if isinstance(o,dict):
        return {k:([round(x/sp,3) for x in v] if isinstance(v,list) and v and all(isinstance(x,(int,float)) for x in v) and ('start' in k or 'end' in k) else (round(v/sp,3) if isinstance(v,(int,float)) and ('start' in k or 'end' in k) else walk(v))) for k,v in o.items()}
    if isinstance(o,list):return [walk(x) for x in o]
    return o
json.dump(walk(d),open(base+'.json','w'),ensure_ascii=False);print(base+'.mp3',base+'.json')
