#!/usr/bin/env node

import crypto from "node:crypto";
import { execFile } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { promisify } from "node:util";

const ROOT = process.cwd();
const MIX_DIR = path.join(ROOT, "WC-2026-FINAL-MIX");
const SOURCE_MANIFEST = path.join(ROOT, "VOLHOLLA", "media-manifest.json");
const OUTPUT = path.join(MIX_DIR, "mix-manifest.js");
const PREVIEW_DIR = path.join(MIX_DIR, "previews");
const execFileAsync = promisify(execFile);

const ROUTE_OVERRIDES = {
  "all-time-ticket.png": "VOLHOLLA/song-heishui-10.html",
  "all-time-ticket (1).png": "VOLHOLLA/song-maquina-33.html",
  "fingerprints-in-the-silicon-ticket.png": "VOLHOLLA/song-betterhands-04.html",
  "sharper-hands-ticket.png": "VOLHOLLA/song-sharperhands-01.html",
  "visible-repair-ticket.png": "VOLHOLLA/song-betterhands-10.html"
};

function normalizeTitle(value) {
  return String(value || "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function titleFromTicket(file) {
  return file
    .replace(/\.(?:png|jpe?g|webp)$/i, "")
    .replace(/-ticket(?: \(\d+\))?$/i, "")
    .replace(/-/g, " ")
    .trim();
}

function relativeFromMix(source) {
  return `../${String(source || "").replace(/^\.\//, "")}`;
}

function sideFor(index, total) {
  const base = Math.floor(total / 4);
  const remainder = total % 4;
  let cursor = 0;
  for (let side = 0; side < 4; side += 1) {
    cursor += base + (side < remainder ? 1 : 0);
    if (index < cursor) return String.fromCharCode(65 + side);
  }
  return "D";
}

async function sha256(file) {
  return crypto.createHash("sha256").update(await fs.readFile(file)).digest("hex");
}

async function fileExists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

async function buildPreview(ticket) {
  const source = path.join(MIX_DIR, ticket.file);
  const stem = ticket.file.replace(/\.(?:png|jpe?g|webp)$/i, "");
  const outputName = `${stem}--preview.webp`;
  const output = path.join(PREVIEW_DIR, outputName);
  if (await fileExists(output)) return `./previews/${outputName}`;

  const temporary = path.join(os.tmpdir(), `wc-2026-preview-${process.pid}-${crypto.randomUUID()}.png`);
  try {
    await execFileAsync("ffmpeg", [
      "-y",
      "-loglevel", "error",
      "-i", source,
      "-vf", "crop=444:444:62:498,scale=320:320:flags=lanczos",
      "-frames:v", "1",
      temporary
    ]);
    await execFileAsync("cwebp", ["-quiet", "-q", "78", temporary, "-o", output]);
  } finally {
    await fs.rm(temporary, { force: true });
  }
  return `./previews/${outputName}`;
}

async function mapWithConcurrency(items, limit, mapper) {
  const results = new Array(items.length);
  let cursor = 0;
  async function worker() {
    while (cursor < items.length) {
      const index = cursor;
      cursor += 1;
      results[index] = await mapper(items[index], index);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}

async function main() {
  const mediaManifest = JSON.parse(await fs.readFile(SOURCE_MANIFEST, "utf8"));
  const tracks = [];

  for (const [albumKey, album] of Object.entries(mediaManifest.albums || {})) {
    for (const track of album.tracks || []) {
      tracks.push({
        ...track,
        albumKey,
        albumLabel: album.label,
        albumPage: `VOLHOLLA/${album.pageSlug}.html`,
        normalizedTitle: normalizeTitle(track.title)
      });
    }
  }

  const trackByRoute = new Map(tracks.map((track) => [track.songPage, track]));
  const files = (await fs.readdir(MIX_DIR)).filter((file) => /\.(?:png|jpe?g|webp)$/i.test(file));
  const tickets = await Promise.all(files.map(async (file) => {
    const absolute = path.join(MIX_DIR, file);
    const stats = await fs.stat(absolute);
    return {
      file,
      hash: await sha256(absolute),
      capturedAt: stats.birthtime.toISOString(),
      capturedAtMs: stats.birthtimeMs
    };
  }));

  tickets.sort((a, b) => a.capturedAtMs - b.capturedAtMs || a.file.localeCompare(b.file));

  const seenHashes = new Map();
  const uniqueTickets = [];
  const duplicatesSkipped = [];
  for (const ticket of tickets) {
    const original = seenHashes.get(ticket.hash);
    if (original) {
      duplicatesSkipped.push({ file: ticket.file, duplicateOf: original });
      continue;
    }
    seenHashes.set(ticket.hash, ticket.file);
    uniqueTickets.push(ticket);
  }

  const resolved = uniqueTickets.map((ticket) => {
    const override = ROUTE_OVERRIDES[ticket.file];
    const candidates = override
      ? [trackByRoute.get(override)].filter(Boolean)
      : tracks.filter((track) => track.normalizedTitle === normalizeTitle(titleFromTicket(ticket.file)));

    if (candidates.length !== 1) {
      const detail = candidates.map((track) => `${track.albumKey}:${track.title}`).join(", ") || "no matches";
      throw new Error(`Ticket ${ticket.file} must resolve to one track; found ${candidates.length} (${detail})`);
    }

    return { ticket, track: candidates[0] };
  });

  await fs.mkdir(PREVIEW_DIR, { recursive: true });
  const previews = await mapWithConcurrency(resolved, 4, ({ ticket }) => buildPreview(ticket));

  const mixTracks = resolved.map(({ ticket, track }, index) => {
    const audio = track.audio?.derivatives?.stream?.mp3
      || track.audio?.derivatives?.fallback?.mp3
      || track.audio?.source
      || track.source;

    return {
      index: index + 1,
      sourceIndex: track.index,
      side: sideFor(index, resolved.length),
      title: track.title,
      album: track.albumLabel,
      albumKey: track.albumKey,
      artwork: `./${ticket.file}`,
      preview: previews[index],
      audio: relativeFromMix(audio),
      sourceAudio: relativeFromMix(track.source),
      songPage: relativeFromMix(track.songPage),
      albumPage: relativeFromMix(track.albumPage),
      capturedAt: ticket.capturedAt
    };
  });

  const payload = {
    key: "wc2026finalmix",
    title: "WC 2026 FINAL MIX",
    subtitle: "121 selections / four sides / one continuous signal",
    sequence: "Ticket export order, July 17, 2026",
    trackCount: mixTracks.length,
    albumCount: new Set(mixTracks.map((track) => track.albumKey)).size,
    duplicatesSkipped,
    tracks: mixTracks
  };

  const serialized = JSON.stringify(payload, null, 2)
    .replace(/\u2028/g, "\\u2028")
    .replace(/\u2029/g, "\\u2029");
  await fs.writeFile(OUTPUT, `window.WC_2026_FINAL_MIX = ${serialized};\n`);

  process.stdout.write(`Built WC 2026 FINAL MIX manifest with ${mixTracks.length} tracks from ${payload.albumCount} albums.\n`);
  process.stdout.write(`Built or reused ${previews.length} isolated ticket previews.\n`);
  if (duplicatesSkipped.length) {
    process.stdout.write(`Skipped ${duplicatesSkipped.length} byte-identical duplicate ticket.\n`);
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
