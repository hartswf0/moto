import fs from "node:fs/promises";
import path from "node:path";
import { stripLeadingDotSlash, toPosixPath } from "./pipeline-utils.mjs";

export function titleFromFilename(file) {
  return String(file || "")
    .replace(/^.*\//, "")
    .replace(/\.(?:mp3|ogg|wav|m4a|aac)$/i, "")
    .replace(/^\d+_/, "")
    .replace(/^coolradio\s*-\s*/i, "")
    .replace(/^geometric ghosts of mitte\s*-\s*/i, "")
    .replace(/^river bank waiting\s*-\s*/i, "")
    .replace(/^solar reveries\s*-\s*/i, "")
    .replace(/^jukebox time collapse\s*-\s*/i, "")
    .replace(/^ghost in the wires\s*-\s*/i, "")
    .replace(/^neon puddles\s*\(night bus edit\)\s*-\s*/i, "")
    .replace(/^neon puddles\s*-\s*/i, "")
    .replace(/^mall patchworld ingest\s*-\s*/i, "")
    .replace(/^the cybernetic winter\s*-\s*/i, "")
    .replace(/^the cathedral of iv drips\s*-\s*/i, "")
    .replace(/^throne of ash\s*-\s*/i, "")
    .replace(/^cathedral of glass\s*-\s*/i, "")
    .replace(/^event horizon discovery\s*-\s*/i, "")
    .replace(/^silence in the 757\s*-\s*/i, "")
    .replace(/^gole yakh memory\s*-\s*/i, "")
    .replace(/^clinical heat\s*-\s*/i, "")
    .replace(/^concreto y cyphers\s*-\s*/i, "")
    .replace(/^usb legacy\s*-\s*/i, "")
    .replace(/^ferrous lament\s*-\s*/i, "")
    .replace(/^the great congregation\s*-\s*/i, "")
    .replace(/^(?:m\u00e1quina|ma\u0301quina) de guerra\s*-\s*/i, "")
    .replace(/^black water run\s*-\s*/i, "")
    .replace(/^executable infrastructure dub\s*-\s*/i, "")
    .replace(/^queen of light\s*-\s*/i, "")
    .replace(/^root and residue\s*-\s*/i, "")
    .replace(/^better hands\s*-\s*/i, "")
    .replace(/^no bright stand\s*-\s*/i, "")
    .replace(/^museum floor thinking\s*-\s*/i, "")
    .replace(/^truth to the rhythm\s*-\s*/i, "")
    .replace(/^unpatched glitch\s*-\s*/i, "")
    .replace(/^the abyssal crown\s*-\s*/i, "")
    .replace(/^sun-faded ghosts?\s*-\s*/i, "")
    .replace(/^doppler phantom\s*-\s*/i, "")
    .replace(/^aeolian drift\s*-\s*/i, "")
    .replace(/^the chapel ring\s*-\s*/i, "")
    .replace(/^the republic spilled its drink\s*-\s*/i, "")
    .replace(/^sanctuary shake\s*-\s*/i, "")
    .replace(/^global stadium sunshine\s*-\s*/i, "")
    .replace(/^cavalry of the marsh\s*-\s*/i, "")
    .replace(/^midnight over the steppe\s*-\s*/i, "")
    .replace(/^brooklyn omen\s*-\s*/i, "")
    .replace(/^paper glasses,\s*electric wonder\s*-\s*/i, "")
    .replace(/^in the middle\s*-\s*/i, "")
    .replace(/^marea memory\s*-\s*/i, "")
    .replace(/^polliwog station\s*-\s*/i, "")
    .replace(/^last week of august\s*-\s*/i, "")
    .replace(/^southern noise catharsis\s*-\s*/i, "")
    .replace(/^\d{1,2}[_\s-]+/, "")
    .replace(/^the d\.c\.\s*pocket\s*&\s*afro-funk\s*-\s*/i, "")
    .replace(/^(?:canyon fog and silver strings|chiptune crossroads|crown on|piassa state of mind|remix of the burn of being|the sad god)\s*-\s*/i, "")
    .replace(/\s*-\s*Sonauto\s*\((\d+)\)$/i, " ($1)")
    .replace(/\s*-\s*Sonauto$/i, "")
    .replace(/\s*-\s*Treblo\s*\((\d+)\)$/i, " ($1)")
    .replace(/\s*-\s*Treblo$/i, "")
    .replace(/_/g, " ")
    .trim()
    .normalize("NFC");
}

function blockValue(block, key) {
  return block.match(new RegExp(`${key}:\\s*"([^"]+)"`))?.[1] || "";
}

function blockObjectByIndex(block, key) {
  const objectBlock = block.match(new RegExp(`${key}:\\s*\\{([\\s\\S]*?)\\n\\s*\\},`))?.[1] || "";
  const values = {};
  for (const match of objectBlock.matchAll(/(\d+):\s*"([^"]+)"/g)) {
    values[Number(match[1])] = match[2];
  }
  return values;
}

function resolveFromVolholla(rootDir, assetPath) {
  if (!assetPath) return "";
  const absolute = path.resolve(rootDir, "VOLHOLLA", assetPath);
  return stripLeadingDotSlash(toPosixPath(path.relative(rootDir, absolute))).normalize("NFC");
}

export function extractAlbumsFromSource(source, rootDir = process.cwd()) {
  const lines = source.split("\n");
  const albums = [];
  let inAlbums = false;
  let currentKey = "";
  let currentLines = [];
  let depth = 0;

  for (const line of lines) {
    if (!inAlbums) {
      if (line.includes("const ALBUMS = {")) inAlbums = true;
      continue;
    }

    if (!currentKey) {
      if (/^  };$/.test(line)) break;
      const start = line.match(/^    ([a-z0-9_]+): \{$/);
      if (!start) continue;
      currentKey = start[1];
      currentLines = [line];
      depth = 1;
      continue;
    }

    currentLines.push(line);
    depth += (line.match(/\{/g) || []).length;
    depth -= (line.match(/\}/g) || []).length;

    if (depth === 0) {
      const block = currentLines.join("\n");
      const key = currentKey;
      currentKey = "";
      currentLines = [];

      const pageSlug = blockValue(block, "pageSlug");
      const label = blockValue(block, "label");
      const subtitle = blockValue(block, "subtitle") || `${label} song page`;
      const basePath = blockValue(block, "basePath");
      const coverImage = blockValue(block, "coverImage");
      const defaultTrackArt = blockValue(block, "defaultTrackArt") || coverImage;
      const trackArtByIndex = blockObjectByIndex(block, "trackArtByIndex");
      const hallKey = blockValue(block, "hallKey");
      const op2Key = blockValue(block, "op2Key");
      const op2Pair = blockValue(block, "op2Pair");
      const accentA = blockValue(block, "accentA");
      const accentB = blockValue(block, "accentB");
      const filesBlock = block.match(/files:\s*\[([\s\S]*?)\n\s*\]/)?.[1] || "";
      const files = Array.from(filesBlock.matchAll(/"([^"]+)"/g), (match) => match[1]);
      if (!pageSlug || !label || !files.length) continue;

      albums.push({
        key,
        pageSlug,
        label,
        subtitle,
        basePath,
        coverImage,
        defaultTrackArt,
        coverSource: resolveFromVolholla(rootDir, coverImage),
        defaultTrackArtSource: resolveFromVolholla(rootDir, defaultTrackArt),
        hallKey,
        op2Key,
        op2Pair,
        accentA,
        accentB,
        files,
        tracks: files.map((file, index) => ({
          index: index + 1,
          file,
          title: titleFromFilename(file),
          source: resolveFromVolholla(rootDir, `${basePath}${file}`),
          artSource: resolveFromVolholla(rootDir, trackArtByIndex[index] || ""),
          songPage: `VOLHOLLA/song-${key}-${String(index + 1).padStart(2, "0")}.html`
        }))
      });
    }
  }

  return albums;
}

export async function readVolhollaAlbums(rootDir = process.cwd()) {
  const source = await fs.readFile(path.join(rootDir, "VOLHOLLA", "song-page.js"), "utf8");
  return extractAlbumsFromSource(source, rootDir);
}
