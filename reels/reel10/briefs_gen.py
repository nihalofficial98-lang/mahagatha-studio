#!/usr/bin/env python3
"""reels/reel10/briefs.json "A Mother Prayed 100 Years for a Son to Kill Indra" (data; helpers reels/briefs_lib.py)"""
import sys;sys.path.insert(0,'/home/user/mahagatha-studio/reels')
from briefs_lib import *
G=Gen('reel10');A=G.shot
SKY_DAY=['#2466c8','#6ab0ee','#c8ecfa','#fff8e8']
SKY_DUSK=['#2a2a6a','#6a5aa8','#e49a9a','#ffd8a8']
SKY_NITE=['#0a0e38','#2a2a7a','#6a58a8','#c8a8c8']
SKY_STORM=['#1a2a6a','#4a64b8','#a8bce8','#eef0ff']
SKY_DAWN=['#3a4ab0','#8a94dc','#ffbc8c','#ffeac4']
def vista(sky=SKY_DAY,ridge=['#a8c4e4','#8ab4cc','#6aa08a','#4a8064'],**k):
    d=bg("vista",sky=sky,sx=640,sy=300,ridge=ridge,haze="240,244,255",dust=10);d.update(k);return d
def L_hut(h='#e8e0d0',col='#3a7a44',lamp=False):return [far("soft blue-green hills in haze behind the ashram",[mtn(470,470,1.0,'#8aa0b8',260,150),mtn(840,480,.9,'#8aa0b8',240,130),cld(520,220,1.1,'#fff0e0')],h,.55),
    mid("a thatched mud hut with a plinth and trees beside a dusty yard",[ground(480,'#c8a878',1100,12),{"o":"hut","x":820,"y":505,"s":.7,"lamp":lamp},tree(420,520,.62,"round",col)],.15),
    near("dark leaves and flowering shrubs low in the corners",[shrub(450,752,1.5,'#2a4a38','#e0a040'),shrub(830,752,1.4,'#2a4a38')],.45)]
def L_open(h='#e8e0d0',col='#3a7a44'):return [far("soft blue-green hills in haze far behind",[mtn(470,470,1.0,'#8aa0b8',260,150),mtn(840,480,.9,'#8aa0b8',240,130),cld(520,220,1.1,'#fff0e0')],h,.55),
    mid("a dusty ashram yard with trees",[ground(480,'#c8a878',1100,12),tree(420,520,.62,"round",col),tree(880,516,.58,"round",col)],.15),
    near("dark leaves and flowering shrubs low in the corners",[shrub(450,752,1.5,'#2a4a38','#e0a040'),shrub(830,752,1.4,'#2a4a38')],.45)]
def L_storm():return [far("storm clouds and dark peaks far behind",[mtn(470,470,1.0,'#5a64a8',260,160),mtn(840,480,.9,'#5a64a8',240,140),cld(520,210,1.3,'#b4bce0')],'#c4cce8',.5),
    mid("a bank of grey-blue clouds underfoot",[cld(480,640,1.6,'#c8d0f0'),cld(810,650,1.5,'#b8c0e8')],.2),
    near("storm cloud puffs in the bottom corners",[cld(450,750,1.7,'#8890c8'),cld(830,752,1.6,'#8890c8')],.3)]
def L_womb():return [far("deep red glow haze behind the womb",[mtn(470,470,1.0,'#6a2a3a',260,150),cld(520,220,1.1,'#a85a5a')],'#8a3a3a',.5),
    mid("a dark red cloud bank below the womb",[cld(480,660,1.6,'#7a2a30'),cld(810,670,1.5,'#6a2428')],.2),
    near("dark red mist puffs in the bottom corners",[cld(450,752,1.7,'#3a1218'),cld(830,754,1.6,'#3a1218')],.4)]
def womb(n=1,cry=0,flash=0,spread=1,w=400,y=440,word="womb",meaning="the womb seen from inside"):
    return pfx("womb_view",word,640,y,w,meaning,n=n,cry=cry,flash=flash,spread=spread)
def tiny_indra(word,pose="sneak",emo="fear"):
    return {"who":"indra","x":640,"y":520,"s":.3,"_fixed":True,"flip":1,"pose":pose,"emo":emo,"look":640,"actions":[{"word":word,"emo":emo,"d":.4}]}
def wbg():return bg("voidR")
GLD="255,214,140"
# 1
A("A mother prayed",meaning="A mother prayed for a hundred years for a son who would kill the king of the gods.",
 why="Diti sits in prayer in front of her hut with closed eyes, her hands folded and a faint gold glow around her; the title card sits above her.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-6),"medium","normal",0,"a slow push in on the long prayer"),
 focus={"subject":"diti","depth":"deep"},vertical={"focus":"diti"},layers=L_open(),background=vista(SKY_DAWN),mood={"emotion":"devotion","grade":"warm"},
 characters=[{"who":"diti","x":640,"y":690,"s":1.0,"_face":.55,"flip":1,"pose":"sitpray","emo":"devotion","mood":{"blink":1},"look":640,"actions":[{"word":"hundred","emo":"devotion","d":.5}]}],
 effects=[glow("prayed",640,360,250,GLD,.35,"the quiet glow of a long prayer")],transition_in="fade")
# 2
A("With three days left",meaning="With three days left, Indra did a cruel deed.",
 why="Indra creeps forward in a crouch with a tense face, one hand holding the Vajra low, a thatched hut at the right behind him.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"medium","normal",0,"a stalking slide with the intruder"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_hut('#c8b8d8',lamp=False),background=vista(SKY_DUSK),mood={"emotion":"dread","grade":"cool"},
 characters=[{"who":"indra","x":640,"y":690,"s":1.0,"_face":.44,"flip":1,"pose":"sneak","emo":"fear","look":760,"actions":[{"word":"terrible","emo":"anger","d":.5}]}],
 effects=[name("three","3 days left",640,128,30)],transition_in="cut")
# 3
A("and cut the unborn",meaning="Indra cut the unborn child apart.",
 why="The womb glows in the dark red space with the unborn child curled inside, a bright white flash of the Vajra slicing across it.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,-4),"insert","normal",3,"a hard push in on the cut"),
 focus={"subject":"womb","depth":"shallow"},vertical={"x":640},layers=L_womb(),background=wbg(),mood={"emotion":"violence","grade":"warm"},
 characters=[tiny_indra("child","throw","rage")],
 effects=[womb(1,0,1,word="cut",meaning="the unborn child glowing in the womb with the Vajra flash across it")],transition_in="flash")
# 4
A("What he cut",meaning="What he cut could not be killed.",
 why="The womb now holds seven small glowing children, all alive and crying, spread around the sac.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"insert","normal",0,"pulling back reveals the pieces are alive"),
 focus={"subject":"womb","depth":"shallow"},vertical={"x":640},layers=L_womb(),background=wbg(),mood={"emotion":"shock","grade":"warm"},
 characters=[tiny_indra("killed","throw","surprise")],
 effects=[womb(7,1,0,word="killed",meaning="seven small glowing children crying inside the womb")],transition_in="cut")
# 5
A("So how did Indra",meaning="The question: so how did Indra survive?",
 why="Indra stands under storm clouds with a puzzled worried look, his crown glowing and the Vajra lowered, glancing sideways.",
 camera=cam("tilt_up",(1.0,0,10),(1.06,0,0),"medium","normal",0,"tilting up to the king who must answer"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_storm(),background=vista(SKY_STORM,['#5a64a8','#4a5498','#3a4488','#2a3478']),mood={"emotion":"question","grade":"cool"},
 characters=[{"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"doubt","look":560,"mood":{"lx":-.7},"actions":[{"word":"survive?","emo":"surprise","d":.5}]}],
 effects=[],transition_in="cut")
# 6
A("The mother was Diti",meaning="The mother was called Diti.",
 why="Diti stands calm in a maroon sari in her ashram yard, hands folded, and her name appears on 'Diti'.",
 camera=cam("static",(1.04,0,0),(1.04,0,0),"medium","normal",0,"the camera rests on the introduction"),
 focus={"subject":"diti","depth":"deep"},vertical={"focus":"diti"},layers=L_open(),background=vista(SKY_DAY),mood={"emotion":"calm","grade":"warm"},
 characters=[{"who":"diti","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"calm","look":700,"actions":[{"word":"Diti.","emo":"devotion","d":.5}]}],
 effects=[name("Diti.","Diti",640,128,32)],transition_in="cut")
# 7
A("Vishnu had killed",meaning="Vishnu had killed her sons Hiranyaksha and Hiranyakashipu.",
 why="Diti stands grieving at the left with a sad face while her two dead sons, the asuras Hiranyaksha and Hiranyakashipu, stand pale and faint like memories at the right.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"two_shot","normal",0,"a slow drift from the mother to the sons she lost"),
 focus={"subject":"diti","depth":"deep"},vertical={"x":640},layers=L_open('#d8c8d8'),background=vista(SKY_DUSK),mood={"emotion":"loss","grade":"cool"},
 characters=[{"who":"hiranyakashipu","x":780,"y":660,"s":.62,"_fixed":True,"flip":-1,"pose":"stand","emo":"anger","look":560,"engine":{"a":.55},"actions":[{"word":"Hiranyakashipu.","emo":"anger","d":.4}]},
   {"who":"hiranyaksha","x":700,"y":680,"s":.7,"_fixed":True,"flip":-1,"pose":"stand","emo":"anger","look":560,"engine":{"a":.65},"actions":[{"word":"Hiranyaksha","emo":"anger","d":.4}]},
   {"who":"diti","x":545,"y":690,"s":.85,"_face":.44,"flip":1,"pose":"stand","emo":"grief","look":720,"actions":[{"word":"killed","emo":"grief","d":.5}]}],
 effects=[pfx("mist_wisps","sons",700,470,420,"mist around the memory of her sons",alpha=.45,par=.8)],transition_in="cut")
# 8
A("She asked her husband",meaning="She asked her husband, the sage Kashyapa, for a son who would kill Indra.",
 why="Diti bows with pleading hands before the white-bearded sage Kashyapa who listens with a grave calm face and his kamandalu.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"two_shot","normal",0,"push in on the request"),
 focus={"subject":"diti","depth":"deep"},vertical={"x":640},layers=L_open(),background=vista(SKY_DAY),mood={"emotion":"request","grade":"warm"},
 characters=[{"who":"diti","x":545,"y":690,"s":.82,"_face":.44,"flip":1,"pose":"plead","emo":"devotion","look":720,"talk":.7,"actions":[{"word":"son","emo":"anger","d":.5}]},
   {"who":"kashyapa","x":735,"y":690,"s":.82,"_face":.44,"flip":-1,"pose":"stand","emo":"calm","look":560,"actions":[{"word":"Kashyapa,","emo":"calm","d":.5}]}],
 effects=[name("Kashyapa,","Kashyapa",735,128,30)],transition_in="cut")
# 9
A("Kashyapa gave strict",meaning="Kashyapa gave her strict rules.",
 why="Kashyapa raises one finger in a stern warning with a grave face, his white beard and kamandalu clear in the yard.",
 camera=cam("tilt_up",(1.0,0,10),(1.06,0,0),"medium","normal",0,"rising with the warning finger"),
 focus={"subject":"kashyapa","depth":"deep"},vertical={"focus":"kashyapa"},layers=L_open(),background=vista(SKY_DAY),mood={"emotion":"strictness","grade":"warm"},
 characters=[{"who":"kashyapa","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"point","emo":"calm","look":700,"talk":.8,"actions":[{"word":"rules:","emo":"calm","d":.5}]}],
 effects=[],transition_in="cut")
# 10
A("live a pure life",meaning="Live a pure life for a hundred years.",
 why="Diti sits in calm prayer with closed eyes under a hundred small lights and the words '100 years' above her.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"a slow push in on the vow"),
 focus={"subject":"diti","depth":"deep"},vertical={"focus":"diti"},layers=L_open('#f0e8d8'),background=vista(SKY_DAWN),mood={"emotion":"vow","grade":"warm"},
 characters=[{"who":"diti","x":640,"y":690,"s":1.0,"_face":.46,"flip":1,"pose":"sitpray","emo":"devotion","mood":{"blink":1},"look":640,"actions":[{"word":"hundred","emo":"calm","d":.5}]}],
 effects=[name("hundred","100 years",640,128,32),pfx("magic_circle","pure",640,420,380,"a faint yantra of the pure vow",alpha=.35,blend="lighter",behind=True)],transition_in="cut")
# 11
A("never lie down",meaning="She must never lie down without washing her feet.",
 why="Diti stands at a water pot and pours water over her feet with a careful face; clear water splashes at her feet on 'washing'.",
 camera=cam("tilt_down",(1.0,0,-8),(1.04,0,6),"medium","normal",0,"tilting down to the feet that must be washed"),
 focus={"subject":"diti","depth":"deep"},vertical={"focus":"diti"},layers=L_open(),background=vista(SKY_DAY),mood={"emotion":"discipline","grade":"warm"},
 characters=[{"who":"diti","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"bow","emo":"calm","look":640,"actions":[{"word":"washing","pose":"stand","emo":"calm","d":.5}]}],
 effects=[pfx("water_splash","washing",640,690,200,"water splashing around her feet",alpha=.8)],transition_in="cut")
# 12
A("If she failed",meaning="If she failed, her son would be Indra's friend.",
 why="Kashyapa lifts a hand in warning at the left while Indra stands at the right with a friendly smile and the Vajra lowered, showing the friend the son would become.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"two_shot","normal",0,"sliding from the rule to the friend it would make"),
 focus={"subject":"kashyapa","depth":"deep"},vertical={"x":640},layers=L_open(),background=vista(SKY_DAY),mood={"emotion":"warning","grade":"warm"},
 characters=[{"who":"kashyapa","x":545,"y":690,"s":.82,"_face":.44,"flip":1,"pose":"point","emo":"calm","look":720,"actions":[{"word":"failed,","emo":"calm","d":.5}]},
   {"who":"indra","x":735,"y":690,"s":.82,"_face":.44,"flip":-1,"pose":"stand","emo":"joy","look":560,"mood":{"smile":.6},"actions":[{"word":"friend.","emo":"joy","d":.5}]}],
 effects=[],transition_in="cut")
# 13
A("Indra hid near",meaning="Indra hid near her hut, waiting for one mistake.",
 why="Indra peeks out from behind the thatched hut at the right with a sly watchful face, one hand on the wall, under a dusk sky.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"medium","normal",0,"a slow creeping slide along the hut wall"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_hut('#c8b8d8'),background=vista(SKY_DUSK),mood={"emotion":"stealth","grade":"cool"},
 characters=[{"who":"indra","x":720,"y":690,"s":1.0,"_face":.44,"flip":-1,"pose":"sneak","emo":"anger","look":520,"mood":{"lx":-.7},"actions":[{"word":"mistake.","emo":"anger","d":.5}]}],
 effects=[],transition_in="cut")
# 14
A("There was none",meaning="There was no mistake, nothing to use.",
 why="Diti sits perfectly still in prayer with serene closed eyes and a steady golden glow, no flaw anywhere.",
 camera=cam("static",(1.04,0,0),(1.04,0,0),"medium","normal",0,"the camera is as still as her vow"),
 focus={"subject":"diti","depth":"deep"},vertical={"focus":"diti"},layers=L_hut('#f0e8d8'),background=vista(SKY_DAWN),mood={"emotion":"purity","grade":"warm"},
 characters=[{"who":"diti","x":640,"y":690,"s":1.0,"_face":.46,"flip":1,"pose":"sitpray","emo":"devotion","mood":{"blink":1},"look":640,"actions":[{"word":"none.","emo":"calm","d":.5}]}],
 effects=[glow("none.",640,360,260,GLD,.4,"a steady golden glow of her purity")],transition_in="cut")
# 15
A("Her prayers kept",meaning="Her prayers kept her womb safe like a fort.",
 why="Diti sits in prayer inside a ring of golden light and a glowing yantra that shields her like fort walls.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"medium","normal",0,"pulling back shows the circle of protection"),
 focus={"subject":"diti","depth":"deep"},vertical={"focus":"diti_p"},layers=L_open('#f0e8d8'),background=vista(SKY_DAWN),mood={"emotion":"protection","grade":"warm"},
 characters=[{"who":"diti_p","x":640,"y":690,"s":1.0,"_face":.46,"flip":1,"pose":"sitpray","emo":"devotion","mood":{"blink":1},"look":640,"actions":[{"word":"fort.","emo":"devotion","d":.5}]}],
 effects=[pfx("magic_circle","fort.",640,450,520,"a glowing circle shields her like a fort",alpha=.5,blend="lighter",behind=True),pfx("halo_ring","safe",640,360,360,"a golden ring of her protection",alpha=.5,blend="lighter",behind=True)],transition_in="cut")
# 16
A("Her belly grew",meaning="Her belly grew as the child grew inside.",
 why="Diti, now pregnant with a round belly in her maroon sari, stands in the yard with a hand resting near it and a peaceful face.",
 camera=cam("tilt_down",(1.0,0,-8),(1.04,0,6),"medium","normal",0,"tilting down to the growing belly"),
 focus={"subject":"diti_p","depth":"deep"},vertical={"focus":"diti_p"},layers=L_open(),background=vista(SKY_DAY),mood={"emotion":"growth","grade":"warm"},
 characters=[{"who":"diti_p","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"calm","look":700,"actions":[{"word":"grew.","emo":"devotion","d":.5}]}],
 effects=[],transition_in="cut")
# 17
A("His end came closer",meaning="His end came closer.",
 why="A close bust of Indra with a fearful tense face and eyes darting sideways, the storm sky dark behind his crown.",
 camera=cam("crane_down",(1.04,0,-10),(1.1,0,0),"close","tele",0,"descending on the king's worry"),
 focus={"subject":"indra","depth":"shallow"},vertical={"focus":"indra"},layers=L_storm(),background=vista(SKY_STORM,['#5a64a8','#4a5498','#3a4488','#2a3478']),mood={"emotion":"fear","grade":"cool"},
 characters=[{"who":"indra","x":640,"y":300,"s":.8,"head":True,"flip":1,"pose":"stand","emo":"fear","look":600,"mood":{"lx":-.6},"actions":[{"word":"closer.","emo":"fear","d":.5}]}],
 effects=[pfx("lightning_forks","end",640,240,420,"lightning behind his anxious head",alpha=.5,blend="lighter",behind=True)],transition_in="cut")
# 18
A("Then, three days",meaning="Then, three days before the birth, Diti was so tired.",
 why="Diti sits wearily with drooping eyes and a heavy belly, one hand pressed to her side, in the evening yard.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"push in on her tiredness"),
 focus={"subject":"diti_p","depth":"deep"},vertical={"focus":"diti_p"},layers=L_hut('#c8b8d8'),background=vista(SKY_DUSK),mood={"emotion":"fatigue","grade":"cool"},
 characters=[{"who":"diti_p","x":640,"y":690,"s":1.0,"_face":.46,"flip":1,"pose":"sitpray","emo":"calm","mood":{"blink":.6},"look":640,"actions":[{"word":"tired","emo":"sad","mood":{"blink":.8},"d":.5}]}],
 effects=[name("three","3 days left",640,128,30)],transition_in="cut")
# 19
A("that she fell",meaning="She fell asleep without washing her feet.",
 why="Diti lies asleep on a mat with her eyes closed and her dusty unwashed feet toward the viewer under a night sky.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"wide","normal",0,"pulling back on the sleeper"),
 focus={"subject":"diti_p","depth":"deep"},vertical={"focus":"diti_p"},layers=L_hut('#a898c8',lamp=True),background=vista(SKY_NITE,['#3a3a7a','#2a2a6a','#1a1a58','#12124a']),mood={"emotion":"sleep","grade":"night"},
 characters=[{"who":"diti_p","x":600,"y":690,"s":1.0,"_face":.5,"flip":1,"pose":"stand","emo":"calm","look":640,"actions":[{"word":"asleep","pose":"sleep","emo":"calm","d":.7}]}],
 effects=[],transition_in="cut")
# 20
A("Indra jumped",meaning="Indra jumped toward the sleeping Diti.",
 why="Indra leaps forward with the Vajra in his raised hand and an eager grin, a streak of dust behind him.",
 camera=cam("handheld",(1.04,0,0),(1.08,0,-4),"medium","normal",3,"a jolt as he springs"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_hut('#a898c8',lamp=True),background=vista(SKY_NITE,['#3a3a7a','#2a2a6a','#1a1a58','#12124a']),mood={"emotion":"attack","grade":"night"},
 characters=[{"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"throw","emo":"rage","look":700,"actions":[{"word":"jumped.","emo":"rage","d":.4}]}],
 effects=[pfx("sand_drift","jumped",420,650,360,"dust at his feet as he springs",alpha=.5)],transition_in="cut")
# 21
A("He went into",meaning="He went into her womb.",
 why="The womb glows red-gold with the curled unborn child and tiny Indra with the Vajra inside it.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"insert","normal",0,"a push in through the wall of the womb"),
 focus={"subject":"womb","depth":"shallow"},vertical={"x":640},layers=L_womb(),background=wbg(),mood={"emotion":"intrusion","grade":"warm"},
 characters=[tiny_indra("womb","sneak","fear")],
 effects=[womb(1,0,0,word="womb",meaning="the unborn child curled in the red-gold womb")],transition_in="iris")
# 22
A("His Vajra",meaning="His Vajra, his thunder weapon, flashed.",
 why="A blinding blue-white flash of the Vajra cuts across the womb, the glowing child beneath it.",
 camera=cam("handheld",(1.04,0,0),(1.1,0,-4),"extreme_close","normal",3,"a shake at the thunderclap"),
 focus={"subject":"womb","depth":"shallow"},vertical={"x":640},layers=L_womb(),background=wbg(),mood={"emotion":"strike","grade":"warm"},
 characters=[tiny_indra("flashed.","throw","rage")],
 effects=[womb(1,0,1,word="flashed.",meaning="the Vajra flash across the unborn child")],transition_in="flash")
# 23
A("Seven pieces",meaning="The child was in seven pieces.",
 why="Seven small glowing children float apart in the womb, each one separate.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-4),"insert","normal",0,"push in on the seven pieces"),
 focus={"subject":"womb","depth":"shallow"},vertical={"x":640},layers=L_womb(),background=wbg(),mood={"emotion":"division","grade":"warm"},
 characters=[tiny_indra("pieces.","stand","surprise")],
 effects=[womb(7,0,0,w=470,y=470,spread=1.3,word="pieces.",meaning="seven small glowing pieces drifting apart")],transition_in="cut")
# 24
A("Then he stopped",meaning="Then Indra stopped, shocked at what he saw.",
 why="Indra freezes with wide eyes and the Vajra lowered, mouth open in shock.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"medium","normal",0,"pulling back from the frozen king"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_womb(),background=wbg(),mood={"emotion":"shock","grade":"warm"},
 characters=[{"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"surprise","look":640,"actions":[{"word":"stopped.","emo":"fear","d":.4}]}],
 effects=[glow("stopped.",640,330,240,"255,150,120",.35,"the red glow inside the womb")],transition_in="cut")
# 25
A("The pieces were alive",meaning="The pieces were alive, and they cried.",
 why="Seven small children glow in the womb with open crying mouths, pulsing as they cry.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"insert","normal",0,"push in on the crying pieces"),
 focus={"subject":"womb","depth":"shallow"},vertical={"x":640},layers=L_womb(),background=wbg(),mood={"emotion":"life","grade":"warm"},
 characters=[tiny_indra("cried.","stand","surprise")],
 effects=[womb(7,1,0,word="alive",meaning="seven crying glowing children in the womb")],transition_in="cut")
# 26
A("\"Maruda!\"",meaning="Indra shouted the word Maruda at the children.",
 why="Indra shouts with his mouth wide open and hands pushed forward, and the word 'Maruda' appears big beside him.",
 camera=cam("dolly_right",(1.0,-10,0),(1.04,10,0),"medium","normal",0,"a slide across the shouting face"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_womb(),background=wbg(),mood={"emotion":"command","grade":"warm"},
 characters=[{"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"open","emo":"surprise","look":640,"talk":1,"actions":[{"word":"shouted.","emo":"anger","d":.4}]}],
 effects=[name("Maruda!","Maruda!",640,128,36)],transition_in="cut")
# 27
A("\"Don't cry!\"",meaning="Indra told the crying children not to cry.",
 why="Indra pleads with both hands out and a desperate pleading face, begging the tiny children to stop.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,-4),"medium","normal",0,"push in on the useless plea"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_womb(),background=wbg(),mood={"emotion":"plea","grade":"warm"},
 characters=[{"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"plead","emo":"fear","look":640,"talk":.8,"actions":[{"word":"cry!\"","emo":"sad","d":.4}]}],
 effects=[],transition_in="cut")
# 28
A("They only cried louder",meaning="They only cried louder.",
 why="Seven glowing children scream with wide open mouths in the womb and the sac shakes with their sound.",
 camera=cam("handheld",(1.04,0,0),(1.08,0,-4),"insert","normal",4,"a shake with the louder crying"),
 focus={"subject":"womb","depth":"shallow"},vertical={"x":640},layers=L_womb(),background=wbg(),mood={"emotion":"noise","grade":"warm"},
 characters=[tiny_indra("louder.","stand","fear")],
 effects=[womb(7,1,0,word="louder.",meaning="seven children crying louder in the womb")],transition_in="cut")
# 29
A("He cut each piece",meaning="He cut each piece into seven more.",
 why="The womb fills with forty-nine small glowing children after a white slash of the Vajra.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"close","normal",2,"a push in as the pieces multiply"),
 focus={"subject":"womb","depth":"shallow"},vertical={"x":640},layers=L_womb(),background=wbg(),mood={"emotion":"multiplication","grade":"warm"},
 characters=[tiny_indra("seven","throw","rage")],
 effects=[womb(49,0,.5,word="seven",meaning="forty-nine small glowing children in the womb")],transition_in="flash")
# 30
A("Still alive, still louder",meaning="They were still alive and still louder.",
 why="Forty-nine small children cry with open mouths in the womb, spread wide and glowing.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"insert","normal",3,"pulling back on the noise"),
 focus={"subject":"womb","depth":"shallow"},vertical={"x":640},layers=L_womb(),background=wbg(),mood={"emotion":"noise","grade":"warm"},
 characters=[tiny_indra("louder","flee","fear")],
 effects=[womb(49,1,0,w=480,y=450,spread=1.3,word="louder",meaning="forty-nine crying children glowing in the womb")],transition_in="cut")
# 31
A("Diti woke up",meaning="Diti woke up from her sleep on the mat.",
 why="Diti sits up from her mat in surprise with wide eyes and a hand on her belly.",
 camera=cam("tilt_up",(1.0,0,8),(1.06,0,-2),"medium","normal",0,"rising with her as she wakes"),
 focus={"subject":"diti_p","depth":"deep"},vertical={"focus":"diti_p"},layers=L_hut('#a898c8',lamp=True),background=vista(SKY_NITE,['#3a3a7a','#2a2a6a','#1a1a58','#12124a']),mood={"emotion":"waking","grade":"night"},
 characters=[{"who":"diti_p","x":640,"y":690,"s":1.0,"_face":.46,"flip":1,"pose":"sleep","emo":"calm","look":640,"actions":[{"word":"woke","pose":"sitpray","emo":"surprise","d":.5}]}],
 effects=[],transition_in="cut")
# 32
A("Indra ran away",meaning="Indra ran away from the hut and from Diti.",
 why="Indra runs away across the dark yard with his Vajra and a scared face, glancing back over his shoulder.",
 camera=cam("pan_right",(1.0,-14,0),(1.0,14,0),"wide","normal",2,"a hard pan with the fleeing king"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_hut('#a898c8',lamp=True),background=vista(SKY_NITE,['#3a3a7a','#2a2a6a','#1a1a58','#12124a']),mood={"emotion":"flight","grade":"night"},
 characters=[{"who":"indra","x":600,"y":690,"s":1.0,"_face":.44,"flip":1,"pose":"flee","emo":"fear","look":700,"walkTo":{"x":690,"c":"ran","d":1.2,"sp":1.2},"actions":[{"word":"away.","emo":"fear","d":.4}]}],
 effects=[pfx("sand_drift","ran",420,650,420,"dust of his flight",alpha=.5)],transition_in="cut")
# 33
A("She gave birth",meaning="She gave birth to forty-nine children.",
 why="Forty-nine tiny storm-god babies with blue halos sit in a grid of seven rows, crying, as dawn light rises behind them; Diti sits smiling above.",
 camera=cam("crane_up",(1.0,0,6),(1.04,0,-6),"wide","normal",0,"rising over the new crowd of children"),
 focus={"subject":"maruta_baby","depth":"deep"},vertical={"x":640},layers=L_open('#f0e8d8'),background=vista(SKY_DAWN),mood={"emotion":"birth","grade":"warm"},
 characters=[{"who":"maruta_baby","x":640,"y":580,"s":.5,"_fixed":True,"flip":1,"pose":"stand","emo":"grief","look":640,"actions":[{"word":"children.","emo":"joy","d":.4}]}],
 effects=[pfx("maruta_pieces","birth",640,560,430,"forty-nine crying storm-god babies in a grid",n=49,spread=1,cry=1,born=1),name("49","49",640,128,34)],transition_in="cut")
# 34
A("They did not kill",meaning="They did not kill Indra.",
 why="Indra stands calm and unharmed under a clear sky with a few small storm-god babies in front of him not attacking.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-4),"medium","normal",0,"push in on the king who is safe"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_open('#e8f0f8'),background=vista(SKY_DAY),mood={"emotion":"safety","grade":"warm"},
 characters=[{"who":"maruta_baby","x":560,"y":580,"s":.5,"_fixed":True,"flip":1,"pose":"stand","emo":"calm","look":640,"actions":[{"word":"kill","emo":"calm","d":.4}]},
   {"who":"maruta_baby","x":720,"y":580,"s":.5,"_fixed":True,"flip":-1,"pose":"stand","emo":"calm","look":640,"actions":[{"word":"kill","emo":"calm","d":.4}]},
   {"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"surprise","look":700,"actions":[{"word":"Indra.","emo":"calm","d":.5}]}],
 effects=[],transition_in="cut")
# 35
A("They became his friends",meaning="They became his friends, as Kashyapa had said.",
 why="Indra smiles with a baby storm god on each side and Kashyapa nodding behind them; light halos glow warm around all.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"medium","normal",0,"a slow friendly slide along the group"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_open('#e8f0f8'),background=vista(SKY_DAY),mood={"emotion":"friendship","grade":"warm"},
 characters=[{"who":"maruta_baby","x":555,"y":595,"s":.55,"_fixed":True,"flip":1,"pose":"stand","emo":"joy","look":640,"actions":[{"word":"friends,","emo":"joy","d":.4}]},
   {"who":"maruta_baby","x":725,"y":595,"s":.55,"_fixed":True,"flip":-1,"pose":"stand","emo":"joy","look":640,"actions":[{"word":"friends,","emo":"joy","d":.4}]},
   {"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"open","emo":"joy","look":700,"mood":{"smile":.7},"actions":[{"word":"Kashyapa","emo":"joy","d":.5}]}],
 effects=[glow("friends,",640,320,300,GLD,.4,"warm friendly light")],transition_in="cut")
# 36
A("Because Indra shouted",meaning="Because Indra shouted Maruda, the children were named after the word.",
 why="Indra shouts with his mouth open and a hand raised, the word 'Maruda' glowing next to him as in the womb.",
 camera=cam("tilt_up",(1.0,0,10),(1.06,0,0),"medium","normal",0,"rising to the shout that named them"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_storm(),background=vista(SKY_STORM,['#5a64a8','#4a5498','#3a4488','#2a3478']),mood={"emotion":"naming","grade":"cool"},
 characters=[{"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"raise","emo":"surprise","look":700,"talk":1,"actions":[{"word":"Maruda,\"","emo":"anger","d":.4}]}],
 effects=[name("Maruda,\"","Maruda",640,128,36)],transition_in="cut")
# 37
A("they were called",meaning="They were called the Marutas, the storm gods.",
 why="Three grown storm gods with fan crowns and storm halos stand side by side in wind and clouds, calm and strong; the name 'Marutas' appears above them.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-4),"medium","normal",0,"push in on the storm gods"),
 focus={"subject":"maruta","depth":"deep"},vertical={"x":640},layers=L_storm(),background=vista(SKY_STORM,['#5a64a8','#4a5498','#3a4488','#2a3478']),mood={"emotion":"majesty","grade":"cool"},
 characters=[{"who":"maruta","x":510,"y":616,"s":.62,"_fixed":True,"flip":1,"pose":"stand","emo":"calm","look":640,"actions":[{"word":"Marutas,","emo":"joy","d":.4}]},
   {"who":"maruta","x":770,"y":616,"s":.62,"_fixed":True,"flip":-1,"pose":"stand","emo":"calm","look":640,"actions":[{"word":"Marutas,","emo":"joy","d":.4}]},
   {"who":"maruta","x":640,"y":690,"s":.74,"_face":.43,"flip":1,"pose":"namaste","emo":"joy","look":700,"actions":[{"word":"storm","emo":"calm","d":.5}]}],
 effects=[name("Marutas,","Marutas",640,128,34),pfx("lightning_forks","storm",640,240,460,"lightning behind the storm gods",alpha=.5,blend="lighter",behind=True)],transition_in="cut")
# 38
A("That is how Indra",meaning="That is how Indra survived.",
 why="Indra stands relieved with a calm smile, one hand open and his crown glowing in clear light.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"medium","normal",0,"pulling back on the survivor"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_open('#e8f0f8'),background=vista(SKY_DAWN),mood={"emotion":"relief","grade":"warm"},
 characters=[{"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"open","emo":"calm","look":700,"mood":{"smile":.5},"actions":[{"word":"survived.","emo":"joy","d":.5}]}],
 effects=[glow("survived.",640,320,260,GLD,.4,"warm light of relief")],transition_in="cut")
# 39
A("Diti's son could",meaning="Diti's son could not be killed, only made into many, and all 49 stood beside him.",
 why="Indra stands in the middle with a row of Marutas on each side, storm-god brothers in blue with halos, all standing beside him; the number 49 appears.",
 camera=cam("crane_up",(1.0,0,8),(1.04,0,-6),"wide","normal",0,"rising over the whole host standing together"),
 focus={"subject":"indra","depth":"deep"},vertical={"x":640},layers=L_storm(),background=vista(SKY_STORM,['#5a64a8','#4a5498','#3a4488','#2a3478']),mood={"emotion":"unity","grade":"warm"},
 characters=[{"who":"maruta","x":470,"y":580,"s":.5,"_fixed":True,"flip":1,"pose":"stand","emo":"joy","look":640,"actions":[{"word":"stood","emo":"joy","d":.4}]},
   {"who":"maruta","x":560,"y":610,"s":.6,"_fixed":True,"flip":1,"pose":"stand","emo":"joy","look":640,"actions":[{"word":"stood","emo":"joy","d":.4}]},
   {"who":"maruta","x":810,"y":580,"s":.5,"_fixed":True,"flip":-1,"pose":"stand","emo":"joy","look":640,"actions":[{"word":"stood","emo":"joy","d":.4}]},
   {"who":"maruta","x":720,"y":610,"s":.6,"_fixed":True,"flip":-1,"pose":"stand","emo":"joy","look":640,"actions":[{"word":"stood","emo":"joy","d":.4}]},
   {"who":"indra","x":640,"y":700,"s":.8,"_face":.43,"flip":1,"pose":"open","emo":"joy","look":700,"actions":[{"word":"beside","emo":"joy","d":.5}]}],
 effects=[name("49","49",640,128,34),pfx("divine_rays","stood",640,330,520,"rays of unity behind the host",alpha=.4,blend="lighter",behind=True)],transition_in="cut")
G.finish()
