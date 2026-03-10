# MOTO

Static audio playground + shield jukebox for GitHub Pages.

## Main pages

- `index.html` (hub)
- `VOLHOLLA/index.html` (multi-album shield hall)
- `op2.html` (OP-style dual-deck crate)
- `mandalla.html` (single radial mixer / sequencer)
- `mandalla-deck.html` (dual Mandalla harness / pair deck)
- `mandalla-ns.html` (single-deck subtractive shell)
- `mandalla-deck-ns.html` (dual-deck subtractive shell)
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

### Mandalla NS (subtractive versions)

- Single NS shell: `mandalla-ns.html?album=elephant`
- Dual NS shell: `mandalla-deck-ns.html?a=elephant&b=loom`

The NS pages keep only core controls (album, play/pause, BPM) and remove setup panels/extra chrome.

### VOLHOLLA share routes

- Album page: `VOLHOLLA/stochastic-elephant.html`
- Song page: `VOLHOLLA/song.html?album=elephant&track=1`
- Song embed: `VOLHOLLA/song.html?album=elephant&track=1&embed=1`

## GitHub Pages

Enable Pages in the repository settings and publish from:

- Branch: `main`
- Folder: `/ (root)`

The repo includes local MP3 files used directly by the pages.
