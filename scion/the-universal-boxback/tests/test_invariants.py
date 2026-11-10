"""Numeric invariants for THE UNIVERSAL BOXBACK. Run: python3 -I tests/test_invariants.py -> tests/invariants.json"""
import sys, os, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "src"))
import film
R = []
def check(name, ok, **d): R.append({"test": name, "pass": bool(ok), **d}); print(("PASS " if ok else "FAIL ") + name, d)
ang = lambda P, j: math.atan2((P[j][1] - film.CY) / 0.80, P[j][0] - film.CX)

# 1. the 3:2 phase relation, measured from trajectories (unwrapped angle of every A and B box)
bs = np.arange(52, 72.0001, 0.01)
th = np.array([[ang(film.ring(b)[0], j) for j in range(20)] for b in bs])
laps = (np.unwrap(th, axis=0)[-1] - np.unwrap(th, axis=0)[0]) / (2 * math.pi)
ratio = laps[:10].mean() / laps[10:].mean()
check("proof phase ratio A:B = 3:2", abs(ratio - 1.5) < 0.01, measured=round(float(ratio), 5), laps_A=round(float(laps[:10].mean()), 4), laps_B=round(float(laps[10:].mean()), 4))

# 2. reunion: at b52 and b72 every A_i shares its angle with B_i
for b in (52, 72):
    P = film.ring(b)[0]
    e = max(abs((ang(P, i) - ang(P, i + 10) + math.pi) % (2 * math.pi) - math.pi) for i in range(10))
    check(f"reunion at b{b}", e < 1e-9, max_angle_err_rad=e)

# 3. interference: at b52+2m, A_i aligns with B_(i+m) (nine passes, one every 2 beats)
worst = 0
for m in range(1, 10):
    P = film.ring(52 + 2 * m)[0]
    worst = max(worst, max(abs((ang(P, i) - ang(P, (i + m) % 10 + 10) + math.pi) % (2 * math.pi) - math.pi) for i in range(10)))
check("nine interference passes on even beats", worst < 1e-9, max_angle_err_rad=worst)

# 4. no accidental collisions in the proof: non-pair boxes never closer than 60 px (box height 56)
w = 1e9
for b in np.arange(52, 72.0001, 0.01):
    P = film.ring(b)[0]
    for i in range(20):
        for j in range(i + 1, 20):
            if j != i + 10: w = min(w, math.dist(P[i], P[j]))
check("proof: non-pair separation >= 60 px", w >= 60, min_px=round(w, 2))

# 5. rational lock closes every 16 beats; detuned drift does not
e_lock = float(np.abs(film.bank(84, 0.0, 0.85) - film.bank(100, 0.0, 0.85)).max())
e_drift = float(np.abs(film.bank(116, 0.06, 0.85) - film.bank(132, 0.06, 0.85)).max())
check("rational lock closes (16-beat period)", e_lock < 1e-6, max_err_px=e_lock)
check("detuned drift does not close", e_drift > 20, max_err_px=round(e_drift, 1))

# 6. Plato test: the beam never seats in the occupied row before the re-phase; afterwards every box is in plan F
bad = [b for b in np.arange(242.5, 262, 0.05) if math.dist(film.state(b)[0][film.BEAM], film.SLOT_P0[film.BEAM]) < 60]
check("beam refused by row 3 until the re-phase", not bad, frames_in_row=len(bad))
P = film.state(264.5)[0]
check("after the re-phase the house is plan F", float(np.abs(P - film.F_ARR).max()) < 3.5, max_err_px=round(float(np.abs(P - film.F_ARR).max()), 3))

# 7. the end returns to the beginning: last downbeat b368 == opening end form (b20), within 0.5 px
e_end = float(np.abs(film.state(368.0)[0] - film.state(20.0)[0]).max())
check("final house == opening end form (eps 0.5 px)", e_end < 0.5, max_err_px=e_end)

# 8. making order: each box lands on its own beat, foundation (rows 1-2) before roof
lands = {j: film.land_beat(k) for k, j in enumerate(film.MAKE_ORDER)}
ok = all(lands[j] < lands[k] for j in film.MAKE_ORDER for k in film.MAKE_ORDER if film.SLOT_P0[j][1] > film.SLOT_P0[k][1])
check("making starts at the first step (lower rows land first)", ok)

json.dump({"film": "the-universal-boxback", "grid": film.G, "results": R, "all_pass": all(r["pass"] for r in R)},
          open(os.path.join(HERE, "invariants.json"), "w"), indent=1)
sys.exit(0 if all(r["pass"] for r in R) else 1)
