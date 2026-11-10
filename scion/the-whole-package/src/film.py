"""THE WHOLE PACKAGE - multiplane timeline on the 110.445 BPM grid (beatgrid.json).

b0 title | b16 day: she walks home past neighbours whose windows go dark | b64 the house warns |
b96 the storm front advances plane by plane | b112-144 PROOF: follows the light through grass, laundry,
boxes into fog; loses it; a nearer hand | b144 the door | b150 sealed inside | b175 labour (bass section) |
b191 dawn: fog lifts near-to-far; the package | b240 title, fade.
"""
import json, math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from engine import W, H, ROOT, LEDGER, font, FONT_MONO, _ac
from mp import F, HORIZON, Fog, proj, scale_at, blur_for, apply_blur, glow, blit_center
import cast as C

G = json.load(open(os.path.join(os.path.dirname(__file__), "beatgrid.json")))["grid"]
PER, OFF = G["period"], G["offset"]
FPS = 24
DUR = 150.93


def T(b): return OFF + b * PER
def B(t): return (t - OFF) / PER
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, u): return a + (b - a) * u
def ease(u): u = clamp(u); return u * u * (3 - 2 * u)
def seg(b, b0, b1): return clamp((b - b0) / (b1 - b0))


FOG_GOLD = (212, 176, 86)
FOG_DAWN = (236, 214, 206)
RED = (242, 56, 44)
FONT_TITLE = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"

A = None


def assets():
    global A
    if A is None:
        A = {}
        A["fog"] = Fog(5)
        A["house"], A["house_pv"] = C.make_house()
        A["village"], A["wins"], A["vs"] = C.make_village()
        A["hills_far"] = C.make_hills(30, 3, (126, 132, 120), 260, 520)
        A["hills_near"] = C.make_hills(18, 8, (92, 104, 82), 160, 460)
        A["package"] = C.make_package()
        A["glow_big"] = glow(160, C.WARM, 0.9); A["glow_mid"] = glow(70, C.WARM, 1.0); A["glow_small"] = glow(26, (255, 236, 200), 1.0)
        A["mono"] = font(FONT_MONO, 26); A["mono_big"] = font(FONT_MONO, 40)
    return A


# ------------------------------------------------------------------ the world: where things are (world units)
HOUSE_X, HOUSE_Z = 1150.0, 6.0
GROUND = 220.0        # world y of the ground line at any z (screen y = HORIZON + (GROUND - cam_y)/z*F)
VILLAGE_X0 = -1200.0


def woman_path(b):
    """(x, z, pose, facing, phase, extras) for the exterior shots."""
    if b < 64:
        x = lerp(-650, 980, seg(b, 16, 60)); return x, 4.6, ("walk" if b < 60 else "stand"), 1, (b - 16) * math.pi, {"box": b < 61}
    if b < 88:
        return 980, 4.6, "stand", 1 if b < 80 else -1, 0, {"head_turn": 1 if 80 <= b < 84 else 0}
    if b < 96:
        return lerp(980, 640, seg(b, 88, 96)), 4.6, "walk", -1, (b - 88) * math.pi, {}
    if b < 112:
        x = lerp(640, 300, seg(b, 100, 110)); return x, 4.2, ("walk" if 100 <= b < 110 else "stand"), -1 if b < 111 else 1, (b - 100) * math.pi, {}
    # PROOF
    if b < 130:
        x = lerp(300, 900, seg(b, 113.5, 130)); return x, 4.2, ("walk" if b >= 113.5 else "stand"), 1, (b - 113.5) * math.pi * 0.9, {}
    if b < 136:
        look = [0, -1, 1, -1, 0, 0][int(min(5, b - 130))]
        return 900, 4.2, "stand", (1 if look >= 0 else -1), 0, {"head_turn": abs(look)}
    if b < 140:
        return 900, 4.2, "reach", 1, 0, {"reach": ease(seg(b, 136.5, 139))}
    if b < 144:
        x = lerp(900, 1060, seg(b, 140, 144)); return x, 4.2, "walk", 1, (b - 140) * math.pi, {}
    return lerp(1060, HOUSE_X + 20, seg(b, 144, 148.5)), lerp(4.2, 5.95, seg(b, 144, 148.5)), "walk", 1, (b - 144) * math.pi, {}


def camera(b):
    if b < 16:   # title: racing pan (motion-blurred plate)
        return {"x": lerp(-1200, 2400, b / 16), "y": 0.0}
    if b < 64:
        wx = woman_path(b)[0]; return {"x": wx + 220, "y": 0.0}
    if b < 96:
        return {"x": lerp(1060, 900, seg(b, 64, 96)), "y": 0.0}
    if b < 112:
        return {"x": lerp(900, 460, seg(b, 96, 111)), "y": 0.0}
    if b < 130:
        wx = woman_path(b)[0]; return {"x": wx + 120, "y": 0.0}
    if b < 140:
        return {"x": 1020 + 14 * math.sin((b - 130) * 0.7), "y": 0.0}     # drift while she is lost
    if b < 150:
        return {"x": lerp(1020, 1180, seg(b, 140, 146)), "y": 0.0}
    return {"x": lerp(1080, 1180, seg(b, 191, 240)), "y": 0.0}


def fog_state(b):
    """Named atmosphere state + sigma(z) density per world unit of depth."""
    if b < 16:
        return "reveal", lambda z: 0.004
    if b < 64:
        return "reveal", lambda z: 0.004 + 0.0004 * z
    if b < 96:
        k = seg(b, 64, 96)
        return "lure", lambda z: 0.006 + 0.03 * k * clamp((z - 20) / 20)
    if b < 112:
        zf = lerp(60, 7, ease(seg(b, 96, 110)))         # storm front sweeps toward camera
        return "obscure", lambda z: 0.01 + 0.07 * clamp((z - zf) / 4 + 0.5)
    if b < 130:
        return "lure", lambda z: 0.02 + 0.9 * clamp((z - 4.6) / 1.0)
    if b < 134:
        k = ease(seg(b, 130, 131.5))
        return "obscure", lambda z: 0.02 + 0.9 * clamp((z - 4.6) / 1.0) + 0.55 * k * clamp((z - 2.6) / 1.0)
    if b < 136.5:
        return "suspend", lambda z: 0.02 + 0.9 * clamp((z - 4.6) / 1.0) + 0.55 * clamp((z - 2.6) / 1.0)
    if b < 150:
        k = ease(seg(b, 139, 143))   # local reveal: the house is right there
        k2 = ease(seg(b, 137, 139))     # the hand arrives: the fog around her thins first, the house later
        return "reveal", lambda z: lerp(0.02 + 0.9 * clamp((z - 4.6) / 1.0) + 0.55 * (1 - k2) * clamp((z - 2.6) / 1.0), 0.02 + 0.06 * clamp((z - 7) / 6), k)
    if b < 191:
        return "suspend", lambda z: 0.09
    zc = lerp(1.0, 70, ease(seg(b, 191, 228)))         # dawn: clears near-to-far
    return "reveal", lambda z: 0.003 + 0.09 * clamp((z - zc) / 6 + 0.5)


def sky(b):
    """Vertical gradient by mood."""
    day = ((112, 170, 214), (236, 226, 196))
    storm = ((150, 128, 70), (214, 186, 110))
    dawn = ((92, 92, 140), (246, 190, 160))
    if b < 64: top, bot = day
    elif b < 96: k = seg(b, 64, 96); top, bot = [tuple(int(lerp(a, c, k)) for a, c in zip(day[i], storm[i])) for i in (0, 1)]
    elif b < 191: top, bot = storm
    else:
        k = seg(b, 191, 226); top, bot = [tuple(int(lerp(a, c, k)) for a, c in zip(storm[i], dawn[i])) for i in (0, 1)]
    g = np.linspace(0, 1, H)[:, None]
    arr = (np.array(top)[None, None, :] * (1 - g[..., None]) + np.array(bot)[None, None, :] * g[..., None]).astype(np.uint8)
    arr = np.repeat(arr, W, 1)
    im = Image.fromarray(arr, "RGB").convert("RGBA")
    if b < 96 or b >= 191:
        sun = glow(120, (255, 244, 210) if b < 191 else (255, 200, 170), 0.85)
        sx = 980 if b < 191 else lerp(300, 380, seg(b, 191, 260)); sy = 150 if b < 191 else lerp(360, 220, seg(b, 191, 240))
        blit_center(im, sun, sx, sy)
    return im


# ------------------------------------------------------------------ messages (the house's worldtext)
MESSAGES = [(40, 47, "POLLEN COUNT: HIGH."), (52, 59, "COME INSIDE SOON."), (64, 71, "THE WIND HAS TURNED."),
            (72, 79, "STORM IN TWO HOURS."), (80, 87, "THEY HAVE CLOSED THEIR DOORS."), (88, 95, "STAY CLOSE TO ME."),
            (112, 119, "FOLLOW MY LIGHT."), (131, 136, "I CANNOT SEE YOU."), (138, 143, "HERE."),
            (151, 158, "SEALING."), (166, 174, "THE AIR INSIDE IS CLEAN."), (176, 183, "BREATHE WITH ME."),
            (184, 190, "AGAIN. WITH ME."), (216, 223, "HANDLE WITH CARE.")]


def message(b):
    for b0, b1, txt in MESSAGES:
        if b0 <= b < b1:
            return txt, b - b0, b1 - b0
    return None


def draw_message(dst, b, pos):
    m = message(b)
    if not m: return
    txt, u, L = m
    a = A
    n = int(len(txt) * clamp(u / 0.8))                   # types on over ~1 beat
    alpha = clamp((L - u) / 0.6)
    f = a["mono_big"]
    d = ImageDraw.Draw(dst)
    bb = d.textbbox((0, 0), txt, font=f)
    x = pos[0] - (bb[2] - bb[0]) / 2; y = pos[1]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
    dl.text((x, y), txt[:n], font=f, fill=(255, 226, 170, int(255 * alpha)))
    halo = layer.filter(ImageFilter.GaussianBlur(6))
    dst.alpha_composite(halo); dst.alpha_composite(layer)


# ------------------------------------------------------------------ exterior frame compositor
def plate_item(img, s, world_x0, z, cam, wy=GROUND, anchor_bottom=True):
    """A static plate whose left edge is at world_x0 and whose bottom sits on the ground line at z."""
    sx = W / 2 + (world_x0 - cam["x"]) / z * F
    sy = HORIZON + (wy - cam["y"]) / z * F
    return sx, sy - img.height if anchor_bottom else sy


def exterior(b, t):
    a = assets()
    cam = camera(b)
    state, sigma = fog_state(b)
    storm = {"reveal": 0.2, "lure": 0.45, "obscure": 1.0, "suspend": 0.0}[state]
    if b < 96: storm = 0.15 + 0.35 * seg(b, 64, 96)
    if 96 <= b < 112: storm = 0.6 + 0.4 * seg(b, 96, 104)
    if 112 <= b < 130: storm = 0.75
    wind = storm
    focus_z = 4.4 if 112 <= b < 150 else (5.0 if b < 112 else 6.0)
    fog_col = FOG_GOLD if b < 191 else tuple(int(lerp(c1, c2, seg(b, 191, 220))) for c1, c2 in zip(FOG_GOLD, FOG_DAWN))
    canvas = sky(b)
    items = []  # (z, fn(layer))

    def plate(key, x0, z, wy=GROUND):
        img, s = a[key]
        def fn(L):
            sx, sy = plate_item(img, s, x0, z, cam, wy)
            _ac(L, img, sx, sy)
        return (z, fn)
    items.append(plate("hills_far", -3000, 30, GROUND + 120))
    items.append(plate("hills_near", -2600, 18, GROUND + 40))

    def village(L):
        img = a["village"]; s = a["vs"]
        sx, sy = plate_item(img, s, VILLAGE_X0, 14, cam)
        _ac(L, img, sx, sy)
        d = ImageDraw.Draw(L)
        for i, (x0, y0, x1, y1) in enumerate(a["wins"]):
            # windows close one by one as she passes (b20-b56) ... and relight at dawn (b232+)
            dark_at = 20 + i * 1.6
            lit = (b < dark_at) or (b >= 232 + i * 0.8)
            col = (255, 214, 120, 255) if lit else (34, 30, 40, 255)
            d.rectangle([sx + x0, sy + y0, sx + x1, sy + y1], fill=col)
    items.append((14.0, village))

    def house(L):
        img = a["house"]; pvx, pvy = a["house_pv"]
        p = proj(HOUSE_X, GROUND, HOUSE_Z, cam)
        _ac(L, img, p[0] - pvx, p[1] - pvy)
        d = ImageDraw.Draw(L)
        ex, ey, er = C.HOUSE_EYE
        cx, cy = p[0] - pvx + ex, p[1] - pvy + ey
        on = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(b * math.pi)) if 175 <= b < 191 else 1.0
        d.ellipse([cx - er, cy - er, cx + er, cy + er], fill=(int(255 * on), int(206 * on), int(120 * on), 255), outline=(60, 40, 24, 255), width=4)
        x0, y0, x1, y1 = C.HOUSE_DOOR
        dx0, dy0 = p[0] - pvx + x0, p[1] - pvy + y0
        opened = (144 <= b < 149.2) or (208 <= b)
        if opened:
            d.rectangle([dx0, dy0, dx0 + (x1 - x0), dy0 + (y1 - y0)], fill=(255, 190, 110, 255))
        else:
            d.rectangle([dx0, dy0, dx0 + (x1 - x0), dy0 + (y1 - y0)], fill=(120, 84, 50, 255), outline=(60, 40, 24, 255), width=3)
        if 149 <= b < 200:   # sealed: tape crosses
            d.line([(dx0 - 10, dy0), (dx0 + (x1 - x0) + 10, dy0 + (y1 - y0))], fill=(214, 186, 128, 255), width=12)
            d.line([(dx0 + (x1 - x0) + 10, dy0), (dx0 - 10, dy0 + (y1 - y0))], fill=(214, 186, 128, 255), width=12)
        if b >= 200:   # flaps open at dawn
            pass
        A["_eye"] = (cx, cy, er)
    items.append((HOUSE_Z, house))

    # woman
    if b < 149.2 or b >= 210:
        if b < 149.2:
            wx, wz, pose, face, phase, ex = woman_path(b)
        else:
            wx, wz, pose, face, phase, ex = HOUSE_X + 30, 5.9, "hold", 1, 0, {}
            if b >= 224:   # she comes out, onto the step
                wx = lerp(HOUSE_X + 30, HOUSE_X - 110, seg(b, 224, 230)); wz = lerp(5.9, 4.8, seg(b, 224, 230))
                pose = "walk" if b < 230 else "hold"; phase = (b - 224) * math.pi
        def wfn(L, wx=wx, wz=wz, pose=pose, face=face, phase=phase, ex=ex):
            p = proj(wx, GROUND, wz, cam)
            fade = 1.0
            if 147.5 <= b < 149.2: fade = clamp((149.2 - b) / 1.7)
            hand = C.woman(L, p[0], p[1], F / wz * 1.25, pose=pose if pose != "hold" else "stand", face=face, phase=phase,
                           box=ex.get("box", False), head_turn=ex.get("head_turn", 0), reach=ex.get("reach", 0),
                           alpha=int(255 * fade), baby=(pose == "hold"))
            A["_hand"] = hand
        items.append((wz, wfn))

    # occluders and props in front of her
    if 64 <= b < 150:
        def laundry(L):
            d = ImageDraw.Draw(L)
            for k, (lx, lz) in enumerate(([(560, 3.3)] if b < 112 else [(520, 2.7)])):
                p0 = proj(lx, GROUND - 190, lz, cam); p1 = proj(lx + 360, GROUND - 190, lz, cam)
                s = F / lz
                d.line([p0, p1], fill=(40, 34, 30, 255), width=max(2, int(s)))
                for j in range(3):
                    if b >= 96 and b < 112 and j == 2 and b > 104: continue   # one sheet torn away by the storm
                    x0 = lerp(p0[0], p1[0], 0.05 + j * 0.32)
                    pts = C.sheet_poly(x0, p0[1], 90 * s, 110 * s, t, j * 1.7, wind)
                    d.polygon(pts, fill=(226, 214, 176, 235), outline=(70, 60, 44, 255))
                for post in (p0, p1):
                    d.line([post, (post[0], HORIZON + (GROUND - cam["y"]) / lz * F)], fill=(40, 34, 30, 255), width=max(3, int(s * 1.4)))
        items.append((2.7 if b >= 112 else 3.3, laundry))
    if 112 <= b < 150:
        def boxes(L):
            d = ImageDraw.Draw(L)
            z = 2.0; s = F / z
            p = proj(820, GROUND, z, cam)
            k = 0
            for row in range(3):
                for col in range(2 - row // 2):
                    x0 = p[0] + (col * 70 + row * 18) * s; y1 = p[1] - row * 64 * s
                    C.box_face(d, x0, y1 - 64 * s, x0 + 70 * s, y1, 30 + k); k += 1
        items.append((2.0, boxes))

        def arm(L):
            if b < 136: return
            d = ImageDraw.Draw(L)
            k = ease(seg(b, 136, 138.5))
            if b >= 139: k = 1
            hx, hy = A.get("_hand", (W / 2, H / 2))
            tip = (lerp(W + 260, hx + 30, k), lerp(140, hy - 2, k))
            base = (W + 220, 40)
            elbow = (lerp(base[0], tip[0], 0.5) + 60, lerp(base[1], tip[1], 0.5) - 70)
            DK = (96, 66, 40, 255); LT = (186, 142, 90, 255)
            for p_, q_, w_ in ((base, elbow, 46), (elbow, tip, 34)):
                d.line([p_, q_], fill=DK, width=w_)
                n = 5
                for i in range(n):
                    u = (i + 0.5) / n; m = (lerp(p_[0], q_[0], u), lerp(p_[1], q_[1], u))
                    d.line([(m[0] - w_ * 0.45, m[1] - w_ * 0.2), (m[0] + w_ * 0.45, m[1] + w_ * 0.2)], fill=LT, width=4)   # box seams
            d.ellipse([elbow[0] - 30, elbow[1] - 30, elbow[0] + 30, elbow[1] + 30], fill=DK, outline=LT, width=4)
            # cardboard hand: palm + three fingers, open toward her
            px, py = tip
            d.ellipse([px - 26, py - 20, px + 26, py + 20], fill=(206, 160, 104, 255), outline=DK, width=4)
            for j in range(3):
                d.line([(px - 14, py - 10 + j * 10), (px - 40, py - 14 + j * 12)], fill=(206, 160, 104, 255), width=11)
            A["_tip"] = tip
        items.append((3.0, arm))
    # foreground grass
    def grass(L):
        d = ImageDraw.Draw(L)
        C.grass_strip(d, cam["x"], 1.5, t, wind, (30, 36, 26, 255), seed=2, dens=110 if 112 <= b < 130 else 50)
    items.append((1.5, grass))

    # composite back to front with depth fog slabs
    items.sort(key=lambda it: -it[0])
    fog = a["fog"]
    zs = [it[0] for it in items] + [0.9]
    drift = t * 18 * (0.3 + wind)
    for i, (z, fn) in enumerate(items):
        r = blur_for(z, focus_z)
        if r >= 0.6:
            L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fn(L); canvas.alpha_composite(apply_blur(L, r))
        else:
            fn(canvas)
        z_near = zs[i + 1]
        zm = (z + z_near) / 2
        tau = sigma(zm) * (z - z_near) + sigma(z) * 0.0
        al = 1 - math.exp(-tau * 6.0)
        if al > 0.01:
            canvas.alpha_composite(fog.slab(i, cam["x"] * F / zm + drift, 40 * math.sin(t * 0.3 + i), min(0.96, al * 1.15),
                                            fog_col, contrast=1.6, floor=0.35))
    # pollen motes (a few depth bands, parallax-correct)
    d = ImageDraw.Draw(canvas)
    rnd = random.Random(5)
    nm = int(40 + 220 * storm) if b >= 16 else 20
    for i in range(nm):
        z = rnd.uniform(1.6, 14); wx = rnd.uniform(-2000, 4000); wy = rnd.uniform(-200, 300)
        ph = rnd.uniform(0, 6)
        still = (state == "suspend")
        mx = wx + (0 if still else (t * 40 * (0.4 + wind) + 30 * math.sin(t + ph)))
        p = proj(mx, wy + (0 if still else 10 * math.sin(t * 1.3 + ph)), z, cam)
        px = (p[0] % (W + 200)) - 100
        r = max(1, 4 * F / z / 2)
        d.ellipse([px - r, p[1] - r, px + r, p[1] + r], fill=(250, 222, 120, 200))
    # the light (house eye) seen through fog: a halo whose size and drift = the "lure"
    if "_eye" in A and b < 150:
        cx, cy, er = A["_eye"]
        tau_h = sigma(HOUSE_Z) * HOUSE_Z
        if state == "lure" and 112 <= b < 130:
            g = A["glow_big"]; sc = 1.0 + 0.6 * math.sin(b * 0.9) ** 2
            gi = g.resize((int(g.width * sc), int(g.height * sc)))
            blit_center(canvas, gi, cx, cy)
        elif state in ("obscure", "suspend") and 130 <= b < 139:
            k = 1 - seg(b, 130, 131.5)
            if k > 0.02:
                gi = A["glow_big"].copy(); gi.putalpha(gi.split()[3].point(lambda v: int(v * k))); blit_center(canvas, gi, cx, cy)
        else:
            blit_center(canvas, A["glow_mid"], cx, cy)
    if "_tip" in A and 136 <= b < 144:
        tip = A["_tip"]; blit_center(canvas, A["glow_small"], tip[0], tip[1])
    if b >= 191 and "_eye" in A:
        cx, cy, er = A["_eye"]; soft = 1 - 0.6 * seg(b, 232, 256)
        gi = A["glow_mid"].copy(); gi.putalpha(gi.split()[3].point(lambda v: int(v * soft))); blit_center(canvas, gi, cx, cy)
    A.pop("_tip", None)
    return canvas


# ------------------------------------------------------------------ interior (b150-191)
def interior(b, t):
    a = assets()
    pulse = 0.5 + 0.5 * math.cos((b % 1) * 2 * math.pi) if 175 <= b < 191 else 0.5
    dim = 1.0 if b < 175 else 0.72 + 0.28 * pulse
    base = np.zeros((H, W, 3), np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = 900, 230
    d2 = ((xx - cx) / 700.0) ** 2 + ((yy - cy) / 500.0) ** 2
    lightk = np.exp(-d2 * 1.6)[..., None]
    wall = np.array([120, 84, 48], np.float32); hot = np.array([255, 196, 116], np.float32)
    base = (wall * 0.55 + (hot - wall * 0.55) * lightk) * dim
    # corrugation
    base *= (1 - 0.06 * (np.sin(xx / 3.2) > 0.6))[..., None]
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(im)
    # window slit with fog pressing outside, closed by boxes sliding in (b150-158)
    wx0, wy0, wx1, wy1 = 160, 150, 420, 330
    close = ease(seg(b, 152, 158))
    fogpatch = a["fog"].slab(2, t * 30, 0, 0.95, FOG_GOLD, contrast=1.8, floor=0.5).crop((wx0, wy0, wx1, wy1))
    im.alpha_composite(fogpatch, (wx0, wy0))
    for k, (dx) in enumerate((0, 1)):
        cover = int((wx1 - wx0) / 2 * close)
        if k == 0: d.rectangle([wx0, wy0, wx0 + cover, wy1], fill=(150, 110, 66, 255), outline=(70, 50, 30, 255), width=3)
        else: d.rectangle([wx1 - cover, wy0, wx1, wy1], fill=(150, 110, 66, 255), outline=(70, 50, 30, 255), width=3)
    # tape across seams on beats
    for i, bt in enumerate((154, 156, 158, 160, 162, 164)):
        if b >= bt:
            y = 140 + i * 70; k = clamp((b - bt) / 0.5)
            d.line([(0, y), (W * k, y + 20)], fill=(212, 184, 126, 230), width=16)
    # floor box she sits on
    d.rectangle([560, 520, 860, 720], fill=(150, 110, 66, 255), outline=(70, 50, 30, 255), width=4)
    arch = 0.0
    if 175 <= b < 191:
        u = b % 1; arch = max(0, math.sin(u * math.pi)) * (0.6 if int(b) % 2 == 0 else 0.3)
    hand = C.woman(im, 700, 530, 2.4, pose="sit", face=1, arch=arch, color=(36, 22, 18))
    # the house's arms hold her hands (from upper right)
    if b >= 160:
        k = ease(seg(b, 160, 164))
        for j, off in enumerate((0, 40)):
            tip = (lerp(W + 60, hand[0] + 30 + off, k), lerp(120 + off, hand[1] - 6 + off * 0.3, k))
            d.line([(W + 80, 100 + off * 2), ((W + tip[0]) / 2, tip[1] - 90), tip], fill=(150, 112, 70, 255), width=22, joint="curve")
            d.ellipse([tip[0] - 16, tip[1] - 12, tip[0] + 16, tip[1] + 12], fill=(214, 176, 120, 255), outline=(70, 50, 30, 255), width=3)
    # the eye-light inside: pulses with the beat in labour
    g = a["glow_big"]; sc = 1.0 + (0.35 * pulse if 175 <= b < 191 else 0)
    gi = g.resize((int(g.width * sc), int(g.height * sc))); blit_center(im, gi, cx, cy)
    draw_message(im, b, (W / 2 + 120, 610 if b < 175 else 90))
    return im


# ------------------------------------------------------------------ title (Touki Bouki: red, tracked, over a motion-blurred plate)
def motion_blur_x(im, r):
    a = np.asarray(im.convert("RGB"), np.float32)
    k = int(r)
    c = np.cumsum(np.pad(a, ((0, 0), (k, k), (0, 0)), mode="edge"), axis=1)
    out = (c[:, 2 * k:, :] - c[:, :-2 * k, :]) / (2 * k)
    out = out[:, :W, :]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB").convert("RGBA")


def title(im, lines, b, b0, size=150, track=0.38, y0=None, alpha=1.0):
    d = ImageDraw.Draw(im)
    while True:
        f = font(FONT_TITLE, size)
        widest = max(sum(d.textlength(ch, font=f) for ch in ln) + track * size * (len(ln) - 1) for ln in lines)
        if widest <= W * 0.86 or size < 40: break
        size -= 4
    lh = size * 1.05
    y = (H - lh * len(lines)) / 2 if y0 is None else y0
    for li, line in enumerate(lines):
        if b < b0 + li * 1.0: break
        adv = [d.textlength(ch, font=f) for ch in line]
        total = sum(adv) + track * size * (len(line) - 1)
        x = (W - total) / 2
        for ch, w in zip(line, adv):
            d.text((x, y), ch, font=f, fill=RED + (int(255 * alpha),))
            x += w + track * size
        y += lh


def render_frame(f):
    t = f / FPS; b = B(t)
    assets()
    if b < 16:
        im = exterior(16 + (b % 4) * 6, t)          # racing through the world
        im = motion_blur_x(im, 34)
        if 2 <= b < 15:
            title(im, ["THE WHOLE", "PACKAGE"], b, 2)
        elif b >= 15:
            pass
    elif 150 <= b < 191:
        im = interior(b, t)
    else:
        im = exterior(b, t)
        if b < 150 or b >= 191:
            eye = A.get("_eye")
            pos = (W / 2, 70)
            draw_message(im, b, pos)
        if b >= 244:
            k = seg(b, 244, 247)
            plate = motion_blur_x(im, 30 * k + 1)
            im = Image.blend(im, plate, k)
            title(im, ["THE WHOLE", "PACKAGE"], b, 246)
    if b < 2:
        im = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), im, clamp(b / 2))
    if t > DUR - 5:
        im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), clamp((t - (DUR - 5)) / 4))
    return im.convert("RGB")


# ------------------------------------------------------------------ depth-placed sound cues
def cues():
    """(beat, kind, z, pan[-1..1], gain). Gain and low-pass are set from z and fog by sfx3d."""
    Q = []
    for i in range(24):
        Q.append((20 + i * 1.6, "shutter", 14.0, -0.6 + i * 0.05, 0.5))        # neighbours' windows closing
    for b0, b1, txt in MESSAGES:
        Q.append((b0, "chime", 6.0, 0.4 if b0 < 150 else 0.2, 0.8))
    for k in range(0, 44, 1):
        Q.append((16 + k, "step", 4.6, -0.2, 0.35))
    for k in range(8): Q.append((113.5 + k * 2, "step", 4.2, 0.0, 0.5))
    Q += [(116, "rustle", 1.5, -0.5, 0.8), (121, "flap", 2.7, 0.0, 0.9), (123, "flap", 2.7, 0.2, 0.7), (127.5, "knock", 2.0, 0.4, 0.6),
          (136, "whir", 3.4, 0.8, 0.8), (139, "chime", 3.4, 0.4, 1.0), (144, "door", 6.0, 0.0, 0.9), (149.2, "door", 6.0, 0.0, 1.0)]
    for i, bt in enumerate((154, 156, 158, 160, 162, 164)):
        Q.append((bt, "tape", 2.0, -0.6 + i * 0.25, 0.8))
    Q.append((152, "slide", 2.5, -0.5, 0.7))
    for k in range(16): Q.append((175 + k, "heart", 2.5, 0.0, 0.6 if k % 2 == 0 else 0.4))
    Q += [(200, "flapopen", 6.0, 0.2, 0.6), (208, "door", 6.0, 0.0, 0.6), (216, "chime", 6.0, 0.0, 0.9), (191, "bell", 30.0, -0.3, 0.7)]
    for i in range(12): Q.append((232 + i * 0.8, "pip", 14.0, -0.7 + i * 0.12, 0.35))
    Q.append((2, "hit", 1.0, 0.0, 0.9)); Q.append((3, "hit", 1.0, 0.0, 0.9)); Q.append((246, "hit", 1.0, 0.0, 0.8)); Q.append((247, "hit", 1.0, 0.0, 0.8))
    return Q


def storm_curve(b):
    """Wind bed amplitude (0..1) and how far it is (z) for the low-pass."""
    if b < 64: return 0.12, 20
    if b < 96: return 0.12 + 0.3 * seg(b, 64, 96), 14
    if b < 130: return 0.65 + 0.3 * seg(b, 96, 104), 6
    if b < 134: return 0.9, 3
    if b < 136.5: return 0.05, 3                       # suspend: the world holds its breath
    if b < 150: return 0.6 - 0.3 * seg(b, 139, 148), 5
    if b < 191: return 0.35, 40                       # heard through the sealed walls
    return 0.3 * (1 - seg(b, 191, 228)), 20
