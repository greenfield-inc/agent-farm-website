---
title: Get started
description: Install Agent Farm from npm, initialize your profiles, and launch your first native coding session.
---

# Get started

## Prerequisites

- macOS or Linux.
- Node.js 22.15 or later.
- Claude Code or Codex installed and authenticated.

Use a repository you are comfortable giving your agent access to. Current launches enable Claude’s `--dangerously-skip-permissions` or Codex’s `--yolo` by default. See [launch permissions](/docs/troubleshooting#launch-permissions) for details.

## Install and launch

```sh
npm install -g @greenfieldco/agent-farm
agent-farm init
agent-farm run greenfield/orchestrator
```

`agent-farm init` checks prerequisites and installs the default `greenfield` profiles and skills. Run the third command from your project folder: `greenfield/orchestrator` is the recommended first agent to try.

Upgrade later with `npm install -g @greenfieldco/agent-farm@latest`. To build from source or contribute, see the [Agent Farm repository](https://github.com/dcouple/agent-farm).

Next, [learn how profiles select agents](/docs/profiles) or [connect project tools](/docs/workspaces).

Source: [Installation and entry points](https://github.com/dcouple/agent-farm/blob/main/README.md).
