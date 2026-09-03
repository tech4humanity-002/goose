<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-proof.yaml | Source SHA-256: 3bd5177842c516d6eb66593b40d704fd0cf855a41ae1039b63649907f01dd692 | -->
# T4H Proof and Verification

Platform: `codex`  
Canonical workflow: `t4h-proof`  
Contract version: `1.4.0`

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
