<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-proof-check.yaml | Source SHA-256: eb6a6249926d661c696c18c6fc32bbd586e02cbf2e5b0c958af5edefce556e58 | -->
# T4H Proof Check

Platform: `codex`  
Canonical workflow: `t4h-proof-check`  
Contract version: `1.4.0`

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
