# THE PhD OF MUSK — PACING & BEAT PROFILE
### Measured bar map, cross-checked against the 60-block SCENT VECTOR cartoon treatment

Interactive sheet: `phd-of-musk-xsheet.html` · Machine contract: `phd-of-musk.orchestration.json`

---

## 1. The headline

**The treatment is already locked to the song's bar grid. Block N = bar N.**

All six of the script's section boundaries land on boundaries the audio analysis found
independently, with no knowledge of the lyric sheet:

| Script boundary | Block | Song boundary found by DSP | Match |
|---|---|---|---|
| VERSE 1 in | 04 | bar 4 — full band enters (low band 0.00 → 0.86) | ✓ |
| HOOK I in | 20 | bar 20 — low band gated out (0.90 → 0.35) | ✓ |
| VERSE 2 in | 28 | bar 28 — full band returns | ✓ |
| HOOK II in | 44 | bar 44 — low band gated out again | ✓ |
| BRIDGE in | 52 | bar 52 — lead leaves centre (0.945 → 0.735) | ✓ |
| OUTRO in | 58 | bar 58 — breakdown, hats gone (high 0.80 → 0.05) | ✓ |

Six for six. One block is one bar is **2.3279 seconds**. Nothing needs re-timing.

**And the storyboard stops at bar 60 of 108.** The iris-out lands at **2:22.8** of a **4:11.29**
song. 48 bars — **1 minute 52 seconds, 44.5% of the track** — have nothing written for them.

---

## 2. Beat profile

| | |
|---|---|
| Duration | 251.29 s (4:11.29) |
| Tempo | **103.10 BPM** (spectral-flux autocorrelation; top-3 candidates 103.1 / 103.0 / 102.9) |
| Beat | 0.58197 s |
| Bar (4/4) | 2.32787 s |
| Downbeat phase | 0.817 s |
| Bars | 108 |
| Beats | 432 |

### Conform before drawing

At 24 fps a beat is **13.967 frames** — not an integer. Un-conformed, a bar-locked board drifts
14.5 frames (0.6 s) by the last bar.

**Slow the master by 0.235%** (ratio 1.002361 → 102.8571 BPM) and the whole song becomes an
integer frame grid:

| Beat | Bar | 8-bar phrase | Whole song |
|---|---|---|---|
| 14 frames | 56 frames | 448 frames | 6048 frames = 252.000 s |

0.235% is far below audibility. Every downbeat then lands on a whole frame for 4 minutes.
One block = 56 frames = 28 drawings on twos = one full
anticipation → action → impact → hold → settle cycle. Which is one gag. Which is how the
treatment is already written.

---

## 3. Section map

Boundaries from a checkerboard-kernel novelty curve on a bar-synchronous log-mel self-similarity
matrix, confirmed against low/high band gating.

| ID | Bars | Time | Frames | State | Blocks | What it does |
|---|---|---|---|---|---|---|
| INTRO | 0–3 | 0:00.82 | 0–224 | sparse | 01–03 | No drums, no low end. First onset at bar 3. |
| A1 | 4–11 | 0:10.13 | 224–672 | full | 04–11 | Full band enters. Verse bed 1. |
| A2 | 12–19 | 0:28.75 | 672–1120 | full | 12–19 | Verse bed 2 — **A1~A2 = −0.19, a genuinely different bed.** |
| B1 | 20–27 | 0:47.37 | 1120–1568 | bass gated | 20–27 | HOOK. Low band 0.35 vs 0.90. Hats + lead only. Weightless. |
| A3 | 28–35 | 1:06.00 | 1568–2016 | full | 28–35 | Verse bed 1 repeat (A1~A3 = 0.89). |
| A4 | 36–43 | 1:24.62 | 2016–2464 | full | 36–43 | Verse bed 2 repeat (A2~A4 = 0.98). Brightest bars in the song. |
| B2 | 44–51 | 1:43.24 | 2464–2912 | bass gated | 44–51 | HOOK repeat. **B1~B2 = 0.99** — near-identical. |
| C | 52–57 | 2:01.86 | 2912–3248 | lead out | 52–57 | Low band at maximum; lead leaves centre (0.945 → 0.735). |
| D | 58–65 | 2:15.83 | 3248–3696 | breakdown | 58–60 **+5 empty** | Hats gone (0.03–0.08), onset ≈ 0. Emptiest 18.6 s in the song. |
| E | 66–69 | 2:34.45 | 3696–3920 | build | — | Kick back at full (0.98), hats still absent. |
| F | 70–75 | 2:43.77 | 3920–4256 | full | — | Full band return. Shares timbre with C (0.81). |
| G | 76–107 | 2:57.73 | 4256–6048 | **new** | — | **32 bars / 74 s unlike anything earlier.** vs A4 = −0.82. |

### The three things the arrangement actually does

1. **The bass is the hook marker.** Low-band energy drops from ~0.90 to ~0.35 for exactly
   8 bars, twice, at bars 20 and 44. That is the hook, and it is *weightless* — the one place
   in the song where gravity gags have no low end under them and float gags land.
2. **The hats are the breakdown marker.** High-band collapses to 0.03–0.08 across bars 58–65.
   Fast cutting there reads as noise. That section wants holds.
3. **The lead steps out of centre exactly once**, at bars 52–57 (C). Everywhere else the
   centre-ratio sits at 0.92–0.96.

---

## 4. The gap — bars 61–107

Section **G** (bars 76–107) is not a tail. Its cosine similarity to every earlier section is
negative (−0.82 against the verse bed). It is darker (centroid 1650 Hz vs 2200 in the verses),
the hats are gone (high 0.12–0.27), a centred lead runs through all of it, and it lasts
**74 seconds**. It is a third movement the treatment never saw.

### Recommended: extend, don't redistribute

Keep block N = bar N exactly as written and author 47 new bars. The treatment already carries
the grammar — blocks 44–51 are explicit REPRISE variants of 20–27, so the reprise logic is
established.

- **D / E / F (bars 58–75)** become the climax the breakdown is built for. Block 60's payoff
  ("Guess which one found dinner") sits at bar 60, mid-breakdown — a superb place to *drop*
  the punchline, a terrible place to iris out.
- **G (bars 76–107)** becomes a wordless 32-bar coda: the one stretch where the film stops
  making jokes and just follows the nose.

### Alternative: cut the song

Edit the master to end at bar 60 for a 2:25 video. Bars 58–65 are already a breakdown, so an
ending built there needs a tail, not a fabricated fade. Cheap, and not a bad film — but it
spends the strongest structural gift the track offers, which is that the breakdown arrives
*before* the ending rather than at it.

### Do not: spread 60 blocks across 108 bars

That puts 1.8 bars under each gag, destroys the 1:1 lock, and moves all six section boundaries
off the music. The alignment is the asset.

---

## 5. Per-bar budgets

Every bar in the JSON carries a `key_budget` and `multiplane_layers` derived from its measured
onset density:

| Onset density | Keys | Planes in motion | Read as |
|---|---|---|---|
| < 0.15 | 2 | 2 | hold, single move, deep stillness |
| 0.15–0.40 | 3 | 4 | one anticipation + one action |
| 0.40–0.70 | 4 | 7 | full gag, full stack |
| > 0.70 | 5 | 7 | impact frames, scramble |

These are ceilings read off the music, not style preferences. A five-key scramble staged on a
two-key bar has nothing under it.

---

## 6. Reasoning protocol for a downstream model

1. **Take the grid as given, not as a variable.** Bar *n* starts at frame 56*n* in conformed
   time. Never re-derive tempo. If a gag does not fit 56 frames, cut the gag, not the bar.
2. **Read the bar's measured state before writing its action.** LOW < 0.45 means no bass under
   it. HIGH < 0.10 means no hats — hold, don't cut.
3. **Respect section identity, not just energy.** B1≡B2 and A2≡A4 give guaranteed rhymes 16 and
   24 bars apart. G rhymes with nothing, so it must introduce rather than reprise.
4. **Author the 47 missing bars against the same schema** — CINEOSIS operation, physical action,
   keys, multiplane assignment — then check against the row's budget, not against taste.
5. **Put the running gags on a schedule.** The bent blade of grass, the sardine tin, the fishbone
   grin, the nose-as-compass. Closer than 8 bars reads as a continuity error; further than 32
   reads as a new object.
6. **Validate the board before rendering.** Every bar 0–107 has exactly one block; no block spans
   a section boundary; total frames = 6048; every gag's key count ≤ its row's budget.

---

## 7. Method and its limits

- Tempo: spectral-flux onset envelope → autocorrelation over 60–190 BPM with 1/2 and 1/4 lag
  reinforcement. Downbeat by phase search maximising mean flux on the bar grid.
- Sections: checkerboard-kernel novelty on a bar-synchronous log-mel SSM (36 bands, 60 Hz–9 kHz),
  cross-checked against low- and high-band gating, which is unambiguous.
- **LEAD** is the ratio of mid-channel to mid-plus-side energy in 250–3800 Hz. It detects a
  *centred lead element*, not specifically a voice.
- **One open question for a human ear:** section C's centre-ratio drop to 0.735 means the lead
  leaves the centre. Whether it stops singing or is merely widened/doubled cannot be settled from
  the spectrum. A syllable-rate (3–8 Hz) modulation test was run and did not discriminate —
  the drums modulate in the same band — so it is not reported as a vocal detector here.
