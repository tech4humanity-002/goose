# T4H Goose Operating Layer

Initial executable/documentation layer for T4H on Goose. It is deliberately usable before every dependency is complete.

## State

- Goose: verify locally on the Mac.
- T4H recipes/playbooks/policies/registries: included.
- bad-mcp: 87 callable tools in the supplied inventory.
- bad-mcp authoritative scope registry: PARTIAL during control-plane migration.
- bad-mcp transport: intentionally not guessed.
- Jobs/tasks/workers/agents/locks: represented as first-class lifecycles and recipes; live calls still require verification.

## Install

```bash
bash scripts/install.sh
```

The installer checks Goose, copies the package to `~/.config/goose/t4h-goose`, installs `~/bin/t4h-goose`, preserves the canonical Goose config, and adds `.goosehints` only when safe. The wrapper can inject a live bad-mcp endpoint with `T4H_BAD_MCP_URI` or a stdio command with `T4H_BAD_MCP_CMD`; neither is guessed by the package.

Configure provider credentials with `goose configure`.

## Verify

```bash
~/.config/goose/t4h-goose/scripts/doctor.sh
```

## Recipes

```bash
export GOOSE_RECIPE_PATH="$HOME/.config/goose/t4h-goose/recipes"
goose recipe list --verbose
goose recipe validate "$HOME/.config/goose/t4h-goose/recipes/core/t4h-start.yaml"
goose run --recipe "$HOME/.config/goose/t4h-goose/recipes/core/t4h-start.yaml"
```

Included workflows: start/orient, build-and-verify, jobs, tasks, agent team, workers, and proof/verification.

## T4H architecture rule

Goose is the orchestration/client layer. bad-mcp is the governed action plane. The standard 200-tool catalogue is reference/gap material, not a reason to load 200 tools into every context. Do not create duplicate direct GitHub/Drive/AWS MCP integrations when bad-mcp already provides the capability.

## First live verification sequence

1. `goose --version`
2. `goose info -v`
3. `goose recipe list --verbose`
4. validate every T4H recipe
5. run `t4h-start`
6. connect the actual bad-mcp transport
7. compare live discovery to the 87-tool inventory
8. test jobs/tasks/workers/agents/locks
9. verify approval behaviour
10. run proof/health checks

For live bad-mcp transport, set exactly one of `T4H_BAD_MCP_URI` (Streamable HTTP) or `T4H_BAD_MCP_CMD` (stdio command) only after reading the actual Mac installation.

This package is **READY WITH WARNINGS** until those environment-dependent checks pass.
