"""Corrugated Sky jelly cut, r3: ONE through-line. The Afterlight Medusa (the song's call) holds its memories, one at a
time, inside the water: the house waking, a family portrait, a painted girl and her dog, the gate (where it lets the
painted dog go INTO the silhouette dog, and is lighter afterwards), the fire, a survivor, the rain, a dog by a hearth.
Writes: bank-spec.json (halftone banks), scene.json (in-scene films for filmsys.js), direct.json (stage directions),
jellycut.json (compositor: labels, titles, kick halo). Run: python3 -I build_cut3.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
BPM, OFF = 141.05, 0.345; PER = 60 / BPM; BAR = 4 * PER
def beat_t(b): return OFF + b * PER
LETGO = 73.5 + 272 / 24
K = "/home/user/hartswf0/bolas/paeleo/handmade/"; SAAM = K + "49-open-content-atelier/sources/media/"
FILM = {"kind": "film", "npy": "/home/user/moto/scion/jelly-cuts/work/corrugated-sky-film.npy"}
SRC = {"family": {"kind": "still", "image": SAAM + "SAAM-1981.172.33_1.jpg"}, "girl_dog": {"kind": "still", "image": SAAM + "SAAM-1939.4.1_1.jpg"},
       "survivor": {"kind": "shot", "frames": K + "53-civic-footage/sources/seated/frames", "masks": K + "53-civic-footage/sources/seated/masks.json", "cut": True},
       "hearth": {"kind": "still", "image": SAAM + "SAAM-1972.84.86_1.jpg"}}
H = "call0"
#            id         source        att    condense        bloom          release   width  label / credit
PLAN = [("house",    "film",      6.0, (7.6, 9.6),   (10.2, 21.6), 22.4, 5.0, "the house wakes", "CORRUGATED SKY · SCION 02 Reiniger"),
        ("family",   "family",   26.5, (28.1, 30.1), (30.7, 39.5), 40.3, 3.2, "a family, 1841", "Samuel Medford, Father, Mother, and Boy · SAAM · CC0"),
        ("girl_dog", "girl_dog", 52.0, (53.6, 55.6), (56.2, 70.6), 71.4, 3.6, "a girl and her dog", "Percy Moran, Young Girl and Dog, 1890 · SAAM · CC0"),
        ("gate",     "film",     71.0, (73.2, 75.2), (75.8, 89.0), 89.8, 5.0, "the gate", "CORRUGATED SKY · SCION 02 Reiniger"),
        ("fire",     "film",     99.5, (101.1, 103.1), (103.7, 117.4), 118.2, 5.0, "the fire", "CORRUGATED SKY · SCION 02 Reiniger"),
        ("survivor", "survivor", 118.4, (119.8, 121.1), (121.5, 127.4), 127.9, 8.4, "someone who stayed outside", "Survival Stresses, 1961 · US government work"),
        ("rain",     "film",     128.1, (129.2, 130.5), (130.9, 135.9), 136.5, 5.0, "the rain", "CORRUGATED SKY · SCION 02 Reiniger"),
        ("hearth",   "hearth",   136.4, (137.4, 138.2), (138.4, 142.3), 142.45, 3.4, "a dog kept by a hearth", "J. Alden Weir, Dogs on the Hearth no. 1, 1887 · SAAM · CC0")]
AFTER = {"house": (0.55, -0.35), "family": (-0.55, 0.3), "girl_dog": (0.0, 0.25), "gate": (0.6, 0.55), "fire": (-0.6, -0.3), "survivor": (0.5, 0.4), "rain": (-0.4, 0.5), "hearth": (0.0, -0.2)}
GW = {"film": 128, "family": 96, "girl_dog": 96, "survivor": 72, "hearth": 96}
bank, films, direct, extra = [], [], [], []
for fid, src, att, cond, bloom, rel, width, lab, cred in PLAN:
    live_end = (LETGO + 1.5) if fid == "girl_dog" else rel + 2.2
    s = FILM if src == "film" else SRC[src]
    bank.append({"id": fid, "source": s, "gw": GW[src], "src_t0": att if src == "film" else 0.0, "dur": live_end - att + 0.2})
    f = {"id": fid, "bank": fid, "by": H, "t": [att, live_end], "condense": list(cond), "bloom": list(bloom), "release": rel, "width": width, "label": lab, "credit": cred}
    if fid == "girl_dog":   # after its bloom the painting stays as a cloud of flecks round the bell (a memory) ...
        f.update(memory=True, release_to="gate", letgo=LETGO, letgo_end=LETGO + 1.2, target=[0.71, 0.76])   # ... and at the let-go travels INTO the gate's dog
    films.append(f)
    # attention: before the picture condenses the medusa swims to the middle of the water and pulses twice a beat
    direct.append({"k": H, "t0": att, "t1": bloom[1], "sx": 0.0, "sy": 0.18, "dist": 10.0, "ramp": 1.4, "out": 0.8})
    # changed state: after the release it goes somewhere else for >= 2 bars, pulse rate back to the song's
    direct.append({"k": H, "t0": rel, "t1": rel + 2 * BAR, "sx": AFTER[fid][0], "sy": AFTER[fid][1], "dist": 13.0, "ramp": 1.0, "out": 1.0})
    b = int((att - OFF) / PER) + 1
    while beat_t(b) < cond[0]: extra += [[round(beat_t(b), 4), .3, -4], [round(beat_t(b) + PER / 2, 4), .3, -8]]; b += 1
    while beat_t(b) < rel: extra.append([round(beat_t(b), 4), .5, -6]); b += 1
# extra pulses never within 0.12 s of the medusa's own song onsets
own = [e[0] for e in json.load(open(os.path.join(HERE, "cast.json")))["roles"]["call"]]
extra = [e for e in extra if all(abs(e[0] - o) > 0.12 for o in own)]
direct.append({"k": "kick0", "t0": 0.0, "t1": 146.0, "sx": -0.6, "sy": -0.36, "dist": 15.0, "ramp": 0.01, "out": 0.5, "w": 1.0, "lock": True})
for k in ["snare0", "snare1", "hat0", "hat1", "bass0", "choir0", "bed0", "call0"]:
    direct.append({"k": k, "t0": 0.0, "t1": 5.6, "sx": 0.0, "sy": -0.95, "dist": 16, "ramp": 0.01, "out": 1.2, "w": 0.85})
# during every bloom the rest of the orchestra swims to the edges of the water, out of the camera's way
EDGE = [(-0.95, 0.75), (0.95, 0.75), (-0.98, -0.1), (0.98, -0.1), (0.9, -0.8), (-0.3, -0.95), (0.35, 0.95), (-0.9, -0.85)]
for fid, src, att, cond, bloom, rel, *_ in PLAN:
    for i, k in enumerate(["snare0", "snare1", "hat0", "hat1", "bass0", "choir0", "bed0"]):
        direct.append({"k": k, "t0": cond[0] - 1.0, "t1": bloom[1], "sx": EDGE[i][0], "sy": EDGE[i][1], "dist": 17, "ramp": 1.2, "out": 1.0, "w": 0.92})
scene = {"films": films, "scale": [{"k": H, "t0": LETGO + 0.1, "t1": LETGO + 1.6, "to": 0.72}]}
json.dump(bank and {"films": bank}, open(os.path.join(HERE, "bank-spec.json"), "w"), indent=1)
json.dump(scene, open(os.path.join(HERE, "scene.json"), "w"), indent=1)
json.dump({"direct": direct, "extra": {H: extra}}, open(os.path.join(HERE, "direct.json"), "w"))
cards = [{"kind": "title", "t": [0.3, 5.6], "lines": ["CORRUGATED", "SKY"], "sub": "JELLY CUT · the Afterlight Medusa remembers", "y": 190},
         {"kind": "title", "t": [142.6, 145.7], "lines": ["CORRUGATED", "SKY"], "sub": "archive: US government work · Smithsonian CC0", "y": 200}]
cfg = {"id": "corrugated-sky", "audio": "/home/user/moto/Et tu, Brute (BOXBACK)/Et tu, Brute_ - Corrugated Sky - Treblo.ogg", "orch_dir": "/home/user/moto/scion/jelly-cuts/work/orch3",
       "sources": {}, "films": [], "scene_films": films, "cards": cards, "letgo": LETGO, "kick_flash": {"key": "kick0"}, "bpm": BPM, "offset": OFF, "label_mode": "bottom"}
json.dump(cfg, open(os.path.join(HERE, "jellycut.json"), "w"), indent=1)
LED = json.load(open(os.path.join(HERE, "source-ledger.json")))
keep = {"src:film", "src:song", "src:orchestra", "src:family", "src:girl_dog", "src:survivor", "src:hearth"}
nodes = [n for n in LED["nodes"] if n["id"] in keep]
ops = [{"op": "analyse", "in": ["src:song"], "out": "cast"},
       {"op": "halftone-bank", "in": ["src:" + (s if s != "film" else "film") for _, s, *_ in PLAN], "out": "bank", "params": "build_bank.py: 8 levels, Bayer pass, SAM cut for the survivor"},
       {"op": "render-orchestra+films-in-scene", "in": ["cast", "bank", "src:orchestra", "direct", "scene"], "out": "layer:scene", "params": "orchestra3.html + filmsys.js; films parented to the medusa; per-bloom camera framing solve"},
       {"op": "composite", "in": ["layer:scene"], "out": "corrugated-sky-jelly.mp4", "params": "labels, titles, kick halo (jellycut.py)"}]
LED.update(nodes=nodes, operations=ops)
LED["dropped"]["r3"] = "fewer films, each staged: cup, interior, lantern, door, twilight dropped from the cut (still cleared, unused)"
json.dump(LED, open(os.path.join(HERE, "source-ledger.json"), "w"), indent=1)
print(len(films), "memories;", len(direct), "directions;", len(extra), "extra pulses; let-go", round(LETGO, 3))
