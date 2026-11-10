"""SCION-SUTHERLAND constraint layer.

Constraint graph (typed, inspectable):
  points : pelvis, neck, shoulder, elbow, hand, hip, knee_n, knee_f, ankle_n, ankle_f
  lines  : torso(pelvis->neck), upper(shoulder->elbow), fore(elbow->hand), thigh(hip->knee), shin(knee->ankle)
  constraints:
    LENGTH(line) == rest length            (equality)
    PIN(ankle_n == plant_n), PIN(ankle_f == plant_f)   (contact: feet planted)
    ATTACH(hand == target)                 (attached-to / held-by)   -- soft when unreachable
  priorities: PIN > LENGTH > ATTACH.  The solver never violates PIN or LENGTH; when ATTACH cannot be met
  it reports UNSOLVABLE with the residual instead of teleporting a joint.

Solver: analytic two-bone IK for each limb + a bounded search over pelvis shift / torso lean
(hierarchical), choosing the elbow branch that keeps the elbow below the shoulder->hand line.
"""
import math

REST = dict(torso=150.0, sh_off=(6.0, -138.0), upper=70.0, fore=66.0, thigh=90.0, shin=88.0)


def _sub(a, b): return (a[0] - b[0], a[1] - b[1])
def _add(a, b): return (a[0] + b[0], a[1] + b[1])
def _len(v): return math.hypot(v[0], v[1])
def _rot(v, deg):
    t = math.radians(deg); return (v[0] * math.cos(t) - v[1] * math.sin(t), v[0] * math.sin(t) + v[1] * math.cos(t))


def two_bone(root, target, a, b, bend):
    """Return (joint, end, reachable). bend=+1/-1 picks the elbow/knee branch.
    Bone lengths are exact by construction; if unreachable the end lies on the root->target ray."""
    d = _sub(target, root); L = _len(d)
    eps = 1e-9
    reach = L <= a + b + 1e-9 and L >= abs(a - b) - 1e-9
    Lc = min(max(L, abs(a - b) + 1e-6), a + b - 1e-6)
    base = math.atan2(d[1], d[0]) if L > eps else 0.0
    cos_r = (a * a + Lc * Lc - b * b) / (2 * a * Lc)
    ang = base + bend * math.acos(max(-1.0, min(1.0, cos_r)))
    joint = (root[0] + a * math.cos(ang), root[1] + a * math.sin(ang))
    dj = _sub((root[0] + Lc * math.cos(base), root[1] + Lc * math.sin(base)), joint)
    k = b / max(_len(dj), eps)
    end = (joint[0] + dj[0] * k, joint[1] + dj[1] * k)
    return joint, end, reach


def body_from(pelvis, lean, plant_n, plant_f, hand_target, face=1, rest=REST, elbow_pref=None):
    neck = _add(pelvis, _rot((0, -rest["torso"]), lean))
    shoulder = _add(pelvis, _rot((rest["sh_off"][0] * face, rest["sh_off"][1]), lean))
    hip = pelvis
    # knees bend forward (toward facing direction): pick branch accordingly
    kb = -1 * face
    knee_n, ank_n, rn = two_bone(hip, plant_n, rest["thigh"], rest["shin"], kb)
    knee_f, ank_f, rf = two_bone(hip, plant_f, rest["thigh"], rest["shin"], kb)
    best = None
    for bend in ((elbow_pref,) if elbow_pref else (1, -1)):
        el, hand, ra = two_bone(shoulder, hand_target, rest["upper"], rest["fore"], bend)
        # believable: elbow below shoulder->hand line (screen y down => larger y)
        sx, sy = shoulder; hx, hy = hand
        cross = (hx - sx) * (el[1] - sy) - (hy - sy) * (el[0] - sx)
        below = cross * face > 0
        score = (0 if below else 1)
        if best is None or score < best[0]:
            best = (score, el, hand, ra, bend)
    _, elbow, hand, reach_a, bend = best
    return dict(pelvis=pelvis, neck=neck, shoulder=shoulder, hip=hip, knee_n=knee_n, ankle_n=ank_n,
                knee_f=knee_f, ankle_f=ank_f, elbow=elbow, hand=hand, legs_ok=rn and rf,
                arm_ok=reach_a, elbow_bend=bend, lean=lean)


def solve_reach(rest_pelvis, plant_n, plant_f, target, face=1, rest=REST, prev=None,
                max_shift=34.0, max_lean=30.0, steps=17):
    """Hierarchical solve: search pelvis shift (x and crouch y) and lean so that PIN and LENGTH hold
    exactly, then minimise ATTACH residual + a comfort cost (stay near rest, and near previous pose
    for stability under small pointer moves)."""
    def ok_pel(p2):
        if p2[1] < rest_pelvis[1] - 1e-6: return False
        lim = rest["thigh"] + rest["shin"] - 0.5
        return _len(_sub(plant_n, p2)) <= lim and _len(_sub(plant_f, p2)) <= lim

    def refine(b, res):
        pel, lean = b["pelvis"], b["lean"]; step = 2.0
        for _ in range(60):
            if res < 1e-3: break
            improved = False
            for ddx, ddy, dl in ((step, 0, 0), (-step, 0, 0), (0, step, 0), (0, -step, 0), (0, 0, step), (0, 0, -step)):
                p2 = (pel[0] + ddx, pel[1] + ddy); l2 = max(-max_lean, min(max_lean, lean + dl))
                if abs(p2[0] - rest_pelvis[0]) > max_shift or not ok_pel(p2): continue
                b2 = body_from(p2, l2, plant_n, plant_f, target, face, rest, elbow_pref=b["elbow_bend"])
                r2 = _len(_sub(b2["hand"], target))
                if r2 < res - 1e-6:
                    b, res, pel, lean, improved = b2, r2, p2, l2, True
            if not improved:
                step *= 0.5
                if step < 0.01: break
        return b, res

    b = None
    if prev is not None:
        # continuation: start from the previous pose so small pointer moves give small pose moves
        b0 = body_from(prev["pelvis"], prev["lean"], plant_n, plant_f, target, face, rest, elbow_pref=prev["elbow_bend"])
        b, res = refine(b0, _len(_sub(b0["hand"], target)))
        if res > 0.5:
            b = None
    if b is None:
        best = None
        for i in range(steps):
            dx = -max_shift + 2 * max_shift * i / (steps - 1)
            for dy in (0.0, 8.0, 16.0, 26.0):
                pel = (rest_pelvis[0] + dx, rest_pelvis[1] + dy)
                if not ok_pel(pel): continue
                for j in range(steps):
                    lean = -max_lean + 2 * max_lean * j / (steps - 1)
                    bb = body_from(pel, lean, plant_n, plant_f, target, face, rest)
                    res = _len(_sub(bb["hand"], target))
                    cost = res * 10 + 0.002 * (dx * dx + 2 * dy * dy) + 0.004 * lean * lean
                    if best is None or cost < best[0]:
                        best = (cost, bb, res)
        if best is None:
            return None
        b, res = refine(best[1], best[2])
    b["residuals"] = residuals(b, plant_n, plant_f, target, rest)
    b["solvable"] = b["residuals"]["attach"] < 0.5
    return b


def residuals(b, plant_n, plant_f, target, rest=REST):
    L = lambda p, q: _len(_sub(p, q))
    lens = {
        "torso": abs(L(b["pelvis"], b["neck"]) - rest["torso"]),
        "upper": abs(L(b["shoulder"], b["elbow"]) - rest["upper"]),
        "fore": abs(L(b["elbow"], b["hand"]) - rest["fore"]),
        "thigh_n": abs(L(b["hip"], b["knee_n"]) - rest["thigh"]),
        "shin_n": abs(L(b["knee_n"], b["ankle_n"]) - rest["shin"]),
        "thigh_f": abs(L(b["hip"], b["knee_f"]) - rest["thigh"]),
        "shin_f": abs(L(b["knee_f"], b["ankle_f"]) - rest["shin"]),
    }
    return {"length_max": max(lens.values()), "lengths": lens,
            "pin_n": L(b["ankle_n"], plant_n), "pin_f": L(b["ankle_f"], plant_f),
            "attach": L(b["hand"], target)}


def max_reach(rest_pelvis, plant_n, plant_f, face=1, rest=REST):
    """Upper bound on shoulder->target distance + shoulder travel (for UI hinting)."""
    return rest["upper"] + rest["fore"]
