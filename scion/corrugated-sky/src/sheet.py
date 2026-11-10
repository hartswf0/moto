"""Contact sheet from an mp4 at given beats: python3 -I sheet.py in.mp4 out.jpg start_beat b1 b2 ..."""
import sys, subprocess, json, os
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
g = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "beatgrid.json")))["grid"]
src, out, start = sys.argv[1], sys.argv[2], float(sys.argv[3]); beats = [float(x) for x in sys.argv[4:]]
t0 = g["offset"] + start * g["period"]
ims = []
for b in beats:
    t = g["offset"] + b * g["period"] - t0
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0,t):.3f}", "-i", src, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    import io; im = Image.open(io.BytesIO(raw)).convert("RGB").resize((480, 270))
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 150, 22], fill=(0, 0, 0)); d.text((4, 4), f"b{b:g}  t={g['offset']+b*g['period']:.2f}s", fill=(255, 255, 0))
    ims.append(im)
cols = 4; rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (480 * cols, 270 * rows), "black")
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 480, (i // cols) * 270))
sh.save(out, quality=82)
