import fs from "node:fs/promises";
import path from "node:path";

const ROOT = process.cwd();
const SONG_PAGE_JS = path.join(ROOT, "VOLHOLLA", "song-page.js");
const OUT_DIR = path.join(ROOT, "VOLHOLLA");
const SITE_BASE = "https://hartswf0.github.io/moto/VOLHOLLA/";

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (m) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;"
  }[m]));
}

function titleFromFilename(file) {
  return String(file || "")
    .replace(/^.*\//, "")
    .replace(/\.(?:mp3|ogg)$/i, "")
    .replace(/^\d+_/, "")
    .replace(/^coolradio\s*-\s*/i, "")
    .replace(/^geometric ghosts of mitte\s*-\s*/i, "")
    .replace(/^river bank waiting\s*-\s*/i, "")
    .replace(/^solar reveries\s*-\s*/i, "")
    .replace(/^jukebox time collapse\s*-\s*/i, "")
    .replace(/^the cybernetic winter\s*-\s*/i, "")
    .replace(/^clinical heat\s*-\s*/i, "")
    .replace(/^the d\.c\.\s*pocket\s*&\s*afro-funk\s*-\s*/i, "")
    .replace(/^(?:canyon fog and silver strings|chiptune crossroads|crown on|piassa state of mind|remix of the burn of being|the sad god)\s*-\s*/i, "")
    .replace(/\s*-\s*Sonauto\s*\((\d+)\)$/i, " ($1)")
    .replace(/\s*-\s*Sonauto$/i, "")
    .replace(/_/g, " ")
    .trim();
}

function extractAlbums(source) {
  const blockRegex = /^ {4}([a-z0-9_]+): \{\n([\s\S]*?)(?=^ {4}[a-z0-9_]+: \{|^  \};)/gm;
  const albums = [];
  for (const match of source.matchAll(blockRegex)) {
    const [, key, block] = match;
    const pageSlug = block.match(/pageSlug:\s*"([^"]+)"/)?.[1];
    const label = block.match(/label:\s*"([^"]+)"/)?.[1];
    const subtitle = block.match(/subtitle:\s*"([^"]+)"/)?.[1] || `${label} song page`;
    const coverImage =
      block.match(/coverImage:\s*"([^"]+)"/)?.[1] ||
      block.match(/defaultTrackArt:\s*"([^"]+)"/)?.[1] ||
      "";
    const filesBlock = block.match(/files:\s*\[([\s\S]*?)\n\s*\]/)?.[1] || "";
    const files = Array.from(filesBlock.matchAll(/"([^"]+)"/g), (fileMatch) => fileMatch[1]);
    if (!pageSlug || !label || files.length === 0) continue;
    albums.push({ key, pageSlug, label, subtitle, coverImage, files });
  }
  return albums;
}

function songPageHtml(album, trackIndex) {
  const file = album.files[trackIndex];
  const trackTitle = titleFromFilename(file);
  const pageFile = `song-${album.key}-${String(trackIndex + 1).padStart(2, "0")}.html`;
  const pageUrl = new URL(pageFile, SITE_BASE).toString();
  const imageUrl = album.coverImage ? new URL(encodeURI(album.coverImage), SITE_BASE).toString() : "";
  const desc = `${album.label} · Track ${String(trackIndex + 1).padStart(2, "0")} of ${album.files.length}`;
  const title = `${trackTitle} · ${album.label}`;
  const iconHref = encodeURI(album.coverImage || "");
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
  <main class="song-wrap" id="songPageRoot" data-album="${escapeHtml(album.key)}" data-track="${trackIndex + 1}"></main>
  <script src="./song-page.js"></script>
</body>
</html>
`;
}

async function main() {
  const source = await fs.readFile(SONG_PAGE_JS, "utf8");
  const albums = extractAlbums(source);
  let written = 0;
  for (const album of albums) {
    for (let i = 0; i < album.files.length; i += 1) {
      const filename = path.join(OUT_DIR, `song-${album.key}-${String(i + 1).padStart(2, "0")}.html`);
      await fs.writeFile(filename, songPageHtml(album, i), "utf8");
      written += 1;
    }
  }
  process.stdout.write(`Generated ${written} song share pages for ${albums.length} albums.\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
