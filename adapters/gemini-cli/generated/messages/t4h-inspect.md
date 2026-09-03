<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-inspect.yaml | Source SHA-256: 2f0c320806500cb1c833a0bce4dd6e8997a702b974f8904bb4f7cd4058429af7 | -->
# T4H Inspect Workspace

Platform: `gemini-cli`  
Canonical workflow: `t4h-inspect`  
Contract version: `1.4.0`

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
