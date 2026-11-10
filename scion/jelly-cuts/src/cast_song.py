"""Cast a song for the Jelly Orchestra: onset analysis by sound role -> events per role.
usage: python3 -I cast_song.py <config.json>"""
import sys, json, numpy as np, librosa
cfg = json.load(open(sys.argv[1]))
y, sr = librosa.load(cfg["audio"], sr=22050, mono=True)
H = 256
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=H)); f = librosa.fft_frequencies(sr=sr, n_fft=2048)
t = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr, hop_length=H)
per = 60.0 / cfg["bpm"]; off = cfg["offset"]
def band_onsets(lo, hi, delta, wait_s, d, gain_floor=-16):
    B = S[(f >= lo) & (f < hi)]
    env = np.maximum(0, np.diff(np.log1p(B.sum(0)), prepend=0))
    env = env / (np.percentile(env, 99.5) + 1e-9)
    pk = librosa.util.peak_pick(env, pre_max=3, post_max=3, pre_avg=12, post_avg=12, delta=delta, wait=int(wait_s * sr / H))
    out = []
    for p in pk:
        g = gain_floor + 16 * min(1, env[p])
        out.append([round(float(t[p]), 4), d, round(float(g), 2)])
    return out
yh, yp = librosa.effects.hpss(y)
def harm_events(lo, hi, d, every_beats):
    Sh = np.abs(librosa.stft(yh, n_fft=2048, hop_length=H)); B = Sh[(f >= lo) & (f < hi)].sum(0)
    rms = B / (B.max() + 1e-9); out = []
    nb = int((t[-1] - off) / per)
    for b in range(0, nb, every_beats):
        tt = off + b * per; i = np.searchsorted(t, tt)
        seg = rms[i:i + int(every_beats * per * sr / H)]
        if len(seg) and seg.mean() > 0.12:
            out.append([round(tt, 4), d, round(-16 + 16 * float(min(1, seg.mean() * 1.6)), 2)])
    return out
roles = {
    "kick": band_onsets(30, 140, 0.25, per * 0.45, 0.35),
    "snare": band_onsets(1500, 4500, 0.3, per * 0.45, 0.3),
    "hat": band_onsets(7000, 11000, 0.25, per * 0.2, 0.18),
    "bass": harm_events(40, 220, round(per * 2, 3), 2),
    "choir": harm_events(300, 1800, round(per * 4, 3), 4),
    "bed": harm_events(1800, 6000, round(per * 8, 3), 8),
}
# 'call': the strongest phrase onsets of the full-band harmonic part (one per bar at most)
env = librosa.onset.onset_strength(y=yh, sr=sr, hop_length=H); env = env / (env.max() + 1e-9)
pk = librosa.util.peak_pick(env, pre_max=20, post_max=20, pre_avg=40, post_avg=40, delta=0.2, wait=int(per * 4 * sr / H))
roles["call"] = [[round(float(t[p]), 4), round(per, 3), round(-14 + 14 * float(env[p]), 2)] for p in pk]
dur = float(len(y) / sr)
out = {"id": cfg["id"], "title": cfg["title"], "bpm": cfg["bpm"], "offset": off, "duration": dur, "roles": roles,
       "method": "librosa band onsets (kick 30-140 Hz, snare 1.5-4.5 kHz, hat 7-11 kHz), HPSS harmonic energy per 2/4/8 beats (bass/choir/bed), harmonic onset peaks per bar (call)"}
json.dump(out, open(cfg["cast"], "w"))
print({k: len(v) for k, v in roles.items()}, "dur", round(dur, 2))
