// node orchestra_capture.js <cast.json> <outdir> <t0> <t1> <fps> [formation] [hue]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [castP, out, t0s, t1s, fpsS, form, hue] = process.argv.slice(2); const C = JSON.parse(fs.readFileSync(castP)); const fps = +fpsS, t0 = +t0s, t1 = +t1s;
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('http://localhost:8766/moto/scion/jelly-cuts/src/' + (process.env.PAGE || 'orchestra.html')); await p.waitForFunction(() => window.__ready, null, { timeout: 60000 });
  const cast = await p.evaluate(([C, o]) => { if (o.shots) window.__SHOTSEQ = o.shots; return window.__init(C, o); }, [C, { formation: form === undefined ? 3 : +form, hue: hue === undefined ? .07 : +hue, shots: process.env.SHOTS ? JSON.parse(process.env.SHOTS) : null, spec: process.env.SPEC || null, bank: process.env.BANK || null, full: process.env.FULL || null, ...(process.env.DIRECT ? JSON.parse(fs.readFileSync(process.env.DIRECT)) : {}) }]);
  fs.writeFileSync(out + '/cast_members.json', JSON.stringify(cast));
  // warm-up so jellies rise into formation deterministically from t0-4s
  for (let t = Math.max(0, t0 - 4); t < t0; t += 1 / fps) await p.evaluate(t => { window.__step(t); return 0; }, t);
  for (let k = 0; k < 6; k++) await p.evaluate(t => { window.__step(t); return 0; }, t0);   // settle locks and the camera at t0
  const meta = []; const tic = Date.now(); let n = 0;
  for (let f = Math.round(t0 * fps); f < Math.round(t1 * fps); f++) {
    const r = await p.evaluate(t => window.__step(t), f / fps);
    if (process.env.MASKS) { const mk = await p.evaluate(([t, every]) => { const S = window.__SPEC; if (!S) return null; const f = Math.round(t * 24); for (const F of S.films) { const [b0, b1] = F.bloom; if (b1 > b0 && t >= b0 && t <= b1 && f % every === 0) { const o = {film: F.id, holder: F.by, ...window.__masks(F.by, F.id)}; const L = S.films.find(x => x.letgo && t >= x.letgo - .3 && t <= x.letgo_end + .3); if (L) o.mlet = window.__masks(L.by, L.id).mfilm; return o; } } return null; }, [f / fps, +process.env.MASKS]); if (mk) { fs.writeFileSync(`${out}/mh${String(f).padStart(5, '0')}.png`, Buffer.from(mk.mhold.split(',')[1], 'base64')); if (mk.mfilm) fs.writeFileSync(`${out}/mf${String(f).padStart(5, '0')}.png`, Buffer.from(mk.mfilm.split(',')[1], 'base64')); if (mk.mlet) fs.writeFileSync(`${out}/mp${String(f).padStart(5, '0')}.png`, Buffer.from(mk.mlet.split(',')[1], 'base64')); r.mask = mk.film; } }
    fs.writeFileSync(`${out}/o${String(f).padStart(5, '0')}.jpg`, Buffer.from(r.img.split(',')[1], 'base64'));
    meta.push({ f, jel: r.jel, lead: r.lead, shot: r.shot }); n++;
    if (n % 120 === 0) console.log('frame', f, ((Date.now() - tic) / n).toFixed(0), 'ms/frame');
  }
  fs.writeFileSync(`${out}/meta_${Math.round(t0 * fps)}.json`, JSON.stringify(meta));
  console.log('done', n, 'frames', errs.slice(0, 5)); await b.close();
})();
