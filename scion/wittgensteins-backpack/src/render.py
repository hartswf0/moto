"""Render: python3 -I render.py [--from BEAT --to BEAT] [--scale 0.5] [--out name] [--sheet]"""
import sys, os, argparse, subprocess, multiprocessing as mp, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film, sfx as SFXM
from engine import ROOT, REPO, W, H, LEDGER

AUDIO = os.path.join(REPO, "Et tu, Brute (BOXBACK)", "Et tu, Brute_ - Wittgenstein's Backpack - Treblo.ogg")

def work(args):
    f, sc = args
    im = film.render_frame(f)
    if sc != 1: im = im.resize((int(W * sc), int(H * sc)))
    return im.tobytes()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="b0", type=float, default=None); ap.add_argument("--to", dest="b1", type=float, default=None)
    ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--out", default="film")
    ap.add_argument("--crf", type=int, default=20); ap.add_argument("--procs", type=int, default=4)
    a = ap.parse_args()
    out = os.path.join(ROOT, "out"); os.makedirs(out, exist_ok=True)
    if not os.path.exists(os.path.join(out, "sketch_poses.pkl")):
        t = time.time(); film.precompute_sketch(); print("sketch solve", round(time.time() - t, 1), "s", flush=True)
    t0 = film.T(a.b0) if a.b0 is not None else 0.0
    t1 = film.T(a.b1) if a.b1 is not None else film.DUR
    f0, f1 = int(round(t0 * film.FPS)), int(round(t1 * film.FPS))
    cues = film.build_sfx()
    sfx_wav = os.path.join(out, "sfx.wav")
    SFXM.render(cues, film.PER, film.OFF, film.DUR, sfx_wav)
    w, h = int(W * a.scale), int(H * a.scale)
    mp4 = os.path.join(out, a.out + ".mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(film.FPS), "-i", "-",
           "-ss", f"{t0:.4f}", "-t", f"{t1 - t0:.4f}", "-i", AUDIO, "-ss", f"{t0:.4f}", "-t", f"{t1 - t0:.4f}", "-i", sfx_wav,
           "-filter_complex", "[2:a]volume=0.32[s];[1:a][s]amix=inputs=2:duration=first:normalize=0[a]", "-map", "0:v", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k", "-shortest", mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t = time.time()
    with mp.Pool(a.procs) as pool:
        for i, buf in enumerate(pool.imap(work, [(f, a.scale) for f in range(f0, f1)], chunksize=4)):
            p.stdin.write(buf)
            if i % 240 == 0: print(f"frame {f0 + i}/{f1}  {time.time() - t:.0f}s", flush=True)
    p.stdin.close(); p.wait()
    film.assets()
    json.dump(LEDGER, open(os.path.join(out, "source-ledger.json"), "w"), indent=1)
    json.dump([{"beat": b, "time_s": round(film.T(b), 4), "frame": int(round(film.T(b) * film.FPS)), "kind": k, "gain": g} for b, k, g in cues],
              open(os.path.join(out, "sfx-cues.json"), "w"), indent=0)
    print("wrote", mp4, round(time.time() - t, 1), "s")

if __name__ == "__main__":
    main()
