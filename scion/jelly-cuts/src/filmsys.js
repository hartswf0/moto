// FILMS INSIDE THE WATER (r4). Flecks in transit only (the user's call): a memory travels and condenses as halftone
// flecks under the WYGWYL dot law, and at its BLOOM it resolves to the full-resolution picture (the law deliberately
// suspended at the peak so the archive is recognisable). Each memory hangs below its holder on visible strands, is fogged
// and occluded by the same water; the camera is solved per bloom to frame the holder's whole body and the picture.
// The Afterlight Medusa is the character: red, larger, with twelve thick memory tentacles; one turns silver for every
// memory it has let go.
export function makeFilmSys(THREE, scene, cam, SONG, SPEC, BANK, bins, FULL) {
  const B8 = [[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],[15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]];
  const ease = u => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };
  const dotTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 32; const x = c.getContext('2d'); x.fillStyle = '#fff'; x.beginPath(); x.arc(16, 16, 14, 0, Math.PI * 2); x.fill(); return new THREE.CanvasTexture(c); })();
  const INK = new THREE.Color('#f3e6c8').multiplyScalar(1.75), WATER = new THREE.Color('#0e1211');
  const J = k => SONG.J.find(j => j.k === k);
  // ---- the character: red, 1.7x, twelve thick memory tentacles
  const hero = J(SPEC.hero.k); hero.sz *= SPEC.hero.scale; hero.rig.group.scale.multiplyScalar(SPEC.hero.scale);
  hero.root.traverse(o => { const m = o.material; if (m && m.uniforms) { if (m.uniforms.uBellColor) m.uniforms.uBellColor.value = new THREE.Color(SPEC.hero.bell); if (m.uniforms.uRimColor) m.uniforms.uRimColor.value = new THREE.Color(SPEC.hero.rim); } });
  const tents = [], TL = .75, TR = .045;
  for (let i = 0; i < 12; i++) { const pts = []; for (let q = 0; q <= 10; q++) pts.push(new THREE.Vector3(Math.sin(q * .6 + i) * .06, -q / 10 * TL, 0));
    const mesh = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 20, TR, 6, false), new THREE.MeshBasicMaterial({color: 0x6a2a20, fog: true})); scene.add(mesh); tents.push(mesh); }
  // ---- films
  const films = SPEC.films.map((f, fi) => {
    const m = BANK[f.bank], gw = m.gw, gh = m.gh, N = gw * gh, data = bins[f.bank];
    const geo = new THREE.BufferGeometry(), pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const pts = new THREE.Points(geo, new THREE.PointsMaterial({size: .05, map: dotTex, alphaTest: .5, vertexColors: true, sizeAttenuation: true, fog: true})); pts.frustumCulled = false;
    const H = f.width * gh / gw, back = new THREE.Mesh(new THREE.PlaneGeometry(f.width * 1.02, H * 1.02), new THREE.MeshBasicMaterial({color: WATER, fog: true}));
    const fullCanvas = document.createElement('canvas'), FI = FULL[f.id]; fullCanvas.width = FI.w; fullCanvas.height = FI.h; const tex = new THREE.CanvasTexture(fullCanvas); tex.colorSpace = THREE.SRGBColorSpace;
    const pic = new THREE.Mesh(new THREE.PlaneGeometry(f.width, H), new THREE.MeshBasicMaterial({map: tex, transparent: true, opacity: 0, fog: false, toneMapped: false, depthWrite: false}));
    const g = new THREE.Group(); g.add(back); g.add(pts); g.add(pic); pic.position.z = .04; scene.add(g); g.visible = false;
    const strands = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({color: 0xf0c48a, fog: true, side: THREE.DoubleSide})); strands.frustumCulled = false; scene.add(strands);
    const th = new Float32Array(N), r1 = new Float32Array(N), r2 = new Float32Array(N);
    for (let y = 0, i = 0; y < gh; y++) for (let x = 0; x < gw; x++, i++) { th[i] = B8[((y >> 1) + fi) % 8][((x >> 1) + 3 * fi) % 8] / 64 * .92 + .04; const s = Math.sin(x * 12.9898 + y * 78.233 + fi * 37.7) * 43758.5453; r1[i] = s - Math.floor(s); const s2 = Math.sin(x * 22.1 + y * 41.7 + fi * 9.1) * 24634.6345; r2[i] = s2 - Math.floor(s2); }
    return {f, gw, gh, N, data, pos, col, geo, pts, back, pic, tex, fullCanvas, imgs: FI.imgs, g, H, strands, th, r1, r2, n: m.n, lastImg: -1};
  });
  const _r = new THREE.Vector3(), _u = new THREE.Vector3(), _fw = new THREE.Vector3(), CPOS = new THREE.Vector3(), CLOOK = new THREE.Vector3();
  const condOf = (f, t) => { const [c0, c1] = f.condense; let c = t >= c0 ? ease((t - c0) / Math.max(.01, c1 - c0)) : -1; if (t > f.release && !f.keep) c = 1 - ease((t - f.release) / 2.0) * 1.3; return c; };
  const resOf = (f, t) => { const [b0, b1] = f.bloom; let w = b1 > b0 ? ease((t - b0) / .7) * (1 - ease((t - b1 + .7) / .7)) : 0;
    if (f.keep && t >= f.keep.t0) w = t < f.letgo ? Math.max(w, ease((t - f.keep.t0) / .4)) : 1 - Math.min(1, (t - f.letgo) / (f.letgo_end - f.letgo - .2)); return w; };
  function widthOf(f, t) { if (f.keep && t >= f.keep.t0 - .8) { const u = ease((t - f.keep.t0 + .8) / .8); return f.width + (f.keep.width - f.width) * u; } return f.width; }
  function anchor(F, t) {
    const j = J(F.f.by), bellR = j.sz * .95 * (j.root.scale.x || 1);
    cam.getWorldDirection(_fw); _r.crossVectors(_fw, cam.up).normalize(); _u.crossVectors(_r, _fw).normalize();
    const w = widthOf(F.f, t), h = F.H * w / F.f.width, gap = F.f.gap ?? .6;
    let c = j.pos.clone().addScaledVector(_u, -(bellR * .55 + gap + h / 2));
    if (F.f.keep && t >= F.f.keep.t0 - .8) { const u = ease((t - F.f.keep.t0 + .8) / .8); c.addScaledVector(_r, F.f.keep.dx * u).addScaledVector(_u, (F.f.keep.dy || 0) * u); }
    return {j, bellR, c, r: _r.clone(), u: _u.clone(), w, h};
  }
  function update(t) {
    // the hero's memory tentacles: silver for every memory let go, swaying with the pulse
    const lit = SPEC.films.filter(f => f.by === SPEC.hero.k && t > (f.letgo_end ?? f.release) + .2).length;
    { cam.getWorldDirection(_fw); _r.crossVectors(_fw, cam.up).normalize(); _u.crossVectors(_r, _fw).normalize(); const bR = hero.sz * .95 * (hero.root.scale.x || 1);
      tents.forEach((m, i) => { const ang = (-75 + i * (150 / 11)) * Math.PI / 180;   // a crown of twelve, counted left to right, pointing out of the top of the bell
        m.position.copy(hero.pos).addScaledVector(_r, Math.sin(ang) * bR * .92).addScaledVector(_u, Math.cos(ang) * bR * .92); m.quaternion.copy(cam.quaternion); m.rotateZ(Math.PI - ang + Math.sin(t * 1.4 + i) * .05);
        m.material.color.set(i < lit ? 0xd8f0ff : 0x5a221a); m.visible = true; }); }
    // camera framing solve for the active bloom
    let wcam = 0, best = null;
    for (const F of films) { const [b0, b1] = F.f.bloom; if (b1 <= b0) continue; const w = ease((t - b0 + 1.0) / 1.0) * (1 - ease((t - b1) / 1.0)); if (w > wcam) { wcam = w; best = F; } }
    if (best && wcam > 0) {
      const A = anchor(best, t), tl = TL * (A.j === hero ? 1 : .6) * (A.j.root.scale.x || 1);
      let uTop = A.c.distanceTo(A.j.pos) + A.bellR * 1.12 + (A.j === hero ? TL * 1.1 : 0), uBot = -A.h / 2, half = A.w / 2 + (best.f.extra_half || 0); uBot -= (uTop - uBot) * .19;   // keep the caption band clear
      const top = A.c.clone().addScaledVector(A.u, uTop), bot = A.c.clone().addScaledVector(A.u, uBot);
      const T = top.clone().add(bot).multiplyScalar(.5).addScaledVector(A.r, (best.f.extra_half || 0) * .5), hgt = (uTop - uBot) * (best.f.frame ?? 1.02), wid = half * 2 * 1.1;
      const tf = Math.tan(cam.fov * Math.PI / 360), D = Math.max(hgt / (2 * tf), wid / (2 * tf * cam.aspect));
      const dir = cam.position.clone().sub(T); dir.y *= .35; dir.normalize(); CPOS.copy(T).addScaledVector(dir, D); CLOOK.copy(T);
      const P0 = cam.position.clone(), L0 = cam.position.clone().add(cam.getWorldDirection(new THREE.Vector3()).multiplyScalar(10));
      cam.position.lerpVectors(P0, CPOS, wcam); cam.lookAt(L0.lerp(CLOOK, wcam)); cam.updateMatrixWorld();
    }
    for (const F of films) {
      const f = F.f, live = t >= f.t[0] && t <= f.t[1]; F.g.visible = live; F.strands.visible = false; if (!live) continue;
      const c = condOf(f, t), wR = resOf(f, t), A = anchor(F, t), sc = A.w / f.width;
      F.g.position.copy(A.c); F.g.quaternion.copy(cam.quaternion); F.g.scale.setScalar(sc);
      // full-resolution picture at the bloom
      if (wR > .005) { const k = Math.min(F.imgs.length - 1, Math.max(0, Math.floor((t - f.full_t0) * 12))); if (k !== F.lastImg) { F.fullCanvas.getContext('2d').drawImage(F.imgs[k], 0, 0, F.fullCanvas.width, F.fullCanvas.height); F.tex.needsUpdate = true; F.lastImg = k; } }
      F.pic.material.opacity = wR; F.pic.visible = wR > .005;
      // the flecks (in transit), hidden under a resolved picture
      const fi = Math.min(F.n - 1, Math.max(0, Math.floor((t - f.t[0]) * 12))), base = fi * F.N, d = F.data, W = f.width, Hh = F.H, scat = f.scatter ?? 2.8;
      let lk = 0, tgt = null;
      if (f.letgo && t > f.letgo) { lk = (t - f.letgo) / (f.letgo_end - f.letgo); const G = films.find(x => x.f.id === f.release_to); if (G && G.g.visible) { G.g.updateMatrixWorld(); tgt = new THREE.Vector3((f.target[0] - .5) * G.f.width, (.5 - f.target[1]) * G.H, .08).applyMatrix4(G.g.matrixWorld); F.g.updateMatrixWorld(); tgt = F.g.worldToLocal(tgt); } }
      const dotsOn = wR < .995 || lk > 0;
      for (let y = 0, i = 0; y < F.gh; y++) for (let x = 0; x < F.gw; x++, i++) {
        const q = d[base + i], k3 = i * 3;
        if (q === 255 || !dotsOn) { F.pos[k3 + 1] = -9999; continue; }
        const gx = (x / (F.gw - 1) - .5) * W, gy = (.5 - y / (F.gh - 1)) * Hh, inpic = c >= F.th[i]; let px = gx, py = gy, pz = .02;
        if (!inpic) { const a = F.r1[i] * 6.283 + t * .3 * (F.r2[i] - .5), R = scat * (.35 + .65 * F.r2[i]), far = Math.max(0, 1 - Math.max(0, c)); px = gx + Math.cos(a) * R; py = gy + Math.sin(a) * R * .7; pz = Math.sin(a * 1.7) * R * .5;
          if (f.mode === 'surface') py -= 6 * far * (.5 + F.r2[i]); else if (f.mode === 'caught') px += (F.r1[i] - .5) * 2 + 9 * far * Math.sin(t * .9 + F.r2[i] * 3); else if (f.mode === 'pulled') { px += 10 * far * (.4 + F.r1[i]); py += 3 * far * (F.r2[i] - .3); } }
        if (tgt) { const st = F.r1[i] * .25, kk = ease((lk - st) / (1 - .25)); if (lk > 1.08 + F.r2[i] * .15) { F.pos[k3 + 1] = -9999; continue; }
          const arc = Math.sin(kk * Math.PI) * 1.2; px += (tgt.x + (F.r1[i] - .5) * .5 - px) * kk; py += (tgt.y + (F.r2[i] - .5) * .3 - py) * kk + arc; pz += (tgt.z - pz) * kk; }
        F.pos[k3] = px; F.pos[k3 + 1] = py; F.pos[k3 + 2] = pz;
        const lv = .42 + .58 * (q / 7), s = inpic ? 1 : .72; F.col[k3] = INK.r * lv * s; F.col[k3 + 1] = INK.g * lv * s; F.col[k3 + 2] = INK.b * lv * s;
      }
      F.geo.attributes.position.needsUpdate = true; F.geo.attributes.color.needsUpdate = true;
      F.pts.material.size = W / F.gw * (c > .5 ? 1.18 : .75) * (tgt ? 1.15 : 1);
      const bc = ease((c - .15) / .6) * (tgt ? 1 - ease(lk * 2) : 1); F.back.visible = bc > .02; F.back.scale.set(1, Math.max(.001, bc), 1); F.back.position.set(0, (1 - bc) * Hh / 2, -.02);
      // strands: six ribbons from the bell rim to the top of the picture (the visible link)
      if (c > .05 && !(tgt && lk > .3)) { const P = [], topY = Hh / 2; F.g.updateMatrixWorld();
        for (let s = 0; s < 6; s++) { const ux = s / 5 - .5, a = A.j.pos.clone().addScaledVector(A.r, ux * A.bellR * 1.1).addScaledVector(A.u, -A.bellR * .35), b = new THREE.Vector3(ux * W * .92, topY, .03).applyMatrix4(F.g.matrixWorld);
          const side = A.r.clone().multiplyScalar(.035 * (A.j === hero ? 1.6 : 1)); [a.clone().sub(side), a.clone().add(side), b.clone().add(side), a.clone().sub(side), b.clone().add(side), b.clone().sub(side)].forEach(v => P.push(v.x, v.y, v.z)); }
        F.strands.geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(P), 3)); F.strands.geometry.attributes.position.needsUpdate = true; F.strands.visible = true; const cc = Math.min(1, c * 1.2); F.strands.material.color.setRGB(.94 * cc, .77 * cc, .54 * cc); }
    }
    for (const s of SPEC.scale || []) { const j = J(s.k), u = ease((t - s.t0) / (s.t1 - s.t0)); j.root.scale.setScalar(1 + (s.to - 1) * u); }
  }
  function masks(R, holderKey, filmId) {
    const vis = []; scene.traverse(o => { if (o !== scene && o.parent === scene) vis.push([o, o.visible]); });
    const bg = scene.background; scene.background = null; const out = {}; const j = J(holderKey), F = films.find(x => x.f.id === filmId), fv = F && F.g.visible;
    const one = objs => { for (const [o] of vis) o.visible = false; for (const o of objs) o.visible = true; R.setClearColor(0, 1); R.render(scene, cam); const c = document.createElement('canvas'); c.width = 320; c.height = 180; c.getContext('2d').drawImage(R.domElement, 0, 0, 320, 180); return c.toDataURL('image/png'); };
    out.mhold = one([j.root]); if (fv) out.mfilm = one([F.g]); for (const [o, v] of vis) o.visible = v; scene.background = bg; return out;
  }
  return {update, masks, films};
}
