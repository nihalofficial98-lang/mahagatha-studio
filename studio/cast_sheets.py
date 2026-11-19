"""Numbered contact sheets of the cast library: python3 studio/cast_sheets.py -> library/review/cast/cast_NN.jpg (+ cast_index.json id->number)"""
import os,json,glob
from PIL import Image,ImageDraw
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));P=R+'/library/puppets/';O=R+'/library/review/cast/';os.makedirs(O,exist_ok=True)
for f in glob.glob(O+'cast_*.jpg'):os.remove(f)
M=json.load(open(P+'cast.json'));ids=[k for k in M['characters'] if os.path.exists(f'{P}{k}/full.png')]
cols,rows=5,3;per=cols*rows;W,H=400,540;idx={}
for pg in range(0,len(ids),per):
    sheet=Image.new('RGB',(W*cols,H*rows),(54,60,78));d=ImageDraw.Draw(sheet)
    for j,k in enumerate(ids[pg:pg+per]):
        n=pg+j+1;idx[k]=n;im=Image.open(f'{P}{k}/full.png').convert('RGBA');s=min((W-24)/im.width,(H-80)/im.height);im=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.LANCZOS)
        x,y=(j%cols)*W,(j//cols)*H;sheet.paste(im,(x+(W-im.width)//2,y+62+(H-80-im.height)//2),im)
        lab=f'{n}. {k}';d.rounded_rectangle((x+8,y+8,x+24+len(lab)*10,y+42),8,fill=(255,208,80));d.text((x+18,y+18),lab,fill=(30,20,5))
    sheet.save(f'{O}cast_{pg//per+1:02d}.jpg',quality=86)
json.dump(idx,open(O+'cast_index.json','w'),indent=1);print(len(ids),'characters ->',(len(ids)+per-1)//per,'sheets')
