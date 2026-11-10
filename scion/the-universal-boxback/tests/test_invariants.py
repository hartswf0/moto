"""Numeric invariants for THE UNIVERSAL BOXBACK (r2). Run: python3 -I tests/test_invariants.py -> tests/invariants.json
All values come from the closed-form trajectories the renderer draws, except T4 (rendered pixels)."""
import sys, os, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "src")); sys.path.insert(0, HERE)
import film, geom
R = []
def check(name, ok, **d): R.append({"test": name, "pass": bool(ok), **d}); print(("PASS " if ok else "FAIL ") + name, d)
ang = lambda P, j: math.atan2((P[j][1] - film.CY) / 0.80, P[j][0] - film.CX)
fb = lambda f: film.B(f / 24) + 0.5 * film.FB          # the beat a frame shows (half-frame snap)

def max_overlap_window(t0, t1):
    worst = (0.0, None, None)
    for f in range(int(math.ceil(t0 * 24)), int(math.floor(t1 * 24)) + 1):
        b = fb(f); P, r, sc, gl, face = film.state(b)
        ws = [film.box_w(j, b) * sc[j] for j in range(20)]; hs = [film.box_h(j) * sc[j] for j in range(20)]
        vis = [(face[j] > 0.01) and sc[j] > 0.1 and (-60 < P[j][1] < 780) and (-140 < P[j][0] < 1420) for j in range(20)]
        w, pr = geom.max_overlap(P, r, ws, hs, vis)
        if w > worst[0]: worst = (w, pr, f)
    return worst

# --- protected: the 3:2 integers, reunions, nine passes, proof separation
bs = np.arange(52, 72.0001, 0.01)
th = np.unwrap(np.array([[ang(film.ring(b)[0], j) for j in range(20)] for b in bs]), axis=0)
laps = (th[-1] - th[0]) / (2 * math.pi)
check("P1 proof phase ratio A:B = 3:2", abs(laps[:10].mean() / laps[10:].mean() - 1.5) < 0.01, laps_A=round(float(laps[:10].mean()), 4), laps_B=round(float(laps[10:].mean()), 4))
for b in (52, 72):
    P = film.ring(b)[0]
    e = max(abs((ang(P, i) - ang(P, i + 10) + math.pi) % (2 * math.pi) - math.pi) for i in range(10))
    check(f"P2 reunion at b{b}", e < 1e-9, max_angle_err_rad=e)
worst = max(max(abs((ang(film.ring(52 + 2 * m)[0], i) - ang(film.ring(52 + 2 * m)[0], (i + m) % 10 + 10) + math.pi) % (2 * math.pi) - math.pi) for i in range(10)) for m in range(1, 10))
check("P3 nine interference passes on even beats", worst < 1e-9, max_angle_err_rad=worst)
w = min(math.dist(film.ring(b)[0][i], film.ring(b)[0][j]) for b in np.arange(52, 72.0001, 0.05) for i in range(20) for j in range(i + 1, 20) if j != i + 10)
check("P4 proof non-pair separation >= 60 px", w >= 60, min_px=round(w, 2))

# --- critic item 1: release window 164-169.85 s, no overlap > 10 %; houses builds row by row; b368 lands on its frame
wo = max_overlap_window(164.0, 169.85)
check("C1a release 164-169.85 s: max box overlap <= 10 %", wo[0] <= 0.10, max_overlap=round(wo[0], 4), pair=wo[1], frame=wo[2])
rows_ok = all(film.RAIN[j] + 1.25 <= film.RAIN[k] + 1e-9 for r1, r2 in zip(film.F_ROWS, film.F_ROWS[1:]) for j in r1 for k in r2)
check("C1b the house rains back row by row (each row lands before the next starts)", rows_ok, rows=[[round(film.RAIN[j] + 1.25, 2) for j in r] for r in film.F_ROWS])
f368 = int(round(film.T(368) * 24))
e_on = float(np.abs(film.state(fb(f368))[0] - film.F_ARR).max()); e_before = float(np.abs(film.state(fb(f368 - 1))[0] - film.F_ARR).max())
check("C1c last box lands ON the b368 frame (nearest frame), not after", e_on < 0.5 and e_before > 0.5, frame=f368, err_on_px=round(e_on, 3), err_prev_frame_px=round(e_before, 1))

# --- critic item 2: every row's arrangement differs between 116.5 s and 122.5 s
def rows_at(t):
    P = film.state(film.B(t) + 0.5 * film.FB)[0]; rows = {}
    for j in range(20):
        for r, y in film.ROWY.items():
            if abs(P[j][1] - y) < 8: rows.setdefault(r, []).append(round(float(P[j][0])))
    return {r: sorted(v) for r, v in rows.items()}
ra, rb = rows_at(116.5), rows_at(122.5)
changed = {r: (len(ra.get(r, [])) != len(rb.get(r, [])) or any(abs(x - y) > 20 for x, y in zip(ra.get(r, []), rb.get(r, [])))) for r in range(1, 7)}
check("C2 every row changed (116.5 s vs 122.5 s)", all(changed.values()), at_116_5=ra, at_122_5=rb)
check("C2b after the re-phase the house is the end form F", float(np.abs(film.state(266)[0] - film.F_ARR).max()) < 3.5)
wp = max_overlap_window(film.T(238), film.T(266))
check("C2c Plato section: max box overlap <= 10 %", wp[0] <= 0.10, max_overlap=round(wp[0], 4), pair=wp[1], frame=wp[2])

# --- critic item 3: markers. A (box 0, red) passes 12 o'clock 3 times, B (box 10, yellow) 2 times, b52-b72
def crossings(j):
    a = np.unwrap([ang(film.ring(b)[0], j) for b in np.arange(52, 72.0001, 0.01)])
    return int(np.floor((a[-1] + math.pi / 2) / (2 * math.pi) + 1e-9) - np.floor((a[0] + math.pi / 2) / (2 * math.pi) + 1e-9))
check("C3 marker A passes 12 o'clock 3x, marker B 2x (b52-72)", crossings(0) == 3 and crossings(10) == 2, A=crossings(0), B=crossings(10))
per_beat = [round(math.degrees(ang(film.ring(b)[0], 0)) % 360) for b in range(52, 73)]
check("C3b per-beat sampling can count it (A moves 54 deg per beat < 180)", max(np.diff(np.unwrap(np.radians(per_beat)))) < math.pi, A_deg_per_beat=per_beat[:6])

# --- critic item 4: something changes ON the b77 frame (rendered pixels)
f77 = int(round(film.T(77) * 24))
im = lambda f: np.asarray(film.render_frame(f), np.float32)
d_hold = float(np.abs(im(f77 - 1) - im(f77 - 2)).mean()); d_stop = float(np.abs(im(f77) - im(f77 - 1)).mean())
check("C4 the stop shows on the b77 frame (pixel change >> hold)", d_stop > 5 * max(d_hold, 0.2), frame=f77, mean_abs_diff_stop=round(d_stop, 3), mean_abs_diff_hold=round(d_hold, 3))

# --- critic item 6: dissolve 16.3-18.7 s and re-lock 70-71.5 s: no overlap > 10 %
for (t0, t1, nm) in ((16.3, 18.7, "dissolve"), (70.0, 71.5, "re-lock")):
    wo = max_overlap_window(t0, t1)
    check(f"C6 {nm} {t0}-{t1} s: max box overlap <= 10 %", wo[0] <= 0.10, max_overlap=round(wo[0], 4), pair=wo[1], frame=wo[2])
ev = {e["kind"]: e["b"] for e in film.EVENTS}
check("C6b lock / unlock / re-lock stars on whole beats", all(abs(ev[k] - round(ev[k])) < 1e-9 for k in ("lock", "unlock", "relock")), beats={k: ev[k] for k in ("lock", "unlock", "relock")})

# --- the bookend and the rest
e_end = float(np.abs(film.state(368.0)[0] - film.state(20.0)[0]).max())
check("B1 final house == opening end form (eps 0.5 px)", e_end < 0.5, max_err_px=e_end)
_, _, _, _, face20 = film.state(20.0); _, _, _, _, face373 = film.state(373.0)
check("B2 both bookends are the constellation (faces off, points on)", float(face20.max()) < 0.01 and float(face373.max()) < 0.01)
e_lock = float(np.abs(film.bank(84, 0.0, 0.85) - film.bank(100, 0.0, 0.85)).max()); e_drift = float(np.abs(film.bank(116, 0.06, 0.85) - film.bank(132, 0.06, 0.85)).max())
check("B3 rational lock closes in 16 beats; detuned drift does not", e_lock < 1e-6 and e_drift > 20, lock_err_px=e_lock, drift_err_px=round(e_drift, 1))
bad = [b for b in np.arange(242.5, 256.5, 0.05) if math.dist(film.state(b)[0][film.BEAM], film.SLOT_P0[film.BEAM]) < 60]
check("B4 beam refused by row 3 until the house is re-planned", not bad)
lands = {j: film.land_beat(k) for k, j in enumerate(film.MAKE_ORDER)}
check("B5 making starts at the first step (lower rows land first)", all(lands[j] < lands[k] for j in film.MAKE_ORDER for k in film.MAKE_ORDER if film.SLOT_P0[j][1] > film.SLOT_P0[k][1]))


# ===== critic round 2 =====
# D1 the stall becomes the densest passage: >=8 boxes move >=15 px between consecutive beats on >=50 % of beats (122-140 s)
bs_ = [b for b in range(int(math.ceil(film.B(122))), int(math.floor(film.B(140))) + 1)]
moving = []
for b0, b1 in zip(bs_, bs_[1:]):
    d = np.hypot(*(film.state(b1)[0] - film.state(b0)[0]).T)
    moving.append(int((d >= 15).sum()))
frac = float(np.mean([m >= 8 for m in moving]))
check("D1 122-140 s: >=8 boxes move >=15 px on >=50 % of beats", frac >= 0.5, fraction_of_beats=round(frac, 3), boxes_moving_per_beat=moving)
# D2 the motion is a visible phase relation: odd rows 3, even rows 2 cycles per 8 beats; rows re-align every 8 beats
ro = [film.row_offsets(b) for b in np.arange(film.ACC_B0, film.ACC_B1, 0.01)]
zc = lambda r: int(np.sum(np.diff(np.sign([o[r] for o in ro])) != 0))
check("D2 accumulation phase relation odd:even rows = 3:2", abs(zc(1) / zc(2) - 1.5) < 0.1, zero_crossings_row1=zc(1), zero_crossings_row2=zc(2))
# D3 pixel coverage of the accumulation exceeds every earlier section (rendered pixels)
import coverage as COV
cov = {n: COV.coverage(a, b)[0] for n, a, b in COV.SECTIONS if b <= 304}
earlier = {k: v for k, v in cov.items() if k != "accumulation"}
check("D3 accumulation coverage exceeds every earlier section", cov["accumulation"] > max(earlier.values()),
      accumulation=round(cov["accumulation"], 4), best_earlier=max(earlier, key=earlier.get), best_earlier_value=round(max(earlier.values()), 4))
# D4 the house is back in its slots exactly by 140 s
e140 = float(np.abs(film.state(film.B(140.0) + 0.5 * film.FB)[0] - film.F_ARR).max())
check("D4 house slots return exactly by 140 s", e140 < 1e-6, max_err_px=e140)
# E1 every caption / card / tag stays within x = 40..1240 (rendered text boxes)
film.TEXT_LOG = []
for f in range(0, int(film.DUR * 24), 3):
    film.render_frame(f)
bad = [t for t in film.TEXT_LOG if t[1] < 39.5 or t[3] > 1240.5]
check("E1 all text within x = 40..1240", not bad, texts_checked=len(film.TEXT_LOG), unique=len({t[0] for t in film.TEXT_LOG}), violations=bad[:5])
film.TEXT_LOG = None
# E2 tags and legend: cap height >= 12 px at 360 px width
a_ = film.assets(); bb = a_["f_card"].getbbox("ARCH")
check("E2 ARCH/BLDR tags and A×3/B×2 legend >= 12 px tall at 360 px", (bb[3] - bb[1]) * 360 / 1280 >= 12, height_at_360_px=round((bb[3] - bb[1]) * 360 / 1280, 1))
# F1 the release ring stays inside the frame (y <= 700), 151.5-160 s
ymax = 0.0
for f in range(int(151.5 * 24), int(160 * 24) + 1):
    b = fb(f); P, r, sc, gl, face = film.state(b)
    for j in range(20):
        for (x, y) in film.corners(P[j], r[j], film.box_w(j, b) * sc[j], film.box_h(j) * sc[j]):
            ymax = max(ymax, y + 6)       # + glow radius
check("F1 151.5-160 s: all content y <= 700", ymax <= 700, max_y_px=round(ymax, 1))
# G1 no overlap > 10 % at 149.75-150.25 s (the house opening)
wo = max_overlap_window(149.75, 150.25)
check("G1 149.75-150.25 s: max box overlap <= 10 %", wo[0] <= 0.10, max_overlap=round(wo[0], 4), pair=wo[1], frame=wo[2])

# ===== critic round 3 =====
# H1 the making section (73-110 s, every 0.25 s): no overlap > 10 %, no box in a label area, >= 8 px from every edge
film.TEXT_LOG = []
worst, pair_w, edge_min, label_hits = 0.0, None, 1e9, []
for q in range(int(73 * 4), int(110 * 4) + 1):
    t_ = q / 4.0; f = int(round(t_ * 24)); b = fb(f)
    film.TEXT_LOG.clear(); film.render_frame(f)
    rects = [(x0 - 4, y0 - 4, x1 + 4, y1 + 4) for (_, x0, y0, x1, y1) in film.TEXT_LOG]
    P, r, sc, gl, face = film.state(b)
    ws = [film.box_w(j, b) * sc[j] for j in range(20)]; hs = [film.box_h(j) * sc[j] for j in range(20)]
    w, pr = geom.max_overlap(P, r, ws, hs)
    if w > worst: worst, pair_w = w, (pr, round(t_, 2))
    for j in range(20):
        cs = film.corners(P[j], r[j], ws[j], hs[j])
        xs, ys = [c[0] for c in cs], [c[1] for c in cs]
        edge_min = min(edge_min, min(xs), min(ys), 1280 - max(xs), 720 - max(ys))
        for (a0, b0, a1, b1) in rects:
            if min(xs) < a1 and max(xs) > a0 and min(ys) < b1 and max(ys) > b0: label_hits.append((j, t_))
film.TEXT_LOG = None
check("H1a making 73-110 s: max box overlap <= 10 %", worst <= 0.10, max_overlap=round(worst, 4), at=pair_w)
check("H1b making 73-110 s: no box enters a label / card area", not label_hits, hits=label_hits[:5])
check("H1c making 73-110 s: every box >= 8 px from the frame edges", edge_min >= 8, min_edge_px=round(edge_min, 1))
# H2 film-wide: boxes stay >= 8 px inside the side and bottom edges (the scripted exits through the top edge
#    - un-making b32-48, lift and rain b348-368 - are exempt from the top-edge rule only)
emin, where = 1e9, None
for q in range(int(16 * 4 / 1), int(film.DUR * 4)):
    t_ = q / 4.0; b = fb(int(round(t_ * 24)))
    if b < 16: continue
    P, r, sc, gl, face = film.state(b)
    for j in range(20):
        if face[j] <= 0.01: continue
        cs = film.corners(P[j], r[j], film.box_w(j, b) * sc[j], film.box_h(j) * sc[j])
        xs, ys = [c[0] for c in cs], [c[1] for c in cs]
        if max(ys) < 0: continue                       # fully off the top: scripted exit
        top_exempt = (32 <= b < 48) or (348 <= b < 368)
        d = min(min(xs), 1280 - max(xs), 720 - max(ys), 1e9 if top_exempt else min(ys))
        if d < emin: emin, where = d, (j, round(t_, 2))
check("H2 film-wide: boxes >= 8 px inside the side / bottom edges (top too, except scripted exits)", emin >= 8, min_edge_px=round(emin, 1), at=where)
# H3 the BEAM 7 tag and the footer are >= 12 px tall at 360 px width
a_ = film.assets()
beam_label_px = a_["box"][film.BEAM].img.getbbox()   # sprite size; the numeral is measured below
fb7 = film.font(film.FONT_STENCIL, 56 * 1.12).getbbox("7"); ffoot = a_["f_cap"].getbbox("BOXBACK")
check("H3 beam numeral and footer >= 12 px tall at 360 px", min(fb7[3] - fb7[1], ffoot[3] - ffoot[1]) * 360 / 1280 >= 12,
      beam_7_px=round((fb7[3] - fb7[1]) * 360 / 1280, 1), footer_px=round((ffoot[3] - ffoot[1]) * 360 / 1280, 1))

# ===== critic round 4 =====
def frame_px(f): return np.asarray(film.render_frame(f), np.int16)
# M1 after 140 s no 4 s window moves more than the 3:2 peak (132-136 s): mean |frame - previous frame|
def motion(t0, t1, step=3):
    v = []
    for f in range(int(t0 * 24), int(t1 * 24) - 1, step):
        v.append(float(np.abs(frame_px(f + 1) - frame_px(f)).mean()))
    return float(np.mean(v))
peak = motion(132, 136)
wins = {f"{a}-{a + 4}": round(motion(a, min(a + 4, 171.0)), 3) for a in range(140, 172, 4)}
check("M1 every 4 s window after 140 s moves less than the 132-136 s peak", max(wins.values()) < peak, peak_132_136=round(peak, 3), windows=wins)
# M2 rendered pixels: nothing lit (max channel > 40) within 8 px of any edge after 7.5 s
hits = []
for f in range(int(7.5 * 24), int((film.DUR - 2.5) * 24), 4):
    im = np.asarray(film.render_frame(f)).max(2) > 40
    border = np.concatenate([im[:8].ravel(), im[-8:].ravel(), im[:, :8].ravel(), im[:, -8:].ravel()])
    if border.any(): hits.append(round(f / 24, 2))
check("M2 rendered pixels: no lit pixel within 8 px of an edge after 7.5 s (every 4th frame)", not hits, frames_checked=len(range(int(7.5 * 24), int((film.DUR - 2.5) * 24), 4)), hits=hits[:10])
# M3 the conveyor is a loop AROUND the stack: lane boxes never closer than 8 px to any landed box (73-110 s)
gap = 1e9
for q in range(int(73 * 4), int(110 * 4) + 1):
    b = fb(int(round(q / 4 * 24)))
    if b < 164: continue
    P, r, sc, gl, face = film.state(b)
    landed = [j for k, j in enumerate(film.MAKE_ORDER) if b >= film.land_beat(k)]
    lane = [j for k, j in enumerate(film.MAKE_ORDER) if b < film.land_beat(k) - 2] + ([film.BEAM] if b < 240 else [])
    for i in lane:
        for j in landed:
            dx = abs(P[i][0] - P[j][0]) - (film.box_w(i, b) + film.box_w(j, b)) / 2
            dy = abs(P[i][1] - P[j][1]) - (film.box_h(i) + film.box_h(j)) / 2
            gap = min(gap, max(dx, dy))
check("M3 conveyor loop stays >= 8 px clear of the stack", gap >= 8, min_gap_px=round(gap, 1))

# ===== critic round 5: motion shape, measured on the RENDERED mp4 (greyscale mean |frame - previous|) =====
import motion_mp4 as MM
MP4 = os.path.join(HERE, "..", "the-universal-boxback.mp4")
if os.path.exists(MP4):
    d_ = MM.per_frame(MP4); w4 = MM.windows(d_, 4); w1 = MM.windows(d_, 1)
    acc_peak = max(w4[30:35])                        # 120-140 s windows
    outside = {f"{4*k}-{4*k+4}": v for k, v in enumerate(w4) if not (30 <= k <= 34)}
    check("K1 (mp4) every 4 s window outside 122-140 s is below the accumulation peak", max(outside.values()) < acc_peak,
          accumulation_peak=acc_peak, max_outside=max(outside.values()), at=max(outside, key=outside.get), windows_4s=w4)
    rel = w1[151:162]
    check("K2 (mp4) release 151-161 s: strictly decreasing 1 s motion, last <= 50 % of the first", all(b_ < a_ for a_, b_ in zip(rel, rel[1:])) and rel[-1] <= 0.5 * rel[0],
          windows_1s_151_161=rel)
json.dump({"film": "the-universal-boxback", "revision": "r6", "grid": film.G, "results": R, "all_pass": all(r["pass"] for r in R)},
          open(os.path.join(HERE, "invariants.json"), "w"), indent=1, default=str)
sys.exit(0 if all(r["pass"] for r in R) else 1)
