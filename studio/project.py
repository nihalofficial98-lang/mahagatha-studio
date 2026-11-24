"""Where a project lives, so the episode tools also run reels.
  '06'                    -> episodes/ep06 (episode.json) + build/ep06            format 16:9 (default)
  'reel02', '_test', ...  -> reels/reel02 (reel.json)    + reels/build/reel02     format from reel.json ("vertical")
A project id that starts with 'reel' or '_' is a reel. meta() returns episode.json or reel.json; target_sec of a reel = its audio
duration (no tempo change of the owner's voice)."""
import os,json
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def is_reel(p):return str(p).startswith(('reel','_'))
def edir(p):return f'{R}/reels/{p}' if is_reel(p) else f'{R}/episodes/ep{p}'
def bdir(p):return f'{R}/reels/build/{p}' if is_reel(p) else f'{R}/build/ep{p}'
def meta_file(p):return edir(p)+('/reel.json' if is_reel(p) else '/episode.json')
def meta(p):
    f=meta_file(p)
    if not os.path.exists(f):return {}
    m=json.load(open(f,encoding='utf-8'))
    if is_reel(p):m.setdefault('format','vertical');m.setdefault('target_sec',m.get('duration',0))
    return m
def fmt(p,override=None):
    if override and override!='auto':return override
    return meta(p).get('format','16:9')
def target(p):return meta(p).get('target_sec',0)
def label(p):return p.upper() if is_reel(p) else f'EP{p}'
