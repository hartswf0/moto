# The Whole Package — SCION production record

A music video for **ET TU, BRUTE? · BOXBACK, track 15, "The Whole Package"** (song by Treblo). It was made with the swarm prompt **SCION 05 · Yuri Norstein — Atmospheric Multiplane Cinema** (`bolas/paeleo/scion/swarms.json`, id 5). The swarm name is a lineage, not a claim that Norstein made or endorsed this.

The theme comes from Nnedi Okorafor's story "Mother of Invention" (*Future Tense Fiction*), used as **theme only**: a pregnant woman whose community has shut her out, an engineered pollen storm, and a house that seals itself and carries her through. No sentences, names or the house's name are taken from the story. Every message the house speaks was written for this film.

* Film: `the-whole-package.mp4` (2:31, 1280×720, 24 fps)
* Proof: `proof.mp4` (beats 110–150)
* Rebuild: `python3 -I src/render.py --out the-whole-package --procs 2` (about 0.3 s per frame per process)
* Tests: `python3 -I tests/test_multiplane.py`, which writes `multiplane-tests.json`

## Thesis

**The fog lies about distance, and the near hand is the truth.** She follows the house's light; the pollen makes it look far, then hides it. What saves her is something closer than she expected: the house itself, reaching out of the fog.

The film would be bland as a flat scroll with a uniform yellow wash, or if the storm were weather rather than a decision-making atmosphere.

## Native primitives (kept in code, not baked into pixels)

* **Glass planes** at explicit z: sky 60, far hills 30, near hills 18, village 14, house 6, woman 4.6/4.2, laundry 3.3/2.7, the house's arm 3.0, box stack 2.0, grass 1.5.
  * Projection: `sx = W/2 + (wx − cam_x)/z · F`, with `F = 6` (`src/mp.py`).
* **Fog field.** A slab between each pair of consecutive planes. Each slab has its own tiled fBm noise that scrolls at that slab's parallax rate plus drift, and an opacity of `1 − exp(−σ(z, t)·Δz)`.
  * Atmosphere states set σ: **reveal / lure / obscure / suspend** (`film.fog_state`).
* **Focus schedule.** The blur radius is ∝ |1/z − 1/focus_z|. Focus is at 5.0 for the day, 4.4 for the proof, and on the near plane for the dawn close-up.
* **Depth audio** (`src/sfx3d.py`). Each cue has a z and a pan:
  * gain ∝ 1/(1 + 0.12 z)
  * the low-pass cutoff falls with z
  * the wind bed is brighter when the storm is near and dull through the sealed walls
  * the **suspend** beat (b134–136.5) drops the wind to −49 dB (measured on `out/sfx.wav`)

## Proof scene (beats; 110.445 BPM, beat b at t = −0.047 + 0.54326·b s)

| beat | event | atmosphere |
|---|---|---|
| 112 | the house writes FOLLOW MY LIGHT.; her light is a halo in the fog | lure |
| 113.5–130 | she walks toward it; foreground grass (z 1.5) crosses her | lure: the house body is hidden, only its glow shows |
| ≈120 | she passes behind the hanging laundry (z 2.7) | lure |
| ≈127 | she passes behind the stacked boxes (z 2.0) | lure |
| 130–131.5 | the fog closes in front of her; the light goes out | obscure |
| 131 | I CANNOT SEE YOU. She stops and looks left and right (b131–133) | obscure |
| 134–136.5 | the motes stop moving and the wind drops to near silence | suspend |
| 136–139 | the house's arm (z 3.0, nearer than her) reaches out of the fog from the upper right; she reaches; their hands meet at b139 (chime, panned right) | the fog thins at her depth first |
| 138 | HERE. | reveal |
| 139–143 | the house is revealed right beside her | reveal |
| 144–149 | the door opens; she goes in; the door shuts and is taped | — |

## Invariants

| invariant | evidence | status |
|---|---|---|
| Parallax speed ratio equals the depth ratio for every pair of 11 planes, on every frame where the camera moves | `tests/test_multiplane.py` (2,356 frames, max relative error 5e-11) | measured |
| Parallax speed is monotonic in 1/z | same test, 0 violations | measured |
| Fog optical depth never decreases with distance (far is never clearer than near) | same test, 515 frames | measured |
| The obscure state is depth-shaped (the arm's depth is clearer than hers) | same test: α 0.76 vs 0.97 (single-point proxy) | measured |
| Every message is original | `MESSAGES` in `src/film.py` | structural |
| The proof reads with the colour removed | — | not yet judged by an independent critic |

## Sources and rights

* Everything is drawn in code: the woman's silhouette, the box house, the village, hills, grass, laundry, the arm, fog and sky.
* One fragment comes from the producer's own artwork: the HANDLE WITH CARE label on the package, cut from `Et tu, Brute (BOXBACK)/Boxback lumbar brace flat-lay.png` (see `source-ledger.json`).
* The song is unaltered. The SFX are synthesised (`sfx-cues.json`).

## Method library

| technique | applies when | proof | failure seen | repair | rejected |
|---|---|---|---|---|---|
| Occluder timing from projection | a tracking camera, an occluder at a different z | b120/b127 | she was lost *behind the laundry* instead of in fog | solve for the occluder world-x where its screen-x meets hers (ox = wx + cam_off·(1 − z_occ/z_her)) | placing occluders by eye |
| Lure = hide the source body, keep its glow | a light that should seem far | b112–130 | the house body showed through the thin fog, so there was no depth ambiguity | σ ramps sharply behind her depth (z > 4.6) | a bigger glow alone |
| Lost = fog *in front of* her | the "loses position" beat | b130–136 | she stayed crisp in the fog | add σ for z > 2.6 in the obscure state; the arm stays clear because it is nearer | dimming her sprite directly |
| Ground line inside frame | a figure at a new depth | all | feet were cut off (the ground at z 4.2 projected below the frame) | GROUND 300 → 220 | — |
| Silhouette hand | a nearer helper must read at once | b136–139 | the kraft arm vanished against the gold fog | a dark jointed arm with seams; a pale cardboard palm and fingers | box beads (they read as dots) |
