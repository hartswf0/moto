"""Depth audio: every cue has a z (distance) and a pan. Gain ~ 1/(1+0.12 z); a one-pole low-pass whose cutoff falls
with distance and fog (far and fogged sounds are dull); equal-power pan. Wind bed follows film.storm_curve."""
import numpy as np, wave
SR = 44100


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def tone(f0, f1, dur, d, kind="sine", a=0.003):
    n = int(dur * SR); f = np.geomspace(f0, f1, n); ph = 2 * np.pi * np.cumsum(f) / SR
    w = np.sin(ph) if kind == "sine" else ((ph / np.pi) % 2 - 1)
    return w * env(n, a, d)


def noise(dur, d, seed, a=0.002):
    return np.random.default_rng(seed).normal(0, 1, int(dur * SR)) * env(int(dur * SR), a, d)


def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y


def lp_fast(x, fc):
    # vectorised one-pole via scipy-free recursion on blocks (good enough for short cues)
    return lowpass(x, fc) if len(x) < 200000 else x


def mix(*xs):
    n = max(len(x) for x in xs); y = np.zeros(n)
    for x in xs: y[:len(x)] += x
    return y


def make(kind, seed):
    if kind == "chime":   # the house speaks: two soft partials
        return mix(tone(880, 880, 1.6, 0.6) * 0.5, tone(1318, 1318, 1.4, 0.5) * 0.3, tone(660, 660, 1.8, 0.8) * 0.3)
    if kind == "shutter": return mix(noise(0.08, 0.03, seed) * 0.6, tone(220, 140, 0.12, 0.05) * 0.6)
    if kind == "step": return lowpass(noise(0.12, 0.04, seed), 1500) * 2.0
    if kind == "rustle": return lowpass(noise(1.4, 0.6, seed, 0.2), 3000) * 1.2
    if kind == "flap": return lowpass(noise(0.4, 0.12, seed, 0.01), 2500) * 1.6
    if kind == "knock": return mix(tone(160, 90, 0.2, 0.08), noise(0.05, 0.02, seed) * 0.3)
    if kind == "whir": return tone(300, 520, 1.4, 1.0, "saw", 0.2) * 0.25
    if kind == "door": return mix(tone(110, 60, 0.4, 0.15), lowpass(noise(0.2, 0.06, seed), 800) * 0.8)
    if kind == "tape": return lowpass(noise(0.45, 0.2, seed, 0.02), 6000) * 0.9 * (1 + 0.6 * np.sin(np.arange(int(0.45 * SR)) / SR * 2 * np.pi * 37))
    if kind == "slide": return lowpass(noise(0.9, 0.5, seed, 0.1), 900) * 1.4
    if kind == "heart": return mix(tone(70, 45, 0.25, 0.08), np.concatenate([np.zeros(int(0.18 * SR)), tone(65, 42, 0.2, 0.07) * 0.7]))
    if kind == "flapopen": return lowpass(noise(0.6, 0.25, seed, 0.03), 1800) * 1.2
    if kind == "bell": return mix(tone(523, 523, 4, 2.0) * 0.5, tone(784, 784, 3.5, 1.6) * 0.3, tone(1046, 1046, 3, 1.2) * 0.2)
    if kind == "whirgrain": return tone(340, 420, 0.32, 0.5, "saw", 0.02) * 0.5
    if kind == "pip": return tone(1760, 1760, 0.15, 0.06) * 0.4
    if kind == "hit": return mix(tone(120, 50, 0.4, 0.15), noise(0.06, 0.02, seed) * 0.4)
    raise ValueError(kind)


def render(cues, T, dur, storm_curve, Bfn, out_wav):
    n = int(dur * SR) + SR
    L = np.zeros(n); R = np.zeros(n)
    for i, (b, kind, z, pan, g) in enumerate(cues):
        s = make(kind, i)
        fc = 9000 / (1 + 0.35 * z)
        s = lowpass(s, fc) * g / (1 + 0.12 * z)
        st = int(T(b) * SR)
        if st < 0 or st >= n: continue
        e = min(n, st + len(s)); th = (pan + 1) * np.pi / 4      # equal-power pan, full range
        L[st:e] += s[:e - st] * np.cos(th); R[st:e] += s[:e - st] * np.sin(th)
    # wind bed: band-limited noise, amplitude & brightness from the storm curve (control rate 100 Hz)
    rng = np.random.default_rng(3)
    wn = rng.normal(0, 1, n)
    ctl_t = np.arange(0, dur + 1, 0.01)
    amp = np.array([storm_curve(Bfn(t))[0] for t in ctl_t]); zz = np.array([storm_curve(Bfn(t))[1] for t in ctl_t])
    amp_s = np.interp(np.arange(n) / SR, ctl_t, amp)
    # three fixed bands, crossfaded by distance (near = bright, far = dull)
    lo = lowpass(wn, 300); mid = lowpass(wn, 1200) - lo; hi = wn - lowpass(wn, 1200)
    near = np.interp(np.arange(n) / SR, ctl_t, np.clip(1 - (zz - 3) / 30, 0, 1))
    wind = (lo * 1.0 + mid * (0.3 + 0.7 * near) + hi * 0.25 * near) * amp_s * 0.5
    sway = 0.5 + 0.4 * np.sin(np.arange(n) / SR * 0.37 * 2 * np.pi)
    L += wind * sway; R += wind * (1 - sway)
    y = np.stack([L, R], 1)[: int(dur * SR)]
    y = y / max(1e-9, np.abs(y).max()) * 0.6
    pcm = (np.clip(y, -1, 1) * 32767).astype(np.int16)
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
