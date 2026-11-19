"""Voiceover scripts with per-line emotion tags. Script text is untouched; tags are added before each line."""
import re,os,sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T={
'01':{1:['slow, hushed, mysterious','hushed, let it sink in','whispers, a long pause after','whispers, rising awe'],
2:['slow, hushed, grave'],
3:['calm, grave, measured','slow, awed, deep','slow, hushed wonder','soft pause, building anticipation'],
4:['slow, hushed','long pause, deep, reverent','grand, awed, swelling'],
5:['grave, steady, teaching tone','measured, each element given its own beat'],
6:['slow, painterly, soft wonder','gentle, explaining','reverent, pause before the name'],
7:['grand, majestic','awed','triumphant, rising wonder'],
8:['majestic, patient','awed, wide and expansive'],
9:['calm, still, reverent','warm, a contented smile in the voice','pause','ominous, quiet, dread creeping in'],
10:['whispers, eerie, creeping dread','sudden, sharp','quick, curious, faintly mocking'],
11:['slow, innocent, curious','ominous, growing heavier','dark, swelling arrogance, low'],
12:['wary, steady','arrogant, booming, mocking','tense, narrating','threatening, shouting, furious'],
13:['urgent, alarmed','panicked, breathless','horrified, hushed','grim, chilling','snarling, cruel'],
14:['alarmed, rising fear','pleading, desperate, trembling','heavy, hollow, despair building'],
15:['quiet resolve, somber','pleading, humble, hushed','soft relief, awe'],
16:['sharp, grand, thrilling','intense, fast, dramatic','fast and relentless, then slowing as the years stretch','heavy, worried, slow'],
17:['slow, thinking, dawning realization','calm, deliberate','sweet, honeyed, playful, feigned admiration'],
18:['loud laughter, mocking','arrogant, scornful, booming','calm, quiet, probing','gloating, eager','soft smile, knowing, quiet triumph'],
19:['whispers, cold, deliberate','long pause','hushed, heavy silence','slow, ominous, realization'],
20:['tense, fast, desperate','shouting, desperate, cunning'],
21:['slow, grand, calm smile','measured, quiet intensity','sharp, decisive, then silence','solemn, reverent'],
22:['tired, wondering, soft','calm, humble, philosophical'],
23:['calm, settled, matter-of-fact','quiet awe'],
24:['hopeful, gentle','uneasy, slowing','whispers, ominous, final'],
25:['warm, teasing, curious','grand, anticipation','warm, friendly, light']},
'03':{1:['soft, wistful recap','questioning, then weary and lonely','hushed, mysterious, building excitement'],
2:['grand, warm','proud, steady, naming each rishi','warm, ceremonial'],
3:['reverent, rising','awed, expanding','blissful, glowing','gentle, content, a smile in the voice'],
4:['sudden, tense, hushed alarm','sharp, startled, powerful'],
5:['soft, serene','tense, disturbed','building anger, low and burning','furious, intense, fast'],
6:['urgent, chaotic, fast','hushed, pivotal','steady, brave, firm'],
7:['fierce, rising','explosive, dramatic','powerful, epic','awed, cosmic, slowing, hushed'],
8:['heavy, grave','tense, slow, measured','ominous, low, dread'],
9:['hushed, urgent','pleading, desperate, trembling','pleading, voice breaking'],
10:['grave, pleading, firm','urgent','quiet, questioning, heavy'],
11:['calm, still, relief softening','warm, relieved','soft, grateful'],
12:['grand, proclaiming','explaining, warm, wise','tender, resonant','triumphant, joyful, resonant'],
13:['calm, winding down','gentle, soft intrigue'],
14:['tender, concerned','gentle, caring, coaxing'],
15:['sad, trembling, emotional','sorrowful, weary','heartbroken, bitter, hushed'],
16:['broken, hopeless, quiet, near tears'],
17:['slow, observing, contemplative','quiet, thoughtful, then soft'],
18:['despairing, doubtful','bitter, helpless'],
19:['calm, assured, wise','gentle but firm'],
20:['mysterious, hushed','hesitant, quiet','prayerful, deep, devotional'],
21:['soft, time passing','warm, moved','deep, calm, divine','pleading, earnest, humble'],
22:['firm, serious, deep','weighty pause','puzzled, short','soft, emphatic'],
23:['awed, rising','hushed wonder','slow, clear, majestic','reverent, marvelling','grand, revelatory'],
24:['stunned, hushed','wondering, soft','whispers, mysterious, gentle'],
25:['deep, calm, wise','teaching, warm','firm, resonant','devotional, joyful'],
26:['humble, grateful','earnest, pleading','warm, gracious, smiling','energized, brightening'],
27:['grand, creative','proud, measured','warm, ringing'],
28:['joyful, glowing','relieved, tender','content, soft'],
29:['whispers, uneasy, slowing','dark, low, foreboding','chilling, whispered quote','ominous, final'],
30:['calm, warm, inviting']}}
LEG='''## टैग-कुंजी (Voiceover tags)
हर पंक्ति से पहले `[ ]` में उसकी भावना/अंदाज़ लिखा है। इन्हें पढ़ना नहीं है। AI वॉइस टूल (जैसे ElevenLabs v3) में आप इन्हें सीधे रख सकते हैं, या अपनी आवाज़ रिकॉर्ड करते समय केवल मार्गदर्शन की तरह इस्तेमाल करें।
- `whispers` = फुसफुसाकर · `slow` = धीमे · `grand` = भव्य, गूँजती आवाज़ · `pause` = रुकें · `furious/shouting` = क्रोध, ऊँची आवाज़
- संवाद वाली पंक्तियों पर बोलने वाले का भाव लिखा है; नैरेशन वाली पंक्तियों पर कथावाचक का।

---
'''
for ep,tags in T.items():
    src=open(f'{R}/episodes/ep{ep}/script.md',encoding='utf-8').read().split('\n');out=[];beat=None;i=0;ok=True
    # collect lines per beat
    blocks={};cur=None
    for ln in src:
        m=re.match(r'\*\*B(\d+)\*\*',ln)
        if m:cur=int(m.group(1));blocks[cur]=[];continue
        if cur and ln.strip() and not ln.startswith(('---','#','*समाप्त')):blocks[cur].append(ln)
        elif cur and ln.startswith(('---','#')):cur=None
    for b,l in blocks.items():assert len(l)==len(tags[b]),(ep,b,len(l),len(tags[b]))
    cur=None;k=0
    for ln in src:
        m=re.match(r'\*\*B(\d+)\*\*',ln)
        if m:cur=int(m.group(1));k=0;out.append(ln);continue
        if ln.startswith('---') and not out[-1:]==['']:pass
        if cur and ln.strip() and not ln.startswith(('---','#','*समाप्त')):
            out.append(f'[{tags[cur][k]}] {ln}');k+=1;continue
        if ln.startswith(('---','#')):cur=None
        out.append(ln)
        if ln.startswith('# एपिसोड'):out.append('');out.append(LEG)
    open(f'{R}/episodes/ep{ep}/script_voiceover.md','w',encoding='utf-8').write('\n'.join(out))
    print(ep,sum(len(v) for v in blocks.values()),'lines tagged')
