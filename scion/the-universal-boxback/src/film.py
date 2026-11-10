"""THE UNIVERSAL BOXBACK - SCION 06 (Whitney, harmonic motion) x The House That Language Built.

Twenty corrugated boxes are one oscillator bank. Every position is a closed-form function of the beat
b (130.03 BPM grid in beatgrid.json): nothing is keyframed by hand, so every phase relation is measurable.

Score (beats):
  b0   TITLE      red letter-spaced caps over a motion-blurred plate (slate style)
  b16  END FORM   the finished house F, drawn first (Aristotle: thought starts from the end)
  b32  BACKWARD   boxes leave F in reverse making order and gather as 10 reunited A/B pairs on a ring
  b48  PROOF      3:2 procession: A laps at 3, B at 2 over 20 beats -> separation, 9 interference passes
                  (one every 2 beats), approach, reunion (b52-b72; holds either side)
  b76  STOP       the song stops (b77-79.8): the field freezes
  b80  DEVELOP    Lissajous bank, rational locks (closes every 16 beats)
  b112 DRIFT      same bank, deliberately detuned: the figure no longer closes, trails accumulate
  b144 RE-LOCK    detune returns to zero; everything reunites on b160
  b160 MAKING     making starts at the first step: one box lands per 4 beats, foundation first (plan P0)
  b238 PLATO      architect: BEAM 7 -> ROW 3. builder: CANNOT GO THERE. next direction re-phases the
                  house; the change propagates upward through the graph; beam lands b264 -> house = F
  b264 BREATHE    house holds, each box micro-orbits its slot at 3:2
  b304 POINTS     breakdown: box faces fade, the house reads from corner points alone
  b324 RELEASE    music returns: the house opens into the widest procession (sparse -> dense)
  b356 RETURN     everything converges; lands in F exactly on b368, the last downbeat
"""
import json, math, os, random
import numpy as np
from engine import *
from engine import _ac, _src

G = json.load(open(os.path.join(os.path.dirname(__file__), "beatgrid.json")))["grid"]
PER, OFF = G["period"], G["offset"]
FPS = 24
DUR = 173.5
N = 20
BEAM = 7
RED = (242, 56, 44)
WARM = np.array([255, 186, 104], float)
COOL = np.array([118, 206, 255], float)
CX, CY = 640.0, 380.0


def T(b): return OFF + b * PER
def B(t): return (t - OFF) / PER


# ------------------------------------------------------------------ the house (two plans)
COLX = [640 + (c - 2) * 90 for c in range(5)]
ROWY = {1: 590, 2: 530, 3: 470, 4: 410, 5: 350, 6: 290}
SLOT_P0, SLOT_F = {}, {}
for i, c in zip((0, 1, 2, 3), (0, 1, 3, 4)): SLOT_P0[i] = (COLX[c], ROWY[1])
for i, c in zip((4, 5, 6, 8), (0, 1, 3, 4)): SLOT_P0[i] = (COLX[c], ROWY[2])
for i, c in zip((9, 10, 11, 12, 13), range(5)): SLOT_P0[i] = (COLX[c], ROWY[3])
for i, dx in zip((14, 15, 16, 17), (-135, -45, 45, 135)): SLOT_P0[i] = (640 + dx, ROWY[4])
for i, dx in zip((18, 19), (-45, 45)): SLOT_P0[i] = (640 + dx, ROWY[5])
SLOT_P0[BEAM] = (640, ROWY[3])          # the plan's mistake: row 3 is already full
SLOT_F.update(SLOT_P0)
for i, dx in zip((10, 11, 12), (-90, 0, 90)): SLOT_F[i] = (640 + dx, ROWY[5])   # the three displaced boxes go up
for i, dx in zip((18, 19), (-45, 45)): SLOT_F[i] = (640 + dx, ROWY[6])          # which pushes the top row up
SLOT_F[BEAM] = (640, ROWY[3])
MAKE_ORDER = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]   # foundation first
F_ARR = np.array([SLOT_F[i] for i in range(N)], float)
P0_ARR = np.array([SLOT_P0[i] for i in range(N)], float)
# propagation delay (beats) of the re-phase wave: graph distance from the beam, measured in rows
WAVE = {i: 0.6 * abs(ROWY[[r for r, y in ROWY.items() if y == SLOT_F[i][1]][0]] - ROWY[3]) / 60 +
        0.15 * abs(SLOT_F[i][0] - 640) / 90 for i in range(N)}


def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def eout(u): u = min(1, max(0, u)); return 1 - (1 - u) ** 3


# ------------------------------------------------------------------ oscillator sections (closed form)
R_RING = 262.0


def ring(b, b0=52.0, span=20.0, R=R_RING, sep=60.0, cx=CX, cy=CY, floor=36.0, squash=0.80):
    """3:2 procession. A (ids 0-9) laps 3x, B (ids 10-19) 2x in `span` beats; radii split then rejoin."""
    u = (b - b0) / span
    uc = min(1, max(0, u))
    s = floor + sep * math.sin(math.pi * uc) ** 2   # reunited pairs sit as radial neighbours
    P = np.zeros((N, 2)); ang = np.zeros(N)
    for j in range(N):
        i = j % 10
        k = 3 if j < 10 else 2
        th = -math.pi / 2 + i * 2 * math.pi / 10 + k * 2 * math.pi * uc
        r = R + s if j < 10 else R - s
        P[j] = (cx + r * math.cos(th), cy + squash * r * math.sin(th))
        ang[j] = th
    return P, ang


RATIOS = [(1, 1), (1, 2), (2, 3), (3, 2), (3, 4), (4, 3), (1, 3), (2, 1), (5, 4), (4, 5)]


def bank(b, detune=0.0, amp=1.0, cyc=16.0, b0=80.0):
    """Lissajous oscillator bank; with detune=0 every figure closes every `cyc` beats."""
    P = np.zeros((N, 2))
    phi = 2 * math.pi * (b - b0) / cyc
    rng = np.random.default_rng(11)
    eps = rng.uniform(-1, 1, N)
    ring0, _ = ring(b0, b0=52, span=20)            # the bank starts from the reunited ring
    for j in range(N):
        a, c = RATIOS[j % 10]
        d = 0.0 if j < 10 else math.pi / 2
        fa = a * (1 + detune * eps[j]); fc = c * (1 - detune * eps[j] * 0.7)
        x = math.sin(fa * phi + d) * 380 * amp
        y = math.sin(fc * phi + d * 0.5) * 230 * amp
        P[j] = (CX + x, CY + y)   # centred figure; continuity with the ring is a blend in state()
    return P


def detune_at(b):
    if b < 112: return 0.0
    if b < 128: return 0.06 * ease((b - 112) / 16)
    if b < 144: return 0.06
    if b < 160: return 0.06 * (1 - ease((b - 144) / 16))
    return 0.0


def amp_at(b):
    # sparse -> dense: the bank widens as the development section grows
    if b < 96: return 0.35 + 0.35 * ease((b - 80) / 16)
    if b < 144: return 0.7 + 0.25 * ease((b - 96) / 16)
    return 0.95


def field(b):
    """b80-160 (and the source for boxes still flying during the making)."""
    bb = min(b, 160.0)
    P = bank(bb, detune_at(bb), amp_at(bb))
    if b >= 144:  # pull toward the reunited ring by b160
        k = ease((b - 144) / 16)
        R, _ = ring(72, b0=52, span=20)
        P = P * (1 - k) + R * k
    if b > 160:   # remaining boxes keep turning on the ring while the house is made
        u = (b - 160) / 32.0
        th = 2 * math.pi * u
        R = np.zeros((N, 2))
        for j in range(N):
            i = j % 10; k = 3 if j < 10 else 2
            a = -math.pi / 2 + i * 2 * math.pi / 10 + k * th
            r = 330 if j < 10 else 300
            R[j] = (CX + r * math.cos(a), CY + 0.6 * r * math.sin(a))
        k0 = ease((b - 160) / 4)
        R0, _ = ring(72, b0=52, span=20)
        P = R0 * (1 - k0) + R * k0
    return P


def flight(p0, p1, u, bulge=90.0, sign=1):
    """harmonic arc from p0 to p1: straight lerp + one half-sine perpendicular bulge."""
    u = ease(u)
    d = p1 - p0; L = np.hypot(*d) + 1e-9
    nrm = np.array([-d[1], d[0]]) / L
    return p0 + d * u + nrm * bulge * sign * math.sin(math.pi * u)


def beam_width(b):
    """the beam folds to box size while it travels with the field, and unfolds only to enter the house."""
    full, fold = 264.0, 110.0
    if b < 32: return full
    if b < 35: return full + (fold - full) * ease((b - 32) / 3)
    if b < 240: return fold
    if b < 242: return fold + (full - fold) * ease((b - 240) / 2)
    if b < 324: return full
    if b < 328: return full + (fold - full) * ease((b - 324) / 4)
    if b < 360: return fold
    if b < 366: return fold + (full - fold) * ease((b - 360) / 6)
    return full


def land_beat(k): return 164 + 4 * k     # k-th box of MAKE_ORDER lands on this beat


def state(b):
    """positions (N,2), rotation deg (N,), scale (N,), glow (N,), outline alpha, extra flags."""
    P = np.zeros((N, 2)); rotd = np.zeros(N); sc = np.ones(N); gl = np.full(N, 0.6)
    face = 1.0
    if b < 32:
        P[:] = F_ARR
    elif b < 48:
        # backward: reverse making order of F leaves first; each departs on its beat and flies 3 beats
        rev = [BEAM] + MAKE_ORDER[::-1]
        R0, _ = ring(52, b0=52, span=20)
        for n, j in enumerate(rev):
            d0 = 32 + n * 0.6
            u = (b - d0) / 3.0
            P[j] = F_ARR[j] if u <= 0 else flight(F_ARR[j], R0[j], min(1, u), 120, 1 if j % 2 else -1)
            rotd[j] = 360 * ease(min(1, max(0, u))) * (1 if j < 10 else -1)
            gl[j] = 0.6 + 0.4 * (0 < u < 1)
    elif b < 80:
        P, ang = ring(b)
        uc = min(1, max(0, (b - 52) / 20))
        for j in range(N):
            rotd[j] = math.degrees(ang[j]) + 90 if 52 <= b <= 72 else (math.degrees(ang[j]) + 90)
        rotd = rotd * ease(min(1, max(0, (b - 48) / 4)))
        gl[:] = 0.75
    elif b < 160:
        P = field(b)
        if b < 84:
            R0, ang = ring(80)
            k = ease((b - 80) / 4)
            P = R0 * (1 - k) + P * k
        rotd[:] = (b - 80) * 22 * np.array([1 if j < 10 else -1 for j in range(N)])
        if b < 84:
            _, ang80 = ring(80)
            rr = np.degrees(ang80) + 90
            kk = ease((b - 80) / 4)
            rotd = rr * (1 - kk) + rotd * kk
        gl[:] = 0.8
    elif b < 238:
        Fd = field(b)
        rotd[:] = (b - 80) * 22 * np.array([1 if j < 10 else -1 for j in range(N)])
        for k, j in enumerate(MAKE_ORDER):
            lb = land_beat(k)
            if b >= lb:
                P[j] = P0_ARR[j]; rotd[j] = 0; gl[j] = 0.5 + 0.5 * math.exp(-4 * (b - lb))
            elif b >= lb - 2:
                u = (b - (lb - 2)) / 2
                src = field(lb - 2)
                P[j] = flight(src[j], P0_ARR[j], u, 70, 1 if k % 2 else -1)
                r0 = (lb - 2 - 80) * 22 * (1 if j < 10 else -1)
                rotd[j] = r0 % 360 * (1 - ease(u)) if True else 0
                gl[j] = 1.0
            else:
                P[j] = Fd[j]
        # the beam keeps circling, alone at the end
        P[BEAM] = Fd[BEAM]
    else:
        P[:] = P0_ARR
        Fd = field(min(b, 238))
        # --- Plato: the beam is directed to row 3, collides, returns; the re-phase wave; the beam lands
        bp0 = Fd[BEAM].copy()
        hover = np.array([960.0, 250.0])
        if b < 240:
            P[BEAM] = bp0
            rotd[BEAM] = (238 - 80) * 22 % 360
        elif b < 242:      # flies to row 3
            u = (b - 240) / 2
            P[BEAM] = flight(bp0, P0_ARR[BEAM] + (0, -40), u, 60)
        elif b < 243.5:    # hits the full row: rebound up, trembling, red
            u = (b - 242) / 1.5
            P[BEAM] = (P0_ARR[BEAM] + (0, -40)) * (1 - eout(u)) + hover * eout(u)
            rotd[BEAM] = 8 * math.sin(b * 40) * (1 - u)
        elif b < 262:
            P[BEAM] = hover + (0, 6 * math.sin((b - 243.5) * math.pi))
        elif b < 264:
            u = (b - 262) / 2
            P[BEAM] = flight(hover, F_ARR[BEAM], u, 0)
        else:
            P[BEAM] = F_ARR[BEAM]
        # the row-3 boxes that the beam hits shudder at b242
        if 242 <= b < 243.5:
            for j in (10, 11, 12):
                P[j] = P0_ARR[j] + (6 * math.sin(b * 50 + j), 0)
        # re-phase wave from b252: every box ripples on its delay; displaced boxes travel P0 -> F
        if b >= 252:
            for j in range(N):
                if j == BEAM: continue
                d = 252 + WAVE[j] * 4
                u = (b - d) / 2.0
                if np.any(P0_ARR[j] != F_ARR[j]):
                    P[j] = flight(P0_ARR[j], F_ARR[j], min(1, max(0, u)), 50, 1 if j % 2 else -1) if u > 0 else P0_ARR[j]
                else:
                    P[j] = F_ARR[j]
                bump = math.sin(math.pi * min(1, max(0, u))) if 0 < u < 1 else 0
                P[j] = P[j] + (0, -14 * bump)
                gl[j] = 0.55 + 0.45 * bump
        if b >= 264:
            P[:] = F_ARR
            # breathe: micro 3:2 orbit around each slot
            if b < 324:
                amp = 3.0 if b < 304 else 0.0
                for j in range(N):
                    ph = 2 * math.pi * (b - 264) / 8
                    P[j] = F_ARR[j] + (amp * math.sin(3 * ph + j), amp * math.sin(2 * ph + j))
                gl[:] = 0.55 + 0.25 * math.exp(-5 * (b % 1))
            elif b < 356:
                # release: the house opens into the widest procession
                k = ease((b - 324) / 4)
                Pr, ang = ring(b, b0=328, span=28, R=268, sep=60)
                P = F_ARR * (1 - k) + Pr * k
                rotd[:] = np.degrees(ang) * k
                gl[:] = 0.85
            else:
                Pr, ang = ring(356, b0=328, span=28, R=268, sep=60)
                u = (b - 356) / 12.0
                for j in range(N):
                    P[j] = flight(Pr[j], F_ARR[j], min(1, u), 80, 1 if j < 10 else -1) if u < 1 else F_ARR[j]
                rotd[:] = np.degrees(ang) * (1 - ease(min(1, u)))
                gl[:] = 0.7 + 0.3 * (u >= 1) * math.exp(-4 * max(0, b - 368))
            if 304 <= b < 324:
                face = 1 - ease((b - 304) / 2) if b < 316 else ease((b - 322) / 2)
                if b >= 316 and b < 322: face = 0.0
    return P, rotd, sc, gl, face


# ------------------------------------------------------------------ sprites
def box_sprite(j, w=84, h=56, label=None, cool=False):
    ss = 3
    W_, H_ = w * ss, h * ss
    im = Image.new("RGBA", (W_ + 8, H_ + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    base = (196, 152, 96) if not cool else (166, 160, 150)
    flute = (166, 124, 72) if not cool else (132, 128, 122)
    d.rectangle([4, 4, 4 + W_, 4 + H_], fill=base + (255,))
    for x in range(4, 4 + W_, 4 * ss):
        d.line([(x, 4), (x, 4 + H_)], fill=flute + (150,), width=ss)
    d.rectangle([4 + W_ * 0.42, 4, 4 + W_ * 0.58, 4 + H_], fill=(226, 206, 166, 235))
    d.rectangle([4, 4, 4 + W_, 4 + H_], outline=(48, 30, 18, 255), width=2 * ss)
    f = font(FONT_STENCIL, (h * 0.42 if label is None else h * 0.5) * ss)
    txt = label if label is not None else str(j)
    bb = d.textbbox((0, 0), txt, font=f)
    d.text((4 + W_ * 0.2 - (bb[2] - bb[0]) / 2 if label is None else 4 + (W_ - (bb[2] - bb[0])) / 2,
            4 + (H_ - (bb[3] - bb[1])) / 2 - bb[1]), txt, font=f, fill=(34, 22, 14, 230))
    im = im.resize((im.width // ss, im.height // ss), Image.LANCZOS)
    return Sprite(im, (im.width / 2, im.height / 2), f"box_{j}",
                  {"kind": "procedural", "note": f"corrugated box {j} drawn in code", "rights": "original"})


A = None


def assets():
    global A
    if A is None:
        A = {}
        A["box"] = [box_sprite(j, 264, 40, "BEAM 7") if j == BEAM else box_sprite(j, cool=j >= 10) for j in range(N)]
        A["beam_fold"] = box_sprite(BEAM, 110, 40, "7")
        A["box_red"] = box_sprite(BEAM, 264, 40, "BEAM 7")
        im = A["box_red"].img.copy(); r, g, b_, a = im.split()
        A["box_red"].img = Image.merge("RGBA", (r.point(lambda v: min(255, v + 70)), g.point(lambda v: v // 2), b_.point(lambda v: v // 2), a))
        A["box_red"]._cache = {}
        # title plates: the producer's own BOXBACK art, motion-blurred horizontally (slate style)
        def plate(name, box):
            im = _src(name).crop(box).resize((1600, 900))
            arr = np.asarray(im, np.float32)
            k = 90
            cs = np.cumsum(np.pad(arr, ((0, 0), (k, k), (0, 0)), mode="edge"), axis=1)
            arr = (cs[:, 2 * k:] - cs[:, :-2 * k]) / (2 * k)
            arr = arr[:, :1600]
            arr = np.clip(arr * 0.85 + 10, 0, 255).astype(np.uint8)
            return Image.fromarray(arr).convert("RGBA")
        A["plate_title"] = plate("Boxback climb under sodium light.png", (0, 300, 1254, 1005))
        A["plate_end"] = plate("Boxback Mountain Frog Warehouse.png", (0, 200, 1254, 905))
        LEDGER["plate_title"] = {"kind": "album-art-plate (motion-blurred)", "source": "Et tu, Brute (BOXBACK)/Boxback climb under sodium light.png",
                                 "crop_box_px": [0, 300, 1254, 1005], "rights": "producer's own BOXBACK album artwork (hartswf0/moto)"}
        LEDGER["plate_end"] = {"kind": "album-art-plate (motion-blurred)", "source": "Et tu, Brute (BOXBACK)/Boxback Mountain Frog Warehouse.png",
                               "crop_box_px": [0, 200, 1254, 905], "rights": "producer's own BOXBACK album artwork (hartswf0/moto)"}
        A["f_title"] = font(FONT_STENCIL, 100)
        A["f_end"] = font(FONT_STENCIL, 46)
        A["f_mono"] = font(FONT_MONO, 26)
        A["f_cap"] = font(FONT_MONO, 22)
    return A


def spaced(d, xy, text, f, fill, track=0.35, anchor_center=True):
    widths = [d.textbbox((0, 0), ch, font=f)[2] for ch in text]
    size = f.size
    tw = sum(widths) + track * size * (len(text) - 1)
    x = xy[0] - tw / 2 if anchor_center else xy[0]
    for ch, w in zip(text, widths):
        d.text((x, xy[1]), ch, font=f, fill=fill); x += w + track * size
    return tw


def typed(d, xy, text, b, b0, cps=10, f=None, fill=(220, 255, 230, 255), cursor=True):
    n = int(max(0, (b - b0)) * cps)
    s = text[:n]
    d.text(xy, s, font=f, fill=fill)
    if cursor and n < len(text) + 8 and int(b * 2) % 2 == 0:
        x = xy[0] + d.textbbox((0, 0), s, font=f)[2] + 4
        d.rectangle([x, xy[1] + 4, x + 16, xy[1] + f.size], fill=fill)


# ------------------------------------------------------------------ render
def corners(p, rot, w, h, s=1.0):
    c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        dx *= s; dy *= s
        out.append((p[0] + dx * c - dy * sn, p[1] + dx * sn + dy * c))
    return out


def trail_len(b):
    if 52 <= b < 72: return 14
    if 80 <= b < 112: return 10
    if 112 <= b < 160: return int(10 + 26 * min(1, (b - 112) / 16)) if b < 144 else int(36 - 26 * ease((b - 144) / 16))
    if 160 <= b < 238: return 8
    if 324 <= b < 368: return 16
    return 0


def render_frame(f):
    a = assets()
    t = f / FPS; b = B(t)
    im = Image.new("RGB", (W, H), (6, 7, 10))
    if b < 16:
        return title_frame(b, t)
    glow = np.zeros((H, W, 3), np.float32)
    gimg = Image.new("RGB", (W, H), (0, 0, 0)); gd = ImageDraw.Draw(gimg)
    P, rotd, sc, gl, face = state(b)
    # trails (closed-form history: the same function evaluated in the past)
    L = trail_len(b)
    if L:
        hist = [state(b - k * 0.09)[0] for k in range(L)]
        for j in range(N):
            col = WARM if j < 10 else COOL
            for k in range(L - 1):
                al = (1 - k / L) * 0.55
                c = tuple(int(v * al) for v in col)
                gd.line([tuple(hist[k][j]), tuple(hist[k + 1][j])], fill=c, width=2)
    # phase strings in the proof: A_i - B_i
    if 48 <= b < 80:
        for i in range(10):
            pa, pb = P[i], P[i + 10]
            gd.line([tuple(pa), tuple(pb)], fill=(90, 90, 90), width=1)
    # boxes
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if face > 0.01:
        for j in sorted(range(N), key=lambda j: (j == BEAM, j >= 10)):
            if j == BEAM:
                wd = beam_width(b)
                if wd > 180:
                    spr = a["box_red"] if 242 <= b < 262 else a["box"][j]; sx = wd / 264
                else:
                    spr = a["beam_fold"]; sx = wd / 110
                blit(layer, spr, tuple(P[j]), rotd[j], sx, 1.0, face)
            else:
                blit(layer, a["box"][j], tuple(P[j]), rotd[j], sc[j], None, face)
    im = im.convert("RGBA"); im.alpha_composite(layer)
    # corner points (the arrangement) + reunion flashes
    for j in range(N):
        w, h = (beam_width(b), 40) if j == BEAM else (84, 56)
        col = WARM if j < 10 else COOL
        if j == BEAM and 242 <= b < 262: col = np.array(RED, float)
        br = gl[j] * (1.0 if face > 0.3 else 1.4)
        for (x, y) in corners(P[j], rotd[j], w, h):
            r = 3.2 * br
            gd.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(min(255, v * br)) for v in col))
    # reunion / interference events in the proof: bright flare where pairs coincide
    for be in EVENTS:
        if 0 <= b - be["b"] < 1.2:
            k = math.exp(-4 * (b - be["b"]))
            for (x, y) in be["where"]:
                r = 16 * k + 4
                gd.ellipse([x - r, y - r, x + r, y + r], outline=(int(255 * k), int(240 * k), int(200 * k)), width=2)
    g = np.asarray(gimg, np.float32)
    g2 = np.asarray(gimg.filter(ImageFilter.GaussianBlur(5)), np.float32)
    base = np.asarray(im.convert("RGB"), np.float32)
    out = np.clip(base + g * 0.9 + g2 * 1.6, 0, 255).astype(np.uint8)
    im = Image.fromarray(out).convert("RGBA")
    d = ImageDraw.Draw(im)
    captions(d, b, a)
    if b >= 368:
        end_card(im, b, a)
    if t > DUR - 2.5:
        im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), min(1, (t - (DUR - 2.5)) / 2.3))
    return im.convert("RGB")


def captions(d, b, a):
    cap = a["f_cap"]; mono = a["f_mono"]
    def c(text, b0, b1, y=40):
        if b0 <= b < b1:
            al = min(1, (b - b0) / 0.5, (b1 - b) / 0.5)
            spaced(d, (640, y), text, cap, (230, 230, 220, int(255 * al)), track=0.25)
    c("THE END FORM", 16, 31)
    c("THINKING STARTS AT THE END", 32, 47)
    c("3 : 2", 48, 76)
    c("RATIONAL LOCK", 84, 111)
    c("DETUNED DRIFT", 114, 143)
    c("RE-LOCK", 146, 159)
    c("MAKING STARTS AT THE FIRST STEP", 160, 190)
    c("THE ARRANGEMENT IS THE THING", 306, 323, y=660)
    # architect / builder cards
    G_ = (205, 255, 220, 255)
    if 238 <= b < 264:
        d.rectangle([20, 70, 410, 140], fill=(0, 0, 0, 210))
        d.text((32, 76), "ARCHITECT", font=cap, fill=(140, 160, 150, 255))
        typed(d, (32, 102), "BEAM 7 -> ROW 3", b, 238, cps=9, f=mono, fill=G_, cursor=b < 241)
    if 244 <= b < 264:
        d.rectangle([840, 70, 1260, 140], fill=(0, 0, 0, 210))
        d.text((852, 76), "BUILDER", font=cap, fill=(160, 120, 110, 255))
        typed(d, (852, 102), "BEAM 7 CANNOT GO THERE", b, 244, cps=11, f=mono, fill=RED + (255,), cursor=b < 247)
    if 248 <= b < 268:
        y = 160
        lines = ["BOXES 10 11 12 -> ROW 5", "ROWS 5 6 -> RE-PHASE", "BEAM 7 -> ROW 3"]
        d.rectangle([20, 156, 410, 160 + 36 * 3 + 34], fill=(0, 0, 0, 210))
        d.text((32, 162), "ARCHITECT", font=cap, fill=(140, 160, 150, 255))
        for n, s in enumerate(lines):
            typed(d, (32, y + 30 + 36 * n), s, b, 248 + n * 1.3, cps=12, f=mono, fill=G_, cursor=False)


def title_frame(b, t):
    a = assets()
    pl = a["plate_title"]
    x = -((t * 140) % 320)            # the whip pan
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    k = ease(min(1, b / 2))
    im.alpha_composite(pl.crop((int(-x), 90, int(-x) + W, 90 + H)))
    im = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), im, k * (1 - ease((b - 14.5) / 1.5)))
    d = ImageDraw.Draw(im)
    if b >= 4: spaced(d, (640, 170), "THE", a["f_title"], RED + (255,), track=0.6)
    if b >= 6: spaced(d, (640, 290), "UNIVERSAL", a["f_title"], RED + (255,), track=0.32)
    if b >= 8: spaced(d, (640, 410), "BOXBACK", a["f_title"], RED + (255,), track=0.5)
    if b >= 10:
        spaced(d, (640, 590), "ET TU, BRUTE? · BOXBACK · 14 / 18", a["f_cap"], (240, 236, 226, 255), track=0.3)
    return im.convert("RGB")


def end_card(im, b, a):
    k = ease((b - 369) / 2)
    if k <= 0: return
    d = ImageDraw.Draw(im)
    spaced(d, (640, 70), "THE UNIVERSAL BOXBACK", a["f_end"], RED + (int(255 * k),), track=0.3)
    spaced(d, (640, 660), "ET TU, BRUTE? · BOXBACK · 14 / 18", a["f_cap"], (230, 230, 220, int(255 * k)), track=0.3)


# ------------------------------------------------------------------ events (shared by picture + sound)
def build_events():
    ev = []
    R0, _ = ring(52)
    ev.append({"b": 48.0, "kind": "reunion", "where": [tuple(R0[i]) for i in range(10)]})
    for m in range(1, 10):
        b = 52 + 2 * m
        P, _ = ring(b)
        # A_i coincides in angle with B_(i+m)
        ev.append({"b": float(b), "kind": "interference", "m": m,
                   "where": [tuple((P[i] + P[(i + m) % 10 + 10]) / 2) for i in range(10)]})
    R1, _ = ring(72)
    ev.append({"b": 72.0, "kind": "reunion", "where": [tuple(R1[i]) for i in range(10)]})
    for bl in (96, 112):
        ev.append({"b": float(bl), "kind": "lock", "where": [tuple(p) for p in bank(bl)[:: 2]]})
    Rr, _ = ring(72)
    ev.append({"b": 160.0, "kind": "reunion", "where": [tuple(Rr[i]) for i in range(10)]})
    for k, j in enumerate(MAKE_ORDER):
        ev.append({"b": float(land_beat(k)), "kind": "land", "id": j, "where": [SLOT_P0[j]]})
    ev.append({"b": 242.0, "kind": "collision", "where": [(640, 430)]})
    for j in range(N):
        if np.any(P0_ARR[j] != F_ARR[j]):
            ev.append({"b": 252 + WAVE[j] * 4 + 2, "kind": "reseat", "id": j, "where": [SLOT_F[j]]})
    ev.append({"b": 264.0, "kind": "beam_lands", "where": [SLOT_F[BEAM]]})
    ev.append({"b": 368.0, "kind": "home", "where": [tuple(p) for p in F_ARR]})
    return ev


EVENTS = build_events()
