"""Round 5, measured on the RENDERED film (the-whole-package.mp4).  python3 -I tests/test_push.py [film.mp4]
(1) a real multiplane push: between frames A (b233.6, fog gone) and B (b236.45), >= 1.5 s apart, the scale factor of the
    NEAR region (her + baby) and of the FAR region (house, village, sky) is estimated from pixels: frame A is warped about the
    push anchor for each candidate scale and compared with B inside each region's mask (far compared after a common blur).
    Pass if near_factor / far_factor >= 1.5.
    No cross-dissolve and no cut inside the reveal: no consecutive-frame mean difference > 30 from b232.2 to the end.
(2) one caption per frame: caption-text rows (warm-white text pixels) form at most ONE cluster in every frame b200-262,
    and during the reveal (b232+) that cluster is in the bottom third (her head is never under a caption bar).
(4) her face tilts down: PCA of her rim-light pixels (left of the baby) on the held close frame, angle from vertical >= 15 deg.
"""
import sys, os, json, math, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import numpy as np
from PIL import Image, ImageFilter
import film
from engine import W, H
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "the-whole-package.mp4")
def grab(t, n=1):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.4f}", "-i", src, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
res = []; ok_all = True
def rec(name, ok, d):
    global ok_all; ok_all &= bool(ok); res.append({"test": name, "pass": bool(ok), "detail": d}); print(("PASS " if ok else "FAIL ") + name, d)

tA, tB = film.T(233.6), film.T(236.45)
A = grab(tA)[0].astype(np.float32); Bf = grab(tB)[0].astype(np.float32)
P = film.PUSH["anchor"]
lumB = Bf.mean(2); lumA = A.mean(2)
near_mask = lumB < 60                                     # her and the baby are the dark near silhouettes
near_mask[:, :420] = False; near_mask[H - 140:, :] = False   # baby + her face region; exclude the caption band
def warp(img, s):
    im = Image.fromarray(img.astype(np.uint8))
    inv = (1 / s, 0, P[0] - P[0] / s, 0, 1 / s, P[1] - P[1] / s)
    return np.asarray(im.transform((W, H), Image.AFFINE, inv, resample=Image.BILINEAR), np.float32)
def best_scale(mask, blur=0, lo=0.9, hi=2.6, steps=86):
    Bt = Bf if not blur else np.asarray(Image.fromarray(Bf.astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur)), np.float32)
    best = None
    for s in np.linspace(lo, hi, steps):
        Aw = warp(A, s)
        if blur: Aw = np.asarray(Image.fromarray(Aw.astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur)), np.float32)
        e = ((Aw - Bt) ** 2).mean(2)[mask].mean()
        if best is None or e < best[0]: best = (e, s)
    return best[1]
sn = best_scale(near_mask, lo=1.0, hi=2.6)
far_mask = (lumB > 90) & (lumA > 90); far_mask[H - 160:, :] = False
far_mask &= np.asarray(Image.fromarray((~(lumB < 60)).astype(np.uint8) * 255).filter(ImageFilter.MinFilter(41)), bool)
sf = best_scale(far_mask, blur=10, lo=0.9, hi=1.6, steps=71)
rec("(1) multiplane push: near scales >= 1.5x faster than far (rendered frames)", sn / sf >= 1.5,
    {"seconds": round(tB - tA, 3), "near_factor": round(float(sn), 3), "far_factor": round(float(sf), 3), "ratio": round(float(sn / sf), 3),
     "expected_from_timeline": [round(film.push_scales(236.45)[0] / film.push_scales(233.6)[0], 3), round(film.push_scales(236.45)[1] / film.push_scales(233.6)[1], 3)]})

t0 = film.T(232.2); n = int((film.DUR - 0.2 - t0) * 24)
fr = grab(t0, n).astype(np.float32)
small = fr[:, ::4, ::4, :].mean(3)
diffs = np.abs(np.diff(small, axis=0)).mean((1, 2))
rec("(1) no dissolve/cut inside the reveal (max consecutive-frame diff <= 30)", diffs.max() <= 30, {"frames": int(n), "max_diff": round(float(diffs.max()), 2), "mean_diff": round(float(diffs.mean()), 3)})

t0 = film.T(200); n = int((film.T(262) - t0) * 24)
fr = grab(t0, n)
bad = 0; top_in_reveal = 0
for i in range(0, n):
    f = fr[i]; txt = (f[..., 0] > 235) & (f[..., 1] > 215) & (f[..., 2] > 175) & (f[..., 2] < 230)
    rows = np.where(txt.sum(1) >= 6)[0]
    if len(rows) == 0: continue
    clusters = 1 + int((np.diff(rows) > 60).sum())
    if clusters > 1: bad += 1
    b = film.B(t0 + i / 24)
    if b >= 232 and rows.min() < H * 2 / 3: top_in_reveal += 1
rec("(2) one caption per frame; in the reveal the caption is in the bottom third", bad == 0 and top_in_reveal == 0,
    {"frames_checked": int(n), "frames_with_2+_captions": bad, "reveal_frames_with_caption_above_bottom_third": top_in_reveal})

f = grab(film.T(240.5))[0].astype(np.int16)
rim = (f[..., 0] > 235) & (f[..., 1] > 190) & (f[..., 1] < 230) & (f[..., 2] > 110) & (f[..., 2] < 185)
rim[:, 560:] = False; rim[H - 140:, :] = False
ys, xs = np.nonzero(rim)
if len(xs) > 20:
    cov = np.cov(np.vstack([xs, ys])); w, v = np.linalg.eigh(cov); ax = v[:, -1]
    tilt = math.degrees(math.atan2(abs(ax[0]), abs(ax[1])))
else:
    tilt = 0.0
rec("(4) her face tilts down toward the baby (rim-light PCA, deg from vertical)", tilt >= 15, {"rim_pixels": int(len(xs)), "tilt_deg": round(tilt, 1)})
json.dump({"suite": "push-round5", "source": os.path.basename(src), "results": res, "all_pass": ok_all},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "push-tests.json"), "w"), indent=1)
sys.exit(0 if ok_all else 1)
