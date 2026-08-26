<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-rollback.yaml | Source SHA-256: 66195699af4e224f8797e9f509056af909a82c675c9f7c06b7b1d619ed261d83 | -->
# T4H Rollback and Recovery

Platform: `codex`  
Canonical workflow: `t4h-rollback`  
Contract version: `1.3.0`

## Parameters

- `failed_change` (required): Failed or unsafe change requiring recovery.
- `recovery_target` (required): Proven revision, snapshot or state to restore.
- `idempotency_key` (optional): Stable rollback replay-protection key.

## Required stages

- `t4h-inspect`: Confirm the failure and recovery target before mutation.
- `t4h-proof-check`: Verify the restored state.

## Operating instruction

Recover from {{ failed_change }} by restoring {{ recovery_target }}. Verify that the target exists and is trusted. Record or derive an idempotency key and check for a prior successful rollback. Require approval when recovery has external, destructive or infrastructure effects. Preserve failure evidence. Apply the narrowest reversible recovery, verify service and data state, and emit structured result and receipt records. If recovery cannot be proven, quarantine the affected resource and return BLOCKED with a named owner and next action.

## Execution contract

- Maximum turns: 100
- Timeout: 900 seconds
- Maximum retries: 1
- Backoff: [10]
- Recovery: `quarantine_and_escalate`
- Required outputs: recovery-status, proof-status, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
