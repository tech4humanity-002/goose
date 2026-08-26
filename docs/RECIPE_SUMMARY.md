# T4H Goose Recipe Catalogue — v1.2.0

Machine-readable metadata lives in `registry/recipe-index.yaml`. Every recipe is version-aligned, indexed and covered by deterministic local contract execution.

| Recipe | Function | Runtime integrity enhancement |
|---|---|---|
| `t4h-start` | Orient and report readiness | Structured readiness state |
| `t4h-change-and-proof` | Govern a generic change | Idempotency, timeout, retry and rollback |
| `t4h-release` | Build, release and prove | Replay suppression and recovery target |
| `t4h-lock` | Protect shared mutable state | Ownership, lease, release and quarantine |
| `t4h-rollback` | Restore trusted state | Evidence preservation and recovery proof |
| `t4h-build-and-verify` | Inspect, implement, test and prove | Fully mapped subrecipe parameters |
| `t4h-job` | Govern asynchronous execution | Bounded polling, timeout and recovery |
| `t4h-task` | Govern bounded owned work | Verify-before-complete and failure receipt |
| `t4h-agent-team` | Delegate specialist work | Duplicate suppression, budget and reaping contract |
| `t4h-worker` | Govern background work | Lease, heartbeat and stale-worker recovery |
| `t4h-proof` | Verify actual outcome | Structured evidence state |
| `t4h-recipe-review-worker` | Review recipe integrity | Registry and subrecipe validation |
| `t4h-inspect` | Reusable inspection | Required `objective` contract |
| `t4h-test` | Reusable verification | Required `objective` contract |
| `t4h-proof-check` | Reusable final proof | Required `outcome` contract |

## Result and receipt contract

Mutating and asynchronous recipes derive or record an idempotency key, use bounded retry and timeout rules, preserve attempt evidence, identify recovery behaviour and emit outputs compatible with `schemas/result.schema.json` and `schemas/receipt.schema.json`.

## Validation

`python3 scripts/validate_runtime_integrity.py` reconciles all 15 recipes across the filesystem, catalogue and index; checks versions and placeholders; resolves every subrecipe parameter binding; and performs deterministic local dry-run execution. This does not replace live Goose and bad-mcp verification.

Every recipe remains due for review on 2026-09-25. Review dates must not be silently extended.
