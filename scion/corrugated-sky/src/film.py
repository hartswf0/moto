"""CORRUGATED SKY - Reiniger shadow theatre on the 140.84 BPM grid (beat = 0.42601 s, offset 0.300 s).

Scenes (beats): b0 title | b16 the house wakes, serves an empty table | b64 noon: the west wall and its lit
family | b112 night: the family steps out of the wall, plays; the ball goes over the gate, the dog follows |
b176 PROOF: the girl climbs the gate, hesitates, offers her hand, lets go | b208 the routines fail: fire |
b264 the family returns to the wall | b280 the house falls | b296 rain on the corrugated sky | b328 last voice.
"""
import json, math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
from engine import ease, ease_out, back_out, clamp, lerp, lerp2, font, FONT_SERIF, FONT_STENCIL
import rigs
from rigs import human, dog, stand, walk, dog_stand, dog_walk, ik2, ik_pick, legs_to_floor, circle, CONTACT_LOG, LIMIT_LOG

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = json.load(open(os.path.join(os.path.dirname(__file__), "beatgrid.json")))["grid"]
PER, OFF = G["period"], G["offset"]
FPS = 24
DUR = 145.73
W, H = 1280, 720
SS = 2  # supersample
INKC = (14, 10, 10)
PAINT = (255, 244, 214)
RED = (242, 56, 44)


def T(b): return OFF + b * PER
def B(t): return (t - OFF) / PER


# ---------------------------------------------------------------- cast (one rig per character)
GIRL = human("girl", "girl", 1.6)
BOY = human("boy", "boy", 1.55)
MOM = human("mother", "mother", 1.25)
DAD = human("father", "father", 1.25)
DOG = dog("dog", 1.7)
ARM = None  # house arm built below

FLOOR = 640          # garden contact plane
HFLOOR = 560         # house floor (cross-section)


# ---------------------------------------------------------------- palette (backlight schedule)
PAL = [(0, (250, 186, 118), (255, 234, 186)), (60, (250, 196, 128), (255, 238, 196)), (68, (255, 222, 156), (255, 248, 220)),
       (108, (255, 214, 150), (255, 240, 205)), (116, (34, 40, 86), (150, 104, 134)), (204, (30, 36, 80), (140, 96, 128)),
       (210, (90, 26, 20), (230, 110, 40)), (290, (120, 24, 12), (255, 150, 50)), (298, (104, 112, 122), (186, 192, 194)),
       (400, (96, 104, 114), (178, 184, 188))]


def palette(b):
    for (b0, t0, l0), (b1, t1, l1) in zip(PAL, PAL[1:]):
        if b0 <= b <= b1:
            u = ease((b - b0) / (b1 - b0))
            return tuple(int(lerp(a, c, u)) for a, c in zip(t0, t1)), tuple(int(lerp(a, c, u)) for a, c in zip(l0, l1))
    return PAL[-1][1], PAL[-1][2]


_GRAD = {}


def backdrop(b, sun=None, corrugate=0.0, glow=None):
    top, low = palette(b)
    key = (top, low, round(corrugate, 2))
    g = _GRAD.get(key)
    if g is None:
        import numpy as np
        y = np.linspace(0, 1, H)[:, None, None]
        t = np.array(top, float)[None, None, :]; l = np.array(low, float)[None, None, :]
        img = t + (l - t) * (y ** 0.8)
        if corrugate:
            band = (np.sin(np.linspace(0, 1, H) * math.pi * 46) * 0.5 + 0.5)[:, None, None]
            img = img * (1 - 0.09 * corrugate * band)
        img = np.repeat(img, W, axis=1)
        xx = np.linspace(-1, 1, W)[None, :, None]; yy = np.linspace(-1, 1, H)[:, None, None]
        img = img * (1 - 0.22 * (xx ** 2 + yy ** 2 * 0.6))
        g = Image.fromarray(np.clip(img, 0, 255).astype("uint8"))
        if len(_GRAD) > 40: _GRAD.clear()
        _GRAD[key] = g
    g = g.copy()
    if sun:
        (sx, sy), r, col = sun
        s = Image.new("L", (W, H), 0)
        ImageDraw.Draw(s).ellipse([sx - r * 3, sy - r * 3, sx + r * 3, sy + r * 3], fill=90)
        ImageDraw.Draw(s).ellipse([sx - r, sy - r, sx + r, sy + r], fill=255)
        s = s.filter(ImageFilter.GaussianBlur(r * 0.6))
        g = Image.composite(Image.new("RGB", (W, H), col), g, s)
    if glow:
        (gx, gy), r, col, a = glow
        s = Image.new("L", (W, H), 0)
        ImageDraw.Draw(s).ellipse([gx - r, gy - r, gx + r, gy + r], fill=int(255 * a))
        s = s.filter(ImageFilter.GaussianBlur(r * 0.4))
        g = Image.composite(Image.new("RGB", (W, H), col), g, s)
    return g


# ---------------------------------------------------------------- stage: layered masks at 2x
class Stage:
    def __init__(self, b):
        self.b = b
        self.m = {k: Image.new("L", (W * SS, H * SS), 0) for k in ("far", "mid", "paint", "fore")}
        self.d = {k: ImageDraw.Draw(v) for k, v in self.m.items()}

    def poly(self, layer, pts, val=255):
        if len(pts) >= 3:
            self.d[layer].polygon([(x * SS, y * SS) for x, y in pts], fill=val)

    def polys(self, layer, ps, val=255):
        for p in ps: self.poly(layer, p, val)

    def rect(self, layer, x0, y0, x1, y1, val=255):
        self.d[layer].rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=val)

    def ellipse(self, layer, cx, cy, rx, ry, val=255):
        self.d[layer].ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS], fill=val)

    def line(self, layer, pts, w, val=255):
        self.d[layer].line([(x * SS, y * SS) for x, y in pts], fill=val, width=max(1, int(w * SS)))

    def text(self, layer, s, center, size, val=0, fontpath=FONT_SERIF, spacing=0):
        f = font(fontpath, size * SS)
        d = self.d[layer]
        if spacing:
            ws = [d.textlength(c, font=f) for c in s]
            tot = sum(ws) + spacing * SS * (len(s) - 1)
            x = center[0] * SS - tot / 2
            for c, w in zip(s, ws):
                d.text((x, center[1] * SS), c, font=f, fill=val, anchor="lm"); x += w + spacing * SS
        else:
            d.text((center[0] * SS, center[1] * SS), s, font=f, fill=val, anchor="mm")

    def compose(self, bg, far_tint=0.5):
        out = bg.copy()
        top, low = palette(self.b)
        def down(m): return m.resize((W, H), Image.LANCZOS)
        far = down(self.m["far"]).filter(ImageFilter.GaussianBlur(1.4))
        fc = tuple(int(c * (1 - far_tint)) for c in low)
        out = Image.composite(Image.new("RGB", (W, H), fc), out, far)
        mid = down(self.m["mid"])
        out = Image.composite(Image.new("RGB", (W, H), INKC), out, mid)
        paint = down(self.m["paint"])
        pc = tuple(int(lerp(a, 255, 0.55)) for a in low)
        out = Image.composite(Image.new("RGB", (W, H), pc), out, paint)
        fore = down(self.m["fore"]).filter(ImageFilter.GaussianBlur(1.6))
        out = Image.composite(Image.new("RGB", (W, H), (4, 2, 2)), out, fore)
        return out


def draw_rig(st, rig, root, pose, layer="mid", face=1, lean=0.0, profile=None, val=255, tag=""):
    Wd = rig.fk(root, pose, lean=lean, face=face, tag=tag)
    st.polys(layer, rig.polys(Wd, profile, face=face), val)
    return Wd


# ---------------------------------------------------------------- set pieces
def corrugated_edge(x0, x1, y, amp, n):
    return [(x0 + (x1 - x0) * i / (n * 2), y - amp * (i % 2)) for i in range(n * 2 + 1)]


def house_cross_section(st, b, x0=300, x1=980, collapse=0.0, rooms_lit=True):
    """Black cardboard house with a cutaway front: two rooms + attic, corrugated roof edge."""
    roof_y, floor_y, attic_y = 250, HFLOOR, 360
    k = collapse
    # outer shell
    shell = [(x0 - 20, floor_y + 12), (x0 - 20, attic_y)] + [(lerp(x0 - 40, (x0 + x1) / 2, u), lerp(attic_y + 6, roof_y - 70, u)) for u in (0, 1)] \
        + [(x1 + 40, attic_y + 6), (x1 + 20, attic_y), (x1 + 20, floor_y + 12)]
    st.poly("mid", shell)
    # cut rooms (negative space) - kitchen, living room, attic window
    st.poly("mid", [(x0 + 10, attic_y + 22), (x0 + 330, attic_y + 22), (x0 + 330, floor_y - 2), (x0 + 10, floor_y - 2)], 0)
    st.poly("mid", [(x0 + 350, attic_y + 22), (x1 - 10, attic_y + 22), (x1 - 10, floor_y - 2), (x0 + 350, floor_y - 2)], 0)
    cx = (x0 + x1) / 2
    st.ellipse("mid", cx, attic_y - 46, 34, 26, 0)
    st.line("mid", [(cx - 34, attic_y - 46), (cx + 34, attic_y - 46)], 3)
    st.line("mid", [(cx, attic_y - 72), (cx, attic_y - 20)], 3)
    # corrugated roof ridge
    for i in range(2):
        side = [(x0 - 40, attic_y + 6), ((x0 + x1) / 2, roof_y - 70)] if i == 0 else [((x0 + x1) / 2, roof_y - 70), (x1 + 40, attic_y + 6)]
        n = 9
        pts = []
        for j in range(n * 2 + 1):
            u = j / (n * 2)
            p = lerp2(side[0], side[1], u)
            pts.append((p[0], p[1] - 9 * (j % 2)))
        st.poly("mid", pts + [side[1], side[0]])
    # kitchen furniture: table, four chairs, stove, clock, window
    return dict(kitchen=(x0 + 10, attic_y + 22, x0 + 330, floor_y - 2), living=(x0 + 350, attic_y + 22, x1 - 10, floor_y - 2),
                ceiling=attic_y + 22, floor=floor_y)


def table_and_chairs(st, room, chairs_out=(0, 0, 0, 0), plates=0, toast=-1.0, steam=0.0, b=0.0):
    x0, y0, x1, y1 = room
    tx = (x0 + x1) / 2 + 10
    ty = y1 - 66
    st.rect("mid", tx - 110, ty, tx + 110, ty + 8)
    st.rect("mid", tx - 100, ty + 8, tx - 92, y1)
    st.rect("mid", tx + 92, ty + 8, tx + 100, y1)
    for i in range(4):
        side = -1 if i < 2 else 1
        bx = tx + side * (124 + 26 * (i % 2)) + side * 40 * chairs_out[i]
        st.rect("mid", bx - 14, y1 - 40, bx + 14, y1 - 34)
        st.rect("mid", bx - 14, y1 - 34, bx - 10, y1)
        st.rect("mid", bx + 10, y1 - 34, bx + 14, y1)
        st.rect("mid", bx + side * 12 - 2, y1 - 90, bx + side * 12 + 3, y1 - 34)
        st.ellipse("mid", bx + side * 12, y1 - 90, 6, 6)
    for i in range(plates):
        px = tx - 78 + i * 52
        st.ellipse("mid", px, ty - 3, 20, 4)
        st.rect("mid", px + 12, ty - 16, px + 20, ty - 3)  # cup
        if steam > 0:
            for k in range(3):
                yy = ty - 22 - k * 12 - (b * 10 % 12)
                st.ellipse("mid", px + 16 + 4 * math.sin(b * 2 + k + i), yy, 2.2, 3.4)
    # stove + toaster
    sx = x0 + 40
    st.rect("mid", sx - 26, y1 - 70, sx + 26, y1)
    st.rect("mid", sx - 18, y1 - 92, sx + 18, y1 - 70)
    if toast >= 0:
        h = 60 * math.sin(math.pi * clamp(toast))
        for dx in (-7, 7):
            st.rect("mid", sx + dx - 5, y1 - 104 - h, sx + dx + 5, y1 - 90 - h)
    return tx, ty


def house_arm(st, root, target, grip=False, val=255):
    """The house's own hand: a two-bone articulated arm hanging from the ceiling (pinned at root)."""
    l1, l2 = 70, 64
    d1, d2, reach = ik2(root, 0, 0, l1, l2, target, 1)
    a1 = d1; a2 = a1 + d2
    e = (root[0] + l1 * math.cos(math.radians(a1)), root[1] + l1 * math.sin(math.radians(a1)))
    h = (e[0] + l2 * math.cos(math.radians(a2)), e[1] + l2 * math.sin(math.radians(a2)))
    st.line("mid", [root, e], 9, val); st.line("mid", [e, h], 7, val)
    st.ellipse("mid", root[0], root[1], 9, 9, val); st.ellipse("mid", e[0], e[1], 7, 7, val)
    for s in (-1, 1):
        ang = a2 + s * (18 if grip else 40)
        st.line("mid", [h, (h[0] + 16 * math.cos(math.radians(ang)), h[1] + 16 * math.sin(math.radians(ang)))], 4, val)
    return h


def clock(st, cx, cy, b):
    st.ellipse("mid", cx, cy, 30, 30)
    st.ellipse("mid", cx, cy, 24, 24, 0)
    for k in range(12):
        a = k * 30
        st.line("mid", [(cx + 19 * math.cos(math.radians(a)), cy + 19 * math.sin(math.radians(a))),
                        (cx + 23 * math.cos(math.radians(a)), cy + 23 * math.sin(math.radians(a)))], 2)
    a = -90 + (int(b) % 60) * 6
    st.line("mid", [(cx, cy), (cx + 18 * math.cos(math.radians(a)), cy + 18 * math.sin(math.radians(a)))], 3)
    st.line("mid", [(cx, cy), (cx + 12 * math.cos(math.radians(-90 + b * 0.5)), cy + 12 * math.sin(math.radians(-90 + b * 0.5)))], 4)
    sw = 22 * math.sin(b * math.pi)  # pendulum swings once per beat pair
    st.line("mid", [(cx, cy + 30), (cx + sw, cy + 80)], 3)
    st.ellipse("mid", cx + sw, cy + 84, 8, 8)


def banner(st, text, b, b0, b1, x=640, y=86, size=30):
    """The house's voice: a black cut-paper banner lowered on strings; the words are cut OUT (light shows through)."""
    if b < b0 or b > b1 + 0.6:
        return
    u = ease_out((b - b0) / 0.35) if b < b1 else 1 - ease((b - b1) / 0.6)
    yy = lerp(-60, y, u)
    f = font(FONT_SERIF, size)
    tw = ImageDraw.Draw(Image.new("L", (1, 1))).textlength(text, font=f)
    w = tw / 2 + 34
    pts = [(x - w, yy - 24)] + [(x - w + i * 2 * w / 16, yy + 26 + (5 if i % 2 else 0)) for i in range(17)] + [(x + w, yy - 24)]
    pts = [(x - w, yy - 26), (x + w, yy - 26)] + [(x + w - i * 2 * w / 20, yy + 26 + (6 if i % 2 else 0)) for i in range(21)]
    st.poly("mid", pts)
    st.line("mid", [(x - w + 20, yy - 26), (x - w + 20, -10)], 2)
    st.line("mid", [(x + w - 20, yy - 26), (x + w - 20, -10)], 2)
    st.text("mid", text, (x, yy + 2), size, 0)


def lawn(st, b, x0=0, x1=W, y=FLOOR, wind=0.0):
    st.rect("mid", x0, y, x1, H)
    rnd = random.Random(7)
    for i in range(int((x1 - x0) / 9)):
        x = x0 + i * 9 + rnd.uniform(-3, 3); h = rnd.uniform(8, 20)
        lean = 4 * math.sin(b * 0.7 + i * 0.3) * wind
        st.poly("mid", [(x - 3, y + 1), (x + lean, y - h), (x + 3, y + 1)])


def fore_leaves(st, b, side=0, sway=1.0):
    """Reiniger foreground: black fern fronds leaning in from the frame edge (fore layer)."""
    rnd = random.Random(11 + side)
    sgn = 1 if side == 0 else -1
    for k in range(3):
        base = (0 if side == 0 else W, H + 10 - k * 40)
        ang = math.radians(-70 + k * 14 + 3 * math.sin(b * 0.5 + k) * sway)
        L = 240 - k * 40
        pts = [base]
        for s_ in range(14):
            u = (s_ + 1) / 14
            c = (base[0] + sgn * L * u * math.cos(ang) * 0.55 + sgn * 30 * u * u, base[1] + L * u * math.sin(ang))
            pts.append(c)
        st.line("fore", pts, 4)
        for s_ in range(2, 13):
            c = pts[s_]; u = s_ / 14
            for side2 in (-1, 1):
                ln = 30 * (1 - u) + 6
                st.poly("fore", [(c[0] - 2, c[1]), (c[0] + sgn * side2 * ln * 0.3 + sgn * ln * 0.6, c[1] - ln * 0.5 + side2 * ln * 0.4), (c[0] + 2, c[1] + 3)])


def gate(st, x=640, top=530, ground=FLOOR, open_amt=0.0):
    """Garden gate: left post (climbing post with pegs), right post, two thin bars, a light gap everywhere else."""
    st.rect("mid", x - 6, top - 26, x + 6, ground)
    st.ellipse("mid", x, top - 34, 10, 10)
    pegs = [ground - 36, ground - 72, top + 6]
    for py in pegs[:-1]:
        st.rect("mid", x - 20, py - 3, x, py + 3)
    rx = x + 90
    st.rect("mid", rx - 5, top - 10, rx + 5, ground)
    st.ellipse("mid", rx, top - 18, 8, 8)
    w = 84 * math.cos(math.radians(80 * open_amt))
    for yy in (top + 4, ground - 50):
        st.rect("mid", x + 6, yy - 3, x + 6 + w, yy + 3)
    for k in range(1, 4):
        xx = x + 6 + w * k / 4
        st.rect("mid", xx - 1.5, top + 4, xx + 1.5, ground - 50)
    # fence to both sides
    for fx in list(range(370, int(x) - 30, 34)) + list(range(int(rx) + 40, W + 30, 34)):
        st.rect("mid", fx - 3, ground - 70, fx + 3, ground)
        st.poly("mid", [(fx - 3, ground - 70), (fx, ground - 80), (fx + 3, ground - 70)])
    st.rect("mid", 370, ground - 56, x - 6, ground - 52)
    st.rect("mid", rx + 5, ground - 56, W, ground - 52)
    return pegs


# ---------------------------------------------------------------- the family on the west wall
WALL_X0, WALL_X1, WALL_TOP = 20, 560, 250


def family_wall_poses():
    """Where the family stood when the light took them: (rig, root, pose, face)."""
    return [
        (DAD, (100, FLOOR - 4), dict(stand(), torso=14, upper_n=-60, fore_n=-20, upper_f=-50, fore_f=-30, thigh_n=-20, shin_n=30), 1, "dad"),
        (MOM, (230, FLOOR - 4), dict(stand(), torso=34, head=26, upper_n=-20, fore_n=-10, upper_f=-30, fore_f=-20, thigh_n=-10, thigh_f=12), 1, "mom"),
        (BOY, (365, FLOOR - 4), dict(stand(), upper_n=-175, fore_n=-10, upper_f=40, fore_f=-30, thigh_n=-15, shin_n=10), 1, "boy"),
        (GIRL, (480, FLOOR - 4), dict(stand(), upper_n=-160, fore_n=-20, upper_f=-150, fore_f=-30, head=-20), -1, "girl"),
    ]


def wall_root(rig, root, pose, face):
    return legs_to_floor(rig, root, pose, FLOOR, face)


def west_wall(st, b, holes_lit=(1, 1, 1, 1), ball=True, x_shift=0):
    st.poly("mid", [(WALL_X0 + x_shift, FLOOR), (WALL_X0 + x_shift, WALL_TOP + 40), (WALL_X0 + 60 + x_shift, WALL_TOP),
                    (WALL_X1 + x_shift, WALL_TOP), (WALL_X1 + 20 + x_shift, FLOOR)])
    for i, (rig, root, pose, face, who) in enumerate(family_wall_poses()):
        r = wall_root(rig, (root[0] + x_shift, root[1]), pose, face)
        Wd = rig.fk(r, pose, face=face, tag="-wall")
        ps = rig.polys(Wd, face=face)
        st.polys("mid", ps, 0)
        if holes_lit[i]:
            st.polys("paint", ps, int(255 * holes_lit[i]))
    if ball:
        st.ellipse("mid", 425 + x_shift, 330, 13, 13, 0)
        st.ellipse("paint", 425 + x_shift, 330, 13, 13, 255)


# ---------------------------------------------------------------- scenes
def sc_title(img, b):
    """Touki Bouki card: red, letter-spaced, over a motion-blurred plate of the house street."""
    st = Stage(b)
    pan = b * 60
    for k in range(-1, 4):
        x0 = k * 520 - pan % 520
        st.poly("mid", [(x0, FLOOR), (x0, 380), (x0 + 120, 300), (x0 + 240, 380), (x0 + 240, FLOOR)])
        st.rect("mid", x0 + 60, 430, x0 + 110, 500, 0)
        st.rect("mid", x0 + 300, 520, x0 + 312, FLOOR)
        st.ellipse("mid", x0 + 306, 500, 40, 34)
    st.rect("mid", 0, FLOOR, W, H)
    bg = backdrop(b, sun=((900, 300), 40, (255, 250, 230)))
    im = st.compose(bg)
    # horizontal motion blur
    sm = im.resize((W // 24, H), Image.BILINEAR).resize((W, H), Image.BILINEAR)
    im = Image.blend(im, sm, 0.85)
    d = ImageDraw.Draw(im)
    f = font("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", 150)
    for row, word in enumerate(("CORRUGATED", "SKY")):
        if b < 2 + row * 2: continue
        s = 1.0
        widths = [d.textlength(c, font=f) for c in word]
        track = 34 if row == 0 else 120
        tot = sum(widths) + track * (len(word) - 1)
        sc = min(1.0, 1180 / tot)
        f2 = font("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", int(150 * sc))
        widths = [d.textlength(c, font=f2) for c in word]; tot = sum(widths) + track * sc * (len(word) - 1)
        x = W / 2 - tot / 2; y = 250 + row * 180
        for c, w in zip(word, widths):
            d.text((x, y), c, font=f2, fill=RED, anchor="lm"); x += w + track * sc
    if b >= 8:
        fs = font("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", 22)
        d.text((W / 2, 640), "ET  TU,  BRUTE?   ·   BOXBACK   ·   11", font=fs, fill=RED, anchor="mm")
    fade = clamp((b - 14) / 2)
    if fade > 0:
        im = Image.blend(im, render_house_morning(b, still=True), fade)
    return im


def render_house_morning(b, still=False):
    st = Stage(b)
    rooms = house_cross_section(st, b)
    kit, liv = rooms["kitchen"], rooms["living"]
    plates = 0 if b < 24 else min(4, int(b - 24) + 1)
    if b >= 52: plates = max(0, 4 - int((b - 52) / 2))
    chairs = tuple(clamp((b - (32 + i)) / 0.5) * (1 - clamp((b - 56) / 2)) for i in range(4))
    toast = (b - 30) / 1.0 if 30 <= b < 31 else -1
    tx, ty = table_and_chairs(st, kit, chairs, plates, toast, steam=1.0 if 36 <= b < 52 else 0, b=b)
    # house arm sets the plates, one per beat
    root = ((kit[0] + kit[2]) / 2 - 40, rooms["ceiling"])
    if 23.5 <= b < 28:
        k = b - 24
        i = min(3, max(0, int(k)))
        px = tx - 78 + i * 52
        u = k - int(k)
        tgt = lerp2((root[0] - 60, root[1] + 100), (px, ty - 12), math.sin(math.pi * clamp(u)) if k >= 0 else 0)
        house_arm(st, root, tgt, grip=True)
    elif 52 <= b < 60:
        u = (b - 52) % 2 / 2
        px = tx + 78 - int((b - 52) / 2) * 52
        house_arm(st, root, lerp2((px, ty - 12), (root[0] - 120, root[1] + 60), u), grip=True)
    else:
        house_arm(st, root, (root[0] - 50, root[1] + 110))
    clock(st, liv[2] - 70, liv[1] + 70, b)
    # front door in the living room right wall
    dx = liv[2] - 10
    open_amt = clamp((b - 46) / 0.5) * (1 - clamp((b - 50) / 0.5))
    st.rect("mid", dx - 70 + 0, liv[3] - 150, dx - 70 + 60 * (1 - open_amt) + 4, liv[3])
    # robot mice
    if 52 <= b < 62:
        for k in range(3):
            mx = lerp(liv[0] + 20, kit[0] + 20, clamp((b - 52 - k * 0.7) / 7))
            st.rect("mid", mx - 12, rooms["floor"] - 16, mx + 12, rooms["floor"] - 2)
            st.line("mid", [(mx + 12, rooms["floor"] - 14), (mx + 22, rooms["floor"] - 26 - 3 * math.sin(b * 8 + k))], 2)
            st.ellipse("mid", mx - 6, rooms["floor"], 4, 4, 0)
    lawn(st, b, y=HFLOOR + 12)
    fore_leaves(st, b, 0); fore_leaves(st, b, 1)
    if not still:
        banner(st, "7:00 · GOOD MORNING, HOUSE OF FOUR", b, 20, 27.5)
        banner(st, "7:09 · BREAKFAST FOR FOUR", b, 28, 35.5)
        banner(st, "7:30 · YOUR TEA IS GOING COLD", b, 38, 43.5)
        banner(st, "8:01 · THE CAR IS WAITING", b, 44, 51.5)
        banner(st, "8:30 · CLEAR THE TABLE", b, 52, 59.5)
    sunx = lerp(200, 1100, clamp((b - 10) / 100))
    bg = backdrop(b, sun=((sunx, lerp(520, 150, clamp((b - 10) / 50))), 48, (255, 250, 236)))
    return st.compose(bg)


def sc_wall(b):
    """Noon: the west wall; the family is where the light left them. The dog comes home."""
    st = Stage(b)
    west_wall(st, b, x_shift=200)
    lawn(st, b)
    # far hills + other houses (far layer)
    st.poly("far", [(0, FLOOR), (0, 520), (260, 470), (520, 500), (800, 450), (1100, 490), (W, 470), (W, FLOOR)])
    for hx in (720, 1000):
        st.poly("far", [(hx, FLOOR), (hx, 470), (hx + 60, 430), (hx + 120, 470), (hx + 120, FLOOR)])
    # sprinkler arcs on beats
    for k in range(9):
        u = ((b * 0.5 + k / 9) % 1)
        x = 940 + 240 * u; y = FLOOR - 160 * 4 * u * (1 - u)
        st.ellipse("mid", x, y, 3, 4)
    st.rect("mid", 936, FLOOR - 16, 944, FLOOR)
    # dog arrives, limping; sits beneath the girl's place, looks up
    if b >= 72:
        if b < 88:
            x = lerp(1340, 900, clamp((b - 72) / 16))
            p = dog_walk((b - 72) * math.pi, wag=-30)
            p["spine"] += 4 * math.sin(b * math.pi)
            r = legs_to_floor(DOG, (x, FLOOR - 70), p, FLOOR, -1)
            draw_rig(st, DOG, r, p, face=-1)
        else:
            p = dog_stand(wag=-40 + 20 * math.sin(b * 0.8))
            p.update(dict(hthigh_n=-70, hshin_n=110, hthigh_f=-64, hshin_f=110, spine=-28, neck=-20, head=-25 if b >= 92 else 0))
            r = legs_to_floor(DOG, (900, FLOOR - 70), p, FLOOR, -1)
            draw_rig(st, DOG, r, p, face=-1)
    banner(st, "12:00 · LUNCH IN THE GARDEN", b, 96, 103.5, x=860)
    banner(st, "SOMEONE IS AT THE DOOR", b, 80, 86, x=860)
    fore_leaves(st, b, 1)
    bg = backdrop(b, sun=((1000, 140), 52, (255, 252, 240)))
    return st.compose(bg)


def family_actor_pose(i, b):
    """Night: the four step out of the wall one by one and play. Returns (rig, root, pose, face) or None."""
    rig, root0, pose0, face0, who = family_wall_poses()[i]
    b_out = 120 + 4 * i
    if b < b_out:
        return None
    u = clamp((b - b_out) / 2)
    x0 = root0[0] + 200 * 0  # wall at x_shift 0 in the garden set
    homes = [610, 700, 790, 870]
    if b < b_out + 2:
        # step out of the hole: pose eases from the wall pose to standing, sliding right
        pose = {k: lerp(pose0.get(k, 0), stand().get(k, 0), ease(u)) for k in set(pose0) | set(stand())}
        x = lerp(root0[0], root0[0] + 40, ease(u)); face = face0 if u < 0.5 else 1
        return rig, (x, None), pose, face
    x_start = root0[0] + 40
    tgt = homes[i]
    k = clamp((b - b_out - 2) / 4)
    if k < 1:
        return rig, (lerp(x_start, tgt, k), None), walk((b - b_out) * math.pi), 1 if tgt > x_start else -1
    return rig, (tgt, None), stand(), 1


def sc_night(b):
    """The family steps out of the wall; the ball goes over the gate; the dog goes after it; the gate shuts."""
    st = Stage(b)
    st.poly("far", [(0, FLOOR), (0, 540), (300, 500), (600, 520), (900, 470), (W, 500), (W, FLOOR)])
    st.ellipse("paint", 1080, 120, 34, 34)  # moon
    holes = (1, 1, 1, 1)
    west_wall(st, b, holes_lit=holes, ball=b < 140)
    gate_open = clamp((b - 150) / 0.6) * (1 - clamp((b - 155) / 0.4))
    gate(st, x=GATE_NIGHT, open_amt=gate_open)
    lawn(st, b)
    # family
    for i in range(4):
        a = family_actor_pose(i, b)
        if a is None: continue
        rig, (x, _), pose, face = a
        if i == 3 and b >= 158:  # the girl goes to the gate
            k = clamp((b - 158) / 14)
            if k < 1:
                x = lerp(870, 1010, k); pose = walk(b * math.pi); face = 1
            else:
                x = 1010; pose = stand(); face = 1
        if i == 1 and b >= 160:  # mother goes back toward the house
            k = clamp((b - 160) / 10)
            x = lerp(700, 610, k); pose = walk(b * math.pi) if k < 1 else stand(); face = -1 if k < 1 else 1
        if i == 0 and 140 <= b < 146:  # father lifts... reaches up to the boy's throw
            pose = dict(stand(), upper_n=-150, upper_f=-140)
        if i == 2 and 142 <= b < 146:
            pose = dict(stand(), upper_n=-170, fore_n=-10)
        r = legs_to_floor(rig, (x, FLOOR - 100), pose, FLOOR, face)
        draw_rig(st, rig, r, pose, face=face, tag="-night")
    # the ball: thrown by the boy at b142, bounces, rolls under the gate at b150, dog follows
    if 140 <= b < 156:
        if b < 146:
            u = (b - 142) / 4
            p = (lerp(790, 900, clamp(u)), FLOOR - 120 - 220 * 4 * clamp(u) * (1 - clamp(u))) if b >= 142 else (800, FLOOR - 190)
        elif b < 150:
            u = (b - 146) / 4
            p = (lerp(900, 1070, u), FLOOR - 12 - 50 * abs(math.sin(u * math.pi * 2)))
        else:
            u = (b - 150) / 6
            p = (lerp(1070, 1300, u), FLOOR - 12)
        st.ellipse("mid", p[0], p[1], 12, 12)
    # dog plays, then goes through the gate after the ball
    if b >= 124:
        if b < 146:
            x = 975 + 45 * math.sin((b - 124) * 0.5)
            face = 1 if math.cos((b - 124) * 0.5) > 0 else -1
            p = dog_walk(b * math.pi * 1.5, wag=30 * math.sin(b * 6))
        elif b < 156:
            k = (b - 146) / 10; x = lerp(980, 1250, k); face = 1; p = dog_walk(b * math.pi * 2, wag=20)
        else:
            k = clamp((b - 156) / 6); x = lerp(1250, 1210, k); face = -1
            p = dog_walk(b * math.pi * 1.5) if k < 1 else dog_stand(wag=20 * math.sin(b * 3))
        r = legs_to_floor(DOG, (x, FLOOR - 70), p, FLOOR, face)
        draw_rig(st, DOG, r, p, face=face, tag="-night")
    banner(st, "9:00 · BATH TIME, BEDTIME, STORY TIME", b, 114, 121.5, x=700)
    if 154 <= b < 160:
        pass
    fore_leaves(st, b, 0, 0.6)
    bg = backdrop(b, glow=((1080, 120), 160, (220, 210, 240), 0.35))
    return st.compose(bg, far_tint=0.35)


# ---------------------------------------------------------------- PROOF: the gate
PROOF_M = (668.0, 455.0)
GATE_NIGHT = 1060  # where hand and paw meet, above the gate top (light gap)


def girl_climb(b):
    """Keyed climb: pelvis path + pinned contacts. Contacts change one limb per beat; others stay pinned.
    Returns (root, pose, profile, contacts{name: target})."""
    g = GIRL
    x = 640
    PEG = [FLOOR - 36, FLOOR - 72, FLOOR - 108]
    POST = lambda y: (x - 7, y)
    FX = 622
    # keyframes: beat -> (pelvis, hand_n, hand_f, foot_n, foot_f)
    K = [
        (176, (560, None), None, None, None, None),
        (178, (596, 562), POST(530), POST(552), (600, FLOOR), (588, FLOOR)),
        (179, (596, 548), POST(518), POST(552), (FX, PEG[0]), (588, FLOOR)),
        (180, (597, 538), POST(518), POST(530), (FX, PEG[0]), (FX, PEG[0])),
        (181, (598, 528), POST(504), POST(530), (FX, PEG[1]), (FX, PEG[0])),
        (182, (599, 518), POST(504), POST(512), (FX, PEG[1]), (FX, PEG[1])),
        (183, (600, 510), POST(500), POST(512), (FX, PEG[2]), (FX, PEG[1])),
        (184, (600, 498), POST(500), POST(506), (FX, PEG[2]), (FX, PEG[1])),
    ]
    return K


def proof_state(b):
    """Full proof state at beat b. Returns dict for the girl (root, pose, profile, contacts) and the dog."""
    S = {}
    x = 640
    hold_post = (x - 7, 506)  # far hand on the post
    # ---- girl
    if b < 178:
        k = clamp((b - 176) / 2)
        root = (lerp(520, 592, k), None); pose = walk(b * math.pi) if k < 1 else stand()
        S["girl"] = dict(root=root, pose=pose, profile={"hand_n": "open", "hand_f": "open"}, contacts={}, head=0)
    elif b < 184:
        K = girl_climb(b)[1:]
        i = min(len(K) - 1, int(b - 178))
        j = min(len(K) - 1, i + 1)
        u = ease(clamp((b - (178 + i)) / 0.5))
        A, Bk = K[i], K[j]
        pel = lerp2(A[1], Bk[1], u)
        tg = {}
        names = ("hand_n", "hand_f", "foot_n", "foot_f")
        for n, ta, tb in zip(names, A[2:], Bk[2:]):
            moving = ta != tb
            if not moving:
                tg[n] = (ta, True)
            else:
                # lift-and-place: arc between the two holds; pinned again once placed
                mid = lerp2(ta, tb, u)
                tg[n] = ((mid[0] + (-10 if n.startswith("hand") else 8) * math.sin(math.pi * u), mid[1] - (12 if n.startswith("hand") else 3) * math.sin(math.pi * u)), u >= 1)
        S["girl"] = dict(root=pel, targets=tg, profile={"hand_n": "grip", "hand_f": "grip"}, head=-10)
    else:
        pel = (600, 498)
        tg = {"hand_f": (hold_post, True), "foot_n": ((622, FLOOR - 108), True), "foot_f": ((622, FLOOR - 72), True)}
        head = 0
        prof = {"hand_f": "grip", "hand_n": "grip"}
        if b < 188:
            # hesitate: near hand still grips the post; head turns to the dog, back to the mother, to the dog
            tg["hand_n"] = ((x - 7, 500), True)
            head = held(b, [(184, 0), (185, -26), (186, 22), (187, -26)])
        elif b < 190:
            u = ease(clamp((b - 188) / 1.5))
            tg["hand_n"] = (lerp2((x - 7, 500), PROOF_M, u), False)
            prof["hand_n"] = "offer"; head = -20
        elif b < 198:
            tg["hand_n"] = (PROOF_M, True)
            prof["hand_n"] = "offer" if b < 190.5 else "grip"; head = -20
            if 196 <= b: head = held(b, [(196, 28), (197, -20)])   # the mother's call: she looks back, then at the dog
        elif b < 200:
            # she lets go: the hand opens first (replacement profile), then withdraws
            u = ease(clamp((b - 198.5) / 1.5))
            tg["hand_n"] = (lerp2(PROOF_M, (x - 7, 500), u), u == 0)
            prof["hand_n"] = "open"; head = -20 if b < 199 else 10
        else:
            # climbs down (reverse of the climb, 1 hold per beat)
            K = list(reversed(girl_climb(b)[1:]))
            i = min(len(K) - 1, int(b - 200)); j = min(len(K) - 1, i + 1)
            u = ease(clamp((b - (200 + i)) / 0.5))
            A, Bk = K[i], K[j]
            if b - 200 >= len(K) - 1:
                k = clamp((b - 206.5) / 1.5)
                S["girl"] = dict(root=(lerp(592, 500, k), None), pose=walk(b * math.pi) if k > 0 else stand(), face=-1 if k > 0 else 1,
                                 profile={"hand_n": "open", "hand_f": "open"}, contacts={}, head=0)
            else:
                pel = lerp2(A[1], Bk[1], u)
                tg = {}
                for n, ta, tb in zip(("hand_n", "hand_f", "foot_n", "foot_f"), A[2:], Bk[2:]):
                    if ta == tb: tg[n] = (ta, True)
                    else:
                        mid = lerp2(ta, tb, u); tg[n] = ((mid[0] + (-10 if n.startswith("hand") else 8) * math.sin(math.pi * u), mid[1] - (12 if n.startswith("hand") else 3) * math.sin(math.pi * u)), u >= 1)
                S["girl"] = dict(root=pel, targets=tg, profile={"hand_n": "grip", "hand_f": "grip"}, head=10)
        if "girl" not in S:
            S["girl"] = dict(root=pel, targets=tg, profile=prof, head=head)
    # ---- dog (outside the gate, facing left toward her)
    dx = 960
    if b < 188:
        p = dog_stand(wag=12 * math.sin(b * 4)); p["head"] = -20 if b >= 185 else 0
        S["dog"] = dict(root=(dx, None), pose=p, face=-1)
    elif b < 200:
        rise = ease(clamp((b - 188) / 1.6)) if b < 198.6 else 1 - ease(clamp((b - 198.6) / 1.2))
        p = dog_stand(wag=24 * math.sin(b * 6) if 190.5 <= b < 198 else 0)
        p["spine"] = -65 * rise
        p["hthigh_n"] = -18 * rise; p["hthigh_f"] = -10 * rise; p["hshin_n"] = 20 + 10 * rise; p["hshin_f"] = 20 + 10 * rise
        p["neck"] = 30 * rise; p["head"] = -10 * rise
        paw_target = PROOF_M if 190 <= b < 198.6 else None
        S["dog"] = dict(root=(lerp(dx, 792, rise), None), pose=p, face=-1, paw=paw_target, rise=rise)
    else:
        p = dog_stand(wag=-10); p["head"] = -24; p["neck"] = -10
        S["dog"] = dict(root=(dx, None), pose=p, face=-1)
    return S


def held(b, keys):
    v = keys[0][1]
    for kb, kv in keys:
        if b >= kb: v = kv
    return v


def solve_girl(G_):
    """Apply contacts with two-bone IK; record contact residuals for pinned holds."""
    g = GIRL
    pose = dict(stand())
    root = G_["root"]
    if "pose" in G_:
        face = G_.get("face", 1)
        r = legs_to_floor(g, (root[0], FLOOR - 100), G_["pose"], FLOOR, face)
        p = dict(G_["pose"]); p["head"] = G_.get("head", 0)
        return r, p, face
    p = pose; p["head"] = G_.get("head", 0)
    p["torso"] = 4
    Wd = g.fk(root, p, check=False)
    k = g.scale
    for side in ("n", "f"):
        for limb, (b1, b2, base, l1, l2, bend) in {"hand": ("upper", "fore", 180, 28 * k, 27 * k, -1),
                                                   "foot": ("thigh", "shin", 90, 36 * k, 35 * k, 1)}.items():
            name = f"{limb}_{side}"
            if name not in G_["targets"]: continue
            tgt, pinned = G_["targets"][name]
            o = Wd[f"{b1}_{side}"][0]
            pa = Wd["torso"][1] if limb == "hand" else 0.0
            lim1 = g.by[f"{b1}_{side}"].limits; lim2 = g.by[f"{b2}_{side}"].limits
            d1, d2, reach = ik_pick(o, pa, base, l1, l2, tgt, lim1, lim2)
            p[f"{b1}_{side}"] = d1; p[f"{b2}_{side}"] = d2
            if limb == "foot": p[f"foot_{side}"] = -d1 - d2 * 0.6 if False else clamp(-(d1 + d2) * 0.5, -30, 40)
    Wd = g.fk(root, p, tag="-proof")
    for side in ("n", "f"):
        for limb, end_bone in (("hand", "fore"), ("foot", "shin")):
            name = f"{limb}_{side}"
            if name in G_["targets"] and G_["targets"][name][1]:
                e = Wd[f"{end_bone}_{side}"][2]; t = G_["targets"][name][0]
                CONTACT_LOG.append(("girl", name, math.hypot(e[0] - t[0], e[1] - t[1])))
    return root, p, 1


def solve_dog(D):
    p = dict(D["pose"]); face = D["face"]
    root = legs_to_floor(DOG, (D["root"][0], FLOOR - 70), p, FLOOR, face)
    if D.get("paw"):
        # paw IK in facing-right space (mirror the target about the root)
        tgt = D["paw"]; tm = (2 * root[0] - tgt[0], tgt[1])
        Wd = DOG.fk(root, p, check=False)
        o = Wd["fleg_n"][0]; pa = Wd["spine"][1]
        d1, d2, reach = ik_pick(o, pa, 85, 28 * DOG.scale, 26 * DOG.scale, tm, DOG.by["fleg_n"].limits, DOG.by["fpaw_n"].limits)
        p["fleg_n"], p["fpaw_n"] = d1, d2
        p["fleg_f"], p["fpaw_f"] = max(-160, min(60, d1 + 14)), max(-130, min(30, d2 - 20))
        Wd = DOG.fk(root, p, face=face, tag="-proof")
        e = Wd["fpaw_n"][2]
        CONTACT_LOG.append(("dog", "paw", math.hypot(e[0] - tgt[0], e[1] - tgt[1])))
    elif D.get("rise", 0) > 0:
        p["fleg_n"], p["fpaw_n"] = -60 * D["rise"], -60 * D["rise"]
        p["fleg_f"], p["fpaw_f"] = -40 * D["rise"], -70 * D["rise"]
    return root, p, face


def sc_gate(b, proof_only=False):
    st = Stage(b)
    st.poly("far", [(0, FLOOR), (0, 540), (300, 500), (600, 520), (900, 470), (W, 500), (W, FLOOR)])
    st.ellipse("paint", 1080, 120, 34, 34)
    west_wall(st, b, ball=False, x_shift=-230, holes_lit=(0.6, 0.6, 0.6, 0.6))
    gate(st)
    lawn(st, b)
    S = proof_state(b)
    r, p, face = solve_girl(S["girl"])
    draw_rig(st, GIRL, r, p, face=face, profile=S["girl"].get("profile"), tag="-proof")
    r, p, face = solve_dog(S["dog"])
    draw_rig(st, DOG, r, p, face=face, tag="-proof")
    # the mother, by the wall, calls at b196 (arm up)
    mp = dict(stand(), upper_n=-150 if 196 <= b < 199 else 6, fore_n=-20)
    mr = legs_to_floor(MOM, (420, FLOOR - 100), mp, FLOOR, 1)
    draw_rig(st, MOM, mr, mp, face=1, tag="-proof")
    fore_leaves(st, b, 0, 0.5)
    bg = backdrop(b, glow=((1080, 120), 160, (220, 210, 240), 0.35))
    return st.compose(bg, far_tint=0.35)


# ---------------------------------------------------------------- fire
def flame(st, x, y, h, b, seed, layer="mid"):
    rnd = random.Random(seed)
    ph = int(b * 4 + seed) % 4  # four replacement profiles cycled on quarter beats
    w = h * 0.42
    pts = [(x - w, y)]
    n = 5
    for i in range(n):
        tx = x - w + (2 * w) * (i + 0.5) / n
        th = h * (0.55 + 0.45 * ((i * 7 + ph * 3 + seed) % 5) / 4)
        pts += [(tx - w / n * 0.4, y - th * 0.5), (tx + (ph - 1.5) * 3, y - th), (tx + w / n * 0.4, y - th * 0.5)]
    pts += [(x + w, y)]
    st.poly(layer, pts)


def sc_fire(b):
    st = Stage(b)
    collapse = clamp((b - 280) / 14)
    rooms = house_cross_section(st, b) if b < 292 else None
    if rooms:
        kit, liv = rooms["kitchen"], rooms["living"]
        tx, ty = table_and_chairs(st, kit, (0, 0, 0, 0), 0)
        clock(st, liv[2] - 70, liv[1] + 70, b)
        # the branch through the window at b216
        if b >= 215:
            u = clamp((b - 215) / 0.6)
            p0 = (kit[0] - 200 + 230 * u, kit[1] + 30); st.line("mid", [(-40, kit[1] - 60), p0], 16)
            st.line("mid", [p0, (p0[0] + 40, p0[1] - 30)], 6); st.line("mid", [p0, (p0[0] + 30, p0[1] + 34)], 5)
        # house arms try to spray water, then run dry
        for k, rx in enumerate((kit[0] + 120, liv[0] + 140)):
            root = (rx, rooms["ceiling"])
            if 226 <= b < 250:
                tgt = (rx - 60 + 40 * math.sin(b * 2 + k), rooms["floor"] - 90)
                h = house_arm(st, root, tgt, grip=False)
                if b < 244:
                    for j in range(7):
                        u = ((b * 2 + j / 7) % 1)
                        st.ellipse("mid", h[0] + 10 + 50 * u, h[1] + 80 * u * u + 10, 2.2, 3)
                else:
                    if int(b * 2) % 2 == 0: st.ellipse("mid", h[0] + 6, h[1] + 12, 2, 3)
            else:
                house_arm(st, root, (rx - 40, rooms["ceiling"] + 120))
        # flames: room by room on downbeats
        spots = [(kit[0] + 40, rooms["floor"] - 92), (kit[0] + 150, rooms["floor"]), (kit[0] + 280, rooms["floor"]),
                 (liv[0] + 60, rooms["floor"]), (liv[0] + 200, rooms["floor"]), ((kit[0] + liv[2]) / 2, rooms["ceiling"] - 8),
                 (liv[2] - 60, rooms["floor"]), (liv[0] + 120, rooms["ceiling"] - 8)]
        for i, (fx, fy) in enumerate(spots):
            b0 = 218 + i * 4
            if b >= b0:
                h = min(1, (b - b0) / 2) * (60 + 20 * i % 50) * (1 + 0.6 * clamp((b - 260) / 20))
                flame(st, fx, fy, h, b, i * 13)
    else:
        # ruins
        for k in range(6):
            x = 320 + k * 110
            st.poly("mid", [(x, HFLOOR + 12), (x + 20, HFLOOR - 40 - (k * 37) % 70), (x + 70, HFLOOR - 10 - (k * 23) % 40), (x + 90, HFLOOR + 12)])
    # collapse: corrugated roof sheets fall on downbeats
    if collapse > 0:
        for k in range(8):
            b0 = 280 + k * 1.5
            if b < b0: continue
            u = b - b0
            x = 340 + k * 80; y = 240 + 120 * u * u * 6
            if y < HFLOOR:
                ang = (k % 2 * 2 - 1) * 40 * u
                pts = corrugated_edge(-50, 50, 0, 8, 6) + [(50, 10), (-50, 10)]
                c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
                st.poly("mid", [(x + px * c - py * s, y + px * s + py * c) for px, py in pts])
    lawn(st, b, y=HFLOOR + 12)
    labels = [("10:00 · STORY TIME", 210, 215), ("THE WINDOW IS BROKEN", 216, 221.5), ("FIRE", 224, 226), ("FIRE · FIRE", 226, 228),
              ("FIRE · FIRE · FIRE", 228, 236), ("WATER", 236, 239.5), ("WATER · WATER", 240, 243.5), ("…", 244, 252),
              ("THE HOUSE IS SORRY", 256, 263.5)]
    for s, b0, b1 in labels:
        banner(st, s, b, b0, b1)
    if b >= 292:
        smoke = [(lerp(400, 300, (b - 292) / 4) + k * 160, 300 - (b - 292) * 20 - k * 30) for k in range(4)]
        for sx, sy in smoke:
            st.ellipse("far", sx, sy, 90, 50)
    fore_leaves(st, b, 1, 2.0)
    glow = ((640, 470), 420, (255, 190, 80), clamp((b - 218) / 20) * (1 - clamp((b - 292) / 4)))
    return st.compose(backdrop(b, glow=glow), far_tint=0.6)


def sc_return(b):
    """In the fire light the family walks back into the wall, each into its own lit place."""
    st = Stage(b)
    west_wall(st, b)
    gate(st, x=GATE_NIGHT)
    lawn(st, b)
    fam = family_wall_poses()
    for i, (rig, root0, pose0, face0, who) in enumerate(fam):
        b0 = 266 + i * 3
        homes = [610, 700, 790, 870]
        if b >= b0 + 3:
            continue  # absorbed: the lit hole is all that is left
        if b < b0:
            x = homes[i]; pose = stand(); face = -1
        else:
            u = clamp((b - b0) / 3)
            if u < 0.66:
                k = u / 0.66
                x = lerp(homes[i], root0[0], ease(k)); pose = walk(b * math.pi); face = -1 if root0[0] < homes[i] else 1
            else:
                k = (u - 0.66) / 0.34
                x = root0[0]; pose = {n: lerp(stand().get(n, 0), pose0.get(n, 0), ease(k)) for n in set(pose0) | set(stand())}; face = face0
        r = legs_to_floor(rig, (x, FLOOR - 100), pose, FLOOR, face)
        draw_rig(st, rig, r, pose, face=face, tag="-return")
    # the dog outside the gate
    p = dog_stand(wag=-20); p["head"] = -20
    r = legs_to_floor(DOG, (1170, FLOOR - 70), p, FLOOR, -1)
    draw_rig(st, DOG, r, p, face=-1, tag="-return")
    flame(st, 1250, FLOOR, 240, b, 3); flame(st, 960, 300, 0, b, 5)
    return st.compose(backdrop(b, glow=((1100, 520), 360, (255, 170, 60), 0.9)), far_tint=0.6)


def sc_rain(b):
    st = Stage(b)
    west_wall(st, b, x_shift=300)
    st.poly("far", [(0, FLOOR), (0, 560), (300, 520), (600, 540), (900, 500), (W, 520), (W, FLOOR)])
    for k in range(5):
        sx = (k * 300 + b * 6) % 1500 - 100
        st.ellipse("far", sx, 200 + 30 * math.sin(k), 140, 40)
    lawn(st, b)
    # the dog lies at the foot of the wall under the girl's place, head on paws; the tail moves once
    p = dog_stand(wag=-50 + (20 * math.sin((b - 316) * math.pi) if 316 <= b < 318 else 0))
    p.update(dict(hthigh_n=-80, hshin_n=118, hthigh_f=-76, hshin_f=118, fleg_n=-70, fpaw_n=-20, fleg_f=-66, fpaw_f=-24, neck=40, head=-30))
    r = legs_to_floor(DOG, (1000, FLOOR - 40), p, FLOOR, -1)
    draw_rig(st, DOG, r, p, face=-1, tag="-rain")
    # rain: thin black lines; ripples on the contact plane
    rnd = random.Random(int(b * 6))
    for k in range(140):
        x = rnd.uniform(0, W + 200); y = rnd.uniform(-40, FLOOR)
        st.line("mid", [(x, y), (x - 10, y + 34)], 1.3)
    for k in range(8):
        x = (k * 173 + b * 37) % W; u = (b * 2 + k * 0.3) % 1
        st.ellipse("paint", x, FLOOR + 30, 30 * u, 4 * u, int(180 * (1 - u)))
    banner(st, "2:26 · NOBODY HOME", b, 318, 323.5, x=800, y=120)
    banner(st, "I WILL KEEP THE LIGHT ON.", b, 324, 333, x=800, y=120)
    im = st.compose(backdrop(b, corrugate=1.0), far_tint=0.3)
    return im


def sc_end(b):
    st = Stage(b)
    flick = 1.0 if not (334 <= b < 334.5) else 0.3
    west_wall(st, b, holes_lit=(1, 1, 1, flick), x_shift=300)
    lawn(st, b)
    im = st.compose(backdrop(b, corrugate=1.0), far_tint=0.3)
    d = ImageDraw.Draw(im)
    f = font("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", 58)
    if b >= 336:
        for row, word in enumerate(("CORRUGATED", "SKY")):
            tr = 18 if row == 0 else 60
            ws = [d.textlength(c, font=f) for c in word]; tot = sum(ws) + tr * (len(word) - 1)
            x = 900 - tot / 2
            for c, w in zip(word, ws):
                d.text((x, 160 + row * 72), c, font=f, fill=RED, anchor="lm"); x += w + tr
    return im


def _zoom(im, z, cx, cy):
    if z <= 1.001: return im
    cw, ch = W / z, H / z
    x0 = clamp(cx - cw / 2, 0, W - cw); y0 = clamp(cy - ch / 2, 0, H - ch)
    return im.transform((W, H), Image.AFFINE, (cw / W, 0, x0, 0, ch / H, y0), resample=Image.BICUBIC)


SCENES = [(-10, 16, "title"), (16, 64, "house"), (64, 112, "wall"), (112, 176, "night"), (176, 208, "proof"), (208, 264, "fire"),
          (264, 280, "return"), (280, 296, "fire"), (296, 334, "rain"), (334, 400, "end")]


def render_frame(f):
    f = frame_time_on_twos(f)  # shadow theatre timing: poses on twos (12 fps), shown at 24 fps
    t = f / FPS
    b = B(t)
    name = next(n for b0, b1, n in SCENES if b0 <= b < b1)
    if name == "title": im = sc_title(None, b)
    elif name == "house":
        im = render_house_morning(b)
        z = 1.0 + 0.32 * ease(clamp((b - 18) / 4)) * (1 - ease(clamp((b - 60) / 3)))
        im = _zoom(im, z, 620, 400)
    elif name == "wall": im = sc_wall(b)
    elif name == "night": im = sc_night(b)
    elif name == "proof":
        im = sc_gate(b)
        z = 1.0 + 0.55 * ease(clamp((b - 176) / 2)) * (1 - ease(clamp((b - 206) / 2)))
        if z > 1.001:
            cw, ch = W / z, H / z
            x0 = clamp(660 - cw / 2, 0, W - cw); y0 = clamp(500 - ch / 2, 0, H - ch)
            im = im.transform((W, H), Image.AFFINE, (cw / W, 0, x0, 0, ch / H, y0), resample=Image.BICUBIC)
    elif name == "fire":
        im = sc_fire(b)
        z = 1.25 * (1 - ease(clamp((b - 276) / 6))) + 1.0 * ease(clamp((b - 276) / 6)) if b < 264 or b >= 280 else 1.0
        if b < 212: z = lerp(1.0, 1.25, ease(clamp((b - 208) / 4)))
        im = _zoom(im, z, 640, 400)
    elif name == "return": im = sc_return(b)
    elif name == "rain": im = sc_rain(b)
    else: im = sc_end(b)
    # cutout timing: the whole film is posed on twos (12 fps), as shadow theatre; the beat grid stays exact
    if t > DUR - 2.2:
        im = Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), clamp((t - (DUR - 2.2)) / 2.0))
    return im


def frame_time_on_twos(f):
    return f - (f % 2)


# ---------------------------------------------------------------- SFX cue sheet
def build_sfx():
    S = []
    add = lambda b, k, g=1.0: S.append((b, k, g))
    for b0 in (20, 28, 38, 44, 52, 80, 96, 114, 210, 216, 224, 226, 228, 236, 240, 256, 318, 324):
        add(b0, "bell", 0.6)
    for i in range(4): add(24 + i, "plate", 0.7)
    add(30, "pop", 0.8)
    for i in range(4): add(32 + i, "chair", 0.5)
    add(46, "door", 0.6); add(50, "door", 0.6)
    for b in range(36, 52): add(b, "tick", 0.25)
    add(72, "whimper", 0.4); add(92, "whimper", 0.5)
    for i in range(4): add(120 + 4 * i, "peel", 0.6)
    add(142, "whoosh", 0.4); add(146, "bounce", 0.5); add(148, "bounce", 0.4); add(150, "gate", 0.7); add(155, "gate_shut", 0.8)
    # proof
    for i in range(6): add(178 + i, "step_wood", 0.6)
    add(188, "breath", 0.4); add(190, "chime", 0.9); add(196, "horn", 0.6); add(198.5, "release", 0.7)
    for i in range(6): add(200 + i, "step_wood", 0.5)
    add(215, "crash", 0.9); add(218, "whoomp", 0.8)
    for i in range(8): add(218 + i * 4, "crackle", 0.5)
    add(226, "spray", 0.5); add(244, "drip", 0.6)
    for i in range(4): add(266 + 3 * i + 2.5, "peel", 0.6)
    for k in range(8): add(280 + k * 1.5 + 0.4, "crash", 0.5)
    add(296, "rain", 0.55); add(316, "whimper", 0.35); add(334, "flick", 0.5)
    return S


def proof_trace():
    """Contact + limit trace for the proof (b176-208), frame by frame, for the invariant test."""
    CONTACT_LOG.clear(); LIMIT_LOG.clear()
    rows = []
    f0, f1 = int(T(176) * FPS), int(T(208) * FPS)
    for f in range(f0, f1):
        b = B(f / FPS)
        n0 = len(CONTACT_LOG)
        S = proof_state(b)
        solve_girl(S["girl"]); solve_dog(S["dog"])
        rows.append({"frame": f, "beat": round(b, 3), "contacts": [(w, n, round(r, 4)) for w, n, r in CONTACT_LOG[n0:]]})
    return rows, list(LIMIT_LOG)
