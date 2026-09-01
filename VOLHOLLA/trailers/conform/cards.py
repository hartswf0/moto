from PIL import Image, ImageDraw, ImageFont
import os
W,H=1920,804
OUT="/tmp/claude-0/-home-user/afaa256a-e659-532b-b1c4-9119d1c62670/scratchpad/cards"
os.makedirs(OUT,exist_ok=True)
SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONOB="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def track(d,txt,font,sp,fill,cx,y,anchor="mm"):
    ws=[d.textlength(c,font=font) for c in txt]
    tot=sum(ws)+sp*(len(txt)-1)
    x=cx-tot/2
    for c,w in zip(txt,ws):
        d.text((x,y),c,font=font,fill=fill,anchor="lm"); x+=w+sp
    return tot

def card(name,lines,bg=(0,0,0),rule=None):
    im=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(im)
    for L in lines:
        f=ImageFont.truetype(L.get("font",MONO),L["size"])
        track(d,L["t"],f,L.get("sp",0),L.get("fill",(232,228,218)),W/2,L["y"])
    if rule:
        y=rule; d.line([(W/2-260,y),(W/2+260,y)],fill=(120,112,96),width=2)
    p=f"{OUT}/{name}.png"; im.save(p); return p

# --- label / open cards
card("volholla",[{"t":"V O L H O L L A","size":44,"font":MONO,"sp":10,"fill":(150,144,132),"y":402}])

# --- TRAILER A (track 34)
card("a_album",[{"t":"THE CHAPEL RING","size":56,"font":MONO,"sp":16,"fill":(214,176,104),"y":402}])
card("a_title",[
 {"t":"THE CHAPEL RING","size":30,"font":MONO,"sp":14,"fill":(150,128,84),"y":300},
 {"t":"The PhD of Musk","size":124,"font":SERIF,"sp":2,"fill":(240,232,214),"y":400},
 {"t":"TRACK 34 OF 42","size":26,"font":MONO,"sp":10,"fill":(126,120,108),"y":492}],rule=352)
card("a_url",[
 {"t":"hartswf0.github.io/moto/VOLHOLLA","size":30,"font":MONO,"sp":4,"fill":(168,160,146),"y":402}])

# --- TRAILER B (track 02)
card("b_album",[{"t":"THE CHAPEL RING","size":56,"font":MONO,"sp":16,"fill":(126,178,206),"y":402}])
card("b_title",[
 {"t":"THE CHAPEL RING","size":30,"font":MONO,"sp":14,"fill":(92,132,156),"y":292},
 {"t":"Ancient Law,","size":110,"font":SERIF,"sp":2,"fill":(228,236,240),"y":388},
 {"t":"New Fine Print","size":110,"font":SERIF,"sp":2,"fill":(228,236,240),"y":492},
 {"t":"TRACK 02 OF 42","size":26,"font":MONO,"sp":10,"fill":(110,124,134),"y":580}],rule=340)
card("b_url",[
 {"t":"hartswf0.github.io/moto/VOLHOLLA","size":30,"font":MONO,"sp":4,"fill":(150,166,176),"y":402}])
print("cards ok", len(os.listdir(OUT)))
