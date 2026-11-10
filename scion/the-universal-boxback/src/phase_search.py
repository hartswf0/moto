"""SCION-06 §7 constrained search: per-box phase offsets for the oscillator bank that minimise box contact.
Deterministic (seeded). Writes src/bank_phases.json; film.py reads it. Run: python3 -I src/phase_search.py"""
import json, math, os, numpy as np
RATIOS = [(1, 1), (1, 2), (2, 3), (3, 2), (3, 4), (4, 3), (1, 3), (2, 1), (5, 4), (4, 5)]
N = 20
phi = np.linspace(0, 2 * math.pi, 192, endpoint=False)   # one closed cycle of the locked bank
a = np.array([RATIOS[j % 10][0] for j in range(N)], float)[:, None]
c = np.array([RATIOS[j % 10][1] for j in range(N)], float)[:, None]
iu = np.triu_indices(N, 1)

def cost(dx, dy, amp=0.85, thr=24.0):
    x = np.sin(a * phi + dx[:, None]) * 380 * amp
    y = np.sin(c * phi + dy[:, None]) * 230 * amp
    D = np.hypot(x[:, None, :] - x[None, :, :], y[:, None, :] - y[None, :, :])[iu]
    return float((D < thr).mean() * len(iu[0])), float(D.min())   # mean overlapping pairs / sample

rng = np.random.default_rng(2026)
base_dx = np.array([(j % 10) * 2 * math.pi / 10 + (0 if j < 10 else math.pi / 10) for j in range(N)])
base_dy = base_dx + math.pi / 2
best = (cost(base_dx, base_dy)[0], base_dx, base_dy); start = best[0]
for it in range(4000):
    dx = best[1] + rng.normal(0, 0.35, N) * (rng.random(N) < 0.3)
    dy = best[2] + rng.normal(0, 0.35, N) * (rng.random(N) < 0.3)
    cst = cost(dx, dy)[0]
    if cst < best[0]: best = (cst, dx, dy)
final, dmin = cost(best[1], best[2])
json.dump({"dx": best[1].tolist(), "dy": best[2].tolist(), "mean_overlapping_pairs_before": start,
           "mean_overlapping_pairs_after": final, "min_center_distance_after_px": dmin, "seed": 2026, "iterations": 4000,
           "threshold_px": 24.0}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bank_phases.json"), "w"), indent=1)
print("mean overlapping pairs: %.3f -> %.3f ; min dist %.1f px" % (start, final, dmin))
