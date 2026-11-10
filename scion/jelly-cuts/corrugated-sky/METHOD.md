# Corrugated Sky · JELLY CUT

**Round 1 (independent critic): proof reference stronger, film reference stronger. r2 applies the repairs; re-review pending.**

A second cut of *Corrugated Sky* (BOXBACK track 11; the accepted SCION 02 Reiniger film). This time the film goes into the contaminant-jelly water. **The Jelly Orchestra plays the song.** Each jelly is one sound role, and each one gathers a film. The BOXBACK film is one of those films, and a counter-archive of public-domain home movies and industrials drifts through the water as flecks that rhyme with the house.

* Film: `corrugated-sky-jelly.mp4` (2:26, 1280×720, 24 fps, the unaltered song)
* Hard proof: `proof.mp4` (song 64–93 s, cut from the film)
* Pipeline: `../src/` (`cast_song.py` → `orchestra.html` + `orchestra_capture.js` → `jellycut.py`), with one config per film (`jellycut.json`)
* Tests: `python3 -I tests/test_jellycut.py` → `tests/invariants.json`

## Thesis
The house in Bradbury's story keeps serving a family that is gone. Here a whole water keeps playing a song for a house that is gone. The house's films have become things the jellies carry. The film is no longer the world; **it is a memory one of the animals holds.** It would be bland as "the old video with jellyfish wallpaper behind it". So every film is gathered by a named character, condenses from the water by a rule, and goes back to the water by the same rule.

## The layers (picture = f(t))
1. **The Jelly Orchestra:** the real `bonus/jellyorchestra.html` from contaminant-jelly, with its drift rigs, water, snow, light shafts and bloom.
   * It is rendered offline in headless Chromium on a deterministic clock: seeded `Math.random`, and a song time we step ourselves, frame by frame.
   * Its song entry is built from our track (`cast.json`) by onset analysis per sound role: kick 30–140 Hz, snare 1.5–4.5 kHz, hats 7–11 kHz; bass, choir and bed from HPSS harmonic energy over 2, 4 and 8 beats; call from harmonic onset peaks, at most one per bar.
   * The camera cycles the Orchestra's four widest shots on its 4-bar cut grid.
   * The full film was captured in two halves. The seam sits on a 4-bar camera cut at 68.06 s, so the cut hides it.
2. **Films as flecks.** This follows the contaminant-jelly rule that films are only clouds of flecks, under **the dot law** borrowed from WYGWYL (hartswf0/butterfly-halfworld, `wygwyl/README.md`, "THE LAWS"):
   * eight ink levels;
   * one ordered (Bayer) halftone pass;
   * **no alpha.**

   A film condenses by **per-dot allegiance on a Bayer schedule**. Dot *k* is in the picture iff *c ≥ θₖ*, otherwise it is a drifting fleck. Release runs the same schedule backwards. Far films are inked darker: fog is an ink colour, not a transparency.
3. **Cards:** title, cast and gathering labels with source, timecode and rights. Text only.

## Characters: every film is a performance by the jelly that holds it (r2)
Round 1's critic found that the jellies did not perform the films. A medusa "gathered" the dog only in its label, and the jelly meant to hold the house film was off screen during every bloom. **The cause:** films were placed beside jellies the camera might not show.

**The r2 fix:** the real Orchestra jellies are **directed** (`direct.json`, written by `build_cut.py`, which also writes the compositor timeline, so the two cannot drift apart). Each held film is a performance:

1. **attention:** at least 1.5 s before the picture condenses, its jelly turns toward the camera and comes forward. It pulses twice a beat.
2. **gesture and resistance:** the picture condenses *hanging from the jelly's bell*, under its projected position. It moves when the jelly moves. While it holds the picture the jelly pulses on every beat.
3. **changed state:** at the release the jelly goes somewhere else for at least 2 bars, and its extra pulses stop.

| jelly (rig) | sound | name | holds |
|---|---|---|---|
| sentinel | kick | THE SENTINEL OF THE SILT FLOOR | nothing: it keeps the house's clock in the lower left, all song, with a halo on every kick |
| celluloid ×2 | snare | THE CELLULOID TWINS OF THE KITCHEN | a NASA cup; *Interior of a House* (Andrews) |
| doodle | hats | THE DOODLE SPARKS OF THE RAIN LINE | *Twilight after the Rain* (MacGilvary, 1906) |
| mantle | sub | THE SEWER CREATURE UNDER THE FLOOR | a survivor sitting still in the snow (*Survival Stresses*, 1961), then a door opened (*Straight Talk*) |
| glass | choir | THE GLASS MOON OF THE PORCH | the family portrait (*Father, Mother, and Boy*, Medford, 1841), then a lamp being checked (*Anthracite*, MSHA) |
| filmbell | bed | THE FILM BELL OF THE WALL | **Corrugated Sky**: the house waking, the gate, the fire, the rain |
| medusa | call | THE AFTERLIGHT MEDUSA AT THE GATE | *Young Girl and Dog* (Moran, 1890). At the let-go it **releases them into the gate film's dog**. Later it keeps *Dogs on the Hearth* (Weir, 1887) |

## What the layer now means (Ernst / Mouris)
The counter-archive answers the film; it does not illustrate it:
- **The hybrid that causes the next.** At the let-go (84.83 s), the Afterlight Medusa lets the painted girl and dog go, and their flecks stream into the silhouette dog at the gate. The jelly lets the dog go *with* the girl, and the archive becomes the film.
- **One motif, changed function.** The painted dog returns at the end as a dog kept by a hearth. It is no longer let go; it is kept.
- **The answer to the fire.** The house burns, and a 1961 government survival film supplies someone who survived, sitting still outside. Bradbury's house was the aftermath of a bomb; the civil-defence era's own footage answers it.
- **The light.** The Glass Moon wants to keep the light on, and it is the one that holds the lamp being checked.

## Grammar borrowed from the mixed-media swarms (bolas `paeleo/scion/swarms.json`)
| swarm | rule | used as |
|---|---|---|
| **SCION 03 Ernst** | one motif repeats in a changed function | the archive DOG is gathered at the gate (66–77 s) and returns in the rain, kept beside the house (134–145.6 s) |
| **SCION 04 Mouris** | density through recurrence and changes of speed, plus two deliberate holds | the Film Bell recurs four times; holds on the gate bloom (76–89 s, 13 s) and the end title (141.6–145.7 s) |
| **SCION 44 Multiplane Parallax** | flat archive gets depth without incoherent space | films live at depths: far ones darker and smaller, bloomed ones near |
| **SCION 53 Civic Footage** | an afterlife without erasing documentary status | every archive film keeps its frame edge. SAM masks only raise the subject's ink, and the rest of the frame stays. The label carries source, timecode and rights |
| **SCION 54 Provenance Graph** | every composite reconstructable | `source-ledger.json` is a node and operation graph: source → analyse → render-orchestra → halftone-fleck → composite |

## References inspected
- contaminant-jelly `current/drift/DRIFTS.md` reference plates (lit haze, near-black silhouettes, marine snow, kelp light) and the level recordings in `current/drift/play/`
- `bonus/SCION_FILM_AS_JELLY.md` (film as matter: the frame's pixels are particles)
- PAELEO handmade kits (`paeleo/handmade/kit/archive-dog`, `archive-door`)
- WYGWYL atlas laws

## Rights (unknown is not permission), r2
Every source now carries a stated **basis** in `source-ledger.json`. Sources whose basis the record does not state were **dropped rather than guessed**:
- This Is Coffee
- Don't Be Afraid
- Frigidaire Imperial Line
- the Amateur Film New Jersey home movie
- the Summers 1941 amateur film
- Light Of Your Life
- Top Of The Cloud
- Door to Heaven

Kept:

| source | basis |
|---|---|
| NASA Ames LunarBioLab clip | US government work (NASA) |
| *Anthracite* (archive.org gov.msha) | probable US government work |
| *Survival Stresses* (archive.org hmdvid, NLM historical audiovisuals) | probable US government work |
| *Straight Talk* (archive.org gov.ntis) | probable US government work |
| Smithsonian Open Access paintings and prints | CC0 (record access: CC0) |

For each "probable US government work" source, the producer is **not verified from here**, and the ledger says so. The Orchestra, rigs, song and film are the producer's own work.

## Invariants
| invariant | how | status |
|---|---|---|
| each role onset starts its jelly's pulse within ±1 frame | `tests/test_jellycut.py` on the capture metadata | measured |
| at most 8 ink levels in a condensed film | spy on the dot renderer | measured |
| every drawn source is public domain or the producer's own, and PD sources carry a URL | ledger check | structural |
| two holds of at least 4 s | config | structural |
| the archive dog recurs in a changed role | config | structural |

## What is judged only by viewing
- whether the gate bloom still carries the let-go;
- whether the counter-archive rhymes or only decorates.

These are for the independent critic.

## Per additional film
Each further film needs:
- a config;
- the cast (one command);
- a capture of about 25 min wall time on 2 processes;
- a fleck timeline with its own rhymes and gatherers (the creative work);
- a render of about 5 min.
