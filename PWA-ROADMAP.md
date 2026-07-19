# MOTO PWA Roadmap (Deferred)

## Decision

MOTO can become an installable progressive web app without changing its static-site distribution model. This should be a later, repository-wide project. The current WC 2026 transcript and set review remains the immediate priority.

The PWA should describe one <MOTO application shell> with many <album>, <track>, and <mix> routes. It should not create a separate service worker or manifest for every album.

## Purpose

The PWA should make the listening interface faster to reopen, resilient on weak networks, and optionally usable offline for a deliberately downloaded set. Installation is useful, but the core product remains a URL-first music archive.

## Required Baseline

- Serve production from HTTPS. GitHub Pages already provides the right origin conditions.
- Add one `manifest.webmanifest` at the MOTO site root with `name`, `short_name`, `start_url`, `scope`, `display`, theme/background colors, and 192 px plus 512 px icons.
- Register one root-scoped service worker with explicit install, activate, and fetch behavior.
- Add iOS home-screen metadata and icons as progressive enhancement.
- Preserve ordinary browser navigation when installation or service workers are unavailable.

## Cache Theory

<application-shell assets> and <audio media> have different lifecycles and must not share one cache policy.

- [precache] the small root shell: index, shared CSS/JS, manifest, icons, and essential navigation data.
- [stale-while-revalidate] album HTML, ticket previews, and generated metadata.
- [network-first] mutable indexes and manifests where an old catalog would be misleading.
- [stream] full audio from the network by default. Do not pre-cache the entire archive.
- [download-for-offline] only a user-selected album or finite themed set, after showing its size.
- [evict] old versioned assets and least-recently-used offline media under a documented storage budget.

Audio range requests, browser storage quotas, and interrupted downloads need dedicated tests. A service worker that caches partial responses incorrectly can make seeking or playback less reliable than the current site.

## State And Playback

- Keep current lightweight preferences in `localStorage` while their schema remains small.
- Use IndexedDB for offline-download records, cached media metadata, transcript corrections, and larger future queues.
- Continue using the existing Media Session integration for lock-screen metadata and transport controls.
- Treat background playback as browser/OS-dependent. PWA installation does not guarantee uninterrupted iOS background audio.
- Version stored state and provide migration or reset behavior when playlist/set schemas change.

## Update Contract

<installed-client> [checks] <versioned application manifest>.

<new service worker> [installs] <new shell cache> without deleting the active version.

<user reload or safe activation point> [activates] <new version>.

<activation> [removes] <obsolete shell caches> but preserves explicitly downloaded media until its own retention policy removes it.

The interface should show a compact update action when a new worker is waiting. It should never replace code during active playback.

## Delivery Phases

1. Add installability only: manifest, icon set, service worker registration, and shell cache.
2. Verify navigation and update behavior across the root index, representative albums, VOLHOLLA, and WC 2026.
3. Add offline metadata and ticket previews.
4. Add opt-in “download set” with size calculation, progress, cancellation, and storage management.
5. Run Lighthouse plus real-device install, airplane-mode, seek, update, and background-playback tests.

## Acceptance Conditions

- Every existing URL still works without service-worker support.
- A fresh install opens the same current MOTO interface, not a parallel landing page.
- The shell opens offline after one successful visit.
- A deliberately downloaded set plays and seeks offline from first through last track.
- App updates do not interrupt active audio or destroy saved playlist order.
- Clearing an offline set removes its audio while leaving ordinary browser state intact.

## Open Human Decisions

- Which route is the installed `start_url`: the MOTO index, VOLHOLLA, or the last active listening desk?
- What is the visual app icon independent of any single album ticket?
- What storage ceiling is acceptable for offline audio?
- Should transcript corrections stay local, export as JSON, or later sync to a server?
- Is offline access meant for private performance preparation only, or for public listeners too?

