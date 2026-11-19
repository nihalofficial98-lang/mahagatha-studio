"""Assemble the film engine (art + main + shots + scenes) into one HTML page next to engine/fonts.
usage: python3 studio/build.py [--scale 1.5|3] [--out engine/_built.html]   (scale 1.5 = 1080p, 3 = 4K)"""
import argparse,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def build(scale=1.5,out=None):
    out=out or os.path.join(ROOT,'engine',f'_built_{scale}.html');d=os.path.join(ROOT,'engine')
    js=''.join(open(os.path.join(d,f)).read() for f in ('art.js','main.js','shots.js','scenes.js'))
    js=js.replace('let SC_=1.5;','let SC_=%s;'%scale).replace('CW_=1920,CH_=1080;','CW_=%d,CH_=%d;'%(int(1280*scale),int(720*scale)))
    html='''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:NSer;font-weight:600;src:url('fonts/noto-serif-devanagari-devanagari-600-normal.woff2')}
@font-face{font-family:NSer;font-weight:700;src:url('fonts/noto-serif-devanagari-devanagari-700-normal.woff2')}
html,body{margin:0;background:#000}canvas{display:block}</style></head><body><canvas id="c" width="%d" height="%d"></canvas><script>
%s</script></body></html>'''%(int(1280*scale),int(720*scale),js)
    open(out,'w').write(html);return out
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--scale',type=float,default=1.5);a.add_argument('--out');x=a.parse_args();print(build(x.scale,x.out))
