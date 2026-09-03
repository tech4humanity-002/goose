<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-lock.yaml | Source SHA-256: 95c2f45fd50502e1c0418d3a8ab45407f38b0e1ad2e1aff8b3a35be5a78ade98 | -->
# T4H Lock Lifecycle

Platform: `codex`  
Canonical workflow: `t4h-lock`  
Contract version: `1.4.0`

## Parameters

- `resource` (required): Canonical shared-resource identifier.
- `owner` (required): Actor responsible for the lock.
- `idempotency_key` (optional): Stable acquisition replay-protection key.

## Required stages

- None

## Operating instruction

Protect {{ resource }} for {{ owner }}. Inspect current lock state first. Derive or record an idempotency key. Acquire only when absent, expired or already owned by the same idempotency key. Record lock_id, owner, acquired_at, lease expiry and correlation_id. Verify ownership before mutation and renew only while progress is observable. Release in a finally-equivalent path. If release fails, quarantine the resource, name a recovery owner and emit BLOCKED. Never steal a live lock. Emit structured result and receipt records.

## Execution contract

- Maximum turns: 50
- Timeout: 120 seconds
- Maximum retries: 2
- Backoff: [2, 10]
- Recovery: `quarantine_and_escalate_stale_lock`
- Required outputs: lock-id, ownership-status, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
