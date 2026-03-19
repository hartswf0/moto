import fs from "node:fs/promises";
import path from "node:path";
import { extractAlbumsFromSource, titleFromFilename } from "./lib/volholla-albums.mjs";
import { readJsonIfExists } from "./lib/pipeline-utils.mjs";

const ROOT = process.cwd();
const SONG_PAGE_JS = path.join(ROOT, "VOLHOLLA", "song-page.js");
const OUT_DIR = path.join(ROOT, "VOLHOLLA");
const MEDIA_MANIFEST_FILE = path.join(ROOT, "VOLHOLLA", "media-manifest.json");
const SITE_BASE = "https://hartswf0.github.io/moto/VOLHOLLA/";
const SITE_ROOT = "https://hartswf0.github.io/moto/";

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (m) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;"
  }[m]));
}

function normalizeAssetPath(value) {
  return String(value || "").normalize("NFC");
}

function pageAssetPath(rootRelativePath) {
  const raw = normalizeAssetPath(rootRelativePath).replace(/^\.\/+/, "");
  if (!raw) return "";
  return raw.startsWith("VOLHOLLA/") ? `./${raw.slice("VOLHOLLA/".length)}` : `../${raw}`;
}

function siteAssetUrl(rootRelativePath) {
  const raw = normalizeAssetPath(rootRelativePath).replace(/^\.\/+/, "");
  if (!raw) return "";
  return new URL(encodeURI(raw), SITE_ROOT).toString();
}

function pickImagePath(entry, preferredKind) {
  return entry?.derivatives?.[preferredKind]?.jpeg
    || entry?.derivatives?.[preferredKind]?.webp
    || entry?.derivatives?.cover?.jpeg
    || entry?.derivatives?.cover?.webp
    || entry?.derivatives?.share?.jpeg
    || entry?.derivatives?.share?.webp
    || entry?.derivatives?.thumb?.jpeg
    || entry?.derivatives?.thumb?.webp
    || entry?.source
    || "";
}

function mediaTypeFor(filePath) {
  const lower = String(filePath || "").toLowerCase();
  if (lower.endsWith(".mp3")) return "audio/mpeg";
  if (lower.endsWith(".ogg")) return "audio/ogg";
  if (lower.endsWith(".wav")) return "audio/wav";
  if (lower.endsWith(".m4a")) return "audio/mp4";
  if (lower.endsWith(".aac")) return "audio/aac";
  return "";
}

function pickAudioSources(entry, fallbackRootRelative) {
  const sources = [];
  const primary = entry?.derivatives?.stream?.mp3 || entry?.derivatives?.fallback?.mp3 || entry?.source || fallbackRootRelative || "";
  const backup = entry?.source || fallbackRootRelative || "";

  if (primary) sources.push({ path: primary, type: mediaTypeFor(primary) });
  if (backup && backup !== primary) sources.push({ path: backup, type: mediaTypeFor(backup) });
  return sources;
}

function renderAudioSources(sources) {
  return sources.map((source) => {
    const href = encodeURI(pageAssetPath(source.path));
    return `<source src="${escapeHtml(href)}"${source.type ? ` type="${escapeHtml(source.type)}"` : ""}>`;
  }).join("\n              ");
}

function songPageHtml(album, trackIndex, manifestAlbum) {
  const file = album.files[trackIndex];
  const trackTitle = titleFromFilename(file);
  const pageFile = `song-${album.key}-${String(trackIndex + 1).padStart(2, "0")}.html`;
  const pageUrl = new URL(pageFile, SITE_BASE).toString();
  const desc = `${album.label} · Track ${String(trackIndex + 1).padStart(2, "0")} of ${album.files.length}`;
  const title = `${trackTitle} · ${album.label}`;
  const coverRootRelative = pickImagePath(manifestAlbum?.cover, "cover");
  const shareRootRelative = pickImagePath(manifestAlbum?.cover, "share") || coverRootRelative;
  const trackArtRootRelative = pickImagePath(manifestAlbum?.defaultTrackArt, "cover") || coverRootRelative;
  const imageUrl = siteAssetUrl(shareRootRelative);
  const iconHref = encodeURI(pageAssetPath(coverRootRelative) || album.coverImage || "");
  const artHref = encodeURI(pageAssetPath(trackArtRootRelative) || album.coverImage || "");
  const audioSources = pickAudioSources(
    manifestAlbum?.tracks?.[trackIndex]?.audio,
    manifestAlbum?.tracks?.[trackIndex]?.source || album.tracks?.[trackIndex]?.source || ""
  );
  const albumHref = `./${album.pageSlug}.html`;
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="${escapeHtml(desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="VOLHOLLA" />
  <meta property="og:title" content="${escapeHtml(title)}" />
  <meta property="og:description" content="${escapeHtml(desc)}" />
  <meta property="og:url" content="${escapeHtml(pageUrl)}" />
  <meta property="og:image" content="${escapeHtml(imageUrl)}" />
  <meta property="og:image:alt" content="${escapeHtml(album.label)} artwork" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="${escapeHtml(title)}" />
  <meta name="twitter:description" content="${escapeHtml(desc)}" />
  <meta name="twitter:image" content="${escapeHtml(imageUrl)}" />
  <meta name="theme-color" content="#111114" />
  <title>${escapeHtml(title)}</title>
  <link rel="canonical" href="${escapeHtml(pageUrl)}" />
  <link rel="icon" type="image/png" href="${escapeHtml(iconHref)}" />
  <link rel="stylesheet" href="./song-page.css" />
</head>
<body>
  <main class="song-wrap" id="songPageRoot" data-album="${escapeHtml(album.key)}" data-track="${trackIndex + 1}">
    <div class="shell">
      <header class="top">
        <div class="top-card">
          <div class="te-strip">
            <div class="te-left">
              <span class="led" aria-hidden="true"></span>
              <span class="mono">Listen</span>
            </div>
            <span class="te-tag">Track ${String(trackIndex + 1).padStart(2, "0")} / ${album.files.length}</span>
          </div>
          <div class="head">
            <div class="head-main">
              <div class="eyebrow">${escapeHtml(album.label)}</div>
              <h1 class="song-title">${escapeHtml(trackTitle)}</h1>
              <div class="album-sub">${escapeHtml(album.subtitle)}</div>
            </div>
          </div>
        </div>
      </header>

      <div class="grid">
        <section class="panel art-panel">
          <div class="cover-frame">
            <div class="cover-head">
              <span class="mono">Song Unit</span>
              <span class="mono">${escapeHtml(album.key)} / ${String(trackIndex + 1).padStart(2, "0")}</span>
            </div>
            <div class="art-square">
              ${artHref ? `<img src="${escapeHtml(artHref)}" alt="${escapeHtml(trackTitle)} artwork">` : ""}
            </div>
            <div class="cover-foot">
              <div class="main">${escapeHtml(trackTitle)}</div>
              <div class="meta">track</div>
            </div>
          </div>
        </section>

        <section class="panel player-panel">
          <div class="now-card">
            <div class="now-head">
              <div>
                <div class="now-kicker">Ready</div>
                <div class="now-line">${escapeHtml(trackTitle)}</div>
                <div class="now-subline">If the enhanced player is slow, the native control below will still play.</div>
              </div>
            </div>
          </div>
          <div class="embed-code">
            <audio controls preload="none" playsinline style="width:100%">
              ${renderAudioSources(audioSources)}
            </audio>
          </div>
          <div class="actions">
            <a class="btn" href="${escapeHtml(albumHref)}">Open Album</a>
            <a class="btn" href="${escapeHtml(pageUrl)}">Copy Link</a>
          </div>
        </section>
      </div>
    </div>
  </main>
  <script src="./song-page.js"></script>
</body>
</html>
`;
}

async function main() {
  const source = await fs.readFile(SONG_PAGE_JS, "utf8");
  const albums = extractAlbumsFromSource(source, ROOT);
  const mediaManifest = await readJsonIfExists(MEDIA_MANIFEST_FILE);
  let written = 0;
  for (const album of albums) {
    for (let i = 0; i < album.files.length; i += 1) {
      const filename = path.join(OUT_DIR, `song-${album.key}-${String(i + 1).padStart(2, "0")}.html`);
      await fs.writeFile(filename, songPageHtml(album, i, mediaManifest?.albums?.[album.key] || null), "utf8");
      written += 1;
    }
  }
  process.stdout.write(`Generated ${written} song share pages for ${albums.length} albums.\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
