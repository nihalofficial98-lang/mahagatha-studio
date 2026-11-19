"""Paint open eyes on Brahma (3 faces) and Daksha cut-outs (closed-line eyes -> open eyes under the brow line)."""
from PIL import Image,ImageDraw
import shutil,os
S=6
def eye(d,cx,cy,w,h,ir,look=0):
    cx*=S;cy*=S;w*=S;h*=S;ir*=S
    d.ellipse((cx-w/2,cy-h/2,cx+w/2,cy+h/2),fill=(250,246,238,255),outline=(70,36,22,255),width=int(1.6*S))
    ix=cx+look*S;d.ellipse((ix-ir,cy-ir,ix+ir,cy+ir),fill=(48,26,16,255));d.ellipse((ix-ir*.9,cy-ir*.9,ix-ir*.1,cy-ir*.1),fill=(255,255,255,255))
def run(name,eyes):
    src=f'library/puppets/{name}/full_orig.png'
    if not os.path.exists(src):src=f'library/puppets/{name}/full.png'
    im=Image.open(src).convert('RGBA');W,H=im.size
    big=Image.new('RGBA',(W*S,H*S),(0,0,0,0));d=ImageDraw.Draw(big)
    for e in eyes:eye(d,*e)
    ov=big.resize((W,H),Image.LANCZOS);out=Image.alpha_composite(im,ov)
    out.save(f'library/puppets/{name}/full.png');out.save(f'library/pilot/assets/lib_{name}.png')
run('brahma',[(391,174,26,12,4.6),(443,174,26,12,4.6),(334,168,19,10,3.8,1),(501,168,19,10,3.8,-1)])
run('daksha',[(196.5,141,32,13,5),(243,141,32,13,5)])
