#!/usr/bin/env python3
"""EP06 offline sound renderer: cues.json -> stems/*.wav (numpy + scipy + soundfile only).

Run (2 cores max, low priority):
    nice -n 19 taskset -c 0,1 /tmp/esenv/bin/python episodes/ep06/sound/render_sound.py
Options:  --only bed,motif,pulse,ambience,sfx   render some stems only
          --cues PATH                            alternative cue sheet

Stems (32 kHz stereo 16-bit, all ducked under the REAL voice envelope, 484 s long):
  bed.wav motif.wav pulse.wav ambience.wav sfx.wav
Everything is procedural (no samples, no network). It reads voiceovers/ep06_voice.mp3
(read only) to build the speech envelope used for ducking.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, shutil, argparse, subprocess, traceback
import numpy as np
from scipy import signal
from scipy.ndimage import maximum_filter1d, minimum_filter1d
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
VOICE = os.path.join(ROOT, "voiceovers", "ep06_voice.mp3")
SR = 32000
TOTAL = 484.0
N = int(TOTAL * SR)
rng = np.random.default_rng(606)

KEYS = {"C": 0, "C#": 1, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}
MODES = {
    "bhairav": [0, 1, 4, 5, 7, 8, 11], "yaman": [0, 2, 4, 6, 7, 9, 11], "marwa": [0, 1, 4, 6, 7, 9, 11],
    "malkauns": [0, 3, 5, 8, 10], "todi": [0, 1, 3, 6, 7, 8, 11], "darbari": [0, 2, 3, 5, 7, 8, 10],
    "bhairavi": [0, 1, 3, 5, 7, 8, 10], "minor": [0, 2, 3, 5, 7, 8, 10], "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10], "lydian": [0, 2, 4, 6, 7, 9, 11], "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
}

# ---------------------------------------------------------------- basics
def db(x): return 10.0 ** (x / 20.0)
def nsamp(s): return max(1, int(round(s * SR)))
def ix(t): return max(0, int(round(t * SR)))
def tt(n): return np.arange(n) / SR
def white(n): return rng.standard_normal(n)
def g(x, c, w): return math.exp(-((x - c) / w) ** 2)

def n_peak(x):
    m = np.max(np.abs(x)) if len(x) else 0.0
    return x / m if m > 1e-12 else x
def n_rms(x):
    r = math.sqrt(float(np.mean(x * x))) if len(x) else 0.0
    return x / r if r > 1e-12 else x

def deg_freq(deg, mode="bhairav", key="C", octave=3, transpose=0):
    sc = MODES.get(mode, MODES["minor"])
    octs, idx = divmod(int(deg) - 1, len(sc))
    midi = 12 * (octave + 1) + KEYS.get(key, 0) + sc[idx] + 12 * octs + transpose
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)

def _sos(kind, fc, order):
    nyq = SR / 2.0
    if kind == "band":
        lo, hi = max(fc[0], 20.0), min(fc[1], nyq * 0.95)
        if hi <= lo * 1.05:
            hi = lo * 1.5
        return signal.butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.butter(order, min(max(fc, 20.0), nyq * 0.95), btype=kind, fs=SR, output="sos")
def lp(x, fc, order=2): return signal.sosfilt(_sos("low", fc, order), x)
def hp(x, fc, order=2): return signal.sosfilt(_sos("high", fc, order), x)
def bp(x, lo, hi, order=2): return signal.sosfilt(_sos("band", (lo, hi), order), x)

def smooth_noise(n, rate):
    x = lp(white(n), rate, 2)
    s = np.std(x)
    return x / s if s > 1e-12 else x

def ramp_up(k): return 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, max(k, 1)))
def apply_fades(x, fi, fo):
    n = len(x)
    if fi and fi > 0:
        k = min(n, nsamp(fi)); x[:k] *= ramp_up(k)
    if fo and fo > 0:
        k = min(n, nsamp(fo)); x[n - k:] *= ramp_up(k)[::-1]
    return x

def place(buf, t, note):
    i = ix(t)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(note))
    buf[i:j] += note[:j - i]

def sustain_env(dur, a, r):
    nd, nr = nsamp(dur), nsamp(r)
    e = np.ones(nd + nr)
    na = min(nsamp(a), nd)
    e[:na] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, na))
    e[nd:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, nr))
    return e

# ---------------------------------------------------------------- reverb / stereo
_IR = {}
def _make_ir(sec, seed):
    r = np.random.default_rng(seed)
    n = nsamp(sec); t = np.arange(n) / SR
    ir = r.standard_normal(n) * np.exp(-6.9 * t / sec)
    ir = lp(ir, 5500, 1) * np.minimum(1.0, t / 0.012)
    return ir / math.sqrt(float(np.sum(ir ** 2)))
def get_ir(kind):
    if kind not in _IR:
        sec = {"short": 1.4, "long": 3.2, "huge": 5.0}[kind]
        _IR[kind] = (_make_ir(sec, 11), _make_ir(sec, 23))
    return _IR[kind]
def spatial(x, wet, kind, pan=0.0):
    th = (pan + 1.0) * math.pi / 4.0
    dl, dr = math.cos(th), math.sin(th)
    if wet <= 0:
        return np.stack([x * dl, x * dr], axis=1)
    il, ir = get_ir(kind)
    yl = signal.fftconvolve(x, il); yr = signal.fftconvolve(x, ir)
    out = np.zeros((len(yl), 2))
    out[:len(x), 0] += x * dl; out[:len(x), 1] += x * dr
    out[:, 0] += wet * yl; out[:, 1] += wet * yr
    return out

# ---------------------------------------------------------------- instruments
def amps_pow(nh, p): return [k ** -p for k in range(1, nh + 1)]
def formant_amps(f, form, nh=24, p=0.7, floor=0.1):
    return [(k ** -p) * (sum(w * g(k * f, c, bw) for c, bw, w in form) + floor) for k in range(1, nh + 1)]

def sin_h(f, n, amps, cents=(0,), vib=None):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for c in cents:
        fc = f * 2.0 ** (c / 1200.0)
        ph = 2 * np.pi * fc * t
        if vib:
            ph = ph - (fc * vib[1] / vib[0]) * np.cos(2 * np.pi * vib[0] * t + rng.uniform(0, 6.283))
        p0 = rng.uniform(0, 6.283)
        for k, a in enumerate(amps, 1):
            if a <= 1e-4 or fc * k > SR * 0.45:
                continue
            out += a * np.sin(k * ph + p0)
    return out / len(cents)

ALIAS = {"strings ensemble": "pad", "string pad": "pad", "synth pad": "pad", "strings": "pad", "pad": "pad",
         "tremolo strings": "trem", "organ": "organ", "choir aahs": "choir", "choir": "choir", "voice oohs": "oohs",
         "french horn": "horn", "horn": "horn", "brass section": "brass", "brass": "brass", "trombone": "brass",
         "tuba": "tuba", "cello": "cello", "violin": "violin", "contrabass": "bass", "flute": "flute",
         "bansuri": "flute", "pan flute": "flute", "sub": "sub"}
VP = {"pad": (0.9, 1.4, (-9, 0, 8), (0.3, 0.002)), "trem": (0.4, 0.8, (-6, 5), None), "organ": (0.08, 0.5, (0,), None),
      "choir": (0.8, 1.2, (-12, 0, 10), (5.2, 0.004)), "oohs": (0.8, 1.2, (-12, 0, 10), (5.0, 0.004)),
      "horn": (0.25, 0.5, (-4, 4), (5.0, 0.002)), "brass": (0.18, 0.4, (-5, 5), None), "tuba": (0.3, 0.5, (-3, 3), None),
      "cello": (0.15, 0.35, (-3, 3), (5.3, 0.005)), "violin": (0.12, 0.3, (-4, 4), (5.8, 0.006)),
      "bass": (0.2, 0.4, (0,), None), "flute": (0.1, 0.25, (0,), (5.0, 0.004)), "sub": (0.3, 0.6, (0,), None)}

def voice_note(inst, f, dur):
    k = ALIAS.get(inst.lower(), "pad")
    a, r, cents, vib = VP[k]
    env = sustain_env(dur, a, r)
    n = len(env)
    if k == "pad": amps = amps_pow(10, 1.1)
    elif k == "trem": amps = amps_pow(12, 0.8)
    elif k == "organ": amps = [1, .55, .45, .3, 0, .2, 0, .15]
    elif k == "choir": amps = formant_amps(f, [(700, 200, 1.0), (1150, 250, 0.6)])
    elif k == "oohs": amps = formant_amps(f, [(350, 120, 1.0), (800, 180, 0.4)])
    elif k == "horn": amps = [kk ** -1.2 * math.exp(-kk * f / 4500) for kk in range(1, 15)]
    elif k == "brass": amps = [kk ** -1.0 * math.exp(-kk * f / 6500) for kk in range(1, 15)]
    elif k == "tuba": amps = [kk ** -1.3 * math.exp(-kk * f / 2500) for kk in range(1, 12)]
    elif k in ("cello", "bass"): amps = [kk ** -1.0 * math.exp(-kk * f / 4000) for kk in range(1, 15)]
    elif k == "violin": amps = [kk ** -1.0 * math.exp(-kk * f / 6000) for kk in range(1, 12)]
    elif k == "flute": amps = [1, .12, .05, .02]
    else: amps = [1, .25]
    body = sin_h(f, n, amps, cents, vib) * env
    if k == "trem":
        body *= 0.65 + 0.35 * np.sin(2 * np.pi * 8.5 * tt(n))
    if k == "flute":
        body += n_rms(bp(white(n), f * 2, f * 6)) * 0.03 * env
    return n_peak(body)

PLUCK_P = {"santoor": (1.5, 0.9, 14, 6, 0), "harp": (2.0, 1.2, 10, 0, 0), "veena": (1.2, 0.7, 16, 0, 0),
           "sitar": (1.1, 0.6, 18, 0, 1), "pizzicato": (0.16, 1.0, 10, 0, 0), "pizz": (0.16, 1.0, 10, 0, 0),
           "celesta": (1.4, 1.5, 6, 0, 0), "ektara": (0.8, 0.5, 18, 0, 1)}
_PLC = {}
def pluck_note(inst, f):
    key = (inst, round(f, 1))
    if key in _PLC:
        return _PLC[key]
    tau, p, nh, chor, buzz = PLUCK_P[inst]
    n = nsamp(min(tau * 4.5, 6.0)); t = tt(n); out = np.zeros(n)
    for c in ((-chor, chor) if chor else (0,)):
        fc = f * 2.0 ** (c / 1200.0)
        for k in range(1, nh + 1):
            if fc * k > SR * 0.45:
                break
            a = k ** -p * (1.8 if (buzz and 6 <= k <= 10) else 1.0)
            dk = tau / (1 + 0.45 * (k - 1))
            out += a * np.sin(2 * np.pi * fc * k * (1 + 0.0004 * k * k) * t + rng.uniform(0, 6.283)) * np.exp(-t / dk)
    if inst == "celesta":
        out += 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / 0.5)
    out += 0.2 * bp(white(n), 1500, 6000) * np.exp(-t / 0.004)
    out *= np.minimum(1.0, t / 0.002)
    _PLC[key] = n_peak(out)
    return _PLC[key]

BELL_P = {"glass": ([1, 2.76, 5.4, 8.93], [1, .5, .3, .2], [2.0, 1.2, .8, .5]),
          "temple": ([0.5, 1, 2.0, 2.51, 3.5, 4.1, 5.8], [.5, 1, .7, .5, .4, .3, .2], [3.5, 4, 3, 2.6, 1.8, 1.4, 1.0]),
          "gong": ([1, 1.47, 2.09, 2.56, 3.41, 4.2], [1, .8, .7, .5, .4, .3], [6, 5, 4, 3, 2.5, 2])}
def bell_note(f, kind, dur=None):
    r, a, tau = BELL_P[kind]
    n = nsamp(dur or max(tau) * 3.2); t = tt(n); out = np.zeros(n)
    for ri, ai, ti in zip(r, a, tau):
        fr = f * ri
        if fr < SR * 0.45:
            out += ai * np.sin(2 * np.pi * fr * t + rng.uniform(0, 6.283)) * np.exp(-t / ti)
    return n_peak(out * np.minimum(1.0, t / 0.002))

def make_note(inst, f, ln):
    k = inst.lower()
    if k in PLUCK_P: return pluck_note(k, f)
    if k in ("glockenspiel", "tinkle bell", "glass bell"): return bell_note(f, "glass", 2.5)
    if k in ("tubular bells", "temple bell", "bell"): return bell_note(f, "temple", 6.0)
    return voice_note(k, f, ln)

_TP = {}
def _jivari(f):
    key = round(f, 1)
    if key in _TP:
        return _TP[key]
    n = nsamp(7.0); t = tt(n); out = np.zeros(n)
    for k in range(1, 22):
        if f * k > SR * 0.45:
            break
        a = k ** -0.45 * (1 + 0.8 * math.exp(-((k - 9) / 3.0) ** 2))
        out += a * np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6.283)) * np.exp(-t / (3.0 / (1 + 0.12 * (k - 1))))
    out *= np.minimum(1.0, t / 0.004)
    _TP[key] = n_peak(out)
    return _TP[key]
def tanpura(f, dur):
    buf = np.zeros(nsamp(dur)); cyc = 3.4; t0 = 0.0
    while t0 < dur:
        for o, m in ((0, 0.75), (0.85, 1.0), (1.7, 1.0), (2.55, 0.5)):
            if t0 + o < dur:
                place(buf, t0 + o, _jivari(f * m))
        t0 += cyc
    return buf

_DR = {}
def drum(f0, tau, click, drop=1.5, noise_f=700):
    key = (round(f0, 1), tau, click, drop)
    if key in _DR:
        return _DR[key]
    n = nsamp(tau * 5); t = tt(n)
    fr = f0 * (1 + (drop - 1) * np.exp(-t / 0.035))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    body = np.sin(ph) * np.exp(-t / tau) + 0.3 * np.sin(2 * ph) * np.exp(-t / (tau * 0.4))
    cl = lp(white(n), noise_f * 3) * np.exp(-t / 0.012) * click
    _DR[key] = n_peak(body + cl)
    return _DR[key]

# ---------------------------------------------------------------- role generators
def gen_bed(c, dur):
    inst = c.get("instrument", "pad").lower(); mode = c.get("mode", "bhairav"); key = c.get("key", "C")
    octv = c.get("octave", 3)
    if inst == "tanpura":
        return tanpura(deg_freq(1, mode, key, octv), dur)
    voicing = c.get("voicing", [[1, 5]]); S = len(voicing); seg = dur / S; ov = min(1.2, seg * 0.5)
    buf = np.zeros(nsamp(dur))
    for i, ch in enumerate(voicing):
        st = max(0.0, i * seg - (ov * 0.5 if i > 0 else 0.0))
        ln = seg + (ov if i < S - 1 else 0.0)
        for d in ch:
            place(buf, st, make_note(inst, deg_freq(d, mode, key, octv), ln))
    return buf

def gen_motif(c, dur):
    inst = c.get("instrument", "flute"); mode = c.get("mode", "bhairav"); key = c.get("key", "C")
    degs = c["degrees"]; rh = c.get("rhythm", [1] * len(degs)); bpm = c.get("bpm", 60); octv = c.get("octave", 3)
    beat = 60.0 / bpm; reps = c.get("repeat", 1); gap = c.get("repeat_gap", 2) * beat
    ev = []; pos = 0.0
    for r in range(reps):
        for d, rt in zip(degs, rh):
            ev.append((pos, d, rt * beat)); pos += rt * beat
        if r < reps - 1:
            pos += gap
    buf = np.zeros(nsamp(pos + 4.0))
    for p, d, ln in ev:
        place(buf, p, make_note(inst, deg_freq(d, mode, key, octv, c.get("transpose", 0)), ln * 0.97))
    return buf

def gen_ostinato(c, dur):
    inst = c.get("instrument", "cello"); mode = c.get("mode", "phrygian"); key = c.get("key", "C")
    degs = c["degrees"]; bpm = c.get("bpm", 96); step = 60.0 / bpm / c.get("subdiv", 2); octv = c.get("octave", 3)
    buf = np.zeros(nsamp(dur) + nsamp(2.0)); t = 0.0; i = 0
    while t < dur:
        d = degs[i % len(degs)]
        acc = 1.0 if i % len(degs) == 0 else 0.7
        place(buf, t, make_note(inst, deg_freq(d, mode, key, octv), step * 0.9) * acc)
        t += step; i += 1
    return buf[:nsamp(dur)]

def gen_pulse(c, dur):
    inst = c.get("instrument", "timpani").lower(); bpm = c.get("bpm", 72); pat = c.get("pattern", "heartbeat")
    beat = 60.0 / bpm
    if "taiko" in inst: hit = drum(78, 0.5, 0.55, 1.7, 900)
    elif "dhol" in inst: hit = drum(140, 0.2, 0.9, 1.3, 2500)
    else: hit = drum(deg_freq(1, "minor", c.get("key", "C"), 2), 0.38, 0.18, 1.35, 700)
    nb = int(dur / beat) + 2; ev = []
    if pat == "heartbeat":
        for i in range(nb): ev += [(i * beat, 1.0), (i * beat + 0.33 * beat, 0.62)]
    elif pat == "march":
        acc = [1, 0.55, 0.8, 0.55]
        for i in range(nb): ev.append((i * beat, acc[i % 4]))
    elif pat == "gallop":
        for i in range(nb): ev += [(i * beat, 1.0), (i * beat + 0.5 * beat, 0.55), (i * beat + 0.75 * beat, 0.75)]
    elif pat == "roll":
        step = beat / 4; m = int(dur / step) + 1
        for i in range(m): ev.append((i * step, 0.3 + 0.7 * i / max(1, m)))
    elif pat == "syncopated":
        for bar in range(nb // 4 + 1):
            for off, v in ((0, 1.0), (0.75, 0.6), (1.5, 0.8), (2.5, 0.6), (3.25, 0.7)):
                ev.append(((bar * 4 + off) * beat, v))
    else:
        ev = [(i * beat, 1.0) for i in range(nb)]
    buf = np.zeros(nsamp(dur) + nsamp(2.0))
    for tp, v in ev:
        if tp >= dur:
            break
        place(buf, max(0.0, tp + float(rng.normal(0, 0.004))), hit * v * rng.uniform(0.9, 1.05))
    return buf[:nsamp(dur)]

def gen_riser(c, dur):
    n = nsamp(dur); t = tt(n); u = t / dur
    f0 = deg_freq(1, "minor", c.get("key", "C"), c.get("octave", 2))
    tone = np.zeros(n)
    for ratio, a in ((1, 1.0), (1.5, 0.7), (2.0, 0.6), (3.0, 0.35), (4.03, 0.2)):
        fr = f0 * ratio * (4.0 ** u)
        tone += a * np.sin(2 * np.pi * np.cumsum(fr) / SR) * (0.4 + 0.6 * u)
    nz = white(n)
    noise = bp(nz, 200, 1000) * u ** 1.2 + 0.7 * bp(nz, 1000, 4000) * u ** 2.2 + 0.5 * hp(nz, 4000) * u ** 3.2
    out = (0.6 * n_peak(tone) + 1.0 * n_peak(noise)) * u ** 2.0
    return apply_fades(n_peak(out), 0.0, 0.05)

# ---- ambience
def amb_fire(dur, inten=5):
    n = nsamp(dur)
    roar = n_rms(lp(white(n), 420)) * (0.75 + 0.25 * np.tanh(smooth_noise(n, 0.8)))
    imp = (rng.random(n) < (8 + inten * 3.0) / SR) * (rng.exponential(1.0, n) ** 1.5)
    kt = tt(nsamp(0.01)); kern = white(len(kt)) * np.exp(-kt / 0.002)
    crack = n_rms(bp(signal.fftconvolve(imp, kern)[:n], 1200, 7000))
    flut = n_rms(bp(white(n), 60, 220)) * (0.75 + 0.25 * np.tanh(smooth_noise(n, 2.0)))
    return 0.9 * roar + 0.5 * crack + 0.5 * flut
def amb_wind(dur, inten=5):
    n = nsamp(dur)
    a = n_rms(bp(white(n), 150, 900)) * (0.55 + 0.45 * np.tanh(smooth_noise(n, 0.15)))
    b = n_rms(bp(white(n), 500, 1600, 3)) * (0.45 + 0.45 * np.tanh(smooth_noise(n, 0.3)))
    return a + 0.35 * b
def amb_cosmic(dur, inten=5):
    n = nsamp(dur); t = tt(n); out = np.zeros(n)
    for f, a, r in ((65.4, 1, 0.07), (98.1, 0.7, 0.05), (130.8, 0.5, 0.09), (196.2, 0.3, 0.06)):
        out += a * np.sin(2 * np.pi * f * t + 0.8 * np.sin(2 * np.pi * r * t))
    for _ in range(8):
        am = 0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(0.05, 0.3) * t + rng.uniform(0, 6.283))
        out += 0.06 * np.sin(2 * np.pi * rng.uniform(900, 3500) * t + rng.uniform(0, 6.283)) * am
    return out + 0.1 * n_rms(bp(white(n), 200, 1200))
def amb_flood(dur, inten=5):
    n = nsamp(dur); t = tt(n)
    sw = 0.45 + 0.55 * np.sin(2 * np.pi * 0.13 * t) ** 2
    return n_rms(lp(white(n), 600)) * sw + 0.25 * n_rms(hp(white(n), 2500)) * sw ** 2
AMB = {"fire": amb_fire, "wind": amb_wind, "cosmic_hum": amb_cosmic, "flood": amb_flood, "sea": amb_flood}

def gen_ambience(c, dur):
    return AMB[c.get("sfx", "wind")](dur, c.get("intensity", 5))

# ---- hits and sfx (peak normalised, tail = to - from)
def g_boom(c, dur):
    tail = max(dur, 1.0); n = nsamp(tail); t = tt(n)
    sub = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t / 0.08)) / SR) * np.exp(-t / (tail / 3.5))
    thud = lp(white(n), 180) * np.exp(-t / 0.12) * 0.6
    return n_peak((sub + thud) * np.minimum(1.0, t / 0.003))

def g_braam(c, dur, tail_override=None):
    tail = tail_override or max(dur, 0.8); n = nsamp(tail + 0.2); t = tt(n)
    key = c.get("key", "C"); mode = c.get("mode", "phrygian"); degs = c.get("degrees", [1, 2, 5]); o0 = c.get("octave", 1)
    out = np.zeros(n)
    for i, d in enumerate(degs):
        f = deg_freq(d, mode, key, o0 + (1 if i == 2 else 0))
        for cents in (-14, 0, 13):
            ft = f * 2.0 ** (cents / 1200.0) * (1 - 0.03 * (1 - np.exp(-t / 0.6)))
            ph = 2 * np.pi * np.cumsum(ft) / SR
            for k in range(1, 10):
                out += (k ** -1.0) * np.sin(k * ph)
    out = lp(out, 2200) * np.minimum(1.0, t / 0.05) * np.exp(-t / (tail / 2.8))
    boom = np.sin(2 * np.pi * np.cumsum(40 + 50 * np.exp(-t / 0.1)) / SR) * np.exp(-t / (tail / 3.0))
    return n_peak(0.8 * n_peak(out) + 0.7 * boom)

def g_stab(c, dur):
    cc = dict(c); cc.setdefault("degrees", [1, 5]); cc["octave"] = c.get("octave", 2)
    return g_braam(cc, dur, 0.6)

def g_taiko(c, dur):
    n = nsamp(max(dur, 1.0)); out = np.zeros(n)
    place(out, 0.0, drum(75, 0.55, 0.55, 1.8, 900))
    place(out, 0.0, g_boom(c, 1.0) * 0.6)
    return n_peak(out)

def g_gong(c, dur):
    tail = max(dur, 3.0); n = nsamp(tail); t = tt(n)
    b = bell_note(110.0, "gong", tail)[:n]
    sw = n_rms(bp(white(n), 800, 3000)) * np.minimum(1.0, t / 0.4) * np.exp(-t / 1.5) * 0.3
    crash = n_rms(lp(white(n), 2000)) * np.exp(-t / 0.08) * 0.4
    out = np.zeros(n); out[:len(b)] += b
    return n_peak(out + sw + crash)

def g_bell(c, dur):
    f = deg_freq(c.get("degree", 5), c.get("mode", "bhairav"), c.get("key", "C"), 4)
    return bell_note(f, "temple", max(dur, 2.0))
def g_glass(c, dur):
    f = deg_freq(c.get("degree", 5), "marwa", c.get("key", "C"), 5)
    return bell_note(f, "glass", max(dur, 1.2))

def g_skull(c, dur):
    n = nsamp(max(dur, 0.8)); out = np.zeros(n)
    for i in range(6):
        k = nsamp(0.08); tk = tt(k)
        kn = np.sin(2 * np.pi * rng.uniform(500, 900) * tk) * np.exp(-tk / 0.012) + bp(white(k), 800, 3500) * np.exp(-tk / 0.008)
        place(out, rng.uniform(0, 0.4) * (i / 5 + 0.3), kn * rng.uniform(0.4, 1.0))
    thud = lp(white(n), 160) * np.exp(-tt(n) / 0.15) * 0.8
    return n_peak(out + thud)

def g_glass_snap(c, dur):
    n = nsamp(max(dur, 1.0)); t = tt(n)
    click = hp(white(n), 3000) * np.exp(-t / 0.004)
    ring = (np.sin(2 * np.pi * 3100 * t) + 0.6 * np.sin(2 * np.pi * 4900 * t)) * np.exp(-t / 0.25)
    return n_peak(n_peak(click) * 0.9 + n_peak(ring) * 0.5)

def g_sparkle(c, dur):
    n = nsamp(max(dur, 1.0)); out = np.zeros(n)
    for i in range(7):
        f = deg_freq([1, 3, 5, 6, 7, 5, 3][i], "marwa", c.get("key", "C"), 6)
        place(out, dur * 0.8 * i / 7, bell_note(f, "glass", 0.8) * (0.9 ** i))
    return n_peak(out)

def g_petal(c, dur):
    n = nsamp(dur); out = np.zeros(n); degs = [5, 4, 3, 2, 1, 2, 1]; cnt = max(3, int(dur * 1.6))
    for i in range(cnt):
        f = deg_freq(degs[i % len(degs)], "marwa", c.get("key", "C"), 5)
        place(out, dur * 0.9 * (i / cnt) ** 0.85, pluck_note("celesta", f) * (0.9 ** i if i < 8 else 0.4))
    air = n_rms(bp(white(n), 2500, 6500)) * np.sin(np.pi * np.linspace(0, 1, n)) ** 2 * 0.05 * max(np.max(np.abs(out)), 1e-6)
    return n_peak(out + air)

def g_wings(c, dur):
    n = nsamp(dur); t = tt(n); rate = c.get("rate", 2.3)
    ph = np.cumsum(rate * (1 + 0.15 * np.sin(2 * np.pi * 0.2 * t))) / SR
    env = (0.5 - 0.5 * np.cos(2 * np.pi * ph)) ** 2.5
    nz = n_rms(bp(white(n), 250, 2200)); air = n_rms(lp(white(n), 400)) * 0.4
    flutter = n_rms(bp(white(n), 3000, 6000)) * 0.15 * env
    out = nz * env + air * (0.3 + 0.7 * env) + 0.3 * np.sin(2 * np.pi * 95 * t) * env + flutter
    return n_peak(out)

def g_crack(c, dur):
    tail = max(dur, 2.5); n = nsamp(tail); t = tt(n)
    click = hp(white(n), 1200) * np.exp(-t / 0.025)
    body = lp(white(n), 1100) * np.exp(-t / 0.4)
    sub = np.sin(2 * np.pi * np.cumsum(28 + 95 * np.exp(-t / 0.09)) / SR) * np.exp(-t / 1.0)
    imp = (rng.random(n) < 60 * np.exp(-t / 0.9) / SR) * rng.standard_normal(n)
    kt = tt(nsamp(0.008))
    spl = bp(signal.fftconvolve(imp, white(len(kt)) * np.exp(-kt / 0.0018))[:n], 1500, 8000)
    groan = bp(white(n), 90, 300) * np.exp(-t / 1.2) * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t))
    out = n_peak(click) + 0.9 * n_peak(body) + 1.1 * n_peak(sub) + 0.6 * n_peak(spl) + 0.4 * n_peak(groan)
    return n_peak(out * np.minimum(1.0, t / 0.001))

def g_trident(c, dur):
    tail = max(dur, 3.0); n = nsamp(tail); t = tt(n)
    click = hp(white(n), 2000) * np.exp(-t / 0.006)
    stone = lp(white(n), 450) * np.exp(-t / 0.25)
    sub = np.sin(2 * np.pi * np.cumsum(42 + 120 * np.exp(-t / 0.06)) / SR) * np.exp(-t / 1.2)
    ring = np.zeros(n)
    for r, a, tau in ((1, .5, 2.4), (2.32, .3, 1.7), (4.17, .2, 1.1), (6.35, .12, .8)):
        ring += a * np.sin(2 * np.pi * 880 * r * t) * np.exp(-t / tau)
    imp = (rng.random(n) < 25 * np.exp(-t / 1.0) / SR) * rng.standard_normal(n)
    kt = tt(nsamp(0.01))
    debris = bp(signal.fftconvolve(imp, white(len(kt)) * np.exp(-kt / 0.002))[:n], 800, 5000)
    out = 0.8 * n_peak(click) + 0.9 * n_peak(stone) + 1.1 * n_peak(sub) + 0.45 * n_peak(ring) + 0.3 * n_peak(debris)
    return n_peak(out * np.minimum(1.0, t / 0.001))

def g_thunder(c, dur, near=True):
    tail = max(dur, 3.0); n = nsamp(tail); t = tt(n)
    env = np.exp(-t / (tail / 3.0)) * (0.55 + 0.45 * np.minimum(np.abs(smooth_noise(n, 2.5)), 2.0) / 2.0)
    out = lp(white(n), 150 if near else 90, 3) * env + bp(white(n), 150, 700) * env * (0.35 if near else 0.15)
    out = n_peak(out) * 0.9
    if near:
        crk = hp(white(n), 600) * np.exp(-t / 0.06) * 0.9 + bp(white(n), 200, 1500) * np.exp(-t / 0.25) * 0.5
        out = out + n_peak(crk) * 0.7
    return n_peak(out * np.minimum(1.0, t / (0.002 if near else 0.5)))

def g_om(c, dur):
    n = nsamp(dur); t = tt(n); u = t / dur
    f0 = deg_freq(1, "minor", c.get("key", "C"), c.get("octave", 2))
    m = np.clip((u - 0.55) / 0.25, 0, 1); m = m * m * (3 - 2 * m)
    out = np.zeros(n)
    for mult, vol in ((1, 1.0), (2, 0.7), (3, 0.25)):
        f = f0 * mult
        ph = 2 * np.pi * np.cumsum(f * (1 + 0.003 * np.sin(2 * np.pi * 4.8 * t) * np.minimum(1.0, t / 1.5))) / SR
        for k in range(1, 22):
            fk = f * k
            if fk > SR * 0.45:
                break
            wo = g(fk, 450, 160) + 0.5 * g(fk, 850, 220) + 0.06
            wm = math.exp(-fk / 320.0) + 0.01
            out += vol * (k ** -0.9) * ((1 - m) * wo + m * wm) * np.sin(k * ph)
    return n_peak(apply_fades(out, 1.1, 1.6))

def g_shankh(c, dur):
    n = nsamp(dur); t = tt(n); f = deg_freq(5, "bhairav", c.get("key", "C"), 3)
    ft = f * (1 - 0.05 * np.exp(-t / 0.3)) * (1 + 0.004 * np.sin(2 * np.pi * 5 * t))
    ph = 2 * np.pi * np.cumsum(ft) / SR
    out = np.zeros(n)
    for k, a in enumerate([1, .9, .75, .55, .4, .3, .2, .12, .08], 1):
        out += a * (1 + g(k * f, 1000, 500)) * np.sin(k * ph)
    out = n_peak(out) + 0.06 * n_rms(bp(white(n), 500, 3000))
    return n_peak(apply_fades(out, 0.6, min(1.2, dur * 0.4)))

def g_damaru(c, dur):
    n = nsamp(dur + 0.3); out = np.zeros(n); pos = 0.0; i = 0
    while pos < dur - 0.05:
        prog = pos / dur
        gap = 0.17 * (1 - prog) + 0.045 * prog
        h = drum(230 if i % 2 == 0 else 175, 0.06, 0.5, 1.3, 2500)
        place(out, pos, h * (0.35 + 0.65 * prog) * (1.0 if i % 2 == 0 else 0.8))
        pos += gap; i += 1
    return n_peak(out)

def g_shimmer(c, dur):
    n = nsamp(dur); t = tt(n); u = t / dur; out = np.zeros(n)
    for _ in range(14):
        am = 0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(0.3, 1.8) * t + rng.uniform(0, 6.283))
        out += np.sin(2 * np.pi * rng.uniform(1100, 5200) * t + rng.uniform(0, 6.283)) * am * rng.uniform(0.3, 1.0)
    return n_peak(apply_fades(out * u ** 1.8, 0.0, 0.08))

def g_whoosh(c, dur):
    n = nsamp(dur); u = np.linspace(0, 1, n)
    env = u ** 2 if c.get("reverse") else np.sin(np.pi * u) ** 2
    return n_peak(bp(white(n), 400, 6000) * env)

def g_flood(c, dur):
    n = nsamp(dur); u = np.linspace(0, 1, n)
    return n_peak(amb_flood(dur) * np.sin(np.pi * u) ** 0.7)

def g_fire(c, dur):
    n = nsamp(dur); u = np.linspace(0, 1, n)
    return n_peak(amb_fire(dur, c.get("intensity", 8)) * np.sin(np.pi * np.minimum(u * 1.4, 1.0) * 0.5 + 0.0) ** 0.8 * (1 - 0.5 * u))

def g_wind(c, dur):
    n = nsamp(dur); u = np.linspace(0, 1, n)
    return n_peak(amb_wind(dur, c.get("intensity", 5)) * np.sin(np.pi * u) ** 0.5)

GEN = {"boom": g_boom, "braam": g_braam, "stab": g_stab, "taiko": g_taiko, "gong": g_gong, "bell": g_bell,
       "glass": g_glass, "skull": g_skull, "glass_snap": g_glass_snap, "sparkle": g_sparkle, "petal": g_petal,
       "wings": g_wings, "crack": g_crack, "trident": g_trident,
       "thunder_near": lambda c, d: g_thunder(c, d, True), "thunder_far": lambda c, d: g_thunder(c, d, False),
       "om": g_om, "shankh": g_shankh, "damaru": g_damaru, "shimmer": g_shimmer, "whoosh": g_whoosh,
       "flood": g_flood, "fire": g_fire, "wind": g_wind}

# ---------------------------------------------------------------- speech envelope (for ducking)
CEN = SF = None
def build_speech():
    global CEN, SF
    wd = os.path.join(HERE, "_work"); os.makedirs(wd, exist_ok=True)
    wav = os.path.join(wd, "voice16k.wav")
    subprocess.run(["nice", "-n", "19", "ffmpeg", "-y", "-v", "error", "-threads", "1", "-i", VOICE,
                    "-ac", "1", "-ar", "16000", wav], check=True)
    x, sr = sf.read(wav)
    hop = int(0.02 * sr); nf = len(x) // hop
    rms = np.sqrt(np.mean(x[:nf * hop].reshape(nf, hop) ** 2, axis=1))
    thr = max(0.08 * float(np.percentile(rms, 90)), 1e-4)
    act = (rms > thr).astype(float)
    act = minimum_filter1d(maximum_filter1d(act, 15), 15)      # close holes < 0.3 s
    s = np.zeros(nf); cur = 0.0
    ac = 1 - math.exp(-0.02 / 0.05); rc = 1 - math.exp(-0.02 / 0.40)
    for i in range(nf):
        cur += (ac if act[i] > cur else rc) * (act[i] - cur); s[i] = cur
    s = np.concatenate([s[3:], np.zeros(3)])                   # 60 ms look-ahead
    CEN = (np.arange(nf) + 0.5) * 0.02; SF = s
    shutil.rmtree(wd, ignore_errors=True)
    print("speech envelope: %.1f s of voice, %.0f%% active" % (nf * 0.02, 100 * float(np.mean(act))))

def speech_at(i0, L):
    return np.interp((np.arange(L) + i0) / SR, CEN, SF, left=0.0, right=0.0)

# ---------------------------------------------------------------- cue rendering
STEM = {"bed": "bed", "ostinato": "bed", "motif": "motif", "pulse": "pulse", "ambience": "ambience",
        "riser": "sfx", "hit": "sfx", "sfx": "sfx"}
DUCK = {"bed": -14, "ostinato": -15, "motif": -14, "pulse": -15, "ambience": -16, "riser": -15, "hit": -12, "sfx": -12}
GAIN = {"bed": -28, "ostinato": -22, "motif": -22, "pulse": -17, "ambience": -30, "riser": -18, "hit": -8, "sfx": -14}
WET = {"bed": (0.35, "long"), "ostinato": (0.25, "short"), "motif": (0.45, "long"), "pulse": (0.12, "short"),
       "ambience": (0.0, "short"), "riser": (0.2, "long"), "hit": (0.4, "long"), "sfx": (0.2, "short")}
SUSTAINED = ("bed", "ostinato", "pulse", "ambience")
FADE_IN = {"bed": 1.5, "ostinato": 0.8, "pulse": 0.5, "ambience": 1.5}
FADE_OUT = {"bed": 2.0, "ostinato": 1.0, "pulse": 0.8, "ambience": 2.0}

def render_cue(c):
    role = c["role"]; t0 = c["from"]["t"]; t1 = c.get("to", {}).get("t", t0 + 1.0)
    dur = max(0.05, t1 - t0)
    if role == "bed": x = gen_bed(c, dur)
    elif role == "motif": x = gen_motif(c, dur)
    elif role == "ostinato": x = gen_ostinato(c, dur)
    elif role == "pulse": x = gen_pulse(c, dur)
    elif role == "ambience": x = gen_ambience(c, dur)
    elif role == "riser": x = gen_riser(c, dur)
    else: x = GEN[c["sfx"]](c, dur)
    x = np.asarray(x, dtype=np.float64)
    if role in ("bed", "ostinato", "motif") and not c.get("no_pocket"):
        x = x - 0.35 * bp(x, 300, 3500)                       # voice pocket (-4 dB, 300 Hz-3.5 kHz)
    if c.get("lpf"):
        x = lp(x, c["lpf"])
    x = n_rms(x) if role in ("bed", "ambience") else n_peak(x)
    if role in SUSTAINED:
        x = apply_fades(x, c.get("fade_in", FADE_IN[role]), c.get("fade_out", FADE_OUT[role]))
    else:
        x = apply_fades(x, c.get("fade_in", 0.0), c.get("fade_out", 0.3 if role in ("hit", "sfx") else 0.0))
    gain = c.get("gain_db", GAIN[role]) + (c.get("intensity", 6) - 6) * 0.8
    x = x * db(gain)
    wet, kind = WET[role]
    st = spatial(x, wet, kind, c.get("pan", 0.0))
    i0 = ix(t0)
    duck = db(c.get("duck_db", DUCK[role]))
    st = st * (1.0 - speech_at(i0, len(st)) * (1.0 - duck))[:, None]
    return i0, st

def silence_mask(cues, amb):
    m = np.ones(N)
    for c in cues:
        if c["role"] != "silence":
            continue
        d = db(c.get("amb_depth_db", -30) if amb else c.get("depth_db", -60))
        i0 = ix(c["from"]["t"]); i1 = ix(c["to"]["t"])
        fi = nsamp(c.get("fade_in", 0.12)); fo = nsamp(c.get("fade_out", 0.5))
        hi = min(N, i1 + fo)
        if i0 >= hi:
            continue
        curve = np.full(hi - i0, d)
        k = min(fi, len(curve)); curve[:k] = 1.0 - (1.0 - d) * ramp_up(k)
        k2 = min(fo, len(curve)); curve[len(curve) - k2:] = d + (1.0 - d) * ramp_up(k2)
        m[i0:hi] = np.minimum(m[i0:hi], curve)
    return m

def add(buf, i0, st):
    m = min(len(st), N - i0)
    if m > 0:
        buf[i0:i0 + m] += st[:m].astype(np.float32)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--cues", default=os.path.join(HERE, "cues.json"))
    args = ap.parse_args()
    cues = json.load(open(args.cues, encoding="utf-8"))["cues"]
    only = [s for s in args.only.split(",") if s]
    build_speech()
    outdir = os.path.join(HERE, "stems"); os.makedirs(outdir, exist_ok=True)
    errors = 0
    for stem in ("bed", "motif", "pulse", "ambience", "sfx"):
        if only and stem not in only:
            continue
        buf = np.zeros((N, 2), dtype=np.float32)
        late = []
        mine = [c for c in cues if STEM.get(c["role"]) == stem]
        for c in mine:
            try:
                r = render_cue(c)
            except Exception:
                errors += 1
                print("ERROR in cue", c.get("id")); traceback.print_exc()
                continue
            if c.get("no_mask"):
                late.append(r)
            else:
                add(buf, r[0], r[1])
        if stem in ("bed", "motif", "pulse"):
            buf *= silence_mask(cues, False)[:, None].astype(np.float32)
        elif stem == "ambience":
            buf *= silence_mask(cues, True)[:, None].astype(np.float32)
        for i0, st in late:
            add(buf, i0, st)
        pk = float(np.max(np.abs(buf))); rm = math.sqrt(float(np.mean(buf.astype(np.float64) ** 2)))
        print("%-9s cues=%3d peak=%6.1f dBFS  rms=%6.1f dBFS" % (stem, len(mine), 20 * math.log10(pk + 1e-9), 20 * math.log10(rm + 1e-9)))
        sf.write(os.path.join(outdir, stem + ".wav"), np.clip(buf, -1.0, 1.0), SR, subtype="PCM_16")
        del buf
    print("done, %d cue errors" % errors)
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
