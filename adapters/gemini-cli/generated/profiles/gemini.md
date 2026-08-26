<!-- GENERATED FILE — DO NOT EDIT | Source: contract/platforms/gemini.yaml | Source SHA-256: 362e6220b681665739ec98ee5074148a7d04cc3668ca4e619efabd490883caca | -->
# Google gemini platform profile

Adapter target: `gemini-cli`

Contract version: `1.4.0`

Replaceable model runtime for bounded inference; never the operating system or authority boundary.

## SDK and authentication

- Python package: `google-genai` (latest-compatible)
- Legacy packages prohibited for new work: `google-generativeai`
- Credential variable: `GEMINI_API_KEY`

## Capability bindings

- `text-generation`: native
- `multimodal-analysis`: native
- `structured-output`: native-with-contract-validation
- `tool-calling`: native-request-governed-execution
- `streaming`: native
- `embeddings`: native-model-dependent
- `batch-processing`: native-model-and-tier-dependent

## Runtime boundaries

- Python or the owning worker controls Google Drive access; the model receives only the bounded file batch supplied to it.
- Model selection is configuration resolved against the current official model catalogue; no model name is a contract default.
- Validate requested modalities, file count, file size, context and output bounds before submission.
- Tool calls are proposals and receive no authority beyond the contract tool router, approval policy and scope registry.
- Validate structured output against the requested schema before accepting it.
- Record provider, resolved model, request correlation, latency, token usage when returned, retries, terminal status and redactions.
- Cost estimates are advisory and must use current provider pricing; never encode static prices in the contract.

## Mutable provider facts

Checked: `2026-08-26`

Review due: `2026-09-02`

Refresh before use: `true`

- `sdk`: https://ai.google.dev/gemini-api/docs/libraries
- `migration`: https://ai.google.dev/gemini-api/docs/migrate
- `models`: https://ai.google.dev/gemini-api/docs/models
- `rate_limits`: https://ai.google.dev/gemini-api/docs/rate-limits
- `pricing`: https://ai.google.dev/gemini-api/docs/pricing
- `gemini_cli`: https://github.com/google-gemini/gemini-cli/blob/main/docs/index.md
