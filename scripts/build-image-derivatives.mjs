#!/usr/bin/env node
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { basenameNoExt, ensureDir, fileExists, humanBytes, matchesFilters, parseArgs, readJsonIfExists, runCommand, statSafe, stripLeadingDotSlash, toPosixPath, walkFiles } from "./lib/pipeline-utils.mjs";

const ROOT = process.cwd();
const args = parseArgs(process.argv.slice(2));
const OUT_ROOT = path.resolve(ROOT, String(args.out || "MEDIA_DERIVATIVES/images"));
const LIMIT = Number(args.limit || 0) || 0;
const FORCE = Boolean(args.force);
const DRY_RUN = Boolean(args.dryRun);
const VERBOSE = Boolean(args.verbose);
const FILTERS = (Array.isArray(args.match) ? args.match : args.match ? [args.match] : []).map(String);

const IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".svg"];
const PROFILES = {
  thumb: {
    maxEdge: 640,
    webpTargetBytes: 80 * 1024,
    jpegTargetBytes: 120 * 1024,
    startWebpQuality: 78,
    minWebpQuality: 48,
    startJpegQScale: 4,
    maxJpegQScale: 14,
    dimensionAttempts: 4
  },
  cover: {
    maxEdge: 1600,
    webpTargetBytes: 380 * 1024,
    jpegTargetBytes: 520 * 1024,
    startWebpQuality: 80,
    minWebpQuality: 50,
    startJpegQScale: 4,
    maxJpegQScale: 12,
    dimensionAttempts: 4
  },
  share: {
    fixedCanvas: true,
    width: 1200,
    height: 630,
    background: "0x111114",
    webpTargetBytes: 260 * 1024,
    jpegTargetBytes: 340 * 1024,
    startWebpQuality: 76,
    minWebpQuality: 46,
    startJpegQScale: 5,
    maxJpegQScale: 14,
    dimensionAttempts: 1
  }
};

function buildFilter(profile, edge) {
  if (profile.fixedCanvas) {
    return [
      `scale=w='min(iw,${profile.width})':h='min(ih,${profile.height})':force_original_aspect_ratio=decrease`,
      `pad=${profile.width}:${profile.height}:(ow-iw)/2:(oh-ih)/2:${profile.background}`
    ].join(",");
  }
  return `scale=w='min(iw,${edge})':h='min(ih,${edge})':force_original_aspect_ratio=decrease`;
}

async function renderTempPng(sourceFile, tempFile, filter) {
  await runCommand("ffmpeg", [
    "-y",
    "-loglevel", "error",
    "-i", sourceFile,
    "-vf", filter,
    "-frames:v", "1",
    tempFile
  ]);
}

async function encodeWebp(tempFile, outFile, quality) {
  await runCommand("cwebp", [
    "-quiet",
    "-q", String(quality),
    tempFile,
    "-o", outFile
  ]);
}

async function encodeJpeg(tempFile, outFile, qScale) {
  await runCommand("ffmpeg", [
    "-y",
    "-loglevel", "error",
    "-i", tempFile,
    "-frames:v", "1",
    "-q:v", String(qScale),
    outFile
  ]);
}

async function findBestWebp(sourceFile, outFile, profile) {
  let edge = profile.maxEdge || profile.width;
  let best = null;
  for (let dimensionAttempt = 0; dimensionAttempt < profile.dimensionAttempts; dimensionAttempt += 1) {
    const tempFile = path.join(os.tmpdir(), `moto-image-${process.pid}-${Date.now()}-${Math.random().toString(16).slice(2)}.png`);
    await renderTempPng(sourceFile, tempFile, buildFilter(profile, edge));
    for (let quality = profile.startWebpQuality; quality >= profile.minWebpQuality; quality -= 5) {
      await encodeWebp(tempFile, outFile, quality);
      const stats = await statSafe(outFile);
      if (!stats) continue;
      best = { size: stats.size, quality, edge };
      if (stats.size <= profile.webpTargetBytes) {
        await fs.rm(tempFile, { force: true });
        return best;
      }
    }
    await fs.rm(tempFile, { force: true });
    if (profile.fixedCanvas) break;
    edge = Math.max(320, Math.round(edge * 0.9));
  }
  return best;
}

async function findBestJpeg(sourceFile, outFile, profile) {
  let edge = profile.maxEdge || profile.width;
  let best = null;
  for (let dimensionAttempt = 0; dimensionAttempt < profile.dimensionAttempts; dimensionAttempt += 1) {
    const tempFile = path.join(os.tmpdir(), `moto-image-${process.pid}-${Date.now()}-${Math.random().toString(16).slice(2)}.png`);
    await renderTempPng(sourceFile, tempFile, buildFilter(profile, edge));
    for (let qScale = profile.startJpegQScale; qScale <= profile.maxJpegQScale; qScale += 2) {
      await encodeJpeg(tempFile, outFile, qScale);
      const stats = await statSafe(outFile);
      if (!stats) continue;
      best = { size: stats.size, qScale, edge };
      if (stats.size <= profile.jpegTargetBytes) {
        await fs.rm(tempFile, { force: true });
        return best;
      }
    }
    await fs.rm(tempFile, { force: true });
    if (profile.fixedCanvas) break;
    edge = Math.max(320, Math.round(edge * 0.9));
  }
  return best;
}

async function buildDerivatives(sourceFile) {
  const relative = stripLeadingDotSlash(toPosixPath(path.relative(ROOT, sourceFile)));
  const dirname = path.join(OUT_ROOT, path.dirname(relative));
  const stem = basenameNoExt(relative);
  await ensureDir(dirname);

  const entry = { source: relative, derivatives: {} };
  for (const [profileName, profile] of Object.entries(PROFILES)) {
    const webpFile = path.join(dirname, `${stem}--${profileName}.webp`);
    const jpegFile = path.join(dirname, `${stem}--${profileName}.jpg`);
    const relWebp = stripLeadingDotSlash(toPosixPath(path.relative(ROOT, webpFile)));
    const relJpeg = stripLeadingDotSlash(toPosixPath(path.relative(ROOT, jpegFile)));

    if (DRY_RUN) {
      entry.derivatives[profileName] = {
        webp: relWebp,
        jpeg: relJpeg,
        skipped: "dry-run"
      };
      continue;
    }

    const alreadyBuilt = !FORCE && await fileExists(webpFile) && await fileExists(jpegFile);
    let webpInfo = null;
    let jpegInfo = null;

    if (!alreadyBuilt || FORCE) {
      webpInfo = await findBestWebp(sourceFile, webpFile, profile);
      jpegInfo = await findBestJpeg(sourceFile, jpegFile, profile);
    }

    const webpStats = await statSafe(webpFile);
    const jpegStats = await statSafe(jpegFile);
    entry.derivatives[profileName] = {
      webp: relWebp,
      jpeg: relJpeg,
      webpBytes: webpStats?.size || 0,
      jpegBytes: jpegStats?.size || 0,
      webpQuality: webpInfo?.quality || null,
      jpegQScale: jpegInfo?.qScale || null
    };
  }
  return entry;
}

async function main() {
  const files = (await walkFiles(ROOT, {
    extensions: IMAGE_EXTENSIONS,
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
      const entry = await buildDerivatives(file);
      manifest.items[relative] = entry;
      built += 1;
      if (VERBOSE || DRY_RUN) {
        const thumb = entry.derivatives.thumb;
        process.stdout.write(`[image] ${relative} -> ${humanBytes(thumb?.webpBytes || 0)} thumb webp\n`);
      }
    } catch (error) {
      manifest.items[relative] = { source: relative, error: String(error.message || error) };
      process.stderr.write(`[image] failed: ${relative}\n${error.stderr || error.message || error}\n`);
    }
  }

  await ensureDir(OUT_ROOT);
  if (!DRY_RUN) {
    await fs.writeFile(path.join(OUT_ROOT, "manifest.json"), JSON.stringify(manifest, null, 2));
  }

  process.stdout.write(`${DRY_RUN ? "Planned" : "Built"} image derivatives for ${built} files.\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
