"""Corrugated Sky jelly cut, r2: one source of truth for BOTH the orchestra stage directions (direct.json) and the
compositor timeline (jellycut.json). Every held film is a performance by its jelly:
  attention (the jelly turns toward the camera and pulses faster, >=1.5 s BEFORE the film condenses)
  -> intention/gesture (the film condenses hanging from its bell; it moves with the bell)
  -> resistance (the hold: extra pulses on every beat while it carries the picture)
  -> changed state (after the release the jelly drifts to a new place and the extra pulses stop, >= 2 bars).
Run: python3 -I build_cut.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
BPM, OFF = 141.05, 0.345
PER = 60 / BPM; BAR = 4 * PER
def beat_t(b): return OFF + b * PER
LETGO = 73.5 + 272 / 24          # film second at which the girl's hand opens (critic-verified proof frame 272)

K = "/home/user/hartswf0/bolas/paeleo/handmade/"
SAAM = K + "49-open-content-atelier/sources/media/"
SM = "/home/user/secondhand-motion/shots/"
SOURCES = {
    "film": {"kind": "film", "npy": "/home/user/moto/scion/jelly-cuts/work/corrugated-sky-film.npy"},
    "cup": {"kind": "shot", "frames": SM + "coffee-cup-sam/frames"},
    "lantern": {"kind": "shot", "frames": SM + "lantern-sam/frames"},
    "survivor": {"kind": "shot", "frames": K + "53-civic-footage/sources/seated/frames", "masks": K + "53-civic-footage/sources/seated/masks.json", "cut": True},
    "door": {"kind": "shot", "frames": K + "kit/archive-door/frames", "masks": K + "kit/archive-door/masks.json", "cut": True},
    "girl_dog": {"kind": "still", "image": SAAM + "SAAM-1939.4.1_1.jpg"},
    "family": {"kind": "still", "image": SAAM + "SAAM-1981.172.33_1.jpg"},
    "interior": {"kind": "still", "image": SAAM + "SAAM-1916.6.39_1.jpg"},
    "twilight": {"kind": "still", "image": SAAM + "SAAM-1913.3.3_2.jpg"},
    "hearth": {"kind": "still", "image": SAAM + "SAAM-1972.84.86_1.jpg"},
}
LEDGER = {
    "film": {"title": "Corrugated Sky (SCION 02 Reiniger), BOXBACK track 11", "url": "moto/scion/corrugated-sky/", "rights": "producer's own work", "basis": "own work"},
    "song": {"title": "Et tu, Brute - Corrugated Sky (Treblo)", "url": "moto/Et tu, Brute (BOXBACK)/", "rights": "producer's own work", "basis": "own work, unaltered"},
    "orchestra": {"title": "The Jelly Orchestra + drift rigs", "url": "hartswf0/contaminant-jelly bonus/jellyorchestra.html", "rights": "producer's own work", "basis": "own work"},
    "cup": {"title": "Biologist Caye Johnson Explains How NASA Searched for Life from the Moon (NASA Ames)", "url": "https://images.nasa.gov/details/ARC-20190708-AAV3208-LunarBioLab-JohnsonNarration-NASAWeb-24fps", "rights": "public_domain",
            "basis": "US government work (NASA media); record: contaminant-jelly paeleo/handmade/kit/found-frames.json"},
    "lantern": {"title": "Anthracite: Pre-Shift Examinations of Underground Mines (MSHA)", "url": "https://archive.org/details/gov.msha.dvd614", "rights": "public_domain",
                "basis": "probable US government work: archive.org gov.msha collection (Mine Safety and Health Administration); producer not verified from here"},
    "survivor": {"title": "Survival Stresses (1961)", "url": "https://archive.org/details/hmdvid-101704143", "timecode": "5.0-9.0 s", "rights": "public_domain",
                 "basis": "probable US government work: archive.org hmdvid (US National Library of Medicine historical audiovisuals); producer not verified from here"},
    "door": {"title": "Straight Talk (1992)", "url": "https://archive.org/details/gov.ntis.ava19144vnb1", "timecode": "5.0-7.5 s", "rights": "public_domain",
             "basis": "probable US government work: archive.org gov.ntis collection (National Technical Information Service); producer not verified from here"},
    "girl_dog": {"title": "Young Girl and Dog, Percy Moran, 1890 (SAAM 1939.4.1)", "url": "https://smithsonian-open-access.s3-us-west-2.amazonaws.com/media/saam/SAAM-1939.4.1_1.jpg", "rights": "CC0", "basis": "Smithsonian Open Access CC0 (record access: CC0)"},
    "family": {"title": "Father, Mother, and Boy, Samuel Medford, 1841 (SAAM 1981.172.33)", "url": "https://smithsonian-open-access.s3-us-west-2.amazonaws.com/media/saam/SAAM-1981.172.33_1.jpg", "rights": "CC0", "basis": "Smithsonian Open Access CC0 (record access: CC0)"},
    "interior": {"title": "Interior of a House, Eliphalet Fraser Andrews, n.d. (SAAM 1916.6.39)", "url": "https://smithsonian-open-access.s3-us-west-2.amazonaws.com/media/saam/SAAM-1916.6.39_1.jpg", "rights": "CC0", "basis": "Smithsonian Open Access CC0 (record access: CC0)"},
    "twilight": {"title": "Twilight after the Rain, Norwood MacGilvary, 1906 (SAAM 1913.3.3)", "url": "https://smithsonian-open-access.s3-us-west-2.amazonaws.com/media/saam/SAAM-1913.3.3_2.jpg", "rights": "CC0", "basis": "Smithsonian Open Access CC0 (record access: CC0)"},
    "hearth": {"title": "Dogs on the Hearth no. 1, J. Alden Weir, 1887 (SAAM 1972.84.86)", "url": "https://smithsonian-open-access.s3-us-west-2.amazonaws.com/media/saam/SAAM-1972.84.86_1.jpg", "rights": "CC0", "basis": "Smithsonian Open Access CC0 (record access: CC0)"},
}
NAME = {"kick0": "THE SENTINEL", "snare0": "THE CELLULOID TWIN", "snare1": "THE CELLULOID TWIN", "hat0": "THE DOODLE SPARK", "hat1": "THE DOODLE SPARK",
        "bass0": "THE SEWER CREATURE", "choir0": "THE GLASS MOON", "bed0": "THE FILM BELL", "call0": "THE AFTERLIGHT MEDUSA"}

def hold(src, k, t_att, cond, bloom, release, after_xy, at_xy, size, bloom_size=None, label="", credit="", bloom_xy=(0.0, 0.62), dist=10.0, aspect=None, extra_pulses=True, release_to=None, dim=0.0, side_after_bloom=None):
    """one performance. t_att: attention starts (jelly turns and comes forward); cond: (c0,c1); bloom: (b0,b1) or None; release: time the
    picture starts to leave; after_xy: the changed-state place (2 bars)."""
    ev = {"src": src, "by": k, "t": [t_att, release + 2.5], "condense": list(cond), "bloom": list(bloom) if bloom else [0, 0], "release": release,
          "size": size, "bloom_size": bloom_size or size, "label": f"{NAME[k]} holds {label}", "credit": credit, "dim": dim, "release_to": release_to}
    if aspect: ev["aspect"] = aspect
    d = [{"k": k, "t0": t_att, "t1": cond[0], "sx": at_xy[0], "sy": at_xy[1], "dist": dist + 2, "ramp": 1.2, "out": 0.5}]   # attention: come forward
    if bloom:
        d.append({"k": k, "t0": cond[0], "t1": bloom[0], "sx": at_xy[0], "sy": at_xy[1], "dist": dist, "ramp": 0.5, "out": 0.6})
        d.append({"k": k, "t0": bloom[0] - 0.6, "t1": bloom[1], "sx": bloom_xy[0], "sy": bloom_xy[1], "dist": dist, "ramp": 0.9, "out": 0.9})
        if side_after_bloom:
            d.append({"k": k, "t0": bloom[1] - 0.6, "t1": release, "sx": side_after_bloom[0], "sy": side_after_bloom[1], "dist": dist, "ramp": 0.9, "out": 0.5})
            ev["side_after_bloom"] = [bloom[1], list(side_after_bloom)]
    else:
        d.append({"k": k, "t0": cond[0], "t1": release, "sx": at_xy[0], "sy": at_xy[1], "dist": dist, "ramp": 0.5, "out": 0.5})
    d.append({"k": k, "t0": release, "t1": release + 2 * BAR, "sx": after_xy[0], "sy": after_xy[1], "dist": dist + 3, "ramp": 1.0, "out": 1.2})   # changed state
    ex = []
    if extra_pulses:                                            # attention: half-beat pulses; hold: one per beat; after: none (a changed rate)
        b = int((t_att - OFF) / PER) + 1
        while beat_t(b) < cond[0]:
            ex.append([round(beat_t(b), 4), 0.3, -4]); ex.append([round(beat_t(b) + PER / 2, 4), 0.3, -8]); b += 1
        while beat_t(b) < release:
            ex.append([round(beat_t(b), 4), 0.5, -6]); b += 1
    return ev, d, ex

films, direct, extra = [], [], {}
def add(*a, **kw):
    ev, d, ex = hold(*a, **kw); films.append(ev); direct.extend(d); extra.setdefault(ev["by"], []).extend(ex)

GA = 0.5625
# -- the house wakes
add("cup", "snare0", 15.0, (16.6, 19.0), None, 28.0, (0.78, 0.8), (0.55, 0.42), 240, label="a cup", credit="NASA Ames · US government work")
add("film", "bed0", 18.5, (20.2, 22.6), (23.4, 43.0), 44.0, (-0.35, -0.25), (-0.5, 0.45), 300, 700, label="CORRUGATED SKY: the house wakes", credit="SCION 02 Reiniger", aspect=GA, dim=0.3)
add("interior", "snare1", 29.0, (30.6, 33.0), None, 46.0, (-0.8, 0.8), (-0.6, 0.42), 230, label="Interior of a House", credit="E. F. Andrews · SAAM · CC0")
add("family", "choir0", 45.0, (46.6, 49.0), (49.6, 56.0), 57.0, (0.6, -0.3), (0.5, 0.4), 250, 470, label="Father, Mother, and Boy", credit="Samuel Medford, 1841 · SAAM · CC0")
# -- night: the medusa holds a painted girl and dog; at the let-go it releases them INTO the gate's dog
GATE_DOG = (0.24, -0.12)   # NDC of the gate film's dog, relative to frame (computed in the compositor from the bloom box)
add("girl_dog", "call0", 57.5, (59.1, 61.5), (62.2, 69.5), LETGO, (0.72, 0.86), (0.55, 0.4), 250, 470, label="Young Girl and Dog", credit="Percy Moran, 1890 · SAAM · CC0",
    side_after_bloom=(0.74, 0.42), release_to="gate_dog")
add("film", "bed0", 71.5, (73.2, 75.4), (76.0, 89.0), 89.8, (-0.4, -0.35), (-0.5, 0.45), 300, 760, label="CORRUGATED SKY: the gate", credit="SCION 02 Reiniger", aspect=GA, dim=0.42)
# -- fire: a lamp is checked; the house burns; someone sits outside and survives
add("lantern", "choir0", 92.0, (93.6, 96.0), (96.6, 101.6), 102.6, (0.7, 0.85), (0.55, 0.42), 240, 470, label="a lamp checked", credit="Anthracite (MSHA) · US government work")
add("film", "bed0", 100.5, (102.2, 104.6), (105.4, 123.0), 124.0, (-0.3, -0.4), (-0.5, 0.45), 300, 700, label="CORRUGATED SKY: the fire", credit="SCION 02 Reiniger", aspect=GA, dim=0.3)
add("survivor", "bass0", 106.0, (107.6, 110.0), None, 122.5, (-0.75, -0.6), (-0.82, -0.35), 220, label="a survivor, sitting still", credit="Survival Stresses, 1961 · US government work")
add("door", "bass0", 126.2, (127.8, 129.6), (130.2, 133.4), 134.4, (-0.7, -0.5), (-0.55, 0.42), 240, 440, label="a door opened", credit="Straight Talk, 1992 · US government work", bloom_xy=(-0.25, 0.62))
# -- rain: twilight after the rain; the dog is kept by a hearth (the girl's dog, recurring in a changed function)
add("twilight", "hat0", 126.0, (127.6, 130.0), None, 141.0, (0.8, 0.85), (0.6, 0.42), 240, label="Twilight after the Rain", credit="N. MacGilvary, 1906 · SAAM · CC0")
add("film", "bed0", 131.0, (132.6, 134.6), (135.0, 141.0), 141.6, (0.0, -0.5), (-0.5, 0.45), 300, 700, label="CORRUGATED SKY: the rain", credit="SCION 02 Reiniger", aspect=GA, dim=0.3)
add("hearth", "call0", 134.0, (135.6, 138.0), None, 145.6, (0.7, 0.6), (0.62, -0.3), 220, label="Dogs on the Hearth", credit="J. Alden Weir, 1887 · SAAM · CC0", extra_pulses=True)
# the sentinel keeps the house's clock in frame, lower left, for the whole song
direct.append({"k": "kick0", "t0": 0.0, "t1": 146.0, "sx": -0.78, "sy": -0.62, "dist": 12.0, "ramp": 0.01, "out": 0.5, "w": 1.0})
# keep the others clear of the titles (first 8 s and last 4 s)
for k in ["snare0", "snare1", "hat0", "hat1", "bass0", "choir0", "bed0", "call0"]:
    direct.append({"k": k, "t0": 0.0, "t1": 8.0, "sx": 0.0, "sy": -0.95, "dist": 16, "ramp": 0.01, "out": 1.5, "w": 0.85})

cast = [("THE SENTINEL OF THE SILT FLOOR", "the kick · keeps the house's clock, in the corner, all song"),
        ("THE CELLULOID TWINS OF THE KITCHEN", "the snare · hold a cup and a painted room: the table set"),
        ("THE DOODLE SPARKS OF THE RAIN LINE", "the hats · hold the twilight after the rain"),
        ("THE SEWER CREATURE UNDER THE FLOOR", "the sub · holds a survivor, then a door"),
        ("THE GLASS MOON OF THE PORCH", "the choir · holds the family portrait, then a lamp"),
        ("THE FILM BELL OF THE WALL", "the bed · holds the house's own film"),
        ("THE AFTERLIGHT MEDUSA AT THE GATE", "the call · holds a painted girl and dog, and lets them go")]
cards = [{"kind": "title", "t": [0.3, 7.6], "lines": ["CORRUGATED", "SKY"], "sub": "JELLY CUT · BOXBACK 11 · THE JELLY ORCHESTRA", "y": 190},
         {"kind": "cast", "t": [8.0, 14.8], "members": cast},
         {"kind": "title", "t": [141.6, 145.7], "lines": ["CORRUGATED", "SKY"], "sub": "archive: US government works · Smithsonian CC0", "y": 200}]
cfg = {"id": "corrugated-sky", "audio": "/home/user/moto/Et tu, Brute (BOXBACK)/Et tu, Brute_ - Corrugated Sky - Treblo.ogg",
       "orch_dir": "/home/user/moto/scion/jelly-cuts/work/orch", "sources": SOURCES, "films": films, "cards": cards, "letgo": LETGO,
       "kick_flash": {"key": "kick0"}, "bpm": BPM, "offset": OFF}
json.dump(cfg, open(os.path.join(HERE, "jellycut.json"), "w"), indent=1)
# an extra pulse never lands within 0.12 s of one of that jelly's own song onsets (the song keeps priority)
ROLE_N = {"kick": 1, "snare": 2, "hat": 2, "bass": 1, "choir": 1, "bed": 1, "call": 1}
cast_roles = json.load(open(os.path.join(HERE, "cast.json")))["roles"]
for key in list(extra):
    role, k = key[:-1], int(key[-1]); n = ROLE_N[role]; own = [e[0] for q, e in enumerate(cast_roles[role]) if q % n == k]
    extra[key] = [e for e in extra[key] if all(abs(e[0] - o) > 0.12 for o in own)]
json.dump({"direct": direct, "extra": extra}, open(os.path.join(HERE, "direct.json"), "w"))
# provenance graph (SCION 54)
nodes = [{"id": "src:" + k, **v} for k, v in LEDGER.items()]
ops = [{"op": "analyse", "in": ["src:song"], "out": "cast", "params": "cast_song.py: librosa band onsets + HPSS"},
       {"op": "render-orchestra", "in": ["cast", "src:orchestra", "direct"], "out": "layer:orchestra", "params": "orchestra.html deterministic clock; stage directions direct.json (attention, hold, changed state); shots [0,1,0,4]"}]
for i, e in enumerate(films):
    s = SOURCES[e["src"]]
    ops.append({"op": "mask-cut" if s.get("cut") else "frame", "in": ["src:" + e["src"]], "out": f"cut:{i}", "params": "SAM polygon; outside the mask is not drawn" if s.get("cut") else "whole frame / whole painting"})
    ops.append({"op": "halftone-fleck", "in": [f"cut:{i}"], "out": f"layer:{i}", "params": {"held_by": e["by"], "t": e["t"], "condense": e["condense"], "bloom": e["bloom"], "release": e["release"], "release_to": e["release_to"]}})
ops.append({"op": "composite", "in": ["layer:orchestra"] + [f"layer:{i}" for i in range(len(films))], "out": "corrugated-sky-jelly.mp4"})
json.dump({"nodes": nodes, "operations": ops, "dropped": {
    "reason": "rights basis not stated by the record (critic round 1, item 6): dropped rather than guessed",
    "sources": ["This Is Coffee (1961)", "Don't Be Afraid (1953)", "[Frigidaire Imperial Line] (1956)", "Amateur Film New Jersey C (home movie)", "Summers collection amateur film (1941)", "Light Of Your Life", "Top Of The Cloud", "Door to Heaven (1941)"]}},
    open(os.path.join(HERE, "source-ledger.json"), "w"), indent=1)
print(len(films), "films,", len(direct), "directions,", sum(len(v) for v in extra.values()), "extra pulses; let-go at", round(LETGO, 3))
