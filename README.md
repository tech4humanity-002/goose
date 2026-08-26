# T4H Agent Operating Contract

Vendor-, model-, agent-, runtime- and tool-neutral operating contract for governed AI execution.

This repository is no longer architected around Goose recipes. `contract/` is the only source of operating truth. Goose, Aider, Codex, Claude Code and Gemini CLI are generated adapters.

## Source-of-truth hierarchy

1. `contract/manifest.yaml`
2. `contract/workflows/`
3. Contract policies, lifecycles, runtime rules and schemas
4. `compiler/compile_adapters.py`
5. Generated platform adapters
6. Runtime receipts and telemetry

Never edit files below `adapters/*/generated/`. CI rejects generated drift.

## One contract change, every platform

```bash
# Edit the canonical contract only
$EDITOR contract/workflows/t4h-build-and-verify.yaml

# Regenerate every adapter
python3 compiler/compile_adapters.py

# Prove contract and adapter conformance
python3 conformance/validate_contract.py
python3 -m unittest discover -s tests -v
```

The compiler currently produces 80 deterministic files: 15 workflows across five adapters plus one manifest per adapter.

## Adapter entrypoints

```bash
adapters/aider/bin/t4h-aider --workflow t4h-build-and-verify --param request="Fix the issue" --dry-run
adapters/codex/bin/t4h-codex --workflow t4h-build-and-verify --param request="Fix the issue" --dry-run
adapters/claude-code/bin/t4h-claude --workflow t4h-build-and-verify --param request="Fix the issue" --dry-run
adapters/gemini-cli/bin/t4h-gemini --workflow t4h-build-and-verify --param request="Fix the issue" --dry-run
adapters/goose/bin/t4h-goose --workflow t4h-build-and-verify --param request="Fix the issue" --dry-run
```

Remove `--dry-run` only when the selected runtime is installed and authorised. Adapter declarations explicitly distinguish native, emulated and unsupported capabilities.

## Contract scope

- Completion and evidence rules
- Approval and authority boundaries
- Tasks, jobs, workers, agents, locks, proof and rollback lifecycles
- Idempotency, retry, timeout, recovery and quarantine
- Structured result and receipt schemas
- Capability requirements and declared platform gaps
- Deterministic compilation and conformance validation

Historical v1.2.0 Goose validation evidence remains in `receipts/`; it is evidence, not current source.
