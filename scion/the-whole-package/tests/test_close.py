"""Round-4 close shot (about 129 s): python3 -I tests/test_close.py
(1) the baby's head is >= 18% of frame height
(5) the face profile, rasterised alone and downscaled to 360 px wide (no captions), shows >= 3 distinct contour changes
    (forehead-nose-lip notches): rays are cast from the head centre along the face normal at positions across the face;
    the edge radius rho(u) is smoothed and the sign changes of its second difference (|d2| >= 0.25 px) are counted.
(4) her profile is in the same frame (its polygon intersects the frame) and faces the baby (her face normal points toward it).
"""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import numpy as np
from PIL import Image, ImageDraw
import film
from engine import W, H
res = []; ok_all = True
def rec(name, ok, d):
    global ok_all; ok_all &= bool(ok); res.append({"test": name, "pass": bool(ok), "detail": d}); print(("PASS " if ok else "FAIL ") + name, d)
C = film.CLOSE; c, r, th = C["baby_c"], C["baby_r"], C["baby_th"]
poly, face, eye = film.baby_face_profile(c, r, th)
ys = [p[1] for p in poly]; frac = (max(ys) - min(ys)) / H
rec("(1) baby head >= 18% of frame height", frac >= 0.18, {"head_height_px": round(max(ys) - min(ys)), "fraction": round(frac, 3)})
m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
sc = 360 / W; small = np.asarray(m.resize((360, int(round(H * sc))), Image.LANCZOS)) > 127
n = (math.cos(th), math.sin(th)); t = (math.sin(th), -math.cos(th)); t = (-t[0], -t[1]) if t[1] < 0 else t
cs = (c[0] * sc, c[1] * sc); rs = r * sc
rho = []
for k in range(61):
    u = -0.8 + 1.6 * k / 60
    ox, oy = cs[0] + t[0] * u * rs, cs[1] + t[1] * u * rs
    last = 0.0
    for step in range(0, int(rs * 2.2 * 8)):
        dd = step / 8; x, y = int(round(ox + n[0] * dd)), int(round(oy + n[1] * dd))
        if 0 <= x < small.shape[1] and 0 <= y < small.shape[0] and small[y, x]: last = dd
    rho.append(last)
rho = np.convolve(np.array(rho), np.ones(3) / 3, mode="valid")
d2 = np.diff(rho, 2); sig = [np.sign(v) for v in d2 if abs(v) >= 0.25]
changes = sum(1 for i in range(1, len(sig)) if sig[i] != sig[i - 1])
rec("(5) >= 3 distinct contour changes on the face edge at 360 px (captions masked)", changes >= 3, {"curvature_sign_changes": int(changes), "samples": len(rho)})
HC, HR = (300.0, 250.0), 140.0
hp, hface, _ = film.baby_face_profile(HC, HR, film.HER_TH)
inframe = any(0 <= x < W and 0 <= y < H for x, y in hface)
hn = (math.cos(film.HER_TH), math.sin(film.HER_TH)); to_b = (c[0] - HC[0], c[1] - HC[1])
facing = (hn[0] * to_b[0] + hn[1] * to_b[1]) > 0
rec("(4) her profile in frame and inclined toward the baby", inframe and facing, {"her_face_points_in_frame": sum(1 for x, y in hface if 0 <= x < W and 0 <= y < H), "faces_baby": facing})
json.dump({"suite": "close-round4", "results": res, "all_pass": ok_all}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "close-tests.json"), "w"), indent=1)
sys.exit(0 if ok_all else 1)
