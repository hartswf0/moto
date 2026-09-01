# CONFORM — TWO TRAILERS, ONE PER SONG

Both trailers are cut from the same 16-patch inventory in `CUTBASTARD-EXTRACTION.md`.
They share no act structure, no grade, and no footage emphasis.

## Music analysis (measured, not assumed)

Spectral-flux onset envelope → autocorrelation tempo → phase and downbeat search.

| | Trailer A | Trailer B |
|---|---|---|
| Song | The PhD of Musk (track 34) | Ancient Law, New Fine Print (track 02) |
| Source | `THE CHAPEL RING/The Chapel Ring - The PhD of Musk - Treblo.ogg` | `THE CHAPEL RING/The Chapel Ring - Ancient Law, New Fine Print - Treblo.ogg` |
| Full length | 251.29s | 165.14s |
| Tempo | **103.10 BPM** | **127.90 BPM** |
| Beat | 0.58197s | 0.46912s |
| Bar (4/4) | 2.32787s | 1.87646s |
| Downbeat phase | 0.817s | 1.462s |
| Energy shape | flat plateau from 10s; no breakdown | build 0–10, body 10–50, **breakdown 50–58**, return 60, second breakdown 120–125, decay from 135 |
| Trailer window | 0.000 → 70.650s | 0.000 → 78.397s |

The songs dictated the two structures. s34 has no dynamic hole to put a title in, so Trailer A
*manufactures* one with a hard cut to black at 56.7s. s02 hands you an eight-second breakdown at
50–58s, so Trailer B's title card sits inside it and needs no trick.

## Trailer A — "The PhD of Musk"
`trailer-chapelring-34-phd-of-musk.mp4` · 1:10.46 · 73 events · grade: honey/amber

Cut on the 103.10 BPM grid. Every act boundary lands on a downbeat.

| Act | Program TC | Beats | Function |
|---|---|---|---|
| 0 — Cold open | 00:00:00:00 → 00:00:10:03 | 17.4 | Four held patches at 0.36×–0.86× speed. Ranger face, honey pour, POV aisle, the portrait archive. |
| 1 — The scholar | 00:00:10:03 → 00:00:24:02 | 24 | 2–3 beat cuts. The lecture hall states itself, the index answers. |
| 2 — Escalation | 00:00:24:02 → 00:00:40:09 | 28 | 1–1.5 beat cuts with two 4-beat honey/archive holds as breath. |
| 3 — The burst | 00:00:40:09 → 00:00:56:16 | 28 | Down to 0.5 beat (0.291s / 7 frames). All punch-in reframes of spent patches, one reversal. |
| 4 — Title & payoff | 00:00:56:16 → 00:01:10:11 | 24 | Smash to black, album card, three payoff shots, title lockup, honey tail, URL. |

Grade A: contrast 1.16, saturation 1.14, warm balance (r+0.06 / b−0.09), blue curve pulled to 0.46
at midpoint, light temporal grain. 2.39:1 scope in a 1920×1080 frame.

## Trailer B — "Ancient Law, New Fine Print"
`trailer-chapelring-02-ancient-law.mp4` · 1:18.40 · 84 events · grade: cold steel

Cut on the 127.90 BPM grid, structured around the song's own breakdown.

| Act | Program TC | Beats | Function |
|---|---|---|---|
| 0 — Machine open | 00:00:00:00 → 00:00:12:17 | 3.1 + 24 | POV aisle at 0.5×, Puddle-Soot named by its own burned-in caption, stage wide, gallery reveal. |
| 1 — The instrument | 00:00:12:17 → 00:00:27:17 | 32 | 2–4 beat cuts. Machine room and control suite trade off; the archive appears once as the authority cutaway. |
| 2 — Fine print | 00:00:27:17 → 00:00:42:17 | 32 | 1.5–2 beat cuts, one reversal, two 4-beat holds. |
| 3 — Pre-breakdown burst | 00:00:42:17 → 00:00:50:06 | 16 | 0.5 beat (0.235s / 5–6 frames) for sixteen cuts, then eight 1-beat cuts. |
| 4 — **Breakdown / title** | 00:00:50:06 → 00:00:57:18 | 16 | Music drops out. Puddle-Soot held at 0.4× speed, black, then the title lockup in the silence. |
| 5 — Return | 00:00:57:18 → 00:01:18:09 | 44 | Music re-enters at 60s. Full institution cycle, honey tail, final POV push, URL. |

Grade B: contrast 1.28, saturation 0.66, cold balance (b+0.14 / r−0.07), crushed blacks via the red
curve, slightly heavier grain. Same 2.39:1 scope.

## Footage split

Deliberately divergent so the two cuts do not read as versions of each other.

- **A leans warm**: V1 (lecture hall, 6 patches) and V3 (sepia gallery) carry the spine; V2c the lecture wide.
- **B leans cold**: V5 (POV aisle) opens four of six acts; V4 (Puddle-Soot) and V6 (control suite) carry the body; V1 appears only twice, as the honey tail and the archive cutaway.

## Reproduce

Requires ffmpeg with libx264, `curves`, `colorbalance`, `noise`, `unsharp`. No `drawtext` needed —
cards are rendered to PNG by Pillow.

```sh
python3 conform/cards.py      # title cards -> PNG
python3 conform/edl_A.py      # segments -> concat -> grade -> mux
python3 conform/edl_B.py
python3 conform/finalize.py A # re-encode from cached picture.mp4 only
python3 conform/finalize.py B
```

`conform/cutbastard.py` holds the patch table (`PATCH`), the reframe/retime engine and the two
grades. `edl_A.py` / `edl_B.py` are the edit decision lists, expressed in **beats**, so changing a
song's BPM constant re-times the whole cut.

## Notes on the source

- Source audio is discarded. Six independently generated stems have no shared acoustic space and
  turn to noise when cross-cut at 0.3s. Both trailers are scored to the song alone.
- V4 ships with a burned-in lower third (`"Puddle-Soot" / Pooh's depraved cousin`). Trailer B
  features it deliberately at 00:00:07 and again in the breakdown; Trailer A crops past it.
- 48s of unique material supports a 70s and a 78s cut through retiming (0.35×–1.0×), punch-in
  reframing (up to 2.4× crop), and two reversals. No patch is used at the same scale twice inside
  the same act.
