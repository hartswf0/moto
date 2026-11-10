# Corrugated Sky · JELLY CUT (r4)

**Critic rounds**
- **Round 1:** proof and film both reference stronger.
- **Round 2:** proof and film both reference stronger, with "not worth watching beyond the original."
- **r3:** changed the staging model per §11.
- **Round 3:** proof and film both reference stronger ("not yet worth watching as its own work").
- **r4:** applies the user's direction and the critic's repairs.
- **Round 4:** proof and film both reference stronger ("watchable, but much of it plays like a slideshow").
- **r4b, the final pass:**
  - the painting is kept fully in frame beside the gate, and its flecks travel into the dog's body over 84.8–87 s;
  - blooms are lifted above the caption band, and crops centre the defining element (the Moran dog, the fire);
  - the memory tentacles are a crown of twelve above the bell, red, turning silver one per release, so they are distinct from the light bars;
  - the medusa dips toward the memory before the family and girl blooms;
  - holds are shorter (house 10–16.5 s, girl 56.5–64.5 s, fire 108–115.5 s);
  - arrivals vary: surfacing, caught, or pulled in (the girl's flecks are pulled in across 36–55 s).

  The film is published with whatever verdict the next check gives.

A second cut of *Corrugated Sky* (BOXBACK track 11; the accepted SCION 02 Reiniger film), set in the contaminant-jelly water. The Jelly Orchestra plays the song: each jelly is one of its sounds. **One of them is the character:**

> **The Afterlight Medusa**, the song's *call*, holds its memories one at a time: the house waking, a family (1841), a painted girl and her dog, the gate, the fire, someone who stayed outside, the rain, a dog by a hearth.

At the gate, as the girl's hand opens, the medusa lets the painted dog go. Its flecks travel into the silhouette dog, and the medusa is lighter for the rest of the song. Each memory it releases lights one of its twelve tentacles silver. That is the rig's own rule: "each film you hold lights one."

* Film: `corrugated-sky-jelly.mp4` · proof: `proof.mp4` (song 64–93 s, cut from the film)
* Build:
  - `build_cut3.py` writes four files from one plan: the banks spec, the scene, the stage directions and the compositor config.
  - `../src/build_bank.py` turns the halftone banks into binaries.
  - `orchestra3.html` + `filmsys.js` render the scene, captured by `orchestra_capture.js` with mask passes.
  - `jellycut.py` adds the labels, titles and kick halo.
* Tests:
  - `python3 -I tests/test_r3.py <orch_dir> <orch_dir>` checks the mask passes and metadata;
  - `tests/sentinel_video.py <video> <t0>` checks the rendered frames.


## The user's call (r4): flecks in transit only
The user decided: **"Flecks in transit only."**
- A memory still travels and condenses as halftone flecks under the WYGWYL dot law.
- At its **bloom** it resolves to the **full-resolution picture**: large, centred and readable, with its holder framed above it.
- At the peak, recognisable archive takes priority over the strict dot law.

The law being **deliberately suspended at the bloom** is WYGWYL's *dot law* (hartswf0/butterfly-halfworld, `wygwyl/README.md`, "THE LAWS" §1: 8 ink levels, one ordered halftone pass, no alpha). The suspension applies only at the bloom. The cross-fade into and out of the picture is the one alpha the film now uses (`filmsys.js`, `pic` plane). Everywhere else the law holds.

## r4 repairs
| critic's condition | r4 |
|---|---|
| legibility at 360 px | the bloom shows the real picture; the crops are chosen so the subject fills it; the closing memory is *Boy with Dog* (SAAM, CC0), a silhouette of a child and a begging dog, chosen over the hearth etching, which did not read cold |
| let-go | the painting is **kept** small beside the gate, on screen, until 84.83 s; then its flecks leave the picture and land in the gate's dog over 1.8 s, along an arc |
| a unique holder | the medusa is red and 1.7× larger, with twelve thick memory tentacles; one turns silver for every memory it has let go |
| close the circle | ends on the medusa holding the boy and dog (bloom 138.4–144.4 s); the title follows the hold |
| pacing and the choice | no stretch between memories is over 6 s; rhythms vary (slow gathering for the painting, a short lamp, the painting kept beside the gate, the final hold); the choice at the let-go reads without captions: rapid pulses (four a beat), then the picture breaks into flecks that travel to the dog, then a tentacle turns silver and the medusa shrinks to 72% |
| the orchestra read on the mp4 | each jelly gets a soft halo on its own onsets in the composite; measured on the mp4 |
| numbers | from r4 on, every reported number is measured on the decoded final mp4 (`tests/test_mp4.py`). Jelly positions from the capture metadata only say where to look |

## Why r3 changed the staging model
Rounds 1 and 2 failed for the same reason: you could not see a jelly hold its film. The films were 2D boxes composited over a 3D orchestra whose camera and jellies the compositor did not control, so ownership could not be staged. The r2 position metric passed while the picture failed.

**r3 puts the films inside the Three.js scene** (`filmsys.js`):
* **Parenting.** Each held film is a cloud of halftone flecks (`THREE.Points`) parented to its jelly. It hangs below the bell on six visible strands, faces the camera, takes the same water fog, and is occluded by depth.
* **Dot law.** This follows WYGWYL (hartswf0/butterfly-halfworld, "THE LAWS"):
  - 8 ink levels and one ordered Bayer pass, precomputed in `build_bank.py`;
  - **no alpha**: dots are opaque (alphaTest);
  - a dot joins the picture when *c* ≥ its Bayer allegiance threshold;
  - an opaque water-coloured backing grows under the condensed picture.
* **Framing solve.** For each bloom the camera is solved so that the holder's **whole rig** (bell plus tentacle length) and its film are in frame. The rest of the orchestra swims to the edges of the water from the start of condensation to the end of the bloom.
* **One film at a time, larger.** Fewer films, each one staged.
* **Verification on rendered frames.** Three.js renders a holder-only and a film-only mask for every 4th bloom frame, at 320×180. Coverage and in-frame are measured on those masks, not on positions.

## The arc (performance: attention → intention → gesture → resistance → changed state)
1. **Attention.** Before every memory the medusa swims to the middle of the water and pulses twice a beat.
2. **Gesture.** The memory condenses below its bell on strands.
3. **Resistance.** It holds the memory, pulsing once a beat.
4. **Changed state.** At the release it goes somewhere else for at least 2 bars, back at the song's rate, and lights one more tentacle.
5. **After the let-go** (84.83 s), it shrinks to 72%.

The painting does not vanish when its bloom ends. It stays as a cloud of flecks around the bell, a memory carried through the gate, until the let-go sends it into the dog (SCION 03 Ernst: one hybrid causes the next). The dog returns as a dog kept by a hearth (one motif, changed function). The fire is answered by a 1961 government survival film: someone who stayed outside, sitting still.

## Grammar borrowed from the mixed-media swarms (bolas `paeleo/scion/swarms.json`)

| swarm | used as |
|---|---|
| **03 Ernst** | the painting's flecks cause the next image: they become the gate's dog |
| **04 Mouris** | recurrence (the dog: painted, then silhouette, then hearth) and holds (the gate bloom 75.8–89 s; the end title) |
| **44 Multiplane Parallax** | the films are real planes in the water's depth, fogged and occluded |
| **53 Civic Footage** | the survivor keeps its documentary frame and its cut-out mask edge; the credit carries source, year and basis |
| **54 Provenance Graph** | `source-ledger.json`: sources → halftone bank → scene render → composite |

## Rights
Every source used is public domain or CC0 and carries a stated **basis** in `source-ledger.json`:
- Smithsonian Open Access paintings: CC0;
- *Survival Stresses* (1961): probable US government work (NLM historical audiovisuals), producer not verified from here;
- the Orchestra, rigs, song and film: the producer's own.

Sources whose basis the record did not state were dropped in r2. The r1–r2 extras (cup, interior, lantern, door, twilight) are still cleared but no longer used.

## Measured invariants
They are measured on the mask passes and metadata (`tests/invariants_r3.json`) and on the rendered video (`tests/sentinel_video.json`):
- the holder is fully in frame and its film covers at most 10% of it, in every sampled bloom frame;
- it moves first, and changes state after;
- the let-go flecks travel into the dog;
- the Sentinel is fully in frame in every frame;
- at least 3 other jellies are onset-locked (r > 0.3);
- the survivor and the hearth are each at least 300 px tall and centred for at least 3 s;
- there is at most one label at a time and none during a title;
- the Sentinel swings at least 15% on every kick in the rendered video.

## Judged only by viewing
- Does the medusa read as a character who remembers and lets go?
- Is the cut worth watching on its own?
