<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-task.yaml | Source SHA-256: a2c1902bf126c0d7ef534fb4895b8ac69e9ff3465f69dbb371eb7ec909049865 | -->
# T4H Task Lifecycle

Platform: `claude-code`  
Canonical workflow: `t4h-task`  
Contract version: `1.4.0`

## Parameters

- `task_request` (required): Bounded task to execute.
- `idempotency_key` (optional): Stable key preventing duplicate task execution.

## Required stages

- None

## Operating instruction

Execute the bounded task: {{ task_request }}. Derive or record an idempotency key and check prior receipts. Use CREATE → CLAIM → EXECUTE → VERIFY → COMPLETE. Record task identifier and owner. Renew ownership only while progress is observable. Retry transient failures within the declared budget. On exhaustion record FAILED or BLOCKED, recovery owner and next executable action. Do not claim completion without checking actual result. Emit the structured result and receipt contracts.

## Execution contract

- Maximum turns: 75
- Timeout: 600 seconds
- Maximum retries: 2
- Backoff: [2, 10]
- Recovery: `release_claim_and_record_failure`
- Required outputs: task-id, owner, completion-status, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
