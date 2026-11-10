// SCION-SUTHERLAND constraint solver (port of src/constraints.py). Works in the browser (window.Sketch) and Node (module.exports).
(function (root) {
  const REST = { torso: 150, shOff: [6, -138], upper: 70, fore: 66, thigh: 90, shin: 88 };
  const len = (v) => Math.hypot(v[0], v[1]);
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
  const add = (a, b) => [a[0] + b[0], a[1] + b[1]];
  const rot = (v, d) => { const t = d * Math.PI / 180; return [v[0] * Math.cos(t) - v[1] * Math.sin(t), v[0] * Math.sin(t) + v[1] * Math.cos(t)]; };
  function twoBone(rootP, target, a, b, bend) {
    const d = sub(target, rootP), L = len(d);
    const reach = L <= a + b + 1e-9 && L >= Math.abs(a - b) - 1e-9;
    const Lc = Math.min(Math.max(L, Math.abs(a - b) + 1e-6), a + b - 1e-6);
    const base = L > 1e-9 ? Math.atan2(d[1], d[0]) : 0;
    const c = Math.max(-1, Math.min(1, (a * a + Lc * Lc - b * b) / (2 * a * Lc)));
    const ang = base + bend * Math.acos(c);
    const joint = [rootP[0] + a * Math.cos(ang), rootP[1] + a * Math.sin(ang)];
    const tip = [rootP[0] + Lc * Math.cos(base), rootP[1] + Lc * Math.sin(base)];
    const dj = sub(tip, joint), k = b / Math.max(len(dj), 1e-9);
    return { joint, end: [joint[0] + dj[0] * k, joint[1] + dj[1] * k], reach };
  }
  function bodyFrom(pelvis, lean, pn, pf, target, face = 1, pref = null) {
    const neck = add(pelvis, rot([0, -REST.torso], lean));
    const shoulder = add(pelvis, rot([REST.shOff[0] * face, REST.shOff[1]], lean));
    const kb = -face;
    const ln = twoBone(pelvis, pn, REST.thigh, REST.shin, kb), lf = twoBone(pelvis, pf, REST.thigh, REST.shin, kb);
    let best = null;
    for (const bend of (pref ? [pref] : [1, -1])) {
      const arm = twoBone(shoulder, target, REST.upper, REST.fore, bend);
      const cross = (arm.end[0] - shoulder[0]) * (arm.joint[1] - shoulder[1]) - (arm.end[1] - shoulder[1]) * (arm.joint[0] - shoulder[0]);
      const score = cross * face > 0 ? 0 : 1;
      if (!best || score < best.score) best = { score, arm, bend };
    }
    return { pelvis, neck, shoulder, hip: pelvis, knee_n: ln.joint, ankle_n: ln.end, knee_f: lf.joint, ankle_f: lf.end,
      elbow: best.arm.joint, hand: best.arm.end, elbow_bend: best.bend, lean };
  }
  function residuals(b, pn, pf, target) {
    const L = (p, q) => len(sub(p, q));
    const lens = [Math.abs(L(b.pelvis, b.neck) - REST.torso), Math.abs(L(b.shoulder, b.elbow) - REST.upper), Math.abs(L(b.elbow, b.hand) - REST.fore),
      Math.abs(L(b.hip, b.knee_n) - REST.thigh), Math.abs(L(b.knee_n, b.ankle_n) - REST.shin), Math.abs(L(b.hip, b.knee_f) - REST.thigh), Math.abs(L(b.knee_f, b.ankle_f) - REST.shin)];
    return { length_max: Math.max(...lens), pin_n: L(b.ankle_n, pn), pin_f: L(b.ankle_f, pf), attach: L(b.hand, target) };
  }
  function solveReach(restPelvis, pn, pf, target, opts = {}) {
    const face = opts.face || 1, maxShift = opts.maxShift ?? 34, maxLean = opts.maxLean ?? 22, steps = 17, prev = opts.prev;
    const lim = REST.thigh + REST.shin - 0.5;
    const okPel = (p) => p[1] >= restPelvis[1] - 1e-6 && len(sub(pn, p)) <= lim && len(sub(pf, p)) <= lim && Math.abs(p[0] - restPelvis[0]) <= maxShift + 1e-9;
    function refine(b, res) {
      let pel = b.pelvis, lean = b.lean, step = 2;
      for (let it = 0; it < 60 && res >= 1e-3; it++) {
        let improved = false;
        for (const [dx, dy, dl] of [[step, 0, 0], [-step, 0, 0], [0, step, 0], [0, -step, 0], [0, 0, step], [0, 0, -step]]) {
          const p2 = [pel[0] + dx, pel[1] + dy], l2 = Math.max(-maxLean, Math.min(maxLean, lean + dl));
          if (!okPel(p2)) continue;
          const b2 = bodyFrom(p2, l2, pn, pf, target, face, b.elbow_bend), r2 = len(sub(b2.hand, target));
          if (r2 < res - 1e-6) { b = b2; res = r2; pel = p2; lean = l2; improved = true; }
        }
        if (!improved) { step *= 0.5; if (step < 0.01) break; }
      }
      return [b, res];
    }
    let b = null, res;
    if (prev) { const b0 = bodyFrom(prev.pelvis, prev.lean, pn, pf, target, face, prev.elbow_bend); [b, res] = refine(b0, len(sub(b0.hand, target))); if (res > 0.5) b = null; }
    if (!b) {
      let best = null;
      for (let i = 0; i < steps; i++) { const dx = -maxShift + 2 * maxShift * i / (steps - 1);
        for (const dy of [0, 8, 16, 26]) { const pel = [restPelvis[0] + dx, restPelvis[1] + dy]; if (!okPel(pel)) continue;
          for (let j = 0; j < steps; j++) { const lean = -maxLean + 2 * maxLean * j / (steps - 1);
            const bb = bodyFrom(pel, lean, pn, pf, target, face), r = len(sub(bb.hand, target));
            const cost = r * 10 + 0.002 * (dx * dx + 2 * dy * dy) + 0.004 * lean * lean;
            if (!best || cost < best[0]) best = [cost, bb, r]; } } }
      if (!best) return null;
      [b, res] = refine(best[1], best[2]);
    }
    b.residuals = residuals(b, pn, pf, target); b.solvable = b.residuals.attach < 0.5;
    return b;
  }
  const api = { REST, solveReach, twoBone, residuals };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.Sketch = api;
})(typeof window !== "undefined" ? window : globalThis);
