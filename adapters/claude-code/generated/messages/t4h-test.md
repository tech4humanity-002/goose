<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-test.yaml | Source SHA-256: 5919c1b2621c6458487449252676d460f1c05c62cc49b4c4a90c240bd3f1a95b | -->
# T4H Test and Verify

Platform: `claude-code`  
Canonical workflow: `t4h-test`  
Contract version: `1.4.0`

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
