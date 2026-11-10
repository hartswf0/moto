"""JELLY CUT compositor: picture = f(t).

Layers, back to front:
  1. THE JELLY ORCHESTRA - the real contaminant-jelly Three.js orchestra, rendered offline on a deterministic clock
     (orchestra.html + orchestra_capture.js), cast from the song by sound role (cast_song.py).
  2. FILMS AS FLECKS - every film (PD archive shots and our BOXBACK film) exists only as a cloud of halftone dots.
     Dot law (after WYGWYL, hartswf0/butterfly-halfworld): 8 ink levels, one ordered (Bayer) halftone pass, no alpha.
     A film condenses by a per-dot allegiance swap on a Bayer schedule: dot k is in the picture iff c >= theta_k,
     otherwise it is a drifting fleck. Far films are inked darker (fog is an ink colour, not a transparency).
  3. Cards (title, cast, credits) - text only.

Every film is gathered by a named character: its centre follows that jelly's projected screen position (meta from
the capture), so the gathering is the jelly's act. A held film blooms toward centre frame.
usage: python3 -I jellycut.py <film-config.json> <t0> <t1> <out.mp4> [--procs 2]
"""
import sys, os, json, math, subprocess, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from multiprocessing import Pool

W, H, FPS = 1280, 720, 24
BAYER8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38],
                   [60, 28, 52, 20, 62, 30, 54, 22], [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                   [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]], float) / 64.0
FONT_D = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FONT_M = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf"
RED = (242, 56, 44)

CFG = None; FILMS = {}; META = {}


def ease(u):
    u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ sources (pure lookups by time)
class Shot:
    """PD archive shot: frames at 12 fps, ping-pong looped; or our film decoded at 12 fps."""
    def __init__(self, frames):
        self.frames = frames  # list of float32 HxW luminance arrays in [0,1]
    def at(self, tau):
        n = len(self.frames); k = int(tau * 12) % max(1, 2 * n - 2)
        return self.frames[k if k < n else 2 * n - 2 - k]


def load_shot(dirp, size=(192, 144), masks=None, outside=0.42):
    """frames in [0,1]; with SAM masks the subject keeps full ink and the rest of the documentary frame is kept but dimmer
    (the footage's edge is never removed - SCION 53)."""
    fs = sorted(x for x in os.listdir(dirp) if x.endswith(".jpg")); M = json.load(open(masks)) if masks else None
    out = []
    for i, f in enumerate(fs):
        im = Image.open(os.path.join(dirp, f)).convert("L"); w0, h0 = im.size
        a = np.asarray(im.resize(size, Image.BILINEAR), np.float32) / 255
        if M and str(i) in M:
            m = Image.new("L", (w0, h0), 0); dm = ImageDraw.Draw(m)
            for poly in M[str(i)]:
                if len(poly) > 2: dm.polygon([tuple(pt) for pt in poly], fill=255)
            mk = np.asarray(m.resize(size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.5)), np.float32) / 255
            lo, hi = np.percentile(a, 4), np.percentile(a, 96); a = np.clip((a - lo) / max(.05, hi - lo), 0, 1)
            a = a * (outside + (1 - outside) * mk)
        out.append(a)
    return Shot(out)


class FilmClock:
    """our BOXBACK film, sampled at song time (film time == song time)."""
    def __init__(self, npy):
        self.a = np.load(npy, mmap_mode="r")
    def at(self, tau):
        return np.asarray(self.a[min(len(self.a) - 1, max(0, int(tau * 12)))], np.float32) / 255


# ------------------------------------------------------------------ the dot law
def dot_film(dst, lum, cx, cy, wpx, c, t, seed, ink=(243, 230, 200), fog=0.0, pitch=7.0, scatter=260.0, water=(18, 22, 20)):
    """Draw one film as halftone flecks. lum: 2-D luminance in [0,1]. c: condensation 0..1 (Bayer allegiance)."""
    if wpx < 8 or c <= -0.5:
        return 0
    gh0, gw0 = lum.shape; gw = max(8, int(wpx / pitch)); gh = max(6, int(gw * gh0 / gw0))
    L = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).resize((gw, gh), Image.LANCZOS), np.float32) / 255
    lo, hi = np.percentile(L, 4), np.percentile(L, 96)                 # per-frame stretch: the picture, not the exposure
    L = np.clip((L - lo) / max(0.05, hi - lo), 0, 1) ** 1.15
    q = np.floor(L * 7.999) / 7.0                                     # 8 ink levels
    yy, xx = np.mgrid[0:gh, 0:gw]
    lit = q > BAYER8[yy % 8, xx % 8]                                  # one ordered halftone pass
    # allegiance threshold per dot: a coarser Bayer order, so the swap reads as an ordered substitution
    theta = BAYER8[(yy // 2 + seed) % 8, (xx // 2 + 3 * seed) % 8] * 0.92 + 0.04
    inpic = c >= theta
    ph = (xx * 12.9898 + yy * 78.233 + seed * 37.719)
    rnd = np.sin(ph) * 43758.5453; rnd = rnd - np.floor(rnd)
    rnd2 = np.sin(ph * 1.7 + 4.1) * 24634.6345; rnd2 = rnd2 - np.floor(rnd2)
    gx = cx + (xx - gw / 2 + 0.5) * pitch; gy = cy + (yy - gh / 2 + 0.5) * pitch
    ang = rnd * 6.2832 + t * 0.35 * (rnd2 - 0.5); rad = scatter * (0.35 + 0.65 * rnd2) * (1 - 0.6 * max(0, c))
    fx = gx + np.cos(ang) * rad + np.sin(t * 0.6 + rnd * 9) * 6; fy = gy + np.sin(ang) * rad * 0.7 + np.cos(t * 0.5 + rnd2 * 9) * 6
    X = np.where(inpic, gx, fx); Y = np.where(inpic, gy, fy)
    # fog is an ink colour: far films are inked toward the water
    col = tuple(int(ink[i] * (1 - fog) + water[i] * fog) for i in range(3))
    fleck = tuple(int(col[i] * 0.72 + water[i] * 0.28) for i in range(3))
    r_in = max(1.0, pitch * 0.44); r_out = max(1.0, pitch * 0.26)
    d = ImageDraw.Draw(dst)
    sel = lit
    for x, y, p, lv in zip(X[sel], Y[sel], inpic[sel], q[sel]):
        r = r_in if p else r_out
        if -4 < x < W + 4 and -4 < y < H + 4:
            k = 0.42 + 0.58 * lv                                          # the ink level sets the dot's brightness
            base = col if p else fleck
            d.ellipse([x - r, y - r, x + r, y + r], fill=(int(base[0] * k), int(base[1] * k), int(base[2] * k)))
    return int(sel.sum())


# ------------------------------------------------------------------ characters: where each jelly is (pure in t)
def jelly_pos(role_idx, t, window=0.6):
    """mean projected screen position of a cast member over [t-window, t]; clamped into a safe frame."""
    fs = [f for f in range(int((t - window) * FPS), int(t * FPS) + 1) if f in META]
    if not fs:
        return (W / 2, H / 2)
    xs = [META[f][role_idx][0] for f in fs]; ys = [META[f][role_idx][1] for f in fs]
    x, y = float(np.mean(xs)), float(np.mean(ys))
    return (min(W - 180, max(180, x)), min(H - 130, max(130, y)))


def jelly_glow(role_idx, t):
    f = int(t * FPS); return META[f][role_idx][3] if f in META else 0.0


def font(p, s):
    return ImageFont.truetype(p, int(s))


def spaced(d, xy, text, f, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track
    return x


def text_width(d, text, f, track):
    return sum(d.textlength(ch, font=f) + track for ch in text) - track


# ------------------------------------------------------------------ one frame
def render(fidx):
    t = fidx / FPS
    op = os.path.join(CFG["orch_dir"], f"o{fidx:05d}.jpg")
    base = Image.open(op).convert("RGB") if os.path.exists(op) else Image.new("RGB", (W, H), (10, 14, 13))
    dim = 1.0
    for ev in CFG["films"]:
        if ev.get("dim") and ev["bloom"][0] - 0.5 <= t <= ev["bloom"][1] + 0.5:
            k = ease((t - ev["bloom"][0] + 0.5)) * (1 - ease(t - ev["bloom"][1]))
            dim = min(dim, 1 - ev["dim"] * k)
    if dim < 0.999:
        base = Image.eval(base, lambda v: int(v * dim))
    labels = []
    for i, ev in enumerate(CFG["films"]):
        t_in, t_out = ev["t"]
        if not (t_in <= t <= t_out):
            continue
        src = FILMS[ev["src"]]
        c0, c1 = ev["condense"]; b0, b1 = ev["bloom"]
        c = ease((t - c0) / max(0.01, c1 - c0)) if t >= c0 else -0.2
        if t > b1:  # release: dots leave on the reverse Bayer schedule
            c = 1 - ease((t - b1) / max(0.01, t_out - b1)) * 1.2
        hx, hy = jelly_pos(ev["by"], t)
        off = ev.get("offset", (140, -60))
        ax, ay = hx + off[0], hy + off[1]
        bk = ease((t - b0) / 0.9) * (1 - ease((t - b1) / 0.9)) if b0 < b1 else 0
        cx = ax + (W / 2 - ax) * bk; cy = ay + (H / 2 + 10 - ay) * bk
        wpx = ev["size"] + (ev["bloom_size"] - ev["size"]) * bk
        tau = (t - t_in) if ev["src"] != "film" else t
        fog = ev.get("fog", 0.35) * (1 - bk)
        pitch = ev.get("pitch", 4.2) + bk * ev.get("bloom_pitch_add", 0.6)
        dot_film(base, src.at(tau), cx, cy, wpx, c, t, seed=i * 5 + 1, fog=fog, pitch=pitch, scatter=ev.get("scatter", 240))
        if c > 0.55 and ev.get("label"):
            labels.append((cx, cy + wpx * 0.75 * (ev.get("aspect", 0.75)) / 2 + 14, ev["label"], ev.get("credit", "")))
    d = ImageDraw.Draw(base)
    fm, fs = font(FONT_M, 24), font(FONT_M, 18)
    for x, y, lab, cr in labels:
        for k, (s, f, col) in enumerate(((lab, fm, (240, 163, 90)), (cr, fs, (190, 200, 196)))):
            if not s: continue
            tw = d.textlength(s, font=f); xx = min(W - tw - 16, max(16, x - tw / 2)); yy = min(H - 64, y + k * 29)
            d.rectangle([xx - 6, yy - 3, xx + tw + 6, yy + (29 if k == 0 else 23)], fill=(6, 10, 10))
            d.text((xx, yy), s, font=f, fill=col)
    for card in CFG.get("cards", []):
        a0, a1 = card["t"]
        if a0 <= t <= a1:
            if card["kind"] == "title":
                fT = font(FONT_D, card.get("size", 96)); y = card.get("y", 230)
                for line in card["lines"]:
                    tw = text_width(d, line, fT, card.get("track", 34)); spaced(d, ((W - tw) / 2, y), line, fT, RED, card.get("track", 34)); y += card.get("size", 96) * 1.15
                if card.get("sub"):
                    fsb = font(FONT_M, 22); tw = text_width(d, card["sub"], fsb, 6); spaced(d, ((W - tw) / 2, y + 16), card["sub"], fsb, (230, 236, 232), 6)
            elif card["kind"] == "cast":
                fc, fw = font(FONT_M, 21), font(FONT_M, 16); y = 92
                d.text((70, 50), "THE CAST · each jelly is one sound of the song", font=fc, fill=(240, 163, 90))
                for name, want in card["members"]:
                    d.text((70, y), name, font=fc, fill=(236, 240, 238)); d.text((70, y + 26), want, font=fw, fill=(170, 186, 182)); y += 60
            elif card["kind"] == "line":
                fl = font(FONT_M, card.get("size", 26)); tw = d.textlength(card["text"], font=fl)
                x = (W - tw) / 2; y = card.get("y", H - 92)
                d.rectangle([x - 12, y - 8, x + tw + 12, y + card.get("size", 26) + 12], fill=(6, 10, 10)); d.text((x, y), card["text"], font=fl, fill=(236, 240, 238))
    return np.asarray(base, np.uint8).tobytes()


def init(cfgp):
    global CFG, FILMS, META
    CFG = json.load(open(cfgp))
    for k, v in CFG["sources"].items():
        FILMS[k] = FilmClock(v["npy"]) if v["kind"] == "film" else load_shot(v["frames"], masks=v.get("masks"))
    for mp in sorted(x for x in os.listdir(CFG["orch_dir"]) if x.startswith("meta_")):
        for m in json.load(open(os.path.join(CFG["orch_dir"], mp))):
            META[m["f"]] = m["jel"]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cfg"); ap.add_argument("t0", type=float); ap.add_argument("t1", type=float); ap.add_argument("out")
    ap.add_argument("--procs", type=int, default=2); ap.add_argument("--crf", type=int, default=21)
    a = ap.parse_args()
    init(a.cfg)
    f0, f1 = int(round(a.t0 * FPS)), int(round(a.t1 * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-ss", f"{a.t0:.4f}", "-t", f"{a.t1 - a.t0:.4f}", "-i", CFG["audio"], "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k", "-shortest", a.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(a.procs, initializer=init, initargs=(a.cfg,)) as pool:
        for i, buf in enumerate(pool.imap(render, range(f0, f1), chunksize=6)):
            p.stdin.write(buf)
            if i % 240 == 0: print("frame", f0 + i, flush=True)
    p.stdin.close(); p.wait(); print("wrote", a.out)


if __name__ == "__main__":
    main()
