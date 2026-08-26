<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-test.yaml | Source SHA-256: 8b6e5a062d3d86e1345c9ffc7e212049b895d66c010eff0d925036ca1388fe05 | -->
# T4H Test and Verify

Platform: `codex`  
Canonical workflow: `t4h-test`  
Contract version: `1.3.0`

## Parameters

- `objective` (required): Change or outcome to verify.

## Required stages

- None

## Operating instruction

Verify: {{ objective }}.
Run the narrowest relevant tests/checks available. If a check fails, diagnose and retry using the next known safe method. Report commands/checks, results and remaining blockers. Never claim success without evidence.

## Execution contract

- Maximum turns: 40
- Timeout: 300 seconds
- Maximum retries: 0
- Backoff: []
- Recovery: `report_blocked`
- Required outputs: test-results, structured-result

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
