#!/usr/bin/env python3
"""CUTBASTARD-1 conform engine. Patch table -> ffmpeg intermediates -> concat -> grade -> mux."""
import os, subprocess, sys, json, shutil
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
SRCDIR = "/root/.claude/uploads/afaa256a-e659-532b-b1c4-9119d1c62670"
WORK = "/tmp/claude-0/-home-user/afaa256a-e659-532b-b1c4-9119d1c62670/scratchpad/build"
AUD = "/home/user/moto/THE CHAPEL RING"
FPS = 24; W, H = 1920, 1080
SCOPE_H = 804  # 2.39:1 letterbox window

SRC = {
 "V1": f"{SRCDIR}/25368d03-473503322_1788283453982079.mp4",
 "V2": f"{SRCDIR}/32c2f117-132443478_1788283462732469.mp4",
 "V3": f"{SRCDIR}/88c63c54-367487608_1788283457127939.mp4",
 "V4": f"{SRCDIR}/98c6c4b5-460024827_1788283455915708.mp4",
 "V5": f"{SRCDIR}/eb61047a-789239680_1788283460779491.mp4",
 "V6": f"{SRCDIR}/fe6973b0-217358703_1788283458884835.mp4",
}
# patch_id -> (src, in, out)  [source seconds, 8.000s clips]
PATCH = {
 "P1A":("V1",0.000,1.458), "P1B":("V1",1.458,2.958), "P1C":("V1",2.958,4.458),
 "P1D":("V1",4.458,5.917), "P1E":("V1",5.917,7.167), "P1F":("V1",7.167,8.000),
 "P2A":("V2",0.000,2.000), "P2B":("V2",2.000,4.000), "P2C":("V2",4.000,6.000), "P2D":("V2",6.000,8.000),
 "P3A":("V3",0.000,3.042), "P3B":("V3",3.042,5.000), "P3C":("V3",5.000,8.000),
 "P4A":("V4",0.000,1.500), "P4B":("V4",1.500,5.458), "P4C":("V4",5.458,8.000),
 "P5A":("V5",0.000,2.600), "P5B":("V5",2.600,4.400), "P5C":("V5",4.400,6.300), "P5D":("V5",6.300,8.000),
 "P6A":("V6",0.000,1.958), "P6B":("V6",1.958,4.458), "P6C":("V6",4.458,6.500), "P6D":("V6",6.500,8.000),
}

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)[:400]); print(r.stderr[-2500:]); sys.exit(1)

def vf_chain(zoom, panx, pany, rev, flip):
    """crop-to-scope with punch-in reframe, then scale to 1920x804."""
    f = []
    # source is 1280x720. crop a scope window of height 536/zoom
    cw, ch = 1280.0/zoom, 536.0/zoom
    x = (1280-cw)/2 + panx*(1280-cw)/2
    y = (720-ch)/2 + pany*(720-ch)/2
    x = max(0, min(1280-cw, x)); y = max(0, min(720-ch, y))
    f.append(f"crop={cw:.0f}:{ch:.0f}:{x:.0f}:{y:.0f}")
    if flip: f.append("hflip")
    f.append(f"scale={W}:{SCOPE_H}:flags=lanczos")
    return f

def build_seg(idx, seg, outdir):
    pid = seg["p"]
    dur = seg["dur"]
    out = f"{outdir}/s{idx:03d}.mp4"
    if pid == "BLACK":
        run([FF,"-y","-loglevel","error","-f","lavfi","-i",
             f"color=c=black:s={W}x{SCOPE_H}:r={FPS}:d={dur:.4f}",
             "-c:v","libx264","-crf","14","-preset","veryfast","-pix_fmt","yuv420p", out])
        return out
    if pid.startswith("CARD:"):
        png = pid.split(":",1)[1]
        run([FF,"-y","-loglevel","error","-loop","1","-t",f"{dur:.4f}","-i",png,
             "-vf",f"scale={W}:{SCOPE_H},fps={FPS},format=yuv420p",
             "-c:v","libx264","-crf","14","-preset","veryfast", out])
        return out
    src, si, so = PATCH[pid]
    avail = so - si
    speed = seg.get("speed")
    if speed is None:
        speed = avail/dur          # consume whole patch across dur
        speed = max(0.28, min(3.2, speed))
    src_len = dur*speed
    if src_len > avail:            # clamp, re-derive speed
        src_len = avail; speed = src_len/dur
    ss = si + seg.get("off",0.0)
    if ss + src_len > so: ss = so - src_len
    vf = ",".join(vf_chain(seg.get("zoom",1.0), seg.get("px",0.0), seg.get("py",0.0),
                  seg.get("rev",False), seg.get("flip",False)))
    chain = vf + (",reverse" if seg.get("rev") else "")
    chain += f",setpts={dur/src_len:.6f}*(PTS-STARTPTS),fps={FPS}"
    cmd = [FF,"-y","-loglevel","error","-ss",f"{ss:.4f}","-t",f"{src_len:.4f}","-i",SRC[src],
           "-an","-vf",chain,"-t",f"{dur:.4f}",
           "-c:v","libx264","-crf","14","-preset","veryfast","-pix_fmt","yuv420p", out]
    run(cmd)
    return out

GRADES = {
 # honey / amber / gold — the scholar
 "A": ("eq=contrast=1.16:saturation=1.14:gamma=0.98,"
       "colorbalance=rs=0.06:gs=0.02:bs=-0.09:rm=0.05:bm=-0.06:rh=0.04:bh=-0.05,"
       "curves=r='0/0.02 0.5/0.54 1/1':g='0/0.015 0.5/0.5 1/0.985':b='0/0.03 0.5/0.46 1/0.95',"
       "unsharp=5:5:0.5,noise=alls=6:allf=t+u"),
 # cold steel / cyan / crushed — the machine
 "B": ("eq=contrast=1.28:saturation=0.66:gamma=0.94,"
       "colorbalance=rs=-0.07:bs=0.14:rm=-0.05:bm=0.08:rh=-0.03:bh=0.05,"
       "curves=r='0/0 0.5/0.46 1/0.96':g='0/0.01 0.5/0.5 1/0.99':b='0/0.05 0.5/0.56 1/1',"
       "unsharp=5:5:0.6,noise=alls=8:allf=t+u"),
}

def assemble(name, segs, song, music_in, grade, outfile, fade_out=1.6):
    outdir = f"{WORK}/{name}"
    shutil.rmtree(outdir, ignore_errors=True); os.makedirs(outdir, exist_ok=True)
    files = [build_seg(i, s, outdir) for i, s in enumerate(segs)]
    total = sum(s["dur"] for s in segs)
    with open(f"{outdir}/list.txt","w") as fh:
        for f in files: fh.write(f"file '{f}'\n")
    run([FF,"-y","-loglevel","error","-f","concat","-safe","0","-i",f"{outdir}/list.txt",
         "-c","copy",f"{outdir}/picture.mp4"])
    g = GRADES[grade]
    vf = (f"{g},pad={W}:{H}:0:{(H-SCOPE_H)//2}:black,"
          f"fade=t=in:st=0:d=0.8,fade=t=out:st={total-fade_out:.3f}:d={fade_out}")
    af = (f"afade=t=in:st=0:d=0.35,afade=t=out:st={total-fade_out:.3f}:d={fade_out},"
          f"loudnorm=I=-14:TP=-1.2:LRA=11")
    run([FF,"-y","-loglevel","error","-i",f"{outdir}/picture.mp4",
         "-ss",f"{music_in:.4f}","-t",f"{total:.4f}","-i",f"{AUD}/{song}",
         "-vf",vf,"-af",af,"-map","0:v","-map","1:a",
         "-c:v","libx264","-crf","19","-preset","slow","-profile:v","high","-level","4.1",
         "-pix_fmt","yuv420p","-x264-params","keyint=48:min-keyint=24",
         "-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",
         "-shortest", outfile])
    print(f"[OK] {outfile}  {total:.2f}s  {len(segs)} events")
    return total
