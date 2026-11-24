import os
"""Assemble the film engine (art + main + shots + scenes) into one HTML page next to engine/fonts.
usage: python3 studio/build.py [--scale 1.5|3] [--format 16:9|vertical] [--out engine/_built.html]   (scale 1.5 = 1080p, 3 = 4K)
--format vertical: 9:16 reel engine, canvas 720x1280 * scale (1.0 = 720x1280, 1.5 = 1080x1920); the 16:9 world is drawn at CH/720 and
shown through a portrait camera window (engine/main.js, VERTICAL section). Default 16:9 output is unchanged."""
import argparse,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def build(scale=1.5,out=None,fmt='16:9'):
    vert=fmt=='vertical';out=out or os.path.join(ROOT,'engine',f'_built_{"v" if vert else ""}{scale}.html');d=os.path.join(ROOT,'engine')
    cw,ch=(int(720*scale),int(1280*scale)) if vert else (int(1280*scale),int(720*scale))
    rd=lambda *p:open(os.path.join(*p),encoding='utf-8').read()
    # v2 characters: Shiva core (single source of truth in library/characters/shiva) + generic cast, wrapped so their helpers stay private
    v2='const V2=(function(){'+rd(d,'paper_kit.js')+'\n'+rd(ROOT,'library','characters','shiva','shiva_v2.js')+'\n'+rd(d,'v2_cast.js')+'\n})();\n'
    js=rd(d,'art.js')+v2+''.join(rd(d,f) for f in ('main.js','shots.js','scenes.js','v2_scenes.js','paper_scenes.js','paper_fx.js'))
    js=js.replace('let SC_=1.5;','let SC_=%s;'%(round(ch/720,6) if vert else scale)).replace('CW_=1920,CH_=1080;','CW_=%d,CH_=%d;'%(cw,ch))
    if vert:js=js.replace('let LAT=false,VERT=false;','let LAT=false,VERT=true;',1)
    latin=os.path.join(d,'fonts','noto-serif-latin-latin-600-normal.woff2')   # optional: drop this file in engine/fonts to bundle a Latin subtitle font (English episodes)
    lat="@font-face{font-family:NSerLat;font-weight:600;src:url('fonts/noto-serif-latin-latin-600-normal.woff2')}\n" if os.path.exists(latin) else ''
    html='''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:NSer;font-weight:600;src:url('fonts/noto-serif-devanagari-devanagari-600-normal.woff2')}
@font-face{font-family:NSer;font-weight:700;src:url('fonts/noto-serif-devanagari-devanagari-700-normal.woff2')}
%shtml,body{margin:0;background:#000}canvas{display:block}</style></head><body><canvas id="c" width="%d" height="%d"></canvas><script>
%s</script></body></html>'''%(lat,cw,ch,js)
    open(out,'w').write(html);return out
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--scale',type=float,default=1.5);a.add_argument('--out');a.add_argument('--format',default='16:9',choices=['16:9','vertical']);x=a.parse_args();print(build(x.scale,x.out,x.format))
