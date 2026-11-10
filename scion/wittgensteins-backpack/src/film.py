"""WITTGENSTEIN'S BACKPACK - timeline. Every event is placed on the 128.01 BPM beat grid (beatgrid.json).

Scene map (beats):  b0 title | b16 PROOF: beetle->box-head->door->crowd | b40 beetle-in-a-box lineup |
b72 box stack (BOX KNOX FOX ...) | b104 throw away the ladder | b136 duck-rabbit | b168 fly-bottle |
b195.3 break (drop) -> Sketchpad constraint mode b203 | b240 operator montage | b312 parade | b348 outro.
"""
import json, math, os, pickle, random
from engine import *
from engine import _ac
from cast import *
from constraints import solve_reach, REST

G = json.load(open(os.path.join(os.path.dirname(__file__), "beatgrid.json")))["grid"]
PER, OFF = G["period"], G["offset"]
FPS = 24
DUR = 180.33
FLOOR = 650


def T(b):
    return OFF + b * PER


def B(t):
    return (t - OFF) / PER


SFX = []  # (beat, kind, gain) - declared statically below so audio and picture share one source of truth


def sfx(b, kind, gain=1.0):
    SFX.append((b, kind, gain))


# ---------------------------------------------------------------- assets (lazy per process)
A = None


def assets():
    global A
    if A is None:
        A = {}
        A["near"] = make_dignitary("dig"); A["far"] = make_dignitary("digf", far=True)
        A["fig"] = Figure(A["near"], A["far"])
        A["F"] = make_fragments(); A["BG"] = backgrounds()
        A["beetle"] = make_beetle(); A["beetle_big"] = make_beetle(6.0); A["duckrabbit"] = make_duckrabbit(); A["bottle"] = make_bottle(); A["fly"] = make_fly(); A["fly_big"] = make_fly(24.0)
        A["doorway"] = make_doorway(76, 78, "doorway_boxhead"); A["doorway_big"] = make_doorway(96, 110, "doorway_bottle")
        A["hand_giant"] = make_hand_giant()
        tags = {"title": ("WITTGENSTEIN'S\nBACKPACK", 54, FONT_SERIF), "everyone": ("EVERYONE HAS A BOX.", 34, FONT_SERIF),
                "empty": ("THE BOX MIGHT\nEVEN BE EMPTY.", 40, FONT_SERIF), "ladder": ("THROW AWAY\nTHE LADDER.", 44, FONT_SERIF),
                "duck": ("DUCK", 50, FONT_STENCIL), "rabbit": ("RABBIT", 50, FONT_STENCIL),
                "duck!": ("DUCK!", 30, FONT_STENCIL), "rabbit!": ("RABBIT!", 30, FONT_STENCIL),
                "fly": ("SHOW THE FLY\nTHE WAY OUT.", 38, FONT_SERIF),
                "pack": ("WHEREOF ONE CANNOT SPEAK,\nTHEREOF ONE MUST PACK.", 40, FONT_SERIF),
                "track": ("TRACK 18 / 18", 28, FONT_STENCIL), "gulp": ("GULP.", 60, FONT_STENCIL), "word_beetle": ("BEETLE", 26, FONT_STENCIL)}
        for op in ("DETACH", "INVERT", "ENLARGE", "REPLACE", "HATCH", "SWALLOW", "EMERGE", "ENTER", "INTERRUPT"):
            tags[op] = (op, 46, FONT_STENCIL)
        A["tag"] = {k: text_tag(v[0], "tag_" + k.lower().replace("!", "_x"), v[1], fontpath=v[2], tilt_seed=i)
                    for i, (k, v) in enumerate(tags.items())}
        sp = os.path.join(ROOT, "out", "sketch_poses.pkl")
        A["sketch"] = pickle.load(open(sp, "rb")) if os.path.exists(sp) else None
    return A


# ---------------------------------------------------------------- helpers
def stamp(dst, spr, pos, b, b0, rot=-3, base=1.0, hold_to=None, out=None):
    """Caption/object stamped onto the page on beat b0: overshoot scale then hold."""
    u = b - b0
    if u < 0 or (hold_to is not None and b > hold_to):
        return
    s = base * (1.5 - 0.5 * ease_out(u / 0.25)) if u < 0.25 else base
    a = 1.0
    if out is not None and b > out:
        a = clamp(1 - (b - out) / 0.5)
    blit(dst, spr, pos, rot, s, None, a)


def pop(u):
    if u < 0: return 1.0
    return 1 + 0.22 * math.exp(-7 * u) * math.cos(14 * u)


def arc(p0, p1, h, u):
    u = clamp(u)
    return (lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u) - h * 4 * u * (1 - u))


def jitter(t, amp, seed=0):
    r = random.Random(int(t * FPS) * 31 + seed)
    return r.uniform(-amp, amp)


def mini(fig, dst, x, floor, s, phase, face=1, head=None, backpack=None, walking=True, alpha=1.0):
    Fv = floor + (REST["thigh"] + REST["shin"] + 6) * (1 - s)
    J = walk_pose(x, Fv, phase, face) if walking else stand_pose(x, Fv, face)
    fig.draw(dst, J, scale=s, head_sprite=head, backpack=backpack, alpha=alpha)
    return J


def held(b, keys):
    """step-hold interpolation over [(beat, value)] - values snap (cutout timing), no tween."""
    v = keys[0][1]
    for kb, kv in keys:
        if b >= kb: v = kv
    return v


def tween(b, keys, fn=ease):
    """eased interpolation over [(beat, value)] (scalars or tuples)."""
    if b <= keys[0][0]: return keys[0][1]
    for (b0, v0), (b1, v1) in zip(keys, keys[1:]):
        if b0 <= b <= b1:
            u = fn((b - b0) / max(1e-9, b1 - b0))
            if isinstance(v0, tuple): return tuple(lerp(a, c, u) for a, c in zip(v0, v1))
            return lerp(v0, v1, u)
    return keys[-1][1]


# ---------------------------------------------------------------- scenes
def sc_title(fr, b, t):
    a = assets(); F = a["F"]; fig = a["fig"]
    lift = ease(clamp((b - 14) / 1.6)) * -520
    if b >= 2:
        y = tween(b, [(2, -80), (3, 120)], ease_out)
        blit(fr.over, F["coolradio"], (640, y + lift), -2)
    if b >= 4:
        u = b - 4
        y = 250 if u > 0.5 else lerp(-200, 250, (u / 0.5) ** 2)
        blit(fr.over, F["logo"], (640, y + lift), 3 * math.sin(b * 0.7) * (u > 0.5), 0.9 * (pop(u - 0.5) if u > 0.5 else 1))
    stamp(fr.over, a["tag"]["title"], (640, 420 + lift), b, 8, rot=-2)
    if b >= 10:
        y = tween(b, [(10, 860), (11, FLOOR + 10)], back_out)
        flip = -1 if int(b - 12) % 2 == 0 and b >= 12 else 1
        blit(fr.fg, F["frog_dj"], (1060, y), 0, 0.85 * flip, 0.85)
    if b >= 12:
        x = tween(b, [(12, -120), (16, 540)], lambda u: u)
        J = walk_pose(x, FLOOR, (b - 12) * math.pi, 1) if b < 16 else stand_pose(540, FLOOR)
        fig.draw(fr.fg, J, backpack=F["backpack"])


def sc_proof(fr, b, t):
    """HARD PROOF: dignitary notices a beetle; his head is replaced by the beetle's box; the box face becomes a
    door; a crowd walks out of his collar."""
    a = assets(); F = a["F"]; fig = a["fig"]
    shock = 25 <= b < 30
    head_rot = held(b, [(16, 0), (20, 24), (23, 30)]) if b < 24 else (lerp(30, -28, ease(b - 24)) if b < 25 else 0)
    if b < 25: sh, el = (6, -4), (10, 10)
    elif b < 26.5: sh, el = (6, 165), (10, -20)
    else:
        k = ease((b - 26.5) / 0.75); sh, el = (6, lerp(165, -4, k)), (10, lerp(-20, 10, k))
    crouch = 0.0
    J = stand_pose(540, FLOOR, 1, lean=held(b, [(16, 0), (20, 6)]), sh=sh, el=el, head=head_rot, crouch=crouch)
    if shock:
        for k in list(J):
            if isinstance(J[k], tuple) and k != "pelvis":
                pass
    # beetle
    box_pos = (800, FLOOR - 4)
    if b < 22:
        bx = tween(b, [(16, 1240), (20, 900), (21.2, 840), (22, 800)], lambda u: u)
        bs = 1.6 if b < 21.2 else lerp(1.6, 0.5, (b - 21.2) / 0.8)
        by = FLOOR - 18 if b < 21.2 else lerp(FLOOR - 18, FLOOR - 50, (b - 21.2) / 0.8)
        blit(fr.fg, a["beetle"], (bx, by), jitter(t, 6, 1) if b < 21.2 else -60, -bs, bs)
    # small box on floor, swallows beetle, rattles, leaps onto head
    head_spr = None; draw_head = True
    SMALL = 0.34
    if b < 24:
        sq = pop(b - 22) if b >= 22 else 1
        r = jitter(t, 16, 2) if 23 <= b < 24 else 0
        hop = abs(math.sin((b - 23) * math.pi * 6)) * 14 if 23 <= b < 24 else 0
        blit(fr.fg, F["boxhead"], (box_pos[0], box_pos[1] - hop), r, SMALL * (2 - sq), SMALL * sq)
    if b >= 25:
        head_spr = F["boxhead"]
    fig.draw(fr.fg, J, head_sprite=head_spr, head_scale=pop(b - 25) if b >= 25 else 1.0, backpack=F["backpack"],
             head_offset=(0, 6) if head_spr else (0, 0), draw_head=not (24.62 <= b < 25))
    if 24 <= b < 25:
        # the same box-head asset flies IN FRONT of the head and grows to head size on the arc
        u = b - 24
        p = arc(box_pos, add(J["neck"], (0, 6)), 260, ease_out(u) if u < 1 else 1)
        blit(fr.fg, F["boxhead"], p, 360 * (1 - ease_out(u)), lerp(SMALL, 1.0, ease(u)))
    if b >= 27.3:
        # door in the box-head (hinge on its left edge)
        hinge = add(J["neck"], (-48, -150))
        blit(fr.fg, a["doorway"], hinge, 0, 1.3, 1.45)
        sw = tween(b, [(28, 1.0), (29.2, -0.55)], ease_out)
        blit(fr.fg, F["door_panel"], hinge, 0, 1.3 * sw, 1.45) if abs(sw) > 0.02 else None
        door_c = add(hinge, (50, 104))
        # the crowd walks out of his collar
        kinds = ["mini", "frog", "mini_box", "mini", "frog", "mini", "mini_box", "frog", "mini", "beetle"]
        for i, kind in enumerate(kinds):
            b0 = 30 + i * 0.85
            u = b - b0
            if u < 0: continue
            if u < 0.5:
                # walking out of the doorway: sized to fit inside the opening (door is 113 px tall)
                s = 0.36
                p = lerp2(add(door_c, (-6, 0)), add(door_c, (62, 0)), u / 0.5)
                ground = False
            elif u < 1.3:
                k = (u - 0.5) / 0.8
                s = lerp(0.36, 1.0, ease(k)); p = arc(add(door_c, (62, 0)), (700 + i * 4, FLOOR), 40, k); ground = False
            else:
                s = 1; p = (700 + i * 4 + (u - 1.3) * 80, FLOOR); ground = True
            if p[0] > 1400: continue
            if kind == "beetle":
                blit(fr.fg, a["beetle"], (p[0], p[1] - 14 * s), jitter(t, 5, 9) if ground else 30 * u, 1.3 * s)
            elif kind == "frog":
                hop = abs(math.sin((u - 1.3) * math.pi * 2)) * 18 if ground else 0
                blit(fr.fg, F["frog_boxed"], (p[0], p[1] - hop), 0, (0.42 if s < 0.4 else 0.95) * max(s, 0.4) if False else 0.95 * s)
            else:
                sc = 0.34 * s
                mini(fig, fr.fg, p[0], p[1], sc, (u - 1.3) * math.pi * 2 if ground else 0.5, 1,
                     head=F["boxhead"] if kind == "mini_box" else None, backpack=F["backpack"], walking=ground)
    if 25 <= b < 25.6:
        c = add(J["neck"], (0, -100)); k = 1 - (b - 25) / 0.6
        pts = [add(c, rot((0, -(150 if i % 2 == 0 else 80) * (1.2 - 0.4 * k)), i * 360 / 16)) for i in range(16)]
        burst = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(burst).polygon(pts, fill=(255, 246, 200, int(235 * k)), outline=INK + (int(255 * k),))
        fr.layers.insert(0, burst)


def sc_lineup(fr, b, t):
    a = assets(); F = a["F"]; fig = a["fig"]
    stamp(fr.over, a["tag"]["everyone"], (640, 80), b, 40, rot=-2, out=63)
    xs = [180, 410, 640, 870, 1100]
    contents = ["beetle", "word", "frog", "box", "empty"]
    for i, x in enumerate(xs):
        b0 = 44 + 4 * i
        look_empty = 64 <= b < 68 and i < 4
        head = held(b, [(40, 0), (b0, 28), (b0 + 3, 0)])
        if look_empty: head = -12
        J = stand_pose(x, FLOOR, 1, sh=(72, 64), el=(-48, -40), head=head)
        s = 0.62
        # draw with scale about pelvis, feet on floor
        Fv = FLOOR + (REST["thigh"] + REST["shin"] + 6) * (1 - s)
        J = stand_pose(x, Fv, 1, sh=(72, 64), el=(-48, -40), head=head)
        P0 = J["pelvis"]; S = lambda p: add(P0, mul(sub(p, P0), s))
        boxp = add(S(J["hand_n"]), (14, -14))
        shake = jitter(t, 5, i) if b0 - 0.5 <= b < b0 else 0
        if i == 4 and 60 <= b < 63:
            brot = tween(b, [(60, 0), (61, 180), (62.5, 180), (63, 0)])
        else:
            brot = shake
        fig.draw(fr.fg, J, scale=s, backpack=None)
        # content rises out of the box at b0, slams back at b68
        if b >= b0 and b < 68 and contents[i] != "empty":
            u = clamp((b - b0) / 0.5)
            cp = add(boxp, (0, -30 - 50 * back_out(u)))
            if contents[i] == "beetle": blit(fr.fg, a["beetle"], cp, -90, 0.9)
            elif contents[i] == "word": blit(fr.fg, a["tag"]["word_beetle"], cp, -6, 1.0)
            elif contents[i] == "frog": blit(fr.fg, F["frog_boxed"], add(cp, (0, 34)), 0, 0.45)
            elif contents[i] == "box": blit(fr.fg, F["smallbox"], add(cp, (0, 26)), 4, 0.7)
        blit(fr.fg, F["backpack"], boxp, brot, 0.62)
    stamp(fr.over, a["tag"]["empty"], (640, 200), b, 64, rot=2)


def sc_stack(fr, b, t, climb=False):
    a = assets(); F = a["F"]; fig = a["fig"]
    s = 0.62
    x0 = 330
    labels = F["labels"]
    n_on = 0 if b < 72 else min(9, int((b - 72) / 2) + 1)
    crouch = min(0.5, 0.06 * n_on) if b < 98 else max(0, 0.5 - (b - 98) * 0.25)
    Fv = FLOOR + (REST["thigh"] + REST["shin"] + 6) * (1 - s)
    # staircase targets (ascending to the right)
    step_w, rise = 74, 34
    steps = [(560 + i * step_w, FLOOR - i * rise) for i in range(9)]
    if not climb:
        sh = (6, -4)
        J = stand_pose(x0, Fv, 1, sh=sh, el=(10, 10), head=held(b, [(72, 0), (96, -20), (99, 18)]), crouch=crouch)
        P0 = J["pelvis"]; S = lambda p: add(P0, mul(sub(p, P0), s))
        base = add(S(J["back"]), (0, -38))
        wob = 0
        if 88 <= b < 96:
            wob = (b - 88) / 8 * 9 * math.sin((b - 88) * math.pi)
        fig.draw(fr.fg, J, scale=s, backpack=F["backpack"])
        y = base[1]
        for k in range(9):
            lb = labels[k]; sc = 0.5
            hgt = lb.size[1] * sc
            pos_stack = rot((0, y - base[1]), wob)
            pos_stack = add(base, pos_stack)
            if b < 72 + 2 * k:
                break
            u = b - (72 + 2 * k)
            if u < 0.5:
                p = (pos_stack[0], lerp(-80, pos_stack[1], (u / 0.5) ** 2))
            else:
                p = pos_stack
            if b >= 96:
                uu = clamp((b - 96 - k * 0.12) / 1.4)
                p = arc(pos_stack, steps[k], 120, ease(uu))
                r = lerp(wob, 0, uu) + 360 * (1 - uu) * (k % 2 * 2 - 1) * (uu < 1)
            else:
                r = wob
            blit(fr.fg, lb, p, r, sc)
            y -= hgt - 4
        if b >= 100:
            stamp(fr.over, F["boxscore"], (1080, 150), b, 100, rot=6, base=1.0)
    else:
        # S4 climb: walk to stairs, step up 1 step per 1.5 beats, kick the ladder away, hang, fall
        kicked = b >= 124
        for k in range(9):
            p = steps[k]
            if kicked:
                u = b - 124 - k * 0.05
                if u > 0:
                    vx = (k - 4) * 60; p = (p[0] + vx * u, p[1] + 260 * u * u - 80 * u)
                    r = (k % 3 - 1) * 140 * u
                else:
                    r = 0
            else:
                r = 0
            blit(fr.fg, labels[k], p, r, 0.5)
        if b < 108:
            x = tween(b, [(104, 330), (108, 520)], lambda u: u); y = FLOOR
            J = walk_pose(x, Fv, (b - 104) * math.pi, 1)
        elif b < 121.5:
            u = (b - 108) / 1.5; k = min(8, int(u)); fu = u - int(u)
            x0s, y0s = steps[k][0] - 10, steps[k][1] - 30 if k > 0 else FLOOR
            if k == 0: y0s = FLOOR
            prev = steps[k - 1] if k > 0 else (520, FLOOR)
            px = lerp(prev[0], steps[k][0], ease(min(1, fu * 1.6)))
            top = lambda i: steps[i][1] - 30
            py = lerp((FLOOR if k == 0 else top(k - 1)), top(k), ease(min(1, fu * 1.6)))
            J = walk_pose(px, py + (Fv - FLOOR), fu * math.pi * 2, 1)
        else:
            topx, topy = steps[8][0], steps[8][1] - 30
            face = -1 if b >= 122.5 else 1
            if b < 131:
                kick = 55 if 124 <= b < 125 else 0
                hd = 34 if b >= 128 else 0
                if 130 <= b < 131:
                    J = walk_pose(topx, topy + (Fv - FLOOR), (b - 130) * 4 * math.pi, face)
                else:
                    J = stand_pose(topx, topy + (Fv - FLOOR), face, sh=(20, -10), head=hd)
                    if kick:
                        J = Figure.fk(J["pelvis"], face, -8, (kick, -4), (0, 0), (40, -20), (10, 10), 0)
            else:
                dy = 900 * (b - 131) ** 2
                J = stand_pose(topx, topy + (Fv - FLOOR) + dy, face, sh=(170, 160), head=-20)
        fig.draw(fr.fg, J, scale=s, backpack=F["backpack"])
        stamp(fr.over, a["tag"]["ladder"], (360, 140), b, 124, rot=-3)
        if b >= 132:
            fr.shake = 10 * math.exp(-8 * (b - 132))


def sc_duck(fr, b, t):
    a = assets(); F = a["F"]; fig = a["fig"]
    s = 1.5
    J = stand_pose(640, FLOOR + 190, 1, sh=(10, -6), el=(30, 20))
    P0 = J["pelvis"]; S = lambda p: add(P0, mul(sub(p, P0), s))
    q = int((b - 136) / 4)
    if b >= 160: q = int((b - 160)) + 6
    ang = 90 * (q % 2)
    if b >= 166: ang = 45
    u = (b - 136) % 4 if b < 160 else (b - 160) % 1
    head_ang = ang - 90 * (1 - ease_out(u / 0.25)) * (u < 0.25) * (1 if q % 2 else -1) if b < 166 else 45
    fig.draw(fr.fg, J, scale=s, head_sprite=a["duckrabbit"], head_scale=1.25 * pop(u), extra_head_rot=head_ang,
             backpack=F["backpack"])
    word = a["tag"]["rabbit" if (ang == 90) else "duck"]
    if b < 166:
        stamp(fr.over, word, (1010, 560), b, 136 + 4 * ((b - 136) // 4) if b < 160 else 160 + (b - 160) // 1, rot=-2)
    # two arguers
    for side, x in ((0, 170), (1, 1110)):
        if side == 0 and 156 <= b:
            uu = clamp((b - 156) / 1.0)
            mouth = S(add(J["neck"], (-90, -80)))
            if uu < 1:
                p = arc((x, FLOOR), mouth, 160, uu)
                mini(fig, fr.fg, p[0], p[1], 0.45 * (1 - uu * 0.9), 0, 1, backpack=F["backpack"], walking=False)
            continue
        jump = max(0, math.sin((b - side) * math.pi)) * 40 if int(b) % 2 == side else 0
        mini(fig, fr.fg, x, FLOOR - jump, 0.45, 0, 1 if side == 0 else -1, backpack=F["backpack"], walking=False)
        if b < 156 or side == 1:
            if int(b) % 2 == side:
                blit(fr.over, a["tag"]["duck!" if side == 0 else "rabbit!"], (x + (60 if side == 0 else -60), 300 - jump), -4 + side * 8, 1.2)


def fly_pos(b):
    # deterministic buzzing inside the bottle body (ellipse), out through the door at b188+
    cx, cy, rx, ry = 640, 560, 80, 92
    ph = b * 2.3
    p = (cx + rx * 0.85 * math.sin(ph * 1.7 + math.sin(ph * 0.9)), cy + ry * 0.8 * math.sin(ph * 2.3 + 1.1) * math.cos(ph * 0.6))
    return p


def sc_bottle(fr, b, t):
    a = assets(); F = a["F"]; fig = a["fig"]
    blit(fr.fg, a["bottle"], (640, 700), 0, 1.5)
    door_hinge = (705, 540)
    if 184 <= b < 184.95:
        blit(fr.fg, F["backpack"], (door_hinge[0] + 50, door_hinge[1] + 54), 0, 0.9)
    door_hinge = (705, 540)
    if b >= 184.95:
        blit(fr.fg, a["doorway_big"], door_hinge, 0, 0.9)
        sw = tween(b, [(186, 1.0), (187, -0.2)], ease_out) if b >= 186 else 1.0
        blit(fr.fg, F["door_panel"], door_hinge, 0, 1.13 * sw, 1.27) if abs(sw) > 0.02 else None
    # dignitary
    if b >= 172:
        if b < 176:
            J = walk_pose(tween(b, [(172, -100), (176, 330)], lambda u: u), FLOOR, (b - 172) * math.pi, 1)
            fig.draw(fr.fg, J, backpack=F["backpack"])
        else:
            arms = held(b, [(176, (6, -4)), (180, (80, 70)), (184, (90, 80)), (185, (6, -4))])
            J = stand_pose(330, FLOOR, 1, sh=arms, el=(-30, -30) if arms[0] > 50 else (10, 10), head=held(b, [(176, 8), (188, -6)]))
            carry = 180 <= b < 184.95
            fig.draw(fr.fg, J, backpack=F["backpack"] if b < 180 else None)
            if carry:
                p = tween(b, [(180, J["back"]), (182, add(J["hand_n"], (30, -10))), (183.2, add(J["hand_n"], (30, -10))),
                              (184, (door_hinge[0] + 50, door_hinge[1] + 54))])
                blit(fr.fg, F["backpack"], p, 0, tween(b, [(183.2, 1.0), (184, 0.9)]))
            elif b >= 185:
                blit(fr.fg, F["backpack"], (760, FLOOR - 50), 0, 1.0) if False else None
    # fly
    if b < 188:
        p = fly_pos(b)
        blit(fr.over, a["fly"], p, jitter(t, 30, 4), 2.8)
    else:
        u = b - 188
        if u < 2:
            p = lerp2(fly_pos(188), (door_hinge[0] + 40, door_hinge[1] + 50), ease(u / 2))
            blit(fr.over, a["fly"], p, jitter(t, 30, 4), 2.8)
        else:
            k = clamp((b - 190) / (195.3 - 190))
            sc = 2.8 * (1 + 40 * k ** 3)
            p = lerp2((door_hinge[0] + 40, door_hinge[1] + 50), (640, 380), ease(k))
            if sc < 8: blit(fr.over, a["fly"], p, jitter(t, 10, 4) * (1 - k), sc)
            else: blit(fr.over, a["fly_big"], p, jitter(t, 10, 4) * (1 - k), sc / 24.0)
    stamp(fr.over, a["tag"]["fly"], (1050, 110), b, 176, rot=3, out=190)


# ---------------------------------------------------------------- Sketchpad (constraint mode)
SK_PEL = (520.0, 466.0); SK_PN = (540.0, 644.0); SK_PF = (492.0, 644.0)
SK_HINGE = (600.0, 300.0); SK_DOOR_W = 120.0; SK_DOOR_H = 220.0  # hinge on the NEAR (left) edge: pulling brings the handle toward him


def sk_handle(open_amt):
    # door seen face-on, hinge on the left edge; opening foreshortens the panel toward the hinge
    return (SK_HINGE[0] + SK_DOOR_W * math.cos(math.radians(70 * open_amt)) - 14, SK_HINGE[1] + 120)


def sk_cursor(b):
    keys = [(203, (1000.0, 160.0)), (204.5, None), (206, "grab"), (210, (600.0, 300.0)), (214, (900.0, 150.0)),
            (218, "handle"), (228, "pull"), (240, "pull")]
    return keys


def sketch_target(b, rest_hand):
    """Light-pen path (beats -> design px). Returns (cursor, attached, door_open)."""
    H0 = sk_handle(0)
    if b < 204.5:
        return lerp2((1000.0, 160.0), rest_hand, ease((b - 203) / 1.5)), False, 0.0
    if b < 206:
        return rest_hand, False, 0.0
    if b < 210:
        return lerp2(rest_hand, (610.0, 300.0), ease((b - 206) / 4)), False, 0.0
    if b < 214:
        return lerp2((610.0, 300.0), (930.0, 140.0), ease((b - 210) / 4)), False, 0.0
    if b < 218:
        return lerp2((930.0, 140.0), H0, ease((b - 214) / 4)), False, 0.0
    if b < 220:
        return H0, True, 0.0
    o = ease(clamp((b - 220) / 8))
    return sk_handle(o), True, o


def precompute_sketch():
    poses = {}
    prev = None
    f0, f1 = int(T(203) * FPS), int(T(240.5) * FPS) + 1
    base = solve_reach(SK_PEL, SK_PN, SK_PF, (560.0, 450.0), max_lean=22.0)
    rest_hand = base["hand"]
    trace = []
    for f in range(f0, f1):
        b = B(f / FPS)
        cur, att, o = sketch_target(b, rest_hand)
        tgt = cur if b >= 206 else rest_hand
        bb = solve_reach(SK_PEL, SK_PN, SK_PF, tgt, prev=prev, max_lean=22.0)
        prev = bb
        poses[f] = dict(body=bb, cursor=cur, attached=att, door_open=o, grabbed=b >= 206)
        r = bb["residuals"]
        trace.append({"frame": f, "beat": round(b, 3), "target": [round(tgt[0], 2), round(tgt[1], 2)],
                      "solvable": bb["solvable"], "attach_px": round(r["attach"], 4), "pin_n_px": round(r["pin_n"], 6),
                      "pin_f_px": round(r["pin_f"], 6), "length_err_max_px": round(r["length_max"], 9),
                      "pelvis": [round(v, 2) for v in bb["pelvis"]], "lean_deg": round(bb["lean"], 2), "elbow_branch": bb["elbow_bend"]})
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    pickle.dump(poses, open(os.path.join(ROOT, "out", "sketch_poses.pkl"), "wb"))
    json.dump({"rest_pelvis": SK_PEL, "plant_n": SK_PN, "plant_f": SK_PF, "rest_lengths": REST, "frames": trace},
              open(os.path.join(ROOT, "out", "solver-trace.json"), "w"))
    return poses


GREEN = (90, 255, 140)


def sc_sketchpad(fr, b, t, f):
    a = assets()
    fr.bg = Image.new("RGBA", (W, H), (3, 20, 10, 255))
    d = ImageDraw.Draw(fr.over)
    mono = font(FONT_MONO, 40); small = font(FONT_MONO, 30)
    if b < 203:
        lines = ["SKETCHPAD // CONSTRAINT MODE", "", "PIN     ankle_n = plant_n", "PIN     ankle_f = plant_f",
                 "LENGTH  thigh shin torso upper fore", "ATTACH  hand -> handle   (held-by)"]
        k = (b - 195.6) / 7.0
        nchar = int(clamp(k) * sum(len(s) + 4 for s in lines))
        y = 150
        for s in lines:
            show = s[:max(0, nchar)]; nchar -= len(s) + 4
            d.text((90, y), show, font=mono, fill=GREEN + (255,)); y += 62
        if int(b * 2) % 2 == 0: d.rectangle([90, y, 114, y + 40], fill=GREEN + (255,))
        _scanlines(fr)
        return
    P = a["sketch"].get(f) if a["sketch"] else None
    if P is None:
        return
    bb = P["body"]; r = bb["residuals"]
    g = GREEN + (255,); dim = (40, 140, 80, 255); red = (255, 90, 80, 255)
    # door (constraint: hinge fixed, handle on the door edge)
    o = P["door_open"]
    wv = SK_DOOR_W * math.cos(math.radians(70 * o))
    d.rectangle([SK_HINGE[0], SK_HINGE[1], SK_HINGE[0] + wv, SK_HINGE[1] + SK_DOOR_H], outline=g, width=2)
    d.rectangle([SK_HINGE[0] - 4, SK_HINGE[1], SK_HINGE[0], SK_HINGE[1] + SK_DOOR_H], fill=dim)
    hx, hy = sk_handle(o)
    d.ellipse([hx - 7, hy - 7, hx + 7, hy + 7], outline=g, width=2)
    # floor + pins
    d.line([(300, 644), (980, 644)], fill=dim, width=1)
    for p in (SK_PN, SK_PF):
        d.polygon([(p[0], p[1]), (p[0] - 9, p[1] + 14), (p[0] + 9, p[1] + 14)], outline=g)
        for k in range(3): d.line([(p[0] - 10 + k * 8, p[1] + 20), (p[0] - 4 + k * 8, p[1] + 14)], fill=dim)
    # skeleton
    segs = [("pelvis", "neck"), ("shoulder", "elbow"), ("elbow", "hand"), ("hip", "knee_n"), ("knee_n", "ankle_n"),
            ("hip", "knee_f"), ("knee_f", "ankle_f")]
    pulse = 1 + 2.5 * math.exp(-8 * (b % 1))
    for s0, s1 in segs:
        d.line([bb[s0], bb[s1]], fill=g, width=int(3 * pulse))
    for k in ("pelvis", "neck", "shoulder", "elbow", "hand", "knee_n", "knee_f", "ankle_n", "ankle_f"):
        x, y = bb[k]; d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(3, 20, 10, 255), outline=g, width=2)
    nx, ny = bb["neck"]; d.ellipse([nx - 26, ny - 56, nx + 26, ny - 4], outline=g, width=3)
    # light pen + residual
    cx, cy = P["cursor"]
    col = g if bb["solvable"] else red
    if P["grabbed"]:
        d.line([bb["hand"], (cx, cy)], fill=col, width=1)
    d.line([(cx - 16, cy), (cx + 16, cy)], fill=(220, 255, 230, 255), width=2)
    d.line([(cx, cy - 16), (cx, cy + 16)], fill=(220, 255, 230, 255), width=2)
    if P["attached"]:
        d.text((hx + 18, hy - 44), "held-by", font=small, fill=g)
    # residual dashboard (live numbers from the solver for this exact frame)
    rows = [f"|hand-target| {r['attach']:7.2f} px", f"|feet-pins|   {max(r['pin_n'], r['pin_f']):7.2f} px",
            f"|len-rest|    {r['length_max']:7.2f} px"]
    y = 30
    for s in rows:
        d.text((40, y), s, font=small, fill=g); y += 40
    status = "SOLVED" if bb["solvable"] else "UNSOLVABLE - nothing stretched"
    d.text((40, y + 8), status, font=mono, fill=col)
    _scanlines(fr)


def _scanlines(fr):
    if not hasattr(_scanlines, "img"):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        for y in range(0, H, 3): dd.line([(0, y), (W, y)], fill=(0, 0, 0, 70))
        _scanlines.img = im
    fr.over.alpha_composite(_scanlines.img)


def sc_flood(fr, b, t, f):
    """b236-240: the green constraint skeleton is re-dressed in paper: same solved pose, engraved parts."""
    a = assets(); F = a["F"]; fig = a["fig"]
    P = a["sketch"].get(f) if a["sketch"] else None
    if P is None: return
    J = Figure.from_solver(P["body"], 1)
    o = P["door_open"]
    wv = SK_DOOR_W * math.cos(math.radians(70 * o))
    door = Image.new("RGBA", (int(max(4, wv)), int(SK_DOOR_H)), KRAFT + (255,))
    ImageDraw.Draw(door).rectangle([0, 0, door.width - 1, door.height - 1], outline=INK + (255,), width=3)
    _ac(fr.fg, a["doorway_big"].img.resize((int(SK_DOOR_W), int(SK_DOOR_H))), SK_HINGE[0], SK_HINGE[1])
    _ac(fr.fg, door, SK_HINGE[0], SK_HINGE[1])
    fig.draw(fr.fg, J, backpack=F["backpack"])


# ---------------------------------------------------------------- operator montage
OPS = ["DETACH", "INVERT", "ENLARGE", "REPLACE", "HATCH", "SWALLOW", "EMERGE", "ENTER", "INTERRUPT"]


def sc_ops(fr, b, t):
    a = assets(); F = a["F"]; fig = a["fig"]
    i = int((b - 240) // 8); u = b - 240 - 8 * i
    op = OPS[i]
    bgk = {"HATCH": "mountain", "SWALLOW": "pallets", "EMERGE": "pallets", "ENTER": "truck"}.get(op, "stage")
    fr.bg = a["BG"][bgk + "_soft" if bgk != "stage" else bgk].copy()
    stamp(fr.over, a["tag"][op], (200, 112), u, 0, rot=-4)
    if op == "DETACH":
        J = stand_pose(560, FLOOR, 1, sh=(20, -4), head=held(u, [(0, 0), (3, 26), (6, 0)]))
        fig.draw(fr.fg, J, backpack=F["backpack"], hide=("near_arm",) if u >= 2 else ())
        if u < 2:
            pass
        else:
            k = u - 2
            sh = J["shoulder"]
            base = lerp2(sh, (sh[0] + 40 + k * 70, FLOOR - 20), ease(min(1, k)))
            wav = math.sin(k * math.pi * 2) * 30
            e = add(base, down_vec(-60 - wav, REST["upper"] * 0.9)); hnd = add(e, down_vec(-90 + wav, REST["fore"]))
            n = a["near"]
            blit(fr.fg, n["upper"], base, seg_angle(base, e)); blit(fr.fg, n["fore"], e, seg_angle(e, hnd))
            blit(fr.fg, n["hand"], hnd, seg_angle(e, hnd))
    elif op == "INVERT":
        J = stand_pose(640, FLOOR, 1, sh=(30, -20))
        ang = 0 if u < 2 else 180
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fig.draw(layer, J, backpack=F["backpack"])
        if ang:
            layer = layer.rotate(180, center=(640, 420))
            layer = layer.transform(layer.size, Image.AFFINE, (1, 0, 0, 0, 1, -(math.sin(u * math.pi) * 12)))
        fr.fg.alpha_composite(layer)
    elif op == "ENLARGE":
        sc = 1.0 + 15 * ease(clamp((u - 1) / 6)) ** 2
        if sc < 3:
            blit(fr.fg, a["beetle"], (860, FLOOR - 20 - 12 * sc), 0, sc)
        else:
            blit(fr.fg, a["beetle_big"], (860, FLOOR - 20 - 12 * sc), -90 if sc > 4 else 0, sc / 6.0)
        fr.new_layer()
        jump = 60 * max(0, math.sin((u - 6) * math.pi)) if u >= 6 else 0
        J = stand_pose(300, FLOOR, 1, head=-30 if u >= 6 else 0, sh=(160, 150) if u >= 6 else (6, -4))
        fig.draw(fr.fg, J if not jump else stand_pose(300, FLOOR - jump, 1, head=-30, sh=(160, 150)), scale=0.55 if False else 1.0,
                 backpack=F["backpack"])
    elif op == "REPLACE":
        heads = [None, F["boxhead"], F["frog_dj"], a["duckrabbit"], a["beetle"], F["smallbox"], F["frog_boxed"], None]
        k = int(u) % 8
        hs = heads[k]
        scl = {None: 1, }.get(hs, 1)
        if hs is F["frog_dj"]: scl = 0.6
        if hs is a["beetle"]: scl = 1.6
        if hs is F["smallbox"]: scl = 1.4
        if hs is F["frog_boxed"]: scl = 0.8
        if hs is a["duckrabbit"]: scl = 1.0
        J = stand_pose(640, FLOOR, 1)
        fig.draw(fr.fg, J, head_sprite=hs, head_scale=scl * pop(u - int(u)), backpack=F["backpack"],
                 head_offset=(0, 6) if hs is F["boxhead"] else ((0, -30) if hs is a["beetle"] else (0, 0)),
                 extra_head_rot=-90 if hs is a["beetle"] else 0)
    elif op == "HATCH":
        shake = jitter(t, 6 * clamp(u / 4), 3) if u < 4 else 0
        if u < 4:
            blit(fr.fg, F["backpack"], (640, 500), shake, 3.4)
            if u > 2:
                d = ImageDraw.Draw(fr.fg)
                d.line([(540, 330), (600, 420), (570, 500), (650, 600), (620, 680)], fill=INK + (255,), width=7)
        else:
            k = u - 4
            blit(fr.fg, F["backpack"], (640 - 260 * ease_out(k), 500 + 300 * k * k), -60 * k, 3.4)
            blit(fr.fg, F["frog_dj"], (640, tween(u, [(4, 860), (4.6, 690)], back_out)), 0, 2.6 * pop(k - 0.6))
    elif op == "SWALLOW":
        gulp = 1 + (0.12 * math.sin((u - 5) * math.pi * 3) * math.exp(-2 * (u - 5)) if u >= 5 else 0)
        frog_c = (940, 690)
        if u < 5:
            if u < 4:
                J = walk_pose(tween(u, [(0, 80), (4, 640)], lambda v: v), FLOOR, u * math.pi, 1)
                fig.draw(fr.fg, J, backpack=F["backpack"])
            else:
                k = u - 4
                p = lerp2((640, FLOOR), (860, 470), ease(k))
                mini(fig, fr.fg, p[0], p[1], 1 - 0.95 * ease(k), 0.4, 1, backpack=F["backpack"], walking=False)
        blit(fr.fg, F["frog_boxed"], frog_c, 0, 3.4 * (2 - gulp), 3.4 * gulp)
        if u >= 5: stamp(fr.over, a["tag"]["gulp"], (760, 250), u, 5, rot=8, base=1.4)
    elif op == "EMERGE":
        cc = (640, 450)
        blit(fr.fg, F["cassette"], cc, 0, 3.2)
        fr.new_layer()
        for j in range(12):
            u0 = j * 0.5
            k = u - u0
            if k < 0: continue
            ang = (j * 47) % 360
            p = add(cc, (math.cos(math.radians(ang)) * 380 * ease_out(k / 2), FLOOR - cc[1] + 0 if k > 2 else math.sin(math.radians(ang)) * 160 * ease_out(k / 2)))
            if k > 2: p = (p[0] + (k - 2) * 60 * (1 if j % 2 else -1), FLOOR)
            mini(fig, fr.fg, p[0], p[1], 0.4 * min(1, k * 2), k * math.pi * 2, 1 if j % 2 else -1,
                 head=F["boxhead"] if j % 3 == 0 else None, backpack=F["backpack"], walking=k > 2)
    elif op == "ENTER":
        k = clamp(u / 6)
        x = lerp(160, 700, k); fy = lerp(FLOOR + 40, 520, k); s = lerp(1.0, 0.16, k)
        if u < 6:
            mini(fig, fr.fg, x, fy, s, u * math.pi, 1, backpack=F["backpack"], walking=True)
        if u >= 6:
            blit(fr.fg, F["smallbox"], (720, 520), jitter(t, 8, 5) if u < 7 else 0, 1.2)
    elif op == "INTERRUPT":
        press = 2 <= u < 5
        hand_y = tween(u, [(1, -460), (2, 360), (5, 360), (6, -460)], ease)
        squash = 0.62 if press else 1.0
        J = stand_pose(640, FLOOR, 1, sh=(150, 140) if press else (6, -4))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fig.draw(layer, J, backpack=F["backpack"])
        if squash < 1:
            sq = layer.resize((W, int(H * squash)))
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); layer.alpha_composite(sq, (0, int(H * (1 - squash)) - int(70 * (1 - squash))))
        fr.fg.alpha_composite(layer)
        blit(fr.fg, a["hand_giant"], (560, hand_y), 0, 1.0)
        if 3 <= u < 5:
            stamp(fr.over, F["handlecare"], (640, 380), u, 3, rot=-6, base=2.0)


def sc_parade(fr, b, t):
    a = assets(); F = a["F"]; fig = a["fig"]
    fr.bg = a["BG"]["mountain_soft"].copy()
    u = b - 312
    if not (b >= 340):
        q = int((b - 312) // 4); uu = (b - 312) % 4
        ev = [a["beetle_big"], F["frog_dj"], F["boxhead"], a["duckrabbit"], F["frog_boxed"], F["labels"][2], F["etubrute"]][q % 7]
        if uu < 1.2:
            sc = {id(a["beetle_big"]): 0.33}.get(id(ev), 1.2)
            y = tween(uu, [(0, -200), (0.35, 300), (0.6, 280), (1.2, 900)], ease)
            blit(fr.over, ev, ((q * 337) % 900 + 190, y), (q % 3 - 1) * 12, sc)
    freeze = b >= 340
    tt = min(b, 340)
    for row, (y, s, d, n) in enumerate(((590, 0.36, 1, 7), (712, 0.5, -1, 5))):
        for j in range(n):
            x = ((j * 1500 / n + (tt - 312) * 46 * d) % 1500) - 110
            kind = (j + row) % 4
            if kind == 3:
                hop = abs(math.sin(tt * math.pi)) * 20
                blit(fr.fg, F["frog_boxed"], (x, y - hop), 0, s * 1.6 * (1 if d > 0 else -1), s * 1.6)
            else:
                mini(fig, fr.fg, x, y, s, tt * math.pi, d, head=F["boxhead"] if kind == 1 else (a["duckrabbit"] if kind == 2 else None),
                     backpack=F["backpack"], walking=not freeze)
        fr.new_layer()
    up = int(b) % 2 == 0 and not freeze
    J = stand_pose(640, 600, 1, sh=(150, 120) if up else (100, 60), el=(10, 30), head=-8 if up else 6)
    if freeze and b >= 344:
        J = stand_pose(640, 600, -1, sh=(170, 170), head=0)
    fig.draw(fr.fg, J, scale=0.8, backpack=F["backpack"])
    if not freeze:
        k = int(b) % 9
        lb = F["labels"][k]
        p = arc((-50 + (int(b) % 5) * 300, 760), (300 + (int(b) % 4) * 260, -60), 300, b - int(b))
        blit(fr.over, lb, p, (b - int(b)) * 360, 0.45)


def sc_outro(fr, b, t):
    a = assets(); F = a["F"]; fig = a["fig"]
    boxp = (760, FLOOR - 6)
    big = 1.7
    if b < 352:
        J = stand_pose(470, FLOOR, 1, sh=held(b, [(348, (6, -4)), (349, (80, 70))]), el=(-30, -30), head=10)
        carry = b >= 349
        fig.draw(fr.fg, J, backpack=None if carry else F["backpack"])
        if carry:
            p = tween(b, [(349, J["back"]), (350.5, (boxp[0], boxp[1] - 60 * big)), (351.5, (boxp[0], boxp[1] - 60 * big))])
            blit(fr.fg, F["backpack"], p, 0, big)
    else:
        # door in the box opens; he walks in, shrinking; door shuts on b358
        jig = 0 if b < 360 or b >= 368 else -abs(math.sin((b - 360) * math.pi)) * 26
        blit(fr.fg, F["backpack"], (boxp[0], boxp[1] - 60 * big + jig), (jitter(t, 4, 6) if 360 <= b < 368 else 0), big)
        hinge = (boxp[0] - 30, boxp[1] - 120)
        if b < 358.5:
            blit(fr.fg, a["doorway"], hinge, 0, 0.8, 1.2)
            sw = tween(b, [(352, 1.0), (353, -0.25), (357.6, -0.25), (358.1, 1.0)], ease_out)
            if b < 357.6:
                k = clamp((b - 353.5) / 4)
                x = lerp(470, hinge[0] + 30, ease(k)); s = lerp(1.0, 0.36, ease(k)); fy = lerp(FLOOR, hinge[1] + 92, ease(k))
                if k < 0.98:
                    mini(fig, fr.fg, x, fy, s, (b - 353.5) * math.pi, 1, backpack=None, walking=k > 0)
            blit(fr.fg, F["door_panel"], hinge, 0, 0.8 * sw, 1.2) if abs(sw) > 0.02 else None
        ending = os.environ.get("ENDING", "A")
        if ending == "B" and b >= 364:
            # the door reopens: out walks the beetle, wearing his hat
            sw = tween(b, [(364, 1.0), (364.6, -0.25)], ease_out)
            blit(fr.fg, a["doorway"], hinge, 0, 0.8, 1.2)
            blit(fr.fg, F["door_panel"], hinge, 0, 0.8 * sw, 1.2) if abs(sw) > 0.02 else None
            k = clamp((b - 364.8) / 6)
            bx = lerp(hinge[0] + 30, 1400, k); by = FLOOR - 16
            blit(fr.fg, a["beetle"], (bx, by), jitter(t, 5, 3), 1.6)
            blit(fr.fg, a["near"]["head"], (bx + 6, by - 4), 0, 0.42) if False else None
            hat = A.setdefault("hat_only", None)
            blit(fr.fg, a["tag"]["word_beetle"], (bx, by - 46), -4, 0.8)
        elif ending == "C" and b >= 364:
            # the box is opened again and it is empty: every box might be
            sw = tween(b, [(364, 1.0), (364.6, -0.25)], ease_out)
            blit(fr.fg, a["doorway"], hinge, 0, 0.8, 1.2)
            blit(fr.fg, F["door_panel"], hinge, 0, 0.8 * sw, 1.2) if abs(sw) > 0.02 else None
            stamp(fr.over, a["tag"]["empty"], (640, 300), b, 366, rot=3)
        stamp(fr.over, a["tag"]["pack"], (640, 140), b, 364 if ending != "C" else 368, rot=-2)
    if b >= 369:
        k = clamp((b - 369) / 2)
        fr.over.alpha_composite(Image.new("RGBA", (W, H), PAPER + (int(230 * k),)))
        stamp(fr.over, F["etubrute"], (640, 300), b, 370, rot=-3, base=1.1)
        stamp(fr.over, a["tag"]["title"], (640, 470), b, 371, rot=2)
        stamp(fr.over, a["tag"]["track"], (640, 600), b, 372, rot=-1)


# ---------------------------------------------------------------- SFX cue sheet
def build_sfx():
    SFX.clear()
    sfx(4.5, "thump", 0.9); sfx(8, "stamp", 0.8)
    sfx(22, "pop", 0.9); sfx(23, "rattle", 0.7); sfx(24, "whoosh", 0.6); sfx(25, "thump", 1.0); sfx(28, "creak", 0.7)
    for i in range(10): sfx(30 + i * 0.9, "pop_small", 0.5)
    sfx(40, "stamp", 0.6)
    for i in range(4): sfx(44 + 4 * i, "pop", 0.7)
    sfx(60, "rattle", 0.6); sfx(64, "stamp", 0.8); sfx(68, "thump", 0.7)
    for k in range(9): sfx(72 + 2 * k + 0.5, "thump", 0.55 + 0.04 * k)
    sfx(96, "whoosh", 0.7); sfx(97.4, "crash", 0.8); sfx(100, "stamp", 0.7)
    sfx(124, "kick", 0.8); sfx(124.4, "crash", 0.7); sfx(124, "stamp", 0.6); sfx(130, "whistle_down", 0.6); sfx(132, "thump", 1.0)
    for q in range(6): sfx(136 + 4 * q, "flip", 0.6)
    for q in range(6): sfx(160 + q, "flip", 0.5)
    sfx(157, "gulp", 0.8)
    sfx(168, "buzz", 0.35); sfx(176, "stamp", 0.5); sfx(186, "creak", 0.6); sfx(190, "buzz_close", 0.6)
    sfx(206, "blip", 0.6); sfx(210.5, "error", 0.5); sfx(220, "blip", 0.7)
    for i in range(9): sfx(240 + 8 * i, "stamp", 0.7)
    sfx(242, "pop", 0.6); sfx(250, "flip", 0.7); sfx(262, "thump", 0.7)
    for k in range(8): sfx(264 + k, "pop_small", 0.6)
    sfx(277, "crash", 0.6); sfx(285, "gulp", 0.9); sfx(302, "thump", 0.6); sfx(306, "thump", 1.0); sfx(310, "pop", 0.7)
    sfx(349, "whoosh", 0.4); sfx(352, "creak", 0.5); sfx(358, "thump", 0.9); sfx(360, "thump", 0.4); sfx(362, "thump", 0.4)
    sfx(364, "stamp", 0.6); sfx(370, "stamp", 0.5); sfx(371, "stamp", 0.5); sfx(372, "stamp", 0.4); sfx(285, "stamp", 0.6)
    return list(SFX)


SCENES = [(0, 16, "title"), (16, 40, "proof"), (40, 72, "lineup"), (72, 104, "stack"), (104, 136, "ladder"),
          (136, 168, "duckrabbit"), (168, 195.3, "flybottle"), (195.3, 236, "sketchpad"), (236, 240, "flood"),
          (240, 312, "operators"), (312, 348, "parade"), (348, 400, "outro")]


def render_frame(f):
    a = assets()
    t = f / FPS
    b = B(t)
    name = next(n for b0, b1, n in SCENES if b0 <= b < b1)
    bgk = {"title": "stage", "proof": "stage", "lineup": "stage", "stack": "stairs", "ladder": "stairs",
           "duckrabbit": "stage", "flybottle": "pallets", "flood": "stage", "outro": "stage"}.get(name, "stage")
    fr = Frame(a["BG"][bgk]); fr.flash = 0.0; fr.shake = 0.0
    if name == "title": sc_title(fr, b, t)
    elif name == "proof": sc_proof(fr, b, t)
    elif name == "lineup": sc_lineup(fr, b, t)
    elif name == "stack": sc_stack(fr, b, t)
    elif name == "ladder": sc_stack(fr, b, t, climb=True)
    elif name == "duckrabbit": sc_duck(fr, b, t)
    elif name == "flybottle": sc_bottle(fr, b, t)
    elif name == "sketchpad": sc_sketchpad(fr, b, t, f)
    elif name == "flood":
        sc_flood(fr, b, t, f)
    elif name == "operators": sc_ops(fr, b, t)
    elif name == "parade": sc_parade(fr, b, t)
    else: sc_outro(fr, b, t)
    im = fr.compose(shadow=None if name == "sketchpad" else (6, 8), flash=fr.flash)
    zoom = 1.0
    cam = None
    if name == "lineup":
        xs = [180, 410, 640, 870, 1100]
        for i in range(5):
            b0 = 44 + 4 * i
            if b0 - 0.25 <= b < b0 + (2.2 if i < 4 else 7.8):
                z = 2.4 if i < 4 else 2.9
                k = ease((b - (b0 - 0.25)) / 0.35) * (1 - ease((b - (b0 + (1.9 if i < 4 else 7.5))) / 0.3))
                cam = (lerp(1, z, k), xs[i] + 10, 470)
    if name == "outro" and b < 364 and b >= 352:
        cam = (1.5, 760, 520)
    if cam and cam[0] > 1.001:
        z, cx, cy = cam; cw, ch = W / z, H / z
        x0 = clamp(cx - cw / 2, 0, W - cw); y0 = clamp(cy - ch / 2, 0, H - ch)
        im = im.transform((W, H), Image.AFFINE, (cw / W, 0, x0, 0, ch / H, y0), resample=Image.BICUBIC)
    ZM = 1.13
    if name == "proof": zoom = lerp(1.0, ZM, ease((b - 16) / 2)) if b < 39 else lerp(ZM, 1.0, ease((b - 39) / 1))
    if zoom > 1.001:
        k = (zoom - 1) / (ZM - 1)
        cw, ch = W / zoom, H / zoom
        x0 = lerp(0, 700 - cw / 2, k); y0 = lerp(0, 32, k)
        im = im.transform((W, H), Image.AFFINE, (cw / W, 0, x0, 0, ch / H, y0), resample=Image.BICUBIC)
    if name == "flood":
        k = clamp((b - 236) / 2.5)
        # green-to-paper: start as a phosphor-tinted print and flood into colour
        g = ImageOps.colorize(im.convert("L"), (3, 20, 10), GREEN).convert("RGBA")
        im = Image.blend(g, im, ease(k))
    if name == "flybottle" and b > 194.6:
        im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), clamp((b - 194.6) / 0.7))
    if fr.shake:
        im = im.transform(im.size, Image.AFFINE, (1, 0, jitter(t, fr.shake, 7), 0, 1, jitter(t, fr.shake, 8)))
    # final fade with the song
    if t > DUR - 2.2:
        im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), clamp((t - (DUR - 2.2)) / 2.0))
    return im.convert("RGB")
