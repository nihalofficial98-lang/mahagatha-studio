"""Voice timeline for the creative agents: every beat, line and word with exact times in the owner's voiceover, plus all pauses.
python3 studio/make_timeline.py 04   (after `studio.py align 04 voice.mp3 --timestamps words.json`)  ->  episodes/ep04/voice_timeline.md"""
import json,sys,os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def mmss(t):return f"{int(t//60)}:{t%60:05.2f}"
def main():
    ep=sys.argv[1];T=json.load(open(f'{R}/build/ep{ep}/timings.json',encoding='utf-8'));B=json.load(open(f'{R}/build/ep{ep}/beats.json',encoding='utf-8'))['scenes']
    out=[f"# Voice timeline — episode {ep}\nAll times are seconds-in-the-final-video (the owner's voice, unchanged). Total {sum(t['duration'] for t in T):.1f} s ({sum(t['duration'] for t in T)/60:.2f} min).\nUse these exact times to place cues and shots. `gap` = silence before a line; gaps >= 0.35 s are the places for swells, stingers, drop-outs and cuts.\n"]
    off=0.0;prev_end=0.0;gaps=[];rates=[]
    for t,sc in zip(T,B):
        out.append(f"\n## Beat {sc['beat']:02d}  ({mmss(off)} – {mmss(off+t['duration'])})")
        i=0
        for li,seg in enumerate(sc['narration']):
            n=len(seg['t'].split());ws=t['words'][i:i+n];i+=n;a=off+ws[0]['start'];b=off+ws[-1]['end'];gap=a-prev_end;rates.append(n/max(.1,b-a))
            if gap>=.35:gaps.append((prev_end,gap))
            out.append(f"\n**L{li+1}** {mmss(a)} – {mmss(b)}  ({b-a:.1f}s, {n} words, {n/max(.1,b-a):.1f} w/s, gap before {max(0,gap):.2f}s)\n{seg['t']}\n`"+' '.join(f"{w['text']}@{off+w['start']:.2f}" for w in ws)+"`")
            prev_end=b
        off+=t['duration']
    out.append("\n\n## Pauses (>= 0.35 s) — breathing spots for music swells, stingers, drop-outs and cuts\n"+'\n'.join(f"- {mmss(a)} for {g:.2f}s" for a,g in gaps))
    out.append(f"\n\nPace: average {sum(rates)/len(rates):.1f} words/s; slowest lines mark emotional weight, fastest are chase/panic.")
    open(f'{R}/episodes/ep{ep}/voice_timeline.md','w',encoding='utf-8').write('\n'.join(out)+'\n');print(f'episodes/ep{ep}/voice_timeline.md', len(gaps),'pauses')
main()
