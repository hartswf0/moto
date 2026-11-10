"""r3 invariants, measured on RENDERED mask passes (three.js holder-only / film-only renders at 320x180) and the capture
metadata. usage: python3 -I tests/test_r3.py <orch_dir> [<letgo_mask_dir>] [--window t0 t1]"""
import json, os, sys, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
orch = sys.argv[1]; letdir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
win = None
if "--window" in sys.argv: i = sys.argv.index("--window"); win = (float(sys.argv[i + 1]), float(sys.argv[i + 2]))
scene = json.load(open(os.path.join(ROOT, "scene.json"))); cast = json.load(open(os.path.join(ROOT, "cast.json")))
META = {}
for mp in glob.glob(os.path.join(orch, "meta_*.json")):
    for m in json.load(open(mp)): META[m["f"]] = m["jel"]
fr = np.array(sorted(META)); keys = {row[6]: i for i, row in enumerate(META[fr[0]])}; FPS = 24
PER = 60 / 141.05; BAR = 4 * PER
R = []
def check(name, ok, detail): R.append({"test": name, "pass": bool(ok), "detail": detail}); print(("PASS " if ok else "FAIL ") + name, json.dumps(detail)[:600])
def inwin(t): return win is None or (win[0] <= t <= win[1])
def mask(p): return np.asarray(Image.open(p).convert("L"), np.float32) > 18

# 1 every bloom frame: holder's whole body in frame (no holder pixel on the frame edge) and not covered by its film
rows = []
for p in sorted(glob.glob(os.path.join(orch, "mh*.png"))):
    f = int(os.path.basename(p)[2:7]); pf = os.path.join(orch, f"mf{f:05d}.png"); Hm = mask(p)
    if not Hm.any(): rows.append((f, 0, 0, 0)); continue
    edge = Hm[0, :].any() or Hm[-1, :].any() or Hm[:, 0].any() or Hm[:, -1].any()
    Fm = mask(pf) if os.path.exists(pf) else np.zeros_like(Hm); unc = float((Hm & ~Fm).sum() / Hm.sum())
    rows.append((f, int(not edge), round(unc, 3), int(Hm.sum())))
ok1 = rows and all(r[1] == 1 and r[2] >= 0.9 for r in rows)
check("bloom: holder fully in frame and >=90% uncovered by its film (mask pass, every sampled bloom frame)", ok1,
      {"frames": len(rows), "in_frame": sum(r[1] for r in rows), "min_uncovered": min(r[2] for r in rows) if rows else None,
       "failing": [r for r in rows if not (r[1] == 1 and r[2] >= 0.9)][:6]})

def jel(t, k="call0"): f = int(round(t * FPS)); row = META.get(f); return None if row is None else row[keys[k]]
def pulses(a, b, k="call0"):
    fs = [f for f in fr if a * FPS <= f <= b * FPS]; g = np.array([META[f][keys[k]][3] for f in fs]); return int(((g[1:] - g[:-1]) > .02).sum()) / max(.1, b - a)
# 2 moves first / changed state
first, after = [], []
for F in scene["films"]:
    ta, c0, rel = F["t"][0], F["condense"][0], F["release"]
    if not (inwin(ta - 2) and inwin(c0)): pass
    else:
        a, b = jel(ta), jel(c0 - .5)
        if a and b: first.append((F["id"], round(pulses(ta - 2, ta - .1), 2), round(pulses(ta + .3, c0 - .5), 2), round(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** .5, 1)))
    if inwin(ta - .2) and inwin(rel + 2 * BAR):
        a, b = jel(ta - .2), jel(rel + 2 * BAR - .2)
        if a and b:
            dpos = (((a[0] - b[0]) / 1280) ** 2 + ((a[1] - b[1]) / 720) ** 2) ** .5; dsz = abs(b[5] - a[5]) / max(1, a[5])
            after.append((F["id"], round(dpos, 3), round(dsz, 3)))
if first: check("moves first: pulse rate rises or it travels >=40 px before condensing", all(x[2] >= 1.3 * x[1] or x[3] >= 40 for x in first), {"(id, base/s, attention/s, moved px)": first})
if after: check("changed state: >20% position (of frame) or size, before the bloom vs 2 bars after the release", all(x[1] > .2 or x[2] > .2 for x in after), {"(id, dpos, dsize)": after})

# 3 the let-go: the painting's flecks travel into the silhouette dog, 84.8-86.0 s
if letdir:
    cs = []
    for p in sorted(glob.glob(os.path.join(letdir, "mp*.png"))):
        f = int(os.path.basename(p)[2:7]); m = mask(p)
        if m.any(): ys, xs = np.where(m); cs.append((round(f / FPS, 2), float(xs.mean()), float(ys.mean()), int(m.sum())))
    if len(cs) >= 3:
        tgt = None
        gate = sorted(glob.glob(os.path.join(letdir, "mf*.png")))
        if gate:
            g = mask(gate[-1]); ys, xs = np.where(g); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); tgt = (x0 + .71 * (x1 - x0), y0 + .76 * (y1 - y0))
        d0 = ((cs[0][1] - tgt[0]) ** 2 + (cs[0][2] - tgt[1]) ** 2) ** .5; dmin = min(((c[1] - tgt[0]) ** 2 + (c[2] - tgt[1]) ** 2) ** .5 for c in cs if c[0] <= 86.05)
        check("let-go: the painting's fleck centroid travels into the gate's dog (84.8-86.0 s)", dmin <= 0.3 * d0, {"start_dist_px@320": round(d0, 1), "closest_px@320": round(dmin, 1), "track": cs[:: max(1, len(cs) // 6)]})

# 4 sentinel fully in frame: projected centre +- its radius inside the frame, every frame
bad = [int(f) for f in fr if not (META[f][keys["kick0"]][0] - META[f][keys["kick0"]][5] > 0 and META[f][keys["kick0"]][0] + META[f][keys["kick0"]][5] < 1280 and META[f][keys["kick0"]][1] - META[f][keys["kick0"]][5] > 0 and META[f][keys["kick0"]][1] + META[f][keys["kick0"]][5] < 720)]
check("sentinel fully in frame (centre +- projected radius), every frame", not bad, {"frames": len(fr), "out": bad[:5]})

# 5 at least 3 other jellies with onset-locked pulses (Pearson r between glow and the onset train through the same decay)
mem = json.load(open(os.path.join(orch, "cast_members.json"))); idx = {}
for i, m in enumerate(mem): idx.setdefault(m["role"], []).append(i)
rs = {}
for role in ["snare", "hat", "bass", "choir", "bed", "call"]:
    ev = [e[0] for e in cast["roles"][role]]; ix = idx.get(role, [])
    for k, j in enumerate(ix):
        ts = [t for q, t in enumerate(ev) if q % len(ix) == k]; g = np.array([META[f][j][3] for f in fr]); imp = np.zeros(len(fr))
        for t in ts:
            q = int(round(t * FPS)) - int(fr[0])
            if 0 <= q < len(fr): imp[q] = 1
        kern = np.exp(-np.arange(48) / FPS * 2.6); s = np.convolve(imp, kern)[:len(fr)]
        if s.std() > 0 and g.std() > 0: rs[mem[j]["k"]] = round(float(np.corrcoef(g, s)[0, 1]), 3)
check(">=3 jellies besides the sentinel pulse locked to their onsets (r>0.3)", sum(v > .3 for v in rs.values()) >= 3, rs)

# 6 rhymes: survivor and hearth bloom >=300 px tall (of 720), centred, uncovered, for >=3 s (film masks)
for fid in ("survivor", "hearth"):
    F = [x for x in scene["films"] if x["id"] == fid][0]; b0, b1 = F["bloom"]
    if not (inwin(b0) and inwin(b1)): continue
    good = []
    for p in sorted(glob.glob(os.path.join(orch, "mf*.png"))):
        f = int(os.path.basename(p)[2:7]); t = f / FPS
        if not (b0 <= t <= b1): continue
        m = mask(p); ys, xs = np.where(m)
        if not len(xs): continue
        hpx = (ys.max() - ys.min()) * 4; cx = (xs.min() + xs.max()) / 2 / 320
        good.append((round(t, 2), hpx >= 300 and abs(cx - .5) < .15))
    run = best = 0; prev = None
    for t, g in good:
        run = run + (t - prev if prev is not None and g else 0) if g else 0; prev = t; best = max(best, run)
    check(f"{fid}: >=300 px tall, centred, for >=3 s", best >= 3.0, {"longest_s": round(best, 2), "samples": len(good)})


# 7 clutter: at most one label at a time, never during a title (every frame)
sys.path.insert(0, os.path.join(ROOT, "..", "src"))
import jellycut as J
J.init(os.path.join(ROOT, "jellycut.json"))
from PIL import ImageDraw
d = ImageDraw.Draw(Image.new("RGB", (1, 1))); bad = []
for f in range(0, int(145.7 * 24)):
    t = f / 24
    if not inwin(t): continue
    L = J.label_boxes(t, d); P = J.title_plates(t, d)
    if len(L) > 1 or (L and P): bad.append(round(t, 2))
check("clutter: at most one label at a time and none during a title (every frame)", not bad, {"bad_at": bad[:8]})
json.dump({"results": R, "all_pass": all(r["pass"] for r in R)}, open(os.path.join(HERE, "invariants_r3.json"), "w"), indent=1)
sys.exit(0 if all(r["pass"] for r in R) else 1)
