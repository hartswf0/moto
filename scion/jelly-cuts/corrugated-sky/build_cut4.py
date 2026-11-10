"""Corrugated Sky jelly cut, r4. 'Flecks in transit only' (the user's call): memories travel and condense as flecks and
RESOLVE to the full-resolution picture at the bloom. One character, the Afterlight Medusa: red, 1.7x, twelve thick
memory tentacles, one turning silver per memory let go. The painted girl and dog is KEPT beside the gate, on screen,
until the let-go, when its flecks leave it and land in the silhouette dog over 1.8 s. Ends on the medusa and a
silhouette boy and dog; the title comes after the hold.
Writes bank-spec.json, scene.json, direct.json, jellycut.json. Run: python3 -I build_cut4.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
BPM, OFF = 141.05, 0.345; PER = 60 / BPM; BAR = 4 * PER
def beat_t(b): return OFF + b * PER
LETGO = 73.5 + 272 / 24
K = "/home/user/hartswf0/bolas/paeleo/handmade/"; SAAM = K + "49-open-content-atelier/sources/media/"; SM = "/home/user/secondhand-motion/shots/"
FILMSRC = {"kind": "film", "npy": "/home/user/moto/scion/jelly-cuts/work/corrugated-sky-film.npy", "mp4": "/home/user/moto/scion/corrugated-sky/corrugated-sky.mp4"}
SRC = {"family": {"kind": "still", "image": SAAM + "SAAM-1981.172.33_1.jpg"},
       "girl_dog": {"kind": "still", "image": SAAM + "SAAM-1939.4.1_1.jpg"},
       "lamp": {"kind": "shot", "frames": SM + "lantern-sam/frames"},
       "survivor": {"kind": "shot", "frames": K + "53-civic-footage/sources/seated/frames"},
       "boy_dog": {"kind": "still", "image": SAAM + "SAAM-1981.172.31_1.jpg"}}
CROP = {"fire": [0.1, 0.12, 0.9, 1.0], "girl_dog": [0.30, 0.14, 0.96, 0.94], "boy_dog": [0.12, 0.08, 0.88, 0.92], "family": [0.06, 0.05, 0.94, 0.95]}
H = "call0"
#  id         src         att    condense        bloom            release  width  label / credit
PLAN = [
 ("house",    "film",      5.8, (7.4, 9.4),     (10.0, 16.5),   17.3, 5.6, "the house wakes", "CORRUGATED SKY · SCION 02 Reiniger"),
 ("family",   "family",   18.5, (20.5, 22.5),   (23.0, 30.0),   30.8, 3.4, "a family, 1841", "Samuel Medford · Father, Mother, and Boy · SAAM · CC0"),
 ("girl_dog", "girl_dog", 36.0, (50.5, 55.5),   (56.5, 64.5),   999,  3.8, "a girl and her dog", "Percy Moran · Young Girl and Dog, 1890 · SAAM · CC0"),
 ("gate",     "film",     71.0, (73.2, 75.2),   (75.8, 89.0),   89.8, 5.0, "the gate", "CORRUGATED SKY · SCION 02 Reiniger"),
 ("lamp",     "lamp",     90.8, (92.0, 93.2),   (93.6, 97.4),   98.0, 4.2, "a lamp, checked", "Anthracite: Pre-Shift Examinations · MSHA · US government work"),
 ("fire",     "film",    104.5, (106.0, 107.5), (108.0, 115.5), 116.3, 5.6, "the fire", "CORRUGATED SKY · SCION 02 Reiniger"),
 ("survivor", "survivor", 117.8, (119.2, 120.4), (120.8, 126.6), 127.2, 5.4, "someone who stayed outside", "Survival Stresses, 1961 · US government work"),
 ("rain",     "film",     127.6, (128.8, 130.0), (130.4, 135.6), 136.2, 5.6, "the rain", "CORRUGATED SKY · SCION 02 Reiniger"),
 ("boy_dog",  "boy_dog",  136.0, (137.0, 138.0), (138.4, 144.4), 145.0, 3.4, "a child and a dog, kept", "Unidentified · Boy with Dog · SAAM · CC0")]
MODE = {"house": "surface", "family": "caught", "girl_dog": "pulled", "gate": "surface", "lamp": "caught", "fire": "surface", "survivor": "pulled", "rain": "surface", "boy_dog": "caught"}
AFTER = {"house": (0.55, -0.35), "family": (-0.55, 0.3), "gate": (0.6, 0.5), "lamp": (-0.5, 0.45), "fire": (-0.6, -0.3), "survivor": (0.5, 0.4), "rain": (-0.4, 0.5)}
GW = {"film": 128, "family": 96, "girl_dog": 96, "lamp": 96, "survivor": 96, "boy_dog": 96}
bank, films, direct, extra = [], [], [], []
for fid, src, att, cond, bloom, rel, width, lab, cred in PLAN:
    s = FILMSRC if src == "film" else SRC[src]
    live_end = (LETGO + 2.2) if fid == "girl_dog" else min(145.73, rel + 2.2)
    full_t0 = cond[0] if src == "film" else att
    b = {"id": fid, "source": s, "gw": GW[src], "src_t0": att if src == "film" else 0.0, "dur": live_end - att + 0.2, "full_t0": full_t0}
    if fid in CROP: b["crop"] = CROP[fid]
    bank.append(b)
    f = {"id": fid, "bank": fid, "by": H, "t": [att, live_end], "condense": list(cond), "bloom": list(bloom), "release": rel, "width": width, "label": lab, "credit": cred, "full_t0": full_t0}
    if fid == "girl_dog":   # kept small beside the gate, on screen, until the let-go
        f.update(keep={"t0": 64.8, "width": 1.7, "dx": 3.7, "dy": 0.6}, letgo=LETGO, letgo_end=LETGO + 2.2, release_to="gate", target=[0.72, 0.70], release=LETGO)
    if fid == "gate": f["extra_half"] = 2.6
    f["mode"] = MODE[fid]
    films.append(f)
    if fid in ("family", "girl_dog"):   # it moves first: a dip toward the memory, then up to the middle
        direct.append({"k": H, "t0": att, "t1": att + 1.6, "sx": 0.32, "sy": -0.22, "dist": 9.0, "ramp": 0.6, "out": 0.6, "w": 1.0})
    # attention: before the memory condenses, the medusa swims to the middle of the water and pulses twice a beat
    direct.append({"k": H, "t0": att, "t1": bloom[1], "sx": 0.0, "sy": 0.18, "dist": 10.0, "ramp": 1.4, "out": 0.8})
    if fid in AFTER:
        direct.append({"k": H, "t0": rel, "t1": rel + 2 * BAR, "sx": AFTER[fid][0], "sy": AFTER[fid][1], "dist": 13.0, "ramp": 1.0, "out": 1.0})
    b = int((att - OFF) / PER) + 1
    while beat_t(b) < cond[0]: extra += [[round(beat_t(b), 4), .3, -4], [round(beat_t(b) + PER / 2, 4), .3, -8]]; b += 1
    while beat_t(b) < min(rel if rel < 900 else LETGO, 145): extra.append([round(beat_t(b), 4), .5, -6]); b += 1
# THE CHOICE (readable without captions): attention - the medusa pulses four times a beat as the girl's hand opens;
# gesture - the kept painting breaks into flecks that travel to the dog; changed state - a tentacle turns silver and the
# medusa shrinks to 72% for the rest of the song.
b = int((LETGO - 1.6 - OFF) / PER) + 1
while beat_t(b) < LETGO: extra += [[round(beat_t(b) + PER * q / 4, 4), .2, -3] for q in range(4)]; b += 1
own = [e[0] for e in json.load(open(os.path.join(HERE, "cast.json")))["roles"]["call"]]
extra = [e for e in extra if all(abs(e[0] - o) > 0.1 for o in own)]
direct.append({"k": "kick0", "t0": 0.0, "t1": 146.0, "sx": -0.56, "sy": -0.3, "dist": 16.0, "ramp": 0.01, "out": 0.5, "w": 1.0, "lock": True})
for k in ["snare0", "snare1", "hat0", "hat1", "bass0", "choir0", "bed0", "call0"]:
    direct.append({"k": k, "t0": 0.0, "t1": 5.6, "sx": 0.0, "sy": -0.95, "dist": 16, "ramp": 0.01, "out": 1.2, "w": 0.85})
EDGE = [(-0.95, 0.75), (0.95, 0.75), (-0.98, -0.1), (0.98, -0.1), (0.9, -0.8), (-0.3, -0.95), (0.35, 0.95)]
for fid, src, att, cond, bloom, rel, *_ in PLAN:
    for i, k in enumerate(["snare0", "snare1", "hat0", "hat1", "bass0", "choir0", "bed0"]):
        direct.append({"k": k, "t0": cond[0] - 1.0, "t1": bloom[1], "sx": EDGE[i][0], "sy": EDGE[i][1], "dist": 17, "ramp": 1.2, "out": 1.0, "w": 0.92})
scene = {"films": films, "hero": {"k": H, "scale": 1.7, "bell": "#e8342a", "rim": "#ffb27a"}, "scale": [{"k": H, "t0": LETGO + 1.8, "t1": LETGO + 3.0, "to": 0.72}]}
json.dump({"films": bank}, open(os.path.join(HERE, "bank-spec.json"), "w"), indent=1)
json.dump(scene, open(os.path.join(HERE, "scene.json"), "w"), indent=1)
json.dump({"direct": direct, "extra": {H: extra}}, open(os.path.join(HERE, "direct.json"), "w"))
cards = [{"kind": "title", "t": [0.3, 5.4], "lines": ["CORRUGATED", "SKY"], "sub": "JELLY CUT · the Afterlight Medusa remembers", "y": 190},
         {"kind": "title", "t": [144.6, 145.73], "lines": ["CORRUGATED", "SKY"], "sub": "archive: US government work · Smithsonian CC0", "y": 200}]
cfg = {"id": "corrugated-sky", "audio": "/home/user/moto/Et tu, Brute (BOXBACK)/Et tu, Brute_ - Corrugated Sky - Treblo.ogg", "orch_dir": "/home/user/moto/scion/jelly-cuts/work/orch4",
       "sources": {}, "films": [], "scene_films": films, "cards": cards, "letgo": LETGO, "kick_flash": {"key": "kick0"}, "halos": 160, "bpm": BPM, "offset": OFF}
json.dump(cfg, open(os.path.join(HERE, "jellycut.json"), "w"), indent=1)
LED = json.load(open(os.path.join(HERE, "source-ledger.json")))
add = {"src:lamp": {"id": "src:lamp", "title": "Anthracite: Pre-Shift Examinations of Underground Mines (MSHA)", "url": "https://archive.org/details/gov.msha.dvd614", "rights": "public_domain",
                    "basis": "probable US government work: archive.org gov.msha collection (Mine Safety and Health Administration); producer not verified from here"},
       "src:boy_dog": {"id": "src:boy_dog", "title": "Boy with Dog, unidentified artist (SAAM 1981.172.31)", "url": "https://smithsonian-open-access.s3-us-west-2.amazonaws.com/media/saam/SAAM-1981.172.31_1.jpg", "rights": "CC0", "basis": "Smithsonian Open Access CC0 (record access: CC0)"}}
ids = {n["id"] for n in LED["nodes"]}
LED["nodes"] = [n for n in LED["nodes"] if n["id"] != "src:hearth"] + [v for k, v in add.items() if k not in ids]
LED["operations"] = [{"op": "analyse", "in": ["src:song"], "out": "cast"},
                     {"op": "halftone-bank", "in": ["src:film", "src:family", "src:girl_dog", "src:lamp", "src:survivor", "src:boy_dog"], "out": "bank", "params": "build_bank.py: 8 levels, Bayer pass (flecks in transit)"},
                     {"op": "full-res-bloom-frames", "in": ["src:film", "src:family", "src:girl_dog", "src:lamp", "src:survivor", "src:boy_dog"], "out": "full", "params": "build_full.py: same crops; shown at the bloom (dot law suspended, the user's call)"},
                     {"op": "render-orchestra+films-in-scene", "in": ["cast", "bank", "full", "src:orchestra", "direct", "scene"], "out": "layer:scene"},
                     {"op": "composite", "in": ["layer:scene"], "out": "corrugated-sky-jelly.mp4", "params": "labels, titles, kick halo, onset halos"}]
json.dump(LED, open(os.path.join(HERE, "source-ledger.json"), "w"), indent=1)
print(len(films), "memories;", len(direct), "directions;", len(extra), "extra pulses; let-go", round(LETGO, 3))
