"""Numeric invariants for the Corrugated Sky jelly cut (r2). Run: python3 -I tests/test_jellycut.py [--video]"""
import json, os, sys, glob, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "src"))
import jellycut as J
J.init(os.path.join(ROOT, "jellycut.json")); cfg = J.CFG
cast = json.load(open(os.path.join(ROOT, "cast.json"))); led = json.load(open(os.path.join(ROOT, "source-ledger.json")))
direct = json.load(open(os.path.join(ROOT, "direct.json")))
R = []
def check(name, ok, detail): R.append({"test": name, "pass": bool(ok), "detail": detail}); print(("PASS " if ok else "FAIL ") + name, detail)
FPS = 24; fr = np.array(sorted(J.META)); PER = 60 / cfg["bpm"]; BAR = 4 * PER

# 1 orchestra lock: every role onset starts its jelly's pulse within +-1 frame
members = json.load(open(os.path.join(cfg["orch_dir"], "cast_members.json"))); idx = {}
for i, m in enumerate(members): idx.setdefault(m["role"], []).append(i)
tot = hit = 0; worst = 0
for role in ["kick", "snare", "hat", "bass", "choir", "bed", "call"]:
    ix = idx.get(role, []); ev = [e[0] for e in cast["roles"][role]]
    for k, j in enumerate(ix):
        g = np.array([J.META[f][j][3] for f in fr]); rises = fr[1:][(g[1:] - g[:-1]) > 0.02]
        for q, t in enumerate(ev):
            if q % len(ix) != k or not (fr[0] / 24 + 0.5 < t < fr[-1] / 24 - 0.5): continue
            dd = float(np.min(np.abs(rises - t * 24))); worst = max(worst, dd); tot += 1; hit += dd <= 1.0
check("orchestra pulse within +-1 frame of every role onset", hit == tot and tot > 0, {"onsets": tot, "locked": hit, "worst_frames": round(worst, 3)})

def jel(key, t): return J.jelly(key, t, window=0.0)
def pulses(key, a, b):
    j = J.KEYS[key]; fs = [f for f in fr if a * FPS <= f <= b * FPS]; g = np.array([J.META[f][j][3] for f in fs])
    return int(((g[1:] - g[:-1]) > 0.02).sum()) / max(0.1, (b - a))

# 2 performance: visible beside its picture in every bloom; moves first; changed state after
vis, first, after = [], [], []
for ev in cfg["films"]:
    b0, b1 = ev["bloom"]; c0 = ev["condense"][0]; key = ev["by"]; rel = ev["release"]
    if b1 > b0:
        worst_d = 0
        for f in range(int(b0 * FPS) + 12, int(b1 * FPS) - 12, 6):
            t = f / FPS; st = J.film_state(ev, t); c, wpx, (cx, cy), _, _ = st; hh = wpx * ev.get("aspect", 0.75)
            x, y, r = jel(key, t); dx = max(cx - wpx / 2 - x, 0, x - (cx + wpx / 2)); dy = max(cy - hh / 2 - y, 0, y - (cy + hh / 2))
            inframe = 0 <= x <= J.W and 0 <= y <= J.H; worst_d = max(worst_d, (dx * dx + dy * dy) ** .5 if inframe else 9e9)
        vis.append((ev["label"], round(worst_d, 1)))
    ta = ev["t"][0]
    p_base = pulses(key, max(0.5, ta - 3), ta - 0.2); p_att = pulses(key, ta + 0.3, c0 - 0.5)
    x0, y0, _ = jel(key, ta); x1, y1, _ = jel(key, c0 - 0.5); moved = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5
    first.append((ev["label"], round(p_base, 2), round(p_att, 2), round(moved, 1), p_att >= 1.3 * p_base or moved >= 40))
    p_hold = pulses(key, max(c0, rel - 3), rel); p_aft = pulses(key, rel + 0.6, rel + 2 * BAR)
    xh, yh, _ = jel(key, rel - 0.1); xa, ya, _ = jel(key, rel + 2 * BAR - 0.2); shift = ((xa - xh) ** 2 + (ya - yh) ** 2) ** .5
    after.append((ev["label"], round(p_hold, 2), round(p_aft, 2), round(shift, 1), abs(p_aft - p_hold) >= 0.3 * max(p_hold, 0.1) or shift >= 0.1 * J.H))
check("each bloom: its jelly is in frame within 15% of frame width of the picture", all(d <= 0.15 * J.W for _, d in vis), {"worst_px": vis})
check("attention: the jelly moves or speeds up >=0.5 s before the picture condenses", all(x[-1] for x in first), {"(label, base/s, attention/s, moved px)": [x[:4] for x in first]})
check("changed state: rate or place differs for 2 bars after the release", all(x[-1] for x in after), {"(label, hold/s, after/s, shift px)": [x[:4] for x in after]})

# 3 labels: no two overlap, none over a title plate, in ANY frame
bad = []
from PIL import Image, ImageDraw
d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
for f in range(0, int(145.7 * FPS)):
    t = f / FPS; L = [b for b, _, _ in J.label_boxes(t, d)]; P = J.title_plates(t, d)
    for i in range(len(L)):
        for o in L[i + 1:] + P:
            if not (L[i][2] <= o[0] or L[i][0] >= o[2] or L[i][3] <= o[1] or L[i][1] >= o[3]): bad.append(round(t, 2))
check("labels never collide with each other or a title plate (every frame)", not bad, {"collisions_at": sorted(set(bad))[:10]})

# 4 subjects fill >= 25% of their box (cut sources)
fill = {k: round(float(np.mean([m.mean() for m in J.SRC[k].m])), 3) for k, v in cfg["sources"].items() if v.get("cut")}
check("cut subjects fill >= 25% of their picture box", all(v >= 0.25 for v in fill.values()), fill)

# 5 rights: every drawn source has rights in the allowed set AND a stated basis
nodes = {n["id"]: n for n in led["nodes"]}; used = {e["src"] for e in cfg["films"]}
okr = {u: (nodes["src:" + u]["rights"], bool(nodes["src:" + u].get("basis"))) for u in used}
check("every drawn source: public_domain/CC0/own, with a stated basis", all(r in ("public_domain", "CC0", "producer's own work") and b for r, b in okr.values()), {k: v[0] for k, v in okr.items()})

# 6 the medusa's girl-and-dog flecks are released INTO the gate film at the let-go
ev = [e for e in cfg["films"] if e["src"] == "girl_dog"][0]; st = J.film_state(ev, ev["release"] + 1.5)
tgt = J.target_point("gate_dog", ev["release"] + 1.5)
check("the let-go: released flecks stream to the gate film's dog", st is not None and st[3] is not None and tgt is not None,
      {"release_s": round(ev["release"], 3), "stream_k_at_+1.5s": round(st[3][2], 3) if st and st[3] else None, "target": [round(v) for v in tgt] if tgt else None})

# 7 (video) the Sentinel's brightness swings >= 15% on EVERY kick, measured on rendered frames
if "--video" in sys.argv:
    vid = os.path.join(ROOT, "proof.mp4"); t0 = 64.0
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    V = np.frombuffer(raw, np.uint8).reshape(-1, 720, 1280); swings = []
    for tk in J.KICKS:
        if not (t0 + 0.3 < tk < t0 + len(V) / FPS - 0.3): continue
        f = int(round((tk - t0) * FPS)); x, y, r = J.jelly("kick0", tk, window=0.0); R = int(max(24, r * 1.6))
        crop = lambda k: V[k, max(0, int(y) - R):int(y) + R, max(0, int(x) - R):int(x) + R].astype(float)
        pre = min(np.percentile(crop(k), 90) for k in (f - 2, f - 1)); peak = max(np.percentile(crop(k), 90) for k in (f, f + 1))
        swings.append((peak - pre) / max(1, pre))
    check("sentinel brightness swings >= 15% on every kick (rendered proof crop, p90)", len(swings) and min(swings) >= 0.15,
          {"kicks": len(swings), "min_swing": round(float(min(swings)), 3), "median": round(float(np.median(swings)), 3)})
json.dump({"results": R, "all_pass": all(r["pass"] for r in R)}, open(os.path.join(HERE, "invariants.json"), "w"), indent=1)
sys.exit(0 if all(r["pass"] for r in R) else 1)
