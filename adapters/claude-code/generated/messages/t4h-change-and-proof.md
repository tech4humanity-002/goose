<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-change-and-proof.yaml | Source SHA-256: 7557f777aef61f0df81055e667a8bbcfacf20c30d086be0ea1ae178323f55401 | -->
# T4H Change and Proof

Platform: `claude-code`  
Canonical workflow: `t4h-change-and-proof`  
Contract version: `1.3.0`

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
