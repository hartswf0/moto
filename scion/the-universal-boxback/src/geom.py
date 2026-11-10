"""Oriented-box overlap from the trajectories (convex polygon clipping, shoelace area)."""
import math, numpy as np

def poly(p, rot, w, h):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [(p[0] + dx * c - dy * s, p[1] + dx * s + dy * c) for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]

def area(P):
    return 0.5 * abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) if len(P) > 2 else 0.0

def clip(subject, clipper):
    def inside(p, a, b): return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0
    def inter(p, q, a, b):
        x1, y1, x2, y2, x3, y3, x4, y4 = *p, *q, *a, *b
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < 1e-12: return q
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    out = subject
    # clipper is CCW in screen coords? ensure orientation
    if sum(clipper[i][0] * clipper[(i + 1) % 4][1] - clipper[(i + 1) % 4][0] * clipper[i][1] for i in range(4)) < 0:
        clipper = clipper[::-1]
    for i in range(len(clipper)):
        a, b = clipper[i], clipper[(i + 1) % len(clipper)]
        inp, out = out, []
        if not inp: break
        for k in range(len(inp)):
            p, q = inp[k], inp[(k + 1) % len(inp)]
            if inside(q, a, b):
                if not inside(p, a, b): out.append(inter(p, q, a, b))
                out.append(q)
            elif inside(p, a, b): out.append(inter(p, q, a, b))
    return out

def max_overlap(P, rot, ws, hs, visible=None):
    """largest pairwise overlap as a fraction of the smaller box's area; boxes fully off screen are skipped."""
    polys = [poly(P[j], rot[j], ws[j], hs[j]) for j in range(len(P))]
    worst, pair = 0.0, None
    for i in range(len(P)):
        if visible is not None and not visible[i]: continue
        for j in range(i + 1, len(P)):
            if visible is not None and not visible[j]: continue
            if math.dist(P[i], P[j]) > (math.hypot(ws[i], hs[i]) + math.hypot(ws[j], hs[j])) / 2: continue
            a = area(clip(polys[i], polys[j]))
            f = a / min(ws[i] * hs[i], ws[j] * hs[j])
            if f > worst: worst, pair = f, (i, j)
    return worst, pair
