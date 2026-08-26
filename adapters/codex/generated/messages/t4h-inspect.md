<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-inspect.yaml | Source SHA-256: c9d381bc4b052127cc566da1cc3a9f6cc13e0b399dcdb57db56e72efb987b255 | -->
# T4H Inspect Workspace

Platform: `codex`  
Canonical workflow: `t4h-inspect`  
Contract version: `1.3.0`

## Parameters

- `objective` (required): Objective being investigated.

## Required stages

- None

## Operating instruction

Inspect the workspace for the objective: {{ objective }}.
Read relevant instructions first. Identify the repository, changed files, relevant implementation, tests and verification mechanisms. Do not mutate anything.

## Execution contract

- Maximum turns: 30
- Timeout: 300 seconds
- Maximum retries: 0
- Backoff: []
- Recovery: `report_blocked`
- Required outputs: inspection-result, structured-result

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
