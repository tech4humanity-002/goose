<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-model-inference.yaml | Source SHA-256: 0b9c442af3b3b1480dd81d0f5c372b3c89f89a6ba2032c217fca59436ce83a57 | -->
# T4H Governed Model Inference

Platform: `codex`  
Canonical workflow: `t4h-model-inference`  
Contract version: `1.4.0`

## Parameters

- `request` (required): Bounded inference objective and acceptance criteria.
- `platform_profile` (required): Contract platform profile used to resolve the provider implementation.
- `input_manifest` (required): Manifest of bounded inputs and their provenance; use none when the request is text-only.
- `output_schema` (required): Schema identifier or explicit human-readable output contract.
- `idempotency_key` (optional): Stable key preventing duplicate externally consequential inference.

## Required stages

- `t4h-inspect`: Resolve current provider facts and validate bounded inputs before submission.
- `t4h-proof-check`: Validate output and receipt evidence before accepting the result.

## Operating instruction

Execute {{ request }} using {{ platform_profile }} with inputs {{ input_manifest }} and output contract {{ output_schema }}.
Resolve the platform through contract/platforms and verify mutable provider facts before use. Validate data classification,
modality, provenance, file count, file size, context and output bounds before submission. Derive or record an idempotency key
and check prior receipts. Treat model tool calls as proposals: route them through the contract allowlist, scope and approval
controls and record separate tool receipts. Apply bounded timeout and retry only transient failures. Validate the final output
against the requested schema. Record provider, resolved model, latency, usage returned by the provider, retries, evidence,
redactions and terminal status. On exhausted retries, cancel or quarantine outstanding work and return BLOCKED or UNPROVEN;
never substitute an unverified model response for a proven result.

## Execution contract

- Maximum turns: 75
- Timeout: 300 seconds
- Maximum retries: 2
- Backoff: [2, 10]
- Recovery: `cancel_or_quarantine_inference`
- Required outputs: resolved-model, schema-valid-result, usage-telemetry, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
