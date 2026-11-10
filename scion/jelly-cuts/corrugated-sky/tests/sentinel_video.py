"""Sentinel brightness on RENDERED frames: p90 of a crop at its bell, kick frame vs the 2 frames before.
usage: python3 -I tests/sentinel_video.py <video> <t0>"""
import sys, os, json, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
import jellycut as J
J.init(os.path.join(HERE, "..", "jellycut.json")); vid, t0 = sys.argv[1], float(sys.argv[2])
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, 720, 1280); sw = []
for tk in J.KICKS:
    if not (t0 + .3 < tk < t0 + len(V) / 24 - .3): continue
    f = int(round((tk - t0) * 24)); x, y, r = J.jelly("kick0", tk, window=0.0); RR = int(max(24, r * 1.6))
    cr = lambda k: V[k, max(0, int(y) - RR):int(y) + RR, max(0, int(x) - RR):int(x) + RR].astype(float)
    pre = min(np.percentile(cr(k), 90) for k in (f - 2, f - 1)); pk = max(np.percentile(cr(k), 90) for k in (f, f + 1)); sw.append((pk - pre) / max(1, pre))
res = {"kicks": len(sw), "min_swing": round(float(min(sw)), 3), "median": round(float(np.median(sw)), 3), "pass": bool(sw and min(sw) >= .15)}
print(res); json.dump(res, open(os.path.join(HERE, "sentinel_video.json"), "w"))
