"""python3 -I render.py [--from B --to B] [--out name] [--procs 2]"""
import sys, os, argparse, subprocess, multiprocessing as mp, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film, sfx3d
from engine import ROOT, REPO, W, H, LEDGER
AUDIO = os.path.join(REPO, "Et tu, Brute (BOXBACK)", "Et tu, Brute_ - The Whole Package - Treblo.ogg")

def make_mix(sfx_wav, out_wav, sfx_gain=0.42):
    """Song (ducked by film.song_gain under the hush) + depth SFX stem, in Python so pan/duck are exact and measurable."""
    import numpy as np, wave
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", AUDIO, "-ac", "2", "-ar", "44100", "-f", "f32le", "-"], capture_output=True).stdout
    song = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    w = wave.open(sfx_wav); sfx = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2) / 32768.0
    n = len(song); sfx = np.pad(sfx, ((0, max(0, n - len(sfx))), (0, 0)))[:n]
    tt = np.arange(0, n / 44100 + 0.01, 0.005)
    g = np.interp(np.arange(n) / 44100, tt, [film.song_gain(film.B(x)) for x in tt])
    y = song * g[:, None] + sfx * sfx_gain
    y = np.clip(y, -1, 1)
    with wave.open(out_wav, "wb") as o:
        o.setnchannels(2); o.setsampwidth(2); o.setframerate(44100); o.writeframes((y * 32767).astype(np.int16).tobytes())


def work(f):
    return film.render_frame(f).tobytes()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="b0", type=float); ap.add_argument("--to", dest="b1", type=float)
    ap.add_argument("--out", default="film"); ap.add_argument("--procs", type=int, default=2); ap.add_argument("--crf", type=int, default=21)
    a = ap.parse_args()
    out = os.path.join(ROOT, "out"); os.makedirs(out, exist_ok=True)
    t0 = film.T(a.b0) if a.b0 is not None else 0.0; t1 = film.T(a.b1) if a.b1 is not None else film.DUR
    t0 = max(0.0, t0)
    f0, f1 = int(round(t0 * film.FPS)), int(round(t1 * film.FPS))
    wav = os.path.join(out, "sfx.wav")
    if not os.path.exists(wav) or os.path.getmtime(wav) < os.path.getmtime(film.__file__):
        sfx3d.render(film.cues(), film.T, film.DUR, film.storm_curve, film.B, wav)
    mixwav = os.path.join(out, "mix.wav")
    make_mix(wav, mixwav)
    mp4 = os.path.join(out, a.out + ".mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(film.FPS), "-i", "-",
           "-ss", f"{t0:.4f}", "-t", f"{t1 - t0:.4f}", "-i", mixwav, "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k", "-shortest", mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); t = time.time()
    with mp.Pool(a.procs) as pool:
        for i, buf in enumerate(pool.imap(work, range(f0, f1), chunksize=4)):
            p.stdin.write(buf)
            if i % 480 == 0: print(f"frame {f0 + i}/{f1} {time.time() - t:.0f}s", flush=True)
    p.stdin.close(); p.wait()
    film.assets()
    json.dump(LEDGER, open(os.path.join(out, "source-ledger.json"), "w"), indent=1)
    json.dump([{"beat": q[0], "time_s": round(film.T(q[0]), 3), "kind": q[1], "z": q[2], "pan": q[3], "gain": q[4]} for q in film.cues()],
              open(os.path.join(out, "sfx-cues.json"), "w"), indent=0)
    print("wrote", mp4, round(time.time() - t, 1), "s")

if __name__ == "__main__":
    main()
