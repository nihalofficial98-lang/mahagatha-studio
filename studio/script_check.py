#!/usr/bin/env python3
"""Retention + length checker for an episode script (any language).

  python3 studio/script_check.py 07                 check episodes/ep07/script.hi.md (or script.md) against beats.json
  python3 studio/script_check.py 07 --lang en       check script.en.md (same beats.json, English pace)
  python3 studio/script_check.py 06 --beats library/examples/ep06_beats_example.json   check with another beats file
  python3 studio/script_check.py 07 --estimate       ignore recorded timings, use words x pace
  python3 studio/script_check.py 07 --anchors hi    print cue_id -> beat + anchor phrase (for shot briefs)
  python3 studio/script_check.py 06 --calibrate     measure pace from build/ep06/timings.json -> library/voice_profile.json
  python3 studio/script_check.py --selftest         run the built-in tests

Rules: guides/SCRIPT_STYLE.md, schema: guides/BEATS_SCHEMA.md, numbers: library/script_rules.json + library/voice_profile.json.
Exit code: 1 if any ERROR (only possible when beats.json exists), else 0. Without beats.json the
structure checks are skipped and everything is a warning (legacy scripts such as EP06 still pass).
"""
import argparse, json, os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE = os.path.join(ROOT, 'library', 'voice_profile.json')
RULES = os.path.join(ROOT, 'library', 'script_rules.json')
ROLES = {'hook', 'stakes', 'plant', 'setup', 'rehook', 'turn', 'climax', 'payoff', 'answer',
         'recap', 'bridge', 'question', 'tease'}
BACKREF = {'hi': ['जैसा हमने देखा', 'जैसा कि हमने देखा', 'जैसा हमने पहले', 'जैसा पहले बताया', 'पहले बताया था',
                  'पिछले हिस्से में', 'पिछले अध्याय'],
           'en': ['as we saw', 'as we have seen', "as we've seen", 'as mentioned', 'as i said', 'like we said',
                  'earlier we saw', 'in the last chapter', 'in the previous part']}
SCRIPT_NAMES = {'hi': ['script.hi.md', 'script.md']}


# ---------- loading ----------
def load_json(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def parse_script(path):
    """**B07** [cue] + lines -> [{id,num,cue,lines,text,words}] (same rules as studio.py beats())."""
    out, cur = [], None
    for raw in open(path, encoding='utf-8').read().split('\n'):
        l = raw.strip()
        m = re.match(r'\*\*B(\d+)\*\*\s*(\[[^\]]*\])?', l)
        if m:
            cur = {'num': int(m.group(1)), 'id': 'B%02d' % int(m.group(1)), 'cue': (m.group(2) or '').strip('[]').strip(), 'lines': []}
            out.append(cur)
            continue
        if l.startswith('---'):
            cur = None
            continue
        if cur and l and not l.startswith(('#', '*समाप्त', '*The End', '<!--')):
            cur['lines'].append(l)
    for b in out:
        b['text'] = ' '.join(b['lines'])
        b['words'] = count_words(b['text'])
    return out


def count_words(t):
    return sum(1 for w in t.split() if any(c.isalpha() for c in w))


def script_path(epdir, lang):
    for name in SCRIPT_NAMES.get(lang, ['script.%s.md' % lang]):
        p = os.path.join(epdir, name)
        if os.path.exists(p):
            return p
    return None


def timings_path(n, lang):
    return os.path.join(ROOT, 'build', 'ep' + n, 'timings.json') if lang == 'hi' else os.path.join(ROOT, 'build', 'ep' + n, lang, 'timings.json')


def pace_for(profile, lang):
    if os.environ.get('PACE'):
        return float(os.environ['PACE']), 'PACE env'
    p = profile.get(lang) or {}
    if 'sec_per_word' not in p:
        sys.exit('no pace for language %r in library/voice_profile.json' % lang)
    return float(p['sec_per_word']), ('measured' if p.get('measurements') else 'PROVISIONAL')


def norm(s):
    return re.sub(r'[\s,.!?।"“”\'‘’—–-]+', ' ', s).strip().lower()


# ---------- core check ----------
class Report:
    def __init__(self):
        self.rows, self.issues = [], []

    def row(self, name, value, rule, ok, level='ERROR'):
        self.rows.append((name, value, rule, 'ok' if ok else ('FAIL' if level == 'ERROR' else 'warn')))

    def add(self, level, msg):
        self.issues.append((level, msg))

    @property
    def errors(self):
        return [m for l, m in self.issues if l == 'ERROR']


def check(script, beats_doc, lang, pace, rules, measured=None, wordband=None):
    """script: parse_script() output; beats_doc: beats.json dict or None; measured: {num: seconds} or None."""
    R = Report()
    E = 'ERROR' if beats_doc else 'WARN'   # legacy scripts: warn only
    wb = wordband or {'short': [15, 40], 'long': [60, 100], 'max': 110}
    if not script:
        R.add('ERROR', 'no beats found in the script (expected lines like **B01** [cue])')
        return R
    # durations + start times
    t = 0.0
    for b in script:
        b['sec'] = measured[b['num']] if measured and b['num'] in measured else b['words'] * pace
        b['start'] = t
        t += b['sec']
    total = t
    words = sum(b['words'] for b in script)
    lo, hi = rules['video_sec']
    R.row('length', '%.2f min (%d words)' % (total / 60, words), '%g-%g min' % (lo / 60, hi / 60), lo <= total <= hi, E)
    if not lo <= total <= hi:
        need = (lo if total < lo else hi) - total
        R.add(E, 'length %.2f min is outside %g-%g min: %s about %d words' % (total / 60, lo / 60, hi / 60, 'add' if need > 0 else 'cut', abs(need) / pace))
    elif not rules['aim_sec'][0] <= total <= rules['aim_sec'][1]:
        R.add('WARN', 'length %.2f min is legal but outside the aim %g-%g min' % (total / 60, rules['aim_sec'][0] / 60, rules['aim_sec'][1] / 60))
    # per-beat basics
    for b in script:
        if not b['cue']:
            R.add(E, '%s: no [emotion cue]' % b['id'])
        if b['words'] == 0:
            R.add(E, '%s: empty' % b['id'])
        if re.search(r'\bTODO\b', b['text']):
            R.add(E, '%s: still has TODO placeholder text' % b['id'])
        if b['words'] > wb['max']:
            R.add('WARN', '%s: %d words (~%.0f s) is too long; split it (max %d)' % (b['id'], b['words'], b['sec'], wb['max']))
        if lang == 'hi' and re.search(r'[A-Za-z]{4,}', b['text']):
            R.add('WARN', '%s: Latin text in Hindi narration' % b['id'])
        if lang != 'hi' and re.search(r'[ऀ-ॿ]', b['text']):
            R.add('WARN', '%s: Devanagari text in %s narration (write names in the language, no transliteration clutter)' % (b['id'], lang))
    R.row('cue tags', '%d/%d beats' % (sum(1 for b in script if b['cue']), len(script)), 'every beat', all(b['cue'] for b in script), E)
    # beat-length variety
    band = lambda w: 'S' if w <= wb['short'][1] else ('L' if w >= wb['long'][0] else 'M')
    bands = [band(b['words']) for b in script]
    ns, nl = bands.count('S'), bands.count('L')
    run, worst, prev = 0, 0, None
    for x in bands:
        run = run + 1 if x == prev else 1
        worst, prev = max(worst, run), x
    var_ok = ns >= rules['min_short_beats'] and nl >= rules['min_long_beats']
    R.row('beat variety', '%d short / %d mid / %d long, run %d' % (ns, bands.count('M'), nl, worst),
          '>=%d S(%d-%dw) >=%d L(%d-%dw)' % (rules['min_short_beats'], wb['short'][0], wb['short'][1], rules['min_long_beats'], wb['long'][0], wb['long'][1]), var_ok, E)
    if not var_ok:
        R.add(E, 'pace is flat: need >=%d short beats (%d-%d words) and >=%d long ones (%d-%d words); word counts: %s'
              % (rules['min_short_beats'], wb['short'][0], wb['short'][1], rules['min_long_beats'], wb['long'][0], wb['long'][1],
                 ' '.join('%s=%d' % (b['id'], b['words']) for b in script)))
    if worst > rules['max_same_band_run']:
        R.add('WARN', '%d beats in a row have the same length band (%s); alternate short punches with longer scenes' % (worst, ''.join(bands)))
    if not beats_doc:
        R.add('WARN', 'no beats.json: chapter/reel/hook/climax checks skipped (write episodes/epNN/beats.json, guides/BEATS_SCHEMA.md)')
        return R
    check_structure(R, script, beats_doc, lang, rules, total)
    return R


def check_structure(R, script, doc, lang, rules, total):
    sb = {b['id']: b for b in script}
    beats = doc.get('beats', [])
    ids = [b.get('id') for b in beats]
    # 1. beats.json <-> script
    missing = [i for i in ids if i not in sb]
    extra = [i for i in sb if i not in ids]
    order_ok = [i for i in ids if i in sb] == [b['id'] for b in script if b['id'] in ids]
    R.row('beats match', '%d json / %d script' % (len(ids), len(script)), 'same ids, same order', not missing and not extra and order_ok)
    if missing:
        R.add('ERROR', 'beats in beats.json but not in the script: %s' % ', '.join(missing))
    if extra:
        R.add('ERROR', 'beats in the script but not in beats.json: %s' % ', '.join(extra))
    if not order_ok:
        R.add('ERROR', 'beat order differs between beats.json and the script')
    chapters = {c['id']: c for c in doc.get('chapters', [])}
    names = doc.get('names', {})
    cues = doc.get('cues', {})
    # annotate
    B = []
    for b in beats:
        s = sb.get(b['id'])
        if not s:
            continue
        x = dict(b, sec=s['sec'], start=s['start'], words=s['words'], text=s['text'], roles=set(b.get('roles', [])))
        bad = x['roles'] - ROLES
        if bad:
            R.add('ERROR', '%s: unknown roles %s (allowed: %s)' % (b['id'], sorted(bad), ', '.join(sorted(ROLES))))
        if b.get('chapter') not in chapters:
            R.add('ERROR', '%s: chapter %r is not in "chapters"' % (b['id'], b.get('chapter')))
        bud = b.get('budget_sec')
        if bud and abs(x['sec'] - bud) > max(6, rules['budget_tolerance'] * bud):
            R.add('WARN', '%s: ~%.0f s vs budget %s s (%+d words to fit)' % (b['id'], x['sec'], bud, round((bud - x['sec']) / (x['sec'] / max(x['words'], 1)))))
        for cid in b.get('cue_ids', []):
            c = cues.get(cid)
            if c is None:
                R.add('ERROR', '%s: cue_id %r not defined in "cues"' % (b['id'], cid))
                continue
            anc = (c.get('anchor') or {}).get(lang)
            if not anc:
                R.add('WARN', '%s: cue %r has no %s anchor phrase yet (needed before shot briefs)' % (b['id'], cid, lang))
            elif norm(anc) not in norm(x['text']):
                R.add('ERROR', '%s: cue %r anchor %r is not in the %s text of the beat' % (b['id'], cid, anc, lang))
        B.append(x)
    allcues = [c for b in beats for c in b.get('cue_ids', [])]
    dup = sorted({c for c in allcues if allcues.count(c) > 1})
    if dup:
        R.add('ERROR', 'cue_ids used in more than one beat: %s' % dup)
    if not B:
        return
    budget_total = sum(b.get('budget_sec') or 0 for b in beats)
    if budget_total and not rules['video_sec'][0] <= budget_total <= rules['video_sec'][1]:
        R.add('ERROR', 'time budgets add up to %.0f s; must be %d-%d s' % (budget_total, *rules['video_sec']))
    # 2. chapters in order: T, C1.., optional X
    order = []
    for b in B:
        if not order or order[-1] != b['chapter']:
            order.append(b['chapter'])
    if len(order) != len(set(order)):
        R.add('ERROR', 'chapters are interleaved: %s (each chapter must be one continuous block)' % '>'.join(order))
    kind = lambda c: chapters.get(c, {}).get('kind', 'chapter')
    story = [c for c in order if kind(c) == 'chapter']
    teaser = [b for b in B if kind(b['chapter']) == 'teaser']
    close = [b for b in B if kind(b['chapter']) == 'close']
    tsec = sum(b['sec'] for b in teaser)
    tlo, thi = rules['teaser_sec']
    R.row('teaser', '%.0f s' % tsec, '%d-%d s, first' % (tlo, thi), bool(teaser) and tlo <= tsec <= thi and order[0] == teaser[0]['chapter'])
    if not teaser:
        R.add('ERROR', 'no teaser chapter (kind "teaser"): open with a ~15 s cold open')
    elif not tlo <= tsec <= thi:
        R.add('ERROR', 'teaser is %.0f s; keep it %d-%d s (cut %d words)' % (tsec, tlo, thi, max(0, tsec - 15) / (tsec / max(1, sum(b['words'] for b in teaser)))))
    R.row('chapters', '%d story chapters' % len(story), '3', len(story) == 3)
    if len(story) != 3:
        R.add('ERROR', 'need exactly 3 story chapters (kind "chapter"), found %d: %s' % (len(story), story))
    clo, chi = rules['chapter_sec']
    for c in story:
        cb = [b for b in B if b['chapter'] == c]
        sec = sum(b['sec'] for b in cb)
        R.row('  ' + c, '%.0f s (%.1f min) %s-%s' % (sec, sec / 60, cb[0]['id'], cb[-1]['id']), '%.1f-%.1f min' % (clo / 60, chi / 60), clo <= sec <= chi)
        if not clo <= sec <= chi:
            R.add('ERROR', '%s is %.0f s; chapters must be %d-%d s' % (c, sec, clo, chi))
        ch_struct(R, c, cb, chapters, names, lang, rules, last=(c == story[-1]))
    if close:
        cs = sum(b['sec'] for b in close)
        if cs > rules['close_max_sec']:
            R.add('ERROR', 'close is %.0f s; max %d s' % (cs, rules['close_max_sec']))
    # 3. first stakes + hook
    hook0 = next((b for b in B if 'hook' in b['roles']), None)
    stakes = next((b for b in B if 'stakes' in b['roles']), None)
    R.row('hook', '%s at %.0f s' % (hook0['id'], hook0['start']) if hook0 else 'none', 'at 0 s', bool(hook0) and hook0['start'] < 1)
    if not hook0 or hook0['start'] >= 1:
        R.add('ERROR', 'the first beat must carry role "hook"')
    lim = rules['first_stakes_by_sec']
    R.row('first stakes', '%s at %.0f s' % (stakes['id'], stakes['start']) if stakes else 'none', '<= %d s' % lim, bool(stakes) and stakes['start'] <= lim)
    if not stakes or stakes['start'] > lim:
        R.add('ERROR', 'stakes (what can be lost, by whom) must be stated by %d s; mark that beat role "stakes"' % lim)
    # 4. re-hook gaps
    marks = [b['start'] for b in B if b['roles'] & set(rules['rehook_roles'])]
    pts = sorted(set([0.0] + marks + [total]))
    gaps = [(pts[i + 1] - pts[i], pts[i]) for i in range(len(pts) - 1)]
    g, at = max(gaps)
    R.row('max re-hook gap', '%.0f s (from %d:%02d)' % (g, at // 60, at % 60), '<= %d s' % rules['max_rehook_gap_sec'], g <= rules['max_rehook_gap_sec'])
    for g, at in gaps:
        if g > rules['max_rehook_gap_sec']:
            nxt = next((b['id'] for b in B if b['start'] > at + 60), '?')
            R.add('ERROR', 'no re-hook for %.0f s from %d:%02d; add a question/turn/reveal around %s (roles: %s)' % (g, at // 60, at % 60, nxt, ', '.join(rules['rehook_roles'])))
    # 5. climax / payoff / post-climax / recap
    climax = [b for b in B if 'climax' in b['roles']]
    if len(climax) != 1:
        R.add('ERROR', 'exactly one beat must carry role "climax" (found %d)' % len(climax))
    else:
        cx = climax[0]
        cend = cx['start'] + cx['sec']
        post = total - cend
        share = post / total
        R.row('climax', '%s at %d:%02d (%.0f%%)' % (cx['id'], cx['start'] // 60, cx['start'] % 60, 100 * cx['start'] / total), 'in last chapter', cx['chapter'] == (story[-1] if story else None))
        if story and cx['chapter'] != story[-1]:
            R.add('ERROR', 'the climax (%s) must be in the last chapter %s' % (cx['id'], story[-1]))
        pay = next((b for b in B if 'payoff' in b['roles'] and b['start'] >= cx['start']), None)
        pdelay = (pay['start'] - cend) if pay and pay is not cx else 0
        pok = pay is not None and pdelay <= rules['payoff_after_climax_sec']
        R.row('payoff after climax', ('%s +%.0f s' % (pay['id'], max(0, pdelay))) if pay else 'none', '<= %d s' % rules['payoff_after_climax_sec'], pok)
        if not pok:
            R.add('ERROR', 'the payoff (the answer / consequence) must land within %d s after the climax ends; mark it role "payoff"' % rules['payoff_after_climax_sec'])
        R.row('after climax', '%.0f s = %.0f%%' % (post, 100 * share), '<= %.0f%%' % (100 * rules['max_post_climax_share']), share <= rules['max_post_climax_share'])
        if share > rules['max_post_climax_share']:
            R.add('ERROR', '%.0f s (%.0f%%) after the climax; cut to <= %.0f s (merge payoff + recap, drop explanations)' % (post, 100 * share, rules['max_post_climax_share'] * total))
    for b in B:
        if 'recap' in b['roles'] and b['words'] > rules['max_recap_words']:
            R.add('ERROR', '%s: recap is %d words; max %d' % (b['id'], b['words'], rules['max_recap_words']))
    # 6. planted question
    pq = doc.get('planted_question') or {}
    pi, ai = pq.get('planted_in'), pq.get('answered_in')
    bid = {b['id']: b for b in B}
    pq_ok = pi in bid and ai in bid and len(story) == 3 and bid[pi]['chapter'] in (story[0], order[0]) and bid[ai]['chapter'] == story[-1]
    R.row('planted question', '%s -> %s' % (pi, ai), 'ch1 (or teaser) -> ch3', pq_ok)
    if not pq_ok:
        R.add('ERROR', 'planted_question must be planted in the teaser/chapter 1 and answered in chapter 3 (planted_in/answered_in beat ids)')
    # 7. closing question / next-episode tease only at the very end
    endc = [story[-1]] + [b['chapter'] for b in close] if story else []
    for b in B:
        r = b['roles'] & {'question', 'tease'}
        if r and b['chapter'] not in endc:
            R.add('ERROR', '%s: %s only in the last chapter bridge / close (found in %s)' % (b['id'], '/'.join(sorted(r)), b['chapter']))
    # 8. reels
    reels = sorted({b.get('reel') for b in B if b.get('reel')})
    rep = []
    for r in reels:
        rb = [b for b in B if b.get('reel') == r]
        sec = sum(b['sec'] for b in rb)
        ok = 'hook' in rb[0]['roles'] and any('payoff' in b['roles'] for b in rb) and any('bridge' in b['roles'] for b in rb[-2:])
        rep.append('%s %.1f min %s' % (r, sec / 60, 'ok' if ok else 'BROKEN'))
        if not ok:
            R.add('ERROR', 'reel %s cannot stand alone: needs hook in its first beat, a payoff beat and a bridge at the end' % r)
        if sec > rules['chapter_sec'][1] + rules['close_max_sec']:
            R.add('WARN', 'reel %s is %.0f s; reels should stay under ~3.5 min' % (r, sec))
        chs = [c for c in order if any(b['chapter'] == c for b in rb)]
        if any(kind(c) == 'teaser' for c in chs):
            R.add('ERROR', 'reel %s includes teaser beats; the teaser belongs to the full episode only (reel: null)' % r)
    R.row('reels', '; '.join(rep) or 'none', 'A, B, C stand alone', len(reels) == 3 and all(x.endswith('ok') for x in rep))
    if len(reels) != 3:
        R.add('ERROR', 'need 3 reels (A/B/C), one per story chapter; found %s' % reels)


def ch_struct(R, c, cb, chapters, names, lang, rules, last):
    first = cb[0]
    if 'hook' not in first['roles']:
        R.add('ERROR', '%s: first beat %s must be the chapter hook (role "hook"; its first line lands in the first %d s)' % (c, first['id'], rules['chapter_hook_within_sec']))
    elif first['sec'] > 25:
        R.add('WARN', '%s: hook beat %s is %.0f s; keep it a short punch (<= 25 s)' % (c, first['id'], first['sec']))
    for role in ('setup', 'payoff'):
        if not any(role in b['roles'] for b in cb):
            R.add('ERROR' if role == 'payoff' else 'WARN', '%s: no beat with role "%s"' % (c, role))
    if not any(b['roles'] & {'turn', 'climax'} for b in cb):
        R.add('ERROR', '%s: no turn (role "turn" or "climax")' % c)
    if 'bridge' not in cb[-1]['roles']:
        R.add('ERROR', '%s: last beat %s must be the bridge line (role "bridge")' % (c, cb[-1]['id']))
    reel = chapters.get(c, {}).get('reel')
    for b in cb:
        if reel and b.get('reel') != reel:
            R.add('ERROR', '%s: reel %r but chapter %s is reel %r' % (b['id'], b.get('reel'), c, reel))
    # names re-introduced inside the chapter before (or when) used
    seen = set()
    for b in cb:
        seen |= set(b.get('names_introduced', []))
        late = [w for w in b.get('characters', []) if w not in seen]
        if late:
            R.add('ERROR', '%s/%s: %s appear(s) before being introduced in this chapter (add to names_introduced with a one-line intro)' % (c, b['id'], ', '.join(late)))
            seen |= set(late)
        for nid in b.get('names_introduced', []):
            nm = (names.get(nid) or {}).get(lang)
            if not nm:
                R.add('WARN', '%s: name %r has no %s spelling in "names"' % (b['id'], nid, lang))
            elif norm(nm) not in norm(b['text']):
                R.add('ERROR', '%s: introduces %r but the %s text does not say %r' % (b['id'], nid, lang, nm))
    txt = ' '.join(b['text'] for b in cb).lower()
    for p in BACKREF.get(lang, []) + (BACKREF['en'] if lang != 'en' else []):
        if p in txt:
            R.add('ERROR', '%s: back-reference "%s" breaks the standalone reel; restate the fact in one line instead' % (c, p))


# ---------- output ----------
def print_report(R, head):
    print(head)
    w = max([len(r[0]) for r in R.rows] + [4])
    v = max([len(r[1]) for r in R.rows] + [5])
    for name, val, rule, st in R.rows:
        print('  %-*s  %-*s  %-30s %s' % (w, name, v, val, rule, st))
    errs = [m for l, m in R.issues if l == 'ERROR']
    warns = [m for l, m in R.issues if l == 'WARN']
    for m in errs:
        print('ERROR', m)
    for m in warns:
        print('WARN ', m)
    print('RESULT: %s (%d errors, %d warnings)' % ('PASS' if not errs else 'FAIL', len(errs), len(warns)))


def run(n, lang='hi', beats=None, estimate=False, quiet=False):
    epdir = os.path.join(ROOT, 'episodes', 'ep' + n)
    sp = script_path(epdir, lang)
    if not sp:
        sys.exit('no script for %s in %s (expected %s)' % (lang, epdir, ' or '.join(SCRIPT_NAMES.get(lang, ['script.%s.md' % lang]))))
    profile, rules = load_json(PROFILE), load_json(RULES)
    pace, psrc = pace_for(profile, lang)
    bp = beats or os.path.join(epdir, 'beats.json')
    doc = load_json(bp) if os.path.exists(bp) else None
    script = parse_script(sp)
    measured, tsrc = None, 'estimate %.3f s/word (%s)' % (pace, psrc)
    tp = timings_path(n, lang)
    if not estimate and os.path.exists(tp):
        tm = {b['beat']: b['duration'] for b in load_json(tp)}
        if set(tm) == {b['num'] for b in script}:
            measured, tsrc = tm, 'recorded %s' % os.path.relpath(tp, ROOT)
    R = check(script, doc, lang, pace, rules, measured, (profile.get(lang) or {}).get('beat_words'))
    if not quiet:
        print_report(R, 'EP%s script check [%s]  %s | beats: %s | timing: %s' % (
            n, lang, os.path.relpath(sp, ROOT), os.path.relpath(bp, ROOT) if doc else 'MISSING', tsrc))
    return R, doc


def anchors(n, lang, beats=None):
    bp = beats or os.path.join(ROOT, 'episodes', 'ep' + n, 'beats.json')
    doc = load_json(bp)
    out = {}
    for b in doc['beats']:
        for cid in b.get('cue_ids', []):
            out[cid] = {'beat': b['id'], 'word': ((doc.get('cues', {}).get(cid) or {}).get('anchor') or {}).get(lang)}
    print(json.dumps(out, ensure_ascii=False, indent=1))


def calibrate(n, lang):
    sp = script_path(os.path.join(ROOT, 'episodes', 'ep' + n), lang)
    tp = timings_path(n, lang)
    if not sp or not os.path.exists(tp):
        sys.exit('need the %s script and %s' % (lang, os.path.relpath(tp, ROOT)))
    words = sum(b['words'] for b in parse_script(sp))
    sec = sum(b['duration'] for b in load_json(tp))
    prof = load_json(PROFILE)
    p = prof.setdefault(lang, {})
    ms = [m for m in p.get('measurements', []) if m.get('ep') != n] + [{'ep': n, 'script_words': words, 'sec': round(sec, 1), 'sec_per_word': round(sec / words, 3)}]
    p['measurements'] = ms
    p['sec_per_word'] = round(sum(m['sec'] for m in ms) / sum(m['script_words'] for m in ms), 3)
    p['source'] = 'measured from %d recording(s): %s' % (len(ms), ', '.join('EP%s %.3f' % (m['ep'], m['sec_per_word']) for m in ms))
    with open(PROFILE, 'w', encoding='utf-8') as f:
        json.dump(prof, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('%s pace: EP%s %d words / %.1f s = %.3f s/word -> profile %.3f s/word' % (lang, n, words, sec, sec / words, p['sec_per_word']))


# ---------- self test ----------
def _synthetic(pace):
    """A well-formed 3-chapter episode: should pass with 0 errors."""
    plan = [  # id, chapter, roles, seconds, characters, names_introduced, cue
        ('T', ['hook', 'stakes', 'plant'], 15, ['brahma'], ['brahma'], 'pillar_glow'),
        ('C1', ['hook'], 10, ['brahma', 'vishnu'], ['brahma', 'vishnu'], None),
        ('C1', ['setup'], 36, ['brahma', 'vishnu'], [], None),
        ('C1', ['rehook'], 13, ['brahma'], [], None),
        ('C1', ['setup'], 36, ['vishnu'], [], None),
        ('C1', ['turn'], 14, ['brahma'], [], 'pillar_appears'),
        ('C1', ['payoff'], 36, ['brahma', 'vishnu'], [], None),
        ('C1', ['bridge'], 14, ['brahma'], [], None),
        ('C2', ['hook'], 10, ['brahma'], ['brahma'], None),
        ('C2', ['setup'], 36, ['brahma'], [], 'flower_falls'),
        ('C2', ['rehook'], 13, ['brahma'], [], None),
        ('C2', ['setup'], 36, ['brahma'], [], None),
        ('C2', ['turn'], 14, ['brahma'], [], None),
        ('C2', ['payoff'], 36, ['brahma', 'vishnu'], ['vishnu'], None),
        ('C2', ['bridge'], 14, ['brahma'], [], None),
        ('C3', ['hook'], 10, ['brahma', 'shiva'], ['brahma', 'shiva'], None),
        ('C3', ['setup'], 36, ['brahma'], [], None),
        ('C3', ['rehook'], 13, ['shiva'], [], None),
        ('C3', ['turn'], 36, ['shiva'], [], None),
        ('C3', ['climax'], 22, ['shiva', 'brahma'], [], 'shiva_verdict'),
        ('C3', ['payoff', 'answer'], 26, ['brahma'], [], None),
        ('C3', ['recap', 'bridge', 'question', 'tease'], 14, ['brahma'], [], None),
    ]
    names = {'brahma': {'hi': 'ब्रह्मा', 'en': 'Brahma'}, 'vishnu': {'hi': 'विष्णु', 'en': 'Vishnu'}, 'shiva': {'hi': 'शिव', 'en': 'Shiva'}}
    beats, lines = [], ['# test', '']
    cues = {}
    for i, (ch, roles, sec, chars, intro, cue) in enumerate(plan, 1):
        bid = 'B%02d' % i
        words = max(1, round(sec / pace))
        text = ' '.join(names[x]['hi'] for x in intro)
        if cue:
            cues[cue] = {'meaning': cue, 'anchor': {'hi': 'संकेत%d' % i}}
            text += ' संकेत%d' % i
        text = (text + ' ' + ' '.join(['कथा'] * (words - count_words(text)))).strip()
        beats.append({'id': bid, 'chapter': ch, 'reel': {'T': None}.get(ch, {'C1': 'A', 'C2': 'B', 'C3': 'C'}.get(ch)), 'intent': 'x',
                      'roles': roles, 'budget_sec': sec, 'emotion': {'hi': 'शांत'}, 'cue_ids': [cue] if cue else [],
                      'characters': chars, 'names_introduced': intro})
        lines += ['**%s** [शांत]' % bid, text, '']
    doc = {'episode': '99', 'languages': ['hi'], 'names': names, 'cues': cues,
           'planted_question': {'text': 'q', 'planted_in': 'B01', 'answered_in': 'B21'},
           'chapters': [{'id': 'T', 'kind': 'teaser'}, {'id': 'C1', 'reel': 'A'}, {'id': 'C2', 'reel': 'B'}, {'id': 'C3', 'reel': 'C'}],
           'beats': beats}
    return doc, '\n'.join(lines)


def selftest():
    rules, prof = load_json(RULES), load_json(PROFILE)
    pace = prof['hi']['sec_per_word']
    fails = 0

    def expect(name, cond):
        nonlocal fails
        print(('ok   ' if cond else 'FAIL ') + name)
        fails += not cond
    doc, text = _synthetic(pace)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'script.md')
        open(p, 'w', encoding='utf-8').write(text)
        R = check(parse_script(p), doc, 'hi', pace, rules)
        expect('synthetic good episode passes (%s)' % (R.errors[:2] or 'no errors'), not R.errors)
        # break it: back-reference + late name + long recap + tease in ch1
        doc['beats'][3]['characters'] = ['shiva']
        doc['beats'][7]['roles'].append('tease')
        open(p, 'w', encoding='utf-8').write(text.replace('**B10** [शांत]\n', '**B10** [शांत]\nजैसा हमने देखा '))
        R = check(parse_script(p), doc, 'hi', pace, rules)
        e = ' | '.join(R.errors)
        expect('catches back-reference', 'back-reference' in e)
        expect('catches name not re-introduced', 'before being introduced' in e)
        expect('catches tease outside last chapter', 'tease only' in e)
        R = check(parse_script(p), None, 'hi', pace, rules)
        expect('legacy mode (no beats.json) never errors', not R.errors)
    # the EP06 analysis file must flag the known problems
    ex = os.path.join(ROOT, 'library', 'examples', 'ep06_beats_example.json')
    s6 = os.path.join(ROOT, 'episodes', 'ep06', 'script.md')
    if os.path.exists(ex) and os.path.exists(s6):
        tm = {b['beat']: b['duration'] for b in load_json(os.path.join(ROOT, 'build', 'ep06', 'timings.json'))} if os.path.exists(os.path.join(ROOT, 'build', 'ep06', 'timings.json')) else None
        R = check(parse_script(s6), load_json(ex), 'hi', pace, rules, tm)
        e = ' | '.join(R.errors)
        for k in ('after the climax', 'recap is', 'pace is flat', 'before being introduced'):
            expect('EP06 example flags "%s"' % k, k in e)
    print('selftest:', 'PASS' if not fails else '%d FAILED' % fails)
    return fails


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('n', nargs='?')
    ap.add_argument('--lang', default='hi')
    ap.add_argument('--beats', help='beats.json to use instead of episodes/epNN/beats.json')
    ap.add_argument('--estimate', action='store_true', help='ignore recorded timings')
    ap.add_argument('--anchors', metavar='LANG')
    ap.add_argument('--calibrate', action='store_true')
    ap.add_argument('--strict', action='store_true', help='exit 1 on warnings-only legacy failures too')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return 1 if selftest() else 0
    if not a.n:
        ap.error('episode number required')
    n = a.n.zfill(2)
    if a.calibrate:
        return calibrate(n, a.lang) or 0
    if a.anchors:
        return anchors(n, a.anchors, a.beats) or 0
    R, doc = run(n, a.lang, a.beats, a.estimate)
    if R.errors:
        return 1
    if a.strict and any(r[3] != 'ok' for r in R.rows):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
