#!/usr/bin/env node
import path from "node:path";
import { parseArgs, runCommand } from "./lib/pipeline-utils.mjs";
import { readVolhollaAlbums } from "./lib/volholla-albums.mjs";

const ROOT = process.cwd();
const args = parseArgs(process.argv.slice(2));
const FORCE = Boolean(args.force);
const VERBOSE = Boolean(args.verbose);
const IMAGES_ONLY = Boolean(args.imagesOnly);
const AUDIO_ONLY = Boolean(args.audioOnly);

function unique(list) {
  return Array.from(new Set(list.filter(Boolean)));
}

async function buildImages(matches) {
  if (!matches.length) return;
  const commandArgs = [
    path.join("scripts", "build-image-derivatives.mjs"),
    ...matches.flatMap((match) => ["--match", match])
  ];
  if (FORCE) commandArgs.push("--force");
  if (VERBOSE) commandArgs.push("--verbose");
  await runCommand("node", commandArgs, { cwd: ROOT, stdio: "inherit" });
}

async function buildAudio(matches) {
  if (!matches.length) return;
  const commandArgs = [
    path.join("scripts", "build-audio-derivatives.mjs"),
    ...matches.flatMap((match) => ["--match", match])
  ];
  if (FORCE) commandArgs.push("--force");
  if (VERBOSE) commandArgs.push("--verbose");
  await runCommand("node", commandArgs, { cwd: ROOT, stdio: "inherit" });
}

async function main() {
  const albums = await readVolhollaAlbums(ROOT);
  const coverMatches = unique(albums.flatMap((album) => [album.coverSource, album.defaultTrackArtSource]));
  const firstTrackMatches = unique(albums.map((album) => album.tracks?.[0]?.source || ""));

  if (!AUDIO_ONLY) await buildImages(coverMatches);
  if (!IMAGES_ONLY) await buildAudio(firstTrackMatches);

  process.stdout.write(`Priority derivatives complete for ${coverMatches.length} image sources and ${firstTrackMatches.length} first-track sources.\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

