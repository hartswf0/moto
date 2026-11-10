"""SCION-06 §7 constrained search (r2): per-box phase offsets for the oscillator bank, scored on the REAL
bank trajectory (amplitude ramp, detune, re-lock) with the boxes at their drawn scale. Objective: frames in
which any two boxes come closer than 46 px (their diagonal at 0.45 scale) - weighted x10 in the re-lock
window b144-160 that the critic flagged. Deterministic (seed 2026). Writes src/bank_phases.json."""
import json, math, os, numpy as np
RATIOS = [(1, 1), (1, 2), (2, 3), (3, 2), (3, 4), (4, 3), (1, 3), (2, 1), (5, 4), (4, 5)]
N = 20; CX, CY = 640.0, 380.0
P_ = 0.4614285829991442
EPS = np.random.default_rng(11).uniform(-1, 1, N)
def ease(u): u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)
bs = np.arange(84, 160, 1 / (24 * P_))
det = np.where(bs < 112, 0, np.where(bs < 128, 0.06 * ease((bs - 112) / 16), np.where(bs < 144, 0.06, 0.06 * (1 - ease((bs - 144) / 16)))))
amp = np.where(bs < 96, 0.55 + 0.3 * ease((bs - 80) / 16), np.where(bs < 144, 0.85 + 0.15 * ease((bs - 96) / 16), 1.0))
phi = 2 * math.pi * (bs - 80) / 16
a = np.array([RATIOS[j % 10][0] for j in range(N)], float)[:, None]
c = np.array([RATIOS[j % 10][1] for j in range(N)], float)[:, None]
fa = a * (1 + det[None] * EPS[:, None]); fc = c * (1 - det[None] * EPS[:, None] * 0.7)
w = np.where(bs >= 144, 10.0, 1.0)
iu = np.triu_indices(N, 1)
def cost(dx, dy):
    x = CX + np.sin(fa * phi + dx[:, None]) * 380 * amp
    y = CY + np.sin(fc * phi + dy[:, None]) * 230 * amp
    D = np.hypot(x[iu[0]] - x[iu[1]], y[iu[0]] - y[iu[1]]).min(0)
    bad = D < 46
    return float((bad * w).sum()), int(bad[bs >= 144].sum()), int(bad.sum()), float(D[bs >= 144].min())
old = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bank_phases.json")))
dx0, dy0 = np.array(old["dx"]), np.array(old["dy"])
best = (cost(dx0, dy0)[0], dx0, dy0); start = cost(dx0, dy0)
rng = np.random.default_rng(2026)
for it in range(3000):
    k = rng.random(N) < 0.25
    dx = best[1] + rng.normal(0, 0.4, N) * k; dy = best[2] + rng.normal(0, 0.4, N) * k
    cst = cost(dx, dy)[0]
    if cst <= best[0]: best = (cst, dx, dy)
    if best[0] == 0: break
fin = cost(best[1], best[2])
json.dump({"dx": best[1].tolist(), "dy": best[2].tolist(), "objective": "frames with any pair < 46 px; x10 in b144-160",
           "before": {"weighted": start[0], "relock_frames": start[1], "all_frames": start[2], "relock_min_px": start[3]},
           "after": {"weighted": fin[0], "relock_frames": fin[1], "all_frames": fin[2], "relock_min_px": fin[3]},
           "seed": 2026, "iterations": it + 1}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bank_phases.json"), "w"), indent=1)
print("before", start, "after", fin, "iters", it + 1)
