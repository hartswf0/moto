import sys; sys.path.insert(0,"/tmp/claude-0/-home-user/afaa256a-e659-532b-b1c4-9119d1c62670/scratchpad")
from cutbastard import assemble
C="/tmp/claude-0/-home-user/afaa256a-e659-532b-b1c4-9119d1c62670/scratchpad/cards"
B=60/103.10   # 0.58197s
def S(p,beats,**k): 
    d=dict(p=p,dur=beats*B); d.update(k); return d
E=[]
# ACT 0 — COLD OPEN (17.4b)  music 0.000 -> 10.128
E+=[S(f"CARD:{C}/volholla.png",1.4),
    S("P3A",4,speed=0.86,off=0.0),          # ranger-hat ECU sinks, gallery reveals
    S("P1F",4,speed=0.358),                 # honey pours over lectern, slow
    S("P5A",4,speed=0.72),                  # POV aisle approach
    S("P1C",4,speed=0.644)]                 # archive of portraits on screen
# ACT 1 — THE SCHOLAR (24b) -> 24.095
E+=[S("P1A",3,speed=0.835), S("P2C",2,speed=1.0,off=0.35), S("P1D",2,speed=1.0,off=0.10),
    S("P1B",2,speed=1.0),   S("P3B",3,speed=1.0,off=0.20), S("P2A",2,speed=1.0,off=0.20),
    S("P1E",2,speed=1.0),   S("P6A",2,speed=1.0,off=0.40), S("P2B",3,speed=1.0,off=0.15),
    S("P1C",3,speed=0.86,zoom=1.5)]
# ACT 2 — ESCALATION (28b) -> 40.390
E+=[S("P5B",2,speed=1.0,off=0.2), S("P4B",1.5,speed=1.0), S("P2D",1.5,speed=1.0,off=0.3),
    S("P1E",1,zoom=1.8,off=0.5),  S("P6C",1,off=0.3),      S("P3C",1,off=1.2),
    S("P2A",1,zoom=1.4,off=1.0),  S("P1F",4,speed=0.358),
    S("P6B",1.5,off=0.3),         S("P4C",1.5,off=0.5),    S("P2C",1,zoom=1.5,off=1.2),
    S("P1A",1,zoom=1.6,off=0.6),  S("P5C",1,off=0.4),      S("P6A",1,zoom=1.5,off=1.0),
    S("P3A",2,speed=1.0,off=1.9), S("P2B",2,speed=1.0,off=0.8), S("P1C",4,speed=0.644,zoom=1.2)]
# ACT 3 — THE BURST (28b) -> 56.685
E+=[S("P1A",.5,zoom=2.0,off=.3), S("P2A",.5,zoom=1.6,off=.6), S("P4A",.5,zoom=1.3,off=.3),
    S("P6A",.5,zoom=1.8,off=.6), S("P3B",1,zoom=1.2,off=.5), S("P5D",1,off=.3),
    S("P2C",.5,zoom=1.9,off=1.4),S("P1E",.5,zoom=2.0,off=.7),S("P4C",.5,zoom=1.5,off=1.2),
    S("P6C",.5,zoom=1.6,off=.8), S("P2B",1,zoom=1.3,off=1.2),S("P1D",1,zoom=1.5,off=.6),
    S("P3C",.5,zoom=1.4,off=2.0),S("P2D",.5,zoom=1.7,off=1.0),S("P1B",.5,zoom=1.8,off=.7),
    S("P5A",.5,zoom=1.4,off=1.6,rev=True), S("P6B",1,zoom=1.4,off=1.6), S("P1F",1,speed=0.5,zoom=1.5),
    S("P2A",.5,zoom=2.2,off=1.4),S("P4B",.5,zoom=1.6,off=2.6),S("P1A",.5,zoom=2.4,off=.9),
    S("P6A",.5,zoom=2.0,off=1.4),S("P3A",1,zoom=1.6,off=2.2), S("P2C",1,zoom=1.4,off=.2),
    S("P5C",1,zoom=1.3,off=.8),  S("P1E",2,zoom=1.2),        S("P2D",2,speed=1.0,off=1.0),
    S("P6D",2,speed=1.0,off=.2), S("P5D",2,speed=1.0,off=.6),S("P3A",1,zoom=2.2,off=.2),
    S("P1F",2,speed=0.358)]
# ACT 4 — TITLE + PAYOFF (24b) -> 70.652
E+=[S("BLACK",1),
    S(f"CARD:{C}/a_album.png",2),
    S("P2C",2,speed=1.0),          S("P1E",2,speed=1.0),  S("P5D",2,speed=0.8),
    S("BLACK",.5),
    S(f"CARD:{C}/a_title.png",5),
    S("P1F",2.5,speed=0.358),
    S(f"CARD:{C}/a_url.png",3),
    S("BLACK",4)]
print("beats:",sum(s["dur"] for s in E)/B, "sec:",sum(s["dur"] for s in E))
assemble("A",E,"The Chapel Ring - The PhD of Musk - Treblo.ogg",0.0,"A",
         "/home/user/moto/VOLHOLLA/trailers/trailer-chapelring-34-phd-of-musk.mp4",fade_out=2.2)
