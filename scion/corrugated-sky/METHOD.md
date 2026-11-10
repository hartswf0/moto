# Corrugated Sky: SCION-REINIGER production record

This is a music video for **ET TU, BRUTE? · BOXBACK, track 11, "Corrugated Sky"** (Treblo). It was made with SCION 02, *Lotte Reiniger: Articulated Shadow Theater* (bolas/paeleo/scion, swarm id 2). The swarm is a lineage, not an endorsement.

The vision follows Ray Bradbury's "There Will Come Soft Rains" (1950) **as theme only**: a house runs its day for a family who are gone, their shapes are left on the wall, a dog comes home, then fire, then rain. No sentence of the story or the poem is used. The house's voice cards are original.

* Grid (r1): 141.05 BPM, beat 0.42538 s, offset 0.345 s; full-band onset phase lock 0.23 (thirds 0.09 / 0.33 / 0.27, consistent phase 0.348 / 0.352 / 0.336 s). r0 was 140.84 BPM at 0.300 s, which led the onsets by ~60 ms mid-song.
* Film: `corrugated-sky.mp4` (2:26, 1280×720, 24 fps; poses on twos, i.e. 12 fps cut-out timing)
* Proof: `proof.mp4` (beats 172–210)
* Rebuild: `python3 -I src/render.py --out corrugated-sky --procs 2`
* Tests: `python3 -I tests/test_invariants.py` writes `invariants.json`

## Thesis

Everything must read from contour alone. The family survives only as **negative space**, lit places cut in a black wall. At night those places let them out: black figures step out of their own light and leave the light behind. The bland version would be a lit diorama with silhouettes standing in it. Here the hole *is* the character.

## Defining passage (hard proof, b176–208)

At night the girl climbs the garden gate to reach the dog shut outside. She hesitates and turns between the dog and her mother. She offers her hand. The dog rises, and its paw meets her hand. The mother calls. Her hand opens (a replacement profile) and she lets go. Then she climbs down and goes back to the wall.

## Protected invariants

| invariant | test | status |
|---|---|---|
| Joint-angle limits are never exceeded: no pose *requests* an angle outside its limit | every proof frame, plus every 6th film frame | measured |
| Pinned holds stay pinned: hand/foot on the gate and paw on hand residual < 1 px | 1,084 pinned samples in the proof | measured (worst 0.78 px) |
| Pinned joints never detach: each child bone starts at its parent pin | FK check over proof poses | measured (1e-13 px) |
| Silhouettes do not merge: girl and dog overlap only at the contact | mask overlap < 1.5% of the smaller shape | measured (1.2%, at the paw) |
| Relationships read with colour removed | — | perceptual (critic) |

## Method library

| technique | conditions | failure seen | repair | rejected |
|---|---|---|---|---|
| Family as lit holes in a black wall | the dead and absent | four holes overlapping into one white blob | widen the wall; space the poses about 125 px | outlined figures |
| Gate climb by two-bone IK on keyed holds, one limb per beat | contact acting | holds placed out of reach (hand 22–43 px off while "pinned") | key the holds from shoulder/hip reach, end crouched on the rail; the test proves < 1 px | stretching the arm |
| Choosing the IK branch | elbow/knee could bend either way | wrong branch broke joint limits | `ik_pick` tries both branches and keeps the one inside the limits | clamping (breaks contact) |
| Dog meets hand | two characters touching across a gate | the long dog body covered the gate and the girl (blob) | smaller dog; it rises *while* stepping in, so its leading edge stays right of x≈690 | a bigger gap with no touch |
| The house's voice | announcements in a silent-film world | — | black banner lowered on strings, text cut out so the light shows through | subtitles |
| Letting go must be HER act (r1) | a release between two characters | read as the dog letting go: its paws folded first and her hand change was a few px | order: hand opens (spread fan + 55° wrist turn) → arm withdraws (+6 frames) → paw folds (+6 more); tested by frame order and changed-region span at 360 px (21 px) | — |
| Head turn (r1) | a look between two targets | only the nose and bow flipped (invisible at 360 px) | replacement head profile (fwd/back) + chin drop + torso ±; the pelvis slides to keep both holds pinned | rotating the head alone |
| Grasp (r1) | hand meets paw | hand and paw knotted | 'offer' profile: flat palm, thumb split by a V of light; the paw rests on the palm (computed palm point) | grip disc |
| Fire (r1) | fire read without colour | spikes read as weeds; collapse cut off-screen; ovals of smoke | curved tapering tongues, new cut every 12-fps pose; the shell sinks and leans on screen (b280–292); roof sheets fall slower; separate puffs | flicker by colour |
| Absent family (r1) | figures stepping out of the wall | 8 figures on screen at once | a place goes solid black as its figure steps out and relights as it is absorbed | lit holes throughout |
| Dog at the return (r1) | dog near the gate and fire | posts through the dog, legs hidden | gate moved left, no fence right of it, fire burns behind the wall; tested: 0 shared px, one region, 4 legs + tail visible | — |
| Proof legibility | a phone-size reading | figures about 150 px tall | camera push-in to 1.55× on the gate | a bigger rig (broke reach geometry) |
| Title card | slate style after the *Touki Bouki* red title | — | red letter-spaced Inter ExtraBold over a motion-blurred silhouette street | — |
