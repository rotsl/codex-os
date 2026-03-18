#!/usr/bin/env node

const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");

const REPO_URL = "https://github.com/rotsl/codex-os.git";
const TARGET = path.join(os.homedir(), ".codex", "codex-os");

function run(cmd, args, opts = {}) {
  const res = spawnSync(cmd, args, { stdio: "inherit", shell: false, ...opts });
  if (res.error) throw res.error;
  if ((res.status ?? 1) !== 0) process.exit(res.status ?? 1);
}

function ensureGit() {
  const res = spawnSync("git", ["--version"], { stdio: "ignore" });
  if ((res.status ?? 1) !== 0) {
    console.error("[codexospackage] git is required for postinstall bootstrap.");
    process.exit(1);
  }
}

if (process.env.CODEXOS_SKIP_POSTINSTALL === "1") {
  console.log("[codexospackage] postinstall skipped via CODEXOS_SKIP_POSTINSTALL=1");
  process.exit(0);
}

try {
  const installScript = path.join(TARGET, "install.sh");
  if (!fs.existsSync(installScript)) {
    ensureGit();
    fs.mkdirSync(path.dirname(TARGET), { recursive: true });
    run("git", ["clone", "--depth", "1", REPO_URL, TARGET]);
  }

  run("bash", [path.join(TARGET, "install.sh")], { cwd: TARGET });
  console.log("[codexospackage] bootstrap complete");
} catch (err) {
  console.error(`[codexospackage] postinstall failed: ${err.message}`);
  process.exit(1);
}
