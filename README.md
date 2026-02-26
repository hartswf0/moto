# MOTO

Static audio playground + shield jukebox for GitHub Pages.

## Main pages

- `index.html` (hub)
- `VOLHOLLA/index.html` (multi-album shield hall)
- `op2.html` (OP-style dual-deck crate)
- `mandalla.html` (single radial mixer / sequencer)
- `mandalla-deck.html` (dual Mandalla harness / pair deck)
- `s01.html`, `s02.html` (experiments)

## Mandalla System (documented routes)

### Album keys

- `volholla`
- `elephant`
- `loom`
- `moto`

### Single Mandalla

- Base: `mandalla.html`
- Album load: `mandalla.html?album=elephant`
- Embed mode (iframe-friendly): `mandalla.html?embed=1&album=loom`

### Mandalla Deck (pair harness)

- Base: `mandalla-deck.html`
- Shareable pair URL: `mandalla-deck.html?a=elephant&b=loom`

The deck embeds two `mandalla.html?embed=1` instances and uses a same-origin audio bridge for playback.

### VOLHOLLA share routes

- Album page: `VOLHOLLA/stochastic-elephant.html`
- Song page: `VOLHOLLA/song.html?album=elephant&track=1`
- Song embed: `VOLHOLLA/song.html?album=elephant&track=1&embed=1`

## GitHub Pages

Enable Pages in the repository settings and publish from:

- Branch: `main`
- Folder: `/ (root)`

The repo includes local MP3 files used directly by the pages.
