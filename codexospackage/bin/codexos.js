#!/usr/bin/env node

const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");

const REPO_URL = "https://github.com/rotsl/codex-os.git";
const DEFAULT_REPO = path.join(os.homedir(), ".codex", "codex-os");

function usage() {
  console.log(`codexospackage v0.0.1

Usage:
  codexos install [--repo <path>]
  codexos install-claude [--repo <path>]
  codexos ro <args...>
  codexos claude <args...>
  codexos doctor
  codexos help

Notes:
  - install clones ${REPO_URL} to ${DEFAULT_REPO} when needed.
  - install runs install.sh for Codex wiring.
  - install-claude runs installclaude.sh for Claude wiring.
  - ro proxies to ~/.local/bin/ro after install.
`);
}

function parseArg(flag, args) {
  const idx = args.indexOf(flag);
  if (idx === -1 || idx + 1 >= args.length) return null;
  return args[idx + 1];
}

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

function runResult(cmd, cmdArgs, opts = {}) {
  return spawnSync(cmd, cmdArgs, {
    stdio: "inherit",
    shell: false,
    ...opts,
  });
}

function runChecked(cmd, cmdArgs, opts = {}) {
  const res = runResult(cmd, cmdArgs, opts);
  if (res.error) fail(res.error.message);
  if ((res.status ?? 1) !== 0) process.exit(res.status ?? 1);
}

function ensureGit() {
  const res = spawnSync("git", ["--version"], { stdio: "ignore" });
  if ((res.status ?? 1) !== 0) {
    fail("git is required to clone Codex-OS. Install git and retry.");
  }
}

function ensureRepo(repoPath) {
  const installScript = path.join(repoPath, "install.sh");
  if (fs.existsSync(installScript)) return repoPath;

  ensureGit();
  fs.mkdirSync(path.dirname(repoPath), { recursive: true });
  runChecked("git", ["clone", "--depth", "1", REPO_URL, repoPath]);

  if (!fs.existsSync(installScript)) {
    fail(`install.sh not found after clone at: ${installScript}`);
  }

  return repoPath;
}

function resolveInstallRepo(args) {
  const explicit = parseArg("--repo", args);
  if (explicit) {
    const repo = path.resolve(explicit);
    const installScript = path.join(repo, "install.sh");
    if (!fs.existsSync(installScript)) {
      fail(`install.sh not found at: ${installScript}`);
    }
    return repo;
  }

  const cwdRepo = process.cwd();
  if (fs.existsSync(path.join(cwdRepo, "install.sh"))) {
    return cwdRepo;
  }

  return ensureRepo(DEFAULT_REPO);
}

const args = process.argv.slice(2);
const sub = args[0] || "help";

if (sub === "help" || sub === "--help" || sub === "-h") {
  usage();
  process.exit(0);
}

if (sub === "install") {
  const repo = resolveInstallRepo(args.slice(1));
  runChecked("bash", [path.join(repo, "install.sh")], { cwd: repo });
  process.exit(0);
}

if (sub === "install-claude") {
  const repo = resolveInstallRepo(args.slice(1));
  runChecked("bash", [path.join(repo, "installclaude.sh")], { cwd: repo });
  process.exit(0);
}

if (sub === "ro") {
  const roPath = path.join(os.homedir(), ".local", "bin", "ro");
  if (!fs.existsSync(roPath)) {
    fail("ro not found at ~/.local/bin/ro. Run: codexos install");
  }
  runChecked(roPath, args.slice(1));
  process.exit(0);
}

if (sub === "claude") {
  const roClaudePath = path.join(os.homedir(), ".local", "bin", "ro-claude");
  if (!fs.existsSync(roClaudePath)) {
    fail("ro-claude not found at ~/.local/bin/ro-claude. Run: codexos install-claude");
  }
  runChecked(roClaudePath, args.slice(1));
  process.exit(0);
}

if (sub === "doctor") {
  const roPath = path.join(os.homedir(), ".local", "bin", "ro");
  const roClaudePath = path.join(os.homedir(), ".local", "bin", "ro-claude");
  const codexPath = path.join(os.homedir(), ".local", "bin", "codex");
  const repoPath = fs.existsSync(path.join(DEFAULT_REPO, "install.sh")) ? DEFAULT_REPO : "missing";

  console.log(`repo: ${repoPath}`);
  console.log(`ro: ${fs.existsSync(roPath) ? roPath : "missing"}`);
  console.log(`ro-claude: ${fs.existsSync(roClaudePath) ? roClaudePath : "missing"}`);
  console.log(`codex shim: ${fs.existsSync(codexPath) ? codexPath : "missing"}`);
  process.exit(0);
}

fail(`Unknown command: ${sub}`);
