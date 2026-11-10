# Corrugated Sky · JELLY CUT

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

## Characters (named by register and habitat, after WYGWYL's `cast.json`)
| jelly (rig) | sound | name | wants | gathers |
|---|---|---|---|---|
| sentinel | kick | THE SENTINEL OF THE SILT FLOOR | to keep the house's clock | an alarm clock |
| celluloid ×2 | snare | THE CELLULOID TWINS OF THE KITCHEN | the table set | a cup, a pan |
| doodle ×2 | hats | THE DOODLE SPARKS OF THE RAIN LINE | to fall | an umbrella, a cloud |
| mantle | sub | THE SEWER CREATURE UNDER THE FLOOR | the house to stand | a door |
| glass | choir | THE GLASS MOON OF THE PORCH | to keep the light on | a stove, a lamp, a bulb |
| filmbell | bed | THE FILM BELL OF THE WALL | the family's film back | **Corrugated Sky** (waking, gate, fire, rain) |
| medusa | call | THE AFTERLIGHT MEDUSA AT THE GATE | an answer, then to let go | the dog, a hand letting go, the dog again |

A film's centre follows its gatherer's projected screen position, averaged over the last 0.6 s from the capture's own metadata. **The gathering is the jelly's act**, not a layout.

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

## Rights (unknown is not permission)
Only footage whose own record says `public_domain` is used:
- the secondhand-motion shots, with rights from `paeleo/handmade/kit/found-frames.json`;
- the PAELEO kits, with `source.json` `rights_statement`.

No cineosis-lab clip, no WarGames and nothing unrecorded is used. The Orchestra, the rigs, the song and the film are the producer's own work. See `source-ledger.json`.

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
