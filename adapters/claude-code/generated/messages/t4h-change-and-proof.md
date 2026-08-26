<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-change-and-proof.yaml | Source SHA-256: 30db6c8dea12b60055440599bcadf8b38386b84116d8c0b3b376e34e7b1c3f0a | -->
# T4H Change and Proof

Platform: `claude-code`  
Canonical workflow: `t4h-change-and-proof`  
Contract version: `1.4.0`

## Parameters

- `request` (required): Requested change.
- `idempotency_key` (optional): Stable replay-protection key.

## Required stages

- `t4h-inspect`: Inspect before mutation.
- `t4h-proof-check`: Verify the final outcome.

## Operating instruction

Execute the requested change: {{ request }}.
Inspect first. Make only necessary changes. Verify after mutation. Require approval for external, infrastructure, destructive, secret, deployment or financial effects. Finish only with evidence.
Before mutation derive or record an idempotency key, check prior receipts, capture recoverable pre-change state and suppress duplicate completed actions. On failure, retry within the declared budget, recover the pre-change state when safe, and emit the structured result contract.

## Execution contract

- Maximum turns: 100
- Timeout: 600 seconds
- Maximum retries: 2
- Backoff: [2, 10]
- Recovery: `invoke_t4h_rollback`
- Required outputs: change-result, proof-status, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
