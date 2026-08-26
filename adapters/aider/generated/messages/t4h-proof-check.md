<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-proof-check.yaml | Source SHA-256: 621732c2ad4579dad9a5a78c266a9c6d52bb2636aee997c72a2a8c5a3f5083d2 | -->
# T4H Proof Check

Platform: `aider`  
Canonical workflow: `t4h-proof-check`  
Contract version: `1.3.0`

## Parameters

- `outcome` (required): Outcome that must be proven.

## Required stages

- None

## Operating instruction

Prove the outcome: {{ outcome }}.
Separate execution evidence, result evidence and authorisation evidence. Return PASS, WARN, BLOCKED or UNPROVEN with the evidence used.

## Execution contract

- Maximum turns: 30
- Timeout: 300 seconds
- Maximum retries: 0
- Backoff: []
- Recovery: `report_blocked`
- Required outputs: proof-status, structured-result

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
