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
- `mitte`
- `moto`
- `river`
- `crossroads`
- `solar`
- `jukebox`
- `cyber`
- `goleyakh`
- `noservice`
- `clinical`
- `usblegacy`
- `ferrous`
- `concreto`
- `cypher`
- `congregation`
- `maquina`
- `blackwater`
- `heishui`
- `doppler`
- `aeolian`
- `chapelring`
- `republicdrink`
- `sanctuaryshake`
- `globalstadium`
- `cavalrymarsh`
- `midnightsteppe`
- `brooklynomen`
- `paperglasses`
- `inthemiddle`
- `mareamemory`

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
- Song page: `VOLHOLLA/song-elephant-01.html`
- Song embed: `VOLHOLLA/song-elephant-01.html?embed=1`

## GitHub Pages

Enable Pages in the repository settings and publish from:

- Branch: `main`
- Folder: `/ (root)`

The repo includes local audio files used directly by the pages. Most albums are `.mp3`; `river`, `crossroads`, `solar`, `jukebox`, `cyber`, `goleyakh`, `noservice`, `concreto`, `cypher`, `usblegacy`, `ferrous`, `congregation`, `maquina`, `blackwater`, `heishui`, `doppler`, `aeolian`, `chapelring`, `republicdrink`, `sanctuaryshake`, `globalstadium`, `cavalrymarsh`, `midnightsteppe`, `brooklynomen`, `paperglasses`, `inthemiddle`, and `mareamemory` currently use `.ogg`.

## Media Derivatives

The repo now includes a simple local compression pipeline for backup delivery assets and future CDN migration.

- Images: `node scripts/build-image-derivatives.mjs`
- Audio: `node scripts/build-audio-derivatives.mjs`
- Priority entry-point pass: `node scripts/build-priority-derivatives.mjs`
- Combined album/media manifest: `node scripts/build-media-manifest.mjs`

Useful flags:

- `--match river` to limit work to matching files
- `--limit 10` to cap the current run
- `--dry-run` to plan outputs without writing files
- `--force` to rebuild existing derivatives
- `--out MEDIA_DERIVATIVES/images` or `--out MEDIA_DERIVATIVES/audio` to change output roots

Generated outputs are mirrored under `MEDIA_DERIVATIVES/` and originals stay untouched.
