"""Halftone film banks for the in-scene films: per film, frames x gh x gw uint8 (0..7 ink level, 255 = no dot).
Dot law (WYGWYL): 8 levels, one ordered Bayer pass; a cut subject keeps dots only inside its SAM mask.
usage: python3 -I build_bank.py <bank-spec.json> <outdir>"""
import sys, json, os, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jellycut import BAYER8, load_frames, Still, FilmClock
spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True); man = {}
for f in spec["films"]:
    s = f["source"]
    src = FilmClock(s["npy"]) if s["kind"] == "film" else (Still(s["image"]) if s["kind"] == "still" else load_frames(s["frames"], s.get("masks"), s.get("cut", False)))
    gw = f["gw"]; n = int(round(f["dur"] * 12)); frames = []
    for i in range(n):
        tau = f["src_t0"] + i / 12
        lum, mask = src.at(tau)
        if f.get("crop"):
            cr = f["crop"]; hh, ww = lum.shape; y0, y1, x0, x1 = int(cr[1] * hh), int(cr[3] * hh), int(cr[0] * ww), int(cr[2] * ww)
            lum = lum[y0:y1, x0:x1]; mask = mask[y0:y1, x0:x1] if mask is not None else None
        gh = max(6, int(round(gw * lum.shape[0] / lum.shape[1])))
        L = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).resize((gw, gh), Image.LANCZOS), np.float32) / 255
        sub = None
        if mask is not None:
            sub = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).resize((gw, gh), Image.BILINEAR), np.float32) / 255 > 0.5
        v = L[sub] if sub is not None and sub.any() else L
        lo, hi = np.percentile(v, 4), np.percentile(v, 96); L = np.clip((L - lo) / max(.05, hi - lo), 0, 1) ** 1.1
        q = np.floor(L * 7.999).astype(np.uint8); yy, xx = np.mgrid[0:gh, 0:gw]
        lit = (q / 7.0) > BAYER8[yy % 8, xx % 8]
        if sub is not None: lit &= sub
        frames.append(np.where(lit, q, 255).astype(np.uint8))
    gh = frames[0].shape[0]; frames = [fr if fr.shape[0] == gh else np.asarray(Image.fromarray(fr).resize((gw, gh), Image.NEAREST)) for fr in frames]
    A = np.stack(frames); A.tofile(os.path.join(out, f["id"] + ".bin"))
    # where the dog is, in the film's own normalised coordinates (for the let-go target)
    man[f["id"]] = {"gw": gw, "gh": gh, "n": n, "fps": 12, "file": f["id"] + ".bin", "lit_frac": round(float((A != 255).mean()), 3)}
    print(f["id"], A.shape, man[f["id"]]["lit_frac"])
json.dump(man, open(os.path.join(out, "bank.json"), "w"), indent=1)
