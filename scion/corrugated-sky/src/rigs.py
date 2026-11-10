"""Reiniger shadow-theatre rigs.

First-class primitives (SCION-REINIGER §2):
  Bone       pinned joint + joint-angle limits (lo, hi) on the deviation from its rest (base) angle
  profiles   replacement profiles per bone (e.g. hand: open / grip / offer; head: left / up)
  Rig.fk     pose (angles) -> world bone frames; every requested angle is checked against its limits
  ik2        analytic two-bone solve for contacts (hand on rung, foot on floor) -> deviations, then checked
  CONTACT / LIMIT logs feed the numeric invariant tests.

Coordinates: design px 1280x720, y down. Angles: degrees, screen convention (0 = right, 90 = down).
Characters are authored facing RIGHT; face=-1 mirrors about the root x.
"""
import math

LIMIT_LOG = []    # (who, bone, requested_dev, lo, hi) for any request outside limits
CONTACT_LOG = []  # (who, name, residual_px)


def _rot(p, a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


class Bone:
    def __init__(self, name, parent, length, base, limits, shape, at=1.0, offset=(0, 0), profiles=None, z=0):
        self.name, self.parent, self.length, self.base, self.limits = name, parent, length, base, limits
        self.shape = shape            # polygon list (or list of polygons) in bone-local coords, x along the bone
        self.at = at                  # where on the parent bone this joint is pinned (fraction of parent length)
        self.offset = offset          # extra local offset of the pin on the parent (parent-local coords)
        self.profiles = profiles or {}
        self.z = z


class Rig:
    def __init__(self, who, bones, scale=1.0):
        self.who = who
        self.bones = bones
        self.by = {b.name: b for b in bones}
        self.scale = scale

    def fk(self, root, pose, lean=0.0, face=1, check=True, tag=""):
        """pose: {bone: deviation}. Returns {bone: (origin(x,y), world_angle, end(x,y))} in facing-right space,
        then mirrored if face==-1."""
        W = {}
        k = self.scale
        for b in self.bones:  # bones are listed parent-before-child
            dev = pose.get(b.name, 0.0)
            lo, hi = b.limits
            if check and not (lo - 1e-6 <= dev <= hi + 1e-6):
                LIMIT_LOG.append((self.who + tag, b.name, round(dev, 3), lo, hi))
                dev = max(lo, min(hi, dev))
            if b.parent is None:
                pa = lean
                o = (root[0] + b.offset[0] * k, root[1] + b.offset[1] * k)
                o = _rot_about(o, root, lean) if b.offset != (0, 0) else o
            else:
                po, pa, _ = W[b.parent]
                pb = self.by[b.parent]
                loc = (pb.length * b.at + b.offset[0], b.offset[1])
                r = _rot((loc[0] * k, loc[1] * k), pa)
                o = (po[0] + r[0], po[1] + r[1])
            ang = pa + b.base + dev
            e = _rot((b.length * k, 0), ang)
            W[b.name] = (o, ang, (o[0] + e[0], o[1] + e[1]))
        if face == -1:
            W = {n: (_mx(o, root), 180 - a, _mx(e, root)) for n, (o, a, e) in W.items()}
        return W

    def polys(self, W, profile=None, face=1):
        """World polygons in bone z order."""
        out = []
        k = self.scale
        for b in sorted(self.bones, key=lambda b: b.z):
            o, a, _ = W[b.name]
            shp = b.profiles.get((profile or {}).get(b.name), b.shape) if profile else b.shape
            if shp is None:
                continue
            polys = shp if (shp and isinstance(shp[0], list)) else [shp]
            for poly in polys:
                if face == 1:
                    pts = [(o[0] + q[0], o[1] + q[1]) for q in (_rot((x * k, y * k), a) for x, y in poly)]
                else:
                    # mirrored: local y flips so the profile faces left
                    pts = [(o[0] + q[0], o[1] + q[1]) for q in (_rot((x * k, -y * k), a) for x, y in poly)]
                out.append(pts)
        return out


def _mx(p, root):
    return (2 * root[0] - p[0], p[1])


def _rot_about(p, c, a):
    r = _rot((p[0] - c[0], p[1] - c[1]), a)
    return (c[0] + r[0], c[1] + r[1])


def ik2(origin, parent_angle, base1, l1, l2, target, bend):
    """Two-bone analytic IK. Returns (dev1, dev2, reachable). bend=+1 bends the joint clockwise."""
    dx, dy = target[0] - origin[0], target[1] - origin[1]
    d = math.hypot(dx, dy)
    reach = d <= l1 + l2 - 1e-6
    dc = max(abs(l1 - l2) + 1e-6, min(d, l1 + l2 - 1e-6))
    a_t = math.degrees(math.atan2(dy, dx))
    c1 = (l1 * l1 + dc * dc - l2 * l2) / (2 * l1 * dc)
    a1 = a_t - bend * math.degrees(math.acos(max(-1, min(1, c1))))
    c2 = (l1 * l1 + l2 * l2 - dc * dc) / (2 * l1 * l2)
    inner = math.degrees(math.acos(max(-1, min(1, c2))))
    a2 = bend * (180 - inner)
    dev1 = _wrap(a1 - parent_angle - base1)
    return dev1, a2, reach


def _wrap(a):
    while a > 180: a -= 360
    while a <= -180: a += 360
    return a


# ------------------------------------------------------------------ shapes (bone-local, x along bone)
def taper(l, w0, w1, round_end=True):
    pts = [(0, -w0 / 2), (l, -w1 / 2), (l, w1 / 2), (0, w0 / 2)]
    return [(0, -w0 / 2)] + [(l, -w1 / 2)] + ([(l + w1 * 0.35, 0)] if round_end else []) + [(l, w1 / 2), (0, w0 / 2), (-w0 * 0.35, 0)]


def circle(cx, cy, r, n=14):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def human(who, kind="girl", scale=1.0):
    """kind: girl | boy | mother | father. Torso points up (base -90). Facing right = +x.
    Head profile: nose toward +y local when torso points up?  Local frame of the head bone points up (-90 world),
    so local +y = world +x (facing direction)."""
    big = kind in ("mother", "father")
    T = 74 if big else 52           # torso
    UA, FA = (40, 38) if big else (28, 27)
    TH, SH = (52, 50) if big else (36, 35)
    hw = 30 if big else 24          # head radius-ish
    bones = []
    torso_w = 30 if big else 22
    torso = [(0, -torso_w / 2), (T, -torso_w / 2 * 0.9), (T + 4, 0), (T, torso_w / 2 * 0.9), (0, torso_w / 2)]
    skirt = None
    if kind in ("girl", "mother"):
        L = 50 if big else 30
        skirt = [(T * 0.55, -torso_w / 2), (-L, -torso_w * 1.25), (-L - 4, -torso_w * 0.2), (-L, torso_w * 1.25), (T * 0.55, torso_w / 2)]
    bones.append(Bone("torso", None, T, -90, (-35, 35), [torso] + ([skirt] if skirt else []), z=2))
    # head: profile facing +local y (= facing direction)
    r = hw * 0.55
    head = circle(r * 1.1, 0, r)
    nose = [(r * 0.9, r * 0.75), (r * 0.55, r * 1.35), (r * 0.3, r * 0.85)]
    neck = [(-4, -5), (6, -5), (6, 5), (-4, 5)]
    extra = []
    if kind == "girl":
        extra = [[(r * 1.2, -r * 1.1), (r * 2.3, -r * 0.9), (r * 2.4, -r * 0.2), (r * 1.5, -r * 0.4)],      # bow
                 [(r * 0.2, -r * 1.05), (r * 1.9, -r * 1.05), (r * 2.0, r * 0.1), (r * 0.1, -r * 0.6)]]    # bob hair back
    if kind == "mother":
        extra = [circle(r * 2.0, -r * 0.6, r * 0.55)]  # bun
    if kind == "father":
        extra = [[(r * 1.7, -r * 1.4), (r * 1.7, r * 1.6), (r * 2.0, r * 1.6), (r * 2.0, -r * 1.4)],
                 [(r * 2.0, -r * 0.9), (r * 3.0, -r * 0.8), (r * 3.0, r * 0.9), (r * 2.0, r * 0.9)]]  # hat
    if kind == "boy":
        extra = [[(r * 1.6, -r * 1.1), (r * 2.2, -r * 0.2), (r * 1.9, r * 0.5), (r * 1.4, r * 1.4), (r * 2.0, r * 1.8), (r * 2.25, r * 0.9)]]  # cap
    head_up = [neck, head, nose] + extra
    head_back = [[(x, -y) for x, y in poly] for poly in head_up]   # replacement profile: the head turned the other way
    bones.append(Bone("head", "torso", r * 0.2, 0, (-40, 40), head_up, at=1.0, z=3, profiles={"fwd": head_up, "back": head_back}))
    for side, z0 in (("f", 0), ("n", 5)):
        bones.append(Bone("upper_" + side, "torso", UA, 180, (-200, 60), [taper(UA, 11 if big else 8, 9 if big else 7)],
                          at=0.92, z=z0))
        bones.append(Bone("fore_" + side, "upper_" + side, FA, 0, (-155, 2), [taper(FA, 9 if big else 7, 7 if big else 5)], z=z0))
        hs = 1.25 if big else 1.0
        # open: palm + four spread fingers + thumb, each separated by light (reads as an opened hand at phone size)
        palm = [(0, -4 * hs), (7 * hs, -5 * hs), (8 * hs, 4 * hs), (0, 4 * hs)]
        fan = [palm]
        for k, a in enumerate((-50, -22, 4, 30)):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            bx, by = 7 * hs, (-4 + 2.6 * k) * hs
            L = 13 * hs
            fan.append([(bx - 1.2 * sa * hs, by + 1.2 * ca * hs), (bx + L * ca - 1.0 * sa * hs, by + L * sa + 1.0 * ca * hs),
                        (bx + L * ca + 1.0 * sa * hs, by + L * sa - 1.0 * ca * hs), (bx + 1.2 * sa * hs, by - 1.2 * ca * hs)])
        fan.append([(1.5 * hs, 1.5 * hs), (6 * hs, 15 * hs), (8.5 * hs, 14 * hs), (5.5 * hs, 1.5 * hs)])  # thumb, rooted inside the palm
        open_h = fan
        grip = [circle(5 * hs, 0, 5.5 * hs, 10)]
        # offer: flat palm up, fingers together, thumb separated from the fingers by a V of light
        offer = [[(0, -4 * hs), (16 * hs, -5 * hs), (18 * hs, -2.5 * hs), (16 * hs, 0.5 * hs), (6.5 * hs, 1 * hs),   # fingers' underside
                  (4.2 * hs, 2.2 * hs),                                                                       # bottom of the V notch (stops at the palm)
                  (9 * hs, 8.5 * hs), (7.5 * hs, 10.5 * hs), (0.5 * hs, 5.5 * hs), (0, 2 * hs)]]              # thumb, joined at its base
        bones.append(Bone("hand_" + side, "fore_" + side, 10 * hs, 0, (-70, 70), open_h,
                          profiles={"open": open_h, "grip": grip, "offer": offer}, z=z0))
        bones.append(Bone("thigh_" + side, None, TH, 90, (-125, 40), [taper(TH, 13 if big else 10, 10 if big else 8)], z=z0 + 1))
        bones.append(Bone("shin_" + side, "thigh_" + side, SH, 0, (-2, 150), [taper(SH, 10 if big else 8, 7 if big else 6)], z=z0 + 1))
        foot = [(-3, -5), (0, -6), (16 if big else 12, -3), (18 if big else 14, 2), (0, 4)]
        bones.append(Bone("foot_" + side, "shin_" + side, 14 if big else 10, -90, (-35, 45), [foot], z=z0 + 1))
    return Rig(who, bones, scale)


def dog(who="dog", scale=1.0):
    """Lean dog authored facing right. Root at the hips; spine points forward (0). Rising: spine dev negative."""
    bones = []
    body = [(-8, -10), (14, -13), (40, -11), (64, -15), (78, -12), (82, 2), (76, 16), (62, 20), (46, 10), (24, 6), (4, 8), (-10, 4)]
    bones.append(Bone("spine", None, 74, 0, (-80, 25), [body], z=2))
    neck = [(0, -8), (24, -6), (26, 6), (0, 9)]
    bones.append(Bone("neck", "spine", 22, -45, (-40, 70), [neck], at=1.0, z=3))
    head = [(-6, -9), (8, -11), (20, -7), (40, -3), (44, 2), (40, 6), (22, 8), (6, 9), (-4, 6)]
    ear = [(2, -9), (6, -26), (14, -9)]
    bones.append(Bone("head", "neck", 12, 45, (-50, 50), [head, ear], at=1.0, z=4))
    tail = [(0, -2.5), (22, -4), (38, -1), (22, 2.5), (0, 3)]
    bones.append(Bone("tail", None, 38, 200, (-70, 70), [tail], offset=(-8, -6), z=1))
    for side, z0 in (("f", 0), ("n", 6)):
        bones.append(Bone("hthigh_" + side, None, 28, 100, (-100, 50), [taper(28, 13, 7)], offset=((-9, -1) if side == "f" else (0, 0)), z=z0))
        bones.append(Bone("hshin_" + side, "hthigh_" + side, 30, 20, (-10, 120), [taper(30, 6, 4.5)], z=z0))
        bones.append(Bone("fleg_" + side, "spine", 28, 85, (-160, 60), [taper(28, 9, 6)], at=(0.7 if side == "f" else 0.92), z=z0))
        bones.append(Bone("fpaw_" + side, "fleg_" + side, 26, 0, (-130, 30), [taper(26, 6, 5)], z=z0))
    return Rig(who, bones, scale)


def ik_pick(origin, pa, base, l1, l2, target, lim1, lim2):
    """Try both bend branches; return the one whose deviations respect both joint limits (else the closest)."""
    best = None
    for bend in (1, -1):
        d1, d2, reach = ik2(origin, pa, base, l1, l2, target, bend)
        bad = max(0, lim1[0] - d1, d1 - lim1[1]) + max(0, lim2[0] - d2, d2 - lim2[1])
        if best is None or bad < best[0]:
            best = (bad, d1, d2, reach)
    return best[1], best[2], best[3]


# ------------------------------------------------------------------ poses
def stand(kind_big=False):
    return {"torso": 0, "head": 0, "upper_n": 6, "fore_n": -12, "upper_f": -4, "fore_f": -10,
            "thigh_n": -3, "shin_n": 4, "foot_n": 0, "thigh_f": 3, "shin_f": 4, "foot_f": 0}


def walk(phase, stride=24):
    s = math.sin(phase)
    p = stand()
    p.update({"thigh_n": -stride * s, "thigh_f": stride * s,
              "shin_n": max(0, 34 * math.sin(phase + 1.2)) + 2, "shin_f": max(0, 34 * math.sin(phase + 1.2 + math.pi)) + 2,
              "upper_n": 18 * s, "upper_f": -18 * s, "fore_n": -18, "fore_f": -18,
              "foot_n": 0, "foot_f": 0})
    return p


def dog_stand(wag=0.0):
    # near and far legs splayed apart so four separate leg plates read in silhouette
    return {"spine": 0, "neck": 0, "head": 0, "tail": wag, "hthigh_n": -10, "hshin_n": 22, "hthigh_f": 14, "hshin_f": 16,
            "fleg_n": -14, "fpaw_n": 2, "fleg_f": 12, "fpaw_f": -4}


def dog_walk(phase, wag=0.0):
    s = math.sin(phase)
    p = dog_stand(wag)
    p.update({"hthigh_n": -10 + 16 * s, "hthigh_f": 14 - 16 * s, "hshin_n": 20 + 12 * max(0, math.sin(phase + 1)),
              "hshin_f": 20 + 12 * max(0, math.sin(phase + 1 + math.pi)), "fleg_n": -14 - 16 * s, "fleg_f": 12 + 16 * s,
              "fpaw_n": -max(0, 30 * math.sin(phase + 1.5)), "fpaw_f": -max(0, 30 * math.sin(phase + 1.5 + math.pi)),
              "spine": 2 * math.sin(phase * 2)})
    return p


def legs_to_floor(rig, root, pose, floor_y, face=1, lean=0.0):
    """Vertical card slide: shift the root so the lowest foot/paw end touches the floor line (contact plane)."""
    W = rig.fk(root, pose, lean=lean, face=face, check=False)
    ys = [W[n][2][1] for n in W if n.startswith(("foot", "hshin", "fpaw"))]
    ys += [W[n][0][1] for n in W if n.startswith("foot")]
    if not ys:
        return root
    return (root[0], root[1] + floor_y - max(ys) - 2 * rig.scale)
