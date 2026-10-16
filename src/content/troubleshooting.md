---
title: Troubleshooting
description: Diagnose command discovery, configuration, MCP authentication, global ownership conflicts, and native launch behavior.
---

# Troubleshooting

Start with the built-in diagnostic and the profile you intend to run:

```sh
agent-farm doctor
agent-farm inspect planner
```

## Find the command

Check the installation path and native prerequisites:

```sh
command -v agent-farm
node --version
command -v claude
command -v codex
```

Use Node.js 22.15 or later. If `command -v agent-farm` prints nothing, install it with `npm install -g @greenfieldco/agent-farm` and make sure npm’s global `bin` directory, `$(npm prefix -g)/bin`, is on your `PATH`. Install and authenticate the native harness selected by your profile.

## Resolve a profile or skill

```sh
agent-farm profiles list
agent-farm inspect planner
```

Check that the profile names an agent file and that each selected skill directory contains `SKILL.md`. Every child binding needs an explicit `native` or `process` mode.

After updating the CLI checkout, use `agent-farm plugin install` to apply the bundled configuration. Resolve any reported local-edit conflicts deliberately.

## Reconnect a workspace tool

```sh
agent-farm inspect planner --workspace my-project
agent-farm mcp login project-tools --workspace my-project --harness claude
```

Replace `project-tools` with your connection name. Complete the native browser sign-in, then launch with the workspace selected. Check the harness’s MCP view for connectivity.

Claude and Codex have separate credentials. Endpoint or connection-name changes, revoked access, and provider policies can require a new sign-in. Local stdio services use their own login flow.

## Refresh global configuration

Start a fresh native session after changing a global workspace or skill install. Project settings can take precedence over global settings.

Agent Farm records global workspace ownership under `~/.local/state/agent-farm/user-workspaces/state.json`. Keep that registry through unloading. Changed managed entries need reconciliation before unload can complete.

For skill file additions, removals, or metadata renames, unload all profiles sharing that skill and load them again.

## Launch permissions

Current launches use these native flags by default, including headless runs and generated process children:

| Harness | Flag | Effect |
| --- | --- | --- |
| Claude Code | `--dangerously-skip-permissions` | Runs with permission checks bypassed. |
| Codex | `--yolo` | Runs with approval prompts and sandboxing bypassed. |

Choose the repository and task scope accordingly. Agent Farm generates these launch settings per session; native global permission settings stay as configured.

## Generated files and parallel work

Bundles live in `.agent-farm/generated/` in the target repository. Keep bundles needed by running sessions and exclude the directory from Git.

Bundles share filesystem access, credentials, and native global configuration. Use separate worktrees for independent code changes.

## Gather a useful report

Include the command, selected harness, operating system, configuration error, and relevant diagnostic output. Redact credentials and private endpoints before sharing.

[Open an Agent Farm issue](https://github.com/dcouple/agent-farm/issues/new).

Sources: [Operational notes](https://github.com/dcouple/agent-farm/blob/main/docs/operations.md) and [configuration reference](https://github.com/dcouple/agent-farm/blob/main/CONFIGURATION.md).
