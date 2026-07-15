#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { basenameNoExt, ensureDir, fileExists, humanBytes, matchesFilters, parseArgs, readJsonIfExists, runCommand, statSafe, stripLeadingDotSlash, toPosixPath, walkFiles } from "./lib/pipeline-utils.mjs";

const ROOT = process.cwd();
const args = parseArgs(process.argv.slice(2));
const OUT_ROOT = path.resolve(ROOT, String(args.out || "MEDIA_DERIVATIVES/audio"));
const LIMIT = Number(args.limit || 0) || 0;
const FORCE = Boolean(args.force);
const DRY_RUN = Boolean(args.dryRun);
const VERBOSE = Boolean(args.verbose);
const FILTERS = (Array.isArray(args.match) ? args.match : args.match ? [args.match] : []).map(String);

const AUDIO_EXTENSIONS = [".mp3", ".ogg", ".wav", ".m4a", ".aac"];
const PROFILES = {
  stream: {
    suffix: "stream",
    codec: "libmp3lame",
    bitrate: "128k"
  },
  fallback: {
    suffix: "fallback",
    codec: "libmp3lame",
    bitrate: "64k"
  },
  preview: {
    suffix: "preview",
    codec: "libmp3lame",
    bitrate: "48k",
    previewSeconds: 30
  }
};

async function probeAudio(file) {
  const { stdout } = await runCommand("ffprobe", [
    "-v", "error",
    "-show_entries", "format=duration,bit_rate",
    "-of", "json",
    file
  ]);
  const data = JSON.parse(stdout || "{}");
  const format = data.format || {};
  return {
    durationSeconds: Number(format.duration || 0),
    bitRate: Number(format.bit_rate || 0)
  };
}

function audioFilter(profile, durationSeconds) {
  if (profile.previewSeconds) {
    const previewLength = Math.max(5, Math.min(profile.previewSeconds, Math.floor(durationSeconds || profile.previewSeconds)));
    const fadeStart = Math.max(0, previewLength - 3);
    return {
      args: ["-t", String(previewLength), "-af", `loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st=${fadeStart}:d=3`],
      previewLength
    };
  }
  return {
    args: ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"],
    previewLength: null
  };
}

async function encodeAudio(sourceFile, outFile, profile, durationSeconds) {
  const filter = audioFilter(profile, durationSeconds);
  await runCommand("ffmpeg", [
    "-y",
    "-loglevel", "error",
    "-i", sourceFile,
    "-map", "0:a:0",
    "-vn",
    "-sn",
    "-dn",
    "-ac", "2",
    "-ar", "44100",
    ...filter.args,
    "-c:a", profile.codec,
    "-b:a", profile.bitrate,
    outFile
  ]);
  return filter.previewLength;
}

async function buildDerivatives(sourceFile, probe) {
  const relative = stripLeadingDotSlash(toPosixPath(path.relative(ROOT, sourceFile)));
  const dirname = path.join(OUT_ROOT, path.dirname(relative));
  const stem = basenameNoExt(relative);
  await ensureDir(dirname);

  const entry = {
    source: relative,
    durationSeconds: probe.durationSeconds,
    sourceBitRate: probe.bitRate,
    derivatives: {}
  };

  for (const [profileName, profile] of Object.entries(PROFILES)) {
    const outFile = path.join(dirname, `${stem}--${profile.suffix}.mp3`);
    const relOut = stripLeadingDotSlash(toPosixPath(path.relative(ROOT, outFile)));

    if (DRY_RUN) {
      entry.derivatives[profileName] = { mp3: relOut, skipped: "dry-run" };
      continue;
    }

    let previewSeconds = null;
    if (FORCE || !await fileExists(outFile)) {
      previewSeconds = await encodeAudio(sourceFile, outFile, profile, probe.durationSeconds);
    }

    const stats = await statSafe(outFile);
    entry.derivatives[profileName] = {
      mp3: relOut,
      bytes: stats?.size || 0,
      bitrate: profile.bitrate,
      previewSeconds
    };
  }

  return entry;
}

async function main() {
  const files = (await walkFiles(ROOT, {
    extensions: AUDIO_EXTENSIONS,
    excludeDirNames: new Set([".git", "node_modules", "MEDIA_DERIVATIVES"])
  }))
    .map((file) => stripLeadingDotSlash(toPosixPath(path.relative(ROOT, file))))
    .filter((file) => matchesFilters(file, FILTERS))
    .slice(0, LIMIT || undefined)
    .map((file) => path.join(ROOT, file));

  const existingManifest = !DRY_RUN && (FILTERS.length || LIMIT)
    ? await readJsonIfExists(path.join(OUT_ROOT, "manifest.json"))
    : null;

  const manifest = {
    generatedAt: new Date().toISOString(),
    outputRoot: stripLeadingDotSlash(toPosixPath(path.relative(ROOT, OUT_ROOT))),
    profiles: PROFILES,
    items: existingManifest?.items ? { ...existingManifest.items } : {}
  };

  let built = 0;
  for (const file of files) {
    const relative = stripLeadingDotSlash(toPosixPath(path.relative(ROOT, file)));
    try {
      const probe = await probeAudio(file);
      const entry = await buildDerivatives(file, probe);
      manifest.items[relative] = entry;
      built += 1;
      if (VERBOSE || DRY_RUN) {
        const stream = entry.derivatives.stream;
        process.stdout.write(`[audio] ${relative} -> ${humanBytes(stream?.bytes || 0)} stream mp3\n`);
      }
    } catch (error) {
      manifest.items[relative] = { source: relative, error: String(error.message || error) };
      process.stderr.write(`[audio] failed: ${relative}\n${error.stderr || error.message || error}\n`);
    }
  }

  await ensureDir(OUT_ROOT);
  if (!DRY_RUN) {
    await fs.writeFile(path.join(OUT_ROOT, "manifest.json"), JSON.stringify(manifest, null, 2));
  }

  process.stdout.write(`${DRY_RUN ? "Planned" : "Built"} audio derivatives for ${built} files.\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
