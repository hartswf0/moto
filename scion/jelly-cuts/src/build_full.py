"""Full-resolution bloom frames (the user's call, r4: 'flecks in transit only' - at the bloom the picture resolves to the
real frame, the WYGWYL dot law deliberately suspended at the peak). One folder per memory: f0000.jpg... at 12 fps,
same crop as its fleck bank. usage: python3 -I build_full.py <bank-spec.json> <outdir>"""
import sys, os, json, subprocess
from PIL import Image
spec = json.load(open(sys.argv[1])); out = sys.argv[2]; man = {}
for f in spec["films"]:
    d = os.path.join(out, f["id"]); os.makedirs(d, exist_ok=True); s = f["source"]; crop = f.get("crop")
    n = int(round(f["dur"] * 12))
    if s["kind"] == "film":
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{f['src_t0']:.3f}", "-t", f"{f['dur']:.3f}", "-i", s["mp4"], "-vf", ("fps=12," + (f"crop=iw*{crop[2]-crop[0]}:ih*{crop[3]-crop[1]}:iw*{crop[0]}:ih*{crop[1]}," if crop else "") + "scale=640:-2"), "-q:v", "4", os.path.join(d, "f%04d.jpg")], check=True)
        n = len(os.listdir(d)); files = sorted(os.listdir(d)); [os.rename(os.path.join(d, x), os.path.join(d, f"f{i:04d}.jpg")) for i, x in enumerate(files)]
    elif s["kind"] == "still":
        im = Image.open(s["image"]).convert("RGB")
        if crop: w, h = im.size; im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        im.thumbnail((900, 900)); im.save(os.path.join(d, "f0000.jpg"), quality=88); n = 1
    else:
        fs = sorted(x for x in os.listdir(s["frames"]) if x.endswith(".jpg")); m = len(fs)
        for i in range(n):
            k = i % max(1, 2 * m - 2); k = k if k < m else 2 * m - 2 - k
            im = Image.open(os.path.join(s["frames"], fs[k])).convert("RGB")
            if crop: w, h = im.size; im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
            im.resize((im.width * 2, im.height * 2), Image.LANCZOS).save(os.path.join(d, f"f{i:04d}.jpg"), quality=86)
    w, h = Image.open(os.path.join(d, "f0000.jpg")).size
    man[f["id"]] = {"n": n, "w": w, "h": h, "aspect": h / w}
    print(f["id"], n, w, h)
json.dump(man, open(os.path.join(out, "full.json"), "w"), indent=1)
