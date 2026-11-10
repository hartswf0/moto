"""contact sheet at times in seconds: python3 -I sheet_s.py in.mp4 out.jpg t1 t2 ..."""
import sys, subprocess, io
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]; ts = [float(x) for x in sys.argv[3:]]; ims = []
for t in ts:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    im = Image.open(io.BytesIO(raw)).convert("RGB").resize((480, 270)); d = ImageDraw.Draw(im); d.rectangle([0, 0, 64, 18], fill=(0, 0, 0)); d.text((4, 3), f"{t:.1f}s", fill=(255, 220, 80)); ims.append(im)
c = 4; r = (len(ims) + c - 1) // c; s = Image.new("RGB", (480 * c, 270 * r))
for i, im in enumerate(ims): s.paste(im, ((i % c) * 480, (i // c) * 270))
s.save(out, quality=82)
