#!/usr/bin/env python3
"""Generator for reels/reel02/briefs.json "Why Go to Kashi?" (cinematographer -> scene -> action -> effects passes, written as data).
Same method as reels/reel01/briefs_gen.py: every face is solved to 38-50% of the 9:16 frame height at the still time (55%)."""
import json,os,sys,copy
R='/home/user/mahagatha-studio'
sys.path.insert(0,R+'/studio')
import validate_brief as VB
W=json.load(open(f'{R}/reels/build/reel02/words.json'))
T=[(w['w'],w['start']) for w in W]
END=86.44
def span(i0,i1):return ' '.join(w for w,_ in T[i0:i1])
def idx(t):
    for i,(w,s) in enumerate(T):
        if abs(s-t)<.02:return i
    raise SystemExit(f'no word at {t}')
# ---------- palette ----------
SKY_GOLD=['#2f4aa8','#7d9ce8','#ffd49a','#fff3d6']
SKY_DAWN=['#3a5ab0','#8aa8e0','#ffc49a','#fff0cc']
SKY_KASHI=['#4a6ac0','#9ab8ea','#ffcf9a','#fff4d8']
SKY_CURSE=['#3a2a78','#7a5ab0','#d8a8d0','#f8e4ec']
SKY_VIOLET=['#251a5a','#5a4aa0','#b09ad8','#ecdff4']
SKY_FURY=['#3a1a3a','#8a3a4a','#e08a6a','#f8d8b8']
SKY_CALM=['#2c3c72','#5d70a8','#aab8d8','#e4e8f4']
SKY_MEADOW=['#3a6ac0','#86b6ea','#d8ecfa','#fff8ec']
SKY_ROSE=['#7a2a72','#c75c8e','#ffb48a','#fff0cc']
RIDGE_DAWN=['#c8b8d8','#a8a0c8','#8a8ab0','#6a7098']
RIDGE_MEADOW=['#b8d0e0','#98bcc8','#6e9a8a','#4a7a5a']
def far_clouds(haze='#f4e6d0',col='#fff4e6',xs=(520,780)):
    return {"d":"far","contents":"soft cloud banks and two hazy peaks far behind","fog":0.55,"haze":haze,
            "items":[{"o":"mountain","x":xs[0]-60,"y":500,"s":1.0,"col":"#9a9ac8"},{"o":"mountain","x":xs[1]+40,"y":510,"s":0.85,"col":"#9a9ac8"},
                     {"o":"cloud","x":xs[0],"y":230,"s":1.3,"col":col},{"o":"cloud","x":xs[1],"y":270,"s":1.1,"col":col}]}
def mid_pillars(xs=(450,830),col='#e8c878',h=520):
    return {"d":"mid","contents":"two gold pillars framing the figure","fog":0.2,"items":[{"o":"pillar","x":x,"y":700,"s":1.0,"col":col,"h":h} for x in xs]}
def near_clouds(xs=(470,810)):
    return {"d":"near","contents":"white cloud puffs low in the bottom corners","dark":0.1,"blur":2,
            "items":[{"o":"cloud","x":xs[0],"y":745,"s":1.7,"col":"#ffffff"},{"o":"cloud","x":xs[1],"y":748,"s":1.6,"col":"#ffffff"}]}
def mid_clouds(xs=(470,820),cols=('#e8dcf4','#f4e4ec')):
    return {"d":"mid","contents":"two soft clouds either side at the figure's shoulders","fog":0.25,"items":[{"o":"cloud","x":xs[0],"y":560,"s":1.1,"col":cols[0]},{"o":"cloud","x":xs[1],"y":570,"s":1.1,"col":cols[1]}]}
# Kashi: sandstone ghat buildings along the river, temple towers, palms, marigold shrubs
def far_ghats(xs=(470,820),haze='#ffe8d0'):
    return {"d":"far","contents":"a hazy row of sandstone ghat buildings along the far river bank","fog":0.5,"haze":haze,
            "items":[{"o":"wall","x":xs[0],"y":470,"s":0.55,"w":420,"h":220,"col":"#e8b888"},{"o":"wall","x":xs[1],"y":476,"s":0.5,"w":460,"h":200,"col":"#e0a878"},
                     {"o":"cloud","x":(xs[0]+xs[1])/2,"y":220,"s":1.1,"col":"#fff4e6"}]}
def mid_ghat(xs=(440,850)):
    return {"d":"mid","contents":"palms and a sandstone pillar on the ghat steps","fog":0.18,
            "items":[{"o":"tree","x":xs[0],"y":610,"s":0.8,"kind":"palm","col":"#2e6a3c"},{"o":"pillar","x":xs[1],"y":690,"s":0.9,"col":"#e8c08a","h":420},{"o":"tree","x":xs[1]+70,"y":600,"s":0.7,"kind":"palm","col":"#2e6a3c"}]}
def near_marigold(xs=(470,820)):
    return {"d":"near","contents":"marigold shrubs in the bottom corners","dark":0.35,
            "items":[{"o":"shrub","x":xs[0],"y":748,"s":1.5,"col":"#2a5a3a","flowers":"#f0a020"},{"o":"shrub","x":xs[1],"y":748,"s":1.4,"col":"#2a5a3a","flowers":"#f0c040"}]}
def bg_kashi(sx=640,sy=300):return {"k":"vista","sky":SKY_KASHI,"sx":sx,"sy":sy,"ridge":RIDGE_DAWN,"haze":"255,228,200","river":"#6ab0e0"}
def far_meadow(xs=(470,820)):
    return {"d":"far","contents":"blue hills and clouds in morning haze","fog":0.55,"haze":"#e4f0f8","items":[{"o":"hill","x":xs[0],"y":520,"s":1.0,"w":420,"h":90,"col":"#8aa0c8"},{"o":"cloud","x":xs[1],"y":220,"s":1.1,"col":"#ffffff"}]}
def mid_meadow(xs=(440,860)):
    return {"d":"mid","contents":"a round tree and a banyan on the meadow","fog":0.2,"items":[{"o":"tree","x":xs[0],"y":620,"s":0.8,"kind":"round","col":"#3a7a44"},{"o":"tree","x":xs[1],"y":615,"s":0.75,"kind":"banyan","col":"#2e6a3c"}]}
def near_shrubs(xs=(470,820)):
    return {"d":"near","contents":"flowering shrubs in the bottom corners","dark":0.45,"items":[{"o":"shrub","x":xs[0],"y":748,"s":1.5,"col":"#2a5a3a","flowers":"#f0c040"},{"o":"shrub","x":xs[1],"y":748,"s":1.4,"col":"#2a5a3a"}]}
def cosmos_layers(cols=('#cfe0ff','#e8d8ff')):
    return [{"d":"far","contents":"star field and nebula drawn by the cosmos background","fog":0.5,"from_background":True},
            mid_clouds(cols=cols),near_clouds()]
def shot(id,t,**k):
    i0=idx(t);s={"id":id,"beat":1,"start":{"t":t,"word":T[i0][0].strip(',.?!')}};s.update(k);return s
S=[]
# 1 ------------------------------------------------------------------- the question
S.append(shot("s01",0.18,
 meaning="The question: why do people travel to Kashi, the holy city also called Varanasi?",
 why="Two pilgrims walk along the bright river ghats of Kashi at sunrise toward a temple tower, under the title card; the woman folds her hands on 'Kashi'.",
 camera={"shot":"wide","lens":"wide","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.05,"x":0,"y":-4,"r":0},"shake":0,"motivation":"slow push in toward the city the question is about"},
 focus={"subject":"villager_w","depth":"deep"},vertical={"x":[640,660]},
 layers=[far_ghats((470,830)),mid_ghat((430,860)),near_marigold((460,830))],
 background=bg_kashi(640,300),
 mood={"emotion":"pilgrimage","grade":"warm"},
 characters=[{"who":"villager_w","x":600,"y":690,"s":0.95,"_face":0.5,"flip":1,"pose":"stand","emo":"calm","look":800,"walk":{"word":"travel","to_x":620,"d":1.6,"speed":0.8},
   "actions":[{"word":"Kashi","pose":"namaste","emo":"devotion","d":0.6}]},
  {"who":"villager","x":710,"y":690,"s":0.95,"_ground":True,"flip":1,"pose":"stand","emo":"calm","look":900,"walk":{"word":"travel","to_x":730,"d":1.6,"speed":0.8},
   "actions":[{"word":"Varanasi","emo":"joy","d":0.6}]}],
 effects=[{"k":"palace_gate","x":640,"y":300,"w":200,"alpha":0.75,"par":0.3,"behind":True,"meaning":"the temple of Kashi the pilgrims are travelling to"},
  {"k":"divine_rays","x":640,"y":120,"w":620,"alpha":0.3,"blend":"lighter","par":0.2,"behind":True,"meaning":"sunrise light over the sacred city"}],
 transition_in="fade"))
# 2
S.append(shot("s02",3.5,
 meaning="They go there to be freed of their sins.",
 why="Closer on the pilgrim at the water's edge: he closes his eyes in prayer on 'freed' and gold motes rise off him like a weight lifting.",
 camera={"shot":"medium","lens":"normal","move":"tilt_up","from":{"z":1.08,"x":0,"y":14,"r":0},"to":{"z":1.08,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilt up with the rising lightness of release"},
 focus={"subject":"villager","depth":"shallow"},vertical={"focus":"villager","z":1.15,"y":0.42},
 layers=[far_ghats((470,820)),mid_ghat((450,840)),near_marigold((480,820))],
 background=bg_kashi(700,280),
 mood={"emotion":"release","grade":"warm"},
 characters=[{"who":"villager","x":550,"y":680,"s":1.0,"_face":0.43,"flip":1,"pose":"stand","emo":"calm","look":760,
   "actions":[{"word":"freed","pose":"namaste","emo":"devotion","mood":{"blink":1,"smile":0.4},"d":0.6}]}],
 effects=[{"k":"embers","word":"freed","x":550,"y":520,"w":320,"alpha":0.55,"blend":"lighter","par":1.0,"rgb":"255,230,160","meaning":"gold motes rising as his sins fall away"},
  {"k":"glow","word":"sins","x":550,"y":400,"r":220,"rgb":"255,220,160","ga":0.45,"par":1.0,"behind":True,"meaning":"the warm light of being freed"}],
 transition_in="cut"))
# 3 ------------------------------------------------------------------- Brahma with five heads
S.append(shot("s03",5.26,
 meaning="The answer starts with Brahma, the creator god.",
 why="An iris opens on a gold heaven: five-headed Brahma sits on his pink lotus between gold pillars and lifts his chin with pride on 'creator'.",
 camera={"shot":"medium","lens":"normal","move":"crane_down","from":{"z":1.0,"x":0,"y":-24,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"descending from heaven to the creator"},
 focus={"subject":"brahma5","depth":"deep"},vertical={"focus":"brahma5"},
 layers=[far_clouds(),mid_pillars(),near_clouds()],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":190},
 mood={"emotion":"majesty","grade":"warm"},
 characters=[{"who":"brahma5","x":640,"y":690,"s":1.05,"_face":0.46,"flip":1,"pose":"sit","emo":"calm","look":640,
   "actions":[{"word":"creator","emo":"pride","mood":{"smile":0.4},"d":0.6}]}],
 effects=[{"k":"divine_rays","x":640,"y":80,"w":700,"alpha":0.4,"blend":"lighter","par":0.2,"behind":True,"meaning":"the light of the creator's heaven"}],
 transition_in="iris"))
# 4
S.append(shot("s04",8.22,
 meaning="Brahma once had five heads.",
 why="Close on Brahma's heads: the fifth head on top is lit by a gold halo ring that opens on 'five'.",
 camera={"shot":"close","lens":"tele","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-4,"r":0},"shake":0,"motivation":"push in to count the heads"},
 focus={"subject":"brahma5","depth":"shallow"},vertical={"focus":"brahma5"},
 layers=[far_clouds('#f4e6d0','#fff4e6',(500,800)),mid_pillars((450,830)),near_clouds()],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":200},
 mood={"emotion":"wonder","grade":"warm"},
 characters=[{"who":"brahma5","x":640,"y":410,"s":1.0,"flip":1,"head":True,"emo":"calm","look":640,
   "actions":[{"word":"five","emo":"pride","d":0.6}]}],
 effects=[{"k":"halo_ring","word":"five","x":640,"y":250,"w":360,"alpha":0.55,"blend":"lighter","par":0.9,"behind":True,"meaning":"the fifth head picked out in light"}],
 transition_in="cut"))
# 5 ------------------------------------------------------------------- the teaser: Shiva's rage, the head that would not let go
S.append(shot("s05",10.2,
 meaning="Shiva cut off one of those heads in rage.",
 why="Shiva lunges forward in fury, red eyes and trishul, in a red storm sky; a red pulse bursts behind him on 'rage'.",
 camera={"shot":"medium","lens":"normal","move":"handheld","from":{"z":1.05,"x":0,"y":0,"r":0.02},"to":{"z":1.1,"x":0,"y":-4,"r":0.03},"shake":3,"motivation":"unsteady frame for sudden fury"},
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[far_clouds('#e8c8c0','#f8e0d8',(520,800)),{"d":"mid","contents":"two dark rocks on the storm plain","fog":0.25,"items":[{"o":"rock","x":460,"y":640,"s":1.0,"col":"#6a4a5a"},{"o":"rock","x":830,"y":645,"s":0.9,"col":"#6a4a5a"}]},near_clouds()],
 background={"k":"cloudscape","sky":SKY_FURY,"sx":640,"sy":200},
 mood={"emotion":"wrath","grade":"red"},
 characters=[{"who":"shiva","x":640,"y":670,"s":1.0,"_face":0.42,"flip":1,"pose":"rage","emo":"anger",
   "actions":[{"word":"cut","pose":"lunge","emo":"rage","e":"antic","d":0.5}]}],
 effects=[{"k":"red_energy_pulse","word":"rage","x":640,"y":380,"w":520,"alpha":0.55,"blend":"lighter","par":0.9,"behind":True,"meaning":"the burst of Shiva's rage"},
  {"k":"lightning_forks","x":640,"y":120,"w":600,"alpha":0.4,"blend":"lighter","par":0.2,"behind":True,"meaning":"thunder of wrath far in the sky"}],
 transition_in="flash"))
# 6
S.append(shot("s06",12.3,
 meaning="Then the cut head would not let go of Shiva.",
 why="Shiva, now still, looks down at his left hand: Brahma's serene severed head, eyes closed, clings to it in a soft violet light.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-4,"r":0},"shake":0,"motivation":"push in on the strange burden"},
 focus={"subject":"kapali","depth":"shallow"},vertical={"focus":"kapali","z":1.15,"y":0.42},
 layers=cosmos_layers(),
 background={"k":"cosmos","rgb":"200,180,255","spin":0.03},
 mood={"emotion":"dread","grade":"cool"},
 characters=[{"who":"kapali","x":640,"y":680,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","prop":"head","emo":"surprise","mood":{"ly":0.5,"lx":0.5},
   "actions":[{"word":"not","emo":"sad","mood":{"ly":0.6,"lx":0.6},"d":0.6}]}],
 effects=[{"k":"glow","x":560,"y":520,"r":160,"rgb":"210,190,255","ga":0.5,"par":1.0,"behind":True,"meaning":"the head that stays fixed to his hand"}],
 transition_in="cut"))
# 7 ------------------------------------------------------------------- the curse
S.append(shot("s07",14.36,
 meaning="It all began with a curse spoken by the sage Narada.",
 why="Flashback iris: Narada with his veena points in anger; a red pulse spreads from his hand on 'curse' and his name appears as it is spoken.",
 camera={"shot":"medium","lens":"normal","move":"tilt_down","from":{"z":1.05,"x":0,"y":-26,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilting down from the sky to the one who curses"},
 focus={"subject":"narada","depth":"deep"},vertical={"focus":"narada"},
 layers=[far_clouds('#e8d8f0','#f8eef8',(520,800)),mid_pillars((460,820),'#d8c0a0'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_CURSE,"sx":640,"sy":200},
 mood={"emotion":"foreboding","grade":"cool"},
 characters=[{"who":"narada","x":640,"y":670,"s":1.0,"_face":0.44,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":800,
   "actions":[{"word":"curse","pose":"point","emo":"anger","e":"antic","d":0.5}]}],
 effects=[{"k":"red_energy_pulse","word":"curse","x":760,"y":360,"w":360,"alpha":0.5,"blend":"lighter","par":1.0,"behind":True,"meaning":"the curse leaving Narada's pointing hand"},
  {"k":"name","word":"Narada","s":"Narada","x":640,"y":140,"size":30,"d":0.25,"meaning":"the sage's name on screen when it is spoken"}],
 transition_in="iris"))
# 8
S.append(shot("s08",17.6,
 meaning="Narada's curse: Brahma would desire what must not be desired.",
 why="Brahma sits on his lotus as a violet mist curls round him on 'desire'; his face clouds with doubt, then fear on 'not'.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.08,"x":0,"y":-6,"r":0},"shake":0,"motivation":"push in as the curse settles on him"},
 focus={"subject":"brahma5","depth":"deep"},vertical={"focus":"brahma5"},
 layers=[far_clouds('#e8d8f0','#f8eef8',(520,800)),mid_pillars((460,820),'#d8c0a0'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_CURSE,"sx":640,"sy":200},
 mood={"emotion":"foreboding","grade":"cool"},
 characters=[{"who":"brahma5","x":640,"y":690,"s":1.05,"_face":0.45,"flip":1,"pose":"sit","emo":"calm","look":640,
   "actions":[{"word":"desire","emo":"doubt","d":0.6},{"word":"not","emo":"fear","mood":{"ly":0.3},"d":0.6}]}],
 effects=[{"k":"mist_wisps","word":"desire","x":640,"y":470,"w":520,"alpha":0.45,"par":1.0,"meaning":"the curse curling around Brahma like a violet mist"},
  {"k":"glow","word":"desire","x":640,"y":380,"r":240,"rgb":"170,120,220","ga":0.4,"par":1.0,"behind":True,"meaning":"the curse's violet shadow on him"}],
 transition_in="cut"))
# 9 ------------------------------------------------------------------- Brahmi
S.append(shot("s09",20.72,
 meaning="Brahma created his daughter Brahmi.",
 why="On 'created' Brahma opens his arms on the lotus and Brahmi takes shape from rose-gold light beside him, folding her hands on 'Brahmi'.",
 camera={"shot":"two_shot","lens":"normal","move":"dolly_right","from":{"z":1.0,"x":-6,"y":0,"r":0},"to":{"z":1.0,"x":6,"y":0,"r":0},"shake":0,"motivation":"dolly from the creator to the one he creates"},
 focus={"subject":"brahmi","depth":"deep"},vertical={"x":[600,700]},
 layers=[far_clouds('#f4e6d0','#fff4e6',(540,800)),mid_pillars((470,900)),near_clouds((480,880))],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":700,"sy":190},
 mood={"emotion":"creation","grade":"warm"},
 characters=[{"who":"brahma5","x":540,"y":690,"s":0.85,"_face":0.46,"flip":1,"pose":"sit","emo":"calm","look":"brahmi",
   "actions":[{"word":"created","emo":"joy","d":0.6}]},
  {"who":"brahmi","x":760,"y":680,"s":0.95,"_face":0.45,"flip":-1,"pose":"stand","emo":"surprise","look":"brahma5","engine_cues":{"ac":"created"},"engine":{"ad":0.7},
   "actions":[{"word":"Brahmi","pose":"namaste","emo":"calm","d":0.6}]}],
 effects=[{"k":"halo_ring","word":"daughter","x":760,"y":380,"w":340,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"Brahmi forming in light"},
  {"k":"glow","word":"created","x":760,"y":420,"r":200,"rgb":"255,200,170","ga":0.5,"par":1.0,"behind":True,"meaning":"rose-gold light of her creation"}],
 transition_in="fade"))
# 10
S.append(shot("s10",22.98,
 meaning="The curse took hold of Brahma.",
 why="Close on Brahma's heads: the sky behind turns violet on 'curse' and his eyes fix sideways, still, on 'hold'; nothing else is shown.",
 camera={"shot":"close","lens":"tele","move":"static","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"stillness: the fixed stare is the event"},
 focus={"subject":"brahma5","depth":"shallow"},vertical={"focus":"brahma5"},
 layers=[far_clouds('#e8d8f0','#f8eef8',(500,800)),mid_pillars((450,830),'#d8c0a0'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":200,"change":{"word":"curse","bg2":{"k":"cloudscape","sky":SKY_CURSE,"sx":640,"sy":200},"d":0.9}},
 mood={"emotion":"obsession","grade":"cool"},
 characters=[{"who":"brahma5","x":640,"y":410,"s":1.0,"flip":1,"head":True,"emo":"calm","look":640,
   "actions":[{"word":"hold","emo":"calm","mood":{"lx":0.8,"ly":0.1,"smile":0.1},"d":0.6}]}],
 effects=[{"k":"glow","word":"curse","x":640,"y":300,"r":300,"rgb":"150,100,210","ga":0.45,"par":0.9,"behind":True,"meaning":"the curse's violet shadow taking hold"}],
 transition_in="cut"))
# 11
S.append(shot("s11",24.58,
 meaning="Brahmi saw how Brahma was looking at her and moved away.",
 why="Brahmi, at a distance from Brahma, notices his gaze on 'saw', lowers her eyes and turns away on 'moved', walking out of his reach.",
 camera={"shot":"two_shot","lens":"normal","move":"pan_right","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"the pan follows her moving away"},
 focus={"subject":"brahmi","depth":"deep"},vertical={"x":[620,690]},
 layers=[far_clouds('#e8d8f0','#f8eef8',(560,820)),{"d":"mid","contents":"gold pillars between them","fog":0.2,"items":[{"o":"pillar","x":400,"y":700,"s":1.0,"col":"#e8c878","h":520},{"o":"pillar","x":640,"y":700,"s":0.8,"col":"#e8c878","h":460},{"o":"pillar","x":900,"y":700,"s":1.0,"col":"#e8c878","h":520}]},near_clouds((470,900))],
 background={"k":"cloudscape","sky":SKY_CURSE,"sx":700,"sy":190},
 mood={"emotion":"unease","grade":"cool"},
 characters=[{"who":"brahma5","x":530,"y":680,"s":0.72,"_face":0.44,"flip":1,"pose":"stand","lotus":False,"emo":"calm","mood":{"lx":0.8},
   "actions":[{"word":"gaze","emo":"calm","mood":{"lx":0.8},"d":0.6}]},
  {"who":"brahmi","x":740,"y":680,"s":0.8,"_ground":True,"flip":-1,"pose":"stand","emo":"calm","look":"brahma5","turn_on":"moved","walk":{"word":"moved","to_x":800,"d":1.2,"speed":1},
   "actions":[{"word":"saw","emo":"fear","d":0.5},{"word":"moved","emo":"shame","mood":{"ly":0.5},"d":0.5}]}],
 effects=[],transition_in="cut"))
# 12
S.append(shot("s12",26.94,
 meaning="Each time Brahmi moved to another side to avoid his gaze...",
 why="Brahmi walks across the cloud floor with her eyes lowered, her face turned from where Brahma is; a pale violet light follows her.",
 camera={"shot":"medium","lens":"normal","move":"dolly_left","from":{"z":1.02,"x":8,"y":0,"r":0},"to":{"z":1.02,"x":-8,"y":0,"r":0},"shake":0,"motivation":"travelling with her as she moves away"},
 focus={"subject":"brahmi","depth":"deep"},vertical={"focus":"brahmi"},
 layers=[far_clouds('#e8d8f0','#f8eef8',(500,800)),mid_pillars((440,840),'#d8c0a0'),near_clouds((460,820))],
 background={"k":"cloudscape","sky":SKY_CURSE,"sx":560,"sy":200},
 mood={"emotion":"avoidance","grade":"cool"},
 characters=[{"who":"brahmi","x":700,"y":680,"s":1.0,"_face":0.44,"flip":-1,"pose":"stand","emo":"sad","mood":{"sad":0.5,"lx":-0.8,"ly":0.4},"walk":{"word":"Each","to_x":600,"d":1.2,"speed":1},
   "actions":[{"word":"moved","emo":"shame","mood":{"sad":0.5,"lx":-0.8,"ly":0.5},"d":0.5}]}],
 effects=[{"k":"glow","x":640,"y":420,"r":220,"rgb":"190,170,240","ga":0.35,"par":1.0,"behind":True,"meaning":"the pale violet light of her unease"}],
 transition_in="cut"))
# 13
S.append(shot("s13",28.16,
 meaning="...a new head grew on Brahma so he could keep looking at her.",
 why="Standing Brahma, eyes turned sideways; on 'grew' a fifth head rises on top of his crown inside a halo ring, facing where she went.",
 camera={"shot":"medium","lens":"normal","move":"tilt_up","from":{"z":1.05,"x":0,"y":16,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilt up to the new head as it grows"},
 focus={"subject":"brahma5","depth":"deep"},vertical={"focus":"brahma5","z":1.12,"y":0.47},
 layers=[far_clouds('#e8d8f0','#f8eef8',(500,800)),mid_pillars((440,840),'#d8c0a0'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_CURSE,"sx":640,"sy":200},
 mood={"emotion":"obsession","grade":"cool"},
 characters=[{"who":"brahma5","x":640,"y":680,"s":1.0,"_face":0.47,"flip":1,"pose":"stand","lotus":False,"emo":"calm","mood":{"lx":0.8},"_hd":{"l":1,"r":1,"b":1,"t":"grew"},
   "actions":[{"word":"looking","emo":"calm","mood":{"lx":0.9},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"grew","x":640,"y":250,"w":300,"alpha":0.55,"blend":"lighter","par":0.9,"behind":True,"meaning":"light around the new fifth head as it grows"}],
 transition_in="cut"))
# 14 ------------------------------------------------------------------- the sons warn
S.append(shot("s14",31.0,
 meaning="Brahma's sons, the sages Marichi and Atri, warned him.",
 why="Marichi raises a warning hand and Atri points sternly toward their father off-frame; each name appears as it is spoken.",
 camera={"shot":"two_shot","lens":"normal","move":"dolly_right","from":{"z":1.0,"x":-6,"y":0,"r":0},"to":{"z":1.0,"x":6,"y":0,"r":0},"shake":0,"motivation":"drifting across the two sons as they speak"},
 focus={"subject":"rishi1","depth":"deep"},vertical={"x":[630,660]},
 layers=[far_clouds('#f0e4d8','#fff4ec',(520,800)),mid_pillars((430,880),'#e0c890'),near_clouds((470,830))],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":200},
 mood={"emotion":"warning","grade":"warm"},
 characters=[{"who":"rishi1","x":570,"y":680,"s":0.95,"_face":0.45,"flip":-1,"pose":"stand","emo":"doubt","talk":0.5,"look":400,
   "actions":[{"word":"warned","pose":"raise","emo":"anger","e":"spring","d":0.5}]},
  {"who":"rishi2","x":720,"y":680,"s":0.95,"_ground":True,"flip":-1,"pose":"stand","emo":"doubt","look":400,
   "actions":[{"word":"Atri","pose":"point","emo":"doubt","d":0.5}]}],
 effects=[{"k":"name","word":"Marichi","s":"Marichi","x":570,"y":120,"size":26,"d":0.25,"meaning":"Marichi's name when it is spoken"},
  {"k":"name","word":"Atri","s":"Atri","x":720,"y":190,"size":26,"d":0.25,"meaning":"Atri's name when it is spoken"}],
 transition_in="fade"))
# 15 ------------------------------------------------------------------- Shatarupa forms
S.append(shot("s15",33.78,
 meaning="Brahmi changed herself into a cow.",
 why="Brahmi stands in a meadow; on 'became' she fades in a ring of light and a white cow wearing her gold necklace stands in her place, facing away from Brahma.",
 camera={"shot":"medium","lens":"normal","move":"pull_out","from":{"z":1.1,"x":0,"y":-6,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"pull out to reveal the new form"},
 focus={"subject":"cow","depth":"deep"},vertical={"x":[600,560]},
 layers=[far_meadow(),mid_meadow(),near_shrubs()],
 background={"k":"vista","sky":SKY_MEADOW,"sx":760,"sy":220,"ridge":RIDGE_MEADOW,"haze":"230,240,255"},
 mood={"emotion":"escape","grade":"warm"},
 characters=[{"who":"brahmi","x":600,"y":500,"s":0.72,"flip":-1,"pose":"stand","emo":"sad","look":300,"mood":{"sad":0.5,"lx":-0.8,"ly":0.4},"engine_cues":{"fo":"became"},"engine":{"fd":0.3}},
  {"who":"cow","x":600,"y":500,"s":0.8,"flip":-1,"pose":"stand","emo":"calm","look":300,"engine_cues":{"ac":"became"},"engine":{"ad":0.6},
   "actions":[{"word":"cow","mood":{"blink":1},"d":0.3}]}],
 effects=[{"k":"halo_ring","word":"became","x":600,"y":340,"w":360,"alpha":0.55,"blend":"lighter","par":1.0,"behind":True,"meaning":"the light of her change of form"}],
 transition_in="wipe"))
# 16
S.append(shot("s16",35.22,
 meaning="She became a mare, and then a duck.",
 why="A palomino mare with Brahmi's necklace trots left across the meadow behind, and a cream duck with the same gold necklace takes shape in front as the forms keep changing.",
 camera={"shot":"wide","lens":"wide","move":"pan_left","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"the pan runs with her as she flees"},
 focus={"subject":"mare","depth":"deep"},vertical={"x":[650,610]},
 layers=[far_meadow((520,800)),mid_meadow((430,880)),near_shrubs((470,820))],
 background={"k":"vista","sky":SKY_MEADOW,"sx":700,"sy":220,"ridge":RIDGE_MEADOW,"haze":"230,240,255","river":"#7ac0e8"},
 mood={"emotion":"escape","grade":"warm"},
 characters=[{"who":"mare","x":760,"y":500,"s":0.5,"flip":-1,"pose":"stand","emo":"calm","look":300,"engine":{"walk":1,"vx":-14},
   "actions":[{"word":"mare","mood":{"blink":1},"d":0.3}]},
  {"who":"duck","x":600,"y":520,"s":1.55,"flip":-1,"pose":"stand","emo":"calm","look":300,"engine_cues":{"ac":"mare"},"engine":{"ad":0.45},
   "actions":[{"word":"duck","mood":{"blink":1},"d":0.3}]}],
 effects=[{"k":"glow","word":"mare","x":590,"y":400,"r":170,"rgb":"255,230,170","ga":0.45,"par":1.0,"behind":True,"meaning":"the light of the next change"}],
 transition_in="cut"))
# 17
S.append(shot("s17",36.66,
 meaning="She became a doe, and a hundred forms in all.",
 why="A spotted doe with Brahmi's necklace steps left in front; behind her in the haze stand her earlier forms, cow and mare, as glowing halo rings multiply on 'hundred'.",
 camera={"shot":"wide","lens":"wide","move":"crane_up","from":{"z":1.06,"x":0,"y":10,"r":0},"to":{"z":1.0,"x":0,"y":-4,"r":0},"shake":0,"motivation":"crane up to show the many forms"},
 focus={"subject":"doe","depth":"deep"},vertical={"x":[630,650]},
 layers=[far_meadow((500,800)),mid_meadow((440,860)),near_shrubs((470,820))],
 background={"k":"vista","sky":SKY_MEADOW,"sx":640,"sy":220,"ridge":RIDGE_MEADOW,"haze":"230,240,255"},
 mood={"emotion":"wonder","grade":"warm"},
 characters=[{"who":"cow","x":520,"y":470,"s":0.4,"flip":-1,"pose":"stand","emo":"calm","look":300,"engine":{"a":0.45},"engine_cues":{"ac":"hundred"},
   "actions":[{"word":"forms","mood":{"blink":1},"d":0.3}]},
  {"who":"mare","x":760,"y":470,"s":0.33,"flip":-1,"pose":"stand","emo":"calm","look":300,"engine":{"a":0.45},"engine_cues":{"ac":"hundred"},
   "actions":[{"word":"forms","mood":{"blink":1},"d":0.3}]},
  {"who":"doe","x":680,"y":525,"s":0.85,"flip":-1,"pose":"stand","emo":"calm","look":300,"engine":{"walk":1,"vx":-10},
   "actions":[{"word":"doe","mood":{"blink":1},"d":0.3}]}],
 effects=[{"k":"halo_ring","word":"hundred","x":560,"y":330,"w":220,"alpha":0.45,"blend":"lighter","par":0.8,"behind":True,"meaning":"one of her many forms"},
  {"k":"halo_ring","word":"forms","x":740,"y":300,"w":200,"alpha":0.45,"blend":"lighter","par":0.8,"behind":True,"meaning":"another of her hundred forms"},
  {"k":"glow","word":"hundred","x":640,"y":360,"r":280,"rgb":"255,235,190","ga":0.35,"par":0.8,"behind":True,"meaning":"the light of a hundred forms"}],
 transition_in="cut"))
# 18
S.append(shot("s18",39.08,
 meaning="Because of her hundred forms she was named Shatarupa.",
 why="Close on Brahmi's calm face inside a rose-gold halo ring, eyes gently lowered; the name Shatarupa appears above her as it is spoken.",
 camera={"shot":"close","lens":"tele","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.08,"x":0,"y":-4,"r":0},"shake":0,"motivation":"push in as she is named"},
 focus={"subject":"brahmi","depth":"shallow"},vertical={"focus":"brahmi"},
 layers=[far_clouds('#f8dcd0','#fff0e8',(500,800)),mid_pillars((450,830),'#f0c890'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_ROSE,"sx":640,"sy":240},
 mood={"emotion":"grace","grade":"warm"},
 characters=[{"who":"brahmi","x":640,"y":380,"s":1.15,"flip":1,"head":True,"emo":"calm","mood":{"ly":0.3},"look":640,
   "actions":[{"word":"Shatarupa","emo":"calm","mood":{"smile":0.3,"ly":0.2},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"named","x":640,"y":360,"w":520,"alpha":0.5,"blend":"lighter","par":0.9,"behind":True,"meaning":"the sacred name given to her"},
  {"k":"name","word":"Shatarupa","s":"Shatarupa","x":640,"y":150,"size":30,"d":0.25,"meaning":"her new name on screen when it is spoken"}],
 transition_in="fade"))
# 19 ------------------------------------------------------------------- Shiva's fury
S.append(shot("s19",41.0,
 meaning="Shiva appeared, furious.",
 why="A white flash and Shiva stands in his rage stance with trishul and red eyes against a red storm sky; lightning forks far behind on 'fury'.",
 camera={"shot":"low_angle","lens":"wide","move":"tilt_up","from":{"z":1.05,"x":0,"y":24,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":2,"motivation":"tilting up to his towering wrath"},
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[far_clouds('#e8c8c0','#f8e0d8',(500,800)),{"d":"mid","contents":"dark rocks either side","fog":0.25,"items":[{"o":"rock","x":450,"y":640,"s":1.0,"col":"#6a4a5a"},{"o":"rock","x":840,"y":645,"s":0.9,"col":"#6a4a5a"}]},near_clouds()],
 background={"k":"cloudscape","sky":SKY_FURY,"sx":640,"sy":200},
 mood={"emotion":"wrath","grade":"red"},
 characters=[{"who":"shiva","x":640,"y":670,"s":1.05,"_face":0.43,"flip":1,"pose":"stand","emo":"anger","engine_cues":{"ac":"appeared"},"engine":{"ad":0.4},
   "actions":[{"word":"fury","pose":"rage","emo":"rage","e":"spring","d":0.5}]}],
 effects=[{"k":"lightning_forks","word":"fury","x":640,"y":120,"w":620,"alpha":0.5,"blend":"lighter","par":0.2,"behind":True,"meaning":"the storm of his fury far in the sky"},
  {"k":"glow","word":"appeared","x":640,"y":360,"r":260,"rgb":"255,110,80","ga":0.4,"par":0.9,"behind":True,"meaning":"the red heat of his anger"}],
 transition_in="flash"))
# 20
S.append(shot("s20",42.92,
 meaning="Brahma came to his senses and begged Shiva for forgiveness.",
 why="Stacked: furious Shiva above glares down; below, five-headed Brahma's face falls in shame on 'senses' and he bows with joined hands on 'begged'.",
 camera={"shot":"two_shot","lens":"normal","move":"crane_down","from":{"z":1.0,"x":0,"y":-16,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"from the angry god down to the pleading creator"},
 focus={"subject":"brahma5","depth":"deep"},vertical={"mode":"stack","stack":["shiva","brahma5"]},
 layers=[far_clouds('#e8c8c0','#f8e0d8',(380,860)),{"d":"mid","contents":"dark rocks and a gold pillar","fog":0.25,"items":[{"o":"rock","x":250,"y":640,"s":1.0,"col":"#6a4a5a"},{"o":"pillar","x":1030,"y":700,"s":1.0,"col":"#d8c08a","h":500}]},near_clouds((300,980))],
 background={"k":"cloudscape","sky":SKY_FURY,"sx":640,"sy":200},
 mood={"emotion":"remorse","grade":"red"},
 characters=[{"who":"shiva","x":420,"y":660,"s":0.95,"flip":1,"pose":"rage","emo":"rage","look":"brahma5",
   "actions":[{"word":"begged","emo":"anger","d":0.6}]},
  {"who":"brahma5","x":880,"y":680,"s":0.9,"flip":-1,"pose":"stand","lotus":False,"emo":"fear","look":"shiva",
   "actions":[{"word":"senses","pose":"plead","emo":"shame","d":0.6},{"word":"begged","pose":"bow","emo":"shame","e":"spring","d":0.6}]}],
 effects=[{"k":"glow","x":420,"y":330,"r":220,"rgb":"255,110,80","ga":0.4,"par":1.0,"behind":True,"meaning":"Shiva's anger"}],
 transition_in="cut"))
# 21 ------------------------------------------------------------------- the cut (tasteful: light slash + cross-fade)
S.append(shot("s21",45.86,
 meaning="Shiva cut off Brahma's fifth head.",
 why="A blade of white light sweeps across the top of Brahma's crown on 'cut' with a bright flash; the fifth head is gone in the light and four-headed Brahma remains, eyes shut.",
 camera={"shot":"medium","lens":"normal","move":"static","from":{"z":1.05,"x":0,"y":0,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":5,"motivation":"a hard jolt on the stroke, nothing else moves"},
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma","z":1.1,"y":0.46},
 layers=[far_clouds('#e8c8c0','#f8e0d8',(500,800)),mid_pillars((450,830),'#d8c08a'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_FURY,"sx":640,"sy":200},
 mood={"emotion":"shock","grade":"red"},
 characters=[{"who":"brahma5","x":640,"y":680,"s":1.0,"flip":1,"pose":"stand","lotus":False,"emo":"fear","engine_cues":{"fo":"off"},"engine":{"fd":0.35},
   "actions":[{"word":"cut","emo":"fear","mood":{"blink":1},"d":0.3}]},
  {"who":"brahma","x":640,"y":680,"s":1.0,"_face":0.46,"flip":1,"pose":"stand","lotus":False,"emo":"shame","mood":{"blink":1},"engine_cues":{"ac":"off"},"engine":{"ad":0.35},
   "actions":[{"word":"head","emo":"grief","mood":{"blink":1},"d":0.5}]}],
 effects=[{"k":"light_beam","word":"cut","x":640,"y":230,"w":90,"rot":1.35,"alpha":0.75,"blend":"lighter","par":1.0,"meaning":"the stroke of the cut as a blade of white light"},
  {"k":"glow","word":"cut","x":640,"y":240,"r":200,"rgb":"255,250,230","ga":0.7,"par":1.0,"meaning":"the flash that hides the cut"},
  {"k":"glow","x":360,"y":360,"r":260,"rgb":"140,170,255","ga":0.4,"par":0.9,"behind":True,"meaning":"Shiva's presence just out of frame"}],
 transition_in="cut"))
# 22
S.append(shot("s22",47.74,
 meaning="Brahma's four remaining mouths would recite the Vedas forever as penance.",
 why="Four-headed Brahma sits in prayer, eyes closed in remorse; on 'Vedas' the four glowing Veda books rise one by one in front of the gold clouds.",
 camera={"shot":"medium","lens":"normal","move":"pull_out","from":{"z":1.04,"x":0,"y":-4,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"pull out into his endless recitation"},
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_clouds('#f4e6d0','#fff4e6',(500,800)),mid_pillars((440,840)),near_clouds()],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":200},
 mood={"emotion":"penance","grade":"warm"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.05,"_face":0.47,"flip":1,"pose":"sitpray","emo":"devotion","talk":0.5,"mood":{"blink":1},"engine_cues":{"_b1":"mouths","_b2":"recite","_b3":"Vedas"},
   "actions":[{"word":"repent","emo":"shame","mood":{"blink":1},"d":0.6}]}],
 effects=[{"k":"books","word":"four","x":640,"y":140,"gap":98,"names":["Rig","Yajur","Sama","Atharva"],"meaning":"the four Vedas that his four mouths recite"}],
 transition_in="fade"))
# 23
S.append(shot("s23",51.92,
 meaning="Then Shiva stopped his attack and his fury left him.",
 why="Shiva, still in his rage stance, freezes; on 'stopped' his fury drains into surprise and the red storm sky cools to dusk blue.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-4,"r":0},"shake":0,"motivation":"push in on the moment he stops"},
 focus={"subject":"shiva","depth":"deep"},vertical={"focus":"shiva"},
 layers=[far_clouds('#e0d8e8','#f4eef8',(500,800)),{"d":"mid","contents":"dark rocks either side","fog":0.25,"items":[{"o":"rock","x":450,"y":640,"s":1.0,"col":"#6a5a7a"},{"o":"rock","x":840,"y":645,"s":0.9,"col":"#6a5a7a"}]},near_clouds()],
 background={"k":"cloudscape","sky":SKY_FURY,"sx":640,"sy":200,"change":{"word":"stopped","bg2":{"k":"cloudscape","sky":SKY_CALM,"sx":640,"sy":200},"d":1.0}},
 mood={"emotion":"stillness","grade":"cool"},
 characters=[{"who":"shiva","x":640,"y":670,"s":1.05,"_face":0.43,"flip":1,"pose":"rage","emo":"anger",
   "actions":[{"word":"stopped","pose":"stand","emo":"surprise","d":0.6}]}],
 effects=[],transition_in="cut"))
# 24 ------------------------------------------------------------------- the head stuck to his hand
S.append(shot("s24",53.52,
 meaning="Brahma's severed head was stuck to Shiva's left hand.",
 why="Shiva looks down at his left hand, where Brahma's serene head with closed eyes hangs fixed in a pale glow; he cannot shake it off.",
 camera={"shot":"medium","lens":"normal","move":"tilt_down","from":{"z":1.08,"x":0,"y":-10,"r":0},"to":{"z":1.08,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilt down from his face to his hand"},
 focus={"subject":"kapali","depth":"shallow"},vertical={"focus":"kapali","z":1.2,"y":0.4},
 layers=[far_clouds('#d8dcec','#eef0f8',(500,800)),{"d":"mid","contents":"grey rocks on the plain","fog":0.25,"items":[{"o":"rock","x":450,"y":640,"s":1.0,"col":"#7a7a9a"},{"o":"rock","x":840,"y":645,"s":0.9,"col":"#7a7a9a"}]},near_clouds()],
 background={"k":"cloudscape","sky":SKY_CALM,"sx":640,"sy":200},
 mood={"emotion":"dread","grade":"cool"},
 characters=[{"who":"kapali","x":640,"y":680,"s":1.05,"_face":0.4,"flip":1,"pose":"stand","prop":"head","emo":"surprise","mood":{"ly":0.6,"lx":0.6},
   "actions":[{"word":"left","emo":"sad","mood":{"ly":0.7,"lx":0.7},"d":0.6}]}],
 effects=[{"k":"glow","word":"stuck","x":555,"y":520,"r":150,"rgb":"230,220,255","ga":0.55,"par":1.0,"behind":True,"meaning":"the severed head held fast to his hand"}],
 transition_in="fade"))
# 25
S.append(shot("s25",56.06,
 meaning="To kill a Brahmin was a sin, so Shiva was now bound by it.",
 why="Shiva's head bows in shame and a dull red shadow gathers behind him on 'sin' as the light around him dims.",
 camera={"shot":"medium","lens":"normal","move":"dolly_left","from":{"z":1.04,"x":8,"y":0,"r":0},"to":{"z":1.04,"x":-8,"y":0,"r":0},"shake":0,"motivation":"a slow sideways drift away from him in judgement"},
 focus={"subject":"kapali","depth":"deep"},vertical={"focus":"kapali"},
 layers=[far_clouds('#d8d0dc','#eee8f0',(500,800)),{"d":"mid","contents":"grey rocks on the plain","fog":0.25,"items":[{"o":"rock","x":450,"y":640,"s":1.0,"col":"#7a6a8a"},{"o":"rock","x":840,"y":645,"s":0.9,"col":"#7a6a8a"}]},near_clouds()],
 background={"k":"cloudscape","sky":SKY_CALM,"sx":640,"sy":200,"change":{"word":"sin","bg2":{"k":"cloudscape","sky":['#3a2a4a','#6a4a6a','#b89098','#e8d8dc'],"sx":640,"sy":200},"d":1.0}},
 mood={"emotion":"guilt","grade":"cool"},
 characters=[{"who":"kapali","x":640,"y":680,"s":1.05,"_face":0.43,"flip":1,"pose":"stand","prop":"head","emo":"sad","look":640,
   "actions":[{"word":"Brahmin","emo":"shame","mood":{"ly":0.8},"tilt":-0.06,"d":0.6}]}],
 effects=[{"k":"glow","word":"sin","x":640,"y":380,"r":280,"rgb":"200,70,80","ga":0.35,"par":0.9,"behind":True,"meaning":"the shadow of the sin of killing a Brahmin"}],
 transition_in="cut"))
# 26
S.append(shot("s26",58.16,
 meaning="Atri said that every action brings its result, whatever the reason behind it.",
 why="The white-bearded sage Atri speaks with an open teaching hand on 'action'; a slow gold yantra wheel turns behind him on 'result', the wheel of cause and effect.",
 camera={"shot":"medium","lens":"normal","move":"pull_out","from":{"z":1.1,"x":0,"y":-6,"r":0},"to":{"z":1.02,"x":0,"y":0,"r":0},"shake":0,"motivation":"pull out as the lesson widens"},
 focus={"subject":"rishi2","depth":"deep"},vertical={"focus":"rishi2"},
 layers=[far_clouds('#f0e4d8','#fff4ec',(500,800)),mid_pillars((450,830),'#e0c890'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_GOLD,"sx":640,"sy":200},
 mood={"emotion":"wisdom","grade":"warm"},
 characters=[{"who":"rishi2","x":640,"y":670,"s":1.0,"_face":0.45,"flip":1,"pose":"stand","emo":"calm","talk":0.6,"look":640,
   "actions":[{"word":"action","pose":"open","emo":"calm","d":0.6},{"word":"reason","emo":"doubt","tilt":0.05,"d":0.6}]}],
 effects=[{"k":"magic_circle","word":"result","x":640,"y":330,"w":420,"alpha":0.45,"spin":0.2,"par":0.9,"behind":True,"meaning":"the turning wheel of every action and its result"}],
 transition_in="fade"))
# 27
S.append(shot("s27",62.26,
 meaning="Brahma had paid for his act, even though a curse drove him to it.",
 why="Four-headed Brahma sits in quiet penance with eyes closed; a faint violet curse-mist drifts away behind him on 'curse'.",
 camera={"shot":"medium","lens":"normal","move":"dolly_right","from":{"z":1.04,"x":-8,"y":0,"r":0},"to":{"z":1.04,"x":8,"y":0,"r":0},"shake":0,"motivation":"a calm sideways drift over the one who has paid"},
 focus={"subject":"brahma","depth":"deep"},vertical={"focus":"brahma"},
 layers=[far_clouds('#e8e0f0','#f8f0f8',(500,800)),mid_pillars((440,840),'#d8c8a8'),near_clouds()],
 background={"k":"cloudscape","sky":SKY_VIOLET,"sx":640,"sy":220},
 mood={"emotion":"atonement","grade":"cool"},
 characters=[{"who":"brahma","x":640,"y":690,"s":1.05,"_face":0.47,"flip":1,"pose":"sitpray","emo":"sad","mood":{"blink":1},
   "actions":[{"word":"paid","emo":"devotion","mood":{"blink":1},"d":0.6}]}],
 effects=[{"k":"mist_wisps","word":"curse","x":640,"y":420,"w":520,"alpha":0.35,"par":0.9,"behind":True,"meaning":"the curse that drove him, drifting behind him"}],
 transition_in="cut"))
# 28
S.append(shot("s28",64.88,
 meaning="So Shiva too must pay.",
 why="Close on Shiva's face: he lowers his eyes and accepts it, the calm sad look of one who knows he must pay.",
 camera={"shot":"close","lens":"tele","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-4,"r":0},"shake":0,"motivation":"push in on his acceptance"},
 focus={"subject":"kapali","depth":"shallow"},vertical={"focus":"kapali"},
 layers=[far_clouds('#d8dcec','#eef0f8',(500,800)),mid_clouds(),near_clouds()],
 background={"k":"cloudscape","sky":SKY_CALM,"sx":640,"sy":220},
 mood={"emotion":"acceptance","grade":"cool"},
 characters=[{"who":"kapali","x":640,"y":330,"s":1.0,"flip":1,"head":True,"emo":"sad","look":640,
   "actions":[{"word":"Shiva","emo":"sad","mood":{"ly":0.6},"d":0.5}]}],
 effects=[{"k":"halo_ring","word":"must","x":640,"y":330,"w":520,"alpha":0.4,"blend":"lighter","par":0.9,"behind":True,"meaning":"the quiet weight of his duty to pay"}],
 transition_in="cut"))
# 29 ------------------------------------------------------------------- wandering
S.append(shot("s29",66.12,
 meaning="Shiva wandered the whole universe, but nothing set him free.",
 why="Shiva walks alone through the starry cosmos with the head fixed to his hand; on 'nothing' his face falls in grief.",
 camera={"shot":"wide","lens":"wide","move":"dolly_left","from":{"z":1.0,"x":10,"y":0,"r":0},"to":{"z":1.0,"x":-10,"y":0,"r":0},"shake":0,"motivation":"travelling with his endless wandering"},
 focus={"subject":"kapali","depth":"deep"},vertical={"focus":"kapali"},
 layers=cosmos_layers(('#cfe0ff','#d8d0ff')),
 background={"k":"cosmos","rgb":"170,190,255","spin":0.05},
 mood={"emotion":"loneliness","grade":"cool"},
 characters=[{"who":"kapali","x":620,"y":680,"s":0.95,"_face":0.44,"flip":1,"pose":"stand","prop":"head","emo":"sad","mood":{"sad":0.6,"ly":0.35},"walk":{"word":"wandered","to_x":680,"d":2.2,"speed":0.8},
   "actions":[{"word":"nothing","emo":"grief","d":0.6}]}],
 effects=[],transition_in="wipe"))
# 30
S.append(shot("s30",69.32,
 meaning="Over time the head's flesh wasted away until only a skull was left.",
 why="Closer on Shiva and his hand: on 'away' the head softly dissolves in pale light and an ivory skull is left in its place.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.04,"x":0,"y":0,"r":0},"to":{"z":1.1,"x":0,"y":-4,"r":0},"shake":0,"motivation":"push in on the slow change"},
 focus={"subject":"kapali","depth":"shallow"},vertical={"focus":"kapali","z":1.2,"y":0.4},
 layers=cosmos_layers(('#cfe0ff','#d8d0ff')),
 background={"k":"cosmos","rgb":"190,180,240","spin":0.04},
 mood={"emotion":"decay","grade":"cool"},
 characters=[{"who":"kapali","x":640,"y":680,"s":1.05,"_face":0.4,"flip":1,"pose":"stand","prop":"head","emo":"sad","mood":{"ly":0.6},"look":800,"engine_cues":{"fo":"away"},"engine":{"fd":0.8}},
  {"who":"kapali","x":640,"y":680,"s":1.05,"_ground":True,"flip":1,"pose":"stand","prop":"skull","emo":"sad","mood":{"ly":0.6,"lx":0.6},"engine_cues":{"ac":"away"},"engine":{"ad":0.8},
   "actions":[{"word":"skull","emo":"grief","mood":{"ly":0.7,"lx":0.6},"d":0.6}]}],
 effects=[{"k":"glow","word":"away","x":555,"y":520,"r":150,"rgb":"240,235,255","ga":0.55,"par":1.0,"behind":True,"meaning":"soft light hiding the change from head to skull"}],
 transition_in="cut"))
# 31
S.append(shot("s31",72.5,
 meaning="Carrying the skull, Shiva was called Kapali, the skull-bearer.",
 why="Shiva stands full figure with the skull in his left hand inside a pale halo ring; the name Kapali appears above as it is spoken.",
 camera={"shot":"medium","lens":"normal","move":"tilt_up","from":{"z":1.05,"x":0,"y":16,"r":0},"to":{"z":1.05,"x":0,"y":0,"r":0},"shake":0,"motivation":"tilt up as he is given his name"},
 focus={"subject":"kapali","depth":"deep"},vertical={"focus":"kapali"},
 layers=cosmos_layers(('#d8e0ff','#e8e0ff')),
 background={"k":"cosmos","rgb":"200,190,255","spin":0.04},
 mood={"emotion":"solemn","grade":"cool"},
 characters=[{"who":"kapali","x":640,"y":670,"s":1.05,"_face":0.43,"flip":1,"pose":"stand","prop":"skull","emo":"sad","look":640,
   "actions":[{"word":"Kapali","emo":"calm","d":0.6}]}],
 effects=[{"k":"halo_ring","word":"called","x":640,"y":330,"w":460,"alpha":0.45,"blend":"lighter","par":0.9,"behind":True,"meaning":"the solemn name he now bears"},
  {"k":"name","word":"Kapali","s":"Kapali","x":640,"y":90,"size":30,"d":0.25,"meaning":"the name Kapali on screen when it is spoken"}],
 transition_in="cut"))
# 32 ------------------------------------------------------------------- Kashi
S.append(shot("s32",74.08,
 meaning="Then Shiva came to a certain place on Earth.",
 why="A wipe to a bright river bank at sunrise with sandstone buildings and a temple tower: Shiva walks in from the left with the skull and looks up on 'Earth'.",
 camera={"shot":"wide","lens":"wide","move":"crane_down","from":{"z":1.0,"x":0,"y":-20,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"descending from the sky to the place on Earth"},
 focus={"subject":"kapali","depth":"deep"},vertical={"focus":"kapali"},
 layers=[far_ghats((460,820)),mid_ghat((420,860)),near_marigold((460,830))],
 background=bg_kashi(700,280),
 mood={"emotion":"arrival","grade":"warm"},
 characters=[{"who":"kapali","x":580,"y":680,"s":0.95,"_face":0.45,"flip":1,"pose":"stand","prop":"skull","emo":"sad","mood":{"sad":0.6,"ly":0.35},"walk":{"word":"reached","to_x":640,"d":1.2,"speed":0.8},
   "actions":[{"word":"Earth","emo":"surprise","mood":{"ly":-0.3},"d":0.6}]}],
 effects=[{"k":"palace_gate","x":700,"y":300,"w":200,"alpha":0.75,"par":0.3,"behind":True,"meaning":"the temple of the sacred place he has reached"}],
 transition_in="wipe"))
# 33
S.append(shot("s33",75.88,
 meaning="And there the skull finally fell from his hand.",
 why="On 'fell' a ring of gold light bursts from Shiva's left hand, the skull is gone from it and lies on the ground at his feet; his face lifts in relief.",
 camera={"shot":"medium","lens":"normal","move":"push_in","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.06,"x":0,"y":-4,"r":0},"shake":0,"motivation":"push in on the moment of release"},
 focus={"subject":"kapali","depth":"deep"},vertical={"focus":"kapali","z":1.1,"y":0.42},
 layers=[far_ghats((470,820)),mid_ghat((430,860)),near_marigold((470,830))],
 background=bg_kashi(640,280),
 mood={"emotion":"release","grade":"warm"},
 characters=[{"who":"kapali","x":640,"y":680,"s":1.0,"_face":0.42,"flip":1,"pose":"stand","prop":"skull","emo":"sad","mood":{"ly":0.5},"look":800,"engine_cues":{"fo":"fell"},"engine":{"fd":0.4}},
  {"who":"kapali","x":640,"y":680,"s":1.0,"_ground":True,"flip":1,"pose":"stand","prop":"none","emo":"surprise","engine_cues":{"ac":"fell"},"engine":{"ad":0.4},
   "actions":[{"word":"hand","emo":"joy","mood":{"smile":0.6},"d":0.6}]}],
 effects=[{"k":"halo_ring","word":"fell","x":560,"y":520,"w":220,"alpha":0.6,"blend":"lighter","par":1.0,"behind":True,"meaning":"the light of release as the skull leaves his hand"},
  {"k":"skull","word":"fell","x":585,"y":668,"w":56,"rot":-0.3,"glow":0.35,"meaning":"the skull lying where it fell"}],
 transition_in="cut"))
# 34
S.append(shot("s34",78.0,
 meaning="Anyone who comes to that place is freed of every sin.",
 why="Pilgrims on the river ghats at sunrise fold their hands as gold motes rise from them on 'freed', their faces lifting in joy.",
 camera={"shot":"two_shot","lens":"normal","move":"pan_right","from":{"z":1.0,"x":0,"y":0,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"the pan moves along the pilgrims on the ghat"},
 focus={"subject":"villager_w","depth":"deep"},vertical={"x":[600,700]},
 layers=[far_ghats((480,840)),mid_ghat((420,880)),near_marigold((460,860))],
 background=bg_kashi(660,280),
 mood={"emotion":"release","grade":"warm"},
 characters=[{"who":"villager_w","x":580,"y":680,"s":0.95,"_face":0.45,"flip":1,"pose":"namaste","emo":"devotion","look":"villager",
   "actions":[{"word":"freed","emo":"joy","mood":{"smile":0.8},"d":0.6}]},
  {"who":"villager","x":730,"y":680,"s":0.95,"_ground":True,"flip":-1,"pose":"stand","emo":"calm","look":"villager_w",
   "actions":[{"word":"came","pose":"namaste","emo":"devotion","d":0.6},{"word":"sin","emo":"joy","mood":{"blink":1,"smile":0.6},"d":0.6}]}],
 effects=[{"k":"embers","word":"freed","x":650,"y":520,"w":380,"alpha":0.55,"blend":"lighter","par":1.0,"rgb":"255,230,160","meaning":"sins lifting off the pilgrims as gold motes"},
  {"k":"divine_rays","x":660,"y":100,"w":620,"alpha":0.3,"blend":"lighter","par":0.2,"behind":True,"meaning":"the sacred morning light of the place"}],
 transition_in="fade"))
# 35
S.append(shot("s35",81.12,
 meaning="That place became the holy city of Kashi, also called Varanasi.",
 why="Shiva, freed, stands calm and smiling on the ghat before the temple tower and the river at sunrise; the name Kashi appears as it is spoken.",
 camera={"shot":"wide","lens":"wide","move":"crane_up","from":{"z":1.06,"x":0,"y":10,"r":0},"to":{"z":1.0,"x":0,"y":-6,"r":0},"shake":0,"motivation":"crane up to the whole holy city"},
 focus={"subject":"kapali","depth":"deep"},vertical={"focus":"kapali"},
 layers=[far_ghats((460,830)),mid_ghat((420,870)),near_marigold((460,830))],
 background=bg_kashi(640,260),
 mood={"emotion":"sanctity","grade":"warm"},
 characters=[{"who":"kapali","x":640,"y":690,"s":0.9,"_face":0.47,"flip":1,"pose":"stand","prop":"none","emo":"calm","mood":{"smile":0.5},"look":640,
   "actions":[{"word":"Kashi","pose":"open","emo":"joy","d":0.6}]}],
 effects=[{"k":"palace_gate","x":640,"y":250,"w":230,"alpha":0.8,"par":0.3,"behind":True,"meaning":"the temple of Kashi rising behind Shiva"},
  {"k":"divine_rays","x":640,"y":80,"w":640,"alpha":0.35,"blend":"lighter","par":0.2,"behind":True,"meaning":"sunrise over the holy city"},
  {"k":"name","word":"Kashi","s":"Kashi · Varanasi","x":640,"y":120,"size":30,"d":0.25,"meaning":"the city's two names on screen as they are spoken"}],
 transition_in="fade"))
# 36
S.append(shot("s36",84.34,
 meaning="That is why people still travel to Kashi today.",
 why="Back to the pilgrims of the opening: they walk on along the ghat toward the temple in the morning light, hands joined, the question answered.",
 camera={"shot":"wide","lens":"wide","move":"pull_out","from":{"z":1.08,"x":0,"y":-4,"r":0},"to":{"z":1.0,"x":0,"y":0,"r":0},"shake":0,"motivation":"final pull out to close the story"},
 focus={"subject":"villager_w","depth":"deep"},vertical={"x":[640,670]},
 layers=[far_ghats((470,840)),mid_ghat((420,880)),near_marigold((460,860))],
 background=bg_kashi(660,260),
 mood={"emotion":"resolution","grade":"warm"},
 characters=[{"who":"villager_w","x":610,"y":690,"s":0.95,"_face":0.46,"flip":1,"pose":"namaste","emo":"joy","look":900,"walk":{"word":"people","to_x":640,"d":1.4,"speed":0.8},
   "actions":[{"word":"go","emo":"devotion","mood":{"smile":0.6},"d":0.6}]},
  {"who":"villager","x":720,"y":690,"s":0.95,"_ground":True,"flip":1,"pose":"namaste","emo":"joy","look":900,"walk":{"word":"people","to_x":750,"d":1.4,"speed":0.8},
   "actions":[{"word":"still","emo":"devotion","d":0.6}]}],
 effects=[{"k":"palace_gate","x":660,"y":290,"w":210,"alpha":0.75,"par":0.3,"behind":True,"meaning":"the temple the pilgrims still go to"},
  {"k":"divine_rays","x":660,"y":100,"w":620,"alpha":0.3,"blend":"lighter","par":0.2,"behind":True,"meaning":"morning light over Kashi"}],
 transition_in="fade"))
# ---------------------------------------------------------------- durations + narration from the word list
for i,s in enumerate(S):
    end=S[i+1]['start']['t'] if i+1<len(S) else END
    s['duration']=round(end-s['start']['t'],2)
    i0=idx(s['start']['t']);i1=idx(S[i+1]['start']['t']) if i+1<len(S) else len(T);s['narration']=span(i0,i1)
# ---------------------------------------------------------------- face placement (38-50% of the frame height at the still time)
ANIMAL={'cow':300,'mare':440,'doe':344,'duck':150}
def ease(k):return k*k*(3-2*k)
def face_off(f):
    if f['who'] in ANIMAL:return ANIMAL[f['who']]
    return 195 if VB.seated(f) else 300
def face_frac(f,s,u=.55):
    c=s['camera'];A=c['from'];B=c['to'];e=ease(u)
    z=A.get('z',1)+(B.get('z',1)-A.get('z',1))*e;cy=A.get('y',0)+(B.get('y',0)-A.get('y',0))*e
    fc=f['y'] if f.get('head') else f['y']-face_off(f)*f['s']
    sy=360+(fc-360-cy)*z;V=s.get('vertical') or {};vz=min(max(V.get('z',1),1),2.2);h=720/vz
    w0=min(max(sy-V.get('y',.36)*h,0),720-h) if vz>1 else 0
    return (sy-w0)/h
for s in S:
    if (s.get('vertical') or {}).get('mode')=='stack':continue
    g=None
    for f in s['characters']:
        if f.get('head'):continue
        if f.pop('_ground',False) and g is not None:f['y']=g;continue
        if '_face' not in f:continue
        tgt=f.pop('_face')
        for _ in range(400):
            fr=face_frac(f,s)
            if abs(fr-tgt)<.004:break
            f['y']=round(f['y']-(fr-tgt)*300)
        print('  place',s['id'],f['who'],f['y'],round(face_frac(f,s),3))
        if g is None:g=f['y']
for s in S:
    for f in s['characters']:f.pop('_face',None);f.pop('_ground',None)
for s in S:
    cam={'from':s['camera']['from'],'to':s['camera']['to']}
    for f in s['characters']:
        if f['who'] in ANIMAL:continue
        y0=f['y']
        while VB.face_cropped_v(f,cam,s.get('vertical')) and y0-f['y']<80:f['y']-=2
        if f['y']!=y0:print('  fit',s['id'],f['who'],y0,'->',f['y'])
# ---------------------------------------------------------------- brahma5 head sprouting: hd values on spoken words -> cue indices
import brief_to_plan as BP
for s in S:
    for f in s['characters']:
        if '_hd' in f:
            for k,v in f['_hd'].items():
                if isinstance(v,str):f.setdefault('engine_cues',{})['_hd_'+k]=v
    if any('_hd' in f for f in s['characters']):
        cues=BP.convert(copy.deepcopy(s),True)['cues']
        for f in s['characters']:
            if '_hd' in f:
                f['hd']={k:(v if not isinstance(v,str) else {'c':cues.index(VB.norm(v)),'d':0.7}) for k,v in f.pop('_hd').items()}
order=["id","beat","start","duration","narration","meaning","why","camera","focus","vertical","layers","background","mood","characters","effects","transition_in"]
S=[{k:s[k] for k in order if k in s} for s in S]
json.dump({"episode":"reel02","format":"vertical","shots":S},open(f'{R}/reels/reel02/briefs.json','w'),ensure_ascii=False,indent=1)
print(len(S),'shots',[s['duration'] for s in S])
allw=' '.join(s['narration'] for s in S).split();assert allw==[w for w,_ in T],'narration gap'
