"""Numbered review sheets: python3 studio/review_sheets.py 03  ->  library/review/ep03/sheet_NN.jpg + ep03_frames.pdf
Each tile = one shot (frame #N, start time, beat). Frame numbers start at 1 and match shots.json order."""
import os,sys,json,glob
from PIL import Image,ImageDraw,ImageFont
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n=sys.argv[1];per=12;cols=3;tw,th=640,360
sh=json.load(open(f'{ROOT}/episodes/ep{n}/shots.json',encoding='utf-8'))
st=sorted(glob.glob(f'{ROOT}/build/ep{n}/stills/t*.png'),key=lambda p:float(os.path.basename(p)[1:-4]))
assert len(st)==len(sh),(len(st),len(sh))
out=f'{ROOT}/library/review/ep{n}';os.makedirs(out,exist_ok=True)
for f in glob.glob(out+'/sheet_*.jpg'):os.remove(f)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',34) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') else ImageFont.load_default()
F2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') else ImageFont.load_default()
pages=[]
for pg in range(0,len(st),per):
    rows=(min(per,len(st)-pg)+cols-1)//cols;sheet=Image.new('RGB',(tw*cols,th*rows),(12,10,8))
    for k in range(min(per,len(st)-pg)):
        i=pg+k;im=Image.open(st[i]).convert('RGB').resize((tw,th),Image.LANCZOS);d=ImageDraw.Draw(im)
        tcode=float(os.path.basename(st[i])[1:-4]);mm,ss=int(tcode//60),int(tcode%60)
        d.rounded_rectangle((8,8,8+16+len(str(i+1))*22+30,56),10,fill=(255,208,80));d.text((20,12),f'#{i+1}',font=F,fill=(30,20,5))
        lab=f'{mm}:{ss:02d}  B{sh[i]["beat"]:02d}';d.rounded_rectangle((tw-8-len(lab)*14-16,8,tw-8,44),8,fill=(0,0,0,));d.text((tw-8-len(lab)*14-8,13),lab,font=F2,fill=(255,235,190))
        d.rectangle((0,0,tw-1,th-1),outline=(60,50,40));sheet.paste(im,((k%cols)*tw,(k//cols)*th))
    p=f'{out}/sheet_{pg//per+1:02d}.jpg';sheet.save(p,quality=88);pages.append(sheet)
pages[0].save(f'{out}/ep{n}_frames.pdf',save_all=True,append_images=pages[1:],resolution=100)
print(len(st),'frames ->',len(pages),'sheets',out)
