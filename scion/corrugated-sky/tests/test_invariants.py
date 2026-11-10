"""Numeric invariants for CORRUGATED SKY (Reiniger shadow theatre). Run: python3 -I tests/test_invariants.py
1 joint-angle limits: no pose in the proof (every frame) or the film (every 6th frame) requests an angle outside its limit
2 pinned contacts: every hold marked pinned in the proof (hand/foot on gate, paw on hand) has residual < 1 px
3 pinned joints never detach: every child bone starts exactly at its pin on the parent (sampled poses)
4 silhouettes do not merge: girl and dog masks overlap only at the hand/paw contact (< 1.5% of the smaller shape)
"""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import film, rigs
from PIL import ImageFilter
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

# ---- 5 the choice to let go (b198.5): her hand opens while the paw has not moved; her arm pulls back >= 2 frames before the paw folds
import numpy as np
def qbeat(f): return film.B(film.frame_time_on_twos(f) / film.FPS)
f0, f1 = int(film.T(197.5) * film.FPS), int(film.T(202) * film.FPS)
P = film.paw_point()
F_open = F_arm = F_paw = None; paw_at_open = None
for f in range(f0, f1):
    b = qbeat(f); S = film.proof_state(b)
    prof = (S["girl"].get("profile") or {}).get("hand_n")
    r, p, face = film.solve_girl(S["girl"], log=False)
    Wg = film.GIRL.fk(r, p, check=False)
    dr, dp, df = film.solve_dog(S["dog"]); Wd = film.DOG.fk(dr, dp, face=df, check=False)
    paw = Wd["fpaw_n"][2]; hand = Wg["fore_n"][2]
    if F_open is None and prof == "open": F_open = f; paw_at_open = math.dist(paw, P)
    if F_open is not None and F_arm is None and math.dist(hand, film.PROOF_M) > 1.0: F_arm = f
    if F_open is not None and F_paw is None and math.dist(paw, P) > 1.0: F_paw = f
check("let-go order: open -> arm back -> paw folds (>= 2 frames)", F_open is not None and paw_at_open < 1.0 and F_open < F_arm and F_paw - F_arm >= 2,
      {"frame_open": F_open, "paw_offset_at_open_px": round(paw_at_open, 3) if paw_at_open is not None else None, "frame_arm_back": F_arm, "frame_paw_folds": F_paw})
# hand contour change at the open, measured at phone size (360 px wide), including the 1.55x proof push-in
def hand_mask(b, scale):
    S = film.proof_state(b); r, p, face = film.solve_girl(S["girl"], log=False)
    W_ = film.GIRL.fk(r, p, check=False)
    prof = dict(S["girl"].get("profile") or {})
    polys = [poly for poly in film.GIRL.polys({"hand_n": W_["hand_n"]} | {k: v for k, v in W_.items() if k != "hand_n"}, prof) ]
    o, a, _ = W_["hand_n"]; bone = film.GIRL.by["hand_n"]
    shp = bone.profiles.get(prof.get("hand_n"), bone.shape)
    m = Image.new("1", (360, 203), 0); d = ImageDraw.Draw(m)
    z = 1.55; cx0 = 660 - 1280 / z / 2; cy0 = 500 - 720 / z / 2
    for poly in shp:
        pts = [rigs._rot((x * film.GIRL.scale, y * film.GIRL.scale), a) for x, y in poly]
        d.polygon([((o[0] + q[0] - cx0) * z * scale, (o[1] + q[1] - cy0) * z * scale) for q in pts], fill=1)
    return np.array(m)
before = hand_mask(198.4, 360 / 1280); after = hand_mask(198.6, 360 / 1280)
x = before ^ after; ys, xs = np.nonzero(x)
span = max(xs.max() - xs.min(), ys.max() - ys.min()) + 1 if len(xs) else 0
check("hand contour visibly opens at 360 px (changed region >= 6 px)", span >= 6, {"changed_px_area": int(x.sum()), "changed_span_px": int(span)})

# ---- 6 the return (116 s): the dog is its own connected black region, legs + tail visible, sharing no pixels with gate or flames
b = film.B(116.0)
other = film.Stage(b)
for k, fx in enumerate((90, 200, 310, 420, 520)):
    film.flame(other, fx, film.WALL_TOP + 20, 170 + 40 * math.sin(k * 1.7), b, 11 + k)
film.gate(other, x=film.RETURN_GATE, fence_right=False)
om = np.array(other.m["mid"].resize((film.W, film.H))) > 127
p = film.dog_stand(wag=-20); p["head"] = -20
r = film.legs_to_floor(film.DOG, film.RETURN_DOG, p, film.FLOOR, -1)
Wd = film.DOG.fk(r, p, face=-1, check=False)
dm_img = Image.new("L", (film.W, film.H), 0); dd = ImageDraw.Draw(dm_img)
for poly in film.DOG.polys(Wd, face=-1): dd.polygon(poly, fill=255)
from PIL import ImageFilter
dil = np.array(dm_img.filter(ImageFilter.MaxFilter(5))) > 127
dm = np.array(dm_img) > 127
shared = int((dil & om).sum())
seed = tuple(int(v) for v in Wd["spine"][0]); ff = dm_img.copy(); ImageDraw.floodfill(ff, seed, 128)
one_region = int((np.array(ff) == 255).sum()) == 0
ends = {n: Wd[n][2] for n in ("hshin_n", "hshin_f", "fpaw_n", "fpaw_f", "tail")}
visible = all(0 <= e[0] < film.W and 0 <= e[1] < film.H and not om[int(e[1]), int(e[0])] for e in ends.values())
check("return set (geometry): dog is a separate single region, 4 legs + tail visible", shared == 0 and one_region and visible,
      {"beat": round(b, 2), "pixels_shared_within_2px_with_gate_or_flames": shared, "single_region": one_region, "leg_tail_ends": {k: [round(v[0]), round(v[1])] for k, v in ends.items()}})

# ---- 7 (round 2) the thumb joins the palm: hand + thumb are ONE connected component in every grasp frame (proof 8-11.3 s)
proof_t0 = film.T(172)
worst_cc = 1
for f in range(int((proof_t0 + 8.0) * film.FPS), int((proof_t0 + 11.3) * film.FPS)):
    b = film.B(film.frame_time_on_twos(f) / film.FPS)
    S = film.proof_state(b); r, p, face = film.solve_girl(S["girl"], log=False)
    W_ = film.GIRL.fk(r, p, check=False)
    prof = (S["girl"].get("profile") or {}).get("hand_n")
    bone = film.GIRL.by["hand_n"]; shp = bone.profiles.get(prof, bone.shape)
    o, a, _ = W_["hand_n"]
    m = Image.new("L", (film.W * 2, film.H * 2), 0); d = ImageDraw.Draw(m)
    for poly in shp:
        d.polygon([((o[0] + q[0]) * 2 * 1.55 / 1.55, (o[1] + q[1]) * 2) for q in (rigs._rot((x * film.GIRL.scale, y * film.GIRL.scale), a) for x, y in poly)], fill=255)
    arr = np.array(m); ys, xs = np.nonzero(arr)
    ImageDraw.floodfill(m, (int(xs[0]), int(ys[0])), 128)
    comps = 1 + (1 if (np.array(m) == 255).any() else 0)
    worst_cc = max(worst_cc, comps)
check("thumb joined: hand + thumb one connected component (every grasp frame)", worst_cc == 1, {"max_components": worst_cc})

# ---- 8 (round 2) the dog in threshold (luma < 70): its own shape, >= 3 px from everything else (paw-ground contact allowed), 4 leg runs + tail
def dog_threshold_check(t):
    f = int(round(t * film.FPS))
    film.SKIP_DOG = False
    full = np.array(film.render_frame(f).convert("L")) < 70
    drawn = list(film.DOG_DRAWN)
    film.SKIP_DOG = True
    other = np.array(film.render_frame(f).convert("L")) < 70
    film.SKIP_DOG = False
    if not drawn:
        return {"t": t, "dog": False}
    polys, Wd = drawn[0]
    dm_img = Image.new("L", (film.W, film.H), 0); dd = ImageDraw.Draw(dm_img)
    for poly in polys: dd.polygon(poly, fill=255)
    dm = np.array(dm_img) > 127
    halo = np.array(dm_img.filter(ImageFilter.MaxFilter(7))) > 127   # 3 px ring
    allow = np.zeros_like(dm)
    for n in ("hshin_n", "hshin_f", "fpaw_n", "fpaw_f"):
        ex, ey = Wd[n][2]
        allow[max(0, min(int(ey) - 8, film.FLOOR - 24)):int(ey) + 12, max(0, int(ex) - 16):int(ex) + 16] = True   # paw on the ground (incl. grass tips)
    touching = int((halo & other & ~allow).sum())
    ys, xs = np.nonzero(dm); seed = (int(xs[len(xs) // 2]), int(ys[len(ys) // 2]))
    ff = dm_img.point(lambda v: 255 if v > 127 else 0); ImageDraw.floodfill(ff, seed, 128)
    one = int((np.array(ff) == 255).sum()) <= 4   # ignore anti-alias crumbs of <= 4 px
    x0, x1 = xs.min(), xs.max()
    row = full[film.FLOOR - 26, max(0, x0 - 2):min(film.W, x1 + 3)].astype(int)
    runs = int(((row[1:] - row[:-1]) == 1).sum() + row[0])
    te = Wd["tail"][2]
    tail = 0 <= te[0] < film.W and dm[min(film.H - 1, int(te[1])), min(film.W - 1, int(te[0]))] or bool(dm[max(0, int(te[1]) - 2):int(te[1]) + 3, max(0, int(te[0]) - 2):int(te[0]) + 3].any())
    return {"t": round(t, 3), "touching_px_within_3px": touching, "one_shape": bool(one), "leg_runs_at_floor-26": runs, "tail_visible": bool(tail),
            "ok": touching == 0 and one and runs == 4 and bool(tail)}
times = [film.T(285.5), 132.0] + [60.0 + k / film.FPS for k in range(int(2.5 * film.FPS) + 1)]
rows8 = [dog_threshold_check(t) for t in times]
bad8 = [r for r in rows8 if not r.get("ok")]
check("dog in threshold: separate shape, >=3 px gap, 4 legs + tail (return, rain 132 s, night 60-62.5 s)", not bad8,
      {"frames": len(rows8), "failures": bad8[:4], "sample": rows8[:2]})

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "invariants.json")
json.dump({"suite": "corrugated-sky invariants", "results": res, "all_pass": all(r["pass"] for r in res)}, open(out, "w"), indent=1)
sys.exit(0 if all(r["pass"] for r in res) else 1)
