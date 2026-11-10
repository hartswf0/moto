"""Synthesised punctuation (original, no samples). Mixed under the song at the cue-sheet beats."""
import numpy as np, subprocess, json, os, sys
SR = 44100

def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

def tone(f0, f1, dur, d=0.15, kind="sine"):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.geomspace(f0, f1, n); ph = 2 * np.pi * np.cumsum(f) / SR
    w = np.sin(ph) if kind == "sine" else (np.sign(np.sin(ph)) * 0.6 if kind == "square" else ((ph / np.pi) % 2 - 1) * 0.7)
    return w * env(n, 0.002, d)

def noise(dur, d, lp=0.2, seed=0):
    n = int(dur * SR); r = np.random.default_rng(seed).normal(0, 1, n)
    y = np.zeros(n); a = lp; acc = 0
    for i in range(n): acc += a * (r[i] - acc); y[i] = acc
    return y / (np.abs(y).max() + 1e-9) * env(n, 0.001, d)

def mix(*xs):
    n = max(len(x) for x in xs); y = np.zeros(n)
    for x in xs: y[:len(x)] += x
    return y

def make(kind, seed=0):
    return _make(kind, seed)

def _make(kind, seed=0):
    if kind == "thump": return mix(tone(110, 38, 0.35, 0.12), noise(0.05, 0.01, 0.3, seed) * 0.4)
    if kind == "stamp": return mix(tone(180, 70, 0.18, 0.05) * 0.8, noise(0.08, 0.02, 0.5, seed) * 0.6)
    if kind == "pop": return tone(900, 300, 0.09, 0.03) * 0.7
    if kind == "pop_small": return tone(1400, 700, 0.06, 0.02) * 0.5
    if kind == "rattle":
        out = np.zeros(int(0.45 * SR))
        for k in range(7):
            s = int(k * 0.06 * SR); c = noise(0.05, 0.012, 0.6, seed + k) * 0.6; out[s:s + len(c)] += c[:len(out) - s]
        return out
    if kind == "whoosh": return noise(0.5, 0.25, 0.05, seed) * 0.8
    if kind == "creak": return tone(180, 120, 0.6, 0.5, "saw") * (0.6 + 0.4 * np.sin(np.arange(int(0.6 * SR)) / SR * 2 * np.pi * 23)) * 0.4
    if kind == "crash":
        return mix(*[np.concatenate([np.zeros(int(k * 0.05 * SR)), noise(0.6, 0.18 + 0.05 * k, 0.4, seed + k)]) for k in range(4)]) * 0.4
    if kind == "kick": return tone(300, 80, 0.15, 0.05) * 0.7
    if kind == "whistle_down": return tone(1600, 300, 0.9, 1.5, "sine") * 0.35
    if kind == "flip": return mix(noise(0.08, 0.02, 0.7, seed) * 0.6, tone(600, 900, 0.05, 0.02) * 0.3)
    if kind == "gulp": return tone(300, 90, 0.3, 0.15) * 0.9
    if kind == "buzz":
        n = int(9.5 * SR); t = np.arange(n) / SR
        f = 210 + 25 * np.sin(2 * np.pi * 1.3 * t) + 12 * np.sin(2 * np.pi * 3.7 * t)
        w = ((np.cumsum(f) / SR) % 1 - 0.5) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.9 * t) ** 2)
        return w * 0.3 * np.minimum(1, t / 0.3) * np.minimum(1, (t[-1] - t) / 0.3)
    if kind == "buzz_close":
        n = int(2.4 * SR); t = np.arange(n) / SR
        w = ((np.cumsum(230 + 40 * t) / SR) % 1 - 0.5) * (t / t[-1]) ** 2
        return w * 0.9 * np.minimum(1, (t[-1] - t) / 0.03)
    if kind == "blip": return tone(1200, 1200, 0.12, 0.08, "square") * 0.35
    if kind == "error": return np.concatenate([tone(300, 300, 0.12, 0.1, "square"), tone(220, 220, 0.18, 0.12, "square")]) * 0.35
    raise ValueError(kind)

def render(cues, per, off, dur, out_wav):
    y = np.zeros((int(dur * SR) + SR, ))
    for i, (b, kind, g) in enumerate(cues):
        s = make(kind, i); st = int((off + b * per) * SR)
        if st < 0 or st >= len(y): continue
        e = min(len(y), st + len(s)); y[st:e] += s[:e - st] * g
    y = y[:int(dur * SR)]
    y = y / max(1e-9, np.abs(y).max()) * 0.5
    import wave
    pcm = (np.clip(y, -1, 1) * 32767).astype(np.int16)
    st = np.stack([pcm, pcm], 1)
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
