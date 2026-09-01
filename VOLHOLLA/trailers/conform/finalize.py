import sys, subprocess
sys.path.insert(0,"/tmp/claude-0/-home-user/afaa256a-e659-532b-b1c4-9119d1c62670/scratchpad")
from cutbastard import FF, AUD, W, H, SCOPE_H
GR={
 "A":("eq=contrast=1.16:saturation=1.14:gamma=0.98,"
      "colorbalance=rs=0.06:gs=0.02:bs=-0.09:rm=0.05:bm=-0.06:rh=0.04:bh=-0.05,"
      "curves=r='0/0.02 0.5/0.54 1/1':g='0/0.015 0.5/0.5 1/0.985':b='0/0.03 0.5/0.46 1/0.95',"
      "unsharp=5:5:0.5,noise=alls=2:allf=t"),
 "B":("eq=contrast=1.28:saturation=0.66:gamma=0.94,"
      "colorbalance=rs=-0.07:bs=0.14:rm=-0.05:bm=0.08:rh=-0.03:bh=0.05,"
      "curves=r='0/0 0.5/0.46 1/0.96':g='0/0.01 0.5/0.5 1/0.99':b='0/0.05 0.5/0.56 1/1',"
      "unsharp=5:5:0.6,noise=alls=3:allf=t"),
}
def fin(name,song,total,fo,out,grade):
    W_="/tmp/claude-0/-home-user/afaa256a-e659-532b-b1c4-9119d1c62670/scratchpad/build"
    vf=(f"{GR[grade]},pad={W}:{H}:0:{(H-SCOPE_H)//2}:black,"
        f"fade=t=in:st=0:d=0.8,fade=t=out:st={total-fo:.3f}:d={fo}")
    af=(f"afade=t=in:st=0:d=0.35,afade=t=out:st={total-fo:.3f}:d={fo},"
        f"loudnorm=I=-14:TP=-1.2:LRA=11")
    c=[FF,"-y","-loglevel","error","-i",f"{W_}/{name}/picture.mp4",
       "-ss","0","-t",f"{total:.4f}","-i",f"{AUD}/{song}",
       "-vf",vf,"-af",af,"-map","0:v","-map","1:a",
       "-c:v","libx264","-crf","25","-preset","slow",
       "-maxrate","2900k","-bufsize","5800k","-profile:v","high","-level","4.1",
       "-pix_fmt","yuv420p","-x264-params","keyint=48:min-keyint=24",
       "-c:a","aac","-b:a","160k","-ar","48000","-movflags","+faststart","-shortest",out]
    r=subprocess.run(c,capture_output=True,text=True)
    print(name, r.returncode, r.stderr[-800:] if r.returncode else "OK")
if __name__=="__main__":
    which=sys.argv[1]
    if which=="A":
        fin("A","The Chapel Ring - The PhD of Musk - Treblo.ogg",70.64985,2.2,
            "/home/user/moto/VOLHOLLA/trailers/trailer-chapelring-34-phd-of-musk.mp4","A")
    else:
        fin("B","The Chapel Ring - Ancient Law, New Fine Print - Treblo.ogg",78.39734,2.4,
            "/home/user/moto/VOLHOLLA/trailers/trailer-chapelring-02-ancient-law.mp4","B")
