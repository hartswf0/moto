"""python3 -I render.py [--from B --to B] [--out name] [--procs 2]"""
import sys, os, argparse, subprocess, multiprocessing as mp, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film, score
from engine import ROOT, REPO, W, H, LEDGER
AUDIO = os.path.join(REPO, "Et tu, Brute (BOXBACK)", "Et tu, Brute_ - The Universal Boxback - Treblo.ogg")

def typing_beats():
    out = []
    for text, b0 in (("BEAM 7 -> ROW 3", 238), ("BEAM 7 CANNOT GO THERE", 244), ("LIFT ROOF. OPEN DOOR.", 248),
                     ("BEAM 7 -> ROW 3", 255.5), ("ROOF -> NEW PLAN", 258), ("BEAM 7 IN ROW 3", 258)):
        out += [b0 + k / 14 for k in range(len(text)) if text[k] != " "]
    return out

def work(f):
    return film.render_frame(f).tobytes()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="b0", type=float); ap.add_argument("--to", dest="b1", type=float)
    ap.add_argument("--out", default="film"); ap.add_argument("--crf", type=int, default=21); ap.add_argument("--procs", type=int, default=2)
    a = ap.parse_args()
    out = os.path.join(ROOT, "out"); os.makedirs(out, exist_ok=True)
    t0 = film.T(a.b0) if a.b0 is not None else 0.0
    t1 = film.T(a.b1) if a.b1 is not None else film.DUR
    f0, f1 = int(round(t0 * film.FPS)), int(round(t1 * film.FPS))
    cues = score.cue_list(film.EVENTS, typing_beats())
    sw = os.path.join(out, "sfx.wav"); score.render(cues, film.PER, film.OFF, film.DUR, sw)
    mp4 = os.path.join(out, a.out + ".mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(film.FPS), "-i", "-",
           "-ss", f"{t0:.4f}", "-t", f"{t1 - t0:.4f}", "-i", AUDIO, "-ss", f"{t0:.4f}", "-t", f"{t1 - t0:.4f}", "-i", sw,
           "-filter_complex", "[2:a]volume=0.3[s];[1:a][s]amix=inputs=2:duration=first:normalize=0[a]", "-map", "0:v", "-map", "[a]",
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
    json.dump([{"beat": round(b, 4), "time_s": round(film.T(b), 4), "frame": int(round(film.T(b) * film.FPS)), "voice": n, "gain": g} for b, n, g in cues],
              open(os.path.join(out, "sfx-cues.json"), "w"), indent=0)
    print("wrote", mp4, round(time.time() - t, 1), "s")

if __name__ == "__main__":
    main()
