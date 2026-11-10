"""Multiplane engine (SCION-NORSTEIN primitives).

Glass plane  : a layer at explicit distance z (world units). Screen offset of a world point:
               sx = W/2 + (wx - cam_x) / z * F,  sy = HORIZON + (wy - cam_y) / z * F
               => parallax speed of a plane is exactly F/z per unit camera move (tested in tests/).
Fog field    : depth slabs between consecutive planes. Each slab carries its own noise texture that
               scrolls at the slab's parallax rate plus drift, and an alpha from the density integral
               over the slab thickness: a = 1 - exp(-sigma(z, t) * dz) * noise. Far planes therefore
               accumulate more fog than near ones (fog is NOT a uniform overlay).
Fog states   : reveal / obscure / lure / suspend - a function of time that sets sigma(z, t).
Focus        : focus_z(t); a plane is blurred by radius k * |1/z - 1/focus_z| (thin-lens style).
"""
import math, numpy as np
from PIL import Image, ImageFilter, ImageDraw
from engine import W, H, _ac

F = 6.0            # projection constant: a plane at z = 6 is drawn 1:1 (world unit = 1 px)
HORIZON = 330.0


def proj(wx, wy, z, cam):
    return (W / 2 + (wx - cam["x"]) / z * F, HORIZON + (wy - cam["y"]) / z * F)


def scale_at(z):
    return F / z


# ----------------------------------------------------------------- fog noise (precomputed, tileable)
def _fbm(w, h, seed, octaves=5):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        gw, gh = 4 * 2 ** o, max(2, int(4 * 2 ** o * h / w))
        g = rng.random((gh, gw)).astype(np.float32)
        g = np.concatenate([g, g[:, :1]], 1); g = np.concatenate([g, g[:1, :]], 0)  # tile seam
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w + w // gw, h + h // gh), Image.BICUBIC)
        a = np.asarray(im, np.float32)[:h, :w] / 255.0
        out += a * amp; tot += amp; amp *= 0.55
    out /= tot
    out = (out - out.min()) / (out.max() - out.min() + 1e-9)
    return out


class Fog:
    """Tileable noise tiles at 1/4 resolution; upscaled per slab per frame."""
    def __init__(self, n=4):
        self.tiles = [_fbm(640, 180, 11 + i) for i in range(n)]

    def slab(self, i, offx, offy, alpha, color, contrast=1.0, floor=0.25):
        t = self.tiles[i % len(self.tiles)]
        sx = int(offx / 4) % t.shape[1]; sy = int(offy / 4) % t.shape[0]
        a = np.roll(np.roll(t, -sx, 1), -sy, 0)[:, :320]          # 320 x 180 window
        a = floor + (1 - floor) * np.clip((a - 0.5) * contrast + 0.5, 0, 1)
        a = np.clip(a * alpha, 0, 1)
        A = Image.fromarray((a * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
        L = Image.new("RGBA", (W, H), color + (0,)); L.putalpha(A)
        return L


def blur_for(z, focus_z, k=55.0, cap=9.0):
    r = k * abs(1.0 / z - 1.0 / focus_z)
    return min(cap, r)


def apply_blur(im, r):
    if r < 0.6:
        return im
    return im.filter(ImageFilter.GaussianBlur(r))


def glow(radius, color, strength=1.0):
    s = int(radius * 2)
    yy, xx = np.mgrid[0:s, 0:s]
    d = np.hypot(xx - radius, yy - radius) / radius
    a = np.clip(np.exp(-d * d * 3.2) * strength, 0, 1)
    im = np.zeros((s, s, 4), np.uint8); im[..., 0], im[..., 1], im[..., 2] = color
    im[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(im, "RGBA")


def blit_center(dst, im, x, y):
    _ac(dst, im, x - im.width / 2, y - im.height / 2)
