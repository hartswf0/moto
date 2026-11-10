"""Numeric invariants for CORRUGATED SKY (Reiniger shadow theatre). Run: python3 -I tests/test_invariants.py
1 joint-angle limits: no pose in the proof (every frame) or the film (every 6th frame) requests an angle outside its limit
2 pinned contacts: every hold marked pinned in the proof (hand/foot on gate, paw on hand) has residual < 1 px
3 pinned joints never detach: every child bone starts exactly at its pin on the parent (sampled poses)
4 silhouettes do not merge: girl and dog masks overlap only at the hand/paw contact (< 1.5% of the smaller shape)
"""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import film, rigs
from PIL import Image, ImageDraw

res = []
def check(name, ok, detail):
    res.append({"test": name, "pass": bool(ok), "detail": detail}); print(("PASS " if ok else "FAIL ") + name, detail)

rows, limits = film.proof_trace()
check("proof: joint limits respected (every frame b176-208)", len(limits) == 0, {"violations": limits[:5], "frames": len(rows)})
pins = [c for r in rows for c in r["contacts"]]
worst = max(pins, key=lambda c: c[2]) if pins else None
check("proof: pinned contacts residual < 1 px", worst is not None and worst[2] < 1.0, {"n_pinned_samples": len(pins), "worst": worst})

rigs.LIMIT_LOG.clear()
n = 0
for f in range(0, int(film.DUR * film.FPS), 6):
    film.render_frame(f); n += 1
viol = sorted(set((a, b) for a, b, *_ in rigs.LIMIT_LOG))
check("film: joint limits respected (every 6th frame)", len(viol) == 0, {"frames": n, "violations": viol[:8]})

worst_pin = 0.0
for b in (180, 186, 192, 199, 203):
    S = film.proof_state(b)
    r, p, face = film.solve_girl(S["girl"])
    for rig, root, pose, fc in ((film.GIRL, r, p, face), (film.DOG,) + film.solve_dog(S["dog"])):
        W = rig.fk(root, pose, face=fc, check=False)
        for bone in rig.bones:
            if bone.parent is None: continue
            po, pa, _ = W[bone.parent]; pb = rig.by[bone.parent]
            loc = (pb.length * bone.at + bone.offset[0], bone.offset[1])
            if fc == -1: loc = (loc[0], -loc[1])
            rr = rigs._rot((loc[0] * rig.scale, loc[1] * rig.scale), pa)
            pin = (po[0] + rr[0], po[1] + rr[1])
            worst_pin = max(worst_pin, math.dist(pin, W[bone.name][0]))
check("pinned joints never detach", worst_pin < 1e-6, {"max_pin_gap_px": worst_pin})

def mask(rig, root, pose, face, profile=None):
    m = Image.new("1", (film.W, film.H), 0); d = ImageDraw.Draw(m)
    W = rig.fk(root, pose, face=face, check=False)
    for poly in rig.polys(W, profile, face=face): d.polygon(poly, fill=1)
    return m
worst_ov = 0.0; at = None
for b in [184 + 0.25 * k for k in range(60)]:
    S = film.proof_state(b)
    r, p, face = film.solve_girl(S["girl"]); gm = mask(film.GIRL, r, p, face, S["girl"].get("profile"))
    dr, dp, df = film.solve_dog(S["dog"]); dm = mask(film.DOG, dr, dp, df)
    import numpy as np
    g, dd = np.array(gm), np.array(dm)
    ov = (g & dd).sum() / max(1, min(g.sum(), dd.sum()))
    if ov > worst_ov: worst_ov, at = ov, b
check("silhouettes do not merge (girl vs dog, b184-199)", worst_ov < 0.015, {"max_overlap_fraction": round(float(worst_ov), 4), "at_beat": at})

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "invariants.json")
json.dump({"suite": "corrugated-sky invariants", "results": res, "all_pass": all(r["pass"] for r in res)}, open(out, "w"), indent=1)
sys.exit(0 if all(r["pass"] for r in res) else 1)
