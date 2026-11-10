// FILMS INSIDE THE WATER (r3). Each held film is a cloud of halftone flecks (THREE.Points) PARENTED to its jelly:
// it hangs below the bell on visible strands, faces the camera, is fogged by the same water and occluded by depth.
// Dot law (WYGWYL): 8 ink levels, one Bayer pass (precomputed in build_bank.py), no alpha: dots are opaque
// (alphaTest), a dot joins the picture when c >= its Bayer allegiance threshold, and an opaque water-coloured backing
// grows under the condensed picture. During a bloom the camera is solved to frame the WHOLE bell and its film.
export function makeFilmSys(THREE, scene, cam, SONG, SPEC, BANK, bins) {
  const B8 = [[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],[15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]];
  const ease = u => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };
  const dotTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 32; const x = c.getContext('2d'); x.fillStyle = '#fff'; x.beginPath(); x.arc(16, 16, 14, 0, Math.PI * 2); x.fill(); const t = new THREE.CanvasTexture(c); return t; })();
  const INK = new THREE.Color('#f3e6c8').multiplyScalar(1.75), WATER = new THREE.Color('#0e1211');
  const films = SPEC.films.map((f, fi) => {
    const m = BANK[f.bank], gw = m.gw, gh = m.gh, N = gw * gh, data = bins[f.bank];
    const geo = new THREE.BufferGeometry(), pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const mat = new THREE.PointsMaterial({size: f.width / gw * 0.92, map: dotTex, alphaTest: 0.5, vertexColors: true, sizeAttenuation: true, fog: true});
    const pts = new THREE.Points(geo, mat); pts.frustumCulled = false;
    const H = f.width * gh / gw, back = new THREE.Mesh(new THREE.PlaneGeometry(f.width * 1.02, H * 1.02), new THREE.MeshBasicMaterial({color: WATER, fog: true}));
    const g = new THREE.Group(); g.add(back); g.add(pts); scene.add(g); g.visible = false;
    const strands = new THREE.LineSegments(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(new Float32Array(6 * 2 * 3), 3)), new THREE.LineBasicMaterial({color: 0xf0c48a, fog: true}));
    strands.frustumCulled = false; scene.add(strands); strands.visible = false;
    const th = new Float32Array(N), r1 = new Float32Array(N), r2 = new Float32Array(N);
    for (let y = 0, i = 0; y < gh; y++) for (let x = 0; x < gw; x++, i++) { th[i] = B8[((y >> 1) + fi) % 8][((x >> 1) + 3 * fi) % 8] / 64 * .92 + .04; const s = Math.sin(x * 12.9898 + y * 78.233 + fi * 37.7) * 43758.5453; r1[i] = s - Math.floor(s); const s2 = Math.sin(x * 22.1 + y * 41.7 + fi * 9.1) * 24634.6345; r2[i] = s2 - Math.floor(s2); }
    return {f, gw, gh, N, data, pos, col, geo, pts, back, g, H, strands, th, r1, r2, n: m.n};
  });
  const J = k => SONG.J.find(j => j.k === k);
  const _r = new THREE.Vector3(), _u = new THREE.Vector3(), _fw = new THREE.Vector3(), CPOS = new THREE.Vector3(), CLOOK = new THREE.Vector3();
  function stateOf(f, t) {
    const [c0, c1] = f.condense, rel = f.release; let c = t >= c0 ? ease((t - c0) / Math.max(.01, c1 - c0)) : -1;
    if (t > rel) c = f.memory ? 0 : 1 - ease((t - rel) / 2.0) * 1.3;
    return c;
  }
  function anchor(F, t) {   // the film hangs below its holder's bell, facing the camera
    const j = J(F.f.by), bellR = j.sz * (F.f.bell ?? 0.95) * (j.root.scale.x || 1);
    cam.getWorldDirection(_fw); _r.crossVectors(_fw, cam.up).normalize(); _u.crossVectors(_r, _fw).normalize();
    const gap = F.f.gap ?? 0.55, c = j.pos.clone().addScaledVector(_u, -(bellR * 0.55 + gap + F.H / 2));
    return {j, bellR, c, r: _r.clone(), u: _u.clone(), fw: _fw.clone()};
  }
  let lastFrame = -1;
  function update(t) {
    // 1. camera framing solve for the active bloom (whole bell + film in frame)
    let wcam = 0, best = null;
    for (const F of films) { const [b0, b1] = F.f.bloom; if (b1 <= b0) continue; const w = ease((t - b0 + 1.0) / 1.0) * (1 - ease((t - b1) / 1.0)); if (w > wcam) { wcam = w; best = F; } }
    if (best && wcam > 0) {
      const A = anchor(best, t); A.j.root.updateMatrixWorld(true); const bb = new THREE.Box3().setFromObject(A.j.root, true);
      const tl = 2.1 * (A.j.rig.norm || 1) * A.j.sz * (A.j.root.scale.x || 1); let uTop = A.c.distanceTo(A.j.pos) + Math.max(A.bellR * 1.25, tl * 1.05), half = Math.max(best.f.width / 2, tl * .8);   // extents measured from the film centre along camera up / right
      for (const x of [bb.min.x, bb.max.x]) for (const y of [bb.min.y, bb.max.y]) for (const z of [bb.min.z, bb.max.z]) { const v = new THREE.Vector3(x, y, z).sub(A.c); uTop = Math.max(uTop, v.dot(A.u)); half = Math.max(half, Math.abs(v.dot(A.r))); }
      const uBot = -best.H / 2, top = A.c.clone().addScaledVector(A.u, uTop), bot = A.c.clone().addScaledVector(A.u, uBot);
      const T = top.clone().add(bot).multiplyScalar(.5), hgt = (uTop - uBot) * (best.f.frame ?? 1.16), wid = half * 2 * 1.12;
      const tf = Math.tan(cam.fov * Math.PI / 360), D = Math.max(hgt / (2 * tf), wid / (2 * tf * cam.aspect));
      const dir = cam.position.clone().sub(T); dir.y *= .35; dir.normalize();
      CPOS.copy(T).addScaledVector(dir, D); CLOOK.copy(T);
      const P0 = cam.position.clone(), L0 = cam.position.clone().add(cam.getWorldDirection(new THREE.Vector3()).multiplyScalar(10));
      cam.position.lerpVectors(P0, CPOS, wcam); cam.lookAt(L0.lerp(CLOOK, wcam)); cam.updateMatrixWorld();
    }
    // 2. each film: flecks, backing, strands
    for (const F of films) {
      const f = F.f, live = t >= f.t[0] && t <= f.t[1]; F.g.visible = live; F.strands.visible = false; if (!live) continue;
      const c = stateOf(f, t), A = anchor(F, t);
      F.g.position.copy(A.c); F.g.quaternion.copy(cam.quaternion);
      const fi = Math.min(F.n - 1, Math.max(0, Math.floor((t - f.t[0]) * 12))), base = fi * F.N, d = F.data;
      const W = f.width, Hh = F.H, scat = f.scatter ?? 2.6; let lk = 0, tgt = null;
      if (f.release_to && t > f.letgo) { lk = ease((t - f.letgo) / ((f.letgo_end ?? f.letgo + 1.2) - f.letgo)); const G = films.find(x => x.f.id === f.release_to); if (G && G.g.visible) { G.g.updateMatrixWorld(); tgt = new THREE.Vector3((f.target[0] - .5) * G.f.width, (.5 - f.target[1]) * G.H, .05).applyMatrix4(G.g.matrixWorld); F.g.updateMatrixWorld(); tgt = F.g.worldToLocal(tgt); } }
      const memory = f.memory && t > f.release; let shown = 0;
      for (let y = 0, i = 0; y < F.gh; y++) for (let x = 0; x < F.gw; x++, i++) {
        const q = d[base + i], k = i * 3;
        if (q === 255 || (f.letgo_end && t > f.letgo_end + .15)) { F.pos[k + 1] = -9999; continue; }
        const gx = (x / (F.gw - 1) - .5) * W, gy = (.5 - y / (F.gh - 1)) * Hh, inpic = c >= F.th[i];
        let px = gx, py = gy, pz = .02;
        if (!inpic) { const a = F.r1[i] * 6.283 + t * .3 * (F.r2[i] - .5), R = (memory ? 1.1 : scat) * (.35 + .65 * F.r2[i]); px = gx * (memory ? .25 : 1) + Math.cos(a) * R; py = gy * (memory ? .25 : 1) + Math.sin(a) * R * .7 + (memory ? A.bellR * 1.2 + F.H / 2 : 0); pz = Math.sin(a * 1.7) * R * .5; }
        if (tgt) { const kk = Math.min(1, lk * (1 + .6 * F.r2[i])); px += (tgt.x + (F.r1[i] - .5) * .22 - px) * kk; py += (tgt.y + (F.r2[i] - .5) * .14 - py) * kk; pz += (tgt.z - pz) * kk; }
        F.pos[k] = px; F.pos[k + 1] = py; F.pos[k + 2] = pz;
        const lv = .42 + .58 * (q / 7), s = inpic ? 1 : .72; F.col[k] = INK.r * lv * s; F.col[k + 1] = INK.g * lv * s; F.col[k + 2] = INK.b * lv * s; shown++;
      }
      F.geo.attributes.position.needsUpdate = true; F.geo.attributes.color.needsUpdate = true;
      F.pts.material.size = W / F.gw * (c > .5 ? 1.18 : .7) * (tgt ? 1 - .6 * lk : 1);
      const bc = ease((c - .15) / .6); F.back.visible = bc > .02 && !memory; F.back.scale.set(1, Math.max(.001, bc), 1); F.back.position.set(0, (1 - bc) * Hh / 2, -.02);
      // strands: from the bell rim to the top of the picture (the visible link)
      if (c > .05 && !memory) { const P = F.strands.geometry.attributes.position.array, topY = Hh / 2; F.g.updateMatrixWorld(); let w = 0;
        for (let s = 0; s < 6; s++) { const ux = (s / 5 - .5); const a = A.j.pos.clone().addScaledVector(A.r, ux * A.bellR * 1.1).addScaledVector(A.u, -A.bellR * .35); const b = new THREE.Vector3(ux * W * .92, topY * (1 - (1 - bc) * 0), .03).applyMatrix4(F.g.matrixWorld);
          P[w++] = a.x; P[w++] = a.y; P[w++] = a.z; P[w++] = b.x; P[w++] = b.y; P[w++] = b.z; }
        F.strands.geometry.attributes.position.needsUpdate = true; F.strands.visible = true; F.strands.material.color.setRGB(.94 * Math.min(1, c * 1.2), .77 * Math.min(1, c * 1.2), .54 * Math.min(1, c * 1.2)); }
    }
    // the medusa lights one tentacle in silver for every memory it has let go (its own rig: 'each film you hold lights one')
    for (const F of films) { const j = J(F.f.by); j.lit = films.filter(G => G.f.by === F.f.by && t > G.f.release).length; }
    // 3. the holder's changed state after the let-go: lighter for the rest of the song
    for (const s of SPEC.scale || []) { const j = J(s.k), u = ease((t - s.t0) / (s.t1 - s.t0)); const k = 1 + (s.to - 1) * u; j.root.scale.setScalar(k); }
  }
  // mask passes: holder-only and film-only, rendered without bloom, for verification on rendered frames
  function masks(R, holderKey, filmId) {
    const keep = new Set(), vis = []; scene.traverse(o => { if (o !== scene && o.parent === scene) vis.push([o, o.visible]); });
    const bg = scene.background; scene.background = null; const out = {};
    const one = (objs) => { for (const [o] of vis) o.visible = false; for (const o of objs) o.visible = true; R.setClearColor(0x000000, 1); R.render(scene, cam); const c = document.createElement('canvas'); c.width = 320; c.height = 180; c.getContext('2d').drawImage(R.domElement, 0, 0, 320, 180); return c.toDataURL('image/png'); };
    const j = J(holderKey), F = films.find(x => x.f.id === filmId);
    const fv = F && F.g.visible; out.mhold = one([j.root]); if (fv) out.mfilm = one([F.g]);
    for (const [o, v] of vis) o.visible = v; scene.background = bg; return out;
  }
  return {update, masks, films};
}
