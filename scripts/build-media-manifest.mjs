#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { ensureDir, readJsonIfExists, stripLeadingDotSlash, toPosixPath } from "./lib/pipeline-utils.mjs";
import { readVolhollaAlbums } from "./lib/volholla-albums.mjs";

const ROOT = process.cwd();
const IMAGE_MANIFEST_FILE = path.join(ROOT, "MEDIA_DERIVATIVES", "images", "manifest.json");
const AUDIO_MANIFEST_FILE = path.join(ROOT, "MEDIA_DERIVATIVES", "audio", "manifest.json");
const OUT_FILE = path.join(ROOT, "VOLHOLLA", "media-manifest.json");

function imageEntryFor(items, relativePath) {
  if (!relativePath) return null;
  const found = items?.[relativePath];
  if (found) return found;
  return {
    source: relativePath,
    derivatives: {}
  };
}

function audioEntryFor(items, relativePath) {
  if (!relativePath) return null;
  const found = items?.[relativePath];
  if (found) return found;
  return {
    source: relativePath,
    derivatives: {}
  };
}

async function main() {
  const imageManifest = await readJsonIfExists(IMAGE_MANIFEST_FILE);
  const audioManifest = await readJsonIfExists(AUDIO_MANIFEST_FILE);
  const albums = await readVolhollaAlbums(ROOT);

  const out = {
    generatedAt: new Date().toISOString(),
    imagesManifest: stripLeadingDotSlash(toPosixPath(path.relative(ROOT, IMAGE_MANIFEST_FILE))),
    audioManifest: stripLeadingDotSlash(toPosixPath(path.relative(ROOT, AUDIO_MANIFEST_FILE))),
    albums: {}
  };

  for (const album of albums) {
    out.albums[album.key] = {
      key: album.key,
      label: album.label,
      subtitle: album.subtitle,
      pageSlug: album.pageSlug,
      hallKey: album.hallKey,
      op2Key: album.op2Key,
      op2Pair: album.op2Pair,
      accentA: album.accentA,
      accentB: album.accentB,
      cover: imageEntryFor(imageManifest?.items, album.coverSource),
      defaultTrackArt: imageEntryFor(imageManifest?.items, album.defaultTrackArtSource),
      tracks: album.tracks.map((track) => ({
        index: track.index,
        title: track.title,
        file: track.file,
        source: track.source,
        songPage: track.songPage,
        audio: audioEntryFor(audioManifest?.items, track.source)
      }))
    };
  }

  await ensureDir(path.dirname(OUT_FILE));
  await fs.writeFile(OUT_FILE, JSON.stringify(out, null, 2));
  process.stdout.write(`Built media manifest for ${albums.length} albums.\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

