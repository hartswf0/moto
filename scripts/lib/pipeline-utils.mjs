import fs from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";

export function parseArgs(argv = []) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      out._.push(token);
      continue;
    }
    const eq = token.indexOf("=");
    const rawKey = token.slice(2, eq >= 0 ? eq : undefined);
    const next = eq >= 0 ? token.slice(eq + 1) : argv[i + 1];
    const key = rawKey.replace(/-([a-z])/g, (_, ch) => ch.toUpperCase());
    let value = true;
    if (eq >= 0) {
      value = next;
    } else if (next && !next.startsWith("--")) {
      value = next;
      i += 1;
    }
    if (key in out) {
      out[key] = Array.isArray(out[key]) ? [...out[key], value] : [out[key], value];
    } else {
      out[key] = value;
    }
  }
  return out;
}

export function toPosixPath(value) {
  return String(value || "").split(path.sep).join("/");
}

export function stripLeadingDotSlash(value) {
  return toPosixPath(String(value || "").replace(/^[.][/\\]/, ""));
}

export function basenameNoExt(file) {
  return path.basename(file, path.extname(file));
}

export function humanBytes(bytes) {
  const value = Number(bytes) || 0;
  if (value < 1024) return `${value} B`;
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KB`;
  if (value < 1024 * 1024 * 1024) return `${(value / (1024 * 1024)).toFixed(1)} MB`;
  return `${(value / (1024 * 1024 * 1024)).toFixed(2)} GB`;
}

export async function fileExists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

export async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

export async function readJsonIfExists(file) {
  try {
    const text = await fs.readFile(file, "utf8");
    return JSON.parse(text);
  } catch {
    return null;
  }
}

export async function walkFiles(rootDir, options = {}) {
  const extensions = new Set((options.extensions || []).map((ext) => ext.toLowerCase()));
  const excludeDirNames = new Set(options.excludeDirNames || []);
  const results = [];

  async function visit(dir) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name.startsWith(".") && entry.name !== ".nojekyll") continue;
      const abs = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (excludeDirNames.has(entry.name)) continue;
        await visit(abs);
        continue;
      }
      if (!entry.isFile()) continue;
      if (extensions.size && !extensions.has(path.extname(entry.name).toLowerCase())) continue;
      results.push(abs);
    }
  }

  await visit(rootDir);
  return results.sort((a, b) => a.localeCompare(b));
}

export async function statSafe(file) {
  try {
    return await fs.stat(file);
  } catch {
    return null;
  }
}

export function matchesFilters(relPath, filters = []) {
  if (!filters.length) return true;
  const lower = relPath.toLowerCase();
  return filters.some((filter) => lower.includes(String(filter).toLowerCase()));
}

export async function runCommand(command, args, options = {}) {
  const { cwd, stdio = "pipe" } = options;
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { cwd, stdio: stdio === "inherit" ? "inherit" : ["ignore", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";

    if (stdio !== "inherit") {
      child.stdout.on("data", (chunk) => { stdout += chunk; });
      child.stderr.on("data", (chunk) => { stderr += chunk; });
    }

    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) {
        resolve({ stdout, stderr });
        return;
      }
      const error = new Error(`${command} ${args.join(" ")} exited with code ${code}`);
      error.stdout = stdout;
      error.stderr = stderr;
      reject(error);
    });
  });
}

