"""Numeric invariants for the multiplane stage.  python3 -I tests/test_multiplane.py
1. Parallax: for every pair of planes and every frame where the camera moves, screen speed ratio == (1/z_a)/(1/z_b)
   and speed is monotonic in 1/z (nearer planes always move faster).
2. Depth fog: for every exterior frame, accumulated fog optical depth in front of a plane is non-decreasing with z
   (far things are never clearer than near things) -- the fog is not a uniform overlay.
3. Fog is not uniform: in the proof's obscure state, the fog alpha at the arm's depth (z=3.0) is lower than at her depth.
"""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import film
from mp import proj, F

PLANES = [30, 18, 14, 6, 4.6, 4.2, 3.3, 3.0, 2.7, 2.0, 1.5]
res = []; ok_all = True
def rec(name, ok, d):
    global ok_all; ok_all &= bool(ok); res.append({"test": name, "pass": bool(ok), "detail": d}); print(("PASS " if ok else "FAIL ") + name, d)

nframes = int(film.DUR * film.FPS); moving = 0; worst_ratio = 0.0; mono_viol = 0
for f in range(1, nframes):
    b0, b1 = film.B((f - 1) / film.FPS), film.B(f / film.FPS)
    if 150 <= b1 < 191 or 232 <= b1 < 244: continue      # interior / close-up: no multiplane camera
    c0, c1 = film.camera(b0), film.camera(b1)
    if abs(c1["x"] - c0["x"]) < 1e-6: continue
    moving += 1
    sp = [abs(proj(0, 0, z, c1)[0] - proj(0, 0, z, c0)[0]) for z in PLANES]
    for i in range(len(PLANES)):
        for j in range(i + 1, len(PLANES)):
            r = (sp[j] / sp[i]) / (PLANES[i] / PLANES[j]); worst_ratio = max(worst_ratio, abs(r - 1))
            if sp[j] <= sp[i]: mono_viol += 1
rec("parallax speed ratio equals depth ratio", worst_ratio < 1e-9, {"moving_frames": moving, "max_rel_error": worst_ratio})
rec("parallax monotonic in 1/z", mono_viol == 0, {"violations": mono_viol})

viol = 0; checked = 0
for f in range(0, nframes, 6):
    b = film.B(f / film.FPS)
    if 150 <= b < 191: continue
    _, sigma = film.fog_state(b)
    prev = -1
    for z in sorted(PLANES):
        zs = [z * k / 40 for k in range(41)]
        tau = sum(sigma((zs[k] + zs[k + 1]) / 2) * (zs[k + 1] - zs[k]) for k in range(40))
        if tau < prev - 1e-12: viol += 1
        prev = tau
    checked += 1
rec("fog optical depth non-decreasing with distance", viol == 0, {"frames_checked": checked, "violations": viol})

st, sigma = film.fog_state(133.0)
a_arm = 1 - math.exp(-sigma(3.0) * 6); a_her = 1 - math.exp(-sigma(4.2) * 6)
rec("obscure state is depth-shaped (arm depth clearer than her depth)", a_arm < a_her, {"state": st, "alpha_z3.0": round(a_arm, 3), "alpha_z4.2": round(a_her, 3)})
json.dump({"suite": "multiplane", "results": res, "all_pass": ok_all}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "multiplane-tests.json"), "w"), indent=1)
sys.exit(0 if ok_all else 1)
