"""Measured audio checks on the FINAL film's mixed track.  python3 -I tests/test_audio.py [film.mp4]
1. Pan follows the hand: during b136.2-137.2 the mix pans toward the arm side (right): (R-L)/(R+L) RMS > 0.3.
2. The hush is audible: RMS over b134.4-136.4 is at least 6 dB below b131.5-133.5.
3. The mix is not mono: L/R correlation over the proof window (b110-150) is below the 0.98 found by the critic.
"""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import film
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "the-whole-package.mp4")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "2", "-ar", "44100", "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def win(b0, b1): return x[int(film.T(b0) * 44100):int(film.T(b1) * 44100)]
def rms(a): return np.sqrt((a ** 2).mean() + 1e-12)
res = []; ok = True
w = win(136.2, 137.2); L, R = rms(w[:, 0]), rms(w[:, 1]); pan = (R - L) / (R + L)
res.append({"test": "pan toward arm b136.2-137.2", "pan": round(pan, 3), "pass": pan > 0.3})
db = 20 * np.log10(rms(win(134.4, 136.4)) / rms(win(131.5, 133.5)))
res.append({"test": "hush dip b134.4-136.4 vs b131.5-133.5", "db": round(db, 2), "pass": db <= -6})
w = win(110, 150); c = np.corrcoef(w[:, 0], w[:, 1])[0, 1]
res.append({"test": "L/R correlation over proof", "corr": round(c, 3), "pass": c < 0.98})
for r in res: print(("PASS " if r["pass"] else "FAIL ") + json.dumps(r)); ok &= r["pass"]
json.dump({"suite": "audio", "source": os.path.basename(src), "results": res, "all_pass": bool(ok)},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio-tests.json"), "w"), indent=1)
sys.exit(0 if ok else 1)
