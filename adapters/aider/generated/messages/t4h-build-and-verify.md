<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-build-and-verify.yaml | Source SHA-256: 669ef0bac73f522b83983beef1dec5449b1d15a91c590737ae3aebd005a521a0 | -->
# T4H Build and Verify

Platform: `aider`  
Canonical workflow: `t4h-build-and-verify`  
Contract version: `1.3.0`

## Parameters

- `request` (required): Development request.
- `idempotency_key` (optional): Stable key used to detect replay of the same requested change.

## Required stages

- `t4h-inspect`: Inspect repository and relevant implementation before editing.
- `t4h-test`: Run relevant tests and checks after implementation.
- `t4h-proof-check`: Prove the final outcome.

## Operating instruction

Complete this development request: {{ request }}.
Use inspect first, then implement the smallest correct change, then test, then proof.
Fix failures using the next known safe method. Preserve changed-file and verification evidence. Do not claim completion without proof.
Derive or record an idempotency key before mutation, check for an existing successful receipt, and do not repeat a completed side effect. Enforce the retry/timeout contract below. On exhausted retries, restore the pre-change state when safe and return a structured BLOCKED or DEGRADED result with recovery details.

## Execution contract

- Maximum turns: 100
- Timeout: 300 seconds
- Maximum retries: 2
- Backoff: [2, 10]
- Recovery: `restore_pre_change_state`
- Required outputs: changed-files, test-results, proof-status, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
