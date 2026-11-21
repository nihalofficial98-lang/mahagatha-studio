"""Voiceover text for ElevenLabs-style generation: narration lines ONLY (no titles, headings, beat labels, metadata), each with an emotion tag.
python3 studio/vo_script.py 04"""
import re,sys,os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGS={'04':{
1:['fast, shocking, intense','deep, grave, slow-burning','dark, mysterious, building curiosity'],
2:['calm, measured, storyteller','ominous, dread under the words; the quoted curse slow and cold','grave, firm, weight on every word'],
3:['tense, unease building','cold, hollow, heavy','alarmed, quick breath, then tense','slow, awed, shaken disbelief'],
4:['fast, rising panic','stunned, shaken, one beat of silence','urgent, pleading, worried (the sages speaking)','heavy, defeated'],
5:['fast, breathless, chase','quick, dramatic, rhythmic list','steady, wide, awed list','light surprise, curious, then a calm reveal of the name'],
6:['sudden, powerful, burning anger','tense, then breaking into shame and pleading','harsh, final, cold fury','stern, thundering judgement (Shiva speaking)','calm, explanatory, settling'],
7:['slow, uneasy, discovery','tense then grave, realisation sinking in'],
8:['thoughtful, questioning, gentle','calm, wise, measured (Atri explaining)'],
9:['sad, weary, slow','awed, wondering, the miracle','relieved, reverent, glowing'],
10:['tender, concerned','trembling, fearful, near tears (her words)','heavy pause, then a fragile voice'],
11:['trembling, pained, slow','pained, slower','pained, voice breaking','despairing, fading','broken, trembling, almost crying'],
12:['light, shift of tone, storyteller','surprised, proud, a little boastful (Narada)','calm, knowing smile (Vishnu)','curious, eager (Narada)','gentle, playful, hinting (Vishnu)'],
13:['dreamy, drawn in','warm, quick, almost carried away'],
14:['warm, gentle, time flowing, happy'],
15:['sudden, dark, alarming','shocked, helpless, rushed, then dazed and stunned'],
16:['calm, simple, devastating','stunned, shaky, disbelieving','sharp, sinking realisation','slow, deeply moved, heavy'],
17:['gentle, wise, smiling','calm, teaching, measured','calm, final, serene'],
18:['thoughtful, widening awe','playful, ominous smile, light warning'],
19:['warm, direct to the audience, friendly question','calm, warm, inviting teaser']}}
def main():
    ep=sys.argv[1];src=open(f'{R}/episodes/ep{ep}/script.md',encoding='utf-8').read().split('\n');T=TAGS[ep];blocks={};cur=None
    for ln in src:
        m=re.match(r'\*\*B(\d+)\*\*',ln)
        if m:cur=int(m.group(1));blocks[cur]=[];continue
        if ln.startswith(('---','#')):cur=None;continue
        if cur and ln.strip() and not ln.startswith(('*','**')):blocks[cur].append(ln.strip())
    for b,l in blocks.items():assert len(l)==len(T[b]),(b,len(l),len(T[b]))
    out=[]
    for b in sorted(blocks):out.append('\n'.join(f'[{t}] {l}' for t,l in zip(T[b],blocks[b])))
    txt='\n\n'.join(out)+'\n'
    name={'04':'EP04_Shiva_Ne_Kata_Brahma_Ka_Sir_Aur_Narad_Ki_Maya_Voiceover_Script_With_Emotion_Tags.txt'}[ep]
    open(f'{R}/deliverables/{name}','w',encoding='utf-8').write(txt);print(name,sum(len(v) for v in blocks.values()),'lines')
main()
