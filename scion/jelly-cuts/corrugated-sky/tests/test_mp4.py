"""Claims measured on the FINAL mp4 pixels only (r4), as an outside critic would.
Positions of jellies come from the capture metadata (where to look); every brightness, motion and size is read from
the decoded video. usage: python3 -I tests/test_mp4.py <video.mp4> <video_t0> [--blooms]"""
import sys, os, json, subprocess, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, os.path.join(ROOT, "..", "src"))
import jellycut as J
J.init(os.path.join(ROOT, "jellycut.json")); vid, t0 = sys.argv[1], float(sys.argv[2])
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, 720, 1280); n = len(V); FPS = 24
cast = json.load(open(os.path.join(ROOT, "cast.json"))); out = {"video": os.path.basename(vid), "t0": t0, "frames": n}

def crop_p90(k, x, y, r):
    RR = int(max(20, r * 1.4)); c = V[k, max(0, int(y) - RR):int(y) + RR, max(0, int(x) - RR):int(x) + RR]
    return float(np.percentile(c, 90)) if c.size else np.nan

# 1 sentinel: p90 brightness swing on every kick
sw = []
for tk in J.KICKS:
    if not (t0 + .3 < tk < t0 + n / FPS - .3): continue
    f = int(round((tk - t0) * FPS)); x, y, r = J.jelly("kick0", tk, window=0.0)
    pre = min(crop_p90(k, x, y, r) for k in (f - 2, f - 1)); pk = max(crop_p90(k, x, y, r) for k in (f, f + 1)); sw.append((pk - pre) / max(1, pre))
out["sentinel"] = {"kicks": len(sw), "min_swing": round(float(min(sw)), 3), "median_swing": round(float(np.median(sw)), 3)}

# 2 onset lock of the other jellies: Pearson r between the crop's p90 brightness series and the role-onset train
mem = {}; N = {"snare": 2, "hat": 2, "bass": 1, "choir": 1, "bed": 1}
for role, nn in N.items():
    evs = sorted(e[0] for e in cast["roles"][role])
    for k in range(nn):
        key = f"{role}{k}"; ts = [t for q, t in enumerate(evs) if q % nn == k]; ser, train = [], []
        imp = np.zeros(n)
        for t in ts:
            q = int(round((t - t0) * FPS))
            if 0 <= q < n: imp[q] = 1
        kern = np.exp(-np.arange(24) / FPS / 0.12); s = np.convolve(imp, kern)[:n]
        for k2 in range(n):
            x, y, r = J.jelly(key, t0 + k2 / FPS, window=0.0)
            ser.append(crop_p90(k2, x, y, r) if (30 < x < 1250 and 30 < y < 690) else np.nan)
        ser = np.array(ser); m = ~np.isnan(ser)
        if m.sum() > 48 and s[m].std() > 0 and ser[m].std() > 0:
            mem[key] = {"r": round(float(np.corrcoef(ser[m], s[m])[0, 1]), 3), "frames_in_view": int(m.sum())}
out["orchestra_r"] = mem; out["jellies_r_gt_0.3"] = sum(v["r"] > .3 for v in mem.values())

# 3 pacing: the longest run (s) whose 0.5 s windows have mean |frame difference| < 0.8 grey levels at 320 px
small = V[:, ::4, ::4].astype(np.int16); d = np.abs(np.diff(small, axis=0)).mean(axis=(1, 2)); w = 12
win = [float(d[i:i + w].mean()) for i in range(0, len(d) - w, w)]
run = best = 0
for v in win:
    run = run + .5 if v < .8 else 0; best = max(best, run)
out["longest_still_s"] = best

# 4 bloom picture height on the rendered frame (rows bounded by the strongest horizontal edges near the centre)
if "--blooms" in sys.argv:
    hs = {}
    for f in J.CFG["scene_films"]:
        b0, b1 = f["bloom"]; tp = (b0 + b1) / 2
        if not (t0 < tp < t0 + n / FPS) or b1 <= b0: continue
        k = int((tp - t0) * FPS); g = V[k].astype(float); gy = np.abs(np.diff(g, axis=0))[:, 320:960].mean(1)
        top = int(np.argmax(gy[:360])); bot = 360 + int(np.argmax(gy[360:]))
        hs[f["id"]] = {"t": round(tp, 1), "picture_height_frac": round((bot - top) / 720, 3)}
    out["bloom_height"] = hs
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "mp4_" + os.path.splitext(os.path.basename(vid))[0] + ".json"), "w"), indent=1)
