"""Numeric invariants for THE UNIVERSAL BOXBACK (r2). Run: python3 -I tests/test_invariants.py -> tests/invariants.json
All values come from the closed-form trajectories the renderer draws, except T4 (rendered pixels)."""
import sys, os, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "src"))
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

json.dump({"film": "the-universal-boxback", "revision": "r2", "grid": film.G, "results": R, "all_pass": all(r["pass"] for r in R)},
          open(os.path.join(HERE, "invariants.json"), "w"), indent=1, default=str)
sys.exit(0 if all(r["pass"] for r in R) else 1)
