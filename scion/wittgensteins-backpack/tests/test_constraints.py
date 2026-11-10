"""Numeric invariants for the Sutherland constraint layer. Run: python3 -I tests/test_constraints.py"""
import sys, os, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from constraints import solve_reach, REST

PEL = (500.0, 520.0); PN = (520.0, 698.0); PF = (470.0, 698.0)
results = []

def check(name, ok, detail):
    results.append({"test": name, "pass": bool(ok), "detail": detail}); print(("PASS " if ok else "FAIL ") + name, detail)

# 1 reachable targets: exact lengths, exact pins, attach < 0.5 px
reach_targets = [(600, 380), (620, 420), (585, 350), (640, 440), (560, 470)]
for t in reach_targets:
    b = solve_reach(PEL, PN, PF, t)
    r = b["residuals"]
    check(f"reachable {t}", r["length_max"] < 1e-6 and r["pin_n"] < 1e-6 and r["pin_f"] < 1e-6 and r["attach"] < 0.5,
          {"len": round(r["length_max"], 9), "pins": round(max(r["pin_n"], r["pin_f"]), 9), "attach": round(r["attach"], 4)})

# 2 unreachable: flagged unsolvable, lengths & pins still exact (no teleport / stretch)
for t in [(900, 300), (500, 100)]:
    b = solve_reach(PEL, PN, PF, t)
    r = b["residuals"]
    check(f"unreachable {t} flagged", (not b["solvable"]) and r["length_max"] < 1e-6 and r["pin_n"] < 1e-6,
          {"attach_residual": round(r["attach"], 2), "solvable": b["solvable"]})

# 3 stability: 1 px pointer moves never jump any joint more than 6 px
prev = None; worst = 0; t0 = (560.0, 470.0)
path = [(t0[0] + i * 1.0, t0[1] - i * 0.8) for i in range(90)]
for t in path:
    b = solve_reach(PEL, PN, PF, t, prev=prev)
    if prev:
        for k in ("pelvis", "neck", "shoulder", "elbow", "hand", "knee_n", "knee_f"):
            worst = max(worst, math.dist(b[k], prev[k]))
    prev = b
check("stability under 1px drags", worst < 6.0, {"max_joint_jump_px": round(worst, 3)})

# 4 believable elbow: below shoulder->hand line for forward reaches
bad = 0
for t in reach_targets:
    b = solve_reach(PEL, PN, PF, t)
    s, h, e = b["shoulder"], b["hand"], b["elbow"]
    cross = (h[0] - s[0]) * (e[1] - s[1]) - (h[1] - s[1]) * (e[0] - s[0])
    bad += cross <= 0
check("elbow below shoulder-hand line", bad == 0, {"violations": bad})

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "constraint-tests.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump({"suite": "constraints", "results": results, "all_pass": all(r["pass"] for r in results)}, open(out, "w"), indent=1)
sys.exit(0 if all(r["pass"] for r in results) else 1)
