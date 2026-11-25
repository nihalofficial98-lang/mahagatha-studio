#!/usr/bin/env python3
"""reels/reel15/briefs.json "How Did Garuda Become Vishnu's Vahana?" (written as data, see reels/briefs_lib.py)"""
import sys;sys.path.insert(0,'/home/user/mahagatha-studio/reels')
from briefs_lib import *
G=Gen('reel15');A=G.shot
# ---- palettes / scenes
SKY_VK=['#2a5cc4','#7ab0ee','#ffdca8','#fff6e2']
SKY_DIV=['#1d4fae','#5aa0e8','#c4e4fa','#fff6dc']
SKY_FIRE=['#3a1a3c','#a8403a','#ff9a4a','#ffd88a']     # the gods' guarded heaven, hot dusk
SKY_NAGA=['#1a3a4a','#3a7a7a','#a8d4a0','#f0f4c8']     # the snake kingdom, teal dusk
SKY_STORM=['#1a2a6a','#4a64b8','#a8bce8','#eef0ff']
SKY_DAWN=['#3a4ab0','#8a94dc','#ffbc8c','#ffeac4']
def vk(sx=640,sy=250):return bg("vaikuntha",sx=sx,sy=sy)
def sky(c=SKY_DIV,sx=640,sy=200):return bg("cloudscape",sky=c,sx=sx,sy=sy)
def vista(sky=SKY_NAGA,ridge=['#6a9a8a','#4a8070','#386a58','#2a5444'],sx=640,sy=300,**k):
    d=bg("vista",sky=sky,sx=sx,sy=sy,ridge=ridge,haze="240,244,255",dust=10);d.update(k);return d
def L_clouds(h='#eef2fa'):return [far("pale peaks and white clouds far behind",[mtn(470,470,1.0,'#9aaad8'),mtn(830,480,.85,'#9aaad8'),cld(520,220,1.3),cld(790,270,1.0)],h),
    mid("a bank of white clouds at the figures' feet",[cld(480,640,1.6),cld(810,650,1.5,'#f4f6ff')]),near("white cloud puffs low in the bottom corners",[cld(450,750,1.7),cld(830,752,1.6)],.1)]
def L_vk():return [far("a golden palace and pale clouds far behind",[cld(500,230,1.2,'#fff4dc'),cld(800,270,1.0,'#fff4dc'),mtn(470,470,.9,'#d8b88a',200,120)],'#fff0d4',.5),
    mid("lotus-dotted golden shore of the milk ocean",[ground(470,'#f2dca8',1100,12),cld(430,640,1.5,'#fff8ec'),cld(850,650,1.4,'#fff8ec')],.15),
    near("golden lotus leaves low in the corners",[shrub(450,752,1.5,'#3a7a54','#ffd0e0'),shrub(830,752,1.4,'#3a7a54','#ffe8b0')],.35)]
def L_fire():return [far("dark red hills and smoke far behind",[mtn(470,470,1.0,'#8a4a5a',260,160),mtn(840,480,.9,'#8a4a5a',240,140),cld(520,220,1.2,'#c07a6a')],'#e8a888',.5),
    mid("scorched rocky ground of the gods' guarded heaven",[ground(480,'#6a3a3a',1100,12),{"o":"rock","x":430,"y":520,"s":.8,"col":"#4a2a2a"},{"o":"rock","x":860,"y":516,"s":.7,"col":"#4a2a2a"}],.15),
    near("dark rocks low in the bottom corners",[{"o":"rock","x":440,"y":752,"s":1.6,"col":"#2a1a1e"},{"o":"rock","x":840,"y":756,"s":1.5,"col":"#2a1a1e"}],.5)]
def L_naga():return [far("teal hills in haze behind the snake lair",[mtn(470,470,1.0,'#6aa0a0',260,150),mtn(840,480,.9,'#6aa0a0',240,130),cld(520,220,1.1,'#d8f0d8')],'#d0ecd4',.55),
    mid("a mossy bank by the snakes' lair with reeds",[ground(480,'#6a9a6a',1100,12),tree(410,520,.6,"palm",'#2e6a44'),tree(870,516,.55,"round",'#2e6a44')],.18),
    near("dark reeds low in the corners",[shrub(450,752,1.5,'#1e4a3a','#c0e0a0'),shrub(830,752,1.4,'#1e4a3a')],.45)]
def L_storm():return [far("storm clouds and dark peaks far behind",[mtn(470,470,1.0,'#5a64a8',260,160),mtn(840,480,.9,'#5a64a8',240,140),cld(520,210,1.3,'#b4bce0')],'#c4cce8',.5),
    mid("a bank of grey-blue clouds underfoot",[cld(480,640,1.6,'#c8d0f0'),cld(810,650,1.5,'#b8c0e8')],.2),
    near("storm cloud puffs in the bottom corners",[cld(450,750,1.7,'#8890c8'),cld(830,752,1.6,'#8890c8')],.3)]
GLD="255,214,140"
# 1
A("Out of every creature",meaning="The question: out of every creature in the universe, why did Vishnu choose Garuda to carry him?",
 why="Vishnu stands calm in his golden Vaikuntha with a gold halo opening behind him as the question is asked; the title card sits above his head.",
 camera=cam("push_in",(1.0,0,0),(1.06,0,-6),"medium","normal",0,"a slow push in to the god who will choose"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},layers=L_vk(),background=vk(),mood={"emotion":"question","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":690,"s":1.0,"_face":.52,"flip":1,"pose":"stand","emo":"calm","look":700,"actions":[{"word":"choose","pose":"open","emo":"calm","d":.6}]}],
 effects=[pfx("halo_ring","choose",640,300,420,"the quiet divinity of Vishnu, a pale halo",alpha=.5,blend="lighter",behind=True)],transition_in="fade")
# 2
A("Not because Garuda",meaning="It was not because Garuda was the strongest.",
 why="Garuda spreads his red-gold wings wide and proud in a bright sky, a gold glow behind him on 'strongest', then his wings close as if the answer lies elsewhere.",
 camera=cam("pull_out",(1.1,0,-6),(1.0,0,0),"medium","normal",0,"pulling back shows his full wingspan, then leaves it behind"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_clouds(),background=sky(),mood={"emotion":"pride","grade":"warm"},
 characters=[{"who":"garuda","x":640,"y":690,"s":.9,"_face":.44,"flip":1,"pose":"spread","emo":"pride","look":700,"actions":[{"word":"strongest","pose":"stand","emo":"calm","d":.7}]}],
 effects=[glow("strongest",640,300,260,GLD,.4,"the glow of a famous strength")],transition_in="cut")
# 3
A("It was because",meaning="It was because of what Garuda did with the amrut, and who he did it for.",
 why="A glowing gold amrut pot floats in a ring of soft light between golden clouds, pulsing on 'amrut'; Garuda looks up at it with devotion.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-8),"insert","normal",0,"push in on the object the whole story turns on"),
 focus={"subject":"garuda","depth":"shallow"},vertical={"x":635},layers=L_clouds('#fff0d4'),background=sky(SKY_VK),mood={"emotion":"wonder","grade":"warm"},
 characters=[{"who":"garuda","x":545,"y":690,"s":.85,"_face":.46,"flip":1,"pose":"stand","emo":"devotion","look":720,"actions":[{"word":"amrut","emo":"surprise","mood":{"lx":.8,"ly":-.2},"d":.6},{"word":"who","emo":"devotion","d":.6}]}],
 effects=[pfx("amrut_pot","amrut",715,430,125,"the amrut pot glows between the sky and Garuda",behind=False),glow("amrut",715,410,170,"255,240,190",.45,"the pale gold light of the amrut")],transition_in="cut")
# 4
A("Garuda, half bird",meaning="Garuda was half bird and half man.",
 why="Garuda stands at full height with folded red-gold wings; on 'bird' he spreads them and a name plate 'Garuda' appears above him.",
 camera=cam("tilt_up",(1.0,0,10),(1.06,0,0),"medium","normal",0,"tilting up the half-bird, half-man figure from talons to crest"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_clouds(),background=sky(SKY_STORM),mood={"emotion":"awe","grade":"warm"},
 characters=[{"who":"garuda","x":640,"y":690,"s":.95,"_face":.43,"flip":1,"pose":"stand","emo":"calm","look":700,"actions":[{"word":"bird","pose":"spread","emo":"pride","d":.6},{"word":"man","pose":"stand","emo":"calm","d":.6}]}],
 effects=[name("Garuda","Garuda",640,128,32)],transition_in="cut")
# 5
A("was the son of Vinata",meaning="Garuda was the son of Vinata.",
 why="Vinata in a faded brown sari stands with a gentle tired smile at the left, Garuda beside her turns to her with warm eyes; her name appears on 'Vinata'.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"two_shot","normal",0,"a drift across the mother and son who stand together"),
 focus={"subject":"vinata","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"tenderness","grade":"warm"},
 characters=[{"who":"vinata","x":545,"y":690,"s":.8,"_face":.44,"flip":1,"pose":"stand","emo":"sad","look":720,"mood":{"smile":.3},"actions":[{"word":"Vinata","emo":"joy","mood":{"smile":.4},"d":.6}]},
   {"who":"garuda","x":735,"y":690,"s":.78,"_face":.44,"flip":-1,"pose":"stand","emo":"devotion","look":560,"actions":[{"word":"son","emo":"devotion","d":.6}]}],
 effects=[name("Vinata","Vinata",660,128,30)],transition_in="cut")
# 6
A("The snakes kept her",meaning="The snakes kept Vinata as a slave.",
 why="Vinata kneels sad and small at the left in the shadow of two big raised cobras, one teal and one black-gold, that sway over her with forked tongues out.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-6),"medium","normal",0,"push in on the woman held under the snakes"),
 focus={"subject":"vinata","depth":"deep"},vertical={"x":640},layers=L_naga(),background=vista(),mood={"emotion":"oppression","grade":"cool"},
 characters=[{"who":"naga","x":700,"y":660,"s":.8,"_fixed":True,"flip":-1,"pose":"stand","emo":"anger","look":560,"actions":[{"word":"slave","pose":"point","emo":"anger","d":.5}]},
   {"who":"naga2","x":790,"y":650,"s":.68,"_fixed":True,"flip":-1,"pose":"stand","emo":"calm","look":560,"actions":[{"word":"kept","emo":"anger","d":.5}]},
   {"who":"vinata","x":555,"y":690,"s":.8,"_face":.46,"flip":1,"pose":"plead","emo":"grief","look":700,"actions":[{"word":"slave","emo":"grief","tilt":-.05,"d":.6}]}],
 effects=[pfx("mist_wisps","slave",640,470,520,"a cold mist of captivity over the snake lair",alpha=.4,par=.8)],transition_in="cut")
# 7
A("They would free her",meaning="The snakes would free her in return for amrut, the drink of immortality.",
 why="A big teal cobra rises at the right with a cunning look toward a glowing amrut pot that appears on 'amrut', while Vinata watches hopefully at the left.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"two_shot","normal",0,"sliding from the captive to the price of her freedom"),
 focus={"subject":"naga","depth":"deep"},vertical={"x":640},layers=L_naga(),background=vista(),mood={"emotion":"bargain","grade":"cool"},
 characters=[{"who":"vinata","x":555,"y":690,"s":.76,"_face":.46,"flip":1,"pose":"plead","emo":"sad","look":700,"actions":[{"word":"free","emo":"joy","mood":{"smile":.3},"d":.6}]},
   {"who":"naga","x":740,"y":670,"s":.85,"_face":.40,"flip":-1,"pose":"stand","emo":"calm","look":560,"actions":[{"word":"amrut","pose":"point","emo":"anger","d":.5}]}],
 effects=[pfx("amrut_pot","amrut",650,440,100,"the amrut pot appears as the price of freedom"),glow("immortality",660,420,200,"255,240,190",.4,"the shine of immortality")],transition_in="cut")
# 8
A("The gods guarded it",meaning="The gods guarded the amrut with a ring of fire.",
 why="The amrut pot glows inside a tall ring of flames that flicker around it in a dark red heaven.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,-4),"insert","normal",0,"push in on the guarded treasure"),
 focus={"subject":"amrut_pot","depth":"shallow"},vertical={"x":640},layers=L_fire(),background=vista(SKY_FIRE,['#8a4a5a','#6a3a4a','#4a2a3a','#2a1a2a'],sx=640,sy=300),mood={"emotion":"danger","grade":"warm"},
 characters=[{"who":"naga2","x":470,"y":600,"s":.5,"_fixed":True,"flip":1,"pose":"stand","emo":"anger","look":640,"engine":{"a":.0},"actions":[{"word":"fire","emo":"anger","d":.4}]}],
 effects=[pfx("fire_ring","guarded",640,560,420,"the back of the ring of fire behind the pot",behind=True,part="back"),pfx("amrut_pot","guarded",640,460,130,"the amrut pot at the centre of the fire"),
   pfx("fire_ring","fire",640,560,420,"the front flames of the ring cross the pot",part="front"),pfx("embers","fire",640,480,500,"sparks rising from the guarding fire",alpha=.7)],transition_in="cut")
# 9
A("spinning blades",meaning="The gods also guarded it with spinning blades and two snakes.",
 why="A wheel of steel blades spins fast in the middle of the frame with a big crowned guard serpent with glowing red eyes on each side; the guards strike on 'snakes'.",
 camera=cam("handheld",(1.04,0,0),(1.0,0,-4),"wide","normal",2,"a restless handheld shake on the guarded way"),
 focus={"subject":"naga_guard","depth":"deep"},vertical={"x":640},layers=L_fire(),background=vista(SKY_FIRE,['#8a4a5a','#6a3a4a','#4a2a3a','#2a1a2a'],sx=640,sy=300),mood={"emotion":"danger","grade":"warm"},
 characters=[{"who":"naga_guard","x":510,"y":690,"s":.72,"_fixed":True,"flip":1,"pose":"stand","emo":"rage","look":640,"actions":[{"word":"snakes","pose":"point","emo":"rage","d":.4}]},
   {"who":"naga_guard","x":770,"y":690,"s":.72,"_fixed":True,"flip":-1,"pose":"stand","emo":"rage","look":640,"actions":[{"word":"snakes","pose":"point","emo":"rage","d":.4}]}],
 effects=[pfx("spinning_blades","spinning",640,440,230,"the wheel of blades spinning between the guard serpents",sp=9)],transition_in="cut")
# 11
A("Garuda broke through",meaning="Garuda broke through all of it.",
 why="Garuda dives into the ring of fire with wings swept back and a fierce face; flames part around him and a white flash fills the frame on 'broke'.",
 camera=cam("push_in",(1.0,-10,0),(1.1,10,-6),"medium","wide",3,"a hard push as he crashes through the flames"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_fire(),background=vista(SKY_FIRE,['#8a4a5a','#6a3a4a','#4a2a3a','#2a1a2a'],sx=640,sy=300),mood={"emotion":"force","grade":"warm"},
 characters=[{"who":"garuda","x":640,"y":690,"s":.9,"_face":.44,"flip":1,"pose":"fly","emo":"anger","look":700,"wing":1,"flap":.7,"actions":[{"word":"through","pose":"glide","emo":"anger","d":.5}]}],
 effects=[pfx("fire_ring","broke",640,600,520,"flames of the ring behind Garuda as he breaks it",behind=True,part="back"),pfx("fire_ring","broke",640,600,520,"flames of the ring in front of his legs",part="front",alpha=.8),
   {"k":"flash","word":"broke","x":640,"y":360,"meaning":"a white flash as the guard is broken"}],transition_in="flash")
# 12
A("On the way back",meaning="On the way back, he froze.",
 why="Garuda hovers in the sky with the amrut pot held at his chest, eyes wide and wings stopped half open, a still frozen moment.",
 camera=cam("static",(1.06,0,0),(1.06,0,0),"medium","normal",0,"the camera freezes with him"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_clouds(),background=sky(SKY_DAWN),mood={"emotion":"shock","grade":"warm"},
 characters=[{"who":"garuda","x":640,"y":690,"s":.92,"_face":.44,"flip":1,"pose":"glide","emo":"fear","prop":"amrut","wing":.6,"flap":0,"look":720,"actions":[{"word":"froze","emo":"surprise","d":.4}]}],
 effects=[pfx("divine_rays","froze",640,300,520,"a faint ray of divine light ahead of him",alpha=.35,blend="lighter",behind=True)],transition_in="cut")
# 13
A("Vishnu stood in his path",meaning="Vishnu stood in Garuda's path.",
 why="Vishnu stands calm and tall on the right in a golden glow with his hand raised; Garuda hovers small at the left holding the pot, facing him.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"two_shot","normal",0,"a slide toward Vishnu blocking the way"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"awe","grade":"warm"},
 characters=[{"who":"garuda","x":545,"y":690,"s":.74,"_face":.46,"flip":1,"pose":"stand","emo":"surprise","prop":"amrut","look":760,"actions":[{"word":"path","emo":"fear","d":.5}]},
   {"who":"vishnu","x":735,"y":690,"s":.86,"_face":.43,"flip":-1,"pose":"open","emo":"calm","look":540,"actions":[{"word":"stood","emo":"calm","d":.5}]}],
 effects=[glow("Vishnu",780,300,240,GLD,.4,"the golden light around Vishnu")],transition_in="cut")
# 14
A("He knew why",meaning="Vishnu knew why Garuda took the amrut.",
 why="A close bust of Vishnu with a knowing quiet smile and gentle eyes, a pale halo behind his head.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,-4),"close","tele",0,"push in on the god who sees the reason"),
 focus={"subject":"vishnu","depth":"shallow"},vertical={"focus":"vishnu"},layers=L_vk(),background=vk(),mood={"emotion":"insight","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":300,"s":.8,"head":True,"flip":1,"pose":"stand","emo":"calm","look":600,"mood":{"smile":.4},"actions":[{"word":"why","emo":"calm","mood":{"smile":.6},"d":.6}]}],
 effects=[pfx("halo_ring","knew",640,330,380,"the halo of Vishnu's knowing",alpha=.5,blend="lighter",behind=True)],transition_in="cut")
# 15
A("He was happy",meaning="He was happy that Garuda had not tasted any.",
 why="Vishnu smiles warmly with open hands; Garuda stands before him humbly with the full amrut pot untouched at his chest.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"two_shot","normal",0,"pulling back shows the untouched pot between them"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"joy","grade":"warm"},
 characters=[{"who":"garuda","x":545,"y":690,"s":.74,"_face":.46,"flip":1,"pose":"bow","emo":"devotion","prop":"amrut","look":760,"actions":[{"word":"tasted","emo":"devotion","d":.5}]},
   {"who":"vishnu","x":735,"y":690,"s":.86,"_face":.43,"flip":-1,"pose":"stand","emo":"joy","look":540,"actions":[{"word":"happy","pose":"open","emo":"joy","mood":{"smile":.8},"d":.6}]}],
 effects=[],transition_in="cut")
# 16
A("Vishnu offered him",meaning="Vishnu offered him a gift.",
 why="Vishnu holds out his open hand toward the viewer with a warm smile and a ray of light falling from it.",
 camera=cam("tilt_up",(1.02,0,8),(1.08,0,-2),"medium","normal",0,"rising with the open offering hand"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},layers=L_vk(),background=vk(),mood={"emotion":"generosity","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":690,"s":1.0,"_face":.44,"flip":1,"pose":"open","emo":"joy","look":700,"actions":[{"word":"gift","emo":"joy","mood":{"smile":.8},"d":.6}]}],
 effects=[pfx("light_beam","gift",700,330,520,"a beam of light from Vishnu's offering hand",alpha=.5,blend="lighter",behind=True)],transition_in="cut")
# 17
A("Garuda asked for two",meaning="Garuda asked for two things.",
 why="Garuda folds his hands in a humble namaste with wings folded, looking up with devotion as two small gold lights appear beside him.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"push in on the one making a careful request"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_vk(),background=vk(),mood={"emotion":"humility","grade":"warm"},
 characters=[{"who":"garuda","x":640,"y":690,"s":.95,"_face":.43,"flip":1,"pose":"namaste","emo":"devotion","look":720,"actions":[{"word":"two","emo":"devotion","tilt":.04,"d":.5}]}],
 effects=[name("two","Two boons",640,128,30)],transition_in="cut")
# 18  stack: Garuda above Vishnu
A("He wanted to stay",meaning="He wanted to stay above Vishnu.",
 why="Stacked, Garuda hovers in the top half with wings spread and Vishnu stands in the bottom half looking up at him, so Garuda is literally above Vishnu.",
 camera=cam("static",(1.0,0,0),(1.0,0,0),"two_shot","normal",0,"two stacked crops show who is above whom"),
 focus={"subject":"garuda","depth":"deep"},vertical={"mode":"stack","stack":["garuda","vishnu"]},layers=L_clouds('#fff0d4'),background=sky(SKY_VK),mood={"emotion":"aspiration","grade":"warm"},
 characters=[{"who":"garuda","x":420,"y":690,"s":.9,"flip":1,"pose":"fly","emo":"devotion","wing":1,"flap":.2,"look":760,"actions":[{"word":"above","emo":"joy","d":.5}]},
   {"who":"vishnu","x":860,"y":690,"s":.9,"flip":-1,"pose":"stand","emo":"joy","look":540,"actions":[{"word":"stay","emo":"calm","d":.5}]}],
 effects=[],transition_in="wipe")
# 19
A("and he wanted to live",meaning="And he wanted to live forever and never be sick.",
 why="Garuda glows with a bright gold aura and a calm strong smile; his wings are half open and radiant light rays fan out behind him.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"push in on a body that will not age"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_vk(),background=vk(),mood={"emotion":"vitality","grade":"warm"},
 characters=[{"who":"garuda","x":640,"y":690,"s":.95,"_face":.43,"flip":1,"pose":"spread","emo":"joy","aura":"255,214,140","look":700,"actions":[{"word":"forever","emo":"joy","d":.5},{"word":"sick","emo":"calm","mood":{"smile":.6},"d":.5}]}],
 effects=[pfx("divine_rays","forever",640,340,560,"rays of deathless light behind Garuda",alpha=.5,blend="lighter",behind=True)],transition_in="cut")
# 20
A("without drinking",meaning="He wanted this without drinking the amrut.",
 why="Garuda turns his head away from the glowing amrut pot with calm eyes, refusing it while the pot glows quietly at the right.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"two_shot","normal",0,"a drift past the refused pot"),
 focus={"subject":"garuda","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"restraint","grade":"warm"},
 characters=[{"who":"garuda","x":560,"y":690,"s":.82,"_face":.44,"flip":1,"pose":"stand","emo":"calm","look":380,"mood":{"lx":-.8,"turn":-.5},"actions":[{"word":"amrut","emo":"calm","d":.5}]}],
 effects=[pfx("amrut_pot","drinking",725,470,110,"the amrut pot Garuda does not touch"),glow("drinking",725,450,160,"255,240,190",.4,"the pale glow of the untouched amrut")],transition_in="cut")
# 21
A("Vishnu said yes",meaning="Vishnu said yes to both.",
 why="Vishnu smiles with a clear nod and an open palm; a soft gold glow shows his yes.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"medium","normal",0,"pulling back from the answering face"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"focus":"vishnu"},layers=L_vk(),background=vk(),mood={"emotion":"assent","grade":"warm"},
 characters=[{"who":"vishnu","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"open","emo":"joy","look":700,"tilt":.04,"actions":[{"word":"both","emo":"joy","mood":{"smile":.9},"d":.5}]}],
 effects=[glow("yes",640,330,260,GLD,.45,"the warm gold of Vishnu's yes")],transition_in="cut")
# 22
A("In return",meaning="In return, Vishnu asked Garuda to carry him.",
 why="Vishnu points toward Garuda, who stands at the right with wings half open and listens with a serious face; a gold line of light joins them.",
 camera=cam("dolly_left",(1.0,10,0),(1.0,-10,0),"two_shot","normal",0,"sliding from the asker to the one asked"),
 focus={"subject":"vishnu","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"request","grade":"warm"},
 characters=[{"who":"vishnu","x":545,"y":690,"s":.86,"_face":.43,"flip":1,"pose":"point","emo":"calm","look":760,"actions":[{"word":"carry","emo":"calm","d":.5}]},
   {"who":"garuda","x":735,"y":690,"s":.78,"_face":.45,"flip":-1,"pose":"stand","emo":"surprise","look":540,"wing":.5,"actions":[{"word":"carry","emo":"devotion","d":.5}]}],
 effects=[],transition_in="cut")
# 23
A("A carrier like that",meaning="A carrier like that is called a vahana.",
 why="Garuda in his carry pose with strong arms ready and wings half raised, and the word 'Vahana' appears above him on 'vahana'.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"push in on the carrier as the word is named"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_vk(),background=vk(),mood={"emotion":"service","grade":"warm"},
 characters=[{"who":"garuda","x":640,"y":690,"s":.95,"_face":.43,"flip":1,"pose":"carry","emo":"devotion","look":700,"wing":.6,"actions":[{"word":"vahana","pose":"spread","emo":"pride","d":.6}]}],
 effects=[name("vahana","Vahana",640,128,34)],transition_in="cut")
# 24
A("Further on",meaning="Further on, Indra, king of the gods, was angry.",
 why="Indra stands among storm clouds in his crown with a dark angry face and the Vajra in his raised hand, lightning flickering behind him.",
 camera=cam("tilt_up",(1.0,0,10),(1.06,0,0),"medium","normal",0,"tilting up to the king of the gods as his anger rises"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_storm(),background=sky(SKY_STORM),mood={"emotion":"anger","grade":"cool"},
 characters=[{"who":"indra","x":640,"y":690,"s":1.0,"_face":.43,"flip":1,"pose":"stand","emo":"anger","look":700,"actions":[{"word":"gods","pose":"throw","emo":"rage","d":.5}]}],
 effects=[pfx("lightning_forks","Indra",640,260,520,"lightning crackling behind Indra",alpha=.6,blend="lighter",behind=True),name("Indra","Indra",640,128,32)],transition_in="cut")
# 25
A("threw his thunder",meaning="He threw his thunder weapon, the Vajra, at Garuda.",
 why="Indra throws his arm forward at the left with a roaring face while the Vajra flies away from his hand in a streak of lightning toward the right.",
 camera=cam("handheld",(1.04,0,0),(1.08,0,-4),"medium","wide",3,"a sudden shake as the weapon leaves his hand"),
 focus={"subject":"indra","depth":"deep"},vertical={"x":640},layers=L_storm(),background=sky(SKY_STORM),mood={"emotion":"attack","grade":"cool"},
 characters=[{"who":"indra","x":540,"y":690,"s":.95,"_face":.43,"flip":1,"pose":"throw","emo":"rage","look":780,"actions":[{"word":"Vajra","emo":"rage","d":.4}]}],
 effects=[pfx("vajra_thrown","Vajra",620,330,260,"the Vajra flies from Indra's hand with a lightning trail",vx=240),pfx("lightning_bolt_a","thunder",700,250,420,"a bolt of the thunder weapon",alpha=.7,blend="lighter",behind=True)],transition_in="flash")
# 26
A("at Garuda",meaning="The Vajra struck Garuda, and it took only one golden feather from him.",
 why="Garuda hovers calm in the storm sky, wings spread; the thrown Vajra streaks in from the left and a white flash bursts on 'Garuda', then one golden feather drifts down and he looks at it unhurt.",
 camera=cam("push_in",(1.0,0,0),(1.1,0,-4),"medium","normal",2,"push in on the target of the thunderbolt"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_storm(),background=sky(SKY_STORM),mood={"emotion":"impact","grade":"cool"},
 characters=[{"who":"garuda","x":660,"y":690,"s":.92,"_face":.44,"flip":-1,"pose":"spread","emo":"calm","look":500,"actions":[{"word":"golden","pose":"glide","emo":"calm","mood":{"smile":.4,"ly":.5},"d":.5}]}],
 effects=[pfx("vajra_thrown","at",380,360,240,"the Vajra arrives from the left",vx=200),{"k":"flash","word":"Garuda","x":640,"y":340,"meaning":"a flash as the Vajra strikes"},
   pfx("golden_feather","golden",700,300,180,"one golden feather falls away from him",fall=1,vy=40)],transition_in="cut")
# 28
A("Indra saw",meaning="Indra saw his strength and stepped aside.",
 why="Indra, with wide eyes and lowered Vajra, steps back out of the way to the left and looks at Garuda with respect.",
 camera=cam("pan_left",(1.04,10,0),(1.04,-10,0),"medium","normal",0,"panning with the retreating king"),
 focus={"subject":"indra","depth":"deep"},vertical={"focus":"indra"},layers=L_storm(),background=sky(SKY_STORM),mood={"emotion":"respect","grade":"cool"},
 characters=[{"who":"indra","x":680,"y":690,"s":.95,"_face":.43,"flip":-1,"pose":"stand","emo":"surprise","look":820,"walkTo":{"x":560,"c":"stepped","d":1.2,"sp":.6},"actions":[{"word":"strength","emo":"shame","d":.5}]}],
 effects=[],transition_in="cut")
# 29
A("Garuda put the pot",meaning="Garuda put the pot down before the snakes.",
 why="Garuda gently sets the glowing amrut pot on the ground in front of him while two cobras rise watchfully at the right.",
 camera=cam("tilt_down",(1.0,0,-8),(1.0,0,6),"medium","normal",0,"tilting down with the pot to the ground"),
 focus={"subject":"garuda","depth":"deep"},vertical={"x":640},layers=L_naga(),background=vista(),mood={"emotion":"delivery","grade":"cool"},
 characters=[{"who":"garuda","x":545,"y":690,"s":.8,"_face":.44,"flip":1,"pose":"bow","emo":"calm","prop":"amrut","look":720,"actions":[{"word":"down","pose":"stand","emo":"calm","d":.5}]},
   {"who":"naga","x":720,"y":660,"s":.62,"_fixed":True,"flip":-1,"pose":"stand","emo":"calm","look":560,"actions":[{"word":"snakes","emo":"anger","d":.4}]},
   {"who":"naga2","x":790,"y":650,"s":.55,"_fixed":True,"flip":-1,"pose":"stand","emo":"calm","look":560,"actions":[{"word":"snakes","emo":"anger","d":.4}]}],
 effects=[pfx("amrut_pot","down",640,610,90,"the amrut pot set on the ground",alpha=1)],transition_in="cut")
# 30
A("They freed his mother",meaning="They freed his mother.",
 why="Vinata smiles with joy and presses her hands together while Garuda stands beside her with a happy face; a warm gold glow lights them both.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"two_shot","normal",0,"push in on the reunited mother and son"),
 focus={"subject":"vinata","depth":"deep"},vertical={"x":640},layers=L_naga(),background=vista(SKY_DAWN,['#8a94dc','#6a80c0','#5a6aa0','#4a5a88']),mood={"emotion":"joy","grade":"warm"},
 characters=[{"who":"vinata","x":545,"y":690,"s":.8,"_face":.44,"flip":1,"pose":"namaste","emo":"joy","look":720,"actions":[{"word":"mother","emo":"joy","mood":{"smile":.9},"d":.5}]},
   {"who":"garuda","x":735,"y":690,"s":.78,"_face":.44,"flip":-1,"pose":"stand","emo":"joy","look":560,"actions":[{"word":"freed","emo":"joy","d":.5}]}],
 effects=[glow("freed",650,320,300,GLD,.45,"the warm light of freedom")],transition_in="cut")
# 31
A("Later, Garuda said",meaning="Later, Garuda said he would carry Vishnu.",
 why="Garuda bows with folded hands before Vishnu, who stands tall in golden light on the right; his wings are folded in respect.",
 camera=cam("dolly_right",(1.0,-10,0),(1.0,10,0),"two_shot","normal",0,"a slow slide from the one who bows to the one he serves"),
 focus={"subject":"garuda","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"devotion","grade":"warm"},
 characters=[{"who":"garuda","x":545,"y":690,"s":.78,"_face":.45,"flip":1,"pose":"bow","emo":"devotion","look":760,"actions":[{"word":"carry","pose":"namaste","emo":"devotion","d":.5}]},
   {"who":"vishnu","x":735,"y":690,"s":.86,"_face":.43,"flip":-1,"pose":"stand","emo":"joy","look":540,"actions":[{"word":"Vishnu","emo":"joy","d":.5}]}],
 effects=[glow("Vishnu",780,300,240,GLD,.4,"the golden light around Vishnu")],transition_in="cut")
# 32
A("Vishnu had made him",meaning="Vishnu had made him his mount.",
 why="Vishnu points a hand of blessing at Garuda, who spreads his wings proudly beside him; light rays open behind both.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"two_shot","normal",0,"pulling back to show the two together"),
 focus={"subject":"garuda","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"honour","grade":"warm"},
 characters=[{"who":"vishnu","x":545,"y":690,"s":.86,"_face":.43,"flip":1,"pose":"open","emo":"joy","look":760,"actions":[{"word":"mount","emo":"joy","d":.5}]},
   {"who":"garuda","x":735,"y":690,"s":.78,"_face":.44,"flip":-1,"pose":"spread","emo":"pride","look":540,"actions":[{"word":"mount","emo":"pride","d":.5}]}],
 effects=[pfx("divine_rays","made",650,330,520,"rays of blessing behind them",alpha=.45,blend="lighter",behind=True)],transition_in="cut")
# 33
A("That is why",meaning="That is why Garuda became Vishnu's vahana.",
 why="Garuda flies high in glory with wings wide and a proud face under rays of light, and the word 'Vahana' appears above him.",
 camera=cam("push_in",(1.0,0,0),(1.08,0,-4),"medium","normal",0,"push in on the finished answer"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_clouds('#fff0d4'),background=sky(SKY_VK),mood={"emotion":"triumph","grade":"warm"},
 characters=[{"who":"garuda","x":640,"y":690,"s":.95,"_face":.43,"flip":1,"pose":"fly","emo":"pride","wing":1,"flap":.5,"look":700,"actions":[{"word":"vahana","emo":"joy","d":.5}]}],
 effects=[pfx("divine_rays","why",640,340,560,"rays of glory behind Garuda",alpha=.5,blend="lighter",behind=True),name("vahana","Vahana",640,128,34)],transition_in="fade")
# 34
A("He won the amrut",meaning="He won the amrut for his mother's freedom and never tasted it.",
 why="Garuda holds the glowing amrut pot at his chest and looks gently away from it with a faint loving smile, thinking of his mother.",
 camera=cam("dolly_right",(1.0,-8,0),(1.04,8,0),"medium","normal",0,"a slow drift past the pot he never drank"),
 focus={"subject":"garuda","depth":"deep"},vertical={"focus":"garuda"},layers=L_clouds('#fff0d4'),background=sky(SKY_VK),mood={"emotion":"selflessness","grade":"warm"},
 characters=[{"who":"garuda","x":640,"y":690,"s":.95,"_face":.43,"flip":1,"pose":"stand","emo":"devotion","prop":"amrut","look":560,"mood":{"smile":.4},"actions":[{"word":"freedom","emo":"joy","mood":{"smile":.5},"d":.5}]}],
 effects=[glow("amrut",640,360,260,"255,240,190",.4,"the pale glow of the untouched amrut")],transition_in="cut")
# 35
A("Vishnu rewarded him",meaning="Vishnu rewarded him, and Garuda gave his strength in return.",
 why="Garuda bows his head with folded hands before smiling Vishnu; a gold glow and drifting petals close the story.",
 camera=cam("pull_out",(1.1,0,-4),(1.0,0,0),"two_shot","normal",0,"the last pull back on the god and his mount"),
 focus={"subject":"garuda","depth":"deep"},vertical={"x":640},layers=L_vk(),background=vk(),mood={"emotion":"fulfilment","grade":"warm"},
 characters=[{"who":"garuda","x":545,"y":690,"s":.78,"_face":.45,"flip":1,"pose":"namaste","emo":"devotion","look":760,"actions":[{"word":"strength","pose":"bow","emo":"devotion","d":.5}]},
   {"who":"vishnu","x":735,"y":690,"s":.86,"_face":.43,"flip":-1,"pose":"open","emo":"joy","look":540,"actions":[{"word":"rewarded","emo":"joy","mood":{"smile":.8},"d":.5}]}],
 effects=[glow("rewarded",650,300,300,GLD,.45,"the gold of the reward")],transition_in="cut")
G.finish()
