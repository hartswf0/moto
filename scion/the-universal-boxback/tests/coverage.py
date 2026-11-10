"""Lit-pixel coverage per section (fraction of pixels whose max channel > 40), rendered frames every 6 frames."""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "src"))
import film
SECTIONS = [("end form", 16, 32), ("backward", 32, 48), ("proof", 48, 77), ("lock", 80, 112), ("drift", 112, 144),
            ("re-lock", 144, 160), ("making", 160, 238), ("plato", 238, 264), ("accumulation", 264.3, 303.3),
            ("points", 304, 324), ("release", 324, 348), ("rain", 348, 368)]
def coverage(b0, b1, step=6):
    f0, f1 = int(film.T(b0) * 24), int(film.T(b1) * 24)
    v = [float((np.asarray(film.render_frame(f)).max(2) > 40).mean()) for f in range(f0, f1, step)]
    return float(np.mean(v)), float(np.max(v))
if __name__ == "__main__":
    out = {n: dict(zip(("mean", "max"), [round(x, 4) for x in coverage(a, b)])) for n, a, b in SECTIONS}
    for k, v in out.items(): print(f"{k:14s} mean {v['mean']*100:5.1f}%  max {v['max']*100:5.1f}%")
    json.dump(out, open(os.path.join(HERE, "coverage.json"), "w"), indent=1)
