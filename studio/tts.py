"""Step 1: scenes json -> <build>/audio/NN.mp3 + <build>/timings.json (word-level timing).
narration may be a plain string, or a list of segments for expressive delivery:
  {"t": "text", "rate": "-10%", "pitch": "-3Hz", "vol": "+0%", "pause": 0.4, "voice": "hi-IN-MadhurNeural"}"""
import asyncio, json, os, subprocess, sys
import edge_tts

PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")  # None on a normal machine
PAD = 0.3  # extra silence after each scene (seconds)

def probe(path):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",path]))

async def synth(text, voice, rate, vol, pitch, out):
    c = edge_tts.Communicate(text, voice, rate=rate, volume=vol, pitch=pitch, boundary="WordBoundary", proxy=PROXY)
    words = []
    with open(out, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"text": ch["text"], "start": ch["offset"]/1e7, "end": (ch["offset"]+ch["duration"])/1e7})
    return words

async def main():
    SC = sys.argv[1] if len(sys.argv) > 1 else "scenes.json"; B = sys.argv[2] if len(sys.argv) > 2 else "build"
    cfg = json.load(open(SC)); voice0 = cfg.get("voice", "hi-IN-MadhurNeural")
    os.makedirs(f"{B}/audio", exist_ok=True); timings = []
    for i, s in enumerate(cfg["scenes"]):
        segs = s["narration"]
        if isinstance(segs, str): segs = [{"t": segs}]
        wavs, words, off = [], [], 0.0
        for j, g in enumerate(segs):
            mp3 = f"{B}/audio/{i:02d}_{j:02d}.mp3"; wav = f"{B}/audio/{i:02d}_{j:02d}.wav"
            for attempt in range(4):
                try:
                    w = await synth(g["t"], g.get("voice", voice0), g.get("rate", "+0%"), g.get("vol", "+0%"), g.get("pitch", "+0Hz"), mp3); break
                except Exception as e:
                    print("retry", i, j, e); await asyncio.sleep(2)
            pause = g.get("pause", 0.25)
            subprocess.check_call(["ffmpeg","-y","-v","error","-i",mp3,"-af",f"apad=pad_dur={pause}","-ar","44100","-ac","2",wav])
            d = probe(wav)
            if not w:  # fallback: spread words by length
                toks = g["t"].split(); tot = sum(len(t) for t in toks); t0 = 0; dd = d - pause
                for tok in toks:
                    x = dd*len(tok)/tot; w.append({"text": tok, "start": t0, "end": t0+x}); t0 += x
            words += [{"text": x["text"], "start": x["start"]+off, "end": x["end"]+off} for x in w]
            wavs.append(wav); off += d
        with open(f"{B}/audio/{i:02d}.txt", "w") as f:
            for w in wavs: f.write(f"file '{os.path.basename(w)}'\n")
        mp3 = f"{B}/audio/{i:02d}.mp3"
        subprocess.check_call(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{B}/audio/{i:02d}.txt","-c:a","libmp3lame","-q:a","2",mp3])
        dur = probe(mp3); timings.append({"audio": dur, "duration": dur + PAD, "words": words})
        print(f"scene {i}: {dur:.1f}s, {len(words)} words, {len(segs)} segments")
    json.dump(timings, open(f"{B}/timings.json", "w"), ensure_ascii=False)
    print(f"TOTAL {sum(t['duration'] for t in timings)/60:.2f} min")

asyncio.run(main())
