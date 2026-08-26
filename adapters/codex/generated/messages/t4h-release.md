<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-release.yaml | Source SHA-256: f68b0a1563bd709a6786f0e07bba1f3b9d3be72d9902cee3c8d84e6e01b64e1c | -->
# T4H Release

Platform: `codex`  
Canonical workflow: `t4h-release`  
Contract version: `1.4.0`

## Parameters

- `release_request` (required): Release request.
- `idempotency_key` (optional): Stable release replay-protection key.

## Required stages

- `t4h-build-and-verify`: Build and verify the requested release change.
- `t4h-proof-check`: Prove the release outcome.

## Operating instruction

Execute a governed T4H release for: {{ release_request }}.
Build and verify first. Require explicit approval before deployment or other external effects. Complete final proof before reporting release success.
Record the release idempotency key and pre-release revision. Suppress a duplicate release already proven successful. On deployment failure invoke the rollback recipe with the recorded revision, verify recovery, and emit structured result and receipt records.

## Execution contract

- Maximum turns: 120
- Timeout: 1200 seconds
- Maximum retries: 1
- Backoff: [10]
- Recovery: `invoke_t4h_rollback`
- Required outputs: release-result, proof-status, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
