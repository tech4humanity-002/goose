<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-worker.yaml | Source SHA-256: 7e483ee956f7c6efb3c053d3bd179b3f9ca99fca13556b935a2b80b2b6a8f2dd | -->
# T4H Worker Lifecycle

Platform: `gemini-cli`  
Canonical workflow: `t4h-worker`  
Contract version: `1.4.0`

## Parameters

- `worker_request` (required): Worker/schedule operation requested.
- `idempotency_key` (optional): Stable key for schedule or trigger deduplication.

## Required stages

- None

## Operating instruction

Handle the worker request: {{ worker_request }}. Inspect existing schedules, status and receipts first. Derive or record an idempotency key. Creating or triggering persistent/background execution is an approved action and must not be performed silently. Record schedule/worker identifiers, lease owner, heartbeat expectation and resulting state. Suppress duplicate schedules/triggers. On timeout or stale heartbeat attempt safe cancellation or quarantine and name a recovery owner. Emit structured result and receipt records.

## Execution contract

- Maximum turns: 75
- Timeout: 900 seconds
- Maximum retries: 2
- Backoff: [5, 30]
- Recovery: `cancel_or_quarantine`
- Required outputs: worker-status, schedule-id, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
