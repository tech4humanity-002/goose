# T4H Goose Recipe Catalogue

Canonical human-readable summary. Machine-readable metadata lives in `registry/recipe-index.yaml`.

| Recipe | What it does | Resources | Expected outputs | Known limitations | Review |
|---|---|---|---|---|---|
| `t4h-start` | Orients Goose and reports actual readiness | Workspace, config, bad-mcp if configured | Readiness, blockers, warnings | Callable bad-mcp tools are not proof of grants | 2026-09-25 |
| `t4h-build-and-verify` | Inspect → build → test → proof | Filesystem, Git, developer, tests | Changed files, test results, proof | External actions require approval; live tools may vary | 2026-09-25 |
| `t4h-change-and-proof` | Govern a generic change and prove it | Workspace, Git, action tools | Change result + proof | Cannot prove unavailable systems | 2026-09-25 |
| `t4h-job` | Run/inspect asynchronous job lifecycle | bad-mcp job tools | Job ID, status, result, verification | Cancellation/progress not proven | 2026-09-25 |
| `t4h-task` | Create → claim → execute → complete | bad-mcp task tools | Task ID, owner, completion | Failure/retry/dependency not exposed | 2026-09-25 |
| `t4h-agent-team` | Delegate and reconcile specialist agents | Summon + bad-mcp agents | Agent IDs, messages, consensus | Termination/budget need validation | 2026-09-25 |
| `t4h-worker` | Govern scheduled/background work | bad-mcp worker tools | Worker/schedule state | Cancellation/heartbeat not proven | 2026-09-25 |
| `t4h-proof` | Verify actual outcome | Proof tools | PASS/WARN/BLOCKED/UNPROVEN | Depends on available evidence | 2026-09-25 |
| `t4h-release` | Build → approval → proof release | Build/proof + deployment tools | Release result + proof | Deployment requires approval | 2026-09-25 |
| `t4h-recipe-review-worker` | Review due recipes and validate subrecipes | Goose CLI, registry, filesystem, worker plane | Review report, overdue list | Does not silently change recipes | 2026-09-25 |

## Composition

`sub_recipes` are used for reusable stages. Goose's CLI supports subrecipes and the CLI can retrieve complete GitHub recipe directories, including referenced subrecipes. Desktop web-registry deeplinks have historically had a separate subrecipe-import limitation, so T4H uses the CLI/Git path as the canonical bulk installation route.

## Review policy

Every recipe carries a `review_due` date. The review worker identifies due/overdue recipes, validates them and reports findings. It must not extend a review date simply to clear an overdue state.
