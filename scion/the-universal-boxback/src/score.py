"""Tuned punctuation for the event list (Ab major pentatonic, the song's measured key). Original synthesis."""
import numpy as np, wave
SR = 44100
NOTES = {"Ab4": 415.30, "C5": 523.25, "Eb5": 622.25, "F5": 698.46, "Bb5": 932.33, "Ab5": 830.61, "C6": 1046.5, "Eb4": 311.13, "Ab3": 207.65, "Ab2": 103.83}
PENTA = ["Ab4", "Bb5", "C5", "Eb5", "F5", "Ab5", "C6", "Eb5", "F5", "Ab5"]

def bell(f, dur=1.2, d=0.5, amp=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    env = np.minimum(1, t / 0.004) * np.exp(-t / d)
    return amp * env * (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2.01 * f * t) + 0.12 * np.sin(2 * np.pi * 3.02 * f * t))

def click(seed):
    r = np.random.default_rng(seed).normal(0, 1, int(0.02 * SR)); return r * np.exp(-np.arange(len(r)) / (0.003 * SR)) * 0.25

def cue_list(events, typing):
    cues = []
    for e in events:
        k = e["kind"]
        if k == "reunion": cues += [(e["b"], "Ab4", 0.35), (e["b"], "C5", 0.3), (e["b"], "Eb5", 0.3)]
        elif k == "interference": cues.append((e["b"], PENTA[e["m"]], 0.22))
        elif k == "lock": cues += [(e["b"], "Ab5", 0.25), (e["b"], "Eb5", 0.2)]
        elif k == "unlock": cues += [(e["b"], "Bb5", 0.22), (e["b"] + 0.25, "F5", 0.18)]
        elif k == "relock": cues += [(e["b"], "Ab4", 0.3), (e["b"], "C5", 0.25), (e["b"], "Eb5", 0.25)]
        elif k == "rain": cues.append((e["b"], ["Ab3", "Eb4", "Ab4", "C5", "Eb5", "F5"][[0, 0, 0, 0, 1, 1, 1, 0, 1, 4, 4, 4, 2, 2, 3, 3, 3, 3, 5, 5][int(e["id"])]], 0.22))
        elif k == "land": cues.append((e["b"], ["Ab3", "Eb4", "Ab4", "C5", "Eb5", "F5"][min(5, int(e["id"]) // 4)], 0.22))
        elif k == "collision": cues += [(e["b"], "Ab4", 0.3), (e["b"], "Bb5", 0.3), (e["b"] + 0.02, "C6", 0.25)]
        elif k == "reseat": cues.append((e["b"], "Eb5", 0.25))
        elif k == "beam_lands": cues += [(e["b"], "Ab3", 0.4), (e["b"], "Eb4", 0.3), (e["b"], "C5", 0.3), (e["b"], "Ab5", 0.25)]
        elif k == "home": cues += [(e["b"], n, 0.3) for n in ("Ab2", "Ab3", "Eb4", "C5", "Eb5", "Ab5")]
    cues += [(b, "click", 1.0) for b in typing]
    return cues

def render(cues, per, off, dur, path):
    y = np.zeros(int(dur * SR) + SR)
    for i, (b, n, g) in enumerate(cues):
        s = click(i) if n == "click" else bell(NOTES[n], amp=g)
        st = int((off + b * per) * SR)
        if 0 <= st < len(y):
            e = min(len(y), st + len(s)); y[st:e] += s[:e - st]
    y = y[:int(dur * SR)]; y = y / max(1e-9, np.abs(y).max()) * 0.6
    pcm = (np.clip(y, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([pcm, pcm], 1).tobytes())
