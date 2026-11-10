# The Whole Package — SCION production record

A music video for **ET TU, BRUTE? · BOXBACK, track 15, "The Whole Package"** (song by Treblo). It was made with the swarm prompt **SCION 05 · Yuri Norstein — Atmospheric Multiplane Cinema** (`bolas/paeleo/scion/swarms.json`, id 5). The swarm name is a lineage, not a claim that Norstein made or endorsed this.

The theme comes from Nnedi Okorafor's story "Mother of Invention" (*Future Tense Fiction*), used as **theme only**: a pregnant woman whose community has shut her out, an engineered pollen storm, and a house that seals itself and carries her through. No sentences, names or the house's name are taken from the story. Every message the house speaks was written for this film.

* Film: `the-whole-package.mp4` (2:31, 1280×720, 24 fps)
* Proof: `proof.mp4` (beats 110–150)
* Rebuild: `python3 -I src/render.py --out the-whole-package --procs 2` (about 0.3 s per frame per process)
* Tests: `python3 -I tests/test_multiplane.py` (writes `multiplane-tests.json`) and `python3 -I tests/test_audio.py [film.mp4] [clip_start_beat]` (writes `audio-tests.json`)
* Audio is mixed in Python (`render.make_mix`): the song is ducked by `film.song_gain` under the hush, and the depth SFX stem is added at 0.42. Pan and duck are exact and measurable.

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
| The hand pans with its screen x: (R−L)/(R+L) > 0.3 during b136.2–137.2 | `tests/test_audio.py` on the final mix | measured (see `audio-tests.json`) |
| The hush is audible: ≥ 6 dB dip at b134.4–136.4 vs b131.5–133.5 | same | measured |
| The mix is not mono over the proof (L/R correlation < 0.98) | same | measured: barely (0.977); the song itself is close to mono |
| The proof reads with the colour removed | — | not judged |

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

## Critic round 1 and repairs

Verdict: **proof reference stronger (narrowly), film reference stronger.** One bounded repair pass followed. Re-review is pending.

| # | failure (critic) | cause | repair | condition |
|---|---|---|---|---|
| 1 | The nearer hand entered from off-frame and read as a pole | the arm was rooted off-screen with no link to the house; the glow hid the hand | the arm grows out of the house's middle box (root = projected house + offset), as three jointed box segments with visible seams; an open palm with four fingers and a thumb (1.8×); a near grass clump (z 1.5, world x 1062) crosses it; the glow is reduced to 45% | the arm starts at the house body, overlaps a foreground occluder, and the hand reads in silhouette |
| 2 | Baby reveal: a second copy of her stayed in the midground; the bundle read as a sticker; the reveal wasn't tied to the fog | the close-up composited over `exterior()`, which still drew her; the package *was* the label | `exterior(hide_woman=True)`; an open box with a swaddled baby silhouette (head, body, raised fist) at 1.4×, with the label back on the box; a near fog plane (z ≈ 1.2) parts over the baby at b232.6–235 | one of her; the baby readable at 360 px; fog parts at the reveal |
| 3 | Sound was effectively mono; the hush had no dip | the SFX stem sat under a centred song at 0.34; the wind bed came back at b136.5 | a Python mix with `song_gain`: −9 dB b134–136.1, −12 dB b136.1–137.4, −6 dB to b138.6, release by b139.3. The servo is split into 10 grains panned by the hand's screen x (`arm_pan`, a steep law of 2.4×). The wind bed stays down until the hands meet (b139) | measured pan > 0.3 toward the arm; dip ≥ 6 dB |
| 4 | The interior had no parallax, with identical frames | a single flat layer | three planes (back wall k 0.4, her k 1.0, near torn flaps and dust k 2.2) with a slow push of +10% over b150–191, a 1.8% breath on every beat, and a lateral drift | a near plane moves against her; the pulse is kept |
| 5 | FOLLOW MY LIGHT with no glow until b116 | the camera tracked her only; the house was off-frame right | the camera weights her and the house (0.6·wx + 0.4·house); occluders re-solved for that camera (laundry 530, boxes 830) | the glow is in frame at b112 |
| 6 | Captions about 7 px at phone size, contrast 1.7:1 | 40 px mono in light gold on gold fog | 80 px Inter ExtraBold, wrapped to ≤ 1100 px, warm white on a dark band (α 0.75). Contrast is about 11:1 over the gold fog (computed: text (255,238,206) on band ≈ (59,49,24)) | ≥ 3× size, ≥ 4.5:1 |
| 7 | 0:08–0:20 nearly static | the camera locked on her while she walked | a held frame b16–40: she crosses the whole frame and the village windows (now 24×26 world units) go dark one by one behind her | an action in the shot |

## Critic round 2 and repairs

Verdict: **proof reference stronger, film inconclusive.** Met and untouched: the hush, the interior parallax, the glow at b112, captions, the 0:08–0:20 walk, one of her with the fog parting at dawn.

The failure persisted on the same beat after two fixes (b139, the nearer hand), so per doctrine §6 the *model* changed, not the parameters.

| | round 1 model (failed) | round 2 model |
|---|---|---|
| Hypothesis | "the hand reads as the house's if it comes from the house's direction" | "it reads as the house's only if root, arm and hand are all in one frame, the house body is visible, and the arm is the nearest plane" |
| Staging | the camera tracked her; the house was off-frame or ghosted; the arm came in from the frame edge | while she is lost the camera settles at x 1100, solved so the z 2.0 box stack (world 830–988) clears her (cam ≥ 1094). She is at screen x ≈ 354 and the house body is at 480–900 beside her |
| Depth | the arm was drawn at z 3.0 inside the plane loop, so a stalk drew over it and the focus blurred it | the arm is the nearest plane (ARM_Z 1.3 < stalk 1.5 < her 4.2), drawn after fog and focus, crisp. A stalk at world x 1112 sits under the forearm |
| Fog | the fog in front of her was a full-frame slab, so it also hid the house behind her | from b136.3 the near fog shrinks to a **pocket around her** (`pocket_mask`); the house body clears over b136.3–137.0; she still goes faint-to-crisp on HERE (k2, b137–139) |
| Hand | a blurred mitt | `draw_hand`: palm, four separated fingers (spread ±11°, ±33°), thumb, crisp outline |
| Sound | servo grains panned by the hand tip, which travels toward the centre, and peak-normalised with the stem (the servo *was* the peak, so gain did nothing) | the servo is its own track (`film.servo_cues`, `render.SERVO_GAIN` 0.55), starting one beat later (b137–139.25) and panned by the **elbow** joint, which stays at the house. The HERE chime is panned to the house. The duck holds −12 dB to b138 and −6 dB to b138.8 |
| Baby | the head sat by her face; a fist near her chin; a mini box in her hands | `baby_geometry`: the box forward and lower (×1.7); the fist raised on the far side; no hand-held box; the glow moved off the baby |

New assertions are in `tests/test_reach.py` (written to `reach-tests.json`): (a) the arm root lies on the house silhouette and in frame, and the house's fog opacity is < 0.35 through b137–139 (computed with the compositor's own rule, `film.fog_opacity_at`); (b) the depth order, drawn after fog, and the chain crossing the stalk; (c) the finger count on an arc at 360 px; (e) the baby's separation from her head at 360 px. `tests/test_audio.py` now measures pan over **b137–139**.
