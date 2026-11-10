// node orchestra_capture.js <cast.json> <outdir> <t0> <t1> <fps> [formation] [hue]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [castP, out, t0s, t1s, fpsS, form, hue] = process.argv.slice(2); const C = JSON.parse(fs.readFileSync(castP)); const fps = +fpsS, t0 = +t0s, t1 = +t1s;
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('http://localhost:8766/moto/scion/jelly-cuts/src/orchestra.html'); await p.waitForFunction(() => window.__ready, null, { timeout: 60000 });
  const cast = await p.evaluate(([C, o]) => window.__init(C, o), [C, { formation: form === undefined ? 3 : +form, hue: hue === undefined ? .07 : +hue }]);
  fs.writeFileSync(out + '/cast_members.json', JSON.stringify(cast));
  // warm-up so jellies rise into formation deterministically from t0-4s
  for (let t = Math.max(0, t0 - 4); t < t0; t += 1 / fps) await p.evaluate(t => { window.__step(t); return 0; }, t);
  const meta = []; const tic = Date.now(); let n = 0;
  for (let f = Math.round(t0 * fps); f < Math.round(t1 * fps); f++) {
    const r = await p.evaluate(t => window.__step(t), f / fps);
    fs.writeFileSync(`${out}/o${String(f).padStart(5, '0')}.jpg`, Buffer.from(r.img.split(',')[1], 'base64'));
    meta.push({ f, jel: r.jel, lead: r.lead, shot: r.shot }); n++;
    if (n % 120 === 0) console.log('frame', f, ((Date.now() - tic) / n).toFixed(0), 'ms/frame');
  }
  fs.writeFileSync(`${out}/meta_${Math.round(t0 * fps)}.json`, JSON.stringify(meta));
  console.log('done', n, 'frames', errs.slice(0, 5)); await b.close();
})();
