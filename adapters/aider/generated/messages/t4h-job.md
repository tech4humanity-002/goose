<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-job.yaml | Source SHA-256: fea1d5abbd025b470f53a3e9bd7137d5bfd185cf9e87e813d39c8348d44da719 | -->
# T4H Job Lifecycle

Platform: `aider`  
Canonical workflow: `t4h-job`  
Contract version: `1.3.0`

## Parameters

- `job_request` (required): Description of the asynchronous job to perform.
- `idempotency_key` (optional): Stable key preventing duplicate job creation.

## Required stages

- None

## Operating instruction

Use the T4H job lifecycle for: {{ job_request }}. 1. Define the job precisely and derive or record an idempotency key. 2. Check prior receipts before creating a job. 3. Create only when no completed or active equivalent exists. 4. Record job_id. 5. Poll with bounded backoff until terminal state, timeout or explicit blocked condition. 6. Retrieve and verify the result. 7. On timeout attempt safe cancellation when available and record the recovery owner. If unavailable, report UNPROVEN/BLOCKED; do not simulate success. Emit the structured result and receipt contracts.

## Execution contract

- Maximum turns: 75
- Timeout: 900 seconds
- Maximum retries: 2
- Backoff: [5, 15, 30]
- Recovery: `cancel_or_quarantine`
- Required outputs: job-id, terminal-status, result, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
