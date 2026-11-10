# The Universal Boxback: production record

A music video for **ET TU, BRUTE? · BOXBACK, Track 14 "The Universal Boxback"** (Treblo). It was made with **SCION 06, John Whitney (Harmonic Motion Orchestra)**, from `bolas/paeleo/scion/swarms.json`. The lineage is an interpretation, not an endorsement. The vision texts are the producer's *The House That Language Built* cards: **Aristotle 01** (*from the end to the first step*) and **Plato 02** (*the architect gives directions*).

* Film: `the-universal-boxback.mp4` (173.5 s, 1280×720, 24 fps, H.264 CRF 24 + AAC 192k)
* Proof: `proof.mp4` (b44–80)
* Rebuild: `python3 -I src/phase_search.py`, then `python3 -I src/render.py --out the-universal-boxback --procs 2`, then `python3 -I tests/test_invariants.py`

## Thesis

The viewer should **see a rule**. Two groups of boxes run at 3 and 2. That one ratio makes them separate, pass each other nine times on the beat, and come home together. The same field that dances is also the material of a house that the film shows finished first and then makes.

The defining passage is the Plato test as a motion event. One wrong direction (BEAM 7 → ROW 3) meets a builder's refusal. The next direction moves three boxes and re-phases two rows, and the change visibly climbs the house.

It would be bland as a screensaver: ornamental Lissajous figures that never close, never fail and never become anything.

## Native formal language (kept first-class in `src/film.py`)

* **Parametric trajectories.** Every position is a closed-form function of the beat (`state(b)`). Trails are the same function evaluated in the past.
* **Oscillator bank.** Ten ratio pairs (1:1 … 4:5) × 2 groups. Each box's phase comes from the searched `bank_phases.json`.
* **Phase relationships.** These are the 3:2 ring, rational lock vs detuned drift (`detune_at`), and the 16-beat closure.
* **Event envelope.** `EVENTS` (reunion, interference, lock, land, collision, reseat, beam_lands, home) drive both the flares and the tuned bells (`score.py`). Picture and sound share one source.
* **Compositional field.** This is the sparse → dense → release schedule: `amp_at`, `bank_scale`, `trail_len`, the points-only breakdown and the final ring.

## Beat grid

130.03 BPM, with the offset fitted to low-band onsets and then refined against all onsets (`src/beatgrid.json`). Measured landmarks:

| landmark | beats |
|---|---|
| stop | b77–79.8 |
| breakdown | b304–324 |
| last downbeat | b368 |

## Invariants (`tests/invariants.json`)

| invariant | result |
|---|---|
| A:B lap ratio | 1.50000 (3.0 : 2.0 laps) |
| reunion at b52 and b72 | angle error 0 |
| nine interference passes on even beats | angle error < 1e-14 rad |
| non-pair separation in the proof | ≥ 66.6 px (box height 56) |
| locked bank | closes in 16 beats (error 1e-12 px) |
| detuned bank | does not close (331 px) |
| beam | never seats in row 3 until the re-phase |
| after b264 | house = plan F (≤ 3 px breathing) |
| final frame | equals the opening end form (0.0 px) |

These are **structural**: computed from the trajectories, not tracked from the pixels.

## Method library

| technique | applies when | proof | observed failure | repair | rejected |
|---|---|---|---|---|---|
| 3:2 ring with radial separation | two groups must cross without hiding each other | b48–76 | at reunion, B was drawn exactly over A, so 20 boxes read as 10 | keep a radial floor (36 px) so reunited pairs sit as neighbours with matching labels | identical radii |
| Proof ring size | 10 boxes on the inner ring | b62 | inner ring too small, so B boxes overlapped each other | R 228 → 262, separation 80 → 60 | smaller boxes in the proof |
| Odd-sized ornament | one box is a 264 px beam | b47–72 | the beam collided with its ring neighbours | the beam folds to a 110 px "7" box in the field and unfolds only to enter the house | squashing the label |
| Lissajous bank phases | many boxes on closed curves | b84–112 | equal phases sent every A box to the centre on the lock beats (b96, b104) | per-box phases, then a seeded search: mean contact 2.59 → 0.97 pairs | uniform spacing |
| Ornament scale | dense bank sections | b80–160 | full-size boxes crowded the figure | the boxes shrink to 0.45 during the bank, so the figure reads, not the boxes | fewer boxes |
| Orbit during the making | the house is being built in the middle of the field | b160–238 | the orbit crossed the house | an ellipse that encloses the house (min 72.6 px from any slot) | — |
| Cards vs actors | text overlay during the climax | b238–268 | cards covered the hovering beam and the roof | cards in the left/right columns; the beam hovers at (960, 250) | — |

## Sources and rights

* All boxes, points, trails and cards are drawn in code.
* Two title/end plates are motion-blurred crops of the producer's own BOXBACK art (`source-ledger.json`).
* Bells and key clicks are synthesised (`score.py`) in the song's measured key (A♭ major / F minor) and mixed at −10 dB under the unaltered song.
* Critic round 1: the **proof passes** (3:2 measured as 1077.5° vs 719.9°), and the **film is "reference stronger"**; the r2 repairs are applied. Critic round 2: the **proof passes** and the **film is "reference stronger"** (conditions 3–6 met; the largest gap is the 122–140 s stall); the r3 repairs are applied. Re-review is pending.

### r2 rows (after critic round 1)

| technique | applies when | proof | observed failure (critic) | repair | rejected |
|---|---|---|---|---|---|
| Rain by rows | rebuilding a house from a moving field | b354.9–368 | release pile-up: simultaneous flights overlapped, and the beam crossed boxes | the field lifts away; boxes drop vertically, a row at a time, foundation first (a box's column is empty because the rows above it don't exist yet); overlap 0.000 | simultaneous harmonic arcs |
| Half-frame snap | beat events at 24 fps | b368, b54, b68, title | landings and flashes 0.6–1.3 frames late | picture beat = B(t) + ½ frame, so events land on the nearest frame | rounding each event separately |
| Whole-house re-plan | the Plato test must change the house, not ripple it | b238–264 | rows 1–2 ended where they began | P0 has no door and a flat roof; the refusal forces lift roof → open door → beam → new roof, so every row changes (test C2) | moving three boxes |
| Marker boxes | a ratio must be countable on a phone | b52–72 | 3:2 not countable | box 0 red and box 10 yellow, a 12-o'clock tick, an A×3 / B×2 legend | numbers only |
| Stop as an event | the song stops | b77 | the freeze was identical to the hold | dim, glow off, STOP on the b77 frame (pixel test C4) | — |
| LIFO un-making / lowest-first gather | dissolving and re-forming without collisions | b32–48 | clumps | top rows rise first, straight up; the ring fills from the lowest slot (both 0.000) | blended flights |
| Point capture | moving from free Lissajous paths into a locked ring | b144–148 | clumps at the re-lock; phase search alone barely helped (173 → 154 bad frames) | the boxes collapse to points, blend onto the locked ring, then regrow on the RE-LOCK star b148 | more phase search |

### r3 rows (after critic round 2)

| technique | applies when | proof | observed failure (critic) | repair | rejected |
|---|---|---|---|---|---|
| Accumulation | the finished form must become the densest passage | b266–302 | a 39-beat stall: only shimmer moved, and coverage stayed 4–12% throughout | rigid row cards at 3:2 (odd/even rows) under an accumulating envelope, with filled echo copies; rows re-align every 8 beats; envelope 0 at b302 | box-by-box jitter (would overlap) |
| Fit-to-safe text | any caption or card | whole film | "THE ARRANGEMENT IS THE THING" clipped | every text is measured and shrunk to fit 40–1240; a text log feeds test E1 | hand-tuned sizes |
| Frame-bounded rings | rings near the frame edge | b328–348 | content on row 719 | release ellipses 600×280 / 500×220 centred on y 380 (max y 696.9) | moving the house |
| Open as points | leaving a packed form | b324–328 | the beam lay across six boxes | collapse to points, travel, regrow (the re-lock vocabulary) | staggered flights |
