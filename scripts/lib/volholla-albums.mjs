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
    .replace(/^the cybernetic winter\s*-\s*/i, "")
    .replace(/^clinical heat\s*-\s*/i, "")
    .replace(/^concreto y cyphers\s*-\s*/i, "")
    .replace(/^the d\.c\.\s*pocket\s*&\s*afro-funk\s*-\s*/i, "")
    .replace(/^(?:canyon fog and silver strings|chiptune crossroads|crown on|piassa state of mind|remix of the burn of being|the sad god)\s*-\s*/i, "")
    .replace(/\s*-\s*Sonauto\s*\((\d+)\)$/i, " ($1)")
    .replace(/\s*-\s*Sonauto$/i, "")
    .replace(/_/g, " ")
    .trim()
    .normalize("NFC");
}

function blockValue(block, key) {
  return block.match(new RegExp(`${key}:\\s*"([^"]+)"`))?.[1] || "";
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
