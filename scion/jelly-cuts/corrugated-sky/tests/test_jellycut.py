"""Numeric invariants for the Corrugated Sky jelly cut. Run: python3 -I tests/test_jellycut.py"""
import json, os, sys, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "src"))
cfg = json.load(open(os.path.join(ROOT, "jellycut.json"))); cast = json.load(open(os.path.join(ROOT, "cast.json")))
ledger = json.load(open(os.path.join(ROOT, "source-ledger.json")))
R = []
def check(name, ok, detail): R.append({"test": name, "pass": bool(ok), "detail": detail}); print(("PASS " if ok else "FAIL ") + name, detail)

# 1 the orchestra is locked to the song: every role onset starts a pulse of its jelly within +-1 frame
orch = cfg["orch_dir"]; META = {}
for mp in glob.glob(os.path.join(orch, "meta_*.json")):
    for m in json.load(open(mp)): META[m["f"]] = m["jel"]
members = json.load(open(os.path.join(orch, "cast_members.json")))
idx = {}
for i, m in enumerate(members): idx.setdefault(m["role"], []).append(i)
ROLE = {"kick": "kick", "snare": "snare", "hat": "hat", "bass": "bass", "choir": "choir", "bed": "bed", "call": "call"}
fr = np.array(sorted(META)); worst = 0; tot = hit = 0
for role, cr in ROLE.items():
    ix = idx.get(cr, []); ev = [e[0] for e in cast["roles"].get(role, [])]
    for k, j in enumerate(ix):
        g = np.array([META[f][j][3] for f in fr]); rises = fr[1:][(g[1:] - g[:-1]) > 0.02]
        for q, t in enumerate(ev):
            if q % len(ix) != k or not (fr[0] / 24 + 0.5 < t < fr[-1] / 24 - 0.5): continue
            d = float(np.min(np.abs(rises - t * 24))) if len(rises) else 99; worst = max(worst, d); tot += 1; hit += d <= 1.0
check("orchestra pulse within +-1 frame of its role onset", tot > 0 and hit == tot, {"onsets": tot, "locked": hit, "worst_frames": round(worst, 3)})

# 2 rights: every source drawn into the film is public domain or the producer's own work
used = {e["src"] for e in cfg["films"]}
nodes = {n["id"]: n for n in ledger["nodes"]}
bad = [u for u in used if nodes.get("src:" + u, {}).get("rights") not in ("public_domain", "producer's own work")]
check("every drawn source ledgered public_domain or producer's own", not bad, {"sources": sorted(used), "bad": bad})
pd = [u for u in used if nodes["src:" + u]["rights"] == "public_domain"]
check("every PD source has an archive URL", all(nodes["src:" + u].get("url", "").startswith("https://") for u in pd), {"pd_sources": len(pd)})

# 3 dot law: one film's dots use at most 8 ink levels
import jellycut as J
from PIL import Image
J.CFG = cfg
img = Image.new("RGB", (J.W, J.H), (0, 0, 0)); grad = np.tile(np.linspace(0, 1, 192, dtype=np.float32), (144, 1))
cols = set()
_orig = J.ImageDraw.ImageDraw.ellipse
def spy(self, xy, fill=None, **kw): cols.add(fill); return _orig(self, xy, fill=fill, **kw)
J.ImageDraw.ImageDraw.ellipse = spy
J.dot_film(img, grad, 640, 360, 600, 1.0, 0.0, 1)
J.ImageDraw.ImageDraw.ellipse = _orig
check("dot law: at most 8 ink levels in a condensed film", 1 <= len(cols) <= 8, {"levels": len(cols)})

# 4 two deliberate holds (Mouris): the gate bloom and the end title, each >= 4 s
gate = [e for e in cfg["films"] if e["src"] == "film" and "gate" in e["label"]][0]
title = [c for c in cfg["cards"] if c["kind"] == "title"][-1]
check("two deliberate holds >= 4 s", gate["bloom"][1] - gate["bloom"][0] >= 4 and title["t"][1] - title["t"][0] >= 4,
      {"gate_hold_s": gate["bloom"][1] - gate["bloom"][0], "title_hold_s": round(title["t"][1] - title["t"][0], 2)})

# 5 the archive dog recurs in a changed function (Ernst)
dogs = [e for e in cfg["films"] if e["src"] == "dog"]
check("archive dog recurs with a changed role", len(dogs) >= 2 and dogs[0]["label"] != dogs[1]["label"], {"appearances": [d["t"] for d in dogs]})
json.dump({"results": R, "all_pass": all(r["pass"] for r in R)}, open(os.path.join(ROOT, "tests", "invariants.json"), "w"), indent=1)
sys.exit(0 if all(r["pass"] for r in R) else 1)
