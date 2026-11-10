"""Cutout silhouettes and multiplane plates for THE WHOLE PACKAGE (all procedural unless the ledger says so)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from engine import W, H, LEDGER, cut_photo, _src, print_tone, INK
from mp import F, HORIZON, proj, scale_at

SIL = (24, 22, 34)          # silhouette ink (blue-black)
KRAFT = (178, 138, 88)
KRAFT_D = (140, 104, 62)
WARM = (255, 196, 110)

LEDGER["procedural"] = {"kind": "procedural", "note": "woman, house, village, hills, grass, laundry, arm, fog, sky drawn in code",
                        "rights": "original drawing for this video"}


def _poly(d, pts, fill, ss, ox, oy):
    d.polygon([(ox + x * ss, oy + y * ss) for x, y in pts], fill=fill)


def woman(dst, x, y, s, pose="stand", face=1, phase=0.0, box=False, head_turn=0.0, reach=0.0, arch=0.0,
          color=SIL, alpha=255, baby=False):
    """Draw the woman with feet at screen (x, y), world height 150 * s px. Returns her hand point (screen)."""
    ss = 2
    sc = s * ss
    pad = int(200 * s * ss) + 8
    im = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ox, oy = pad, pad + int(40 * sc)
    f = face
    c = color + (alpha,)
    X = lambda px: px * f

    def P(pts):
        return [(ox + X(px) * sc, oy + py * sc) for px, py in pts]

    def line(a, b, w):
        d.line(P([a, b]), fill=c, width=max(1, int(w * sc)))
        for p in (a, b):
            q = P([p])[0]; r = w * sc / 2; d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=c)

    step = math.sin(phase) if pose == "walk" else 0.0
    if pose == "sit":
        hip = (0, -44)
        sh = (4 - 10 * arch, -92 + 6 * arch)
        head = (8 - 18 * arch, -110 + 10 * arch)
        d.polygon(P([(-14, -40), (16, -40), (40, -30), (44, -4), (30, 0), (-16, 0)]), fill=c)         # skirt over knees
        d.polygon(P([(sh[0] - 10, sh[1]), (sh[0] + 10, sh[1] - 2), (14, -66), (2, -42), (-12, -44)]), fill=c)
        q0 = P([(2, -80)])[0]; q1 = P([(26, -48)])[0]
        d.ellipse([min(q0[0], q1[0]), q0[1], max(q0[0], q1[0]), q1[1]], fill=c)
    else:
        hip = (0, -72)
        sh = (4, -118)
        head = (8 + 2 * head_turn, -134)
        # wrapper skirt with sway
        sw = 4 * step
        d.polygon(P([(-12, -78), (14, -78), (17 + sw, -8), (-15 + sw, -8)]), fill=c)
        # torso + belly
        d.polygon(P([(-9, -122), (12, -120), (14, -100), (6, -76), (-12, -76), (-11, -100)]), fill=c)
        bl = P([(0, -104)])[0]; br = P([(30, -72)])[0]
        d.ellipse([min(bl[0], br[0]), bl[1], max(bl[0], br[0]), br[1]], fill=c)
        # feet
        for k in (-1, 1):
            fx = 10 * step * k
            q0 = P([(fx - 6, -8)])[0]; q1 = P([(fx + 10, 0)])[0]
            d.ellipse([min(q0[0], q1[0]), q0[1], max(q0[0], q1[0]), q1[1]], fill=c)
    # neck + head + head-wrap
    line((sh[0] + 2, sh[1] - 4), (head[0] - 1, head[1] + 6), 6)
    hc = P([head])[0]; r = 9 * sc
    d.ellipse([hc[0] - r, hc[1] - r, hc[0] + r, hc[1] + r], fill=c)
    wrap = P([(head[0] - 11, head[1] - 4), (head[0] + 8, head[1] - 12), (head[0] + 2, head[1] - 24), (head[0] - 14, head[1] - 20)])
    d.polygon(wrap, fill=c)
    kn = P([(head[0] - 14, head[1] - 22)])[0]; d.ellipse([kn[0] - 5 * sc, kn[1] - 5 * sc, kn[0] + 5 * sc, kn[1] + 5 * sc], fill=c)
    # nose / chin profile so facing reads in pure silhouette
    d.polygon(P([(head[0] + 8, head[1] - 3), (head[0] + 13, head[1] + 1), (head[0] + 8, head[1] + 3)]), fill=c)
    # arms
    hand = None
    if pose == "walk":
        a1 = (sh[0] + 14 * step, sh[1] + 34); a2 = (sh[0] - 14 * step + 4, sh[1] + 30)
        line(sh, a1, 6); line(sh, a2, 6); hand = a1
    elif pose == "sit":
        line(sh, (20, -66), 6); line((20, -66), (12, -60), 5); hand = (12, -60)
    elif pose == "hold" or baby:
        line(sh, (18, -92), 6); line((18, -92), (26, -100), 5); hand = (26, -100)
    else:
        # reach: 0 = arm down, 1 = arm stretched forward-low toward a nearer hand
        ang = math.radians(10 + 70 * reach)
        e = (sh[0] + 30 * math.sin(ang), sh[1] + 30 * math.cos(ang))
        hnd = (e[0] + 30 * math.sin(ang * 1.1), e[1] + 30 * math.cos(ang * 1.1))
        line(sh, e, 6); line(e, hnd, 5); hand = hnd
        line(sh, (sh[0] - 4, sh[1] + 32), 6)
    if box:
        b0 = P([(-34, -124)])[0]; b1 = P([(-8, -84)])[0]
        d.rectangle([min(b0[0], b1[0]), b0[1], max(b0[0], b1[0]), b1[1]], fill=KRAFT_D + (alpha,), outline=c, width=int(2 * sc))
    if baby:
        # round 5: a small swaddled bundle in her arms - one soft silhouette, no box, no rim, no knob
        q0 = P([(10, -108)])[0]; q1 = P([(40, -90)])[0]
        d.ellipse([min(q0[0], q1[0]), q0[1], max(q0[0], q1[0]), q1[1]], fill=c)
    im = im.resize((im.width // ss, im.height // ss), Image.LANCZOS)
    from engine import _ac
    _ac(dst, im, x - ox / ss, y - oy / ss)
    hx, hy = hand
    return (x + X(hx) * s, y + hy * s)


# ------------------------------------------------------------------ house of boxes (z = 6, drawn 1:1)
def box_face(d, x0, y0, x1, y1, seed, label=None):
    rnd = random.Random(seed)
    tone = tuple(int(v * rnd.uniform(0.9, 1.06)) for v in KRAFT)
    d.rectangle([x0, y0, x1, y1], fill=tone, outline=(70, 50, 30), width=3)
    for xx in range(int(x0) + 6, int(x1) - 2, 7):
        d.line([(xx, y0 + 3), (xx, y1 - 3)], fill=tuple(int(v * 0.93) for v in tone), width=1)
    ty = (y0 + y1) / 2 + rnd.uniform(-8, 8)
    d.rectangle([x0, ty - 6, x1, ty + 6], fill=(206, 176, 120), outline=None)          # tape band
    if label:
        d.text((x0 + 10, y0 + 8), label, fill=(60, 30, 26))


def make_house():
    """Stack of corrugated boxes, a door, one round window (the eye). Pivot: bottom-centre at (0, 0)."""
    w, h = 420, 360
    im = Image.new("RGBA", (w, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rows = [(h - 120, h, [(10, 150), (150, 290), (290, 410)]),
            (h - 230, h - 120, [(40, 200), (200, 380)]),
            (h - 330, h - 230, [(110, 310)])]
    k = 0
    for y0, y1, cols in rows:
        for x0, x1 in cols:
            box_face(d, x0, y0, x1, y1, k, label=["FRAGILE", None, "THIS SIDE UP", None, "HANDLE WITH CARE", None][k % 6]); k += 1
    # flaps on the top box
    d.polygon([(110, h - 330), (150, h - 352), (220, h - 352), (210, h - 330)], fill=KRAFT_D, outline=(70, 50, 30))
    d.polygon([(210, h - 330), (230, h - 354), (300, h - 352), (310, h - 330)], fill=KRAFT_D, outline=(70, 50, 30))
    LEDGER["house"] = {"kind": "procedural", "note": "box house", "rights": "original"}
    return im, (w / 2, h)
HOUSE_DOOR = (150, 250, 230, 360)     # in house image px (x0, y0, x1, y1)
HOUSE_EYE = (210, 85, 34)             # centre x, y, radius (in the top box)


def make_village():
    """Neighbours' houses: z = 14 plate. Returns image (world units / z scaled) + window rects."""
    s = F / 14
    w = int(3400 * s); h = int(420 * s)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rnd = random.Random(4); wins = []
    x = 20
    while x < w - 80:
        bw = rnd.randint(70, 120); bh = rnd.randint(60, 110)
        y1 = h; y0 = h - bh
        d.rectangle([x, y0, x + bw, y1], fill=(58, 52, 66))
        d.polygon([(x - 8, y0), (x + bw / 2, y0 - rnd.randint(24, 40)), (x + bw + 8, y0)], fill=(48, 42, 56))
        for j in range(rnd.randint(1, 2)):
            wx = x + 12 + j * 38; wy = y0 + 18
            wins.append((wx, wy, wx + 24, wy + 26))
        x += bw + rnd.randint(30, 90)
    return im, wins, s


def make_hills(z, seed, color, amp, height, width_world=6000):
    s = F / z
    w = int(width_world * s); h = int(height * s) + 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rnd = random.Random(seed)
    pts = [(0, h)]
    ph = [rnd.uniform(0, 6) for _ in range(3)]
    for x in range(0, w + 8, 8):
        y = h * 0.45 - amp * s * (0.5 * math.sin(x / (180 * s) + ph[0]) + 0.3 * math.sin(x / (70 * s) + ph[1]) + 0.2 * math.sin(x / (31 * s) + ph[2]))
        pts.append((x, y))
    pts.append((w, h))
    d.polygon(pts, fill=color)
    return im, s


def sheet_poly(x0, y0, w, h, t, seed, wind=1.0):
    """A flapping sheet hung from (x0, y0): the hem waves with wind."""
    pts = [(x0, y0), (x0 + w, y0)]
    n = 10
    for i in range(n + 1):
        u = 1 - i / n
        xx = x0 + w * u + wind * 16 * math.sin(t * 6 + u * 4 + seed)
        yy = y0 + h + wind * 9 * math.sin(t * 7.3 + u * 6 + seed * 2)
        pts.append((xx + wind * 10, yy))
    return pts


def grass_strip(d, cam_x, z, t, wind, color, seed=1, dens=60, tall=340):
    """Foreground clumps of grass with pollen seed-heads on plane z (drawn per frame: they sway)."""
    s = F / z
    rnd = random.Random(seed)
    for i in range(dens):
        wx = rnd.uniform(-3000, 6000); hh0 = rnd.uniform(0.35, 0.75); nb = rnd.randint(5, 9); ph = rnd.uniform(0, 6)
        sx = W / 2 + (wx - cam_x) / z * F
        if sx < -200 or sx > W + 200:
            continue
        base = H + 10
        for k in range(nb):
            hh = hh0 * tall * s / 2 * (0.55 + 0.45 * ((k * 37) % 10) / 10)
            lean = (k - nb / 2) * 7 * s / 4
            bend = wind * 26 * s / 4 * math.sin(t * 2.2 + ph + k * 0.4) + wind * 26 * s / 4 + lean
            x0 = sx + (k - nb / 2) * 4 * s / 4
            mid = (x0 + bend * 0.35, base - hh * 0.55); top = (x0 + bend, base - hh)
            d.line([(x0, base), mid, top], fill=color, width=max(2, int(2.2 * s / 2)), joint="curve")
            if k % 3 == 0:
                rr = 3.5 * s / 4
                for kk in range(6):
                    an = kk / 6 * 6.283; q = (top[0] + math.cos(an) * rr * 1.5, top[1] + math.sin(an) * rr * 1.5)
                    d.ellipse([q[0] - rr, q[1] - rr, q[0] + rr, q[1] + rr], fill=color)


def grass_clump(d, cam_x, z, t, wind, color, wx, tall=420):
    s = F / z
    sx = W / 2 + (wx - cam_x) / z * F
    base = H + 10
    for k in range(9):
        hh = tall * s / 2 * (0.6 + 0.4 * ((k * 37) % 10) / 10)
        bend = wind * 20 * s / 4 * math.sin(t * 2.0 + k * 0.5) + (k - 4) * 9 * s / 4
        x0 = sx + (k - 4) * 6 * s / 4
        d.line([(x0, base), (x0 + bend * 0.35, base - hh * 0.55), (x0 + bend, base - hh)], fill=color, width=max(3, int(3 * s / 2)), joint="curve")
        if k % 2 == 0:
            rr = 4 * s / 4; top = (x0 + bend, base - hh)
            for kk in range(6):
                an = kk / 6 * 6.283; q = (top[0] + math.cos(an) * rr * 1.5, top[1] + math.sin(an) * rr * 1.5)
                d.ellipse([q[0] - rr, q[1] - rr, q[0] + rr, q[1] + rr], fill=color)


def make_package():
    """The baby's box: wrapped with the producer's HANDLE WITH CARE label (album fragment)."""
    lab = cut_photo("Boxback lumbar brace flat-lay.png", (470, 470, 800, 650), "package_label", height=40, rough=1.5, edge=2)
    return lab
