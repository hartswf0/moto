"""Motion on the RENDERED mp4: mean |frame - previous frame| on greyscale (0-255), per 4 s and per 1 s window."""
import sys, subprocess, json, numpy as np
def per_frame(path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    prev, d = None, []
    while True:
        buf = p.stdout.read(1280 * 720)
        if len(buf) < 1280 * 720: break
        a = np.frombuffer(buf, np.uint8).astype(np.int16)
        if prev is not None: d.append(float(np.abs(a - prev).mean()))
        prev = a
    return np.array(d)          # d[i] = diff between frame i+1 and i
def windows(d, size):
    n = int(len(d) / 24 / size)
    return [round(float(d[int(k * size * 24):int((k + 1) * size * 24)].mean()), 3) for k in range(n)]
if __name__ == "__main__":
    d = per_frame(sys.argv[1])
    w4 = windows(d, 4); w1 = windows(d, 1)
    json.dump({"w4": w4, "w1": w1}, open(sys.argv[2], "w"))
    print("4s:", {f"{4*k}-{4*k+4}": v for k, v in enumerate(w4)})
    print("1s 148-163:", {f"{k}": w1[k] for k in range(148, 163)})
