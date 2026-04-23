# Codex-OS

语言: [English](./README.md) | [中文](./README.zh-CN.md) | [Français](./README.fr.md) | [Deutsch](./README.de.md)

本文件是 `README.md` 的中文说明版。英文版仍然是规范和最新的主文档。

## 项目简介

Codex-OS 是一套面向 Codex 的“操作层”，由 Markdown 规则、内存文件和一个轻量运行器组成。
它不是用来替代 Codex，而是帮助你在不同仓库中以一致、可重复、可控的方式使用 Codex。

它解决的问题：
- 每个仓库都重复维护 prompt、记忆、执行习惯
- 上下文容易漂移
- 多项目切换时工作方式不一致

Codex-OS 通过统一的规则、技能、内存和 CLI 包装器，让这些行为稳定下来。

Claude Code 也受支持，通过并行的 `ro-claude` 运行器和独立的 Claude 指令层接入。

## 托管前端

- 在线站点: https://rotsl.github.io/codex-os/
- 前端源码: `docs/index.html`
- GitHub Pages 工作流: `.github/workflows/pages.yml`
- 输出渲染支持：
  - 纯文本
  - 代码
  - Markdown
  - JSON
  - 表格类内容

## 安装前的重要说明

先备份你当前的 Codex 目录：

```bash
cp -R ~/.codex ~/.codex.backup.$(date +%Y%m%d%H%M%S)
```

原因：
- 安装脚本会连接全局加载器与系统路径
- 备份可以让你快速回滚

## 安装

在仓库根目录执行：

```bash
./install.sh
```

如果要安装 Claude Code 支持：

```bash
./installclaude.sh
```

安装器支持两种范围：
- `this repo only`
- `systemwide`

### 仅当前仓库

- 只在当前仓库中使用
- 不修改 `~/.codex`、`~/.claude` 或 PATH
- 可直接运行 `./ro` 或 `./ro-claude`

### 全局安装

- 在修改全局配置前显示备份和恢复命令
- 只有输入 `Accept` 才继续
- 输入 `Decline` 会取消
- 支持非交互模式：

```bash
CODEXOS_INSTALL_SCOPE=systemwide CODEXOS_INSTALL_ACCEPT=Accept ./install.sh
```

## 安装后会连接哪些内容

### `install.sh`

- `~/.codex/system -> <this repo>`
- `~/.local/bin/ro -> ~/.codex/system/ro`
- 若能找到 Codex 二进制，则创建 `~/.local/bin/codex` shim
- `~/.codex/AGENTS.md -> ~/.codex/system/AGENTS.md`
- 创建缺失的：
  - `~/.codex/config.toml`
  - `~/.codex/system/plugins/`
  - `~/.codex/system/plugin-registry.json`

### `installclaude.sh`

- `~/.codex/system -> <this repo>`
- `~/.local/bin/ro-claude -> ~/.codex/system/ro-claude`
- `~/.claude/CLAUDE.md -> ~/.codex/system/claude/CLAUDE.md`
- `~/.claude/agents/*.md -> ~/.codex/system/claude/agents/*.md`

## Codex 与 Claude Code 的接入方式

### Codex

1. Codex 从 `~/.codex/AGENTS.md` 加载全局指令
2. 该文件链接到本仓库的 `AGENTS.md`
3. 各项目内的 `AGENTS.md` 可以扩展本地规则
4. `ro` 基于 `codex exec` 增加：
   - 项目上下文
   - 内存处理
   - 插件加载
   - 有界重试
5. 新仓库首次运行 `ro` 时会自动创建：
   - `AGENTS.md`
   - `memory/context.md`
   - `memory/decisions.md`

### Claude Code

1. Claude Code 加载 `~/.claude/CLAUDE.md`
2. 该文件链接到 `claude/CLAUDE.md`
3. 子代理来自 `claude/agents/*.md`
4. `ro-claude` 基于 `claude -p` 运行
5. 支持两种内存模式：
   - `auto`
   - `deterministic`

Claude CLI 前提：
- 本地 Claude CLI 已登录
- 否则会失败并提示 `/login`

## 常见用法

### 终端

```bash
ro "build login API"
ro build "task"
ro write "task"
ro analyze "task"
```

Claude：

```bash
ro-claude --memory-mode auto "task"
ro-claude --memory-mode deterministic "task"
```

### Python 虚拟环境中

```bash
source .venv/bin/activate
ro "run tests and fix failures"
```

如有需要，可指定 Codex 二进制路径：

```bash
export RO_CODEX_BIN="/absolute/path/to/codex"
```

### VS Code 聊天框

你可以直接写任务：

```text
refactor auth middleware
```

也可以写命令风格文本：

```text
ro "check dataset counts"
```

在聊天模式中，这会被解释为任务意图，而不是 shell 命令。

## npm 包

仓库中包含 `codexospackage/`。

全局安装：

```bash
npm install -g ./codexospackage
```

安装后可使用：

```bash
codexos install
codexos install-claude
codexos ro "build login API"
codexos claude --memory-mode auto "review this project"
codexos doctor
```

可选参数：
- `CODEXOS_SKIP_POSTINSTALL=1`
- `codexos install --repo /absolute/path/to/codex-os`

## 插件

```bash
ro plugin install sql-helper
ro plugin install https://github.com/user/repo
ro plugin list
ro plugin remove sql-helper
```

全局注册表：
- `~/.codex/system/plugin-registry.json`

插件约定：
- 每个插件都必须提供 `SKILL.md`
- 插件只提供指导，不直接执行远程仓库中的运行时代码

## 内存与隔离

默认项目本地文件：
- `.ro_history.json`
- `memory/context.md`
- `memory/decisions.md`

Claude 内存模式：
- `auto`
- `deterministic`

可选共享上下文：
- `--context`：按需读取其他本地仓库摘要
- `--share`：写入隔离的 `memory/shared_<hash>.md`
- 默认不会自动合并跨项目内存

可选全局内存：
- `~/.codex/global_memory.md`

## 仓库结构

### 根目录

- `AGENTS.md`: 主调度器与模式约定
- `ro`: Codex CLI 包装器
- `ro-claude`: Claude CLI 包装器
- `install.sh`: Codex 全局安装脚本
- `installclaude.sh`: Claude 安装脚本
- `docs/index.html`: GitHub Pages 前端
- `.github/workflows/pages.yml`: Pages 部署工作流
- `plugin-registry.json`: 默认插件注册表

### 目录说明

- `agents/`: 规划、架构、构建、审查、写作代理
- `skills/`: reasoning、structure、completion、notai
- `rules/`: workflow、token-efficiency、memory
- `contexts/`: autoload、loading、repository-classification、summarization
- `memory/`: `context.md`、`decisions.md`、`shared_<hash>.md`
- `plugins/`: 可选插件技能
- `claude/`: Claude 指令与子代理

## 回滚

```bash
rm -f ~/.codex/system
rm -f ~/.codex/AGENTS.md
rm -f ~/.local/bin/ro
rm -f ~/.local/bin/codex
mv ~/.codex.backup.<timestamp> ~/.codex
```

## 版本记录

### v0.0.2 — 2026-03-24
- `codexospackage` 升级到 `v0.0.2`
- 新增 Claude Code 支持
- 新增安装范围选择与备份确认
- 更新前端文案

### v0.0.1 — 2026-03-18
- 初始公开版本
- 新增 Codex-OS 编排层、代理、技能、规则、上下文与内存系统
- 新增 `ro` CLI 与 `codexospackage`

## 实用建议

- 将规则放在 `rules/`，技能放在 `skills/`
- 保持内存简短且最新
- 仅在确有需要时使用 `--context` 和 `--share`
- `ro-claude` 是围绕 `claude -p` 的轻量包装器

---

<div align="center">
  <h3>Codex-OS</h3>
  <p><code>autoload • memory • plugins • repeatable workflows</code></p>
  <p>
    <a href="https://rotsl.github.io/codex-os/">Live Site</a>
    ·
    <a href="https://github.com/rotsl/codex-os">GitHub</a>
    ·
    <a href="https://www.npmjs.com/package/codexospackage">npm</a>
  </p>
  <sub>为终端、VS Code 与 Codex 聊天而构建。</sub>
</div>
