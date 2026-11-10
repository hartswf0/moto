"""JELLY CUT compositor (r2): picture = f(t).

Layers, back to front:
  1. THE JELLY ORCHESTRA: the real contaminant-jelly Three.js orchestra, rendered offline on a deterministic clock and
     DIRECTED (direct.json): a jelly that holds a film turns toward the camera first (attention), carries the film
     (hold, with extra pulses), and after the release goes somewhere else at a different rate (changed state).
  2. FILMS AS FLECKS, HELD BY THEIR JELLY. Each film hangs from its jelly's bell, under the projected bell position
     from the capture's own metadata, so it moves when the jelly moves. Dot law (after WYGWYL): 8 ink levels, one
     ordered Bayer halftone pass, no alpha. A film condenses by a per-dot allegiance swap on a Bayer schedule. A
     masked subject is CUT OUT by its SAM mask: no dots outside it, an opaque water-coloured backing inside it, so no
     jelly ever shows through the subject. A release can stream the flecks INTO another film (release_to).
  3. A kick halo on the Sentinel, labels laid out without collisions, and titles on opaque plates.
usage: python3 -I jellycut.py <cfg.json> <t0> <t1> <out.mp4> [--procs 2] [--crf 31]
"""
import os, json, math, subprocess, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from multiprocessing import Pool

W, H, FPS = 1280, 720, 24
BAYER8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38],
                   [60, 28, 52, 20, 62, 30, 54, 22], [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                   [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]], float) / 64.0
FONT_D = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FONT_M = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf"
RED = (242, 56, 44); WATER = (14, 18, 17); INK = (243, 230, 200)
CFG = None; SRC = {}; META = {}; KEYS = {}; KICKS = []


def ease(u):
    u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ sources: each returns (lum, mask) for a time
class Frames:
    def __init__(self, lums, masks=None):
        self.l, self.m = lums, masks
    def at(self, tau):
        n = len(self.l); k = int(tau * 12) % max(1, 2 * n - 2); k = k if k < n else 2 * n - 2 - k
        return self.l[k], (self.m[k] if self.m is not None else None)


def load_frames(dirp, masks=None, cut=False, size=(192, 144)):
    fs = sorted(x for x in os.listdir(dirp) if x.endswith(".jpg")); M = json.load(open(masks)) if masks else None
    lums, mks = [], []
    for i, f in enumerate(fs):
        im = Image.open(os.path.join(dirp, f)).convert("L"); w0, h0 = im.size
        a = np.asarray(im.resize(size, Image.BILINEAR), np.float32) / 255
        if M is not None:
            m = Image.new("L", (w0, h0), 0); dm = ImageDraw.Draw(m)
            for poly in M.get(str(i), []):
                if len(poly) > 2: dm.polygon([tuple(pt) for pt in poly], fill=255)
            mks.append(np.asarray(m.resize(size, Image.BILINEAR), np.float32) / 255)
        lums.append(a)
    if cut and mks:
        # crop every frame to the union of the subject's masks, so the subject fills the box
        U = np.max(np.stack(mks), 0) > 0.5; ys, xs = np.where(U)
        if len(xs):
            pad = 6; x0, x1 = max(0, xs.min() - pad), min(size[0], xs.max() + pad); y0, y1 = max(0, ys.min() - pad), min(size[1], ys.max() + pad)
            lums = [l[y0:y1, x0:x1] for l in lums]; mks = [m[y0:y1, x0:x1] for m in mks]
        return Frames(lums, mks)
    return Frames(lums, None)


class Still:
    """a painting: one frame with a slow drift (the camera breathes across it); no mask: the picture is the subject."""
    def __init__(self, path, size=(240, 180)):
        im = Image.open(path).convert("L"); im.thumbnail((size[0] * 2, size[1] * 2)); self.im = im
    def at(self, tau):
        w, h = self.im.size; z = 1.0 + 0.05 * math.sin(tau * 0.25); cw, ch = w / z, h / z
        x0 = (w - cw) * (0.5 + 0.4 * math.sin(tau * 0.17)); y0 = (h - ch) * (0.5 + 0.4 * math.cos(tau * 0.13))
        c = self.im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((200, int(200 * h / w)), Image.BILINEAR)
        return np.asarray(c, np.float32) / 255, None


class FilmClock:
    def __init__(self, npy):
        self.a = np.load(npy, mmap_mode="r")
    def at(self, tau):
        return np.asarray(self.a[min(len(self.a) - 1, max(0, int(tau * 12)))], np.float32) / 255, None


# ------------------------------------------------------------------ the dot law
def grid_of(lum, mask, wpx, pitch):
    gh0, gw0 = lum.shape; gw = max(8, int(wpx / pitch)); gh = max(6, int(gw * gh0 / gw0))
    L = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).resize((gw, gh), Image.LANCZOS), np.float32) / 255
    sub = None
    if mask is not None:
        sub = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).resize((gw, gh), Image.BILINEAR), np.float32) / 255 > 0.5
    v = L[sub] if sub is not None and sub.any() else L
    lo, hi = np.percentile(v, 4), np.percentile(v, 96)
    L = np.clip((L - lo) / max(0.05, hi - lo), 0, 1) ** 1.1
    return L, sub, gw, gh


def dot_film(dst, lum, mask, cx, cy, wpx, c, t, seed, fog=0.0, pitch=4.2, scatter=240.0, stream=None, back=True):
    """one film as halftone flecks centred at (cx,cy), width wpx. c: condensation. stream: (x,y,k) pulls released flecks
    toward a point (k 0..1). Returns the box it occupies when condensed."""
    if wpx < 8 or c <= -0.5:
        return None
    L, sub, gw, gh = grid_of(lum, mask, wpx, pitch)
    q = np.floor(L * 7.999) / 7.0                                     # 8 ink levels
    yy, xx = np.mgrid[0:gh, 0:gw]
    lit = q > BAYER8[yy % 8, xx % 8]                                  # one ordered halftone pass
    if sub is not None:
        lit = lit & sub                                               # cut out: nothing outside the subject is drawn
    theta = BAYER8[(yy // 2 + seed) % 8, (xx // 2 + 3 * seed) % 8] * 0.92 + 0.04
    inpic = c >= theta
    ph = (xx * 12.9898 + yy * 78.233 + seed * 37.719)
    rnd = np.sin(ph) * 43758.5453; rnd = rnd - np.floor(rnd)
    rnd2 = np.sin(ph * 1.7 + 4.1) * 24634.6345; rnd2 = rnd2 - np.floor(rnd2)
    gx = cx + (xx - gw / 2 + 0.5) * pitch; gy = cy + (yy - gh / 2 + 0.5) * pitch
    ang = rnd * 6.2832 + t * 0.35 * (rnd2 - 0.5); rad = scatter * (0.35 + 0.65 * rnd2) * (1 - 0.6 * max(0, c))
    fx = gx + np.cos(ang) * rad + np.sin(t * 0.6 + rnd * 9) * 6; fy = gy + np.sin(ang) * rad * 0.7 + np.cos(t * 0.5 + rnd2 * 9) * 6
    if stream is not None:
        sx, sy, k = stream; kk = k * (0.6 + 0.4 * rnd2)
        fx = fx + (sx + (rnd - 0.5) * 40 - fx) * kk; fy = fy + (sy + (rnd2 - 0.5) * 24 - fy) * kk
    X = np.where(inpic, gx, fx); Y = np.where(inpic, gy, fy)
    col = tuple(int(INK[i] * (1 - fog) + WATER[i] * fog) for i in range(3))
    fleck = tuple(int(col[i] * 0.72 + WATER[i] * 0.28) for i in range(3))
    r_in = max(1.0, pitch * 0.44); r_out = max(1.0, pitch * 0.26) * (1 - 0.6 * (stream[2] if stream else 0))
    d = ImageDraw.Draw(dst)
    box = (cx - gw * pitch / 2, cy - gh * pitch / 2, cx + gw * pitch / 2, cy + gh * pitch / 2)
    if back and c > 0.15:
        # an opaque backing inked in the water colour, under the condensed picture: nothing behind shows through it
        if sub is not None:
            bm = Image.fromarray((sub & (c >= theta)).astype(np.uint8) * 255).resize((max(1, int(gw * pitch)), max(1, int(gh * pitch))), Image.NEAREST).filter(ImageFilter.MaxFilter(5))
            dst.paste(WATER, (int(box[0]), int(box[1])), bm)
        else:
            fr = ease((c - 0.15) / 0.6)
            if fr > 0.02:
                bx = (box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2)
                hb = (bx[3] - bx[1]) * fr
                d.rectangle([bx[0], bx[1], bx[2], bx[1] + hb], fill=WATER)
    for x, y, p, lv in zip(X[lit], Y[lit], inpic[lit], q[lit]):
        r = r_in if p else r_out
        if -4 < x < W + 4 and -4 < y < H + 4:
            k = 0.42 + 0.58 * lv; base = col if p else fleck
            d.ellipse([x - r, y - r, x + r, y + r], fill=(int(base[0] * k), int(base[1] * k), int(base[2] * k)))
    return box


# ------------------------------------------------------------------ the held film: geometry is a pure function of t
def jelly(key, t, window=0.15):
    j = KEYS.get(key); fs = [f for f in range(int((t - window) * FPS), int(t * FPS) + 1) if f in META]
    if j is None or not fs:
        return (W / 2, H / 3, 40.0)
    x = float(np.mean([META[f][j][0] for f in fs])); y = float(np.mean([META[f][j][1] for f in fs])); r = float(np.mean([META[f][j][5] for f in fs]))
    return (min(W - 60, max(60, x)), min(H - 60, max(40, y)), max(18.0, min(140.0, r)))


def film_state(ev, t):
    """(c, width, centre, stream) of one held film at t, or None."""
    t_in, t_out = ev["t"]
    if not (t_in <= t <= t_out):
        return None
    c0, c1 = ev["condense"]; b0, b1 = ev["bloom"]; rel = ev["release"]
    c = ease((t - c0) / max(0.01, c1 - c0)) if t >= c0 else -0.2
    if t > rel:
        c = 1 - ease((t - rel) / 2.2) * 1.25
    bk = 0.0
    if b1 > b0:
        bk = ease((t - b0) / 0.9) * (1 - ease((t - b1) / 0.9))
    wpx = ev["size"] + (ev["bloom_size"] - ev["size"]) * bk
    jx, jy, jr = jelly(ev["by"], t)
    asp = ev.get("aspect", 0.75)
    cx, cy = jx, jy + jr * 0.85 + wpx * asp / 2 + 6           # hanging from the bell
    cx = min(W - wpx / 2 - 8, max(wpx / 2 + 8, cx)); cy = min(H - wpx * asp / 2 - 8, max(wpx * asp / 2 + 8, cy))
    stream = None
    if ev.get("release_to") and t > rel:
        tgt = target_point(ev["release_to"], t)
        if tgt: stream = (tgt[0], tgt[1], ease((t - rel) / 1.8))
    return c, wpx, (cx, cy), stream, (jx, jy, jr)


def target_point(name, t):
    if name == "gate_dog":
        for ev in CFG["films"]:
            if ev["src"] == "film" and "gate" in ev["label"]:
                st = film_state(ev, t)
                if st:
                    c, wpx, (cx, cy), _, _ = st; h = wpx * 0.5625
                    return (cx - wpx / 2 + 0.70 * wpx, cy - h / 2 + 0.74 * h)
    return None


def label_boxes(t, d=None):
    """the label layout for frame t (shared by the renderer and the test): one label per condensed film, under its
    picture; on a collision it tries above, then is dropped (the earlier label in the timeline keeps its place)."""
    fm, fs = font(FONT_M, 24), font(FONT_M, 18)
    d = d or ImageDraw.Draw(Image.new("RGB", (1, 1)))
    placed = []; plates = [p for p in title_plates(t, d)]
    fboxes = {}
    for i, ev in enumerate(CFG["films"]):
        st = film_state(ev, t)
        if st and st[0] > 0.3:
            c, wpx, (cx, cy), _, _ = st; hh = wpx * ev.get("aspect", 0.75); fboxes[i] = (cx - wpx / 2, cy - hh / 2, cx + wpx / 2, cy + hh / 2)
    for i, ev in enumerate(CFG["films"]):
        st = film_state(ev, t)
        if not st: continue
        c, wpx, (cx, cy), _, _ = st
        if c < 0.55 or not ev.get("label"): continue
        h = wpx * ev.get("aspect", 0.75)
        tw = max(d.textlength(ev["label"], font=fm), d.textlength(ev["credit"], font=fs)); bh = 56
        for y in (cy + h / 2 + 10, cy - h / 2 - bh - 10):
            x0 = min(W - tw - 22, max(10, cx - tw / 2 - 6)); b = (x0, y, x0 + tw + 12, y + bh)
            if b[1] < 4 or b[3] > H - 4: continue
            if any(not (b[2] <= o[0] or b[0] >= o[2] or b[3] <= o[1] or b[1] >= o[3]) for o in [p[0] for p in placed] + plates + [fb for j, fb in fboxes.items() if j != i]):
                continue
            placed.append((b, ev["label"], ev["credit"])); break
    return placed


def title_plates(t, d):
    out = []
    for card in CFG.get("cards", []):
        a0, a1 = card["t"]
        if a0 <= t <= a1:
            if card["kind"] == "title":
                fT = font(FONT_D, card.get("size", 96)); y = card.get("y", 230); tw = max(text_width(d, ln, fT, 34) for ln in card["lines"])
                hgt = len(card["lines"]) * card.get("size", 96) * 1.15 + (60 if card.get("sub") else 0)
                out.append(((W - tw) / 2 - 40, y - 24, (W + tw) / 2 + 40, y + hgt + 20))
            elif card["kind"] == "cast":
                out.append((40, 30, 760, 92 + 60 * len(card["members"])))
    return out


def font(p, s):
    return ImageFont.truetype(p, int(s))


def spaced(d, xy, text, f, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track


def text_width(d, text, f, track):
    return sum(d.textlength(ch, font=f) + track for ch in text) - track


def kick_env(t):
    """1 on a kick, decaying over ~110 ms; pure in t (from the cast)."""
    i = np.searchsorted(KICKS, t + 1e-6) - 1
    if i < 0: return 0.0
    return math.exp(-(t - KICKS[i]) / 0.11)


# ------------------------------------------------------------------ one frame
def render(fidx):
    t = fidx / FPS
    op = os.path.join(CFG["orch_dir"], f"o{fidx:05d}.jpg")
    base = Image.open(op).convert("RGB") if os.path.exists(op) else Image.new("RGB", (W, H), WATER)
    dim = 1.0
    for ev in CFG["films"]:
        b0, b1 = ev["bloom"]
        if ev.get("dim") and b1 > b0 and b0 - 0.5 <= t <= b1 + 0.9:
            dim = min(dim, 1 - ev["dim"] * ease(t - b0 + 0.5) * (1 - ease(t - b1)))
    if dim < 0.999:
        base = Image.eval(base, lambda v: int(v * dim))
    # the Sentinel's kick: a halo at its bell on every kick
    if CFG.get("kick_flash"):
        e = kick_env(t)
        if e > 0.02:
            x, y, r = jelly(CFG["kick_flash"]["key"], t, window=0.0)
            ov = Image.new("RGB", (W, H), (0, 0, 0)); od = ImageDraw.Draw(ov); R = r * 1.9
            for k, a in ((1.0, 0.35), (0.72, 0.65), (0.45, 1.0)):
                v = int(150 * e * a); od.ellipse([x - R * k, y - R * k, x + R * k, y + R * k], fill=(v, int(v * 0.8), int(v * 0.55)))
            base = ImageChops.add(base, ov.filter(ImageFilter.GaussianBlur(6)))
    for i, ev in enumerate(CFG["films"]):
        st = film_state(ev, t)
        if not st: continue
        c, wpx, (cx, cy), stream, _ = st
        src = SRC[ev["src"]]; tau = t if ev["src"] == "film" else t - ev["t"][0]
        lum, mask = src.at(tau)
        bk = 0.0 if ev["bloom"][1] <= ev["bloom"][0] else ease((t - ev["bloom"][0]) / 0.9) * (1 - ease((t - ev["bloom"][1]) / 0.9))
        pitch = (4.0 if ev["src"] == "film" else 4.2) + 0.5 * bk
        dot_film(base, lum, mask, cx, cy, wpx, c, t, seed=i * 5 + 1, fog=0.25 * (1 - bk), pitch=pitch, stream=stream)
    d = ImageDraw.Draw(base)
    for card in CFG.get("cards", []):
        a0, a1 = card["t"]
        if not (a0 <= t <= a1): continue
        for p in title_plates(t, d):
            pass
        if card["kind"] == "title":
            fT = font(FONT_D, card.get("size", 96)); y = card.get("y", 230)
            pl = title_plates(t, d)
            for p in pl: d.rounded_rectangle(p, radius=10, fill=(8, 12, 12))
            for line in card["lines"]:
                tw = text_width(d, line, fT, 34); spaced(d, ((W - tw) / 2, y), line, fT, RED, 34); y += card.get("size", 96) * 1.15
            if card.get("sub"):
                fsb = font(FONT_M, 22); tw = text_width(d, card["sub"], fsb, 6); spaced(d, ((W - tw) / 2, y + 16), card["sub"], fsb, (230, 236, 232), 6)
        elif card["kind"] == "cast":
            d.rounded_rectangle((40, 30, 760, 92 + 60 * len(card["members"])), radius=10, fill=(8, 12, 12))
            fc, fw = font(FONT_M, 23), font(FONT_M, 17); y = 96
            d.text((70, 50), "THE CAST · each jelly is one sound of the song", font=fc, fill=(240, 163, 90))
            for name, want in card["members"]:
                d.text((70, y), name, font=fc, fill=(236, 240, 238)); d.text((70, y + 27), want, font=fw, fill=(176, 190, 186)); y += 60
    fm, fs = font(FONT_M, 24), font(FONT_M, 18)
    for b, lab, cr in label_boxes(t, d):
        d.rectangle(b, fill=(6, 10, 10)); d.text((b[0] + 6, b[1] + 4), lab, font=fm, fill=(240, 163, 90)); d.text((b[0] + 6, b[1] + 32), cr, font=fs, fill=(196, 206, 202))
    return np.asarray(base, np.uint8).tobytes()


def init(cfgp):
    global CFG, META, KEYS, KICKS
    CFG = json.load(open(cfgp))
    for k, v in CFG["sources"].items():
        SRC[k] = FilmClock(v["npy"]) if v["kind"] == "film" else (Still(v["image"]) if v["kind"] == "still" else load_frames(v["frames"], v.get("masks"), v.get("cut", False)))
    for mp in sorted(x for x in os.listdir(CFG["orch_dir"]) if x.startswith("meta_")):
        for m in json.load(open(os.path.join(CFG["orch_dir"], mp))):
            META[m["f"]] = m["jel"]
    if META:
        f0 = next(iter(META)); KEYS = {row[6]: i for i, row in enumerate(META[f0])}
    cast = json.load(open(os.path.join(os.path.dirname(cfgp), "cast.json")))
    KICKS = np.array(sorted(e[0] for e in cast["roles"]["kick"]))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cfg"); ap.add_argument("t0", type=float); ap.add_argument("t1", type=float); ap.add_argument("out")
    ap.add_argument("--procs", type=int, default=2); ap.add_argument("--crf", type=int, default=31)
    a = ap.parse_args(); init(a.cfg)
    f0, f1 = int(round(a.t0 * FPS)), int(round(a.t1 * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-ss", f"{a.t0:.4f}", "-t", f"{a.t1 - a.t0:.4f}", "-i", CFG["audio"], "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "slow", "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k", "-shortest", a.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(a.procs, initializer=init, initargs=(a.cfg,)) as pool:
        for i, buf in enumerate(pool.imap(render, range(f0, f1), chunksize=6)):
            p.stdin.write(buf)
            if i % 480 == 0: print("frame", f0 + i, flush=True)
    p.stdin.close(); p.wait(); print("wrote", a.out)


if __name__ == "__main__":
    main()
