"""Build frames/contact_sheet.jpg from the rendered PNG frames (4 columns, labelled)."""
import glob,os
from PIL import Image,ImageDraw,ImageFont
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'frames')
fs=sorted(glob.glob(D+'/*.png'),key=lambda f:(['brahma','vishnu','shiva','trio'].index(os.path.basename(f).split('_')[0]),f))
W,H,C=480,270,4;rows=(len(fs)+C-1)//C;im=Image.new('RGB',(W*C,(H+28)*rows+60),(14,10,24))
try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17);big=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',30)
except Exception:font=big=ImageFont.load_default()
d=ImageDraw.Draw(im);d.text((16,14),'Trimurti - new paper-cut look: key frames (Brahma, Vishnu on Shesha, Shiva, trio)',fill=(242,193,78),font=big)
for i,f in enumerate(fs):
    x,y=(i%C)*W,60+(i//C)*(H+28);im.paste(Image.open(f).convert('RGB').resize((W-6,H-6)),(x+3,y+3));d.text((x+8,y+H+2),os.path.basename(f)[:-4],fill=(235,225,255),font=font)
im.save(os.path.join(D,'contact_sheet.jpg'),quality=88);print(len(fs),'frames ->',os.path.join(D,'contact_sheet.jpg'))
