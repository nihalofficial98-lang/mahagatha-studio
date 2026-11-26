"""Speech to text (no cloud): python3 studio/transcribe.py <audio> [--lang en|hi|auto] [--model small] -> prints text and writes <audio>.txt + <audio>.words.json (word times)."""
import sys,subprocess,json,numpy as np
from faster_whisper import WhisperModel
a=sys.argv[1];lang=sys.argv[sys.argv.index('--lang')+1] if '--lang' in sys.argv else 'auto'
mod=sys.argv[sys.argv.index('--model')+1] if '--model' in sys.argv else 'small'
x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',a,'-ac','1','-ar','16000','-f','f32le','-']),'<f4')
m=WhisperModel(mod,device='cpu',compute_type='int8')
seg,info=m.transcribe(x,language=None if lang=='auto' else lang,word_timestamps=True,vad_filter=True)
segs=[];words=[]
for s in seg:
    segs.append(s.text.strip());words+= [dict(word=w.word.strip(),start=round(w.start,2),end=round(w.end,2)) for w in s.words]
open(a+'.txt','w').write('\n'.join(segs));json.dump(dict(language=info.language,words=words),open(a+'.words.json','w'),ensure_ascii=False)
print(info.language);print('\n'.join(segs))
