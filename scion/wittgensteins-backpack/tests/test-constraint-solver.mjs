// node tests/test-constraint-solver.mjs  — same invariants as tests/test_constraints.py, against the browser solver.
import { createRequire } from "module"; const require = createRequire(import.meta.url);
const S = require("../constraint-solver.js");
const PEL = [500, 520], PN = [520, 698], PF = [470, 698]; let fails = 0;
const check = (name, ok, d) => { console.log((ok ? "PASS " : "FAIL ") + name, JSON.stringify(d)); if (!ok) fails++; };
for (const t of [[600, 380], [620, 420], [585, 350], [640, 440], [560, 470]]) {
  const r = S.solveReach(PEL, PN, PF, t).residuals;
  check(`reachable ${t}`, r.length_max < 1e-6 && r.pin_n < 1e-6 && r.pin_f < 1e-6 && r.attach < 0.5, r);
}
for (const t of [[900, 300], [500, 100]]) { const b = S.solveReach(PEL, PN, PF, t);
  check(`unreachable ${t}`, !b.solvable && b.residuals.length_max < 1e-6 && b.residuals.pin_n < 1e-6, { attach: b.residuals.attach.toFixed(2) }); }
let prev = null, worst = 0;
for (let i = 0; i < 90; i++) { const b = S.solveReach(PEL, PN, PF, [560 + i, 470 - 0.8 * i], { prev, maxLean: 30 });
  if (prev) for (const k of ["pelvis", "neck", "shoulder", "elbow", "hand", "knee_n", "knee_f"]) worst = Math.max(worst, Math.hypot(b[k][0] - prev[k][0], b[k][1] - prev[k][1]));
  prev = b; }
check("stability under 1px drags", worst < 6, { max_joint_jump_px: +worst.toFixed(3) });
process.exit(fails ? 1 : 0);
