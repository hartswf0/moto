# Wittgenstein's Backpack — SCION production record

A music video for **ET TU, BRUTE? · BOXBACK — Track 18, "Wittgenstein's Backpack"** (song by Treblo). It was made with two swarm prompts: SCION-TERRY-GILLIAM (*comic cutout metamorphosis*) and SCION-IVAN-SUTHERLAND (*constraint sketchpad*). These prompts take inspiration from those artists' documented techniques. They are not claims that either person wrote or endorsed this work.

* Film: `wittgensteins-backpack.mp4` (3:00, 1280×720, 24 fps, H.264 + AAC)
* Hard-proof clip: `proof.mp4` (beats 16–40)
* Operator page: `index.html`. Constraint editor: `constraint.html` (with `constraint-solver.js`)
* Rebuild: `pip install numpy pillow librosa`, then `python3 -I src/render.py --out wittgensteins-backpack` (about 80 s on 4 cores)
* Tests: `python3 -I tests/test_constraints.py` and `node tests/test-constraint-solver.mjs`

## Thesis

*Everyone has a box, and nobody can look into anyone else's.* The film borrows the beetle-in-a-box, the ladder, the duck-rabbit and the fly-bottle as **physical gags**, not lectures. Each idea gets one image that *does* something:

* a box replaces a head,
* a head becomes a door,
* a word comes out of a box where a beetle should be,
* a ladder is kicked away while the man stays up.

It would be bland as captioned illustrations that merely sit there, or as smooth tweening that hides the paper.

## Protected invariants

| invariant | how it is tested | status |
|---|---|---|
| Every gag event lands on the 128.01 BPM grid (±1 frame) | grid fit to kick onsets (86% within ±28 ms); independent critic frame counts on the proof | measured |
| Constraint scene: bone lengths exact, both feet pinned | `solver-trace.json` per frame; max length error 0.0 px, pin error 0.0 px | measured |
| UNSOLVABLE is reported, not hidden; no joint is stretched to fake contact | trace: unsolvable only in b210–218 (deliberate out-of-reach drag) | measured |
| 1 px pointer moves ⇒ < 6 px joint moves | unit test (5.75 px) | measured, Python + JS |
| Every visible fragment is linked to its source and rights state | `source-ledger.json` | structural |
| The box head lands as the same asset that leapt (continuous scale) | independent critic, proof r2/r3 | perceptually judged |

## Source and rights

* **Picture.** Fragments are cut from the producer's own six BOXBACK artworks in `Et tu, Brute (BOXBACK)/`. Crop boxes and polygons are in `source-ledger.json`. Everything else (dignitary, beetle, duck-rabbit, bottle, fly, doors, giant hand, captions) is a procedural engraving drawn in code for this video.
* **No third-party images are used.** Wikimedia and archive engravings were unreachable from this build environment's network, and image generation was unavailable (the fal account balance was exhausted). The "found engraving" look is therefore drawn, not found.
* **Sound.** The song is the producer's own Treblo track (unaltered). Punctuation SFX are synthesised (`src/sfx.py`) and mixed at −10 dB under the song (`sfx-cues.json`).
* **Captions.** These paraphrase the *Tractatus* (6.54, 7) and *Philosophical Investigations* §293/§309. They are short paraphrases, not quotations of a copyrighted translation.

## Living method library

| technique | applies when | proof clip | observed failure | repair | rejected |
|---|---|---|---|---|---|
| Hard substitution (head → box) | the replacing object already exists in-shot | proof b24–25 | the leaping box was a different asset and drawn behind the head, so it read as a cut to another puppet | use the same asset; draw it in front; grow it continuously along the arc; hide the old head once it is covered | a cross-dissolve (reads as a glitch) |
| Puppet continuity through a gag | any substitution | proof b25 | lean change + both arms up revealed the vest, so "a different man" | lock lean and the near arm; only the far arm flies up | a squash on impact (changed the silhouette) |
| Door-from-object | the object has a flat face | proof b27–29 | a black square read as a hole | engraved panel door with a frame and knob, shown closed for a beat before it opens | photo-crop door panel |
| Crowd exits a door | the door is small relative to the walkers | proof b30–40 | minis 2× the door height looked pasted on | fit inside the opening, then grow while falling (Gilliam scale cheat) | constant scale |
| Constraint pull | hand held-by a moving handle | sketch b220–236 | hinge on the far side pulled the handle out of reach: hand 25 px off while the overlay said held-by | hinge on the near side; the trace proves 0.0 px | silently teleporting the hand |
| Pre-grab pen | the cursor approaches the figure | sketch b203–206 | the solver chased the cursor before the grab, reporting false UNSOLVABLE | hold the rest pose until the grab | — |
| Enlarge | object scale > 3× | ops b256 | upscaled sprite pixelated | separate high-resolution engraving variant | — |
| Background plates | busy album art behind gags | stack b72 | plate repeated the label boxes being animated | crop to the mural wall | full plate |
