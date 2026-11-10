"""Phase visualiser: unwrapped phase of A and B in the proof, their difference, the event beats, and the bank
locked vs detuned. Writes phase-visualiser.png."""
import sys, os, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
from PIL import Image, ImageDraw
from engine import font, FONT_MONO
W_, H_ = 1600, 900
im = Image.new("RGB", (W_, H_), (8, 9, 12)); d = ImageDraw.Draw(im)
f = font(FONT_MONO, 20); fs = font(FONT_MONO, 15)
ang = lambda P, j: math.atan2((P[j][1] - film.CY) / 0.8, P[j][0] - film.CX)
bs = np.arange(48, 76.001, 0.02)
th = np.unwrap(np.array([[ang(film.ring(b)[0], j) for j in (0, 10)] for b in bs]), axis=0)
th -= th[0]
x0, y0, w, h = 80, 70, 900, 360
X = lambda b: x0 + (b - 48) / 28 * w
Y = lambda v: y0 + h - v / (6 * math.pi) * h
d.rectangle([x0, y0, x0 + w, y0 + h], outline=(60, 60, 70))
d.text((x0, 30), "PROOF b48-76 · unwrapped phase (laps): A = 3, B = 2 over b52-72", font=f, fill=(230, 230, 220))
for k in range(4):
    d.line([(x0, Y(k * 2 * math.pi)), (x0 + w, Y(k * 2 * math.pi))], fill=(30, 30, 38)); d.text((x0 - 60, Y(k * 2 * math.pi) - 8), f"{k} lap", font=fs, fill=(120, 120, 130))
for col, k in (((255, 186, 104), 0), ((118, 206, 255), 1)):
    d.line([(X(b), Y(v)) for b, v in zip(bs, th[:, k])], fill=col, width=3)
rel = th[:, 0] - th[:, 1]
d.line([(X(b), Y(v)) for b, v in zip(bs, rel)], fill=(242, 56, 44), width=2)
for e in film.EVENTS:
    if 48 <= e["b"] <= 76:
        c = (255, 255, 255) if e["kind"] == "reunion" else (150, 150, 160)
        d.line([(X(e["b"]), y0), (X(e["b"]), y0 + h)], fill=c, width=1)
        d.text((X(e["b"]) - 8, y0 + h + 6), str(int(e["b"])), font=fs, fill=c)
d.text((x0, y0 + h + 32), "amber A (0-9) · blue B (10-19) · red A-B: 1 lap = 9 passes (grey) between reunions (white)", font=fs, fill=(200, 200, 200))
# bank: locked vs detuned traces of 4 boxes
for n, (det, lo, title) in enumerate(((0.0, 84, "RATIONAL LOCK b84-100: figures close"), (0.06, 116, "DETUNED DRIFT b116-132: figures do not close"))):
    ox = 1040; oy = 60 + n * 420
    d.text((ox, oy - 26), title, font=f, fill=(230, 230, 220))
    d.rectangle([ox, oy, ox + 500, oy + 340], outline=(60, 60, 70))
    for j, col in ((0, (255, 186, 104)), (3, (255, 140, 90)), (12, (118, 206, 255)), (15, (160, 230, 255))):
        pts = [film.bank(b, det, 0.85)[j] for b in np.arange(lo, lo + 16.001, 0.05)]
        pts = [(ox + 250 + (p[0] - film.CX) * 0.3, oy + 170 + (p[1] - film.CY) * 0.6) for p in pts]
        d.line(pts, fill=col, width=2)
        d.ellipse([pts[0][0] - 5, pts[0][1] - 5, pts[0][0] + 5, pts[0][1] + 5], outline=(255, 255, 255))
        d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3], fill=col)
d.text((80, 520), "white ring = start of the 16-beat window · dot = end. Locked: dot sits in the ring. Detuned: it does not.", font=fs, fill=(200, 200, 200))
im.save(os.path.join(film.ROOT, "phase-visualiser.png"))
print("ok")
