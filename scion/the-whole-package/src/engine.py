"""Cutout engine for WITTGENSTEIN'S BACKPACK.

Primitives kept first-class (SCION-GILLIAM §2):
  Sprite      - a cut piece of paper: RGBA image + pivot (card joint) + provenance id
  engrave()   - procedural engraved figure parts (hatch-filled polygons, ink outline)
  cut_photo() - scissor-cut fragment of an album artwork (source + crop box recorded)
  Figure      - pivot/card-joint rig, solved to world joints (FK or the constraint solver)
  Frame       - bg / fg layers; paper shadow is computed from the fg alpha each frame

Coordinates: design space is 1280x720 px, y down, angles in degrees CLOCKWISE.
Time base: seconds (float); the beat grid is in beatgrid.json.
"""
import math, os, json, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(ROOT))
ART = os.path.join(REPO, "Et tu, Brute (BOXBACK)")
W, H = 1280, 720
PAPER = (236, 226, 202)
INK = (28, 22, 18)
KRAFT = (190, 152, 104)

FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_STENCIL = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FONT_MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf"

LEDGER = {}  # sprite id -> provenance record


def font(path, size):
    return ImageFont.truetype(path, int(size))


# ---------------------------------------------------------------- sprites
class Sprite:
    def __init__(self, img, pivot, sid, provenance):
        self.img = img
        self.pivot = (float(pivot[0]), float(pivot[1]))
        self.id = sid
        self._cache = {}
        LEDGER[sid] = provenance

    @property
    def size(self):
        return self.img.size

    def variant(self, sx, sy):
        key = (round(sx, 3), round(sy, 3))
        v = self._cache.get(key)
        if v is None:
            w, h = self.img.size
            nw, nh = max(1, int(round(w * abs(sx)))), max(1, int(round(h * abs(sy))))
            im = self.img if (nw, nh) == (w, h) else self.img.resize((nw, nh), Image.LANCZOS)
            px, py = self.pivot[0] * abs(sx), self.pivot[1] * abs(sy)
            if sx < 0:
                im = ImageOps.mirror(im); px = nw - px
            if sy < 0:
                im = ImageOps.flip(im); py = nh - py
            v = (im, (px, py))
            if len(self._cache) < 64:
                self._cache[key] = v
        return v


def paper_edge(img, border=3, color=(246, 240, 226)):
    """Add the visible scissor margin around a cut piece."""
    a = img.split()[3]
    pad = border + 2
    big = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    big.paste(img, (pad, pad))
    a2 = Image.new("L", big.size, 0); a2.paste(a, (pad, pad))
    grown = a2.filter(ImageFilter.MaxFilter(2 * border + 1)).point(lambda v: 255 if v > 40 else 0)
    base = Image.new("RGBA", big.size, color + (0,)); base.putalpha(grown)
    base.alpha_composite(big)
    return base, pad


def _hatch(size, angle, gap, width, color, jitter=0.0, seed=0):
    rnd = random.Random(seed)
    w, h = size
    L = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    diag = int(math.hypot(w, h)) + 4
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    cx, cy = w / 2, h / 2
    k = -diag
    while k < diag:
        off = k + (rnd.uniform(-jitter, jitter) if jitter else 0)
        x0, y0 = cx + off * -sa - diag * ca, cy + off * ca - diag * sa
        x1, y1 = cx + off * -sa + diag * ca, cy + off * ca + diag * sa
        d.line([(x0, y0), (x1, y1)], fill=color, width=width)
        k += gap
    return L


def engrave(shapes, pivot, sid, note, ss=2, edge=3, extra_draw=None):
    """shapes: list of dict(pts=[(x,y)...] | ellipse=(x0,y0,x1,y1), fill, hatch=(angle,gap,width),
    cross=(angle,gap,width), outline=int, lines=[[(x,y),...]])  - all in design px."""
    xs, ys = [], []
    for s in shapes:
        if "pts" in s:
            xs += [p[0] for p in s["pts"]]; ys += [p[1] for p in s["pts"]]
        if "ellipse" in s:
            x0, y0, x1, y1 = s["ellipse"]; xs += [x0, x1]; ys += [y0, y1]
        for ln in s.get("lines", []):
            xs += [p[0] for p in ln]; ys += [p[1] for p in ln]
    pad = 6
    minx, miny = min(xs) - pad, min(ys) - pad
    w, h = int((max(xs) - minx + pad) * ss), int((max(ys) - miny + pad) * ss)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    T = lambda p: ((p[0] - minx) * ss, (p[1] - miny) * ss)
    for i, s in enumerate(shapes):
        mask = Image.new("L", (w, h), 0)
        md = ImageDraw.Draw(mask)
        if "pts" in s:
            md.polygon([T(p) for p in s["pts"]], fill=255)
        elif "ellipse" in s:
            x0, y0, x1, y1 = s["ellipse"]
            md.ellipse([T((x0, y0)), T((x1, y1))], fill=255)
        else:
            mask = None
        if mask is not None:
            layer = Image.new("RGBA", (w, h), s.get("fill", PAPER) + (255,))
            for key in ("hatch", "cross", "cross2"):
                if key in s:
                    ang, gap, lw = s[key]
                    layer.alpha_composite(_hatch((w, h), ang, gap * ss, max(1, int(lw * ss)),
                                                 s.get("ink", INK) + (255,), jitter=0.6 * ss, seed=i * 7 + len(key)))
            img.paste(layer, (0, 0), mask)
            ow = s.get("outline", 2)
            if ow:
                d = ImageDraw.Draw(img)
                if "pts" in s:
                    pts = [T(p) for p in s["pts"]]
                    d.line(pts + [pts[0]], fill=INK + (255,), width=int(ow * ss), joint="curve")
                else:
                    x0, y0, x1, y1 = s["ellipse"]
                    d.ellipse([T((x0, y0)), T((x1, y1))], outline=INK + (255,), width=int(ow * ss))
        d = ImageDraw.Draw(img)
        for ln in s.get("lines", []):
            d.line([T(p) for p in ln], fill=s.get("line_color", INK) + (255,), width=max(1, int(s.get("lw", 1.5) * ss)), joint="curve")
    if extra_draw:
        extra_draw(ImageDraw.Draw(img), T, ss)
    img = img.resize((max(1, w // ss), max(1, h // ss)), Image.LANCZOS)
    pv = ((pivot[0] - minx), (pivot[1] - miny))
    if edge:
        img, p = paper_edge(img, edge)
        pv = (pv[0] + p, pv[1] + p)
    return Sprite(img, pv, sid, {"kind": "procedural-engraving", "note": note,
                                  "rights": "original procedural drawing made for this video (no third-party source)"})


def _rough_poly(box, n=10, amp=5, seed=1):
    """Scissor path around a crop box: jittered rectangle."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    pts = []
    for i in range(n):
        pts.append((x0 + (x1 - x0) * i / n, y0 + rnd.uniform(-amp, amp)))
    for i in range(n):
        pts.append((x1 + rnd.uniform(-amp, amp), y0 + (y1 - y0) * i / n))
    for i in range(n):
        pts.append((x1 - (x1 - x0) * i / n, y1 + rnd.uniform(-amp, amp)))
    for i in range(n):
        pts.append((x0 + rnd.uniform(-amp, amp), y1 - (y1 - y0) * i / n))
    return pts


_SRC = {}


def _src(name):
    if name not in _SRC:
        _SRC[name] = Image.open(os.path.join(ART, name)).convert("RGB")
    return _SRC[name]


def print_tone(im, sat=0.85, contrast=1.12, warm=True):
    """Shared material palette so photo fragments sit with the engravings."""
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    if warm:
        r, g, b = im.split()
        r = r.point(lambda v: min(255, int(v * 1.04 + 6)))
        b = b.point(lambda v: int(v * 0.9))
        im = Image.merge("RGB", (r, g, b))
    return im


def cut_photo(src, poly, sid, height=None, pivot="center", edge=4, tone=True, rough=0, seed=3):
    """poly: list of (x,y) in source px, or a crop box (x0,y0,x1,y1)."""
    im = _src(src)
    if len(poly) == 4 and not isinstance(poly[0], tuple):
        box = poly
        poly = _rough_poly(box, amp=rough, seed=seed) if rough else [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    bx = (int(max(0, min(xs))), int(max(0, min(ys))), int(min(im.width, max(xs))), int(min(im.height, max(ys))))
    crop = im.crop(bx)
    if tone:
        crop = print_tone(crop)
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).polygon([(p[0] - bx[0], p[1] - bx[1]) for p in poly], fill=255)
    rgba = crop.convert("RGBA"); rgba.putalpha(mask)
    if height:
        s = height / rgba.height
        rgba = rgba.resize((max(1, int(rgba.width * s)), int(height)), Image.LANCZOS)
    else:
        s = 1.0
    if pivot == "center":
        pv = (rgba.width / 2, rgba.height / 2)
    elif pivot == "bottom":
        pv = (rgba.width / 2, rgba.height)
    elif pivot == "left":
        pv = (0, rgba.height / 2)
    else:
        pv = ((pivot[0] - bx[0]) * s, (pivot[1] - bx[1]) * s)
    if edge:
        rgba, p = paper_edge(rgba, edge)
        pv = (pv[0] + p, pv[1] + p)
    return Sprite(rgba, pv, sid, {"kind": "album-art-fragment", "source": "Et tu, Brute (BOXBACK)/" + src,
                                   "crop_box_px": list(bx), "polygon_px": [list(map(float, p)) for p in poly],
                                   "rights": "producer's own BOXBACK album artwork in this repository (hartswf0/moto)"})


def text_tag(text, sid, size=40, fg=INK, bg=KRAFT, fontpath=FONT_STENCIL, padx=22, pady=12, tilt_seed=0, hatch=True):
    f = font(fontpath, size)
    tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
    lines = text.split("\n")
    bbs = [tmp.textbbox((0, 0), ln, font=f) for ln in lines]
    tw = max(b[2] - b[0] for b in bbs); lh = int(size * 1.15)
    w, h = tw + 2 * padx, lh * len(lines) + 2 * pady
    im = Image.new("RGBA", (w, h), bg + (255,))
    if hatch:
        im.alpha_composite(_hatch((w, h), 0, 5, 1, (0, 0, 0, 22), seed=tilt_seed))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        bb = bbs[i]
        d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], pady + i * lh), ln, font=f, fill=fg)
    poly = _rough_poly((0, 0, w, h), n=6, amp=2.5, seed=tilt_seed + 11)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    im.putalpha(m)
    im, p = paper_edge(im, 3)
    return Sprite(im, (im.width / 2, im.height / 2), sid, {"kind": "caption-tag", "text": text,
                                                            "rights": "original text set in a system font"})


# ---------------------------------------------------------------- frame + blit
class Frame:
    def __init__(self, bg):
        self.bg = bg.copy() if bg is not None else Image.new("RGBA", (W, H), PAPER + (255,))
        self.layers = [Image.new("RGBA", (W, H), (0, 0, 0, 0))]
        self.over = Image.new("RGBA", (W, H), (0, 0, 0, 0))  # no shadow (captions / UI)

    @property
    def fg(self):
        return self.layers[-1]

    def new_layer(self):
        self.layers.append(Image.new("RGBA", (W, H), (0, 0, 0, 0)))

    def compose(self, shadow=(6, 8), shadow_alpha=0.5, flash=0.0):
        out = self.bg.copy()
        for L in self.layers:
            if shadow:
                a = L.split()[3].filter(ImageFilter.BoxBlur(4)).point(lambda v: int(v * shadow_alpha))
                sh = Image.new("RGBA", (W, H), (20, 12, 8, 0)); sh.putalpha(a)
                out.alpha_composite(sh, (shadow[0], shadow[1])) if False else _ac(out, sh, shadow[0], shadow[1])
            out.alpha_composite(L)
        out.alpha_composite(self.over)
        if flash > 0:
            out = Image.blend(out, Image.new("RGBA", (W, H), (255, 250, 238, 255)), min(1, flash))
        return out


def _ac(dst, src, x, y):
    x, y = int(round(x)), int(round(y))
    sx0, sy0 = max(0, -x), max(0, -y)
    dx0, dy0 = max(0, x), max(0, y)
    w = min(src.width - sx0, dst.width - dx0)
    h = min(src.height - sy0, dst.height - dy0)
    if w <= 0 or h <= 0:
        return
    s = src if (sx0, sy0, w, h) == (0, 0, src.width, src.height) else src.crop((sx0, sy0, sx0 + w, sy0 + h))
    dst.alpha_composite(s, (dx0, dy0))


def blit(dst, spr, pos, rot=0.0, sx=1.0, sy=None, alpha=1.0):
    """Draw sprite with its pivot at pos, rotated `rot` degrees clockwise, scaled sx/sy."""
    if sy is None:
        sy = abs(sx) if sx >= 0 else abs(sx)
    if abs(sx) < 0.01 or abs(sy) < 0.01 or alpha <= 0.003:
        return
    im, (px, py) = spr.variant(sx, sy)
    if alpha < 1:
        im = im.copy(); a = im.split()[3].point(lambda v: int(v * alpha)); im.putalpha(a)
    if abs(rot) > 0.05:
        w, h = im.size
        cx, cy = w / 2, h / 2
        im = im.rotate(-rot, resample=Image.BICUBIC, expand=True)
        th = math.radians(rot)
        vx, vy = px - cx, py - cy
        rx, ry = vx * math.cos(th) - vy * math.sin(th), vx * math.sin(th) + vy * math.cos(th)
        px, py = im.width / 2 + rx, im.height / 2 + ry
    _ac(dst, im, pos[0] - px, pos[1] - py)


# ---------------------------------------------------------------- math helpers
def rot(v, deg):
    t = math.radians(deg)
    return (v[0] * math.cos(t) - v[1] * math.sin(t), v[0] * math.sin(t) + v[1] * math.cos(t))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, k):
    return (a[0] * k, a[1] * k)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def lerp(a, b, u):
    return a + (b - a) * u


def lerp2(a, b, u):
    return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(u):
    u = clamp(u); return u * u * (3 - 2 * u)


def ease_out(u):
    u = clamp(u); return 1 - (1 - u) ** 3


def back_out(u, s=1.8):
    u = clamp(u) - 1; return 1 + (s + 1) * u ** 3 + s * u ** 2


def seg_angle(a, b):
    """clockwise-from-down angle of the segment a->b (sprites are authored pointing down)."""
    return math.degrees(math.atan2(-(b[0] - a[0]), (b[1] - a[1])))


def down_vec(deg, length):
    t = math.radians(deg)
    return (-math.sin(t) * length, math.cos(t) * length)
