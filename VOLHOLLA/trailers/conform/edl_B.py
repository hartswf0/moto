import sys; sys.path.insert(0,"/tmp/claude-0/-home-user/afaa256a-e659-532b-b1c4-9119d1c62670/scratchpad")
from cutbastard import assemble
C="/tmp/claude-0/-home-user/afaa256a-e659-532b-b1c4-9119d1c62670/scratchpad/cards"
B=60/127.90   # 0.46912s
def S(p,beats,**k):
    d=dict(p=p,dur=beats*B); d.update(k); return d
E=[]
# ACT 0 — MACHINE OPEN (3.117b pickup + 24b) music 0.000 -> 12.721
E+=[S(f"CARD:{C}/volholla.png",3.117),
    S("P5A",5,speed=0.5),               # POV aisle, crawl
    S("P4A",4,speed=0.5),               # Puddle-Soot ECU + its own caption
    S("P6D",5,speed=0.7),               # wide stage, waveform wall
    S("P3A",5,speed=0.9,off=1.2),       # gallery reveal
    S("P5B",5,speed=0.75)]              # paws enter POV frame
# ACT 1 — THE INSTRUMENT (32b) -> 27.733
E+=[S("P4B",4,speed=1.0),          S("P6B",3,speed=1.0,off=0.2), S("P2B",3,speed=1.0,off=0.1),
    S("P5C",3,speed=1.0,off=0.1),  S("P3B",3,speed=1.0,off=0.3), S("P6A",2,speed=1.0,off=0.5),
    S("P4C",3,speed=1.0,off=0.3),  S("P1C",3,speed=0.9,zoom=1.3),S("P2A",2,speed=1.0,off=0.4),
    S("P5D",3,speed=1.0,off=0.2),  S("P3C",3,speed=1.0,off=1.5)]
# ACT 2 — FINE PRINT (32b) -> 42.745
E+=[S("P4A",2,zoom=1.5,off=0.4), S("P6C",2,off=0.2),        S("P5A",2,zoom=1.3,off=1.0),
    S("P2B",2,zoom=1.4,off=1.0), S("P1E",1.5,zoom=1.6,off=0.4), S("P4B",1.5,zoom=1.3,off=1.8),
    S("P6B",1.5,zoom=1.5,off=1.2),S("P3C",1.5,zoom=1.3,off=0.5),S("P5C",2,zoom=1.2,off=0.9),
    S("P4C",2,zoom=1.4,off=1.4), S("P2D",2,off=0.5),        S("P6D",2,zoom=1.3,off=0.4),
    S("P1F",4,speed=0.4),        S("P5B",2,zoom=1.2,off=0.3,rev=True), S("P3A",4,speed=0.9,off=2.0)]
# ACT 3 — PRE-BREAKDOWN BURST (16b) -> 50.251
E+=[S("P4A",.5,zoom=1.8,off=.6), S("P6A",.5,zoom=1.9,off=.9), S("P2B",.5,zoom=1.6,off=1.5),
    S("P5D",.5,zoom=1.4,off=.9), S("P3B",.5,zoom=1.5,off=1.2),S("P4C",.5,zoom=1.7,off=1.8),
    S("P1A",.5,zoom=2.0,off=.5), S("P6C",.5,zoom=1.8,off=1.0),S("P2A",.5,zoom=1.9,off=1.2),
    S("P5A",.5,zoom=1.5,off=2.0),S("P3C",.5,zoom=1.6,off=2.4),S("P4B",.5,zoom=2.0,off=3.0),
    S("P2C",.5,zoom=1.7,off=1.5),S("P6B",.5,zoom=1.7,off=2.0),S("P1E",.5,zoom=2.2,off=.8),
    S("P5C",.5,zoom=1.6,off=1.3),
    S("P4A",1,zoom=1.2,off=.2),  S("P2D",1,off=1.2),         S("P6D",1,off=.8),
    S("P5D",1,zoom=1.1,off=.1),  S("P3A",1,zoom=2.0,off=2.4),S("P4C",1,zoom=1.2,off=1.0),
    S("P1F",1,speed=.5,zoom=1.4),S("P5A",1,zoom=1.3,off=2.0)]
# ACT 4 — BREAKDOWN / TITLE (16b) -> 57.757   [music drops out here]
E+=[S("BLACK",1),
    S("P4A",4,speed=0.4,zoom=1.15),
    S("BLACK",.5),
    S(f"CARD:{C}/b_title.png",8),
    S("BLACK",2.5)]
# ACT 5 — RETURN (44b) -> 78.398
E+=[S("P5A",3,speed=0.8),   S("P6A",2,off=.4),  S("P4B",2,off=1.2), S("P2B",2,off=.6),
    S("P5C",2,off=.3),      S("P3B",2,off=.6),  S("P6C",2,off=.5),  S("P4C",2,off=.8),
    S("P2C",2,off=.6),      S("P1E",1.5,zoom=1.4), S("P5D",1.5,off=.4), S("P6B",1.5,off=1.0),
    S("P3C",1.5,off=1.0),   S("P2A",1.5,off=.3),S("P4A",1,zoom=1.5,off=.3), S("P6D",1,off=.3),
    S("P5B",1,off=.8),      S("P2D",1,off=1.0), S("P1F",3,speed=.4), S("P5A",3,speed=.7,off=1.4),
    S("BLACK",.5),
    S(f"CARD:{C}/b_url.png",4),
    S("BLACK",3)]
print("beats:",round(sum(s["dur"] for s in E)/B,3), "sec:",sum(s["dur"] for s in E))
assemble("B",E,"The Chapel Ring - Ancient Law, New Fine Print - Treblo.ogg",0.0,"B",
         "/home/user/moto/VOLHOLLA/trailers/trailer-chapelring-02-ancient-law.mp4",fade_out=2.4)
