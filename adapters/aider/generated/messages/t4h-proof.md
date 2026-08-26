<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-proof.yaml | Source SHA-256: 11cdec956f8830b5ff3dd6937166052640ac3aebcb1d98431970927716227d3b | -->
# T4H Proof and Verification

Platform: `aider`  
Canonical workflow: `t4h-proof`  
Contract version: `1.3.0`

## Parameters

- `outcome` (required): Outcome that must be verified.

## Required stages

- None

## Operating instruction

Verify the actual outcome: {{ outcome }}. Use the narrowest live proof/health/evidence tools available. Distinguish evidence of execution from evidence of authorisation. Report PASS, WARN, BLOCKED or UNPROVEN with the evidence used.

## Execution contract

- Maximum turns: 75
- Timeout: 300 seconds
- Maximum retries: 0
- Backoff: []
- Recovery: `report_blocked`
- Required outputs: proof-status, evidence-list, structured-result

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
