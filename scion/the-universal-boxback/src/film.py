"""THE UNIVERSAL BOXBACK - SCION 06 (Whitney, harmonic motion) x The House That Language Built.  r2

Twenty corrugated boxes are one oscillator bank. Every position is a closed-form function of the beat b
(130.03 BPM grid, beatgrid.json). Picture time is snapped half a frame early, so beat events land on the
nearest frame rather than the following one.

Score (beats):
  b0   TITLE      red letter-spaced caps over a motion-blurred plate; plate jump-cuts every 2 beats
  b16  END FORM   the finished house F as a constellation (corner points only): the Aristotle bookend
  b32  BACKWARD   un-making, top row first: each box materialises and rises straight out (LIFO)
  b40  GATHER     boxes drop into the proof ring, lowest slot first (collision-free by construction)
  b48  PROOF      3:2 procession; markers: box 0 red (A), box 10 yellow (B); 12-o'clock tick
  b77  STOP       the song stops: field dims, glow off, label switches; returns b80
  b80  BANK       Lissajous bank. LOCK star b96; UNLOCK star b112 (detune begins); RE-LOCK star b160
  b160 MAKING     plan P0 (no door, flat roof), foundation first, one box per 4 beats
  b238 PLATO      A: BEAM 7 -> ROW 3. B: CANNOT GO THERE. A: LIFT ROOF . OPEN DOOR -> roof clears to the
                  sides, door opens -> A: BEAM 7 -> ROW 3 -> beam drops in -> A: ROOF -> NEW PLAN -> roof
                  returns in a new shape. Every row ends differently from plan P0. House = F at b264.
  b264 BREATHE    / b304 POINTS (constellation again)
  b324 RELEASE    3:2 on the wide ellipses (b328-348), the field lifts away (b348-354.9)
  b354.9 RAIN     the house rains back row by row (vertical drops, foundation first); last box lands b368
  b369 END        faces fade back to the constellation; end card
"""
import json, math, os
import numpy as np
from engine import *
from engine import _ac, _src

G = json.load(open(os.path.join(os.path.dirname(__file__), "beatgrid.json")))["grid"]
PER, OFF = G["period"], G["offset"]
FPS = 24
DUR = 173.5
FB = 1.0 / (FPS * PER)          # one frame in beats
N = 20
BEAM = 7
MARK_A, MARK_B = 0, 10
RED = (242, 56, 44)
YEL = (255, 214, 0)
WARM = np.array([255, 186, 104], float)
COOL = np.array([118, 206, 255], float)
CX, CY = 640.0, 380.0
BW, BH = 84.0, 56.0


def T(b): return OFF + b * PER
def B(t): return (t - OFF) / PER
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def eout(u): u = min(1, max(0, u)); return 1 - (1 - u) ** 3
def ein(u): u = min(1, max(0, u)); return u * u
def lerp2(p, q, u): return (p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u)


# ------------------------------------------------------------------ the house: plan P0 (made) and plan F (the end form)
COLX = [640 + (c - 2) * 90 for c in range(5)]
ROWY = {1: 590, 2: 530, 3: 470, 4: 410, 5: 350, 6: 290}
SLOT_P0, SLOT_F = {}, {}
# P0: a solid block with no door and a flat roof: there is nowhere for a beam to go
for i, x in zip((0, 1, 2, 3), (505, 595, 685, 775)): SLOT_P0[i] = (x, ROWY[1])
for i, x in zip((4, 5, 6, 8), (505, 595, 685, 775)): SLOT_P0[i] = (x, ROWY[2])
for i, c in zip((9, 10, 11, 12, 13), range(5)): SLOT_P0[i] = (COLX[c], ROWY[3])
for i, c in zip((14, 15, 16, 17, 18), range(5)): SLOT_P0[i] = (COLX[c], ROWY[4])
SLOT_P0[19] = (640, ROWY[5])
SLOT_P0[BEAM] = (640, ROWY[3])
# F: door, lintel beam, stepped roof (the end form shown first)
for i, c in zip((0, 1, 2, 3), (0, 1, 3, 4)): SLOT_F[i] = (COLX[c], ROWY[1])
for i, c in zip((4, 5, 6, 8), (0, 1, 3, 4)): SLOT_F[i] = (COLX[c], ROWY[2])
SLOT_F[9], SLOT_F[13], SLOT_F[BEAM] = (COLX[0], ROWY[3]), (COLX[4], ROWY[3]), (640, ROWY[3])
for i, x in zip((14, 15, 16, 17), (505, 595, 685, 775)): SLOT_F[i] = (x, ROWY[4])
for i, x in zip((10, 11, 12), (550, 640, 730)): SLOT_F[i] = (x, ROWY[5])
for i, x in zip((18, 19), (595, 685)): SLOT_F[i] = (x, ROWY[6])
MAKE_ORDER = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
F_ARR = np.array([SLOT_F[i] for i in range(N)], float)
P0_ARR = np.array([SLOT_P0[i] for i in range(N)], float)
F_ROWS = [[0, 1, 2, 3], [4, 5, 6, 8], [9, 13, BEAM], [14, 15, 16, 17], [10, 11, 12], [18, 19]]   # rain order


def box_w(j, b=None):
    return beam_width(b) if j == BEAM else BW


def box_h(j):
    return 40.0 if j == BEAM else BH


# ------------------------------------------------------------------ the 3:2 ring and the wide release ellipses
R_RING = 262.0


def ring(b, b0=52.0, span=20.0, R=R_RING, sep=60.0, floor=36.0, squash=0.80, spin=0.0):
    u = min(1, max(0, (b - b0) / span))
    s = floor + sep * math.sin(math.pi * u) ** 2
    P = np.zeros((N, 2)); ang = np.zeros(N)
    for j in range(N):
        i, k = j % 10, (3 if j < 10 else 2)
        th = -math.pi / 2 + i * 2 * math.pi / 10 + k * 2 * math.pi * u + spin
        r = R + s if j < 10 else R - s
        P[j] = (CX + r * math.cos(th), CY + squash * r * math.sin(th)); ang[j] = th
    return P, ang


ELL_A, ELL_B, ELL_C = (600.0, 330.0), (500.0, 260.0), (640.0, 400.0)


def ellipse_ring(b, b0=328.0, span=20.0, spin=0.0):
    """3:2 on two ellipses that enclose the house; `spin` adds a common slow turn after the reunion."""
    u = min(1, max(0, (b - b0) / span))
    P = np.zeros((N, 2)); ang = np.zeros(N)
    for j in range(N):
        i, k = j % 10, (3 if j < 10 else 2)
        th = -math.pi / 2 + i * 2 * math.pi / 10 + k * 2 * math.pi * u + spin
        rx, ry = ELL_A if j < 10 else ELL_B
        P[j] = (ELL_C[0] + rx * math.cos(th), ELL_C[1] + ry * math.sin(th)); ang[j] = th
    return P, ang


# ------------------------------------------------------------------ the oscillator bank
BANK_PH = json.load(open(os.path.join(os.path.dirname(__file__), "bank_phases.json")))
RATIOS = [(1, 1), (1, 2), (2, 3), (3, 2), (3, 4), (4, 3), (1, 3), (2, 1), (5, 4), (4, 5)]
_EPS = np.random.default_rng(11).uniform(-1, 1, N)


def bank(b, detune=0.0, amp=1.0, cyc=16.0, b0=80.0):
    P = np.zeros((N, 2))
    phi = 2 * math.pi * (b - b0) / cyc
    for j in range(N):
        a, c = RATIOS[j % 10]
        fa = a * (1 + detune * _EPS[j]); fc = c * (1 - detune * _EPS[j] * 0.7)
        P[j] = (CX + math.sin(fa * phi + BANK_PH["dx"][j]) * 380 * amp, CY + math.sin(fc * phi + BANK_PH["dy"][j]) * 230 * amp)
    return P


def detune_at(b):
    if b < 112: return 0.0
    if b < 128: return 0.06 * ease((b - 112) / 16)
    if b < 144: return 0.06
    if b < 160: return 0.06 * (1 - ease((b - 144) / 16))
    return 0.0


def amp_at(b):
    if b < 96: return 0.55 + 0.3 * ease((b - 80) / 16)
    if b < 144: return 0.85 + 0.15 * ease((b - 96) / 16)
    return 1.0


def bank_scale(b):
    if b < 80 or b >= 164: return 1.0
    if b < 84: return 1 - 0.55 * ease((b - 80) / 4)
    if b < 144: return 0.45
    if b < 145.5: return 0.45 - 0.40 * ease((b - 144) / 1.5)    # capture: the boxes collapse to points ...
    if b < 147: return 0.05
    if b < 148: return 0.05 + 0.40 * ease((b - 147) / 1.0)      # ... and regrow on the locked ring for b148
    if b < 160: return 0.45
    return 0.45 + 0.55 * ease((b - 160) / 4)


def relock_ring(b):
    """the locked ring: pairs reunited, the whole ring turning at one rate (unison)."""
    return ring(72, spin=2 * math.pi * (b - 148) / 16)


def making_orbit(b):
    u = (b - 164) / 32.0
    P = np.zeros((N, 2))
    for j in range(N):
        i, k = j % 10, (3 if j < 10 else 2)
        a = -math.pi / 2 + i * 2 * math.pi / 10 + k * 2 * math.pi * u
        rx, ry = ELL_A if j < 10 else ELL_B
        P[j] = (ELL_C[0] + rx * math.cos(a), ELL_C[1] + ry * math.sin(a))
    return P


def field(b):
    if b <= 144:
        return bank(b, detune_at(b), amp_at(b))
    if b < 147:                       # capture (as points): bank -> locked ring
        k = ease((b - 144) / 3)
        return bank(b, detune_at(b), amp_at(b)) * (1 - k) + relock_ring(b)[0] * k
    if b <= 160:
        return relock_ring(b)[0]
    if b < 164:
        k = ease((b - 160) / 4)
        return relock_ring(b)[0] * (1 - k) + making_orbit(b) * k
    return making_orbit(b)


def beam_width(b):
    full, fold = 264.0, 110.0
    if b is None or b < 32: return full
    if b < 33: return full + (fold - full) * ease((b - 32) / 1)
    if b < 240: return fold
    if b < 242: return fold + (full - fold) * ease((b - 240) / 2)
    if b < 324: return full
    if b < 328: return full + (fold - full) * ease((b - 324) / 4)
    if b < 355: return fold
    return full                     # the beam rains back at full length


def flight(p0, p1, u, bulge=90.0, sign=1):
    u = ease(u)
    d = np.asarray(p1, float) - np.asarray(p0, float); L = np.hypot(*d) + 1e-9
    nrm = np.array([-d[1], d[0]]) / L
    return np.asarray(p0, float) + d * u + nrm * bulge * sign * math.sin(math.pi * u)


def land_beat(k): return 164 + 4 * k


# --- schedules -----------------------------------------------------------------------------------
# un-making (b32-40): top rows first, each rises straight up and out (LIFO of the F rows)
RISE_ORDER = [j for row in F_ROWS[::-1] for j in sorted(row, key=lambda j: abs(SLOT_F[j][0] - 640))]
RISE = {j: 32.0 + n * 0.38 for n, j in enumerate(RISE_ORDER)}           # start beat; duration 1.2
# gather (b40-48): drops into the proof ring, lowest slot first
_R0, _A0 = ring(52)
GATHER_ORDER = sorted(range(N), key=lambda j: -_R0[j][1])
GATHER = {j: 40.0 + n * 0.33 for n, j in enumerate(GATHER_ORDER)}        # start beat; duration 1.4
# rain (b354.9-368): rows in order, a row starts when the previous row has landed
RAIN = {}
_t = 368.0 - sum(1.25 + 0.4 * (len(r) - 1) for r in F_ROWS)
for row in F_ROWS:
    for n, j in enumerate(sorted(row, key=lambda j: abs(SLOT_F[j][0] - 640))):
        RAIN[j] = _t + 0.4 * n
    _t = max(RAIN[j] for j in row) + 1.25
RAIN_END = max(RAIN.values()) + 1.25       # == 368.0


# --- Plato choreography (b238-264): move list (start beat, duration, waypoints) -------------------
PARK = {14: (240, 410), 15: (330, 410), 18: (1040, 410), 17: (950, 410), 16: (860, 410),
        19: (1150, 350), 10: (330, 300), 12: (1040, 300), 11: (950, 300)}
HOVER = (640.0, 215.0)
PLATO_MOVES = {
    19: [(252.0, 1.0, [SLOT_P0[19], PARK[19]])],
    14: [(252.5, 1.0, [SLOT_P0[14], PARK[14]])], 18: [(252.5, 1.0, [SLOT_P0[18], PARK[18]])],
    15: [(253.0, 1.0, [SLOT_P0[15], PARK[15]])], 17: [(253.0, 1.0, [SLOT_P0[17], PARK[17]])],
    16: [(253.0, 1.0, [SLOT_P0[16], PARK[16]])],
    10: [(254.0, 1.0, [SLOT_P0[10], (550, 300)]), (255.0, 1.0, [(550, 300), PARK[10]])],
    11: [(254.0, 1.0, [SLOT_P0[11], (640, 300)]), (255.5, 1.0, [(640, 300), PARK[11]])],
    12: [(254.0, 1.0, [SLOT_P0[12], (730, 300)]), (255.0, 0.5, [(730, 300), PARK[12]])],
}
for j in (4, 5, 6, 8): PLATO_MOVES[j] = [(252.5, 1.5, [SLOT_P0[j], SLOT_F[j]])]      # the door opens: row 2 ...
for j in (0, 1, 2, 3): PLATO_MOVES[j] = [(253.0, 1.5, [SLOT_P0[j], SLOT_F[j]])]      # ... then row 1
PLATO_MOVES[15] += [(258.5, 0.75, [PARK[15], SLOT_F[15]])]; PLATO_MOVES[16] += [(258.5, 0.75, [PARK[16], SLOT_F[16]])]
PLATO_MOVES[14] += [(259.25, 0.75, [PARK[14], SLOT_F[14]])]; PLATO_MOVES[17] += [(259.25, 0.75, [PARK[17], SLOT_F[17]])]
PLATO_MOVES[10] += [(260.0, 0.75, [PARK[10], SLOT_F[10]])]; PLATO_MOVES[11] += [(260.0, 0.75, [PARK[11], SLOT_F[11]])]
PLATO_MOVES[12] += [(260.75, 0.75, [PARK[12], SLOT_F[12]])]
PLATO_MOVES[18] += [(261.5, 0.6, [PARK[18], (1040, 290)]), (262.1, 0.6, [(1040, 290), SLOT_F[18]])]
PLATO_MOVES[19] += [(262.75, 0.6, [PARK[19], (1150, 290)]), (263.35, 0.65, [(1150, 290), SLOT_F[19]])]
# row-by-row propagation wave (kept from r1): every box gives a small lift when the wave reaches its row
WAVE = {j: 252.0 + 0.5 * abs(SLOT_P0[j][1] - ROWY[3]) / 60 for j in range(N)}


def plato_pos(j, b):
    p = SLOT_P0[j]
    for (b0, dur, (p0, p1)) in PLATO_MOVES.get(j, []):
        if b >= b0 + dur: p = p1
        elif b >= b0: return lerp2(p0, p1, ease((b - b0) / dur))
    return p


def beam_plato(b, bp0):
    if b < 240: return bp0
    if b < 241.2: return lerp2(bp0, (bp0[0], HOVER[1]), ease((b - 240) / 1.2))  # directed: up the left side ...
    if b < 241.7: return lerp2((bp0[0], HOVER[1]), HOVER, ease((b - 241.2) / 0.5))  # ... over the house ...
    if b < 242: return lerp2(HOVER, (640, 302), ein((b - 241.7) / 0.3))           # ... down onto the roof ...
    if b < 243.5: return lerp2((640, 302), HOVER, eout((b - 242) / 1.5))         # ... refused: rebound
    if b < 256.5: return (HOVER[0], HOVER[1] + 5 * math.sin((b - 243.5) * math.pi))
    if b < 258: return lerp2(HOVER, SLOT_F[BEAM], ein((b - 256.5) / 1.5))        # drops into the cleared row
    return SLOT_F[BEAM]


# ------------------------------------------------------------------ state
def state(b):
    """positions (N,2), rotation deg, scale, glow, face alpha per box."""
    P = np.zeros((N, 2)); rotd = np.zeros(N); sc = np.ones(N); gl = np.full(N, 0.6); face = np.ones(N)
    if b < 32:
        P[:] = F_ARR; face[:] = 0.0; gl[:] = 0.9                         # the end form as a constellation
    elif b < 48:
        for j in range(N):
            rs, gs = RISE[j], GATHER[j]
            if b < rs:
                P[j] = F_ARR[j]; face[j] = 0.0; gl[j] = 0.9
            elif b < rs + 1.2:
                u = (b - rs) / 1.2
                P[j] = (F_ARR[j][0], F_ARR[j][1] + (-90 - F_ARR[j][1]) * ein(u)); face[j] = ease(u / 0.3)
            elif b < gs:
                P[j] = (F_ARR[j][0], -200)                                  # off screen, waiting above
            else:
                u = min(1, (b - gs) / 1.4)
                tgt = _R0[j]
                P[j] = (tgt[0], -90 + (tgt[1] + 90) * (1 - (1 - u) ** 2)); rotd[j] = math.degrees(_A0[j]) + 90
        gl[:] = np.where(face > 0, 0.7, gl)
    elif b < 80:
        P, ang = ring(b)
        rotd = np.degrees(ang) + 90
        gl[:] = 0.75
        if b >= 77:                                                          # the song stops: dim, no glow
            face[:] = 0.4; gl[:] = 0.0
    elif b < 160:
        P = field(b)
        sc[:] = bank_scale(b)
        rot = (b - 80) * 22 * np.array([1 if j < 10 else -1 for j in range(N)])
        if b >= 146:                                         # on the locked ring the boxes ride tangent
            rr = np.degrees(relock_ring(b)[1]) + 90
            k2 = ease((b - 146) / 2)
            rot = rot * (1 - k2) + rr * k2
        if b < 84:
            R0, ang80 = ring(80); kk = ease((b - 80) / 4)
            P = R0 * (1 - kk) + P * kk
            rot = (np.degrees(ang80) + 90) * (1 - kk) + rot * kk
        rotd = rot
        gl[:] = 0.8
    elif b < 238:
        Fd = field(b)
        sc[:] = bank_scale(b)
        rot = (b - 80) * 22 * np.array([1 if j < 10 else -1 for j in range(N)])
        if b < 164:
            k3 = ease((b - 160) / 4)
            rot = (np.degrees(relock_ring(b)[1]) + 90) * (1 - k3) + rot * k3
        for k, j in enumerate(MAKE_ORDER):
            lb = land_beat(k)
            if b >= lb:
                P[j] = P0_ARR[j]; rotd[j] = 0; gl[j] = 0.5 + 0.5 * math.exp(-4 * (b - lb))
            elif b >= lb - 2:
                u = (b - (lb - 2)) / 2
                P[j] = flight(field(lb - 2)[j], P0_ARR[j], u, 70, 1 if k % 2 else -1)
                rotd[j] = ((lb - 2 - 80) * 22 * (1 if j < 10 else -1)) % 360 * (1 - ease(u)); gl[j] = 1.0
            else:
                P[j] = Fd[j]; rotd[j] = rot[j]
        P[BEAM] = Fd[BEAM]; rotd[BEAM] = rot[BEAM]
    elif b < 264:
        for j in range(N):
            if j != BEAM: P[j] = plato_pos(j, b)
        bp0 = field(238)[BEAM]
        P[BEAM] = beam_plato(b, bp0)
        if b < 240: rotd[BEAM] = ((238 - 80) * 22) % 360 * (1 - ease((b - 238) / 2))
        elif 242 <= b < 243.5: rotd[BEAM] = 8 * math.sin(b * 40) * (1 - (b - 242) / 1.5)
        if 242 <= b < 243.5:
            for j in (19, 15, 16, 17):              # the roof it hit shudders
                P[j] = (P[j][0] + 6 * math.sin(b * 50 + j), P[j][1])
        for j in range(N):
            if j == BEAM: continue
            u = (b - WAVE[j]) / 1.0
            if 0 < u < 1:
                P[j] = (P[j][0], P[j][1] - 3 * math.sin(math.pi * u)); gl[j] = 0.6 + 0.9 * math.sin(math.pi * u)
    elif b < 324:
        P[:] = F_ARR
        amp = 3.0 if b < 304 else 0.0
        ph = 2 * math.pi * (b - 264) / 8
        for j in range(N):
            P[j] = F_ARR[j] + (amp * math.sin(3 * ph + j), amp * math.sin(2 * ph + j))
        gl[:] = 0.55 + 0.25 * math.exp(-5 * (b % 1))
        if 304 <= b < 324:
            f = 1 - ease((b - 304) / 2) if b < 316 else (0.0 if b < 322 else ease((b - 322) / 2))
            face[:] = f; gl[:] = 0.9
    elif b < 348:
        k = ease((b - 324) / 4)
        Pr, ang = ellipse_ring(b)
        P = F_ARR * (1 - k) + Pr * k
        rotd = (np.degrees(ang) + 90) * k
        gl[:] = 0.85
    elif b < RAIN_END + 1e-9 or b < 400:
        # the field lifts away (b348-354.9) while turning, then the house rains back row by row
        lift = 820 * ease((b - 348) / 6.9)
        Pr, ang = ellipse_ring(348, spin=2 * math.pi * (b - 348) / 16)
        for j in range(N):
            r0 = RAIN[j]
            if b < r0:
                P[j] = (Pr[j][0], Pr[j][1] - lift); rotd[j] = math.degrees(ang[j]) + 90
            else:
                u = min(1, (b - r0) / 1.25)
                P[j] = (SLOT_F[j][0], -90 + (SLOT_F[j][1] + 90) * ein(u))
                gl[j] = 0.6 + 0.4 * math.exp(-5 * max(0, b - r0 - 1.25))
        if b >= 369:
            face[:] = 1 - ease((b - 369) / 3); gl[:] = 0.9                 # back to the constellation
    return P, rotd, sc, gl, face


# ------------------------------------------------------------------ sprites
def box_sprite(j, w=84, h=56, label=None, cool=False, tint=None):
    ss = 3
    W_, H_ = int(w * ss), int(h * ss)
    im = Image.new("RGBA", (W_ + 8, H_ + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    base = (196, 152, 96) if not cool else (166, 160, 150)
    flute = (166, 124, 72) if not cool else (132, 128, 122)
    if tint: base, flute = tint, tuple(int(v * 0.8) for v in tint)
    d.rectangle([4, 4, 4 + W_, 4 + H_], fill=base + (255,))
    for x in range(4, 4 + W_, 4 * ss):
        d.line([(x, 4), (x, 4 + H_)], fill=flute + (130,), width=ss)
    d.rectangle([4, 4, 4 + W_, 4 + H_], outline=(30, 18, 10, 255), width=2 * ss)
    txt = label if label is not None else str(j)
    f = font(FONT_STENCIL, (h * 0.86 if label is None else h * 0.62) * ss)    # r2: numbers fill the face
    bb = d.textbbox((0, 0), txt, font=f)
    d.text((4 + (W_ - (bb[2] - bb[0])) / 2 - bb[0], 4 + (H_ - (bb[3] - bb[1])) / 2 - bb[1]), txt, font=f,
           fill=(255, 255, 255, 255) if tint else (20, 12, 6, 255))
    im = im.resize((im.width // ss, im.height // ss), Image.LANCZOS)
    return Sprite(im, (im.width / 2, im.height / 2), f"box_{j}" + ("_tint" if tint else ""),
                  {"kind": "procedural", "note": f"corrugated box {j} drawn in code", "rights": "original"})


A = None


def assets():
    global A
    if A is None:
        A = {}
        A["box"] = []
        for j in range(N):
            if j == BEAM: A["box"].append(box_sprite(j, 264, 40, "BEAM 7"))
            elif j == MARK_A: A["box"].append(box_sprite(j, tint=RED))
            elif j == MARK_B: A["box"].append(box_sprite(j, tint=(214, 176, 0)))
            else: A["box"].append(box_sprite(j, cool=j >= 10))
        A["beam_fold"] = box_sprite(BEAM, 110, 40, "7")
        A["box_red"] = box_sprite(BEAM, 264, 40, "BEAM 7", tint=(200, 40, 30))

        def plate(name, box):
            im = _src(name).crop(box).resize((1600, 900))
            arr = np.asarray(im, np.float32); k = 90
            cs = np.cumsum(np.pad(arr, ((0, 0), (k, k), (0, 0)), mode="edge"), axis=1)
            arr = ((cs[:, 2 * k:] - cs[:, :-2 * k]) / (2 * k))[:, :1600]
            return Image.fromarray(np.clip(arr * 0.85 + 10, 0, 255).astype(np.uint8)).convert("RGBA")
        A["plate_title"] = plate("Boxback climb under sodium light.png", (0, 300, 1254, 1005))
        LEDGER["plate_title"] = {"kind": "album-art-plate (motion-blurred)", "source": "Et tu, Brute (BOXBACK)/Boxback climb under sodium light.png",
                                 "crop_box_px": [0, 300, 1254, 1005], "rights": "producer's own BOXBACK album artwork (hartswf0/moto)"}
        A["f_title"] = font(FONT_STENCIL, 100)
        A["f_end"] = font(FONT_STENCIL, 46)
        A["f_card"] = font(FONT_MONO, 60)          # r2: 2.3x the old card text, white / red on solid black
        A["f_tag"] = font(FONT_MONO, 40)
        A["f_cap"] = font(FONT_STENCIL, 66)        # r2: section labels ~3x (was 22 px mono, grey)
        A["f_small"] = font(FONT_MONO, 26)
    return A


def spaced(d, xy, text, f, fill, track=0.35, anchor_center=True):
    widths = [d.textbbox((0, 0), ch, font=f)[2] for ch in text]
    tw = sum(widths) + track * f.size * (len(text) - 1)
    x = xy[0] - tw / 2 if anchor_center else xy[0]
    for ch, w in zip(text, widths):
        d.text((x, xy[1]), ch, font=f, fill=fill); x += w + track * f.size
    return tw


def typed(d, xy, text, b, b0, cps=10, f=None, fill=(255, 255, 255, 255), cursor=True):
    n = int(max(0, (b - b0)) * cps)
    s = text[:n]
    d.text(xy, s, font=f, fill=fill)
    if cursor and n < len(text) + 8 and int(b * 2) % 2 == 0:
        x = xy[0] + d.textbbox((0, 0), s, font=f)[2] + 6
        d.rectangle([x, xy[1] + 6, x + 0.5 * f.size, xy[1] + f.size], fill=fill)


# ------------------------------------------------------------------ render
def corners(p, rot, w, h, s=1.0):
    c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [(p[0] + dx * s * c - dy * s * sn, p[1] + dx * s * sn + dy * s * c)
            for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]


def trail_len(b):
    if 52 <= b < 72: return 14
    if 80 <= b < 112: return 10
    if 112 <= b < 160: return int(10 + 26 * min(1, (b - 112) / 16)) if b < 144 else int(36 - 26 * ease((b - 144) / 16))
    if 160 <= b < 238: return 8
    if 328 <= b < 348: return 16
    return 0


def render_frame(f):
    a = assets()
    t = f / FPS
    b = B(t) + 0.5 * FB                       # half-frame snap: beat events land on the nearest frame
    if b < 16:
        return title_frame(b, t)
    im = Image.new("RGBA", (W, H), (6, 7, 10, 255))
    gimg = Image.new("RGB", (W, H), (0, 0, 0)); gd = ImageDraw.Draw(gimg)
    P, rotd, sc, gl, face = state(b)
    L = trail_len(b)
    if L:
        hist = [state(b - k * 0.09)[0] for k in range(L)]
        for j in range(N):
            col = np.array(RED, float) if j == MARK_A else (np.array(YEL, float) if j == MARK_B else (WARM if j < 10 else COOL))
            wdt = 4 if j in (MARK_A, MARK_B) else 2
            for k in range(L - 1):
                al = (1 - k / L) * (0.9 if j in (MARK_A, MARK_B) else 0.55)
                gd.line([tuple(hist[k][j]), tuple(hist[k + 1][j])], fill=tuple(int(v * al) for v in col), width=wdt)
    if 48 <= b < 77:
        for i in range(10):
            gd.line([tuple(P[i]), tuple(P[i + 10])], fill=(90, 90, 90), width=1)
        # the 12 o'clock tick: count the markers past it (A three times, B twice, b52-b72)
        top = (CX, CY - 0.8 * (R_RING + 130))
        gd.line([(top[0], top[1] - 18), (top[0], top[1] + 26)], fill=(255, 255, 255), width=4)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    order = sorted(range(N), key=lambda j: (j == BEAM, j in (MARK_A, MARK_B), j >= 10))
    for j in order:
        if face[j] <= 0.01: continue
        if j == BEAM:
            wd = beam_width(b)
            if wd > 180:
                spr = a["box_red"] if 242 <= b < 256.5 else a["box"][j]; sx = wd / 264
            else:
                spr = a["beam_fold"]; sx = wd / 110
            blit(layer, spr, tuple(P[j]), rotd[j], sx * sc[j], sc[j], face[j])
        else:
            blit(layer, a["box"][j], tuple(P[j]), rotd[j], sc[j], None, face[j])
    im.alpha_composite(layer)
    for j in range(N):
        w, h = box_w(j, b) * sc[j], box_h(j) * sc[j]
        col = np.array(RED, float) if j == MARK_A else (np.array(YEL, float) if j == MARK_B else (WARM if j < 10 else COOL))
        if j == BEAM and 242 <= b < 256.5: col = np.array(RED, float)
        br = gl[j] * (1.0 if face[j] > 0.3 else 1.5)
        if br <= 0: continue
        for (x, y) in corners(P[j], rotd[j], w, h):
            r = 3.2 * br
            gd.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(min(255, v * br)) for v in col))
    for be in EVENTS:
        db = b - be["b"]
        if 0 <= db < 1.2:
            k = math.exp(-4 * db)
            if be["kind"] in ("lock", "unlock", "relock"):          # the star: rays from the centre to every box
                for p in P:
                    gd.line([(CX, CY), tuple(p)], fill=(int(255 * k), int(255 * k), int(255 * k)), width=2)
            for (x, y) in be["where"]:
                r = 16 * k + 4
                gd.ellipse([x - r, y - r, x + r, y + r], outline=(int(255 * k), int(240 * k), int(200 * k)), width=3)
    g = np.asarray(gimg, np.float32)
    g2 = np.asarray(gimg.filter(ImageFilter.GaussianBlur(5)), np.float32)
    base = np.asarray(im.convert("RGB"), np.float32)
    out = np.clip(base + g * 0.9 + g2 * 1.6, 0, 255).astype(np.uint8)
    im = Image.fromarray(out).convert("RGBA")
    d = ImageDraw.Draw(im)
    captions(d, b, a)
    if b >= 370: end_card(im, b, a)
    if t > DUR - 2.5:
        im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), min(1, (t - (DUR - 2.5)) / 2.3))
    return im.convert("RGB")


def captions(d, b, a):
    cap = a["f_cap"]

    def c(text, b0, b1, y=18, col=(255, 255, 255), x=640):
        if b0 <= b < b1:
            al = min(1, (b - b0) / 0.25, (b1 - b) / 0.25)
            spaced(d, (x, y), text, cap, col + (int(255 * al),), track=0.12)
    c("THE END FORM", 16, 31.5)
    c("FROM THE END", 32, 47.5)
    c("3 : 2", 48, 77, y=630, x=1140)
    c("STOP", 77, 80, y=630, x=1140, col=RED)
    c("LOCK", 84, 111.5)
    c("UNLOCK · DRIFT", 112, 143.5)
    c("RE-LOCK", 144, 159.5)
    c("FIRST STEP", 160, 190)
    c("THE ARRANGEMENT IS THE THING", 306, 323.5, y=640)
    if 52 <= b < 77:   # marker legend on the proof
        sm = a["f_small"]
        d.rectangle([24, 640, 52, 668], fill=RED + (255,)); d.text((62, 638), "A x3", font=sm, fill=(255, 255, 255, 255))
        d.rectangle([180, 640, 208, 668], fill=YEL + (255,)); d.text((218, 638), "B x2", font=sm, fill=(255, 255, 255, 255))
    # the architect and the builder (Plato): white / red on solid black, 60 px
    cf, tg = a["f_card"], a["f_tag"]
    arch = None
    for b0, text in ((238, "BEAM 7 -> ROW 3"), (248, "LIFT ROOF. OPEN DOOR."), (255.5, "BEAM 7 -> ROW 3"),
                     (258, "ROOF -> NEW PLAN"), (264, None)):
        if b >= b0: arch = (b0, text)
    if arch and arch[1] and 238 <= b < 264:
        d.rectangle([16, 12, 960, 92], fill=(0, 0, 0, 235))
        d.text((28, 28), "ARCH", font=tg, fill=(120, 255, 170, 255))
        typed(d, (150, 18), arch[1], b, arch[0], cps=14, f=cf, fill=(255, 255, 255, 255), cursor=False)
    bld = None
    for b0, text, col in ((244, "BEAM 7 CANNOT GO THERE", RED), (252, None, None), (258, "BEAM 7 IN ROW 3", (120, 255, 170))):
        if b >= b0: bld = (b0, text, col)
    if bld and bld[1] and b < 264:
        d.rectangle([160, 100, 1264, 180], fill=(0, 0, 0, 235))
        d.text((172, 116), "BLDR", font=tg, fill=bld[2] + (255,))
        typed(d, (294, 106), bld[1], b, bld[0], cps=14, f=cf, fill=bld[2] + (255,), cursor=False)


TITLE_CUTS = [(2, 0), (4, 410), (6, 130), (8, 520), (10, 260), (12, 60), (14, 380)]


def title_frame(b, t):
    a = assets()
    pl = a["plate_title"]
    x0 = 0
    for cb, off in TITLE_CUTS:                  # jump cuts on beats 2, 4 ... 14 (Touki Bouki whip pans)
        if b >= cb: x0 = off
    seg_start = max([cb for cb, _ in TITLE_CUTS if b >= cb], default=0)
    x = int((x0 + (b - seg_start) * 120) % 300)
    im = pl.crop((x, 90, x + W, 90 + H))
    k = ease(min(1, b / 2)) * (1 - ease((b - 14.5) / 1.5))
    im = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), im, k)
    d = ImageDraw.Draw(im)
    if b >= 4: spaced(d, (640, 170), "THE", a["f_title"], RED + (255,), track=0.6)
    if b >= 6: spaced(d, (640, 290), "UNIVERSAL", a["f_title"], RED + (255,), track=0.32)
    if b >= 8: spaced(d, (640, 410), "BOXBACK", a["f_title"], RED + (255,), track=0.5)
    if b >= 10: spaced(d, (640, 590), "ET TU, BRUTE? · BOXBACK · 14 / 18", a["f_small"], (240, 236, 226, 255), track=0.3)
    return im.convert("RGB")


def end_card(im, b, a):
    k = ease((b - 370) / 2)
    if k <= 0: return
    d = ImageDraw.Draw(im)
    spaced(d, (640, 70), "THE UNIVERSAL BOXBACK", a["f_end"], RED + (int(255 * k),), track=0.3)
    spaced(d, (640, 660), "ET TU, BRUTE? · BOXBACK · 14 / 18", a["f_small"], (230, 230, 220, int(255 * k)), track=0.3)


# ------------------------------------------------------------------ events (picture + sound share one list)
def build_events():
    ev = []
    R0, _ = ring(52)
    ev.append({"b": 52.0, "kind": "reunion", "where": [tuple(R0[i]) for i in range(10)]})
    for m in range(1, 10):
        b = 52 + 2 * m
        P, _ = ring(b)
        ev.append({"b": float(b), "kind": "interference", "m": m, "where": [tuple((P[i] + P[(i + m) % 10 + 10]) / 2) for i in range(10)]})
    R1, _ = ring(72)
    ev.append({"b": 72.0, "kind": "reunion", "where": [tuple(R1[i]) for i in range(10)]})
    ev.append({"b": 77.0, "kind": "stop", "where": []})
    ev.append({"b": 96.0, "kind": "lock", "where": []})
    ev.append({"b": 112.0, "kind": "unlock", "where": []})
    ev.append({"b": 148.0, "kind": "relock", "where": []})
    for k, j in enumerate(MAKE_ORDER):
        ev.append({"b": float(land_beat(k)), "kind": "land", "id": j, "where": [SLOT_P0[j]]})
    ev.append({"b": 242.0, "kind": "collision", "where": [(640, 322)]})
    ev.append({"b": 258.0, "kind": "beam_lands", "where": [SLOT_F[BEAM]]})
    for j, mv in PLATO_MOVES.items():
        b0, dur, (p0, p1) = mv[-1]
        if tuple(p1) == tuple(SLOT_F[j]) and b0 >= 258:
            ev.append({"b": b0 + dur, "kind": "reseat", "id": j, "where": [SLOT_F[j]]})
    for j in range(N):
        ev.append({"b": RAIN[j] + 1.25, "kind": "rain", "id": j, "where": [SLOT_F[j]]})
    ev.append({"b": 368.0, "kind": "home", "where": [tuple(p) for p in F_ARR]})
    return ev


EVENTS = build_events()
