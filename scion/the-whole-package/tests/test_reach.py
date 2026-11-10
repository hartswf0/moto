"""Round-2 assertions for the nearer-hand shot (b137-139) and the baby close-up.  python3 -I tests/test_reach.py
(a) the arm root lies inside the house-box silhouette and inside the frame; the house is not a ghost:
    fog opacity in front of the house (slab z 6 -> 4.2) < 0.35 for every frame b137-139
(b) depth order: ARM_Z < STALK_Z < her z, the arm is drawn after fog/focus (no blur), and its chain crosses the stalk's screen x
(c) finger count: the hand drawn alone, downsampled to 360 px wide, sampled on an arc through the fingers -> >= 3 separate runs
(e) baby: >= 4 px gap at 360 px between her head (circle + face) and every baby shape
"""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import numpy as np
from PIL import Image, ImageDraw
import film
from mp import proj, F
from engine import W, H
film.assets()
res = []; ok_all = True
def rec(name, ok, d):
    global ok_all; ok_all &= bool(ok); res.append({"test": name, "pass": bool(ok), "detail": d}); print(("PASS " if ok else "FAIL ") + name, d)

frames = [f for f in range(int(film.T(137) * 24), int(film.T(139) * 24) + 1)]
inside = []; fogmax = 0
house_alpha = np.asarray(film.A["house"].split()[3])
for f in frames:
    b = film.B(f / 24); g = film.reach_geometry(b)
    x0, y0, x1, y1 = g["house_box"]; rx, ry = g["root"]
    ix, iy = int(rx - x0), int(ry - y0)
    on = 0 <= ix < house_alpha.shape[1] and 0 <= iy < house_alpha.shape[0] and house_alpha[iy, ix] > 128
    inside.append(on and 0 <= rx < W and 0 <= ry < H)
    _, sigma = film.fog_state(b)
    zs = np.linspace(4.2, 6.0, 30); tau = sum(sigma((zs[i] + zs[i + 1]) / 2) * (zs[i + 1] - zs[i]) for i in range(29))
    fogmax = max(fogmax, 1 - math.exp(-tau * 6.0))
rec("(a) arm root on the house silhouette, in frame, b137-139", all(inside), {"frames": len(frames), "inside": sum(inside)})
rec("(a) house visible: fog opacity in front of it < 0.35, b137-139", fogmax < 0.35, {"max_opacity": round(fogmax, 3)})

wz = film.woman_path(138)[1]
b = 138.6; cam = film.camera(b); sx = proj(film.STALK_WX, 0, film.STALK_Z, cam)[0]
ch = film.reach_geometry(b)["chain"]
xs = [p[0] for p in ch]
crosses = any(min(xs[i], xs[i + 1]) <= sx <= max(xs[i], xs[i + 1]) for i in range(len(xs) - 1))
rec("(b) arm nearer than stalk and her; drawn after fog; crosses the stalk", film.ARM_Z < film.STALK_Z < wz and film.ARM_DRAWN_AFTER_FOG and crosses,
    {"ARM_Z": film.ARM_Z, "STALK_Z": film.STALK_Z, "her_z": wz, "stalk_screen_x": round(sx), "chain_x": [round(v) for v in xs]})

m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
g = film.reach_geometry(139.0); ch = g["chain"]; ang = math.atan2(ch[-1][1] - ch[-2][1], ch[-1][0] - ch[-2][0])
film.draw_hand(d, ch[-1], ang, 255, 255)
sc = 360 / W; small = np.asarray(m.resize((360, int(H * sc)), Image.LANCZOS)) > 127
P = film.HAND; r = (P["palm"][0] + P["finger_len"] * 0.8) * sc
cx, cy = ch[-1][0] * sc, ch[-1][1] * sc
vals = []
for k in range(400):
    a2 = ang + math.radians(-70 + 140 * k / 399)
    x, y = int(round(cx + math.cos(a2) * r)), int(round(cy + math.sin(a2) * r))
    vals.append(bool(small[y, x]) if 0 <= x < small.shape[1] and 0 <= y < small.shape[0] else False)
runs = sum(1 for i in range(1, len(vals)) if vals[i] and not vals[i - 1]) + (1 if vals[0] else 0)
rec("(c) >= 3 separate finger shapes at 360 px", runs >= 3, {"runs_on_arc": runs, "arc_radius_px_at_360": round(r, 1)})

G = film.baby_geometry(540, 790, 2.7)
hx, hy, hr = G["her_head"]; fx, fy = G["her_face_tip"]
def dist_rect(px, py, R):
    x0, y0, x1, y1 = R; dx = max(x0 - px, 0, px - x1); dy = max(y0 - py, 0, py - y1); return math.hypot(dx, dy)
shapes = {k: G[k] for k in ("box", "body", "head", "fist")}
gap = min(min(dist_rect(hx, hy, R) - hr, dist_rect(fx, fy, R)) for R in shapes.values())
rec("(e) baby separated from her head by >= 4 px at 360 px", gap * 360 / W >= 4, {"gap_px_full": round(gap, 1), "gap_px_at_360": round(gap * 360 / W, 1)})
json.dump({"suite": "reach-round2", "results": res, "all_pass": ok_all}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reach-tests.json"), "w"), indent=1)
sys.exit(0 if ok_all else 1)
